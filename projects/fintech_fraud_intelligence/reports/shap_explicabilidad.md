# Explicabilidad con SHAP — fintech_fraud_intelligence

## Resumen general
Ver `shap_summary.png` — cada punto es una transacción del set de muestra;
el color indica si esa feature era alta (rojo) o baja (azul) para esa
transacción, y la posición horizontal indica si empujó la predicción hacia
fraude (derecha) o no-fraude (izquierda).

## Casos individuales
Ver `shap_casos_individuales.png` para el gráfico. Detalle:

### Caso 1: FRAUDE real
amount=21571.00, type=CASH_OUT, origin_balance_delta=-21571.00, balance_mismatch=False
- `num__balance_mismatch`: +0.2858 (empuja hacia FRAUDE)
- `num__origin_balance_after`: +0.1010 (empuja hacia FRAUDE)
- `num__origin_balance_delta`: -0.0405 (empuja hacia NO fraude)
- `num__amount`: +0.0380 (empuja hacia FRAUDE)
- `cat__dest_account_kind_customer`: +0.0333 (empuja hacia FRAUDE)
- `cat__type_PAYMENT`: +0.0324 (empuja hacia FRAUDE)
- `cat__dest_account_kind_merchant`: +0.0312 (empuja hacia FRAUDE)
- `cat__type_CASH_OUT`: +0.0288 (empuja hacia FRAUDE)

### Caso 2: FRAUDE real
amount=4162555.99, type=TRANSFER, origin_balance_delta=-4162555.99, balance_mismatch=False
- `num__balance_mismatch`: +0.1379 (empuja hacia FRAUDE)
- `num__origin_balance_delta`: +0.0899 (empuja hacia FRAUDE)
- `num__amount`: +0.0449 (empuja hacia FRAUDE)
- `cat__type_TRANSFER`: +0.0439 (empuja hacia FRAUDE)
- `num__origin_balance_after`: +0.0402 (empuja hacia FRAUDE)
- `num__dest_balance_before`: +0.0390 (empuja hacia FRAUDE)
- `num__origin_balance_before`: +0.0373 (empuja hacia FRAUDE)
- `cat__type_PAYMENT`: +0.0204 (empuja hacia FRAUDE)

### Caso 3: FRAUDE real
amount=1736804.93, type=TRANSFER, origin_balance_delta=-1736804.93, balance_mismatch=False
- `num__balance_mismatch`: +0.1450 (empuja hacia FRAUDE)
- `num__origin_balance_delta`: +0.0912 (empuja hacia FRAUDE)
- `cat__type_TRANSFER`: +0.0432 (empuja hacia FRAUDE)
- `num__origin_balance_after`: +0.0432 (empuja hacia FRAUDE)
- `num__dest_balance_before`: +0.0390 (empuja hacia FRAUDE)
- `num__amount`: +0.0369 (empuja hacia FRAUDE)
- `num__origin_balance_before`: +0.0350 (empuja hacia FRAUDE)
- `cat__type_PAYMENT`: +0.0205 (empuja hacia FRAUDE)

### Caso 4: no-fraude real
amount=1081660.18, type=TRANSFER, origin_balance_delta=0.00, balance_mismatch=True
- `num__balance_mismatch`: -0.3014 (empuja hacia NO fraude)
- `num__dest_balance_before`: -0.0629 (empuja hacia NO fraude)
- `num__origin_balance_before`: -0.0623 (empuja hacia NO fraude)
- `num__origin_balance_delta`: -0.0599 (empuja hacia NO fraude)
- `num__dest_balance_after`: -0.0438 (empuja hacia NO fraude)
- `cat__type_CASH_OUT`: -0.0218 (empuja hacia NO fraude)
- `num__amount`: +0.0160 (empuja hacia FRAUDE)
- `num__origin_balance_after`: +0.0145 (empuja hacia FRAUDE)

### Caso 5: no-fraude real
amount=17999.83, type=TRANSFER, origin_balance_delta=-17999.82, balance_mismatch=False
- `num__origin_balance_after`: -0.3684 (empuja hacia NO fraude)
- `num__balance_mismatch`: +0.1062 (empuja hacia FRAUDE)
- `num__dest_balance_before`: -0.0694 (empuja hacia NO fraude)
- `num__origin_balance_delta`: -0.0672 (empuja hacia NO fraude)
- `num__dest_balance_after`: -0.0498 (empuja hacia NO fraude)
- `num__origin_balance_before`: -0.0372 (empuja hacia NO fraude)
- `num__amount`: -0.0351 (empuja hacia NO fraude)
- `cat__type_CASH_OUT`: -0.0277 (empuja hacia NO fraude)

### Caso 6: no-fraude real
amount=25476.21, type=PAYMENT, origin_balance_delta=0.00, balance_mismatch=True
- `num__balance_mismatch`: -0.2256 (empuja hacia NO fraude)
- `cat__type_PAYMENT`: -0.0558 (empuja hacia NO fraude)
- `num__origin_balance_delta`: -0.0526 (empuja hacia NO fraude)
- `cat__dest_account_kind_merchant`: -0.0504 (empuja hacia NO fraude)
- `cat__dest_account_kind_customer`: -0.0495 (empuja hacia NO fraude)
- `num__origin_balance_before`: -0.0380 (empuja hacia NO fraude)
- `num__amount`: -0.0379 (empuja hacia NO fraude)
- `num__dest_balance_before`: +0.0346 (empuja hacia FRAUDE)

