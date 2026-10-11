# Alcance de la auditoría experimental

**Trabajo:** Detección y clasificación de ataques en tráfico HTTP mediante enfoques binario, multiclase y multietiqueta.

**Fecha de la revisión documentada:** 10 de octubre de 2026.

**Entorno experimental:** clúster Arandu, con ejecución y asignación de recursos mediante Slurm.

## 1. Qué permite comprobar el repositorio

La auditoría relaciona los resultados de la tesis con los corpus, las representaciones HTTP, las configuraciones, los trabajos Slurm, los registros de ejecución y las versiones de código examinadas. La lectura de archivos y el recálculo de métricas se distinguen de una nueva ejecución experimental. Esta documentación no acredita un reentrenamiento de los modelos.

Las colecciones de evidencia se identifican mediante los códigos **S01–S14**. Sus inventarios conservan nombres históricos, tamaños, SHA-256, clasificación y vínculos con las corridas. Esos códigos identifican conjuntos de material examinado, no trabajos Slurm ni directorios que deban existir en una instalación nueva. El [inventario de archivos](inventario_archivos.csv) y el [catálogo de colecciones](fuentes_originales.csv) describen ese alcance histórico. La presencia de una entrada en un inventario no garantiza que el artefacto esté publicado en Git.

La captura de Slurm del 03/08/2026 permanece como evidencia histórica. Las explicaciones de sus inconsistencias se registran por separado, para mantener los bytes y los manifiestos originales. Las fichas e índices permiten consultar los materiales presentes y reconocer los resultados que sólo están documentados en los informes de auditoría.

## 2. Entradas de consulta

| Sección | Contenido y propósito |
| --- | --- |
| [Documentación](../../01_documentacion/README.md) | Libro, presentación, antecedentes y catálogos de afirmaciones. |
| [Auditoría](../README.md) | Duplicados, conflictos de etiquetas, particiones, coherencia de métricas, ejecución e integridad. |
| [Datasets](../../03_datasets/README.md) | Fuentes públicas de descarga, alias de corpus, taxonomías, esquemas y reglas de preparación. |
| [Experimentos](../../04_experimentos/README.md) | Índice de etapas, variantes y antecedentes con disponibilidad de evidencia. |
| [Código](../../05_codigo/README.md) | Programas de entrenamiento y lanzadores; base binaria histórica y variantes posteriores. |
| [Resultados consolidados](../../06_resultados_consolidados/README.md) | Corridas y métricas con su fuente, denominador y unidad de medida. |
| [Reproducibilidad](../../07_reproducibilidad/README.md) | Entorno, requisitos, verificadores y límites de reproducción. |

Los corpus se descargan desde los enlaces identificados en la guía de datasets. Los datos crudos, modelos y checkpoints no se incluyen automáticamente por estar citados en un informe. Para repetir una etapa se deben reunir sus entradas, identificar la versión de código y comprobar sus dependencias y recursos.

## 3. Identidad de etapas y trabajos Slurm

| Etapa | Descripción | Vínculo documentado |
| --- | --- | --- |
| B1 | Ablación binaria Random Forest en CSIC | Scripts y envíos compatibles; el vínculo de cada cifra final requiere respetar el alcance del informe binario. |
| B2 | Comparación binaria por corpus | Scripts y registros de ejecución; no se equipara por nombre a cualquier salida binaria. |
| M1 | Modelo de 30 atributos; Harvard 9 familias y TorpEda 10 clases | Configuraciones y logs S13: job 2534, 09/06/2026. |
| M2 | Top-14 de combinaciones CAPEC y 30 atributos | Configuraciones y logs S13: job 2657, 19/06/2026. |
| M3 | Expansión a 84 atributos | Configuraciones y logs S13: job 2687, 20/06/2026. |
| M4 | Poda a 58 atributos y Top-14 | Job 2766; comprobación de métricas desde predicciones S09. |
| M5 | Taxonomía operativa de 11 clases | Job 2927; se distingue el intento previo 2883 terminado por tiempo. |
| M6 | Diez clases con Request Manipulation | El informe cita 2966; las configuraciones de resultados identifican 3013. Se conserva la discrepancia. |
| M7 | Tres corpus y 58 atributos | Configuraciones de resultados: job 3068. |
| M8 | Tres corpus y 72 atributos | Configuraciones de resultados: job 3289. |
| L1 | Multietiqueta fixed30, por eventos | Resultado principal CPU, job 3151; reanudación con checkpoints. |
| L1_2625 | Variante previa de L1 | Job 2625 con GPU; modelos y métricas distintos de L1 principal. |
| L2 | Multietiqueta request90, por grupos | Job 3315, con selección y calibración separadas. |
| EXP73 | Extensión posterior de 73 atributos | Job 3361; el log registra el SHA-256 del Python. |
| OC y PRE_* | Antecedentes one-class y búsquedas de selección | Se identifican como antecedentes; no se convierten en resultados principales por semejanza de nombre. |

M1–M8 reflejan la evolución multiclase del libro y la presentación. Los informes 01 y 02 corresponden al mismo tramo M1. EXP73 es una extensión posterior y no se presenta como una etapa M9 de los documentos examinados. El [catálogo de corridas](../../06_resultados_consolidados/catalogo_corridas.csv), el [catálogo de jobs](../historial_slurm/catalogo_jobs.csv) y la [revisión de M1–M3](../datasets_y_multiclase/S13_multiclase_evidencia.md) detallan esas correspondencias.

## 4. Evidencia científica comprobada

### Duplicados, conflictos y particiones

