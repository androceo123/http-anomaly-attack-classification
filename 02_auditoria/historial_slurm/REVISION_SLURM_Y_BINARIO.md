# Revisión de evidencia Slurm y base binaria: S01 y S05

Fecha de revisión: 10 de octubre de 2026. Alcance: lectura e integridad de las colecciones de evidencia S01 y S05, sin ejecutar entrenamientos. Los códigos B/M/L se contrastaron con el [catálogo de la presentación](../../01_documentacion/catalogos/catalogo_presentacion.json); los vínculos por nombre no se presentan como identidad demostrada de resultados.

S01 corresponde a la [captura histórica de Arandu/Slurm del 03/08/2026](evidencia_20260803/). S05 identifica la base binaria y sus antecedentes documentales. Los conteos de este informe describen el material examinado durante la auditoría; su inclusión en un inventario no garantiza que cada archivo esté publicado. La [guía de Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md) conecta la evidencia del clúster con los requisitos de nuevas ejecuciones.

## 1. Resultado y decisión de organización

**Conservar S01 completo como evidencia de auditoría, con vistas e índices por corrida/job.** Sus 391 archivos ocupan solamente 11.034.112 bytes. Los errores pequeños, salidas vacías, intentos fallidos y copias redundantes documentan la cobertura y los límites de la reconstrucción; no constituyen basura por su extensión o tamaño.

**Conservar S05 como versión histórica de código y documentación.** Sus 100 archivos ocupan 15.254.541 bytes. Contiene 21 scripts de jobs y 49 archivos en `waf-ml-starter`, pero no los datasets ni resultados masivos descritos por sus documentos. No usar esa raíz como implementación única para todas las corridas: tiene cuatro rutas de código/dependencias distintas de la captura posterior S01.

El archivo [revision_slurm_y_binario.json](revision_slurm_y_binario.json) ofrece un mapeo de **cada uno de los 491 archivos** examinados, con categoría, corrida, rol, confiabilidad, decisión, ubicación, job, SHA-256, duplicados y evidencia. Incluye además los 133 jobs con sus registros y pasos, los 13 enlaces de `run_config.json`, comprobaciones de integridad y cobertura de scripts. Las rutas sugeridas conservan cada raíz fuente; los índices de corridas permiten relacionar los archivos sin desarmar los árboles ejecutables.

## 2. Función de cada colección de evidencia

| Fuente/carpeta | Qué demuestra | Tratamiento recomendado |
|---|---|---|
| S01 `sacct/` | Solicitudes, asignaciones, estados, fechas, `SubmitLine`, rutas y pasos de los jobs seleccionados | Conservar íntegra en auditoría histórica. |
| S01 `job_ids_tesis.txt` y script extractor | Universo exacto de 133 jobs consultados y método de extracción | Conservar; evita confundir selección con historial completo del cluster. |
| S01 `batch_scripts_recuperados/` | Intentos de recuperación y contradicción entre tabla y archivos reales | Conservar los 133 `.err` y `resultado.tsv`; añadir explicación derivada, sin corregir fuentes. |
| S01 `logs_preservados/` | Evidencia de 26 jobs: comandos, entrenamiento, reanudaciones, errores, finales y auditorías | Conservar con índice por job. Hay 59 archivos y 37 contenidos distintos, porque existen copias y salidas idénticas. |
| S01 `inventario_actual_nodos/` | Hardware y software observados el 03/08/2026, con cuatro capturas interrumpidas | Separar del entorno histórico por corrida; conservar errores y parciales. |
| S01 `slurm_actual/` | Estado del controlador, nodos, particiones y comandos en la auditoría | Conservar como captura fechada, sin retrotraerla a cada ejecución. |
| S01 `proyecto_actual/copias/` | Código actual candidato y resultados textuales disponibles al auditar | Conservar árbol. Relacionar resultados con jobs mediante `run_config`; versionar variantes de código. |
| S01 manifiestos, inventarios y estado Git | Procedencia y límites de identidad del código; comprobaciones SHA-256 | Conservar como evidencia central. |
| S05 `waf-ml-starter/jobs`, `src`, configuración y dependencias | Implementación histórica binaria/one-class, con rutas y dependencias relativas | Conservar raíz ejecutable completa e indexar por B1/B2/antecedentes. |
| S05 informes Markdown y `Justificaciones/` | Decisiones históricas, protocolos y evolución metodológica | Conservar con fecha/estado histórico; no hacerlos pasar por protocolo final. |
| S05 `libroTFG`, `revisiones `, `libroLatex.txt`, propuesta | Evolución documental, correcciones y propuesta previa | Archivar como versiones históricas. Normalizar el nombre de carpeta destino `revisiones` y registrar su espacio final original. |
| S05 `LibrosMetodologia/` y `libroNicoRalf.pdf` | Bibliografía de consulta | Mantener sus referencias bibliográficas; la consulta del texto completo depende de su fuente editorial. |
| S05 `latex/propuesta/aux_files/` | Compilación y algunas copias de dependencias | Material regenerable. `.bib`, `thesis.cls` y `spanish.dtx` allí duplican archivos fuera de `aux_files`. |

