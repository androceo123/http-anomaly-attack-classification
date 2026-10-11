# Índice de experimentos y trabajos Slurm

Las etapas se identifican por su objetivo, representación, taxonomía y evidencia. Este índice enlaza el código y las auditorías publicados; los catálogos también conservan la identidad de salidas históricas que no están disponibles en el repositorio. Una referencia en el inventario no implica que el archivo pueda descargarse desde aquí.

El [catálogo de corridas](../06_resultados_consolidados/catalogo_corridas.csv) distingue archivos catalogados, copias publicadas de los mismos bytes y referencias sin archivo publicado. Las cifras corresponden a registros del catálogo de identidades, no a nuevos experimentos. La [guía Slurm](../07_reproducibilidad/ENTORNO_SLURM.md) explica cómo preparar y enviar una nueva corrida.

| Etapa | Propósito | Código relacionado | Evidencia |
| --- | --- | --- | --- |
| [B1](#b1) | Ablación binaria RF en CSIC | [Ver implementación](../05_codigo/base_binaria_historica/waf-ml-starter/jobs) | [Auditoría](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) |
| [B2](#b2) | Comparación binaria por corpus | [Ver implementación](../05_codigo/base_binaria_historica/waf-ml-starter/jobs/run_compare_binary.sh) | [Auditoría](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) |
| [M1](#m1) | Modelo base de 30 atributos; Harvard 9 familias y TorpEda 10 clases | [Ver implementación](../05_codigo/pipelines/train_waf_multiclass_DEFINITIVO_histgb_fixed30.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M2](#m2) | Top-14 de combinaciones CAPEC y 30 atributos | [Ver implementación](../05_codigo/pipelines/pipeline14classes.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M3](#m3) | Expansión a 84 atributos | [Ver implementación](../05_codigo/pipelines/corrida3mejoresResultadosPosibles.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M4](#m4) | Poda a 58 atributos y Top-14 | [Ver implementación](../05_codigo/pipelines/corrida3mejoresResultadosPosibles_featuresUtiles58.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M5](#m5) | Taxonomía operativa de 11 clases | [Ver implementación](../05_codigo/pipelines/11claseResults.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M6](#m6) | 10 clases con Request Manipulation | [Ver implementación](../05_codigo/pipelines/10claseResults.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M7](#m7) | Tres corpus y 58 atributos | [Ver implementación](../05_codigo/pipelines/3datasetsMulticlase.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [M8](#m8) | Tres corpus y 72 atributos | [Ver implementación](../05_codigo/pipelines/3datasetsMulticlase2.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [L1](#l1) | Multietiqueta fixed30; resultado principal job 3151 | [Ver implementación](../05_codigo/pipelines/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30_gpu_metrics.py) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) |
| [L1_2625](#l1_2625) | Variante previa GPU de L1; job 2625 | [Ver implementación](../05_codigo/pipelines/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30_gpu_metrics.py) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/S13_L1_2625.md) |
| [L2](#l2) | Multietiqueta request90 por grupos; job 3315 | [Ver implementación](../05_codigo/pipelines/multietiquetaCorrida2.py) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) |
| [EXP73](#exp73) | Extensión posterior de 73 atributos; job 3361 | [Ver implementación](../05_codigo/pipelines/3datasetsMulticlase3.py) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [OC](#oc) | Antecedentes one-class en CSIC | [Ver implementación](../05_codigo/base_binaria_historica/waf-ml-starter/jobs) | [Auditoría](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) |
| [PRE_MC](#pre_mc) | Selección multiclase preliminar resultsOptimo | [Ver implementación](../05_codigo/README.md) | [Auditoría](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) |
| [PRE_XGB](#pre_xgb) | Selección multietiqueta preliminar; ganador local XGBoost sin ponderación | [Ver implementación](../05_codigo/README.md) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) |
| [PRE_LGBM](#pre_lgbm) | Selección multietiqueta LightGBM sin ponderación | [Ver implementación](../05_codigo/README.md) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) |
| [PRE_LGBM_W](#pre_lgbm_w) | Selección multietiqueta LightGBM con ponderaciones; ganador local cuberoot | [Ver implementación](../05_codigo/README.md) | [Auditoría](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) |

La implementación enlazada es una versión relacionada con la etapa. La identidad exacta de los bytes ejecutados sólo se atribuye cuando la evidencia conserva el hash correspondiente. Los lanzadores y los nombres históricos mantienen sus diferencias.

## B1

**Ablación binaria RF en CSIC.** Ablación RF-25, RF-33, RF-57 y RF-10-Gini en CSIC. RF34 es un alias histórico de 33 atributos; no corresponde al conjunto de 34 de OCSVM.

[Consultar evidencia](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) · [Código relacionado](../05_codigo/base_binaria_historica/waf-ml-starter/jobs)

## B2

**Comparación binaria por corpus.** Entrenamientos binarios independientes para CSIC, TorpEda y SR-BH. Se consultó prueba para seleccionar umbrales; el nombre cross_dataset no acredita transferencia de un modelo entre corpus.

[Consultar evidencia](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) · [Código relacionado](../05_codigo/base_binaria_historica/waf-ml-starter/jobs/run_compare_binary.sh)

## M1

**Modelo base de 30 atributos; Harvard 9 familias y TorpEda 10 clases.** fixed30: nueve familias Harvard y diez clases TorpEda. La revisión vincula las configuraciones al job2534.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/train_waf_multiclass_DEFINITIVO_histgb_fixed30.py)

## M2

**Top-14 de combinaciones CAPEC y 30 atributos.** Treinta atributos y catorce combinaciones exactas CAPEC. Configuraciones y logs vinculados al job2657.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/pipeline14classes.py)

## M3

**Expansión a 84 atributos.** Expansión a 84 atributos. Configuraciones y logs vinculados al job2687; la selección posterior de atributos tuvo carácter exploratorio.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/corrida3mejoresResultadosPosibles.py)

## M4

**Poda a 58 atributos y Top-14.** Poda a 58 atributos manteniendo Top14. Las métricas fueron contrastadas con las predicciones en la auditoría S09.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/corrida3mejoresResultadosPosibles_featuresUtiles58.py)

## M5

**Taxonomía operativa de 11 clases.** Taxonomía operativa de once clases Harvard con 58 atributos. Se mantiene separada de Top10.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/11claseResults.py)

## M6

**10 clases con Request Manipulation.** Diez clases Harvard, con RequestManipulation. Los informes citan job2966 y las configuraciones S07 job3013; la misma etapa metodológica no identifica un único evento.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/10claseResults.py)

## M7

**Tres corpus y 58 atributos.** Tres corpus y 58 atributos. Configuración registrada para job3068. Los modelos se entrenan por corpus.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/3datasetsMulticlase.py)

## M8

**Tres corpus y 72 atributos.** Tres corpus y 72 atributos, job3289. Las curvas de Harvard y DS usan muestras de 50.000 casos; las tablas globales usan el test completo.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/3datasetsMulticlase2.py)

## L1

**Multietiqueta fixed30; resultado principal job 3151.** Resultado principal fixed30, job3151. Usa filas/eventos y reanuda estados previos; el tiempo del job no es el tiempo de entrenar desde cero. La separación de índices no elimina las coincidencias de contenido.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) · [Código relacionado](../05_codigo/pipelines/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30_gpu_metrics.py)

## L1_2625

**Variante previa GPU de L1; job 2625.** Variante previa de L1, job2625 con GPU. Sus resultados se distinguen de los del job3151.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/S13_L1_2625.md) · [Código relacionado](../05_codigo/pipelines/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30_gpu_metrics.py)