El CSV de referencia Harvard auditado contiene **907.815 eventos y 38 columnas**. La auditoría distingue duplicados de eventos completos de las coincidencias bajo una huella de quince campos HTTP. L2 excluye dos peticiones vacías y consolida los 907.813 eventos restantes en **542.990 grupos**. Esos recuentos describen una versión identificada por hash; una descarga posterior debe contrastarse con esa identidad.

La revisión S10 recontó 27.624 grupos repetidos con los vacíos incluidos, 392.448 eventos dentro de esos grupos y 364.824 excedentes. Registró 288 grupos con variación de etiquetas y 284 con presencia normal/ataque. La unión OR de L2 conserva las etiquetas observadas en el grupo; no adjudica mediante revisión humana qué etiqueta era correcta.

Las cuatro particiones L2 reconstruidas contienen **347.513 grupos de entrenamiento, 43.439 de selección, 43.440 de calibración y 108.598 de prueba**. Coinciden los índices y su orden en prueba, etiquetas, huellas y soportes. Las seis intersecciones dan cero bajo la identidad documentada. Los archivos de particiones están marcados como reconstrucciones porque no se encontraron listas históricas completas de los cuatro bloques.

Para L1 se verificaron índices, orden y soportes. El 42,3908 % histórico de coincidencias por huella entre prueba y desarrollo procede del libro; no se presenta como un nuevo recálculo completo del CSV. Separar índices de fila no demuestra independencia del contenido. Véanse la [revisión de datasets](../datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md), la [verificación S10](../datasets_y_multiclase/S10_auditoria_excel_recalculado.json) y las verificaciones de [L1](../particiones_y_multietiqueta/verificacion_20261010/L1_verificacion.json) y [L2](../particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json).

### Resultados, metas y unidades

Los reportes L1 y L2 documentan el recálculo de métricas desde predicciones, scores y umbrales, sin cargar modelos ni reentrenar. Para M4/M5 se recalcularon accuracy, balanced accuracy, F1 macro y MCC sobre cuatro CSV de predicciones: las dieciséis comparaciones coinciden. Otras etapas se verificaron mediante lectura de configuraciones, métricas y logs; ese alcance no equivale a repetir todos los experimentos.

L2 obtiene F1 micro 0,976042922, F1 macro 0,939399314 y exactitud de conjunto 0,969198328. CAPEC-153 alcanza F1 0,80863039 y CAPEC-272 0,58035034, por debajo de la meta 0,85. NORMAL reconoce 33.925 de 34.270 casos, **98,9932886 %**; faltan tres aciertos para cumplir estrictamente el 99 %. El redondeo a 99,0 % no acredita cumplimiento exacto.

Los benchmarks distinguen predicción, preparación, procesamiento por lote, duración Slurm y trabajo reanudado. La unidad L2 es el **grupo de peticiones**, aunque ciertas claves históricas contengan `req_s`. Los tiempos de checkpoints L1 no se suman como si todo el entrenamiento hubiera ocurrido dentro del job 3151. Las curvas M8 de Harvard y DS-Augmented-v2 usan muestras de 50.000 eventos; las tablas globales usan los conjuntos de prueba completos. TorpEda usa sus 14.827 eventos completos en ambas vistas. Los [resultados M4/M5](../datasets_y_multiclase/S09_multiclase_recalculado.json) y la [revisión multietiqueta](../particiones_y_multietiqueta/multietiqueta_evidencia.md) conservan el detalle.

## 5. Entorno e integridad

La captura S01 incluye 133 jobs seleccionados, 369 registros de jobs y pasos y logs de 26 jobs. Sus estados son 57 COMPLETED, 55 FAILED, 9 TIMEOUT y 12 CANCELLED. No representa todo el historial del clúster. La tabla histórica que marca 133 scripts batch como `recuperado` contradice los 133 mensajes de error y la ausencia de scripts recuperados; esa limitación permanece visible.

Los manifiestos internos dan **167/167 coincidencias** para código, configuración y resultados del proyecto y **389/390** para el manifiesto global. En la excepción, el hash histórico coincide con los primeros 1.111 bytes del log; los 187 bytes finales se añadieron al cerrar la auditoría. Se conserva el registro original y la explicación.

El inventario del 03/08/2026 describe Slurm 24.11.5, AlmaLinux 9.4, Xeon Gold 6242 y Tesla V100 de 16 GB. Es una captura fechada, no prueba del entorno exacto de cada job anterior. El HEAD Git de esa captura tampoco acredita retrospectivamente el commit ejecutado en cada entrenamiento. Los nombres que contienen `gpu` no determinan el uso de GPU: lo establecen las configuraciones y los logs. Véanse la [revisión Slurm](../historial_slurm/REVISION_SLURM_Y_BINARIO.md) y la [guía de Arandu/Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md).

## 6. Límites y requisitos de reproducción

Las colecciones auditadas no contenían los brutos identificados de CSIC, TorpEda y DS-Augmented-v2. Sus entradas deben obtenerse desde las [fuentes públicas de datasets](../../03_datasets/README.md) y prepararse conforme a los programas. El CSV Harvard auditado tiene una identidad de contenido registrada; no se incorpora al repositorio por el hecho de citarla.

Tampoco se localizaron los nombres exactos `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py` referenciados por dos lanzadores preliminares. Las versiones con otros nombres no se declaran sustitutos históricos. Los [criterios de conservación](CRITERIOS_DE_LIMPIEZA.md) registran además qué estados de selección preliminar no se retuvieron.

La auditoría no establece generalización temporal, transferencia entre corpus, resultados con múltiples semillas ni rendimiento de un WAF desplegado. Las etapas exploratorias conservan su historia de consulta a prueba y cambios de representación o taxonomía. La separación por grupos L2 verifica la regla de identidad y la reconstrucción descritas, sin extenderse a esos otros alcances.
