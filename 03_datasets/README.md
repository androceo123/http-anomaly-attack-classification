# Datasets, etiquetas y universos de evaluación

## Cuatro fuentes y sus alias

Este catálogo, actualizado el 10 de octubre de 2026 tras revisar el directorio completo de S13 y sus salidas pequeñas M1–M3, distingue el corpus, la versión local y la transformación usada por cada etapa. Un mismo nombre de dataset no implica las mismas filas, clases, particiones o unidad de evaluación. Las cifras llevan referencia al libro, presentación o artefacto preservado; las marcadas como verificadas se recontaron durante esta organización. Las métricas y filtrados de S13 se leyeron de sus archivos guardados, sin reentrenamiento.

| Nombre canónico | Alias en archivos | Uso documentado | Universo y estado |
|---|---|---|---|
| [CSIC 2010](CSIC2010/README.md) | CSIC, csic | Antecedentes one-class, B1 y B2 | No se atribuye un único tamaño general: los antecedentes y benchmarks usan poblaciones distintas. El libro no fija claramente el total B2. |
| [TorpEda 2012](TorpEda2012/README.md) | TorpEda, TORPEDA, CSIC TorpEda 2012 | Binario y multiclase | Configs/reportes S07/S09/S13: 74.133 eventos, 59.306 desarrollo y 14.827 test, diez clases nativas. |
| [SR-BH 2020](SRBH2020/README.md) | Harvard, SR-BH, Harvard Dataverse | Binario, multiclase y multietiqueta | CSV S11 verificado: 907.815 eventos y 38 columnas. Versiones top14 y L2 tienen universos distintos, detallados abajo. |
| [DS-Augmented-v2](DSAugmentedV2/README.md) | Egipcios, DS, DS-v2; `combined_data.csv` | Multiclase M7/M8 y extensión posterior 73 | Configs S07: 704.665 eventos, 563.732 desarrollo y 140.933 test. M7/M8 usan 8 clases; la fuente y extensión 73 usan 9. |

Referencias: libro PDF 46–52 / pp. 30–36 y PDF 75 / p. 59; presentación D20, D39–40, D45–47 y D70. Los modelos fueron entrenados por corpus; el título histórico `documento_cross_dataset_waf.pdf` no acredita que un modelo entrenado en uno se haya evaluado en otro. La transferencia entre corpus figura como trabajo futuro. [D16, D35, D54.]

## 1. Disponibilidad y procedencia

Harvard está disponible como CSV bruto S11 de 436.437.661 bytes, SHA-256 `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910`. Este contenido coincide con el hash de entrada registrado por la extensión 73 en S01. El ZIP S11 coincide además con el ancla SHA del libro. [Libro PDF 101 / p. 85; S11; `coincidencias_hash_libro.json`; revisión Slurm.]

S07/S09/S13 conservan matrices procesadas por representación y corrida para TorpEda/Harvard, y S07 para Egipcios. Las entradas TorpEda se declaran como `allAnomalies1.xml`, `allAnomalies2.xml`, `allAttacks1.xml` a `allAttacks5.xml` y `allNormals1.xml`. Egipcios se carga desde `DS_Augmented_v2_csv/combined_data.csv`; S01 conserva una etapa de exportación con job 3045. Estas rutas documentan la procedencia registrada por la ejecución.

**No se localizaron los brutos CSIC, TorpEda ni DS-Augmented-v2 en los paquetes inspeccionados.** La revisión del directorio completo de S13 confirmó que tampoco incorpora los XML TorpEda, `combined_data.csv` de DS ni archivos brutos identificados de CSIC. Sus 722 entradas incluyen 622 archivos de salidas, búsquedas, predicciones, código y caches procesadas. Esta conclusión usa el índice completo del ZIP, además de los archivos pequeños leídos; no depende de una extracción parcial. [Inventarios originales y directorio completo S13; `S13_multiclase_evidencia.json`.]

Quedan identificadas también dos dependencias ausentes de los lanzadores preliminares S11: `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py`. Ninguno de esos basenames aparece en S13 ni en las demás fuentes extraídas revisadas. El Python multifamily preservado sin `DEFINITIVO` y el multiclass v12 tienen otros nombres/versiones; no se consideran reemplazos acreditados. [Lanzadores S11, líneas 33 y 48; directorio completo S13.]

Los paquetes históricos de código se preservan como raíces ejecutables. No sustituirlos por el parser más reciente y atribuir luego los resultados al código antiguo. Mantener por cada copia nombre original, fuente Sxx, tamaño y SHA-256, incluso cuando dos copias sean idénticas.

## 2. Harvard: del original a sus derivados

