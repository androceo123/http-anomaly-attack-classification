# Auditoría y trazabilidad de la tesis HTTP

## Propósito y alcance

La auditoría es una de las cinco contribuciones explícitas de esta tesis y debe poder consultarse desde la documentación principal. Reúne procedencia de los datos, reglas de preparación, repeticiones y conflictos de etiquetas, separación de particiones, relación entre corridas y trabajos Slurm, integridad de archivos y límites de las conclusiones. El objetivo 4 del libro pide esta trazabilidad; el cierre la enumera como aporte propio. [Libro `08282026v4.pdf`, PDF 21 / p. 5 y PDF 96 / p. 80; presentación D14–16, D26 y D51–53.]

Esta revisión, actualizada el 10 de octubre de 2026, documenta el análisis de evidencia experimental de Arandu/Slurm. Incluye la inspección de la colección S13 y la lectura de sus configuraciones, métricas, filtrados y logs de M1–M3. No se ejecutaron entrenamientos durante las verificaciones documentadas. Las referencias `PDF` usan la página física del libro; `p.` la impresa; `Dxx` el orden real de las 71 diapositivas. **S01–S14 identifican colecciones de evidencia**, descritas en el [catálogo](integridad_y_procedencia/fuentes_originales.csv); no son números de job. Los informes y tablas conservan esos identificadores para que cada afirmación pueda rastrearse.

Los inventarios describen el material examinado por la auditoría. La mención de un archivo original no implica que esté publicado en este repositorio. Los informes de verificación y la captura histórica de Slurm se consultan desde esta sección; el [índice experimental](../04_experimentos/README.md) identifica la disponibilidad por etapa. Los corpus se obtienen desde las [fuentes públicas de datasets](../03_datasets/README.md), y la [guía de Arandu/Slurm](../07_reproducibilidad/ENTORNO_SLURM.md) distingue el entorno capturado de los requisitos de una nueva ejecución.

## 1. Contribuciones declaradas y dónde se sostienen

| Contribución del libro | Evidencia que la hace revisable | Alcance |
|---|---|---|
| Esquema común adaptado a cuatro corpus | Parsers, configuración de entradas, nombres canónicos y alias, diccionario de campos, filtrados y distribuciones por corrida | Se revisaron el libro y código/configuraciones preservados; disponer de un esquema común no significa que todos los corpus tengan la misma distribución. |
| Representaciones de petición HTTP, incluido request90 | Catálogos ordenados de variables, versión, código y firma de esquema; `features_used.csv` por corrida | La firma request90 coincide con código/configuración/libro. Las listas 30, 58, 72, 73 y 90 son versiones diferentes. |
| Auditoría de duplicados, conflictos y solapamientos | Fuente Harvard, S10 Excel y diccionario, S01 scripts/logs, S06 huellas y grupos L2 | Se distinguen duplicados completos de 38 columnas y coincidencias según 15 campos de petición. |
| Reconstrucción de evolución experimental y decisiones | Informes PDF/TEX, historial de cambios de representación y clases, `run_config`, `sacct`, logs, manifiestos y checkpoints | Permite identificar consultas a prueba y reanudaciones. No acredita automáticamente el código histórico exacto de cada job. |
| Evaluación de tres formulaciones y costos | Resultados binarios, multiclase y multietiqueta, métricas por clase/etiqueta y benchmarks por fase | Las métricas operativas pertenecen al entorno y unidad medidos; no son una validación de WAF en producción. |

La enumeración procede de PDF 96 / p. 80. Las diapositivas D15, D20, D26 y D51–53 explican el flujo revisable. El libro marca los objetivos como alcanzados en PDF 91–92 / pp. 75–76: esto describe implementación y evaluación; no convierte en cumplidos todos los umbrales de rendimiento propuestos para L2.

## 2. Matriz de afirmaciones y evidencia

