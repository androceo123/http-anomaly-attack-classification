# CSIC 2010

CSIC 2010 participa en el desarrollo binario y en los antecedentes de detección de anomalías. Esta ficha documenta la descarga y la preparación de las entradas para las ejecuciones en Arandu con Slurm. El corpus completo se mantiene fuera del repositorio.

## Descarga y archivos de entrada

Utilizar el [directorio CSIC 2010 de msudol](https://github.com/msudol/Web-Application-Attack-Datasets/tree/master/OriginalDataSets/csic_2010). Es una réplica comunitaria del corpus creado por CSIC; su documentación distingue los TXT de peticiones HTTP de las versiones reformateadas. La [referencia institucional](https://www.tic.itefi.csic.es/dataset/) identifica la fuente original, aunque su disponibilidad puede variar.

| Archivo | Función en el corpus | Descarga directa |
|---|---|---|
| `normalTrafficTraining.txt` | Peticiones normales para entrenamiento | [TXT](https://raw.githubusercontent.com/msudol/Web-Application-Attack-Datasets/master/OriginalDataSets/csic_2010/normalTrafficTraining.txt) |
| `normalTrafficTest.txt` | Peticiones normales de prueba | [TXT](https://raw.githubusercontent.com/msudol/Web-Application-Attack-Datasets/master/OriginalDataSets/csic_2010/normalTrafficTest.txt) |
| `anomalousTrafficTest.txt` | Peticiones anómalas de prueba | [TXT](https://raw.githubusercontent.com/msudol/Web-Application-Attack-Datasets/master/OriginalDataSets/csic_2010/anomalousTrafficTest.txt) |

Estos archivos contienen peticiones HTTP con su línea inicial, cabeceras y cuerpo. La revisión del repositorio de descarga identificada el 10 de octubre de 2026 es `424c6e1c1951570473d9d6c0227eaaac6fdd6d02`. Al preparar una corrida, registrar la revisión que realmente se descargue y los SHA-256 de sus tres archivos. La comprobación de su formato no acredita por sí sola igualdad con todas las entradas históricas usadas por el proyecto.

## Preparación para Arandu y Slurm

1. Descargar los tres TXT en el almacenamiento de trabajo accesible desde los nodos de cómputo. El lanzador histórico usa `data/raw/csic/` bajo el directorio del proyecto.
2. Conservar separados los tres archivos y aplicar la selección de entradas correspondiente al experimento. Los antecedentes one-class y los benchmarks binarios no necesariamente evalúan la misma población.
3. Revisar el [cargador CSIC](../../05_codigo/base_binaria_historica/waf-ml-starter/src/waf_ml/data/csic_loader.py) y la versión del extractor antes de construir los atributos. El número de variables por sí solo no identifica una representación.
4. Ajustar las rutas y los recursos del lanzador según la [guía del entorno Slurm](../../07_reproducibilidad/ENTORNO_SLURM.md), enviar el trabajo mediante `sbatch` y conservar sus entradas, configuración, particiones y logs bajo una nueva identidad de corrida.

El [lanzador one-class](../../05_codigo/pipelines/run_csic_oneclass_gpu_optimo.sh) acepta `PROJECT_DIR` y `RAW_DIR`; la configuración de otros antecedentes debe revisarse en su propio código. El [catálogo de datasets](../README.md) explica los esquemas y la relación entre los corpus.

## Corridas y alcance de la evidencia

El [índice experimental](../../04_experimentos/README.md) y la [revisión de Slurm y del desarrollo binario](../../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) reúnen la evidencia de estas etapas:

- **B1, ablación de atributos:** comparación de conjuntos de 25, 33, 57 y 10 atributos. El alias histórico RF34 corresponde a 33 atributos; no debe confundirse con el conjunto de 34 de OCSVM.
- **B2, comparación de corpus:** entrenamientos Random Forest independientes por corpus. El nombre histórico `cross_dataset` no demuestra transferencia de un modelo entre datasets.
- **Antecedentes one-class:** configuraciones y salidas históricas de detección de anomalías, con sus propias entradas y representaciones.

No se atribuye un único tamaño de evaluación a todas estas etapas: el libro no fija claramente el total de CSIC utilizado en B2. Las etapas binarias mantienen el carácter exploratorio explicado por la tesis, incluida la consulta al conjunto de prueba durante el desarrollo. Una ejecución nueva debe documentar sus propios denominadores y no asumir que reproduce los resultados históricos por utilizar el mismo nombre de corpus.
