# Datasets, etiquetas y universos de evaluación

## Cuatro fuentes y sus alias

Este catálogo documenta las entradas y transformaciones de los experimentos ejecutados en Arandu con Slurm. Distingue el corpus público, la versión de entrada identificada por cada corrida y su universo de evaluación. Un mismo nombre de dataset no implica las mismas filas, clases, particiones o unidad de evaluación. El repositorio publica código, esquemas y evidencia de auditoría; los corpus completos se descargan desde los enlaces siguientes y se preparan en el almacenamiento de trabajo del clúster.

Las cifras experimentales proceden de las configuraciones, perfiles e informes enlazados. Los recuentos de la auditoría posterior se distinguen de las ejecuciones históricas; actualizar esta documentación no supone haber reentrenado los modelos ni validado una nueva descarga completa.

| Nombre canónico | Alias en archivos | Uso documentado | Universo y estado |
|---|---|---|---|
| [CSIC 2010](CSIC2010/README.md) | CSIC, csic | Antecedentes one-class, B1 y B2 | No se atribuye un único tamaño general: los antecedentes y benchmarks usan poblaciones distintas. El libro no fija claramente el total B2. |
| [TorpEda 2012](TorpEda2012/README.md) | TorpEda, TORPEDA, CSIC TorpEda 2012 | Binario y multiclase | Configuraciones y reportes históricos: 74.133 eventos, 59.306 desarrollo y 14.827 test, diez clases nativas. |
| [SR-BH 2020](SRBH2020/README.md) | Harvard, SR-BH, Harvard Dataverse | Binario, multiclase y multietiqueta | Perfil de la entrada histórica: 907.815 eventos y 38 columnas. Top14 y L2 tienen universos distintos, detallados abajo. |
| [DS-Augmented-v2](DSAugmentedV2/README.md) | Egipcios, DS, DS-v2; `combined_data.csv` | Multiclase M7/M8 y extensión posterior 73 | Configuraciones históricas: 704.665 eventos, 563.732 desarrollo y 140.933 test. M7/M8 usan 8 clases; la extensión 73 usa 9. |

Referencias: [revisión de datasets y multiclase](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md), [revisión binaria y Slurm](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) e [índice experimental](../04_experimentos/README.md). En el libro corresponden a PDF 46–52 / pp. 30–36 y PDF 75 / p. 59; en la presentación, a D20, D39–40, D45–47 y D70. Los modelos fueron entrenados por corpus; el título histórico `documento_cross_dataset_waf.pdf` no acredita que un modelo entrenado en uno se haya evaluado en otro. La transferencia entre corpus figura como trabajo futuro (D16, D35 y D54).

## 1. Fuentes públicas y preparación en Arandu

