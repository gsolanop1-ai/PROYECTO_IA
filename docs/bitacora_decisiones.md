# Bitácora de Decisiones del Proyecto
## Sistema Inteligente de Recomendación Alimenticia

**Curso:** Inteligencia Artificial: Principios y Técnicas (ISIA-108)
**Universidad:** UPAO — Semestre 2026-10
**Última actualización:** 

---

## 1. Descripción del proyecto

Sistema inteligente de recomendación alimenticia personalizada que entrega al usuario un plan diario (desayuno, almuerzo, cena, snack) con ingredientes específicos y cantidades exactas, basándose en sus datos personales (edad, sexo, peso, altura, nivel de actividad, objetivo) y aplicando técnicas de inteligencia artificial. La modalidad de presentación combina ingredientes con cantidades y un nombre creativo de platillo generado por IA generativa.

El proyecto está inspirado en aplicaciones comerciales como Fitia, pero diferenciándose por su enfoque en ingredientes peruanos (incluyendo tarwi, kiwicha, maca, olluco, ají amarillo) y su arquitectura modular que permite extensiones futuras como visión por computadora.

---

## 2. Resumen de decisiones tomadas

### 2.1 Alcance y modalidad

| Decisión | Opción elegida | Razón |
|---|---|---|
| Modalidad de recomendación | Ingredientes con cantidades + nombre de platillo (modelo "tipo Fitia") | Mayor flexibilidad y simplicidad de implementación que recomendar platillos cerrados; el usuario decide cómo combinar |
| Cantidad de modalidades | Una sola modalidad de presentación | Permite enfocar esfuerzo en hacer una bien en lugar de dos a medias |
| Recetario predefinido | Descartado en versión base | Demasiado costoso para el tiempo del curso; se sustituye con generación creativa por LLM |
| Visión por computadora | Arquitectura preparada, no implementada | Permite agregarla en Semana 12-13 sin reestructurar; si no se llega, no se pierde nada |

### 2.2 Técnicas de IA elegidas

El proyecto cubre los cuatro Resultados de Aprendizaje (RA) del sílabo mediante una arquitectura de cinco capas:

| Capa | Técnica | Semana del sílabo | RA cubierto |
|---|---|---|---|
| 1 | Cálculo nutricional (Mifflin-St Jeor) | base lógica | — |
| 2 | Sistema Experto con reglas (implementado a mano) | Semana 6 | RA1.2 |
| 3 | K-Means clustering | Semana 9 | RA2.1 |
| 4 | Optimización con PuLP (programación lineal) | Semanas 3-4 | RA1.1 |
| 5 | LLM (IA Generativa) | Semana 14 | RA2.2 |

### 2.3 Decisiones técnicas específicas

| Componente | Decisión | Alternativa descartada | Razón |
|---|---|---|---|
| Fórmula calórica | Mifflin-St Jeor (1990) | Harris-Benedict (1919) | Mifflin-St Jeor es más precisa para población general; usada por Fitia y MyFitnessPal |
| Tipo de reglas del Sistema Experto | Soft rules (con pesos) + Hard rules estructurales | Solo hard rules | Soft rules evitan que el sistema falle por restricciones contradictorias |
| Reparto de macronutrientes | Fijo según objetivo | Personalizable por usuario | Más simple, suficiente para nivel académico |
| Implementación del motor de reglas | A mano (clase Python) | Librería `experta` | Mayor control, mejor pedagógicamente, evita problemas de compatibilidad |
| Algoritmo de optimización | Programación lineal con PuLP | Algoritmos genéticos, hill climbing | Más limpio, didáctico y matemáticamente óptimo |
| Modelo de LLM | Gemini API o Claude API | Generación local con modelo descargado | API es gratuita en niveles bajos y no consume recursos del Colab |

---

## 3. Decisiones sobre el dataset

### 3.1 Origen de los datos

Tras analizar tres fuentes distintas, se descartaron las opciones existentes y se construyó un dataset propio:

**Datasets evaluados y descartados:**

- **USDA FoodData Central API:** demasiado densa (cientos de miles de registros), API compleja, requiere autenticación. No apta para un proyecto académico de pregrado.
- **Daily Food & Nutrition Dataset (Kaggle, adilshamim8):** muy pequeña, datos limitados, no incluye ingredientes peruanos.
- **Comprehensive Foods USDA (Kaggle, 40K registros):** **descartada por problemas graves de calidad de datos:**
  - Inconsistencia en columna de calorías (mezcla de kcal y kJ sin etiquetar; ej. pollo marcaba 659 kcal/100g cuando el valor real es 165)
  - Columnas `serving_size` y `serving_unit` completamente vacías (0 valores no-nulos en 40,000 registros)
  - 80% del contenido son productos comerciales con marca, no ingredientes genéricos
  - Múltiples variantes confusas para cada ingrediente (403 entradas para "chicken")

**Decisión final:** construir un dataset curado de 81 ingredientes con valores verificados contra fuentes oficiales.

### 3.2 Estructura del dataset propio

