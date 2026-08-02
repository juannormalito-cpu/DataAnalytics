# Comparación de algoritmos — fintech_fraud_intelligence

| Métrica | Random Forest | Logistic Regression |
|---|---|---|
| ROC-AUC (test) | 0.9997 | 0.9952 |
| F1 (CV, 5-fold) | 0.9906 (+/- 0.0038) | 0.2849 (+/- 0.0020) |

## Random Forest — classification report
```
              precision    recall  f1-score   support

           0     1.0000    0.9999    0.9999    200000
           1     0.9820    0.9976    0.9897      1643

    accuracy                         0.9998    201643
   macro avg     0.9910    0.9987    0.9948    201643
weighted avg     0.9998    0.9998    0.9998    201643

```

## Logistic Regression — classification report
```
              precision    recall  f1-score   support

           0     1.0000    0.9587    0.9789    200000
           1     0.1653    0.9951    0.2835      1643

    accuracy                         0.9590    201643
   macro avg     0.5826    0.9769    0.6312    201643
weighted avg     0.9932    0.9590    0.9732    201643

```

## Por qué pueden diferir

Random Forest puede capturar **relaciones no lineales** entre features
(ej. "fraude solo si `balance_mismatch=True` Y `type=TRANSFER`" — una
combinación, no una suma ponderada). Logistic Regression solo aprende
**combinaciones lineales** de las features — es más simple, más rápida,
más fácil de explicar ("cada feature suma o resta X puntos de riesgo"), y
en muchos negocios reales se prefiere por eso, aunque pierda algo de
performance frente a un modelo más complejo.