| Dataset | Descarga pública | Formato que utiliza el proyecto |
|---|---|---|
| CSIC 2010 | [Directorio CSIC 2010 de msudol](https://github.com/msudol/Web-Application-Attack-Datasets/tree/master/OriginalDataSets/csic_2010) | Tres TXT de peticiones HTTP: entrenamiento normal, prueba normal y prueba anómala. |
| TorpEda 2012 | [Directorio de datos de DuckDuckBug](https://github.com/DuckDuckBug/cnn_waf/tree/master/data); [XML en `data/torpeda`](https://github.com/DuckDuckBug/cnn_waf/tree/master/data/torpeda) | Ocho XML con peticiones normales, anómalas y ataques. |
| SR-BH 2020 | [Harvard Dataverse — DOI 10.7910/DVN/OGOIXX](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/OGOIXX) | `data_capec_multilabel.csv`, con campos HTTP y etiquetas CAPEC. |
| DS-Augmented-v2 | [Repositorio WAMM de Cyshield](https://github.com/CyShield-Security-R-D/WAMM-Dataset-Repository); [DS_Augmented_v2.db.xz](https://github.com/CyShield-Security-R-D/WAMM-Dataset-Repository/blob/main/DS_Augmented_v2.db.xz) | La publicación ofrece SQLite; el pipeline utiliza un CSV preparado con petición completa y etiqueta. |

CSIC es el autor de CSIC 2010 y TorpEda 2012; los enlaces de GitHub proporcionan réplicas comunitarias en sus formatos HTTP y XML. Las fichas de cada corpus incluyen los archivos concretos y la referencia institucional. SR-BH se obtiene del repositorio de sus autores en Harvard Dataverse, y DS-Augmented-v2 del repositorio oficial de Cyshield. Los enlaces describen dónde obtener los datos, sin afirmar que una descarga actual sea idéntica a la entrada de una corrida histórica.

Para preparar una ejecución:

1. Elegir la etapa experimental y revisar sus entradas, esquema, etiquetas y particiones en el [índice experimental](../04_experimentos/README.md) y las auditorías enlazadas.
2. Descargar el corpus público en una ubicación externa al repositorio, accesible desde los nodos de Arandu. Conservar la versión o revisión utilizada, los nombres de archivo, los tamaños y los SHA-256 de la descarga.
3. Mantener los TXT de CSIC y los XML de TorpEda en su formato de petición. Preparar el CSV de DS-Augmented-v2 según [su ficha](DSAugmentedV2/README.md). Aplicar el parser y la taxonomía de la etapa elegida; una matriz de otra representación no sustituye esa preparación.
4. Configurar las rutas del lanzador y enviar el trabajo mediante `sbatch`, siguiendo la [guía del entorno Slurm](../07_reproducibilidad/ENTORNO_SLURM.md). Guardar el identificador de job, la configuración, los hashes de entrada y código, los reportes de filtrado y las salidas en un directorio propio de la nueva corrida.

En la evidencia histórica, el proyecto reside en `/home_data/aroman/TFG/waf-ml-starter`. TorpEda usa `data/raw/torpeda/`, Harvard `data/raw/harvard/data_capec_multilabel.csv` y DS-Augmented-v2 `egipcios/DS_Augmented_v2_csv/combined_data.csv`. Estas son rutas de ejecución registradas, que deben ajustarse al espacio asignado al nuevo usuario. Los corpus completos y las matrices de entrenamiento no se publican en estas carpetas de documentación.

La entrada Harvard identificada por la auditoría tenía 436.437.661 bytes y SHA-256 `9c73c90ce6564ae48b14f7179cd864d037a6a130ef69c68c1626ec5d7ce4a910`. El mismo hash figura en `input_fingerprints` de la [configuración de la extensión 73](../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/3datasetsMulticlase3/multiclase/harvard/run_config.json). Este identificador corresponde a esa entrada histórica; no es una verificación de la descarga pública actual.

Dos lanzadores preliminares requieren versiones no presentes en el código publicado: `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py`. El multifamily sin `DEFINITIVO` y el multiclass v12 tienen otros nombres y versiones; no constituyen reemplazos históricos acreditados. La [evidencia de multiclase](../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.md) documenta esta limitación. Para cada ejecución nueva, registrar qué versión se utiliza y evitar atribuirle automáticamente las métricas de otra.

## 2. Harvard: del original a sus derivados

| Derivado / fase | Filas o grupos | Qué cambia |
|---|---:|---|
| Tamaño publicado citado por el libro | 907.814 filas | Referencia bibliográfica; se distingue del recuento de la entrada histórica auditada. |
| CSV de entrada histórica auditado | 907.815 eventos | Recontado: 525.195 normales y 382.620 con al menos una CAPEC. |
| Multiclase M1, nueve familias | 907.815 eventos | Job 2534: `optimized-family` y resolución `severity`; frecuencia mínima 20 sin exclusiones. Train/test: 726.252/181.563. |
| Top14 multiclase | 902.411 eventos | Conserva 14 combinaciones exactas frecuentes; excluye 5.404 eventos de 46 combinaciones. |
| Top11 y Top10 | 902.411 eventos | Parten de Top14 y fusionan clases; conservan filas, cambian el objetivo. |
| Auditoría por 15 campos con peticiones vacías | 542.991 grupos totales | Incluye un grupo con los dos eventos vacíos. |
| Entrada válida L2 | 907.813 eventos | Excluye los dos eventos sin contenido en los 15 campos de petición. |
| Procesado L2 por huella | 542.990 grupos | Agrupa, une CAPEC mediante OR; 171.348 grupos normales y 371.642 con ataque. |
| Test L1 | 181.563 eventos | Por filas históricas; contiene repeticiones de petición respecto de desarrollo. |
| Test L2 | 108.598 grupos | Separación por grupo, con huellas disjuntas en las particiones reconstruidas. |

Fuentes: [perfil del CSV histórico](../02_auditoria/datasets_y_multiclase/sr_bh_raw_profile.json), [evidencia multiclase](../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.md) y [evidencia multietiqueta](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md); libro PDF 48–52 / pp. 32–36 y PDF 75–76 / pp. 59–60; presentación D45–48. Las configuraciones identifican M1/job 2534, M2/job 2657 y M3/job 2687. Son ramas de preparación diferentes: Top14 no se obtiene de la deduplicación L2, ni las 902.411 filas son una versión sin repetidos.

El perfil histórico registra 60 combinaciones, ningún registro CSV mal formado, ninguna fila con NORMAL y una CAPEC simultáneas y ninguna fila con las 14 etiquetas a cero. Hay dos eventos con los 15 campos HTTP vacíos: registros 14.411 y 163.885, numerados desde 1. El CSV puede ser sintácticamente válido y contener una petición vacía; por eso el [análisis de combinaciones](taxonomias_y_capec/analisis_combinaciones_capec.xlsx) informa 907.815 «válidos» y L2 usa 907.813 bajo otra regla.

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

Fuente: [perfil del CSV histórico](../02_auditoria/datasets_y_multiclase/sr_bh_raw_profile.json). Los análisis de combinaciones coinciden con ese perfil. La frecuencia exacta «solo SQL Injection» es 248.093; no es el marginal 250.311 que incluye combinaciones. CAPEC-248 tiene un único positivo y se excluye como objetivo de las evaluaciones L1/L2 de doce etiquetas; se conserva en la fuente y en el procesado previo al descarte. NORMAL se deriva de no activar objetivos CAPEC. Véase la [evidencia multietiqueta](../02_auditoria/particiones_y_multietiqueta/multietiqueta_evidencia.md), el libro PDF 56–58 / pp. 40–42 y PDF 75–76 / pp. 59–60.

| Etapa | Representación del objetivo |
|---|---|
| M1 | Nueve familias Harvard, incluido NORMAL; configuración del job 2534 con `optimized-family`. No equivale a nueve CAPEC originales. |
| M2–M4 | Catorce combinaciones exactas admitidas, incluida NORMAL. |
| M5 Top11 | CAPEC-153 y 194 pasan a DataManipulation; CAPEC-272,274 y 272+274 pasan a HTTPProtocolManipulation. |
| M6–M8 Top10 | Esas cinco categorías fuente se reúnen en RequestManipulation. CAPEC-88+126 permanece como una clase compuesta. |
| L1/L2 | Doce objetivos CAPEC separados; no se aplica la fusión Top10. L2 agrupa peticiones, no fusiona las identidades CAPEC objetivo. |
| Extensión 73 | Harvard conserva Top10; tiene una representación distinta y ejecución propia. |

Evidencia: [revisión de datasets y multiclase](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md), [configuraciones y reportes de M1–M3](../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.md) y [pipelines](../05_codigo/pipelines/); libro PDF 55, 72, 75 / pp. 39, 56, 59; presentación D19–20 y D39–46.

En M1 las familias guardadas son NORMAL, SQLi, DataManipulation, CommandInjection, CRLFi, PathTraversal, HTTPProtocolManipulation, VulnerabilityScanning y PasswordAttack. En M2/M3 se conservan las 14 combinaciones exactas admitidas y se excluyen 5.404 filas de 46 combinaciones. La [auditoría de multiclase](../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.json) registra los nombres y conteos leídos de sus reportes de filtrado; no se debe aplicar retrospectivamente Top14 al M1 de nueve familias.

## 4. TorpEda y DS-Augmented-v2

TorpEda conserva NORMAL (8.363), ANOMALOUS (16.459), SQLi (43.013), XSS (4.818), SSI (451), BufferOverflow (412), CRLFi (327), XPath (175), LDAPi (74) y FormatString (41). Estos conteos están documentados en la [auditoría de datasets y multiclase](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md). El mínimo soporte de algunas clases explica por qué accuracy y F1 macro pueden moverse en direcciones diferentes; siempre conservar las métricas por clase y sus denominadores. La [imagen de taxonomía](taxonomias_y_capec/c7662371-aa01-40c7-9bc3-35200ff5d058.png) muestra las nueve categorías distintas de NORMAL, sin métricas.

DS-Augmented-v2 conserva 704.665 registros en M7/M8. Tras la unión de dos clases de comando, sus ocho clases son NORMAL (493.515), SQLi (146.086), CommandInjection (38.711), PathTraversal (17.718), XSS (2.894), SSRF (2.645), SSTI (1.897) y CodeInjection (1.199). En la extensión de 73 variables, CommandInjection (2.597) y OSCommandInjection (36.114) se mantienen separadas y quedan nueve clases. Las métricas de esa extensión no deben interpretarse como una ablación de una sola variable respecto de M8: cambian representación, clases y política de pesos. Véase la [revisión multiclase](../02_auditoria/datasets_y_multiclase/REVISION_DATASETS_Y_MULTICLASE.md) y el libro PDF 49, 75 / pp. 33, 59. Estos son conteos de las corridas históricas; compartir el total de filas de una publicación actual no demuestra igualdad de contenidos ni de etiquetas.

## 5. Representación, huella y particiones

El catálogo binario incluye RF-25, RF-33, RF-57 y RF-10-Gini. RF-34 es un alias histórico incorrecto para 25 + 8 = 33; debe conservarse el nombre original con la aclaración. OCSVM con 26/34 variables pertenece a otros antecedentes. Multiclase usa 30 → 84 → 58 → 72; la extensión posterior 73 es otra versión. Multietiqueta compara fixed30 y request90. El orden de las variables y el extractor, además del número, forman parte de la identidad de un esquema. Véanse la [revisión binaria](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md), los [esquemas documentados](esquemas/), el libro PDF 71–75 / pp. 55–59 y D20, D34, D38, D45.

La [huella de identidad](esquemas/huella_peticion_15_campos.json) usa 15 campos de petición y BLAKE2b de 128 bits; el hash del archivo es SHA-256. La firma request90 se calcula a partir del identificador de versión y la lista ordenada de variables. La `input_signature` L2 resume ruta/tamaño/mtime y no es un SHA del contenido bruto. Conservar estos identificadores con su tipo y función.

Las configuraciones M1–M8 documentadas usan 80/20 por filas y semilla 42, con consultas históricas a la prueba durante el desarrollo. La [auditoría de M1–M3](../02_auditoria/datasets_y_multiclase/S13_multiclase_evidencia.json) confirma fixed30 en M1/M2 y optimized84 en M3, con catálogos ordenados iguales a las listas estáticas del código inspeccionado; fixed30 coincide también con el anexo del libro. Esta comprobación posterior conserva su propio alcance y no acredita el hash histórico de cada Python ejecutado.

L1 usa 581.001/145.251/181.563 eventos. L2 usa 347.513/43.439/43.440/108.598 grupos, semillas 42/43/44, y separa selección y umbrales. La [verificación posterior de L2](../02_auditoria/particiones_y_multietiqueta/verificacion_20261010/L2_verificacion.json) reconstruyó particiones y confirmó seis intersecciones de huellas iguales a cero. No se dispone de las listas históricas completas de entrenamiento, selección y calibración; las listas reconstruidas en octubre de 2026 se identifican como tales.

## 6. Archivos estadísticos y auditoría de calidad

[ataques.xlsx](taxonomias_y_capec/ataques.xlsx) contiene 13 encabezados CAPEC y 14 tipos de ataque con la matriz de correspondencias vacía. Es una propuesta incompleta, no un mapeo etiquetado. La planilla `estadisticas harvard.xlsx`, disponible en [taxonomías y CAPEC](taxonomias_y_capec/), contiene las 60 combinaciones verificadas. [analisis_combinaciones_capec.xlsx](taxonomias_y_capec/analisis_combinaciones_capec.xlsx) agrega diccionario, marginales y coocurrencias. Estos archivos son documentos de análisis y no reemplazan las entradas descargables.

El [reporte de auditoría de duplicados](../02_auditoria/datasets_y_multiclase/S10_auditoria_excel_recalculado.json) documenta los recuentos de la planilla histórica `harvard_duplicados.xlsx`, consistentes con el universo que incluye vacíos. El formato Excel puede truncar celdas largas y escapar caracteres; no sustituye al CSV completo. Los conflictos, exclusiones y duplicados se documentan en [02_auditoria](../02_auditoria/README.md), mientras que estas fichas indican cómo obtener cada corpus y cómo relacionarlo con su configuración experimental.