Los `__init__.py` vacíos y marcadores de directorios de datos tienen función estructural. No eliminarlos porque compartan el hash del contenido vacío con un log. Dos salidas idénticas de jobs distintos tampoco equivalen al mismo evento.

## 3. Historia Slurm y límites de recuperación

### Cobertura

`sacct_jobs_asignacion.psv` conserva **133 jobs**, desde el envío del 27/05/2026 hasta ejecuciones terminadas el 24/07/2026. `sacct_jobs_y_steps.psv` contiene **369 filas de jobs y pasos**, por lo que no deben contarse como 369 ejecuciones independientes. El script consulta una lista fija de IDs dentro de un período amplio; esta es la cobertura seleccionada de la auditoría, no todo el historial de Arandu.

Estados de los 133 jobs: **57 COMPLETED, 55 FAILED, 9 TIMEOUT y 12 CANCELLED**. Hay **16 jobs sin nodo asignado y sin inicio**. Para estos últimos, hardware usado debe ser «No aplica: no recibió nodo», como indica el LEEME original. No convertir una solicitud de recursos en consumo medido.

Se conservaron logs de **26 de los 133 jobs**. Para los otros 107, la ausencia de log en esta captura indica un límite de evidencia, no un diagnóstico de éxito/fracaso adicional al estado que conserva `sacct`.

### Inconsistencia de recuperación de scripts batch

`batch_scripts_recuperados/resultado.tsv` marca **133 veces `recuperado`**. Sin embargo:

- No existe ningún `.sh` recuperado en esa carpeta.
- Existen 133 archivos `job_<id>.err` de 54 bytes, todos con el mismo contenido: `job script retrieval failed: Invalid job id specified`.
- Su SHA-256 común es `d46c9a59de43b199cecee7a5013528718fcaf2579e64af09ec7b5410e327e27e`.
- `slurm_actual/scontrol_jobs_retenidos.txt` registra que no había jobs retenidos en el sistema al consultar.
- El extractor preservado, líneas 346–354, decide éxito por el retorno de `scontrol write batch_script`; no valida que el `.sh` exista y contenga un script.

La tabla original **no acredita recuperación de los scripts**. Su resultado es compatible con un falso positivo del procedimiento basado únicamente en retorno del comando; no quedó registrado un código de salida separado para reconstruir cada llamada. Debe añadirse una tabla derivada con `recuperado_verificado=false` para los 133 IDs y conservar la tabla original contradictoria. El mensaje no permite concluir por sí solo un problema de permisos.

### Integridad de manifiestos

La revisión documentó el recálculo de SHA-256 de los **491 archivos** y su coincidencia con el inventario de archivos examinado. Al contrastar con los manifiestos históricos internos:

- `proyecto_actual/hashes_codigo_config_y_resultados.sha256`: **167/167 coincidencias**.
- `manifest_sha256.txt`: **389/390 coincidencias**; el único distinto es `ejecucion_auditoria.log`.
- El hash histórico del log coincide **exactamente con sus primeros 1.111 bytes**. Los **187 bytes finales** son el mensaje «Auditoria terminada…» y las rutas de salida, añadidos después del cálculo del manifiesto. El orden se observa en el extractor, líneas 484–495.

Registrar esta excepción comprobada por agregado posterior, conservando ambos hashes y tamaños. No describirla sin más como corrupción ni modificar el manifiesto original para ocultarla.