| Derivado / fase | Filas o grupos | Qué cambia |
|---|---:|---|
| Tamaño publicado citado por el libro | 907.814 filas | Referencia bibliográfica; no es el recuento de esta copia local. |
| CSV local original | 907.815 eventos | Recontado: 525.195 normales y 382.620 con al menos una CAPEC. |
| Multiclase M1, nueve familias | 907.815 eventos | Configs S13, job 2534: `optimized-family` y resolución `severity`; frecuencia mínima 20 sin exclusiones. Train/test: 726.252/181.563. |
| Top14 multiclase | 902.411 eventos | Conserva 14 combinaciones exactas frecuentes; excluye 5.404 eventos de 46 combinaciones. |
| Top11 y Top10 | 902.411 eventos | Parten de Top14 y fusionan clases; conservan filas, cambian el objetivo. |
| Auditoría por 15 campos con peticiones vacías | 542.991 grupos totales | Incluye un grupo con los dos eventos vacíos. |
| Entrada válida L2 | 907.813 eventos | Excluye los dos eventos sin contenido en los 15 campos de petición. |
| Procesado L2 por huella | 542.990 grupos | Agrupa, une CAPEC mediante OR; 171.348 grupos normales y 371.642 con ataque. |
| Test L1 | 181.563 eventos | Por filas históricas; contiene repeticiones de petición respecto de desarrollo. |
| Test L2 | 108.598 grupos | Separación por grupo, con huellas disjuntas en las particiones reconstruidas. |

Fuentes: PDF 48–52 / pp. 32–36, PDF 75–76 / pp. 59–60; D45–48; S11 perfil crudo, S07/S09/S13 filtrados y S06 verificación L2. S13 confirma M1/job 2534, M2/job 2657 y M3/job 2687. Son ramas de preparación diferentes: Top14 no se obtiene de la deduplicación L2, ni las 902.411 filas son una versión sin repetidos.

La lectura completa del CSV confirmó 60 combinaciones, ningún registro CSV mal formado, ninguna fila con NORMAL y una CAPEC simultáneas y ninguna fila con las 14 etiquetas a cero. Hay dos eventos con los 15 campos HTTP vacíos: registros 14.411 y 163.885, numerados desde 1. El CSV puede ser sintácticamente válido y contener una petición vacía; por eso S14 informa 907.815 «válidos» y L2 usa 907.813 bajo otra regla.

## 3. Etiquetas originales y taxonomías Harvard

El original tiene NORMAL y 13 CAPEC. Los valores siguientes son conteos marginales: una fila multietiqueta puede sumar en más de una CAPEC, por lo que no se deben sumar como clases mutuamente excluyentes.

| Etiqueta original | Positivos en el CSV |
|---|---:|
| 000 – Normal | 525.195 |
| 272 – Protocol Manipulation | 9.153 |
| 242 – Code Injection | 15.827 |
| 88 – OS Command Injection | 7.482 |
| 126 – Path Traversal | 20.992 |
| 66 – SQL Injection | 250.311 |
| 16 – Dictionary-based Password Attack | 1.847 |
| 310 – Scanning for Vulnerable Software | 2.718 |
| 153 – Input Data Manipulation | 2.272 |
| 248 – Command Injection | 1 |
| 274 – HTTP Verb Tampering | 5.437 |
| 194 – Fake the Source of Data | 56.145 |
| 34 – HTTP Response Splitting | 19.738 |
| 33 – HTTP Request Smuggling | 1.059 |

Verificado en S11, `sr_bh_raw_profile.json`; los análisis S08/S14 coinciden con sus combinaciones. La frecuencia exacta «solo SQL Injection» es 248.093; no es el marginal 250.311 que incluye combinaciones. CAPEC-248 tiene un único positivo y se excluye como objetivo de las evaluaciones L1/L2 de doce etiquetas; se conserva en la fuente y en el procesado previo al descarte. NORMAL se deriva de no activar objetivos CAPEC. [Libro PDF 56–58 / pp. 40–42 y PDF 75–76 / pp. 59–60; S06/S11.]

| Etapa | Representación del objetivo |
|---|---|
| M1 | Nueve familias Harvard, incluido NORMAL; config S13/job 2534 con `optimized-family`. No equivale a nueve CAPEC originales. |
| M2–M4 | Catorce combinaciones exactas admitidas, incluida NORMAL. |
| M5 Top11 | CAPEC-153 y 194 pasan a DataManipulation; CAPEC-272,274 y 272+274 pasan a HTTPProtocolManipulation. |
| M6–M8 Top10 | Esas cinco categorías fuente se reúnen en RequestManipulation. CAPEC-88+126 permanece como una clase compuesta. |
| L1/L2 | Doce objetivos CAPEC separados; no se aplica la fusión Top10. L2 agrupa peticiones, no fusiona las identidades CAPEC objetivo. |
| Extensión 73 | Harvard conserva Top10; tiene una representación distinta y ejecución propia. |

Evidencia: PDF 55, 72, 75 / pp. 39, 56, 59; D19–20 y D39–46; S09 `harvard_top14_to_operational_groups_mapping.csv`; S07 `harvard_top14_to_request_groups_mapping.csv`; S11 código; S13 configuraciones y reportes de filtrado M1–M3.