## L2

**Multietiqueta request90 por grupos; job 3315.** Resultado principal request90, job3315, CPU. Agrupa peticiones por huella y separa entrenamiento, selección, calibración y prueba. Las particiones de verificacion_20261010 son reconstrucciones identificadas como tales.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) · [Código relacionado](../05_codigo/pipelines/multietiquetaCorrida2.py)

## EXP73

**Extensión posterior de 73 atributos; job 3361.** Extensión de 73 atributos, job3361. Harvard conserva Top10 y DS utiliza nueve clases nativas. Cambian representación, clases y política de pesos; no es una ablación de una única variable sobre M8 ni una etapa M9 del libro.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/pipelines/3datasetsMulticlase3.py)

## OC

**Antecedentes one-class en CSIC.** Antecedentes one-class en CSIC con protocolos y representaciones diferentes. La revisión Slurm distingue intentos, fallos y resultados preservados.

[Consultar evidencia](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) · [Código relacionado](../05_codigo/base_binaria_historica/waf-ml-starter/jobs)

## PRE_MC

**Selección multiclase preliminar resultsOptimo.** Búsquedas preliminares multiclase. Verificar la versión de cada Python: el motor preliminar v10 no está publicado con el nombre que espera su lanzador.

[Consultar evidencia](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) · [Código relacionado](../05_codigo/README.md)

## PRE_XGB

**Selección multietiqueta preliminar; ganador local XGBoost sin ponderación.** Selección preliminar multietiqueta cuyo ganador local fue XGBoost sin ponderación. La selección y los checkpoints se documentan en la auditoría.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) · [Código relacionado](../05_codigo/README.md)

## PRE_LGBM

**Selección multietiqueta LightGBM sin ponderación.** Selección preliminar LightGBM sin ponderación; no se mezcla con el resultado final L1/L2.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) · [Código relacionado](../05_codigo/README.md)

## PRE_LGBM_W

**Selección multietiqueta LightGBM con ponderaciones; ganador local cuberoot.** Selección preliminar LightGBM con ponderaciones; ganador local cuberoot según la evidencia registrada.

[Consultar evidencia](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md) · [Código relacionado](../05_codigo/README.md)

## Datos y resultados de una nueva ejecución

Obtener los corpus desde sus [fuentes públicas](../03_datasets/README.md), respetar el formato que espera el pipeline y registrar la versión y las huellas. Cada corrida nueva utiliza un directorio propio para configuración, métricas, predicciones, modelos y logs. Los archivos de una ejecución nueva no sustituyen a las identidades históricas del inventario.

Las métricas conservan su unidad: L1 evalúa eventos y L2 grupos por huella. El recálculo requiere los artefactos indicados en la [guía de reproducibilidad](../07_reproducibilidad/README.md); descargar el dataset original no proporciona por sí solo predicciones, checkpoints o modelos históricos.