| Afirmación | Referencia documental | Evidencia examinada / verificación documentada | Estado y límite |
|---|---|---|---|
| El archivo Harvard tiene 907.815 eventos y 38 columnas | PDF 48–52 / pp. 32–36; D20, D45–47 | S11 `data_capec_multilabel.csv`; `sr_bh_raw_profile.json` | Recuento de todos los registros y 14 columnas de etiquetas; SHA-256 y tamaño registrados. |
| La fuente tiene 60 combinaciones exactas | PDF 48–49 / pp. 32–33 | S08 `estadisticas harvard.xlsx`, S14 `analisis_combinaciones_capec.xlsx`, perfil CSV | Las 60 combinaciones coinciden exactamente; también 38 pares y 22 ternas S14. |
| Hay dos peticiones vacías y L2 las excluye | PDF 51, 75 / pp. 35, 59; D45–47 | CSV S11; S10 `source_record` 14.411 y 163.885; S06 configuración/auditoría | Vacíos observados en los 15 campos HTTP; índice CSV desde cero 14.410 y 163.884. |
| El extracto S10 contiene 27.624 grupos repetidos | PDF 51–52 / pp. 35–36 | S10 `Duplicados` y `Diccionario_auditoria`; `S10_auditoria_excel_recalculado.json` | Recontadas sus columnas de auditoría: 392.448 eventos, 364.824 excedentes y máximo 453. No se rehicieron todas las huellas del raw. |
| Existen 288 grupos con variación de etiquetas y 284 con normal/ataque | PDF 52 / p. 36; D52 | S10; S06 `request_duplicate_groups.csv` y `request_deduplication_audit.json` | Recontados los indicadores y reconciliados con la tabla L2. OR no decide cuál etiqueta era correcta. |
| L2 conserva 542.990 grupos y 907.813 eventos subyacentes | PDF 75–76 / pp. 59–60; D45–48 | S06 `processed_request90_multilabel.csv`, tamaños y huellas | Huellas procesadas únicas; suma de tamaños y 27.623 grupos repetidos verificadas. |
| Las seis intersecciones L2 son cero | PDF 76, 86 / pp. 60, 70; D45, D47–48, D51–53 | Configuración, procesado, índices de test, particiones reconstruidas y `L2_intersecciones_recalculadas.csv` | Confirmado sobre la reconstrucción semilla 42/43/44; índices/etiquetas/test concuerdan. No se hallaron listas históricas completas de las cuatro particiones. |
| Las divisiones históricas Harvard tenían coincidencias por huella | PDF 86 / p. 70; D41, D45, D52 | Tabla del libro, scripts/logs de auditoría y evidencia histórica | Porcentajes documentados; no se repitieron aquí las cinco auditorías completas del raw. B2 Harvard no fue reconstruida en el libro. |
| El desarrollo consultó resultados de prueba | PDF 68–70, 75–76 / pp. 52–54, 59–60; D27, D34–36, D41–42 | Código B2 `threshold_sweep(y_test, ...)`, regla de poda 58 de M3, cronología y reportes | Evidencia de selección exploratoria; conservarla junto a las métricas. |
| M1–M3 tienen resultados vinculados a configuraciones y jobs concretos | Libro PDF 72–75, 80 / pp. 56–59, 64; D42, D69; S02 informes 02, 03 y 04 | S13 `DEFINITIVO/multiclase`, `pipeline14classesResult` y `corrida3mejoresResultadosPosibles`; configs y logs de los jobs 2534, 2657 y 2687 | Se leyeron seis configuraciones y sus métricas/filtrados. Los logs conservan terminación. No se recalcularon predicciones ni se acreditó el hash histórico del Python ejecutado. |
| Las métricas M4/M5 corresponden a sus predicciones guardadas | PDF 80 / p. 64; D42, D69 | S09 cuatro CSV de predicciones y `metrics_flat.csv` | Recalculadas accuracy, balanced accuracy, F1 macro y MCC: 16 coincidencias exactas. No se reentrenó. |
| Las métricas L1/L2 corresponden a sus predicciones guardadas | PDF 82–85 / pp. 66–69; D47–50 | S06 predicciones, scores, umbrales, métricas y verificación multietiqueta | Recalculadas métricas globales, por etiqueta y NORMAL/ataque; los scores y umbrales reconstruyen las decisiones. |
| M8 tiene resultados con 72 variables | PDF 80–81 / pp. 64–65; D38–44 | S07 `3datasetsMulticlase2`, job 3289, tres configuraciones/métricas | Configuración y métricas leídas; no se recalcularon todas las predicciones M8 en esta revisión. |
| Las curvas M8 difieren de las métricas globales por su universo | PDF 80–81 / pp. 64–65; D41 | S07 `loss_curve_metadata.json` por dataset | Harvard y DS: test de curva 50.000, con `test_sampled=true`; tablas 180.483 y 140.933. Aclaración a partir de los metadatos de la corrida. |
| La ejecución Slurm y sus resultados pueden relacionarse | PDF 87–89 / pp. 71–73; D24, D31, D35, D37, D49, D70 | S01 `sacct`, logs, configuraciones y manifiestos; S13 logs de M1–M3 | La captura S01 cubre 133 jobs seleccionados y conserva logs de 26. La lectura posterior de S13 incorpora evidencia directa de 2534, 2657 y 2687; esos conteos se mantienen por colección. |
| Los datos fuente y las dependencias faltantes están identificados | Directorio completo S13 y referencias de entradas/lanzadores S11 | CSV Harvard S11, índices de archivos y `S13_multiclase_evidencia.json` | No se localizaron brutos CSIC/TorpEda/DS en las colecciones inspeccionadas ni los dos Python referenciados por los lanzadores preliminares v10 y multifamily. La ausencia de esos basenames también se confirmó en todo S13. |

