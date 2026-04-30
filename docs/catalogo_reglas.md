# Catálogo de Reglas del Sistema Experto

Documento de referencia de las 18 reglas implementadas en la **Capa 2** del sistema (`src/sistema_experto.py` y `src/nutricion.py`).

## Estructura general

| Grupo | Tipo | Cantidad | Descripción |
|---|---|---|---|
| A | HARD | 2 | Filtrado por dieta |
| B | HARD | 3 | Reparto de macros según objetivo |
| C | HARD | 4 | Estructura por comida |
| D | SOFT | 5 | Reglas de salud (modifican pesos) |
| E | SOFT/HARD | 4 | Contexto del momento |
| F | HARD | 1 | Seguridad calórica |
| **Total** | | **18** | |

## Grupo A — Filtrado por dieta (HARD)

| ID | Condición | Acción |
|---|---|---|
| A1 | dieta = vegetariano | Excluir ingredientes con `apto_vegetariano = False` |
| A2 | dieta = vegano | Excluir ingredientes con `apto_vegano = False` |

> En v1.0 estas reglas no se disparan (solo se acepta dieta omnívora). El código está preparado para reactivación en v2.0 sin migraciones del dataset.

## Grupo B — Reparto de macros según objetivo (HARD)

| ID | Objetivo | Calorías | Proteína | Carbos | Grasa |
|---|---|---|---|---|---|
| B1 | perder_grasa | GET × 0.80 | 40% | 35% | 25% |
| B2 | mantener | GET × 1.00 | 30% | 45% | 25% |
| B3 | ganar_musculo | GET × 1.15 | 35% | 40% | 25% |

## Grupo C — Estructura por comida (HARD)

| ID | Comida | Estructura obligatoria |
|---|---|---|
| C1 | desayuno | Mínimo 1 carbohidrato |
| C2 | almuerzo | Mínimo 1 proteína + 1 carbohidrato + 1 verdura |
| C3 | cena | Mínimo 1 proteína + 1 verdura (carbohidrato opcional) |
| C4 | snack | Sin estructura rígida (configuración contextual por objetivo) |

## Grupo D — Reglas de salud (SOFT, modifican pesos)

| ID | Condición | Acción |
|---|---|---|
| D1 | objetivo = perder_grasa | Peso × 0.5 a ingredientes con grasa saturada > 7g |
| D2 | (descartada) | No incluida por falta de respaldo científico moderno |
| D3 | objetivo = ganar_musculo Y categoría = Proteína | Peso × 1.5 a proteínas con ≥25g/100g |
| D4 | edad > 50 | Peso × 0.5 a ingredientes con grasa saturada > 5g |
| D5 | edad > 50 | Peso × 1.5 a palta, nueces, chía, salmón, pescados grasos |

## Grupo E — Contexto del momento (SOFT + HARD)

| ID | Condición | Acción |
|---|---|---|
| E1 | desayuno + ganar_musculo | HARD: habilitar carnes en desayuno (pollo, pavo, etc.) |
| E2 | comida = snack | SOFT: peso × 1.5 a ingredientes con "snack" en `comidas_recomendadas` |
| E3 | cena + perder_grasa | SOFT: peso × 1.5 a pescado magro y hojas; × 0.7 a carnes rojas |
| E4 | nivel_actividad ∈ ('intenso', 'muy_intenso') | HARD: factor de actividad 1.725 (aplicado en TMB) |

## Grupo F — Seguridad calórica (HARD)

| ID | Condición | Acción |
|---|---|---|
| F1 | calorías_calculadas < mínimo_seguridad | Forzar calorías al mínimo (1500 hombre / 1200 mujer) y emitir advertencia |

## Restricciones adicionales en el optimizador (Capa 4)

Aunque no son "reglas" del Sistema Experto en sentido estricto, complementan su lógica:

- Máximo 1 ingrediente por categoría (excepto verduras: máximo 2 en comidas principales)
- Máximo 1 ingrediente por grupo intercambiable (evita "olluco + camote")
- Solo 1 entre Bebida y Lácteo (no leche + bebida vegetal juntas)
- Límite de cantidad total de ingredientes según objetivo y comida
- En comidas principales: ≥70% de la proteína desde fuentes "reales" (Proteína o Lácteo)
- Snack contextual: categorías y porciones diferentes según objetivo
- Desayuno sin verduras (excepto camote como tubérculo permitido)
- Snack excluye ingredientes que requieren preparación (legumbres, granos andinos, tubérculos)

## Cómo se evidencian en el log

Cada vez que el Sistema Experto evalúa un perfil, registra qué reglas se dispararon. Este log es crucial para defender el proyecto en la exposición:

```python
resultado = sistema.evaluar(perfil, 'almuerzo')
for regla in resultado['reglas_log']:
    print(regla)

# Ejemplo de salida:
# D3: peso×1.5 a 9 proteínas con ≥25g/100g
# E1: carnes habilitadas en desayuno (ganar músculo)
```

## Decisión sobre regla descartada

**Regla D2** ("no carbohidratos de IG alto en la cena") fue evaluada y descartada porque la evidencia científica moderna no respalda este principio. Estudios actuales indican que la distribución horaria de carbohidratos importa menos que el balance calórico total. Esta decisión se mantiene documentada para preservar el rigor científico del proyecto.
