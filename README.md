# Sistema Inteligente de Recomendación Alimenticia — NutriPerú

Proyecto académico del curso **Inteligencia Artificial: Principios y Técnicas (ISIA-108)** — UPAO 2026-10.

Sistema de recomendación nutricional personalizada que genera planes alimenticios diarios con ingredientes peruanos, basado en el perfil del usuario y aplicando técnicas de IA.

---

## Aplicación web (NutriPerú)

Plataforma web construida sobre el sistema del notebook, que permite al usuario interactuar con el motor de IA desde el navegador.

### Tecnologías usadas

| Capa | Tecnología |
|---|---|
| Backend | FastAPI + Python |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| ORM | SQLAlchemy |
| Frontend | HTML + CSS + JavaScript (vanilla) |
| Despliegue | Render.com |

### Páginas de la app

| Ruta | Descripción |
|---|---|
| `/` | Login con nombre de usuario |
| `/perfil` | Formulario de datos personales con preview de IMC y calorías |
| `/ingredientes` | Selección de ingredientes disponibles por el usuario |
| `/plan` | Plan nutricional del día (anillo calórico + 4 comidas) |
| `/cuenta` | Menú de cuenta del usuario |

### Lo que hace la app

- Registra el perfil del usuario (edad, sexo, peso, talla, actividad, objetivo)
- Permite seleccionar qué ingredientes tiene disponibles
- Genera un plan diario de 4 comidas (desayuno, almuerzo, cena, snack) con gramos exactos y unidades amigables
- Almacena el plan en base de datos para no regenerarlo si el usuario vuelve el mismo día
- Cambia el plan automáticamente cada día, evitando repetir ingredientes de días anteriores

---

## Qué se trasladó del notebook al código

| Celda notebook | Componente en el código |
|---|---|
| Celda 4 — Mifflin-St Jeor | `ai_engine.py` → `calcular_tmb()`, `calcular_get()`, `calcular_targets_diarios()` |
| Celda 5 — Distribución de macros | `ai_engine.py` → `REGLAS_OBJETIVO`, `DISTRIBUCION_POR_OBJETIVO` |
| Celda 6 — PerfilUsuario | `ai_engine.py` → clase `PerfilUsuario` |
| Celda 7 — Sistema Experto (reglas A1–A4, B1–B3) | `ai_engine.py` → clase `SistemaExperto` |
| Celda 8 — K-Means | Los clusters validan las categorías del dataset CSV; no corre en tiempo real |
| Celda 9 — Optimización PuLP | `ai_engine.py` → `_construir_y_resolver()`, `optimizar_comida()` |
| Celda 10 — Orquestador | `ai_engine.py` → clase `OrquestadorDiario` |
| Celda 14 — LLM (nombres de platillos) | `ai_engine.py` → `generar_nombre_platillo()` con plantillas locales como fallback |

> Las celdas de análisis (EDA, Cross-Validation K-Means, Suite VV&E) son exclusivas del notebook y no se ejecutan en la app.

---

## Arquitectura del sistema

| Capa | Técnica |
|---|---|
| 1 | Cálculo nutricional (Mifflin-St Jeor) |
| 2 | Sistema Experto (reglas de salud y contexto) |
| 3 | K-Means Clustering (precomputado en dataset) |
| 4 | Optimización con PuLP (programación lineal entera) |
| 5 | Generador de nombres de platillos |

---

## Estructura del proyecto

```
proyecto_ia/
├── data/
│   └── ingredientes_dataset.csv   # 81 ingredientes curados
├── docs/
│   ├── bitacora_decisiones.md
│   └── catalogo_reglas.md
├── notebooks/
│   └── demo.ipynb                 # Notebook para ejecutar en Colab
├── webapp/
│   ├── main.py                    # Endpoints FastAPI
│   ├── ai_engine.py               # Motor de IA trasladado del notebook
│   ├── models.py                  # Modelos de base de datos
│   ├── database.py                # Conexión DB
│   └── static/                   # Frontend HTML/CSS/JS
├── requirements.txt
├── render.yaml                    # Configuración de despliegue
└── README.md
```

---

## Ejecución local

```bash
pip install -r webapp/requirements.txt
uvicorn webapp.main:app --reload --port 8001
```

Abrir: `http://localhost:8001`

---

## Equipo y contexto

Universidad Privada Antenor Orrego — Facultad de Ingeniería
Programa: Ingeniería de Sistemas e Inteligencia Artificial — Semestre 2026-10