## 3. Universos de duplicados e identidad de petición

La huella usada para agrupar peticiones considera método, URI, protocolo, cuerpo y once encabezados: User-Agent, Referer, Host, Origin, Cookie, Content-Type, Accept, Accept-Language, Accept-Encoding, DNT y Connection. Aplica la normalización documentada y BLAKE2b de 128 bits, representado en 32 caracteres hexadecimales. No usa IP, fecha ni respuesta como parte de esa identidad, y la huella no entra como predictor. [PDF 51, 67 / pp. 35, 51; D26, D45; código L2.]

| Regla/universo | Grupos repetidos | Excedentes | Eventos en grupos repetidos | Evidencia |
|---|---:|---:|---:|---|
| Identidad de las 38 columnas, incluidos todos los eventos | 1.415 | 2.746 | 4.161 | Libro y auditoría S01; las 4.161 filas marcadas fueron recontadas en S10. |
| Huella de 15 campos, incluidos dos vacíos | 27.624 | 364.824 | 392.448 | Libro/S01 y columnas de auditoría S10. |
| Huella de 15 campos, sin los dos vacíos | 27.623 | 364.823 | 392.446 | Libro y reconciliación interna S06/L2. |

«Grupo repetido» no incluye las peticiones que aparecen una sola vez. «Excedentes» cuenta todos los eventos salvo el representante de cada grupo. No sumar estas columnas como si fuesen poblaciones disjuntas. Con vacíos hay 542.991 grupos totales; sin ellos, 542.990. La eliminación de dos eventos borra un grupo de tamaño 2.

La unión OR en L2 preserva las CAPEC observadas en el grupo y deriva NORMAL de no activar ninguna CAPEC objetivo. Puede generar una combinación de etiquetas que no figure junta en ningún evento individual. El recuento de conflictos describe esta limitación; no constituye revisión humana de los ataques.

## 4. Solapamiento histórico y separación L2

| Esquema Harvard | Unidades de prueba | Pruebas con huella presente en desarrollo | Porcentaje |
|---|---:|---:|---:|
| Nueve familias | 181.563 eventos | 77.184 | 42,5109 % |
| Top14 | 180.483 eventos | 76.959 | 42,6406 % |
| Top11 | 180.483 eventos | 77.060 | 42,6965 % |
| Top10 | 180.483 eventos | 77.127 | 42,7337 % |
| L1 | 181.563 eventos | 76.966 | 42,3908 % |
| L2 | 108.598 grupos | 0 | 0 % |

