# Inspección del modelo — fintech_fraud_intelligence

## Top 15 features por importancia
```
num__balance_mismatch                0.317107
num__origin_balance_delta            0.196668
num__origin_balance_after            0.116068
num__origin_balance_before           0.102612
num__amount                          0.064457
cat__type_PAYMENT                    0.037171
cat__dest_account_kind_customer      0.033546
cat__type_TRANSFER                   0.030103
cat__dest_account_kind_merchant      0.028722
num__dest_balance_after              0.023711
num__dest_balance_before             0.022517
cat__type_CASH_IN                    0.018296
cat__type_CASH_OUT                   0.008106
cat__type_DEBIT                      0.000914
cat__origin_account_kind_customer    0.000000
```

`balance_mismatch` y `origin_balance_delta` juntas explican más de la mitad
(51.4%) de la importancia total — confirma la sospecha inicial: el modelo se
apoya fuertemente en el patrón de balance que PaySim deja sin querer en sus
transacciones fraudulentas sintéticas.

## Umbral de decisión: algunos puntos de referencia
```
 threshold  precision   recall
  0.000000   0.008148 1.000000
  0.001388   0.024270 1.000000
  0.002290   0.030883 0.999391
  0.003125   0.042051 0.998783
  0.004366   0.062403 0.998783
  0.006882   0.093154 0.998783
  0.011443   0.131091 0.998783
  0.019325   0.192764 0.998783
  0.031407   0.306958 0.998783
  0.048258   0.561218 0.998783
```
Interpretación: con umbrales muy bajos el modelo atrapa el 100% del fraude
pero con precision pésima (más falsas alarmas que fraudes reales). A medida
que sube el umbral, la precision mejora rápido sin perder casi nada de
recall — señal de que el modelo separa muy bien las dos clases en general
(consistente con el ROC-AUC alto). Ver `barrido_umbral.png` para la curva
completa.

## Comparación: con vs. sin features sospechosas de leakage

| | Con `origin_balance_delta`, `balance_mismatch` | Sin esas features |
|---|---|---|
| ROC-AUC | 0.9997 | 0.9992 |
| F1 (CV, 5-fold, umbral 0.5) | 0.9906 | **0.5637** |

**Leakage parcial confirmado, pero de una forma más sutil de lo esperado.**
El ROC-AUC —que mide qué tan bien el modelo *ordena* fraude vs. no-fraude,
sin importar el umbral— casi no cae: el modelo sigue separando bien usando
`type`, `amount` y los balances originales por sí solos. Pero el **F1 en el
umbral por defecto (0.5) se derrumba** sin esas dos features, porque las
probabilidades quedan mal calibradas exactamente en ese punto sin la señal
"fácil" del balance vaciado.

**Lectura correcta:** el modelo no está "roto" sin esas features — sigue
teniendo buena capacidad de separación (ROC-AUC). Pero el número que más se
suele mostrar en un resumen ejecutivo (F1, accuracy en un umbral fijo)
estaba inflado por un atajo que el modelo encontró en el patrón sintético de
PaySim. Esta es la razón exacta por la que el Capítulo 08 del handbook
insiste en mirar varias métricas (no solo una) antes de confiar en un
modelo: el ROC-AUC y el F1 cuentan historias distintas, y solo mirando
ambas —más un experimento de ablación como este— se detecta el problema.