## 4. Mapa de jobs a etapas/corridas

La confianza de cada fila distingue tres cosas: pertenencia a una etapa, vínculo entre job y resultados conservados, e identidad exacta del código ejecutado. No son equivalentes.

| Corrida/etapa | Jobs relevantes | Evidencia y alcance del vínculo |
|---|---|---|
| B1, ablación RF CSIC | 2476 baseline; 2496 (`rf_25feat`), 2497 (`rf_34feat`), 2498 (`rf_top10`) | `sacct.SubmitLine` y scripts S05 compatibles. No hay logs/resultados directos de estos jobs en S01. Identidad con cifras finales pendiente de cruce con otras colecciones. |
| B2, RF por dataset | 2528 TorpEda, 2529 Harvard; 2530 comparación; 2476 posible baseline CSIC | Código/orden de envío compatibles con la comparación. La presentación advierte que no bastan para identificar sus cifras finales. |
| M1, selección y modelo base fixed30 | 2490/2491 TorpEda; 2499/2508/2515 y 2518→2531 Harvard; 2534 HistGB definitivo | Conservar como selección previa y candidato M1. La presentación no identifica un script/job único M1. No elegir entre allmodels y definitivo por el nombre. |
| M2, Top14/30 | 2657 `pipeline14classes.sh` | Nombre de script en `SubmitLine` y código actual con fixed30/Top14; no batch original ni resultado M2 en esta captura. |
| M3, optimized84/Top14 | 2687 `corrida3mejoresResultadosPosibles.sh` | `SubmitLine` y `FEATURE_SET_VERSION=corrida3_optimized84_v1` en la copia actual. Mismo límite de identidad histórica. |
| M4, useful58/Top14 | 2766 `...featuresUtiles58.sh` | `SubmitLine` y política `useful58_intra_request` en la copia; no resultado directo de ese job en S01. |
| M5, Top11 operativo/58 | 2883 TIMEOUT; 2927 COMPLETED, `11claseResults.sh` | Dos intentos de la misma etapa; código actual `useful58_operational_groups_v1`. No presentar ambos como corridas completas independientes. |
| M6, Top10 Request Manipulation/58 | 3013, precedido por 2963–2966/3009–3012 y errores del helper 2960/2962 | Los dos `10claseResults/.../run_config.json` contienen `SLURM_JOB_ID=3013`; los intentos previos se conservan aparte. |
| M7, tres datasets/58 | 3068, precedido por 3046/3053/3065–3067 | Los tres `3datasetsMulticlase/.../run_config.json` identifican 3068. |
| M8, tres datasets/72 | 3289 | Tres `run_config.json` identifican 3289; `3datasetsMulticlase2.py` y versión useful72 coinciden con la presentación. |
| L1, variantes fixed30 | 2625 GPU; 3101/3102 cancelados; 3104 CPU TIMEOUT; 3150 cancelado; 3151 CPU reanudado | Los logs distinguen `DEFINITIVO/multietiqueta/harvard` de `.../multiquetaSalidaXG`. El `run_config` conservado en esta última carpeta identifica 3151. No fusionar variantes como si fueran una misma ejecución. |
| L2, request90 | 3315 `multietiquetaCorrida2.sh` | `run_config`, log con comando completo y métricas identifican directamente el job y su carpeta; coincide con la presentación. |
| Extensión de 73 features | 3296/3305 TIMEOUT; 3331/3332/3357 cancelados; 3358 COMPLETED; 3359/3360 fallidos; 3361 COMPLETED | Hay resultados propios y tres configuraciones con job 3361. El log imprime SHA-256 del Python y coincide con el archivo preservado. Conservar como extensión posterior `3datasetsMulticlase3`, sin asignarle automáticamente el código M9 que no aparece en la presentación analizada. |
| Preparación de Egipcios | 3045 | Log de exportación `DS_Augmented_v2_csv`; está `export_db_to_csv.py`, pero falta el batch `run_db_to_csv.sbatch` en S01/S05. |
| Auditoría Harvard | 3442/3443/3444/3445 fallidos; 3446 COMPLETED; 3453 fallido; 3454 COMPLETED | Logs describen errores de rutas y ejecución posterior de auditoría CSV/Excel. Conservar la secuencia completa. |

