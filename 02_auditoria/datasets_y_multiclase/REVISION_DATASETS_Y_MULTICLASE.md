# Evidencia de datasets, auditoría y corridas multiclase

Revisión de solo lectura del 10 de octubre de 2026. Este documento enlaza el libro y la presentación con evidencia primaria preservada. Los números B/M/L son etapas documentales; un job es una ejecución concreta. Los estados «mencionado», «archivo disponible», «configuración leída», «conteo recalculado» y «entrenamiento reproducido» no son intercambiables. En esta revisión no se entrenó ningún modelo ni se cargaron objetos joblib.

Las referencias `PDF x / p. y` usan página física y página impresa del libro `08282026v4.pdf`. `Dxx` identifica el orden real de las 71 diapositivas. Los códigos `Sxx` remiten al inventario original de Drive, con rutas y SHA-256 conservados en `datasets_multiclase_mapa.json`.

## 1. Fuentes examinadas

| Fuente | Archivo original | Archivos revisados / función |
|---|---|---|
| S02 | pdfsMulticlase.zip | 9 PDF; informes 01 y 02 son M1, 03–09 son M2–M8 |
| S03 | multiclaseCorridasInformes.zip | 8 TEX; fuentes de los informes 01–08; no hay TEX M8 en esta fuente |
| S07 | multiclaseCorridas3datasets.zip | 504 archivos; resultados M6, M7, M8 y extensión73 |
| S08 | ataques que tenemos que considerar.zip | 3 archivos; dos libros Excel y una captura de taxonomía |
| S09 | todoMulticlase.zip | 127 archivos; resultados M4 y M5 |
| S10 | harvard_duplicados.zip | 1 Excel de 102.874.905 bytes; auditoría de repeticiones |
| S11 | datasetYCorridasMulticlaseMultietiqueta.zip | 35 archivos; 34 scripts/lanzadores y CSV Harvard de 436.437.661 bytes |
| S14 | analisis_combinaciones_capec.xlsx | Excel independiente de 7 hojas; combinaciones y coocurrencias |

También se cruzaron el libro, el informe Slurm S01 de otro analista y la verificación L1/L2 de S06. Esas verificaciones se identifican por separado; no se presentan como una segunda repetición independiente.

## 2. Harvard: archivo de origen y etapas distintas

El CSV S11 contiene **907.815 registros lógicos, 38 columnas y 60 combinaciones exactas de etiquetas**. Su SHA-256 es `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910`; tamaño 436.437.661 bytes. Coincide además con la huella de entrada registrada en el log de la extensión73, revisada en S01. Leer las etiquetas de todos los registros confirmó 525.195 normales, 382.620 con al menos una CAPEC, cero filas con NORMAL y ataque simultáneos en la fuente y cero filas con las catorce etiquetas a cero. No se encontraron registros CSV mal formados.

El recuento publicado de 907.814 y el recuento del archivo de 907.815 están diferenciados por el propio libro; esta revisión acredita el segundo para este SHA. Las 38 columnas incluyen contexto de captura y respuesta, además de la petición y las etiquetas. La presencia de una columna en el original no acredita que se use como predictor. [Libro PDF 48–52 / pp. 32–36; D20, D26, D45–47; S11 `data_capec_multilabel.csv`; `sr_bh_raw_profile.json`.]

| Etapa | Universo | Función y evidencia |
|---|---:|---|
| Archivo original | 907.815 eventos | Perfil CSV recalculado. |
| Top14 multiclase | 902.411 eventos | Excluye 5.404 filas de 46 combinaciones no admitidas. Es filtrado de etiquetas, no deduplicación. Confirmado en S09 y S07 `dataset_filtering_report.json`. |
| Auditoría por huella que conserva vacíos | 542.991 grupos | Resultado histórico S01; S10 conserva las 392.448 filas pertenecientes a grupos repetidos, incluidos los dos vacíos. |
| Preparación L2 | 907.813 eventos válidos | Se eliminan dos peticiones con los quince campos HTTP vacíos, índices 0-based 14.410 y 163.884. |
| Consolidación L2 | 542.990 grupos | S06 confirma unicidad de huellas, suma de tamaños 907.813 y unión OR de etiquetas. |
| Prueba L1 | 181.563 eventos | Por filas; tiene solapamiento histórico por huella. |
| Prueba L2 | 108.598 grupos | Por grupos consolidados, con seis intersecciones vacías entre cuatro particiones reconstruidas. |

