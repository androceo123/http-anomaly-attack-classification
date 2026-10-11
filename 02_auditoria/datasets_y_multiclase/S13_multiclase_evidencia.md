# S13: evidencia de M1, M2 y M3

Revisión de solo lectura de la colección de evidencia **S13**, sus configuraciones, métricas, filtrados y logs. El informe documenta la comprobación de SHA-256 de los archivos retenidos. No se cargaron modelos ni se reentrenó. Las cifras siguientes son métricas guardadas leídas, no una nueva evaluación.

Los nombres de rutas identifican los artefactos examinados durante la auditoría. No implican que todos estén publicados en el repositorio. El [índice experimental](../../04_experimentos/README.md) y el [catálogo de corridas](../../06_resultados_consolidados/catalogo_corridas.csv) permiten consultar la disponibilidad por etapa; los [datasets](../../03_datasets/README.md) se descargan desde sus fuentes públicas para preparar nuevas ejecuciones en Arandu/Slurm.

## 1. Identidades confirmadas

| Etapa | Raíz exacta S13 | Job / fecha | Representación y clases |
|---|---|---|---|
| M1 | `DEFINITIVO/multiclase` | 2534, 09/06/2026 | fixed30; TorpEda10, Harvard9 familias |
| M2 | `pipeline14classesResult` | 2657, 19/06/2026 | fixed30; TorpEda10, HarvardTop14 |
| M3 | `corrida3mejoresResultadosPosibles` | 2687, 20/06/2026 | optimized84; TorpEda10, HarvardTop14 |

Cada etapa conserva dos `run_config.json`, uno por corpus, con el mismo job. Los logs indican CPU/OpenMP para HistGradientBoostingClassifier y contienen terminación final: M1 a 17:10:06 del 09/06, M2 a 12:34:12 del 19/06 y M3 a 13:43:28 del 20/06. Los nodos registrados son c2, c2 y c3 respectivamente. Los archivos `.err` son no vacíos y se conservan; no deben descartarse por considerarlos fallos a partir de su extensión.

M1 ya puede vincularse directamente a resultados → configuración → job2534 → nombre `train_waf_multiclass_DEFINITIVO_histgb_fixed30.py`. Ese nombre corresponde al Python preservado en S11, y coincide su lista ordenada de 30 variables. Esta evidencia mejora el estado previo de candidato; sigue sin acreditar el hash histórico del Python ejecutado. M2 registra `pipeline14classes.py`; M3 `corrida3mejoresResultadosPosibles.py`.

El catálogo experimental identifica `pipeline14classesResult` como M2 y asigna únicamente `DEFINITIVO/multiclase` a M1; la rama multietiqueta corresponde a la variante L1 del job 2625.

## 2. Resultados guardados y correspondencia con los informes

| Etapa | Corpus | Variables | Clases | Train / test | Accuracy | F1 macro | MCC |
|---|---|---:|---:|---|---:|---:|---:|
| M1 | torpeda | 30 | 10 | 59306 / 14827 | 99,217643 % | 94,231689 % | 0.986891 |
| M1 | harvard | 30 | 9 | 726252 / 181563 | 95,086003 % | 86,644989 % | 0.918141 |
| M2 | torpeda | 30 | 10 | 59306 / 14827 | 99,217643 % | 94,231689 % | 0.986891 |
| M2 | harvard | 30 | 14 | 721928 / 180483 | 94,879850 % | 80,812802 % | 0.914070 |
| M3 | torpeda | 84 | 10 | 59306 / 14827 | 99,649288 % | 99,369805 % | 0.994125 |
| M3 | harvard | 84 | 14 | 721928 / 180483 | 96,320983 % | 88,831447 % | 0.937551 |

Los valores corresponden al redondeo de las tablas S02: informe02, página3 (M1); informe03, página6 (M2); informe04, página3 (M3). Los informes01/02 siguen siendo versiones documentales de M1, no etapas distintas. Los resultados TorpEda de M1/M2 coinciden numéricamente en estas métricas, pero config/log/timing pertenecen a dos jobs; no fusionar sus eventos.