Las filas M1–M3 describen el alcance específico de S01/S05. La [revisión complementaria S13](../datasets_y_multiclase/S13_multiclase_evidencia.md) aporta configuraciones, métricas y logs que vinculan directamente M1 con 2534, M2 con 2657 y M3 con 2687. Ese avance de trazabilidad no establece el hash histórico de los Python ejecutados.

**Reanudación L1 documentada:** el job 3104 llega al entrenamiento/refit pero termina por tiempo durante la medición operativa; el job 3151 reutiliza datos procesados, candidato y refit final desde checkpoints y termina. Su duración de 32:44 no equivale al costo completo de entrenamiento desde cero. El log 3151 identifica esas tres reutilizaciones explícitamente.

**Variantes L1 numéricamente distintas:** el job 2625 registra `gpu_used=True`, F1 macro de test `0.836362595139409` y salida `.../harvard`; el job 3151 registra `gpu_used=False`, F1 macro de test `0.834976684071172` y salida `.../multiquetaSalidaXG`. Mantener variantes y orígenes separados hasta que el cruce con el libro determine cuál sustenta cada tabla.

**Código exacto excepcionalmente acreditado:** el log job 3361 registra SHA-256 `c930f2a2b7a02d054c11d6a2f6693fec915b238fd9513fea25923dcc4b47efb4` para `3datasetsMulticlase3.py`; coincide con la copia de S01. Esto acredita identidad de ese Python, no del batch ausente ni de todas las dependencias.

## 5. Entornos, comandos y dependencias

Separar tres capas: historial `sacct`, entorno capturado por la propia corrida (`run_config`/logs), e inventario del 03/08. El estado Git de S01 lo dice expresamente: su HEAD actual `7ce11321526c07146ba2bff22294849444a15152` **no prueba el commit histórico de cada job**. Además muestra archivos modificados y numerosos scripts sin seguimiento.

El inventario actual registra Slurm 24.11.5, AlmaLinux 9.4, 32 CPU lógicas, Xeon Gold 6242 y Tesla V100 de 16 GB en las tres máquinas examinadas. El Python de shell era 3.9.18 y el de `.venv` 3.11.7. Estos son datos de la captura; no extrapolarlos a mayo-julio.

Los inventarios c1 CPU/GPU y c3 CPU/GPU terminan por TIME LIMIT antes del `pip freeze`. Los dos de c2 conservan 199 líneas `paquete==version`. El inventario venv informa `matplotlib=3.11.0`, mientras el requirements S01 fija `3.10.9`. Un requirements describe dependencias declaradas, no garantiza que coincidan con las instaladas ni funciona como prueba de entorno histórico completo.

No usar nombres de job terminados en `gpu` como prueba de GPU utilizada. Job2534 declara HistGradientBoosting CPU; job 3151 conserva `gpu3` en su nombre pero configura `USE_GPU=off`. Las asignaciones `ReqTRES/AllocTRES` tampoco prueban utilización efectiva.

Conservar `sacct_jobs_y_steps.psv` completo. Por ejemplo, en job 2529 el wrapper `.batch` registra MaxRSS 5.904 K, mientras el paso Python `2529.1` registra 9.764.792 K; usar solamente `.batch` ocultaría la memoria del entrenamiento. Tampoco sumar sin distinguir la fila agregada del job y sus pasos.

Se observaron 55 nombres de scripts enviados; **16 no tienen copia con ese basename en S01/S05**. El JSON enumera cada caso. Para los otros 39, la coincidencia de basename solo identifica un candidato: algunos envíos apuntan a la raíz y la copia S05 está en `jobs/`.

Los jobs S05 suelen cambiar a `$SLURM_SUBMIT_DIR` y usar `.venv/bin/python3.11`, `PYTHONPATH=src` y rutas relativas `data/...` y `results...`. **Mantener `waf-ml-starter` como unidad**. Los índices por corrida pueden referenciar su script; trasladarlo solo a una carpeta B1/B2 sin su raíz rompería esas relaciones.

Hay fechas con offset explícito `-04:00` en nodos/configuraciones y `-03:00` en la bitácora de auditoría; `sacct` conserva fechas sin offset textual. Guardar valores originales y no comparar cadenas de hora como si todas tuvieran la misma zona.

