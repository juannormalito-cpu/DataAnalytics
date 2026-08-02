# Calibración de probabilidades — fintech_fraud_intelligence

## Sin calibrar
| Probabilidad predicha (bin) | Fracción real de fraude |
|---|---|
| 0.000 | 0.000 |
| 0.000 | 0.000 |
| 0.001 | 0.000 |
| 0.002 | 0.000 |
| 0.005 | 0.000 |
| 0.102 | 0.081 |

## Calibrado (Platt scaling / sigmoid, 3-fold CV)
| Probabilidad predicha (bin) | Fracción real de fraude |
|---|---|
| 0.000 | 0.000 |
| 0.000 | 0.000 |
| 0.000 | 0.000 |
| 0.000 | 0.000 |
| 0.000 | 0.000 |
| 0.081 | 0.081 |

## Interpretación
Si el modelo estuviera perfectamente calibrado, un bin con probabilidad
predicha promedio de 0.7 debería tener exactamente 70% de casos con fraude
real. Cuanto más cerca de la diagonal en `calibracion.png`, mejor calibrado.

Esto importa para decisiones de negocio: si el equipo de Riesgo va a usar
la probabilidad directamente (ej. "revisar manualmente todo caso con
probabilidad > 60%"), esa probabilidad tiene que significar lo que dice —
no solo servir para *ordenar* casos (que es todo lo que el ROC-AUC mide).
