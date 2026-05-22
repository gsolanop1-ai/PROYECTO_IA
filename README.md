# Sistema Inteligente de Recomendación Alimenticia

Proyecto académico del curso **Inteligencia Artificial: Principios y Técnicas (ISIA-108)** — UPAO 2026-10.

Sistema de recomendación nutricional personalizada que genera planes alimenticios diarios (desayuno, almuerzo, cena, snack) con ingredientes peruanos, basado en el perfil del usuario y aplicando técnicas de Inteligencia Artificial.

## Arquitectura del sistema

| Capa | Técnica |
|---|---|
| 1 | Cálculo nutricional (Mifflin-St Jeor) |
| 2 | Sistema Experto (18 reglas) |
| 3 | K-Means Clustering |
| 4 | Optimización con PuLP |

## Estructura del proyecto


```
proyecto_ia/
│
├── data/
│ └── ingredientes_dataset.csv # 81 ingredientes curados
├── docs/
│ ├── bitacora_decisiones.md # Decisiones técnicas tomadas
│ └── catalogo_reglas.md # Las 18 reglas del Sistema Experto
├── notebooks/
│ └── demo.ipynb # Notebook para ejecutar en Colab
├── requirements.txt # Dependencias
└── README.md
```


## Ejecución en Google Colab

1. Sube el archivo `data/ingredientes_dataset.csv` a tu Google Drive en `/MyDrive/proyecto_ia/`
2. Abre `notebooks/demo.ipynb` en Google Colab
3. Ejecuta todas las celdas en orden

## Estado actual

Sistema base completado y validado:
- Cálculo nutricional con Mifflin-St Jeor y regla de seguridad calórica
- Sistema Experto con 18 reglas (filtrado, estructura, salud, contexto)
- K-Means clustering con 4 clusters nutricionales
- Optimización con programación lineal y fallback automático
- Orquestador con memoria de ingredientes para promover variedad
- Validado con 4 perfiles diversos (desviación promedio: 1.7%)

## Equipo y contexto

Universidad Privada Antenor Orrego — Facultad de Ingeniería
Programa: Ingeniería de Sistemas e Inteligencia Artificial
Semestre 2026-10
