# Evidencia material de las corridas multietiqueta L1 y L2

## Resultado de la revisión

Los artefactos de S06 permiten identificar y verificar dos resultados principales: **L1 fixed30, job 3151, por filas originales**, y **L2 request90, job 3315, por grupos de peticiones**. Las métricas guardadas coinciden con las recalculadas desde las predicciones de test, tanto en el resumen global como en los conteos por CAPEC y en la decisión NORMAL/ataque derivada. También coinciden los percentiles de latencia y los rendimientos calculados a partir de los registros operativos.

La reconstrucción de las particiones reproduce los índices y su orden en los archivos de test, los identificadores de muestra, sus etiquetas y los soportes por CAPEC de todos los bloques. En L2, las seis comparaciones entre train, tune, calibration y test tienen **cero índices y cero huellas compartidas**. Los archivos de particiones que produce esta revisión son reconstrucciones nuevas, claramente identificadas: no se encontraron listas históricas completas independientes de los cuatro bloques.

Hay además un antecedente L1 distinto: **job 2625, GPU, junio de 2026**, respaldado inicialmente por uno de los informes TEX y su log Slurm. La revisión posterior de S13 recuperó su configuración, métricas, modelo, checkpoints y entrenador original, y localizó sus predicciones y procesado dentro del ZIP. Su resultado no debe sustituir el de job 3151 ni mezclarse con L2. El complemento `S13_L1_2625.md` incluye el estado final de extracción y hashes, sin presentar un nuevo recálculo de sus predicciones.

La revisión se hizo sin cargar modelos `.joblib`/pickle, sin importar módulos experimentales y sin reentrenar. Se leyeron JSON, CSV, TEX y código; se inspeccionaron constantes mediante AST y se ejecutó únicamente el nuevo programa de auditoría `verificar_multietiqueta.py`.

## 1. Fuentes y unidades de referencia

Las rutas abreviadas de este documento son relativas a `organizacion_tesis`:

| Alias | Ruta de origen | Función |
|---|---|---|
| L1 | `extraidos/S06/DEFINITIVO/multietiqueta/multiquetaSalidaXG/` | Artefactos del resultado L1 principal. |
| L1 padres | `extraidos/S06/DEFINITIVO/` y `.../multietiqueta/` | Manifiestos, comparación consolidada y logs de intentos. |
| L2 | `extraidos/S06/multietiquetaCorrida2/harvard/` | Artefactos del resultado L2 principal. |
| L2 padres | `extraidos/S06/multietiquetaCorrida2/` | Checkpoints, manifiestos, comparación consolidada y logs. |
| Código | `extraidos/S11/` | Diez scripts/lanzadores multietiqueta y CSV raw compartido. |
| Informes | `extraidos/S04/` | Dos informes TEX correspondientes a variantes L1. |
| Antecedente recuperado | `extraidos/S13/DEFINITIVO/multietiqueta/` | Variante job 2625 GPU, incorporada en la revisión complementaria. |
| Evidencia Slurm | `extraidos/S01/evidencia_tesis_slurm_20260803T142006/` | Logs preservados, metadatos y copias exactas de código. |
| Libro | `analisis/libro_catalogo.json`, fuente PDF `08282026v4.pdf` | Catálogo de identidades y afirmaciones del texto. |
| Presentación | `analisis/presentacion_corridas.json`, fuente `cambiosAndres (1).pptx` | Diapositivas reales 1–71; L1/L2 en D47–48 y D69. |

S06 contiene **165 archivos, 1.084.033.861 bytes** expandidos. De ellos, 75 corresponden a la familia L1 y 90 a L2. El mapa `multietiqueta_mapping.json` cubre los 165, más los diez scripts/lanzadores multietiqueta de S11 y los dos TEX de S04: **177 registros**, sin archivos S06 pendientes de clasificación. S11 raw es compartido y está tratado por la auditoría de datasets. El mapa complementario `S13_L1_2625_mapping.json` incorpora **63 entradas adicionales** de la variante histórica, 54 bajo `harvard/`; las 63 fueron descomprimidas y tienen SHA-256; se conservan 62 y se omite una caché Python regenerable.

### Fila original y grupo son universos diferentes