La matriz intermedia `sr_bh_raw_labels.npy` tiene 907.815 × 14 valores uint8 en orden original; se compartió con la verificación L1. No contiene cuerpos HTTP. La evaluación de L1 no debe compararse con L2 como una ablación aislada: cambian representación, unidad, distribución, tratamiento de duplicados, entrenamiento y umbrales. [Libro PDF 75–76, 85–89 / pp. 59–60, 69–73.]

## 3. Excel S08/S14: estadísticas y plantilla de taxonomía

Las sesenta combinaciones y sus frecuencias de S08 `estadisticas harvard.xlsx` coinciden exactamente con el CSV. También coinciden las sesenta combinaciones de S14 `Combos exactas`, sus 38 pares de coocurrencia y sus 22 ternas. Se recontaron desde las etiquetas fuente; no se copiaron sin verificación del Excel. Los casos con 0, 1, 2, 3 y 4 ataques son 525.195, 373.382, 8.132, 1.088 y 18. [S08 y S14; `S08_S14_combinaciones_recalculadas.json`; `sr_bh_raw_profile.json`.]

S14 tiene siete hojas: Resumen, Combos exactas, Por cantidad, Ataques individuales, Coocurrencias 2, Coocurrencias 3 y Diccionario. La fecha declarada de generación es 2026-06-18 (Asia/Manila). «Requests válidos» = 907.815 en este Excel se refiere a registros CSV válidos; L2 descarta dos peticiones HTTP vacías con otro criterio. Conservar ambas descripciones evita una falsa contradicción.

S08 `ataques.xlsx` es una **plantilla incompleta**: trece encabezados CAPEC y catorce tipos de ataques en la primera columna; la matriz de correspondencias está vacía. Debe catalogarse como planificación/taxonomía pendiente, no como mapeo validado ni tabla de experimentos. La imagen PNG muestra nueve categorías TorpEda que excluyen NORMAL; es evidencia visual del catálogo, no de rendimiento. La inspección de XLSX fue `read_only`, sin guardar cambios. [S08; `xlsx_datasets_estructura.json`.]

## 4. Excel S10: evidencia visible de repetición

`harvard_duplicados.xlsx` tiene las hojas `Duplicados` y `Diccionario_auditoria`. La primera conserva 14 columnas de auditoría y las 38 del original: 52 columnas. Se leyó la estructura con openpyxl read_only y se recorrieron incrementalmente solo las columnas de auditoría de todas las filas. No se materializó en memoria el XML de 1,38 GB ni se retuvieron los payloads.

| Indicador recontado en S10 | Resultado |
|---|---:|
| Filas de eventos pertenecientes a grupos repetidos | 392.448 |
| Grupos repetidos | 27.624 |
| Representantes / excedentes | 27.624 / 364.824 |
| Máximo tamaño de grupo | 453 |
| Filas de petición vacía / grupos vacíos | 2 / 1 |
| Grupos con variación de etiquetas / filas involucradas | 288 / 2.331 |
| Grupos normal–ataque / filas involucradas | 284 / 2.322 |
| Filas marcadas como duplicado exacto de las 38 columnas | 4.161 |

