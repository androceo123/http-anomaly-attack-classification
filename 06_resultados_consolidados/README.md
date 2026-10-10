# Resultados consolidados y catálogos

`catalogo_corridas.csv` localiza las etapas, su estado y la cantidad de artefactos asociados. `metricas_registradas.csv` extrae los campos originales de `metrics_flat.csv`, conservando su nombre, valor, corrida y archivo fuente. No convierte automáticamente unidades ni promedia resultados de taxonomías distintas.

Para interpretar cada cifra consulte el [historial experimental](../04_experimentos/README.md), las fichas de corrida y el [catálogo de datasets](../03_datasets/README.md). Los resultados L1 usan filas/eventos y L2 grupos por huella. Los tiempos de reanudación y los tiempos heredados de entrenamiento se distinguen en sus fichas.

Las comprobaciones derivadas están en `02_auditoria`. Las curvas M8 de Harvard y DS usan 50.000 casos muestreados, mientras sus métricas globales usan el test completo; el metadato original permite explicar la diferencia. Las fuentes originales permanecen dentro de cada corrida.