| Universo | Conteo | Evidencia |
|---|---:|---|
| Filas originales SR-BH del CSV disponible | 907.815 | `analisis/sr_bh_raw_profile.json`; lectura streaming del CSV S11. |
| Normales / ataques en filas originales | 525.195 / 382.620 | Mismo perfil; NORMAL no coexiste con CAPEC en una fila original. |
| Filas con los quince campos HTTP vacíos | 2 | Índices originales 0-based 14.410 y 163.884. |
| Filas válidas utilizadas para agrupar L2 | 907.813 | Auditoría original L2 y suma independiente de tamaños de grupo. |
| Grupos L2 | 542.990 | CSV procesado L2; todas las huellas guardadas son únicas. |
| Grupos NORMAL / con alguna CAPEC | 171.348 / 371.642 | Recuento de targets en el CSV procesado. |
| Grupos test L2 | 108.598 | Predicciones guardadas. |

L1 trabaja con las 907.815 filas. L2 consolida por huella antes de dividir, une etiquetas mediante OR y conserva una fila representativa por grupo. Esta unión conserva etiquetas observadas en miembros del grupo; **no demuestra que todos esos ataques aparecieran simultáneamente en cada evento original**. CAPEC-248 se excluye como target por su soporte de uno, sin eliminar su fila por ese solo motivo. NORMAL se deriva de no activar ninguna de las doce CAPEC conservadas. Las métricas binarias que acompañan estas salidas son derivadas del modelo multietiqueta y pertenecen a L1/L2, no a B1/B2. [Libro: PDF pp. 48, 57–58, 67–69, 82–86; presentación D45, D47–48; informes de filtrado de L1/L2.]

## 2. Identidad de corridas, variantes e informes

| Identidad | Evidencia material | Resultado/interpretación |
|---|---|---|
| L1 principal, job 3151 | `L1/run_config.json`, `environment.SLURM_JOB_ID=3151`; log `definitivo_multilabel_harvard_xgboost_gpu_c2_3151.out`; métricas completas | fixed30; doce XGBoost OvR; CPU, `gpu_used=false`; reanuda estados previamente calculados. |
| Intentos L1 3104 y 3150 | Logs del mismo árbol `DEFINITIVO/multietiqueta/logs/` | Preservar como intentos separados. El estado terminal de cada job corresponde a la evidencia Slurm; un log incompleto no basta para declarar fallo. |
| Antecedente L1, job 2625 | S04 `informe_modelo_multietiqueta_revisado (1).tex`; log S01 por job 2625; S13 `DEFINITIVO/multietiqueta/harvard/run_config.json` y resultados | GPU; script antiguo sin `_gpu_metrics`, recuperado en S13; salida histórica `DEFINITIVO/multietiqueta/harvard/`; métricas diferentes del principal. |
| Informe L1 principal | S04 `informe_DEFINITIVO_multilabel.tex` | Sus resultados coinciden con job 3151 y el árbol actual `multiquetaSalidaXG`. Describe también un antecedente; no convertir esas menciones en artefactos encontrados. |
| L2 principal, job 3315 | `L2/run_config.json`; log `multietiquetaCorrida2_3315.out`; métricas completas | request90; doce XGBoost con tuning por CAPEC; CPU; nodo c3; sin refit después de calibration. |

El antecedente 2625 queda vinculado por datos precisos: su `.out` S01 identifica el script sin `_gpu_metrics` en la línea 6, el inicio del 16/06 en la 50, el resultado en la 67 y las salidas `DEFINITIVO/multietiqueta/harvard/` en las 71–72. Registra exact-match `0.9648276355865457`, F1 micro `0.9526020129515487`, F1 macro `0.836362595139409` y GPU activa, valores que coinciden con el TEX revisado. Esos artefactos no estaban en S06, pero **S13 recuperó la variante real**: modelo de 15.131.386 bytes, configuración con `SLURM_JOB_ID=2625`, resultados y 26 checkpoints; el ZIP contiene además predicciones de 84.242.821 bytes y Parquet de 29.582.551 bytes, descomprimidos y verificados por SHA-256 al completar la organización. El entrenador original sin sufijo, ausente de los diez archivos S11, también apareció en S13 con SHA-256 `8c48d777281fe325579bc61610aac52c4df969022a8573e19703fc46654d6663`.