Los tamaños, rangos, representante y excedentes son internamente consistentes; los registros fuente están en orden creciente y son únicos dentro de este extracto. El indicador `raw_http_variant_count` vale 1 en los 27.624 grupos. Es un recuento de lo que registran las columnas de auditoría, **no una recomputación independiente de las huellas o de todos los campos del raw**. Para las cifras de duplicados exactos de 38 columnas, el libro y S01 reportan además 1.415 grupos y 2.746 excedentes; aquí se recontaron sus 4.161 filas marcadas, no se rehizo la agrupación de 38 columnas. [Libro PDF 51–52 / pp. 35–36; S10; `S10_auditoria_excel_recalculado.json`; S01 jobs3446/3454.]

El diccionario aclara que `source_record` es el ordinal de registro CSV, no línea física; los dos vacíos son 14.411 y 163.885 en base1, coincidentes con el raw. Los contenidos HTTP se escriben como texto para Excel, se escapan caracteres no admitidos por XML y se truncan celdas por encima de 32.767 caracteres. El Excel sirve como vista auditable; la fuente CSV conserva la fidelidad completa. Mantener unidos su diccionario, el script `duplicadosHarvard.py` y los logs. No borrar filas repetidas de la evidencia histórica.

La diferencia S10/L2 es explicable: al retirar los dos eventos vacíos desaparece un grupo de tamaño2; quedan 27.623 grupos repetidos, 364.823 excedentes y 392.446 eventos en esos grupos. Los 288 conflictos y 284 mezclas normal/ataque se conservan. La unión OR registra etiquetas presentes en cualquiera de los eventos del grupo y puede producir una combinación no existente en una sola fila; no adjudica cuál etiqueta era correcta. [Libro PDF 51–52, 75–76; D45, D52; S06 verificación L2.]

## 5. Historia documental y evidencia por corrida

Los números de PDF no son códigos M: 01 y 02 corresponden a M1 original/corregido; 03=M2, 04=M3, 05=M4, 06=M5, 07=M6, 08=M7 y 09=M8. Los ocho TEX S03 corresponden a los ocho primeros PDF, no existe fuente M8 en S03. Esta ausencia es local a ese paquete, no una afirmación de que nunca existió. Los nombres exactos y SHA están en el mapa JSON. Se extrajo el texto de los nueve PDF y se inspeccionaron visualmente sus portadas05,06 y09 para confirmar representación, corrida y datos de ejecución.

S11 conserva el código de expansión 30→84→58 y los cambios de taxonomía Harvard. Se inspeccionaron listas y constantes por AST sin ejecutar los scripts. `3datasetsMulticlase3.py` termina en **73 variables**: conserva un catálogo legado de93, elimina25 y añade5. Se corrigió el recuento parcial del análisis estático para considerar esa reasignación final (líneas519–521). El manifiesto S07 `features_used.csv` confirma73; no debe catalogarse como93 por una lista intermedia.

### M4/M5: métricas recalculadas desde predicciones

| Etapa / job | Dataset | Clases | Test | Accuracy | F1 macro | MCC |
|---|---|---|---|---|---|---|
| M4 / 2766 | harvard | 14 | 180.483 | 96,2972 % | 88,8080 % | 0.937152 |
| M4 / 2766 | torpeda | 10 | 14.827 | 99,6493 % | 99,3697 % | 0.994125 |
| M5 / 2927 | harvard | 11 | 180.483 | 97,1615 % | 94,3970 % | 0.951122 |
| M5 / 2927 | torpeda | 10 | 14.827 | 99,6493 % | 99,3697 % | 0.994125 |

Para las cuatro salidas se recalcularon accuracy, balanced accuracy, F1 macro y MCC desde `test_predictions.csv`; los dieciséis valores coinciden exactamente con `metrics_flat.csv`. También se conservó el reporte por clase recalculado. Los índices de prueba son únicos. M4 usa Top14 y M5 Top11, ambos con58 características, seed42, 80/20; Harvard usa `sqrt_balanced`, TorpEda `none`. Esta concordancia valida la aritmética de salidas guardadas, no repite el entrenamiento ni elimina el solapamiento histórico. [S09; `S09_multiclase_recalculado.json`; libro PDF72,75,80 / pp56,59,64; D42, D69.]