## 6. Hallazgos de auditoría metodológica en S05

El protocolo del 02/06/2026 usa IDs **E01–E08**, que no equivalen automáticamente a B1/B2/M1–M8/L1/L2. `resultados_pi1_csic.md` también reutiliza E01/E02 con otro sentido. Preservar el documento y su namespace: no renombrar todas esas menciones al esquema actual. El protocolo histórico incluye alcances y pendientes anteriores a las expansiones documentadas después; esas instrucciones no deben gobernar esta reorganización.

`recalibracion_parametros.md` menciona **job 2463** para el experimento solo_registro, pero la selección `sacct` conserva **job 2462** para ese nombre y no incluye 2463. No corregirlo por suposición; dejar discrepancia pendiente. El informe también presenta una tabla expresamente hipotética antes de una sección de resultados reales: no extraer ambas como mediciones.

`run_csic_rf_34feat.sh` contiene **25 features base + 8 de entropía = 33**, pese al alias34. Conservar alias original y conteo comprobado por separado. `train_binary_rf.py` llama en su línea 380 a `threshold_sweep(y_test, y_prob)`: es evidencia concreta de selección de umbral sobre el test en ese código histórico, no una calibración independiente. La organización no debe retocar ese comportamiento y luego atribuirle los resultados originales.

El README rápido S05 referencia `waf_ml.scripts.train_ocsvm` y `waf_ml.waf.proxy`, que no están en la base histórica examinada. Conservarlo como guía histórica y advertir la incompletitud concreta en el índice de reproducibilidad; no afirmar que el quickstart quedó ejecutado.

En L2 el log registra 907813 filas válidas y 542990 requests únicos, mientras la auditoría posterior 3446/3454 registra 542991 únicos sobre la fuente de 907815 filas. Los universos difieren; conservar las etapas de filtrado/deduplicación. No unificar conteos únicamente porque la fuente se llama Harvard.

## 7. Comparación SHA-256 y evidencia mínima a destacar

Los 491 archivos representan **309 contenidos distintos**, con **37 grupos de duplicados** y 182 ocurrencias adicionales idénticas. Son comparaciones de contenido, no una orden de borrado.

Entre las dos raíces ejecutables hay 15 rutas equivalentes: 11 tienen contenido idéntico y 4 difieren: `requirements.txt`, `src/waf_ml/features/http_features.py`, `src/waf_ml/optimo/ocsvmOptimo.py` y `src/waf_ml/scripts/build_features_csic.py`. La captura S01 cambia el extractor y las features por defecto hacia top25 intra-request y añade controles/cabeceras en CSIC. No reemplazar silenciosamente el extractor histórico que usaban las ablaciones de 57/33/25.

La evidencia que conviene hacer visible desde el README general es:

1. Índice de los 133 jobs, su estado, nodo, comandos registrados y enlaces a 26 con logs.
2. Relación explícita resultado→`run_config`→job para M6/M7/M8/L1/L2 y extensión 73, con variantes/reanudaciones.
3. Límite de recuperación batch y su tabla original contradictoria.
4. Verificación de manifiestos, incluida la excepción exacta del log agregado después.
5. Entornos actuales completos/parciales, separados de evidencia histórica de cada corrida.
6. Mapa de versiones de código y duplicados, conservando todas las procedencias.
7. Lista de datos/dependencias/scripts faltantes y de identidades numéricas aún no acreditadas.

La extensión 73 incluye además huella de entrada Harvard: 436.437.661 bytes y SHA-256 `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910`, útil para contrastar la versión del corpus. No se verificó aquí el contenido de ese dataset porque no pertenece a S01/S05; su perfil figura en la [auditoría de datasets](../datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) y su descarga en la [guía de fuentes públicas](../../03_datasets/README.md).

**Validación efectuada:** integridad de los 491 archivos, cobertura completa del mapeo, relación de 13 configuraciones con jobs, lectura de logs y scripts citados, comparación de 15 rutas equivalentes y de ambos manifiestos históricos. No se ejecutaron entrenamientos, no se instalaron entornos y no se declaró reproducibilidad experimental ejecutada.