El nombre de archivo no determina hardware: L1 principal conserva `gpu` en varios nombres, pero la ejecución seleccionada informa `gpu_used=false`. El alias de log L2 `slurm-multietq_c2-3315.*` tampoco determina el nodo: el contenido registra c3.

El SHA-256 del contenedor S04 `informesMultilabel.zip` coincide con el ancla del libro: `1a1fe9cd6bc75b15ccd414775ad39bf62c547038aa6a70b78cf2613160a7763c`. Que el informe L1 cite otro contenedor antiguo con un inventario mayor no acredita que ese contenedor antiguo sea idéntico al S06 actual.

## 3. Código, versiones e integridad

El archivo `multietiqueta_codigo_y_hashes.json` incluye los diez archivos de código, sus SHA-256 y las rutas de sus copias exactas S01. Los principales son:

| Uso | Archivo S11 | SHA-256 | Estado de vinculación |
|---|---|---|---|
| L1 principal | `train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30_gpu_metrics.py` | `7d1bb308166aaa83bc61e48e2cee0470fc290279dc7a2534e11e06b9b36212d0` | Nombre en `run_config`; copia S01 idéntica. La configuración L1 no guarda un hash histórico del script. |
| L2 principal | `multietiquetaCorrida2.py` | `1120c44776ebd75ad65c98fa2c69a11a4ed086c9f6a6a81d69d2e085c0619ecb` | Coincide exactamente con el hash del libro y la copia S01. |
| Lanzador L2 | `multietiquetaCorrida2.sh` | `ef2891d4cfc1e87626df220661c990b8fe6dab09ed3202ca3695e9f3e810da08` | Coincide exactamente con el hash del libro y la copia S01. |

El complemento S13 agrega el entrenador histórico `DEFINITIVO/multietiqueta/train_waf_multilabel_DEFINITIVO_harvard_xgboost_none_fixed30.py` y su lanzador `run_DEFINITIVO_multilabel_harvard_xgboost_none_fixed30_arandu.sh`. Su configuración y sus resultados corresponden a job 2625; no son reemplazos del entrenador S11 de job 3151. Los hashes y la correspondencia están en `S13_L1_2625_mapping.json`.

Otros cinco lanzadores S11 pertenecen a la familia L1 y apuntan al entrenador principal o a su salida: los tres `run_DEFINITIVO_multilabel...` y `run_resume_multilabel_xgb_cpu_c2.sh`/`...c3.sh`. Se preservan como versiones de lanzamiento: no se atribuye automáticamente cada archivo actual al job 3151. En particular, el default de GPU en un lanzador no debe sustituir los argumentos efectivamente guardados.

`train_waf_multilabel_multifamily_resume_resultsOptimo_fixed30.py` y su lanzador `run_multilabel_harvard_multifamily_resume_resultsOptimo_arandu_safe_fixed30.sh` son antecedentes de búsqueda multifamilia. No son el entrenador definitivo identificado por L1 principal ni por L2.

La inspección AST confirma que las **30 características L1, las 30 base L2 y sus 60 añadidas coinciden en nombre y orden con el apéndice del libro**. Las noventa de L2 coinciden además con `run_config.json`. La serialización original del esquema sí pudo aclararse leyendo el código: SHA-256 de UTF-8 de `version + "\n" + "\n".join(features_en_orden)`. El resultado es `0bbc812611513de0952653b398f5533afa6933d32faf3cbfa8ac88ac12a8e51f`, igual al de la configuración y el libro. [L2 código, líneas 198–202; libro PDF p. 101.]

**No confundir las firmas.** El `input_signature` L2 `f74df5d8f0787c37b888aa960337450b71a526767120efacfc8d8b951d9eb686` se calcula sobre una lista JSON con ruta resuelta, tamaño y `mtime_ns`; no es el SHA-256 de los bytes del CSV. El CSV raw disponible tiene SHA-256 `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910`, pero ese hash de contenido no aparece como ancla histórica en `run_config` L2. Las firmas de preprocesado, entrenamiento, calibration y esquema también deben conservar su significado separado. [L2 código, líneas 836–845; `analisis/hashes_fuentes_y_S11.json`.]