La selección58 conserva características con importancia por permutación positiva en al menos una clase de TorpEda o Harvard de M3. Los archivos explicitan esa regla. Esa selección usó prueba histórica; las versiones posteriores no heredan independencia por cambiar el nombre de la corrida.

### M6/M7/M8 y extensión73: configuraciones y métricas conservadas

| Etapa / job | Dataset | Variables | Clases | Test | Accuracy guardada | F1 macro guardado |
|---|---|---|---|---|---|---|
| M6 / 3013 | harvard | 58 | 10 | 180.483 | 97,4978 % | 97,1006 % |
| M6 / 3013 | torpeda | 58 | 10 | 14.827 | 99,6493 % | 99,3697 % |
| M7 / 3068 | egipcios | 58 | 8 | 140.933 | 99,0144 % | 81,1677 % |
| M7 / 3068 | harvard | 58 | 10 | 180.483 | 97,4978 % | 97,1006 % |
| M7 / 3068 | torpeda | 58 | 10 | 14.827 | 99,6493 % | 99,3697 % |
| M8 / 3289 | egipcios | 72 | 8 | 140.933 | 99,4245 % | 84,4867 % |
| M8 / 3289 | harvard | 72 | 10 | 180.483 | 97,7455 % | 97,2250 % |
| M8 / 3289 | torpeda | 72 | 10 | 14.827 | 99,7774 % | 98,6786 % |
| Extensión 73 / 3361 | egipcios | 73 | 9 | 140.933 | 99,4281 % | 83,8175 % |
| Extensión 73 / 3361 | harvard | 73 | 10 | 180.483 | 98,0103 % | 97,2135 % |
| Extensión 73 / 3361 | torpeda | 73 | 10 | 14.827 | 99,8853 % | 99,9221 % |

Los once `run_config.json` y los once `metrics_flat.csv` fueron leídos; se cotejaron conteos de `features_used.csv` y reportes de filtrado. No se recalcularon todas las predicciones S07. Las rutas/hash/configs de cada fila están en `S07_multiclase_config_metricas.json`.

**M6 tiene dos referencias de ejecución:** PDF07 y el TEX respectivo nombran job2966, 27/06/2026; los dos configs S07 nombran job3013, 28/06/2026. S01 también enlaza los resultados a3013 y conserva intentos previos. Registrar ambos, con origen, aunque coincidan valores globales. Nunca sobrescribir el job de un informe histórico por el de la copia posterior.

**M8 tiene una aclaración de denominadores:** las curvas Harvard y DS usan50.000 filas de prueba, mientras las tablas globales usan180.483 y140.933. `loss_curve_metadata.json` registra `test_sampled=true`. Así, los errores de curva2,284% y0,808% no son errores del test completo (2,254506% y0,575451%). TorpEda usa las14.827 filas y coincide. El libro no había podido establecer ese subconjunto; la organización debe adjuntar esta aclaración derivada sin editar los originales. [Libro PDF80–81 / pp64–65; D41; S07 `3datasetsMulticlase2/multiclase/*/loss_curve_metadata.json`.]

**Extensión73** dispone de resultados reales job3361 y no se introduce como M9. La política es `compact73_cross_dataset_v1`. Harvard conserva10 clases; DS vuelve a9 (CommandInjection2.597 y OSCommandInjection36.114 separados), frente a las8 de M7/M8. Sus métricas DS no constituyen una comparación del mismo objetivo. Las cadenas guardadas de comparación con WAMM son metadatos de la corrida; no acreditan una reproducción del trabajo externo.

## 6. Identidad de artefactos según el libro