Fuente: PDF 86 / p. 70. Las primeras cinco filas son la auditoría documentada en el libro. No hay porcentaje equiparable para B2 Harvard ni auditoría equivalente establecida para los otros corpus. La verificación actual de L1 confirma los índices y soportes de su reconstrucción; no recomputó ese porcentaje histórico de huellas.

Para L2 se reconstruyeron 347.513 grupos de entrenamiento, 43.439 de selección, 43.440 de ajuste de umbrales y 108.598 de prueba. Coinciden el orden de índices de prueba, sample_id, etiquetas, huellas y los soportes guardados. Las seis intersecciones entre esas cuatro particiones dan cero. Esto verifica disyunción bajo la regla de identidad y la reconstrucción descritas; no son seis pruebas independientes de generalización. El detalle y las particiones derivadas están en [L2_verificacion.json](particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json) y sus archivos asociados.

## 5. Resultados principales y metas que siguen sin cumplirse

L2 alcanza F1 micro 97,604292 %, F1 macro 93,939931 %, exactitud de conjunto 96,919833 % y Hamming loss 0,276171 %. La exactitud de conjunto solo en ataques es 95,963836 %, calculada como 71.328/74.328. Los valores se recalcularon de las predicciones S06, sin reentrenamiento. [PDF 82–85 / pp. 66–69; D47–50; `L2_verificacion.json`.]

Diez de las doce CAPEC cumplen F1 ≥ 85 %. CAPEC-153 alcanza 80,863039 % y CAPEC-272 alcanza 58,035034 %; CAPEC-274 llega a 100 % sobre 994 positivos de prueba. NORMAL reconoce 33.925/34.270 = 98,993289 %: el objetivo 99 % no se cumple estrictamente, pese al redondeo a 99,0 %. Habrían hecho falta tres normales correctos adicionales. La matriz NORMAL/ataque derivada es TN 33.925, FP 345, FN 2.438 y TP 71.890; no es la matriz de los Random Forest B2.

Los benchmarks L2 recalculados usan 10.000 grupos: latencia p50 de 7,124564 ms, p95 de 7,627084 ms y p99 de 8,083367 ms; 138,928758 grupos/s en el flujo individual registrado. El campo histórico `req_s` conserva su nombre original, pero la unidad de L2 es el grupo de peticiones. Medición del modelo, flujo completo, ejecución Slurm y tiempo de un job reanudado responden a unidades y fases distintas. No extrapolar a tráfico real, red, TLS o concurrencia.

## 6. Integridad e identidad de las ejecuciones

El Python y el lanzador L2 coinciden con sus anclas SHA-256 del apéndice B. La firma request90 se recalculó a partir de la versión y el orden de características. Las comprobaciones están en [coincidencias_hash_libro.json](integridad_y_procedencia/coincidencias_hash_libro.json) y en la [verificación L2](particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json). Un hash de código, una firma de esquema y una huella de petición tienen funciones distintas. [PDF 101 / p. 85.]

La revisión interna de la captura Slurm S01 confirma 167/167 hashes del proyecto y 389/390 del manifiesto global; la única excepción es un log cuyo hash original coincide con el prefijo anterior a 187 bytes añadidos al terminar. La excepción permanece explicada junto al archivo histórico.

La tabla histórica de recuperación batch S01 dice `recuperado` para 133 jobs, pero no hay 133 scripts recuperados: los 133 resultados de error conservados dicen que la recuperación falló. Es una contradicción del procedimiento, no una prueba de recuperación satisfactoria. Conservar la tabla original y la interpretación verificada. El HEAD Git y el inventario de hardware del 03/08/2026 describen esa captura, no todos los entornos históricos. [S01; [revisión Slurm y binaria](historial_slurm/REVISION_SLURM_Y_BINARIO.md).]

Para M6, el informe 07/TEX cita job 2966 del 27/06, mientras los configs de resultados disponibles S07/S01 identifican 3013 del 28/06. Mantener ambas procedencias. La extensión 73/job 3361 posee resultados y una huella del Python registrada en el log; es una evolución posterior separada de los IDs del libro/presentación, que terminan en M8 para multiclase.