## 4. Verificación de métricas desde predicciones

Se compararon las columnas `true_*`, `pred_*` y `score_*` de los CSV de test contra `test_metrics_multilabel.json`, `per_label_metrics.csv` y los umbrales del JSON completo. Todos los conteos por CAPEC y todas las métricas globales verificadas coinciden; las diferencias numéricas admitidas son solo de representación de punto flotante. Los reportes detallados registran los resultados y las tolerancias.

| Medida recalculada | L1: filas | L2: grupos |
|---|---:|---:|
| Tamaño test | 181.563 | 108.598 |
| Conjunto exacto correcto | 175.264 | 105.253 |
| Exact-match | 0,965306808105 | 0,969198327778 |
| F1 micro | 0,953290456701 | 0,976042921712 |
| F1 macro | 0,834976684071 | 0,939399313718 |
| F1 ponderado | 0,950669563717 | 0,974976520976 |
| Hamming loss | 0,003300048284 | 0,002761714458 |
| Decisiones CAPEC erróneas | 7.190 | 3.599 |
| Jaccard micro | 0,910749751738 | 0,953206870100 |
| AP macro, campo original `pr_auc_macro` | 0,841690157487 | 0,962599308259 |
| ROC-AUC macro | 0,993777934082 | 0,998902154052 |
| Exact-match solo entre ataques | 70.882 / 76.524 = 0,926271496524 | 71.328 / 74.328 = 0,959638359703 |
| Recall de NORMAL | 104.382 / 105.039 = 0,993745180362 | 33.925 / 34.270 = 0,989932885906 |
| CAPEC con F1 ≥ 0,85 | 9 de 12 | 10 de 12 |

La comparación L1–L2 cambia unidad de evaluación, representación, consolidación de etiquetas, ajuste y protocolo. No es una ablación aislada de request90 ni una estimación causal del beneficio de eliminar duplicados. [Libro PDF pp. 82–86; presentación D47–48.]

### Matrices binarias derivadas

| Corrida | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| L1 | 104.382 | 657 | 4.369 | 72.155 |
| L2 | 33.925 | 345 | 2.438 | 71.890 |

L2 no alcanza literalmente el objetivo NORMAL de 99%: faltan tres grupos normales correctamente reconocidos para llegar al entero mínimo que cumple el umbral. F1 de CAPEC-153 es `0.8086303939962477` y de CAPEC-272 `0.5803503427265804`; las otras diez CAPEC alcanzan 0,85. Estos incumplimientos coinciden con `target_attainment.csv`, por lo que deben estar visibles junto al resultado principal.

### Precisión al volver a leer los CSV

Las predicciones guardadas se reproducen con `score >= threshold` usando el `float32` original. El parser por defecto de pandas puede desplazar mínimamente un decimal guardado justo en el umbral: una primera lectura produjo 1.880 diferencias de decisiones L2. Leer con `float_precision="round_trip"` elimina esas diferencias; aplicar además el dtype `float32` usado por el código original también da cero. **Era un problema del procedimiento de lectura de la auditoría, no una incoherencia de los artefactos**. El auditor guardado ya usa la lectura correcta, y el diagnóstico se conserva en el JSON de verificación. [Código L2, líneas 4494–4496; `L2_verificacion.json`, `numeric_reading_note`.]

## 5. Particiones y evidencia de auditoría de contenido

### Particiones reconstruidas y contrastadas

| Corrida | Train | Tune/validación | Calibration | Test | Regla |
|---|---:|---:|---:|---:|---|
| L1 | 581.001 | 145.251 | No separado | 181.563 | Filas; split test semilla 42, validación 43; refit posterior con train+validación. |
| L2 | 347.513 | 43.439 | 43.440 | 108.598 | Grupos; semillas 42, 43 y 44; sin refit posterior. |

Se reprodujo de forma independiente la regla de estratificación leída en el código, incluyendo el fallback entre firma de etiquetas, etiqueta primaria y normal/ataque. Para estos datos, los pasos seleccionan **etiqueta primaria**. Se verificó que las particiones cubren todo el universo, que las listas test coinciden en conjunto y orden con el CSV y que coinciden todos los soportes positivos de cada bloque registrados en la configuración.

