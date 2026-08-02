# Reporte del modelo de fraude — fintech_fraud_intelligence

## Validación cruzada (5-fold, train set)
F1 promedio: 0.9906 (+/- 0.0038)

## Evaluación en test set (hold-out, 20%)
ROC-AUC: 0.9997

```
              precision    recall  f1-score   support

           0     1.0000    0.9999    0.9999    200000
           1     0.9820    0.9976    0.9897      1643

    accuracy                         0.9998    201643
   macro avg     0.9910    0.9987    0.9948    201643
weighted avg     0.9998    0.9998    0.9998    201643

```

## Matriz de confusión (test set)
```
[[199970     30]
 [     4   1639]]
```

## Nota sobre el dataset
Este modelo entrena sobre el dataset muestreado (ver README.md del proyecto):
se conservó el 100% del fraude real y se muestreó la clase mayoritaria a 1M
de filas. Esto NO es la tasa de fraude real de PaySim (~0.13%) sino una
aproximada al 0.81% — el modelo generaliza sobre el patrón, pero cualquier
métrica de "fraude detectado en producción" debería recalibrarse contra el
volumen real antes de usarse para decisiones de negocio.

## ⚠️ Hallazgo importante: posible data leakage / patrón demasiado "fácil"

Un ROC-AUC de 0.9997 y solo 4 falsos negativos sobre 1,643 casos de fraude
en test es **inusualmente alto** para un problema de fraude real. La causa
más probable no es que el modelo sea excelente, sino que **PaySim genera el
fraude sintético con un patrón de balance muy distintivo**: en las
transacciones fraudulentas simuladas, `origin_balance_delta`
(`origin_balance_after - origin_balance_before`) casi siempre vacía la
cuenta por completo de una forma que no ocurre en transacciones legítimas —
un "tell" que el generador sintético dejó sin querer.

**Por qué esto importa:** en fraude real, los estafadores intentan
activamente que sus transacciones parezcan normales. Un modelo con este
nivel de separación perfecta en un dataset real sería motivo de sospecha de
*leakage* (una feature que "filtra" la respuesta), no de celebración.

**Qué habría que hacer antes de confiar en este modelo para producción:**
1. Entrenar un segundo modelo **sin** `origin_balance_delta` ni
   `balance_mismatch` (las features más sospechosas de leakage) y comparar
   el ROC-AUC — si cae mucho, confirma que el modelo dependía casi
   exclusivamente de ese patrón sintético.
2. Validar contra transacciones de fraude reales (no simuladas) antes de
   cualquier decisión de negocio.
3. Tratar este resultado como una demostración del **pipeline completo**
   (feature engineering → Pipeline → validación cruzada → métricas
   correctas), no como evidencia de que el problema de fraude "ya está
   resuelto".
