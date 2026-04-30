# Estado del Proyecto

**Última actualización:** 

## Avance: Versión 1.0 — Sistema base completado

### Implementado y validado

- [x] Módulo de cálculo nutricional 
  - Mifflin-St Jeor para TMB
  - Factores de actividad para GET
  - Reparto de macros según objetivo
  - Distribución calórica entre 4 comidas
  - Regla F1 de seguridad calórica

- [x] Módulo de perfil de usuario 
  - Validación robusta de inputs
  - Diseño modular para futuras fuentes (visión, voz)

- [x] Sistema Experto con 18 reglas 
  - Grupo A: Filtrado por dieta (preparado para v2.0)
  - Grupo B: Reparto de macros
  - Grupo C: Estructura por comida
  - Grupo D: Reglas de salud (D1, D3, D4, D5)
  - Grupo E: Contexto del momento
  - Grupo F: Seguridad calórica

- [x] Optimizador con PuLP 
  - Programación lineal mixta entera
  - Restricciones de macros con tolerancia
  - Estructura obligatoria por comida
  - Snack contextual según objetivo
  - Desayuno sin verduras
  - Límite de ingredientes anti-buffet
  - Fallback automático ante infactibilidad

### Validación realizada

- 4 perfiles de prueba ejecutados con éxito
- Desviación calórica promedio: 1.7%
- 16 comidas generadas sin infactibilidades
- Casos cubiertos:
  - Hombre joven, ganar músculo
  - Mujer adulta, perder grasa
  - Adulto mayor, mantener peso (activa reglas D4/D5)
  - Mujer joven activa, ganar músculo

### Decisiones técnicas tomadas

Ver `docs/bitacora_decisiones.md` para detalles. Resumen:

- Dataset propio de 81 ingredientes peruanos curados
- Solo dieta omnívora en v1.0 (vegetariano/vegano para v2.0)
- Macros perder grasa: 40/35/25 (no 40/30/30)
- Distribución de comidas variable por objetivo
- Snack contextual con configuraciones diferenciadas
- Mínimo de seguridad: 1500 kcal hombre / 1200 kcal mujer

## Pendiente para versiones siguientes

### Versión 1.1 — Completar capas RA2

- [ ] **Celda 8 — K-Means clustering** (Capa 3, RA2.1, Semana 9)
  - Agrupar ingredientes por perfil nutricional
  - Visualización de clusters

- [ ] **Celda 10 — LLM para nombrar platillos** (Capa 5, RA2.2, Semana 14)
  - Integración con Gemini API o Claude API
  - Generación de nombres creativos
  - Sugerencias de preparación con condimentos peruanos

- [ ] **Celda 11 — Orquestador del plan diario**
  - Memoria entre comidas (evitar repetición de ingredientes)
  - Generación coordinada de las 4 comidas

### Versión 1.2 — Visualización y entrega

- [ ] **Celda 12 — Visualizaciones del plan**
  - Distribución de macros (gráficos de barras y pastel)
  - Comparación target vs real

- [ ] **Celdas 13-14 — Casos de prueba documentados y métricas**

### Versión 2.0 — Extensiones

- [ ] **Celda 15 — Visión por computadora** (Semana 13)
  - Integración con Roboflow para reconocer platillos peruanos
  - Tabla "platillo → ingredientes aproximados"

- [ ] Reactivar dietas vegetariana y vegana (OPCIONAL)
  - Requiere ampliar dataset con más proteínas vegetales

- [ ] Interfaz web con Flask/FastAPI

## Estructura del repositorio

```
proyecto_ia/
├── README.md                           Descripción general
├── ESTADO.md                           Este archivo
├── requirements.txt                    Dependencias
├── .gitignore
├── main.py                             Script de demostración
│
├── src/                                Código fuente modular
│   ├── __init__.py
│   ├── nutricion.py                    Capa 1
│   ├── perfil.py                       Datos del usuario
│   ├── sistema_experto.py              Capa 2 (RA1.2)
│   └── optimizador.py                  Capa 4 (RA1.1)
│
├── data/
│   └── ingredientes_dataset.csv        81 ingredientes curados
│
├── docs/
│   ├── bitacora_decisiones.md
│   └── catalogo_reglas.md
│
└── notebooks/
    └── demo.ipynb                      Versión Colab
```

## Cómo continuar el desarrollo

### Para trabajar en VS Code

```bash
git clone <tu-repo>
cd proyecto_ia
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Para trabajar en Colab

1. Sube `data/ingredientes_dataset.csv` a tu Google Drive en `/MyDrive/proyecto_ia/`
2. Abre `notebooks/demo.ipynb` en Colab
3. Ejecuta todas las celdas en orden