`selected_model_summary.txt` L2 conserva `valid_rows=86879`, suma de tune y calibration. No significa que se ajustaron hiperparámetros y umbrales sobre un único bloque; los dos tamaños específicos constan en `run_config.json` y el JSON completo.

| Pares L2 | Índices compartidos | Huellas compartidas |
|---|---:|---:|
| Train / tune | 0 | 0 |
| Train / calibration | 0 | 0 |
| Train / test | 0 | 0 |
| Tune / calibration | 0 | 0 |
| Tune / test | 0 | 0 |
| Calibration / test | 0 | 0 |

L1 tiene cero intersecciones de índices entre sus tres bloques, algo distinto de independencia por contenido. El libro informa **76.966 de 181.563 filas test L1 con huella presente en desarrollo (42,3908%)**. Esta revisión no volvió a calcular las huellas de todas las filas raw para reconstruir ese porcentaje histórico: conserva la afirmación del libro y el alcance de la comprobación efectivamente realizada. Un índice único puede corresponder a una petición repetida en otra fila. [Libro: auditoría de solapamiento; presentación D51–53; `L1_intersecciones_recalculadas.csv`.]

Los NPZ nuevos contienen solo arrays de índices y pueden leerse con `allow_pickle=False`. Sus nombres incluyen `particiones_reconstruidas` para que nunca se presenten como listas encontradas entre los artefactos originales.

### Reconciliación interna de agrupación L2

La lectura de `processed_request90_multilabel.csv` confirma 542.990 huellas únicas y una suma de `duplicate_group_size` de 907.813 filas válidas. Hay 27.623 grupos con tamaño mayor que uno, 364.823 filas adicionales al representante y tamaño máximo 453. El conjunto de huellas repetidas y cada tamaño coinciden exactamente con `request_duplicate_groups.csv`.

En ese catálogo hay 288 grupos con desacuerdo de etiquetas y 284 con conflicto NORMAL/ataque. Son los conteos de `request_deduplication_audit.json`. Estos resultados verifican la consistencia entre **artefactos procesados**; no reemplazan una nueva ejecución de BLAKE2b sobre cada una de las quince columnas raw ni una reconstrucción íntegra de OR desde cada evento original. Se conserva esta frontera para no presentar una comprobación interna como verificación independiente de toda la transformación.

La huella declarada es BLAKE2b-128, versión `request-canonical-blake2b128-v1`, sobre método, URI, versión HTTP, once cabeceras de petición y cuerpo, con normalización y orden definidos. No incluye timestamp, IP/puertos o campos de respuesta. Su igualdad expresa identidad operativa bajo esas reglas; no equivalencia universal de todas las peticiones HTTP. [Auditoría JSON L2; libro PDF pp. 50–51, 67.]

## 6. Tuning, calibración, checkpoints y reanudación

Los 192 registros de `xgb_tuning_trials_by_label.csv` tienen estado `ok`; se identifica exactamente un seleccionado por cada CAPEC. Nueve CAPEC tienen doce ensayos y CAPEC-153, 272 y 274 tienen 28 cada una. Se conservan tanto `xgb_best_params_by_label.csv` como los resúmenes tune y calibration, los umbrales por bloque y el recorrido de optimización conjunta. `calibration_fallback_labels.json` está vacío. Los umbrales de test se leen de la calibración final; `thresholds_validation.csv` de L2 es alias exacto del de tuning, no del de calibration.

Los estados serializados conservados no son duplicados exactos del modelo final:

| Grupo de evidencia | Cantidad `.joblib` | Bytes |
|---|---:|---:|
| Checkpoints L1 | 26 | 56.471.628 |
| Checkpoints L2 | 25 | 40.685.211 |
| Antecedente L1 job 2625, recuperados en S13 | 26 | 55.709.900 |

Se recomienda conservarlos en `90_artefactos_pesados`, manteniendo el árbol interno. L1 guarda candidatos entrenados antes del refit, estados por etiqueta de selección y refit, y bundle de refit final. El log 3151, líneas 52–59, confirma que reutilizó procesado, candidato y refit final. El modelo final permite inferencia, pero no sustituye el estado del candidato evaluado en validación antes del refit.

