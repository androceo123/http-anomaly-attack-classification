# Resultados consolidados y catálogos

El [catálogo de corridas](catalogo_corridas.csv) identifica las etapas, su estado metodológico, la documentación y la disponibilidad de artefactos. `catalogued_artifacts` cuenta registros de identidad asociados a una corrida; `published_artifacts` cuenta los que tienen una copia de los mismos bytes en el repositorio; `referenced_artifacts` cuenta los que sólo están documentados. `artifact_layout` registra la disposición relativa de las salidas y no garantiza que esa carpeta esté publicada.

[metricas_registradas.csv](metricas_registradas.csv) conserva los campos de las tablas de resultados, con su nombre, valor, corrida y archivo de referencia. [configuraciones_y_metricas_S07.json](configuraciones_y_metricas_S07.json) relaciona configuraciones y métricas de las etapas multiclase. Las unidades y los resultados de taxonomías diferentes no se promedian automáticamente.

Para interpretar cada cifra, consultar el [índice de experimentos](../04_experimentos/README.md), el [catálogo de datasets](../03_datasets/README.md) y la [auditoría](../02_auditoria/README.md). Los resultados L1 usan filas/eventos y L2 grupos por huella. Los tiempos de reanudación se distinguen de los tiempos de entrenamiento heredados.

Las curvas M8 de Harvard y DS utilizan 50.000 casos muestreados, mientras sus métricas globales corresponden al test completo. Las configuraciones y metadatos documentan esa diferencia. Las [fuentes de datos](../03_datasets/README.md) permiten preparar nuevas corridas en [Slurm](../07_reproducibilidad/ENTORNO_SLURM.md); las referencias a modelos, predicciones y procesados históricos se consultan en [reproducibilidad](../07_reproducibilidad/README.md).
