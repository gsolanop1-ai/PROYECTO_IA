import json
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from .models import Usuario, PlanDiario
from . import ai_engine
from .ai_engine import PerfilUsuario, generar_plan_completo

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriPerú", version="1.0")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ── HTML routes ───────────────────────────────────────────────
@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/perfil")
def perfil_page():
    return FileResponse(STATIC_DIR / "perfil.html")

@app.get("/plan")
def plan_page():
    return FileResponse(STATIC_DIR / "plan.html")

@app.get("/ingredientes")
def ingredientes_page():
    return FileResponse(STATIC_DIR / "ingredientes.html")


# ── Schemas ───────────────────────────────────────────────────
class EntrarRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=30)

class PerfilRequest(BaseModel):
    edad:            int   = Field(..., ge=10, le=100)
    sexo:            str   = Field(..., pattern="^[MF]$")
    peso_kg:         float = Field(..., ge=30, le=250)
    altura_cm:       float = Field(..., ge=100, le=230)
    nivel_actividad: str
    objetivo:        str

class IngredientesRequest(BaseModel):
    ingredientes: list[str]


# ── Helpers ───────────────────────────────────────────────────
def get_usuario_or_404(db: Session, username: str) -> Usuario:
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        raise HTTPException(404, "Usuario no encontrado")
    return user

def usuario_a_perfil(user: Usuario) -> PerfilUsuario:
    return PerfilUsuario(
        edad=user.edad, sexo=user.sexo,
        peso_kg=user.peso_kg, altura_cm=user.altura_cm,
        nivel_actividad=user.nivel_actividad, objetivo=user.objetivo
    )

def ingredientes_ultimos_dias(db: Session, usuario_id: int, dias: int = 2) -> set:
    """Retorna nombres de ingredientes usados en los últimos `dias` días (excluye snack)."""
    desde = date.today() - timedelta(days=dias)
    planes = db.query(PlanDiario).filter(
        PlanDiario.usuario_id == usuario_id,
        PlanDiario.fecha >= desde,
        PlanDiario.fecha < date.today()
    ).all()
    usados = set()
    for p in planes:
        data = json.loads(p.plan_json)
        for comida in data.get('comidas', []):
            if comida.get('comida') != 'snack':
                for ing in comida.get('plan', []):
                    usados.add(ing['nombre'])
    return usados


# ── API endpoints ─────────────────────────────────────────────
@app.post("/api/usuario/entrar")
def entrar(req: EntrarRequest, db: Session = Depends(get_db)):
    """Entra con username. Crea el usuario si no existe."""
    username = req.username.strip().lower()
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user:
        user = Usuario(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {
        "username":      user.username,
        "tiene_perfil":  user.tiene_perfil(),
        "nuevo":         not user.tiene_perfil(),
    }


@app.get("/api/usuario/{username}/perfil")
def get_perfil(username: str, db: Session = Depends(get_db)):
    user = get_usuario_or_404(db, username)
    return {
        "username":       user.username,
        "edad":           user.edad,
        "sexo":           user.sexo,
        "peso_kg":        user.peso_kg,
        "altura_cm":      user.altura_cm,
        "nivel_actividad": user.nivel_actividad,
        "objetivo":       user.objetivo,
        "tiene_perfil":   user.tiene_perfil(),
    }


@app.post("/api/usuario/{username}/perfil")
def guardar_perfil(username: str, req: PerfilRequest, db: Session = Depends(get_db)):
    user = get_usuario_or_404(db, username)
    user.edad            = req.edad
    user.sexo            = req.sexo
    user.peso_kg         = req.peso_kg
    user.altura_cm       = req.altura_cm
    user.nivel_actividad = req.nivel_actividad
    user.objetivo        = req.objetivo
    db.commit()
    return {"ok": True, "username": user.username}


@app.get("/api/ingredientes")
def get_todos_ingredientes():
    """Retorna todos los ingredientes del dataset agrupados por categoría."""
    grupos: dict = {}
    for _, row in ai_engine.df_ingredientes.iterrows():
        cat = row['categoria']
        if cat not in grupos:
            grupos[cat] = []
        grupos[cat].append({'nombre': row['nombre'], 'categoria': cat})
    return grupos


@app.get("/api/usuario/{username}/ingredientes")
def get_ingredientes_usuario(username: str, db: Session = Depends(get_db)):
    """Ingredientes disponibles del usuario. null en DB = todos."""
    user = get_usuario_or_404(db, username)
    if user.ingredientes_json:
        return {"ingredientes": json.loads(user.ingredientes_json), "personalizado": True}
    return {"ingredientes": ai_engine.df_ingredientes['nombre'].tolist(), "personalizado": False}


@app.post("/api/usuario/{username}/ingredientes")
def guardar_ingredientes(username: str, req: IngredientesRequest,
                         db: Session = Depends(get_db)):
    """Guarda la selección y borra el plan de hoy para regenerarlo."""
    user = get_usuario_or_404(db, username)
    todos = set(ai_engine.df_ingredientes['nombre'].tolist())
    seleccion = [n for n in req.ingredientes if n in todos]
    if len(seleccion) == len(todos):
        user.ingredientes_json = None       # usa todos → no guardar lista
    else:
        user.ingredientes_json = json.dumps(seleccion, ensure_ascii=False)
    # Borrar plan de hoy para forzar regeneración con nuevos ingredientes
    plan_db = db.query(PlanDiario).filter(
        PlanDiario.usuario_id == user.id,
        PlanDiario.fecha == date.today()
    ).first()
    if plan_db:
        db.delete(plan_db)
    db.commit()
    return {"ok": True, "total_seleccionados": len(seleccion)}


@app.get("/api/usuario/{username}/plan")
def get_plan(username: str, db: Session = Depends(get_db)):
    """Devuelve el plan del día. Lo genera si no existe todavía."""
    user = get_usuario_or_404(db, username)
    if not user.tiene_perfil():
        raise HTTPException(400, "El usuario no tiene perfil configurado")

    hoy = date.today()

    # ¿Ya existe plan para hoy?
    plan_db = db.query(PlanDiario).filter(
        PlanDiario.usuario_id == user.id,
        PlanDiario.fecha == hoy
    ).first()

    if plan_db:
        return json.loads(plan_db.plan_json)

    # Generar plan nuevo con variedad entre días
    perfil            = usuario_a_perfil(user)
    ingredientes_ant  = ingredientes_ultimos_dias(db, user.id, dias=2)
    disponibles       = json.loads(user.ingredientes_json) if user.ingredientes_json else None
    plan              = generar_plan_completo(perfil, ingredientes_ant or None, disponibles)

    # Guardar en DB
    nuevo = PlanDiario(
        usuario_id=user.id,
        fecha=hoy,
        plan_json=json.dumps(plan, ensure_ascii=False)
    )
    db.add(nuevo)
    db.commit()
    return plan


@app.delete("/api/usuario/{username}/plan/hoy")
def regenerar_plan(username: str, db: Session = Depends(get_db)):
    """Elimina el plan de hoy para forzar regeneración (útil en desarrollo)."""
    user = get_usuario_or_404(db, username)
    plan_db = db.query(PlanDiario).filter(
        PlanDiario.usuario_id == user.id,
        PlanDiario.fecha == date.today()
    ).first()
    if plan_db:
        db.delete(plan_db)
        db.commit()
    return {"ok": True}