- **81 ingredientes** distribuidos en 8 categorías
- **20 columnas** con macros, micronutrientes, índice glucémico, aptitud dietética
- **Estandarizado a 100g** todos los valores
- **Estado cocido** para todos los ingredientes consumidos cocidos (consistencia con apps comerciales)
- **Validado contra:** USDA FoodData Central oficial y Tabla Peruana de Composición de Alimentos del Instituto Nacional de Salud (INS)

### 3.3 Distribución por categorías

| Categoría | Cantidad | Tipo de uso |
|---|---|---|
| Proteínas | 14 | Principal (incluye carnes peruanas: bistec, lomo, jurel, caballa, salmón, tarwi) |
| Carbohidratos | 19 | Principal (incluye andinos: quinua, kiwicha, maca, olluco) |
| Grasas | 7 | Principal |
| Lácteos | 4 | Principal |
| Bebidas vegetales | 3 | Principal |
| Frutas | 17 | Principal (incluye granadilla, pitahaya) |
| Verduras | 12 | Principal |
| Condimentos peruanos | 5 | Condimento (no entra en optimización, solo en sugerencia LLM) |

### 3.4 Decisión sobre estado de los alimentos

Todos los ingredientes están registrados en estado cocido (excepto frutas, verduras crudas, frutos secos, polvos y bebidas líquidas). Esta decisión se basa en que:

- Es la convención que usan apps comerciales como Fitia y MyFitnessPal
- Es más realista para usuarios casuales que pesan los alimentos al servirse
- Evita inconsistencias mixtas (carbos cocidos + proteínas crudas) que generarían errores de cálculo

---

## 4. Catálogo de reglas del Sistema Experto

### 4.1 Estructura general

El Sistema Experto recibe el perfil del usuario y la comida actual como hechos, y produce:
1. Subset de ingredientes válidos (filtrados por dieta)
2. Targets calóricos y de macronutrientes
3. Restricciones estructurales por comida
4. Pesos de prioridad para cada ingrediente

Estos outputs alimentan a la Capa 4 (PuLP).

### 4.2 Catálogo completo (18 reglas)

#### Grupo A — Filtrado por dieta (HARD)

| ID | Condición | Acción |
|---|---|---|
| A1 | dieta = "vegetariano" | Excluir ingredientes con `apto_vegetariano = False` |
| A2 | dieta = "vegano" | Excluir ingredientes con `apto_vegano = False` |

#### Grupo B — Reparto de macros según objetivo (HARD)

| ID | Objetivo | Ajuste calórico | Proteína | Carbos | Grasa |
|---|---|---|---|---|---|
| B1 | "perder_grasa" | GET × 0.80 | 40% | 30% | 30% |
| B2 | "mantener" | GET × 1.00 | 30% | 45% | 25% |
| B3 | "ganar_musculo" | GET × 1.15 | 30% | 50% | 20% |

#### Grupo C — Estructura por comida (HARD)

| ID | Comida | Estructura obligatoria |
|---|---|---|
| C1 | desayuno | Mínimo 1 carbohidrato + 1 proteína |
| C2 | almuerzo | Mínimo 1 proteína principal + 1 carbohidrato + 1 verdura |
| C3 | cena | Mínimo 1 proteína + 1 verdura (carbohidrato opcional) |
| C4 | snack | (1 fruta o 1 grasa) y/o 1 fuente proteica |

#### Grupo D — Salud (SOFT, modifican pesos)

| ID | Condición | Acción |
|---|---|---|
| D1 | objetivo = "perder_grasa" | Peso × 0.5 a ingredientes con grasa saturada > 7g |
| D3 | objetivo = "ganar_musculo" Y categoria = Proteína | Peso × 1.5 a proteínas con ≥25g por 100g |
| D4 | edad > 50 | Peso × 0.5 a ingredientes con grasa saturada > 5g |
| D5 | edad > 50 | Peso × 1.5 a palta, nueces, chía, salmón, pescados grasos |
| D6 | sodio acumulado > 1500mg | Penalizar ingredientes adicionales de alto sodio |

#### Grupo E — Contexto del momento (SOFT + HARD)

| ID | Condición | Acción |
|---|---|---|
| E1 | comida = "desayuno" Y objetivo = "ganar_musculo" | HARD: habilitar carnes (pollo, pavo, huevo, lomo, bistec) en desayuno |
| E2 | comida = "snack" | SOFT: peso × 1.5 a ingredientes con "snack" en `comidas_recomendadas` |
| E3 | comida = "cena" Y objetivo = "perder_grasa" | SOFT: peso × 1.5 a pescado magro y hojas verdes; peso × 0.7 a carnes rojas |
| E4 | nivel_actividad ∈ ("intenso", "muy_intenso") | HARD: factor de actividad 1.725 |

### 4.3 Reglas evaluadas y descartadas

**Regla D2 — "no carbohidratos de IG alto en la cena":** descartada porque la evidencia científica moderna no respalda este principio. Estudios actuales indican que la distribución horaria de carbohidratos importa menos que el balance calórico total. Se decide no incluir esta regla para mantener el rigor científico del proyecto.