L2 conserva candidato, records por etiqueta y pares `progress.json`/`best_estimator.joblib` para los ensayos. El cargador requiere ambos cuando hay ensayos exitosos; borrar el estimador conservando solo progress rompe esa vía de reanudación. Los CSV conservan parámetros y resultados, pero no los árboles entrenados en el formato esperado por la reanudación. Esta conclusión procede de lectura del código, no de deserialización. [L2 código, líneas 3238–3268; construcción del modelo final, líneas 5792–5823.]

## 7. Tiempos y alcance de las medidas

| Medida | L1, filas/eventos | L2, grupos |
|---|---:|---:|
| Casos medidos individualmente | 181.563 (test completo) | 10.000 (muestra del test) |
| Latencia p50 | 9,293012 ms | 7,124564 ms |
| Latencia p95 | 9,839666 ms | 7,627084 ms |
| Latencia p99 | 10,251287 ms | 8,083367 ms |
| Preparación + predicción individual | 106,979221 casos/s | 138,928758 grupos/s |
| Preparación + predicción por lote | 3.344,959850 casos/s | 1.832,262068 grupos/s |
| Solo predicción por lote | 25.974,380813 casos/s | 65.010,936694 grupos/s |
| RSS máximo del programa | 3.920,859375 MiB | 4.098,558594 MiB |
| Modelo final | 15.327.435 bytes (14,617381 MiB) | 13.561.468 bytes (12,933224 MiB) |

Los percentiles se recalcularon con interpolación lineal de NumPy sobre los CSV de latencias. Los rendimientos se verificaron como cantidad medida dividida por el tiempo de su fase. El tiempo de pared del bucle individual incluye una pequeña sobrecarga y por eso no es exactamente la suma de las latencias: L1 1.697,180047 s frente a 1.696,553067 s; L2 71,979338 s frente a 71,949097 s.

L1 guarda tiempos **heredados de checkpoints**: selección original `20343.918032862246 s` en el resumen del candidato y refit `21648.2045269832 s`, frente a `run_total_seconds=1930.4524821676314` de la reanudación que vuelve a evaluar y medir. El log confirma el reuse. No deben sumarse como si todos fueran fases ejecutadas dentro del job 3151, ni presentar su `train_select_seconds=0.665832806378603` actual como coste de entrenar desde cero.

L2 registra `train_select_seconds=1922.6299338527024`, `final_refit_seconds=0` y `run_total_seconds=2317.4098239205778`. El total del programa, la duración Slurm, tiempos de CPU, extracción, predicción y benchmark son magnitudes distintas. L2 informa 16 hilos asignados y 32 núcleos visibles; su porcentaje CPU calculado sobre todos los visibles no es directamente el porcentaje de la asignación. El nombre histórico de clave `throughput_req_s` se conserva en la fuente, pero al presentar L2 la unidad correcta es **grupos/s**. Estos benchmarks locales no miden solicitudes concurrentes de un WAF desplegado.

## 8. Duplicados exactos y organización recomendada

`multietiqueta_duplicados_exactos.json` identifica 44 grupos SHA-256 relevantes entre S01/S04/S06/S11. Incluye rutas de todas las copias; las del snapshot Slurm pueden conservarse íntegras para no romper su manifiesto. Los grupos no vacíos repetidos dentro de S06 son:

| Corrida | Archivos idénticos |
|---|---|
| L1 | `metrics_flat.csv` y comparación CSV del padre. |
| L1 | `candidate_validation_summary.csv` y `.partial.csv`. |
| L2 | `metrics_flat.csv` y comparación CSV del padre. |
| L2 | `candidate_tuning_summary.csv`, `candidate_validation_summary.csv` y `.partial.csv`. |
| L2 | `candidate_tuning_summary.json` y `candidate_validation_summary.json`. |
| L2 | `target_attainment.csv` y `target_attainment_f1_85_normal_99.csv`. |
| L2 | `thresholds_tuning.csv` y `thresholds_validation.csv`. |
| L2 | Las dos copias `.out` del job 3315 y, por separado, las dos `.err`. |

