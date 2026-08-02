# Modelo honesto — fintech_fraud_intelligence

Excluye: origin_balance_delta, balance_mismatch

- ROC-AUC (test): 0.9991
- F1 (CV, 5-fold): 0.5562 (+/- 0.0038)

```
              precision    recall  f1-score   support

           0     0.9999    0.9870    0.9934    200000
           1     0.3859    0.9927    0.5557      1643

    accuracy                         0.9871    201643
   macro avg     0.6929    0.9899    0.7746    201643
weighted avg     0.9949    0.9871    0.9899    201643

```

Guardado en models/fraud_classifier_honest.joblib — servido en la API bajo
`/score/honest` (ver api.py), como alternativa al modelo completo en `/score`.
