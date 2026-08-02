# 08 · Machine Learning

*Parte 8 · Anterior: [07. Proyectos Profesionales](07_Proyectos_Profesionales.md)*

> 💡 **Qué vas a poder hacer después de este capítulo**
> Enmarcar un problema de negocio como un problema de modelado, construir un pipeline de evaluación apropiado, y entender qué hace falta para llevar un modelo a producción — el puente de Data Analyst → Data Scientist del [01.4](01_Introduccion.md#14-caminos-de-carrera).

---

## 8.1 Los tipos de problema

| Tipo | Predice | Ejemplo |
|---|---|---|
| **Regresión** | Un número continuo | Pronosticar el revenue del próximo mes |
| **Clasificación** | Una categoría | ¿Este cliente va a hacer churn? (sí/no) |
| **Clustering** | Estructura sin etiquetas | Segmentar clientes por comportamiento, sin etiquetas dadas |
| **Recomendación** | Relevancia rankeada | "Los clientes que compraron X también compraron Y" |
| **Series de Tiempo** | Valores futuros en el tiempo | Pronóstico de demanda diaria |
| **NLP** | Estructura/significado de texto | Clasificar tickets de soporte por tema, sentimiento de reseñas |

> 🏢 **Ejemplo real de empresa**
> Un sistema de **Detección de Fraude con Tarjeta de Crédito** (ver [Proyecto 05](../proyectos/05_Deteccion_Fraude_Tarjeta_Credito/)) es un problema de clasificación con desbalance de clases extremo — el fraude es tal vez el 0.1% de las transacciones. Enmarcar esto correctamente (y elegir la métrica correcta) importa más que qué algoritmo elijas.

## 8.2 Ingeniería de Features (repaso + mirada de modelado)

Todo del [05.5](05_Python.md#55-ingeniería-de-features) aplica — ahora con un objetivo de modelado: ¿esta feature realmente ayuda al modelo a separar clases / predecir el número, o es ruido sobre el que el modelo va a hacer overfitting?

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

preprocess = ColumnTransformer([
    ('num', StandardScaler(), ['revenue_por_unidad', 'cantidad_pedidos']),
    ('cat', OneHotEncoder(handle_unknown='ignore'), ['categoria', 'region']),
])
```

## 8.3 Pipelines y Validación Cruzada

```python
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

pipe = Pipeline([
    ('preprocess', preprocess),
    ('model', RandomForestClassifier(random_state=42)),
])

scores = cross_val_score(pipe, X_train, y_train, cv=5, scoring='f1')
pipe.fit(X_train, y_train)
```

> ✅ **Buena práctica**
> Siempre envolvé el preprocesamiento + modelo en un único `Pipeline`, y siempre hacé validación cruzada. Un modelo que se ve genial en un split de train/test y terrible en otro no está listo — esta es la forma #1 en que los proyectos junior sobreestiman sus resultados.

## 8.4 Evaluación de Modelos

| Métrica | Usar cuando |
|---|---|
| **RMSE / MAE** | Regresión — magnitud promedio del error |
| **Accuracy** | Clasificación, solo cuando las clases están balanceadas |
| **Precision / Recall / F1** | Clasificación con desbalance (fraude, churn) |
| **ROC-AUC** | Qué tan bien separa el modelo las clases a lo largo de distintos umbrales |

> ⚠️ **Error común**
> Reportar 99% de accuracy en un modelo de fraude donde el fraude es el 0.1% del dato — un modelo que predice "no es fraude" para todo obtiene 99.9% de accuracy siendo completamente inútil. Exactamente por esto existen **Precision/Recall**.

## 8.5 Optimización de Hiperparámetros

```python
from sklearn.model_selection import GridSearchCV

param_grid = {'model__n_estimators': [100, 300], 'model__max_depth': [5, 10, None]}
grid = GridSearchCV(pipe, param_grid, cv=5, scoring='f1')
grid.fit(X_train, y_train)
print(grid.best_params_)
```

## 8.6 Deployment (el traspaso al ML Engineer)

```mermaid
flowchart LR
    NB[Notebook: modelo entrenado] --> Serialize[Serializar\n.pkl / MLflow]
    Serialize --> API[Envolver en API\nFastAPI / Flask]
    API --> Prod[Servicio en producción]
    Prod --> Monitor[Monitoreo: drift, latencia, accuracy]
    Monitor -->|dispara| Retrain[Pipeline de reentrenamiento]
```

> 🏢 **Ejemplo real de empresa**
> El modelo de churn de un Data Scientist no genera valor de negocio sentado en un notebook. Un **ML Engineer** lo envuelve detrás de una API, el producto lo llama cuando decide quién recibe una oferta de retención, y el modelo se monitorea por **drift** — cuando el dato en vivo empieza a parecerse menos al dato de entrenamiento, el accuracy se degrada silenciosamente. Este es el límite de roles del [01.2](01_Introduccion.md#12-los-seis-roles-y-cómo-se-diferencian-realmente).

---

## Resumen del capítulo

- Enmarcá correctamente el problema de negocio como regresión / clasificación / clustering / recsys / series de tiempo / NLP antes de elegir un algoritmo.
- Usá siempre un `Pipeline` + validación cruzada — nunca confíes en un solo split de train/test.
- Hacé coincidir la métrica con el problema: la clasificación desbalanceada necesita Precision/Recall/F1, no accuracy.
- El deployment es una disciplina distinta (ML Engineering) — entrenar un buen modelo es necesario pero no suficiente.

**Siguiente:** [09. Portfolio y Carrera →](09_Portfolio_Carrera.md) — convirtiendo todo lo que construiste en un trabajo.