### Evidencia incorporada con S13

M1 queda vinculado al job 2534 del 09/06/2026, M2 al 2657 del 19/06 y M3 al 2687 del 20/06. M1/M2 registran fixed30 y preset `strong`; M3 registra optimized84 y preset `max`. Los seis catálogos ordenados de características coinciden con el código estático preservado S11; los cuatro fixed30 coinciden también con el anexo del libro. Los valores guardados corresponden al redondeo de las tablas S02: informe 02, página 3; informe 03, página 6; informe 04, página 3. Es una comprobación de la relación entre artefactos, no una nueva ejecución. [S13 `run_config.json`, `metrics_flat.csv` y logs de las tres ramas; `S13_multiclase_evidencia.json`.]

La lectura inicial exclusivamente documental queda preservada en [catálogo del libro](../01_documentacion/catalogos/catalogo_libro.json): su campo `features.order_not_verified_against_code=true` describe aquel alcance. Las comprobaciones posteriores de S13 y de la firma request90 en `L2_verificacion.json` se documentan por separado. La coincidencia de nombres y catálogos no establece por sí sola el hash histórico del código ejecutado.

La revisión del directorio completo de S13 —722 entradas, 622 archivos— confirmó que no añade los brutos identificados de CSIC, TorpEda ni DS-Augmented-v2. Las colecciones inspeccionadas incluyen la identidad y el perfil del CSV Harvard en S11 y diversas matrices procesadas de otros corpus; los datos crudos deben descargarse desde sus fuentes públicas. También faltan los basenames exactos `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py`, referenciados por dos lanzadores preliminares S11. Conservar esas referencias y la ausencia comprobada; no sustituirlas por scripts de nombre parecido. [Directorio completo S13; lanzadores S11, líneas 33 y 48 respectivamente; `S13_multiclase_evidencia.json`.]

## 7. Acceso por tema

| Tema | Entrada y evidencia |
| --- | --- |
| Dataset, duplicados y evolución multiclase | [Revisión de datasets y multiclase](datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md), [evidencia M1–M3 de S13](datasets_y_multiclase/S13_multiclase_evidencia.md) y [auditoría S10 recalculada](datasets_y_multiclase/S10_auditoria_excel_recalculado.json). |
| Particiones, L1 y L2 | [Revisión multietiqueta](particiones_y_multietiqueta/multietiqueta_evidencia.md), [verificación L1](particiones_y_multietiqueta/verificacion_20261010/L1_verificacion.json), [verificación L2](particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json) y [variante job2625](particiones_y_multietiqueta/S13_L1_2625.md). |
| Ejecución y código histórico | [Revisión Slurm y binaria](historial_slurm/REVISION_SLURM_Y_BINARIO.md), [catálogo de jobs](historial_slurm/catalogo_jobs.csv) y [variantes de código](historial_slurm/variantes_codigo.csv). |
| Integridad y conservación | [Alcance de la auditoría](integridad_y_procedencia/ALCANCE_DE_AUDITORIA.md), [inventario](integridad_y_procedencia/inventario_archivos.csv), [colecciones de evidencia](integridad_y_procedencia/fuentes_originales.csv), [criterios](integridad_y_procedencia/CRITERIOS_DE_LIMPIEZA.md), [exclusiones](integridad_y_procedencia/archivos_descartados.csv) y [copias exactas](integridad_y_procedencia/duplicados_fusionados.csv). |
| Datasets, corridas y reproducción | [Fuentes públicas de datasets](../03_datasets/README.md), [historial experimental](../04_experimentos/README.md), [guía de reproducibilidad](../07_reproducibilidad/README.md) y [entorno Arandu/Slurm](../07_reproducibilidad/ENTORNO_SLURM.md). |

No hay en esta verificación una nueva ejecución experimental, una comparación WAF en producción, ensayos entre corpus, evaluación temporal ni repetición con múltiples semillas. Esos alcances no deben aparecer como validados por el hecho de organizar y contrastar los artefactos.