Las versiones JSON `.partial` no son idénticas a las definitivas: no descartarlas solo por su nombre. `test_predictions.csv` y `request_level_multilabel_match.csv` L1 tampoco son copias exactas. Los archivos vacíos comparten hash aunque tengan distinto significado; no consolidarlos a ciegas.

Cada corrida debe reunir su README, configuración, métricas globales/por etiqueta, matrices cuando existan, tuning/calibración, cobertura e importancias, medidas operativas, manifiestos y enlaces al código exacto y a los registros Slurm. Los binarios y CSV grandes se conservan en el espejo pesado, con ubicación registrada. Los análisis de contenido y las particiones reconstruidas también deben aparecer en `02_auditoria`, enlazando a sus fuentes y al mapa de la corrida. Mantener los informes TEX separados por variante evita contaminar L1 principal con los números GPU de junio.

## 9. Evidencia faltante o alcance pendiente

- No se encontraron listas originales completas e independientes de train/validación/tune/calibration. Las listas nuevas son reconstrucciones verificadas contra test y todos los soportes conservados.
- No se recalcularon huellas de todas las filas raw ni OR por todos los miembros; tampoco el porcentaje de solapamiento histórico L1. Sí se comprobaron unicidad, intersecciones y conciliación del procesado y del catálogo de grupos.
- No se encontró un mapa histórico completo fila raw → huella/grupo como archivo independiente. El CSV procesado conserva representante, tamaño e identidad; raw, código y auditoría permiten una futura reconstrucción explícita.
- No se cargó ningún modelo. Los SHA-256 y tamaños comprueban integridad de bytes, no que el pickle pueda cargarse con cualquier versión o que reentrene idénticamente.
- El Parquet L1 se preservó e inventarió, pero no se decodificó en este entorno. Para reconstruir etiquetas y splits L1 se utilizó la matriz de etiquetas obtenida del CSV raw en orden original, contrastando test y los soportes guardados.
- No hay CSV de probabilidades por caso de tune y calibration entre los artefactos revisados que permita recalcular de manera independiente sus métricas sin ejecutar modelos. Se preservan sus tablas, trazas y resúmenes como evidencia original.
- El hash histórico de bytes del CSV raw no está en la configuración L2; `input_signature` no cubre esa función. Para L1 tampoco existe allí hash histórico del entrenador.
- El faltante anterior de job 2625 se resolvió mediante S13: modelo, checkpoints, configuración, resultados y código extraídos; predicciones y procesado localizados en el ZIP. Los dos archivos grandes quedaron descomprimidos y verificados por SHA-256; no se recalculó test desde esas predicciones. El Parquet idéntico al de job 3151 se consolidó por hash, conservando ambas procedencias; las predicciones y modelos distintos siguen separados.

## 10. Entregables de esta revisión

- `analisis/multietiqueta_mapping.json`: 177 originales con corrida, variante, rol, categoría, unidad, estado, SHA-256 y copias exactas.
- `analisis/multietiqueta_codigo_y_hashes.json`: identidad de diez archivos, cotejo del apéndice y cálculo del esquema.
- `analisis/multietiqueta_duplicados_exactos.json`: grupos de identidad binaria y política de alias.
- `analisis/verificar_multietiqueta.py`: auditor independiente de CSV/JSON y reconstrucción de splits, sin ejecución de entrenadores.
- `analisis/multietiqueta_verificacion/`: resultados por corrida, resumen con entorno, métricas por CAPEC, tablas de intersección y NPZ de particiones reconstruidas.
- `analisis/README_L1_fixed30.md` y `analisis/README_L2_request90.md`: textos preparados para las carpetas de experimentos.
- `analisis/S13_L1_2625.md`, `S13_L1_2625_mapping.json` y `S13_L1_2625_verificacion.json`: recuperación y cotejo de la variante GPU, con estado explícito de extracción y límites de la verificación complementaria.

Las fuentes originales permanecen sin cambios. Este documento describe lo verificado y lo que debe conservar la organización; no afirma que los archivos originales inexistentes se hayan recuperado ni que se haya repetido el entrenamiento.
