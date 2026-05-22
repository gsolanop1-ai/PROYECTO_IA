# Estado del Proyecto

**Última actualización:** 

## Avance: Versión 1.0 — Sistema completado

### Implementado y validado

- [x] Módulo de cálculo nutricional 
  - Mifflin-St Jeor para TMB
  - Factores de actividad para GET
  - Reparto de macros según objetivo
  - Distribución calórica entre 4 comidas
  - Regla de seguridad calórica

- [x] Módulo de perfil de usuario 
  - Validación robusta de inputs
  - Diseño modular para futuras fuentes

- [x] Sistema Experto con 18 reglas 
  - Grupo C: Estructura por comida
  - Grupo D: Reglas de salud (D1, D3, D4, D5)
  - Grupo E: Contexto del momento

- [x] K-Means Clustering
  - 4 clusters nutricionales identificados
  - Visualización con PCA
  - Coeficiente de silueta: 0.45

- [x] Optimizador con PuLP 
  - Programación lineal mixta entera
  - Restricciones de macros con tolerancia
  - Estructura obligatoria por comida
  - Snack contextual según objetivo
  - Desayuno sin verduras
  - Límite de ingredientes anti-buffet
  - Fallback automático ante infactibilidad

- [x] Orquestador del Plan Diario
  - Memoria entre comidas (penalización ×0.3)
  - Generación coordinada de las 4 comidas

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
- Macros perder grasa: 40/35/25
- Distribución de comidas variable por objetivo
- Snack contextual con configuraciones diferenciadas
- Mínimo de seguridad: 1500 kcal hombre / 1200 kcal mujer

## Estructura del repositorio
proyecto_ia/
├── README.md Descripción general
├── ESTADO.md Este archivo
├── requirements.txt Dependencias
├── .gitignore
│
├── data/
│ └── ingredientes_dataset.csv 81 ingredientes curados
│
├── docs/
│ ├── bitacora_decisiones.md
│ └── catalogo_reglas.md
│
└── notebooks/
└── demo.ipynb Versión Colab


### Para trabajar en Colab

1. Sube `data/ingredientes_dataset.csv` a tu Google Drive en `/MyDrive/proyecto_ia/`
2. Abre `notebooks/demo.ipynb` en Colab
3. Ejecuta todas las celdas en orden