| Ancla del libro, PDF 101 / p. 85 | Archivo disponible / tipo | Estado |
|---|---|---|
| corridasBinarias(5).zip | corridasBinarias.zip | coincidencia exacta de bytes |
| datasetYCorridasMulticlaseMultietiqueta.zip | datasetYCorridasMulticlaseMultietiqueta.zip | coincidencia exacta de bytes |
| informesMultilabel.zip | informesMultilabel.zip | coincidencia exacta de bytes |
| multiclaseCorridasInformes(1).zip | multiclaseCorridasInformes.zip | coincidencia exacta de bytes |
| evidencia_tesis_slurm_20260803T142006.tar.gz | S01 ZIP | no coincidencia de contenedor disponible |
| multietiquetaCorrida2.sh | multietiquetaCorrida2.sh | coincidencia exacta de bytes |
| multietiquetaCorrida2.py | multietiquetaCorrida2.py | coincidencia exacta de bytes |
| sr-bh-request90-v2 | sr-bh-request90-v2 | firma recalculada coincide |

Los cuatro ZIP coincidentes y los dos scripts L2 fueron verificados por SHA-256 exacto; cambios de nombre como `(5)` o `(1)` no cambian contenido. La firma request90 también coincide mediante la serialización de versión y nombres ordenados. SHA de contenedor, SHA del script, firma de esquema y huella BLAKE2b128 de petición responden preguntas distintas. El `input_signature` L2 es un hash de manifiesto de ruta/tamaño/mtime, no prueba identidad del CSV por contenido. [Libro PDF101 / p85; `coincidencias_hash_libro.json`; verificación L2; revisión Slurm S01.]

El contenedor S01 es ZIP, mientras la ancla del libro es TAR.GZ; no hay identidad binaria entre esos formatos. La auditoría interna de S01, realizada por el otro analista, encontró167/167 hashes en el manifiesto del proyecto y389/390 en el global. La excepción del log corresponde exactamente a un agregado posterior de187bytes. Conservar ambos hechos y no sustituirlos por «todo coincide».

## 7. Criterio de organización y alcance final

La auditoría debe ser una entrada visible en `02_auditoria`, con referencias a fuente cruda, reglas de huella, duplicados, conflictos, particiones, Slurm y límites. `03_datasets` reúne corpus, alias, taxonomías, filtrados y diccionarios. `04_experimentos` debe permitir localizar B1–B2/M1–M8/L1–L2 y la extensión73 separada. `05_codigo` conserva variantes; `06_resultados_consolidados` reúne tablas con denominadores y estados de verificación; `07_reproducibilidad` enlaza comandos, entornos, hashes y esquemas; `90_artefactos_pesados` ofrece acceso a raw/caches/modelos/predicciones voluminosos. `01_documentacion` guarda libro, presentación e informes históricos con sus fuentes.

El mapa JSON clasifica todos los archivos de las ocho fuentes de esta revisión y registra categoría semántica, papel, etapa, SHA y decisión de conservación. La categoría semántica no ordena romper árboles: conservar cada raíz de corrida y agregar índices/enlaces cuando un traslado aislado perdería rutas relativas o contexto.

No se verificó aquí una generalización temporal o entre corpus, ni una implantación WAF, ni múltiples semillas. Los cinco porcentajes históricos de solapamiento del libro permanecen como resultados documentados, no fueron todos recalculados desde raw en este análisis. La verificación L2 confirma intersecciones sobre particiones reconstruidas y predicciones concordantes; no recupera manifiestos históricos de entrenamiento que no se guardaron. La fuente bruta Harvard sí está disponible; disponibilidad final de otros corpus se debe completar con el inventario global, incluida S13 cuando se incorpore.


### Alcance temporal del catálogo inicial del libro

`libro_catalogo.json` conserva el resultado de una lectura inicial exclusivamente documental. Su campo `features.order_not_verified_against_code=true` describe esa lectura y no invalida verificaciones posteriores: `L2_verificacion.json` registra el recálculo concordante de la firma request90, y las verificaciones L1/L2 posteriores contrastan predicciones, métricas y particiones con sus fuentes preservadas. Se mantiene el catálogo inicial sin reescribir su alcance; la evidencia posterior se documenta por separado.