En M1 las familias guardadas son NORMAL, SQLi, DataManipulation, CommandInjection, CRLFi, PathTraversal, HTTPProtocolManipulation, VulnerabilityScanning y PasswordAttack. En M2/M3 se conservan las 14 combinaciones exactas admitidas y se excluyen 5.404 filas de 46 combinaciones. Los nombres y conteos de ambas taxonomías se conservan en los respectivos `dataset_filtering_report.json`; no se debe aplicar retrospectivamente Top14 al M1 de nueve familias.

## 4. TorpEda y DS-Augmented-v2

TorpEda conserva NORMAL (8.363), ANOMALOUS (16.459), SQLi (43.013), XSS (4.818), SSI (451), BufferOverflow (412), CRLFi (327), XPath (175), LDAPi (74) y FormatString (41). Estos conteos figuran en los reportes de filtrado S07/S09/S13. El mínimo soporte de algunas clases explica por qué accuracy y F1 macro pueden moverse en direcciones diferentes; siempre conservar las métricas por clase y sus denominadores. La imagen S08 muestra las nueve categorías distintas de NORMAL, sin métricas. [S07/S09/S13 `dataset_filtering_report.json`; S08 PNG.]

DS-Augmented-v2 conserva 704.665 registros en M7/M8. Tras la unión de dos clases de comando, sus ocho clases son NORMAL (493.515), SQLi (146.086), CommandInjection (38.711), PathTraversal (17.718), XSS (2.894), SSRF (2.645), SSTI (1.897) y CodeInjection (1.199). En la extensión de 73 variables, CommandInjection (2.597) y OSCommandInjection (36.114) se mantienen separadas y quedan nueve clases. Las métricas de esa extensión no deben interpretarse como una ablación de una sola variable respecto de M8: cambian representación, clases y política de pesos. [S07 `3datasetsMulticlase*`, reportes de filtrado; libro PDF 49, 75 / pp. 33, 59.]

## 5. Representación, huella y particiones

El catálogo binario incluye RF-25, RF-33, RF-57 y RF-10-Gini. RF-34 es un alias histórico incorrecto para 25 + 8 = 33; debe conservarse el nombre original con la aclaración. OCSVM con 26/34 variables pertenece a otros antecedentes. Multiclase usa 30 → 84 → 58 → 72; la extensión posterior 73 es otra versión. Multietiqueta compara fixed30 y request90. El orden de las variables y el extractor, además del número, forman parte de la identidad de un esquema. [Libro PDF 71–75 / pp. 55–59; S05/S11; D20, D34, D38, D45.]

La huella de identidad usa 15 campos de petición y BLAKE2b de 128 bits; el hash del archivo es SHA-256. La firma request90 se calcula a partir del identificador de versión y la lista ordenada de variables. La `input_signature` L2 resume ruta/tamaño/mtime y no es un SHA del contenido bruto. Conservar estos identificadores con su tipo y función.

Las configuraciones M1–M8 conservadas usan 80/20 por filas y semilla 42, con consultas históricas a la prueba durante el desarrollo. S13 confirma fixed30 en M1/M2 y optimized84 en M3, con catálogos ordenados iguales a las listas estáticas S11; fixed30 coincide también con el anexo del libro. Esta comprobación posterior conserva su propio alcance y no acredita el hash histórico de cada Python ejecutado. [S13 `run_config.json`; `S13_multiclase_evidencia.json`.]

L1 usa 581.001/145.251/181.563 eventos. L2 usa 347.513/43.439/43.440/108.598 grupos, semillas 42/43/44, y separa selección y umbrales. La verificación L2 actual reconstruyó particiones y confirmó seis intersecciones de huellas iguales a cero. No se hallaron listas históricas completas de entrenamiento, selección y calibración; las listas generadas ahora se rotulan como reconstrucción.

## 6. Archivos estadísticos y auditoría de calidad

S08 `ataques.xlsx` contiene 13 encabezados CAPEC y 14 tipos de ataque con la matriz de correspondencias vacía. Es una propuesta incompleta, no un mapeo etiquetado. S08 `estadisticas harvard.xlsx` sí contiene las 60 combinaciones verificadas. S14 agrega diccionario, marginales y coocurrencias. Conservar propósito y estado en el nombre/índice para evitar que una plantilla se interprete como resultado.

S10 `harvard_duplicados.xlsx` conserva los eventos de grupos repetidos y su diccionario. Sus columnas de auditoría se recontaron y son consistentes con el universo que incluye vacíos. El formato Excel puede truncar celdas largas y escapar caracteres; no sustituye al CSV completo. Los conflictos, exclusiones y duplicados deben quedar accesibles en `02_auditoria`, junto al corpus en `03_datasets` y a las configuraciones de cada corrida.