---

## 5. Estructura de celdas del notebook

El notebook se organiza en 6 bloques con 15 celdas:

### Bloque A — Setup y Datos
- Celda 1: Configuración del entorno (instalaciones, imports)
- Celda 2: Carga del dataset
- Celda 3: Análisis Exploratorio (EDA)

### Bloque B — Cálculo Nutricional
- Celda 4: Función de cálculo TMB y GET (Mifflin-St Jeor)
- Celda 5: Reparto de macronutrientes
- Celda 6: Perfil del usuario (diseñado modularmente para entradas alternativas)

### Bloque C — Inteligencia Artificial
- Celda 7: Sistema Experto (Capa 2)
- Celda 8: K-Means Clustering (Capa 3)
- Celda 9: Optimización PuLP (Capa 4)
- Celda 10: Generación con LLM (Capa 5)

### Bloque D — Plan Diario y Salida
- Celda 11: Generador de plan diario (orquestador)
- Celda 12: Visualización del plan

### Bloque E — Demostración y Validación
- Celda 13: Casos de prueba (3-4 perfiles distintos)
- Celda 14: Métricas de evaluación

### Bloque F — Punto de Extensión
- Celda 15: Placeholder para módulo de visión por computadora (Semana 12-13)

---

## 6. Cronograma sugerido

| Sesión | Bloques | Duración estimada | Resultado |
|---|---|---|---|
| Sesión 1 | Bloques A + B (Celdas 1-6) | 2-3 horas | Sistema calcula TMB, GET y macros del usuario |
| Sesión 2 | Celdas 7 y 9 | 3-4 horas | Sistema genera planes alimenticios completos |
| Sesión 3 | Celdas 8, 10, 11 | 2-3 horas | Sistema con K-Means y LLM funcional |
| Sesión 4 | Celdas 12-15 | 2-3 horas | Visualizaciones, casos de prueba y entregables |
| **Total** | — | **9-13 horas de equipo** | — |

---

## 7. Atributos del graduado cubiertos

El proyecto evidencia los siguientes atributos del perfil de egreso de Ingeniería de Sistemas e Inteligencia Artificial de la UPAO:

- **AG-C09 (Diseño y Desarrollo de Soluciones):** se diseña, implementa y evalúa una solución para un problema complejo (recomendación alimenticia personalizada) con consideraciones de salud y desarrollo sostenible.
- **AG-C11 (Uso de Herramientas):** se selecciona, adapta y aplica un conjunto de herramientas modernas (Python, PuLP, scikit-learn, LLM API) reconociendo sus limitaciones.
- **AG-C12 (Teoría y Fundamentos):** se aplica la teoría de IA y los fundamentos de desarrollo de software para producir una solución basada en computadora.

---

## 8. Justificación académica frente al sílabo

### Cobertura de Resultados de Aprendizaje

| RA | Cómo lo cumple el proyecto |
|---|---|
| **RA1.1** — Algoritmos de resolución, razonamiento y planificación | Optimización con programación lineal (PuLP) en la Capa 4 |
| **RA1.2** — Razonamiento incierto y aprendizaje en sistemas expertos | Sistema Experto con 18 reglas (5 hard + 6 estructurales + 7 soft) en la Capa 2 |
| **RA2.1** — Modelos de Machine Learning | K-Means clustering de ingredientes en la Capa 3 |
| **RA2.2** — Aprendizaje por representación e IA generativa | LLM (Gemini/Claude) para nombrado creativo de platillos en la Capa 5 |

### Cobertura de semanas del sílabo

- **Semana 1-2:** Definición del proyecto y agentes inteligentes (arquitectura del sistema)
- **Semana 3-4:** Búsqueda y optimización heurística (PuLP)
- **Semana 5:** Limpieza y preprocesamiento de datos (construcción del dataset curado)
- **Semana 6:** Sistemas Expertos (Capa 2)
- **Semana 9:** Machine Learning (K-Means)
- **Semana 14:** IA Generativa (LLM)
- **Semana 13 (opcional):** Visión por Computadora (placeholder preparado)

---

## 9. Riesgos identificados y mitigaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| PuLP devuelve "infactible" si las restricciones son contradictorias | Alto | Sistema de soft rules + manejo de excepciones que reintenta con menos restricciones |
| LLM puede alucinar nombres absurdos de platillos | Medio | Prompts estructurados, temperatura baja, lista de ejemplos en el prompt |
| API de LLM puede no estar disponible en momento de la demo | Medio | Fallback a respuesta simple sin IA generativa si la API falla |
| K-Means da resultados inestables con pocos datos | Bajo | 81 ingredientes son suficientes; usar `random_state` fijo para reproducibilidad |
| Diferencias entre Fitia/MyFitnessPal y nuestros valores | Bajo | Documentar fuentes oficiales (USDA, INS) en el informe final |

---

*Esta bitácora sirve como documento de referencia para el equipo y como evidencia de las decisiones técnicas que respaldan el proyecto. Se recomienda actualizarla cada vez que se tome una nueva decisión importante durante el desarrollo.*
