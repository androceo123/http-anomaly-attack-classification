# CSIC 2012 / TorpEda

Los artefactos usan los alias `TorpEda`, `TorpEda2012` y `torpeda`. Esta ficha identifica los XML de entrada, las rutas de preparación en Arandu y el universo registrado por las corridas. El corpus completo se descarga de su fuente pública y se mantiene fuera del repositorio.

## Descarga y formato

Utilizar el [directorio de datos de DuckDuckBug/cnn_waf](https://github.com/DuckDuckBug/cnn_waf/tree/master/data). Los archivos de peticiones del corpus están específicamente en [**`data/torpeda`**](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda), separados en tres grupos:

| Directorio público | Archivos necesarios |
|---|---|
| [`normals`](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda/normals) | `allNormals1.xml` |
| [`anomalies`](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda/anomalies) | `allAnomalies1.xml`, `allAnomalies2.xml` |
| [`attacks`](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda/attacks) | `allAttacks1.xml`, `allAttacks2.xml`, `allAttacks3.xml`, `allAttacks4.xml`, `allAttacks5.xml` |

Esta es una réplica comunitaria de CSIC. La [especificación original de TORPEDA](https://recsi2012.mondragon.edu/es/programa/recsi2012_submission_73.pdf) describe peticiones HTTP en XML con etiquetas de tipo normal, anómala o ataque y su categoría. Las muestras inspeccionadas de la réplica contienen `dataset author="CSIC" name="Tienda2012"`, elementos `sample`, `request` y `label`, coherentes con ese formato. Las carpetas `torpeda_csv` y `torpeda_train_test` del mismo repositorio contienen representaciones derivadas y no son las entradas XML usadas por estos pipelines.

La revisión del repositorio público identificada el 10 de octubre de 2026 es `e35143352ae224abbaca4edf8f9d36e24f7df683`. Registrar la revisión y los hashes de los archivos que se utilicen; la coherencia de formato no demuestra igualdad byte a byte con la entrada histórica. También se conserva como referencia el [sitio institucional de TORPEDA](https://www.tic.itefi.csic.es/torpeda/).

## Preparación para Arandu y Slurm

Descargar los ocho XML en el almacenamiento de trabajo del clúster. Las [configuraciones históricas](../../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/3datasetsMulticlase2/multiclase/torpeda/run_config.json) sitúan sus nombres directamente en `/home_data/aroman/TFG/waf-ml-starter/data/raw/torpeda/`. Para una ejecución nueva, adaptar el directorio al espacio asignado y configurar `TORPEDA_RAW_DIR` en el lanzador correspondiente.

Conservar todos los campos de petición y las etiquetas nativas antes de aplicar los filtros del experimento. La categoría `ANOMALOUS` se mantiene diferenciada de las familias de ataques en la formulación multiclase. El parser, las reglas de filtrado y la representación de atributos deben corresponder a la misma etapa; no intercambiar matrices de 30, 58, 72 o 73 atributos.

La [guía del entorno Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md) explica cómo adaptar rutas y recursos antes de enviar un trabajo mediante `sbatch`. Registrar los hashes de entrada, la configuración, las clases admitidas, los tamaños de las particiones y el identificador de job de la nueva ejecución.

## Universo documentado y clases

En las corridas comparadas de M7/M8, el corpus contiene **74.133 registros**, con 59.306 para desarrollo y 14.827 para prueba. La [auditoría de datasets y multiclase](../../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) documenta diez clases:

| Clase | Registros históricos |
|---|---:|
| NORMAL | 8.363 |
| ANOMALOUS | 16.459 |
| SQLi | 43.013 |
| XSS | 4.818 |
| SSI | 451 |
| BufferOverflow | 412 |
| CRLFi | 327 |
| XPath | 175 |
| LDAPi | 74 |
| FormatString | 41 |

Estos conteos corresponden a las entradas procesadas de las corridas documentadas y deben comprobarse de nuevo si se descarga otra revisión. El bajo soporte de algunas clases exige conservar las métricas por clase y sus denominadores, además de accuracy y F1 macro.

## Corridas relacionadas y alcance

El [índice experimental](../../04_experimentos/README.md) relaciona B2 (comparación binaria por corpus), M1 (fixed30), M7 (58 atributos), M8 (72 atributos) y la extensión posterior de 73 atributos. La [evidencia de multiclase](../../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.md) y la [revisión de Slurm](../../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) precisan las configuraciones y ejecuciones disponibles.

En M8, las curvas de TorpEda utilizan el conjunto de prueba de 14.827 registros. Las curvas de Harvard y DS-Augmented-v2 se produjeron sobre muestras de 50.000; sus métricas globales tienen otros denominadores. La comparación de corpus corresponde a modelos entrenados independientemente y no constituye por sí misma una evaluación de transferencia entre corpus.