M1/M2 usan preset `strong`; M3 usa `max`. Las tres etapas dividen por filas 80/20, seed42. TorpEda utiliza `sample_weight_mode=none`; Harvard `sqrt_balanced`. M3 registra `feature_policy=optimized84_intra_request` y `feature_set_version=corrida3_optimized84_v1`. Los seis catálogos de features coinciden en orden con las listas estáticas preservadas S11; los cuatro fixed30 también coinciden con el anexo del libro. Es una comprobación posterior que no cambia el alcance del catálogo inicial.

## 3. Población y etiquetas

TorpEda conserva 74.133 filas y diez clases en M1/M2/M3, con 59.306/14.827 de train/test. Los ocho nombres XML originales se registran en `inputs`, pero esos XML no estaban en la colección examinada. La [guía de TorpEda](../../03_datasets/TorpEda2012/README.md) identifica la fuente de descarga.

M1 Harvard conserva las 907.815 filas, nueve familias y 726.252/181.563 de train/test. Su `harvard_label_mode` es `optimized-family`, con resolución `severity`. El filtro de frecuencia mínima 20 no elimina filas. Familias/conteos guardados: NORMAL 525.195; SQLi 249.227; DataManipulation 57.618; CommandInjection 22.013; CRLFi 19.204; PathTraversal 18.047; HTTPProtocolManipulation 13.262; VulnerabilityScanning 2.413; PasswordAttack 836. No son nueve columnas CAPEC originales.

M2/M3 usan `top14-combo`:907.815→902.411, excluyendo 5.404 eventos de 46 combinaciones. Mantienen las mismas 14 combinaciones exactas admitidas y el split 721.928/180.483. Las tablas de clases permitidas y combinaciones descartadas están presentes. M3 agrega archivos de importancia por clase y NORMAL/ataque, relevantes para la selección posterior de 58 variables de M4; se conserva la historia de consulta a prueba.

## 4. Qué contiene y qué no contiene S13

El inventario de S13 registra 722 entradas: 622 archivos y 100 directorios, con 7.508.810.812 bytes de contenido. Las raíces examinadas son DEFINITIVO, resultsOptimo_extra_lgbm_weights, resultsOptimo_extra_lgbm, resultsOptimo, pipeline14classesResult y corrida3mejoresResultadosPosibles. Es el universo de revisión, no un recuento de los archivos publicados en Git.

**No incorpora los brutos TorpEda, DS-Augmented-v2 ni CSIC.** No hay XML/DB ni nombres/rutas de sus ficheros fuente identificados; todos los basenames CSV/Parquet revisados corresponden a métricas, búsquedas, predicciones o datos procesados. La ausencia se comprobó sobre el inventario completo de la colección.

Tampoco aparecen los basenames `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py`. S13 solo conserva dos scripts: `DEFINITIVO/multietiqueta/run_DEFINITIVO_multilabel_harvard_xgboost_none_fixed30_arandu.sh` y `DEFINITIVO/multietiqueta/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30.py`. Ninguno reemplaza las dependencias faltantes por identidad de nombre.

## 5. Integración

El [JSON de evidencia S13](S13_multiclase_evidencia.json) contiene las seis configuraciones resumidas con sus métricas y filtrados, marcadores de log con línea, comprobaciones de características y un mapa de los archivos de las tres ramas examinadas. La publicación de cada artefacto debe distinguirse de su inclusión en ese inventario. Las raíces resultsOptimo permanecen identificadas como selección, antecedentes y variantes; no se convierten automáticamente en M1/L1 final.

Los nuevos vínculos M1–M3 mejoran trazabilidad sin convertir las evaluaciones exploratorias en pruebas independientes. Deben actualizarse las frases anteriores que decían que solo había nombre de envío o código candidato, preservando la limitación de identidad exacta del código histórico.
