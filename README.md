# Sistema Inteligente de Recomendación Alimenticia

Proyecto académico del curso **Inteligencia Artificial: Principios y Técnicas (ISIA-108)** — UPAO 2026-10.

Sistema de recomendación nutricional personalizada que genera planes alimenticios diarios (desayuno, almuerzo, cena, snack) con ingredientes peruanos, basado en el perfil del usuario y aplicando técnicas de Inteligencia Artificial.

## Arquitectura del sistema

| Capa | Técnica | Semana del sílabo | RA |
|---|---|---|---|
| 1 | Cálculo nutricional (Mifflin-St Jeor) | Base lógica | — |
| 2 | Sistema Experto con 18 reglas | Semana 6 | RA1.2 |
| 3 | K-Means Clustering | Semana 9 | RA2.1 |
| 4 | Optimización con PuLP | Semanas 3-4 | RA1.1 |
| 5 | LLM (IA Generativa) | Semana 14 | RA2.2 |

## Estructura del proyecto

```
proyecto_ia/
│
├── data/
│   └── ingredientes_dataset.csv  # 81 ingredientes curados
├── docs/
│   ├── bitacora_decisiones.md    # Decisiones técnicas tomadas
│   └── catalogo_reglas.md        # Las 18 reglas del Sistema Experto
├── notebooks/
│   └── demo.ipynb                # Notebook para ejecutar en Colab
├── requirements.txt              # Dependencias
└── README.md
```

## Ejecución en Google Colab

Sube los archivos al Drive y ejecuta el notebook `notebooks/demo.ipynb`.

## Estado actual

Versión 1.0 — Sistema base completado:
- Cálculo nutricional con regla de seguridad calórica
- Sistema Experto con 18 reglas (5 hard + 6 estructurales + 7 soft)
- Optimización con programación lineal y fallback automático
- Validado con 4 perfiles diversos (desviación promedio: 1.7%)

Pendiente:
- K-Means clustering
- Integración con LLM
- Orquestador del plan diario completo
- Visualizaciones

## Equipo y contexto

Universidad Privada Antenor Orrego — Facultad de Ingeniería
Programa: Ingeniería de Sistemas e Inteligencia Artificial
Semestre 2026-10
