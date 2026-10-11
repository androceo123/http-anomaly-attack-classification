# Entorno de ejecución: Arandu y Slurm

Los experimentos se organizaron como trabajos batch en Arandu, con código Python, entornos virtuales y directorios de datos/resultados accesibles desde los nodos de cómputo. Esta guía relaciona los lanzadores del repositorio con las evidencias de ejecución y explica cómo preparar una nueva corrida.

La ruta de trabajo registrada en numerosos jobs es `/home_data/aroman/TFG/waf-ml-starter`. Es una ruta del entorno experimental; cada persona debe configurar sus propias rutas antes de enviar un trabajo. Los ejemplos siguientes usan un directorio de trabajo nuevo y el código de `05_codigo/`.

## 1. Infraestructura documentada

La captura de infraestructura corresponde al **3 de agosto de 2026**. El nombre del host de envío es `arandu`; el identificador de clúster registrado por Slurm es `cluster`. Las fuentes son los [inventarios de nodos](../02_auditoria/historial_slurm/evidencia_20260803/inventario_actual_nodos/), la [versión de comandos](../02_auditoria/historial_slurm/evidencia_20260803/slurm_actual/versiones_comandos.txt) y las [particiones](../02_auditoria/historial_slurm/evidencia_20260803/slurm_actual/scontrol_particiones.txt).

| Componente | Valor observado en la captura |
|---|---|
| Slurm | 24.11.5 |
| Sistema operativo de c1, c2 y c3 | AlmaLinux 9.4; kernel Linux `5.14.0-427.35.1.el9_4.x86_64` |
| Servidores c1, c2 y c3 | Dell PowerEdge R740 |
| CPU por nodo examinado | 2 sockets Intel Xeon Gold 6242 a 2,80 GHz; 16 núcleos por socket; 32 CPU lógicas visibles; 1 hilo por núcleo |
| Memoria configurada por nodo en Slurm | `RealMemory=128000` MiB, presentada también como `mem=125G` |
| GPU en c1, c2 y c3 | Una Tesla V100 PCIe de 16 GiB por nodo, visible en las capturas con asignación GPU |
| Controlador NVIDIA observado | 560.35.03; `nvidia-smi` informa compatibilidad CUDA 12.6 |
| Almacenamiento del proyecto | `/home_data` montado mediante NFS en los nodos examinados |
| Python del sistema | `/usr/bin/python`, versión 3.9.18 |
| Python del entorno del proyecto | `.venv/bin/python`, versión 3.11.7 |

El dato CUDA corresponde a la salida de `nvidia-smi`; por sí solo no identifica la versión del toolkit ni las bibliotecas utilizadas por cada entrenamiento. La captura tampoco acredita que todos los jobs anteriores hayan tenido exactamente este entorno.

| Partición | Nodos en la captura | Tiempo máximo configurado | Memoria máxima configurada por nodo para una asignación |
|---|---|---:|---:|
| `normal` — predeterminada | `c1`, `c2`, `c3` | 7 días | 65.536 MiB, equivalentes a 64 GiB |
| `gpu` | `c4` | 3 días | 65.536 MiB, equivalentes a 64 GiB |

La partición `normal` también declaraba recursos `gres/gpu`; el nombre de la partición no determina por sí solo el backend del modelo. La [salida de `sinfo`](../02_auditoria/historial_slurm/evidencia_20260803/slurm_actual/sinfo_nodos.txt) incluye `c4`, pero los inventarios detallados de CPU/GPU conservados cubren c1–c3. No se atribuye a c4 el hardware de esos otros nodos.

Para una ejecución nueva, consultar la configuración vigente antes de elegir recursos:

```bash
sinfo -Nel
scontrol show partition normal
scontrol show node c3
```

## 2. Qué recursos constan para los jobs

Los recursos de cada ejecución deben leerse en su registro de contabilidad y en sus logs/configuraciones. Estos ejemplos proceden de [sacct_jobs_asignacion.psv](../02_auditoria/historial_slurm/evidencia_20260803/sacct/sacct_jobs_asignacion.psv). Todos terminaron con estado `COMPLETED`; la tabla muestra tiempo transcurrido del job y memoria asignada, no una medición del pico de RAM del modelo.

| Job | Lanzador registrado | Nodo | CPU asignadas | Memoria asignada | Tiempo transcurrido |
|---:|---|---|---:|---:|---:|
| 2534 | `run_DEFINITIVO_multiclass_histgb_fixed30_arandu_safe.sh` | c2 | 8 | 32 GiB | 01:49:46 |
| 3013 | `10claseResults.sh` | c3 | 8 | 64 GiB | 01:46:05 |
| 3068 | `3datasetsMulticlase.sh` | c3 | 8 | 64 GiB | 10:24:04 |
| 3151 | `run_resume_multilabel_xgb_cpu_c2.sh` | c2 | 8 | 32 GiB | 00:32:44 |
| 3289 | `3datasetsMulticlase2.sh` | c2 | 8 | 64 GiB | 02:57:23 |
| 3315 | `multietiquetaCorrida2.sh` | c3 | 16 | 60 GiB | 00:39:10 |
| 3361 | `3datasetsMulticlase3.sh` | c3 | 8 | 64 GiB | 06:03:24 |

El job 3151 reanudó procesamiento y entrenamiento previos desde checkpoints. Su tiempo no representa el costo de entrenar desde cero. Aunque su nombre de job conserva `gpu3`, la línea de envío especifica `USE_GPU=off`. El job 3315 también corresponde a CPU: su lanzador utiliza `--use-gpu off`. HistGradientBoosting se ejecuta con CPU en los pipelines correspondientes. Para contrastar resultados, recursos y backend se dispone de la [revisión de Slurm](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) y los [vínculos entre configuraciones y jobs](../02_auditoria/historial_slurm/vinculos_config_job.csv).

Hay tres niveles de evidencia que conviene distinguir:

1. **Contabilidad del job:** nodo, recursos solicitados/asignados, tiempos, estado y comando de envío.
2. **Configuración y logs de esa corrida:** argumentos, backend efectivo, versiones que realmente se registraron y reutilización de checkpoints.
3. **Inventario fechado del entorno:** hardware/software observado el día de la captura, con el alcance y las interrupciones que documenta cada archivo.

La coincidencia entre un nombre de script y un comando histórico identifica un candidato. La identidad exacta del código requiere una huella conservada. Por ejemplo, el log de 3361 registra el SHA-256 de `3datasetsMulticlase3.py`; el lanzador también comprueba esa huella. La recuperación posterior de los batch antiguos no produjo scripts válidos, como explica la revisión de Slurm.

## 3. Entorno Python y dependencias

El [inventario de c2 con CPU](../02_auditoria/historial_slurm/evidencia_20260803/inventario_actual_nodos/inventario_actual_c2_cpu.txt) conserva el listado completo de paquetes del entorno inspeccionado. Los siguientes son los principales para los pipelines de esta guía:

| Paquete | Versión observada |
|---|---:|
| NumPy | 2.4.0 |
| pandas | 2.3.3 |
| SciPy | 1.17.1 |
| scikit-learn | 1.8.0 |
| XGBoost | 3.2.0 |
| joblib | 1.5.3 |
| psutil | 7.2.2 |
| PyArrow | 22.0.0 |
| Matplotlib | 3.11.0 |
| PyYAML | 6.0.3 |
| tqdm | 4.67.1 |

Los archivos de dependencias tienen un alcance distinto. El [requirements de la base binaria](../05_codigo/base_binaria_historica/waf-ml-starter/requirements.txt) incluye la instalación editable `-e .`, pero no declara XGBoost ni Matplotlib. El [requirements de la captura del proyecto](../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/requirements.txt) añade XGBoost 3.2.0 y fija Matplotlib 3.10.9; esta última versión difiere de la instalada que informa el inventario. Mantener esa distinción permite reconstruir el entorno sin convertir una declaración de dependencias en prueba de lo instalado en cada job.

### Preparación de un directorio de trabajo

Ejecutar lo siguiente desde la raíz del repositorio clonado. `PROJECT_DIR` debe quedar en un sistema de archivos al que también accedan los nodos de cómputo. Elegir una ubicación con espacio suficiente para datos, cachés, modelos y resultados.

```bash
REPO_DIR="$(pwd -P)"
export PROJECT_DIR="$HOME/http-anomaly-runs/ejecucion-$(date +%Y%m%dT%H%M%S)"
export VENV_DIR="$PROJECT_DIR/.venv"

mkdir -p "$PROJECT_DIR/logs" \
  "$PROJECT_DIR/data/raw/harvard" \
  "$PROJECT_DIR/data/raw/torpeda" \
  "$PROJECT_DIR/data/raw/csic" \
  "$PROJECT_DIR/data/raw/egipcios"

python3.11 -m venv "$VENV_DIR"
(
  cd "$REPO_DIR/05_codigo/base_binaria_historica/waf-ml-starter"
  "$VENV_DIR/bin/python" -m pip install -r requirements.txt
)
"$VENV_DIR/bin/python" -m pip install \
  scipy==1.17.1 xgboost==3.2.0 matplotlib==3.11.0
"$VENV_DIR/bin/python" -m pip check
"$VENV_DIR/bin/python" -m pip freeze > "$PROJECT_DIR/logs/requirements_instalados.txt"
```

Esta receta propone preparar las dependencias principales observadas para los ejemplos de CPU. Su ejecución requiere acceso a los paquetes y a un intérprete compatible del clúster; no constituye una validación de instalación ni una nueva ejecución experimental. El `pyproject.toml` de la base exige Python ≥ 3.10, y sus jobs históricos invocan `.venv/bin/python3.11`. La disponibilidad de `/usr/bin/python` no basta para esos lanzadores.

El pipeline one-class con GPU contempla cuML/CuPy y, para su autoencoder opcional, PyTorch. Otros motores pueden incorporar CatBoost, LightGBM o utilidades adicionales. Esas ramas requieren sus dependencias específicas y una configuración GPU compatible; no quedan cubiertas por la receta de CPU.

## 4. Descarga y preparación de datos

Los datos se obtienen de las [fuentes públicas de los datasets](../03_datasets/README.md). Las fichas incluyen enlaces de descarga y condiciones de preparación. Los archivos crudos se colocan en el almacenamiento de trabajo del clúster; los pipelines generan sus propias características, particiones y resultados.

| Dataset y ficha de descarga | Entrada esperada por el código | Variable de los lanzadores |
|---|---|---|
| [SR-BH 2020 / Harvard](../03_datasets/SRBH2020/README.md) | Tabla CSV/TSV con campos HTTP y etiquetas CAPEC. Los valores por defecto incluyen `request_http_method`, `request_http_request`, `request_body` y `000 - Normal`; L2 también recibe `request_http_protocol`. | `HARVARD_RAW_DIR` |
| [TorpEda 2012](../03_datasets/TorpEda2012/README.md) | Archivos XML del corpus; los lanzadores multiclase buscan `*.xml`. | `TORPEDA_RAW_DIR`; el lanzador TorpEda v10 usa `RAW_DIR` con respaldo en esa variable. |
| [CSIC 2010](../03_datasets/CSIC2010/README.md) | `normalTrafficTraining.txt`, `normalTrafficTest.txt` y `anomalousTrafficTest.txt` para `run_csic_oneclass_gpu_optimo.sh`. | `RAW_DIR` en ese lanzador. |
| [DS-Augmented-v2 / WAMM, alias Egipcios](../03_datasets/DSAugmentedV2/README.md) | `combined_data.csv`: `col1` contiene la petición HTTP completa; `col2` contiene la etiqueta textual. La distribución estricta del pipeline compact73 exige 704.665 filas y nueve clases. | `EGIPCIOS_INPUT` en `3datasetsMulticlase3.sh`. |

Para Harvard, usar una única copia de cada tabla original. Los cargadores que reciben una carpeta concatenan las tablas compatibles que encuentran: incluir allí otra copia del corpus o una salida de análisis altera el universo de entrada. Para TorpEda debe descargarse la versión XML que consumen estos cargadores; un corpus convertido a otro formato no es una entrada intercambiable por su nombre.

### Preparación de DS-Augmented-v2

La fuente pública ofrece una base SQLite. Después de obtener `DS_Augmented_v2.db` siguiendo la ficha del dataset, se puede utilizar el [exportador conservado](../02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/egipcios/export_db_to_csv.py):

```bash
TFG_EXPORTER="$REPO_DIR/02_auditoria/historial_slurm/evidencia_20260803/proyecto_actual/copias/egipcios/export_db_to_csv.py"
TFG_DATABASE="$PROJECT_DIR/data/raw/egipcios/DS_Augmented_v2.db"
export EGIPCIOS_INPUT="$PROJECT_DIR/data/raw/egipcios/combined_data.csv"

"$VENV_DIR/bin/python" "$TFG_EXPORTER" "$TFG_DATABASE" --list-tables
"$VENV_DIR/bin/python" "$TFG_EXPORTER" "$TFG_DATABASE" \
  --table combined_data --output "$EGIPCIOS_INPUT"
```

El exportador conserva los nombres de columna de la tabla. Verificar `col1` y `col2` antes del entrenamiento, junto con las etiquetas y el número de filas de la versión elegida. El comando `--list-tables` permite comprobar el nombre de tabla de la descarga. Si difiere, revisar su esquema antes de adaptar el argumento; renombrar un archivo no convierte otro corpus en la versión que esperan las guardas.

Las bases binarias pueden requerir Parquet preprocesado. Por ejemplo, `run_harvard_binary_rf.sh` espera `data/processed/harvard/harvard.parquet`, con `label_binary` y campos HTTP crudos. Preparar esa entrada con la versión de extractor correspondiente a la corrida; las variantes de `http_features.py` y `build_features_csic.py` no son equivalentes. El [índice de código](../05_codigo/README.md) y la [comparación de variantes](../02_auditoria/historial_slurm/variantes_codigo.csv) permiten elegir la implementación adecuada.

## 5. Envío de nuevas corridas

Las líneas `#SBATCH` de varios lanzadores contienen rutas absolutas del proyecto experimental. Exportar `PROJECT_DIR` cambia las rutas utilizadas por Bash/Python, pero no reescribe esas directivas. Por eso los ejemplos fijan también `--chdir`, `--output` y `--error` en el comando de envío. Las opciones se procesan antes de iniciar el script; los directorios de logs deben existir. Véase la [documentación oficial de `sbatch`](https://slurm.schedmd.com/sbatch.html).

Preparar este arreglo Bash una vez, después de crear el directorio de trabajo del apartado 3:

```bash
TFG_SBATCH_OPTIONS=(
  --partition=normal
  --nodelist=c3
  --chdir="$PROJECT_DIR"
  --output="$PROJECT_DIR/logs/slurm-%x-%j.out"
  --error="$PROJECT_DIR/logs/slurm-%x-%j.err"
)

export HARVARD_RAW_DIR="$PROJECT_DIR/data/raw/harvard"
export TORPEDA_RAW_DIR="$PROJECT_DIR/data/raw/torpeda"
```

Estos ejemplos se ejecutan en Bash y mantienen las variables preparadas en los apartados anteriores. Ajustar la partición y el nodo si se usa otro clúster. `CHECK_ONLY=1` tiene el alcance implementado por cada lanzador: en algunos revisa rutas, imports y sintaxis; en otros también invoca la validación de datos del Python. Una comprobación de entorno no demuestra que un entrenamiento completo terminará correctamente.

### Multietiqueta L2: request90 y XGBoost en CPU

El [lanzador L2](../05_codigo/pipelines/multietiquetaCorrida2.sh) admite `TRAIN_PY`, `VENV_DIR`, `HARVARD_RAW_DIR`, `RUN_ROOT`, `OUTPUT_DIR` y `CHECKPOINT_DIR`. Sus recursos predeterminados son 16 CPU, 60 GiB y 72 horas. Se limita la extracción a un máximo predeterminado de ocho workers y se usa XGBoost en CPU.

```bash
export TRAIN_PY="$REPO_DIR/05_codigo/pipelines/multietiquetaCorrida2.py"
export RUN_ROOT="$PROJECT_DIR/L2_request90"
export OUTPUT_DIR="$RUN_ROOT/harvard"
export CHECKPOINT_DIR="$RUN_ROOT/checkpoints"
export LOG_DIR="$RUN_ROOT/logs"
mkdir -p "$LOG_DIR"

sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=1 \
  "$REPO_DIR/05_codigo/pipelines/multietiquetaCorrida2.sh"
```

Después de revisar la salida de esa comprobación, enviar la corrida completa:

```bash
sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=0 \
  "$REPO_DIR/05_codigo/pipelines/multietiquetaCorrida2.sh"
```

El lanzador activa la reanudación por defecto. Utilizar otro `RUN_ROOT` para un experimento independiente; reutilizarlo únicamente cuando corresponda reanudar el mismo experimento con entradas, código y configuración compatibles.

### Multiclase HistGradientBoosting con fixed30

El [lanzador HistGB](../05_codigo/pipelines/run_DEFINITIVO_multiclass_histgb_fixed30_arandu_safe.sh) admite `TRAIN_PY` y `DEFINITIVO_DIR`. `RUN_DATASET` acepta `both`, `torpeda` o `harvard`. Los valores de recursos del archivo son 8 CPU, 32 GiB y 12 horas.

```bash
export TRAIN_PY="$REPO_DIR/05_codigo/pipelines/train_waf_multiclass_DEFINITIVO_histgb_fixed30.py"
export DEFINITIVO_DIR="$PROJECT_DIR/multiclase_fixed30"
export RUN_DATASET=both
export CLEAN_OUTPUT_DIR=0
export USE_GPU=off

sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=1 \
  "$REPO_DIR/05_codigo/pipelines/run_DEFINITIVO_multiclass_histgb_fixed30_arandu_safe.sh"
```

Para entrenar después de la comprobación:

```bash
sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=0 \
  "$REPO_DIR/05_codigo/pipelines/run_DEFINITIVO_multiclass_histgb_fixed30_arandu_safe.sh"
```

`CLEAN_OUTPUT_DIR=0` evita la limpieza automática que este lanzador habilita por defecto. Elegir una carpeta nueva para cada experimento. Los parámetros metodológicos —conjunto de características, taxonomía, pesos, particiones y umbrales— deben corresponder a la corrida que se quiera estudiar.

### Pipeline unificado de tres datasets con compact73

El [lanzador compact73](../05_codigo/pipelines/3datasetsMulticlase3.sh) fija el motor en `${PROJECT_DIR}/3datasetsMulticlase3.py` y la salida en `${PROJECT_DIR}/3datasetsMulticlase3`. No toma un `TRAIN_PY` alternativo del entorno. Crear en el directorio de trabajo un enlace al motor conservado:

```bash
ln -s "$REPO_DIR/05_codigo/pipelines/3datasetsMulticlase3.py" \
  "$PROJECT_DIR/3datasetsMulticlase3.py"

export EGIPCIOS_INPUT="$PROJECT_DIR/data/raw/egipcios/combined_data.csv"

sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=1 \
  "$REPO_DIR/05_codigo/pipelines/3datasetsMulticlase3.sh"
```

Para entrenar después de la comprobación:

```bash
sbatch "${TFG_SBATCH_OPTIONS[@]}" --export=ALL,CHECK_ONLY=0 \
  "$REPO_DIR/05_codigo/pipelines/3datasetsMulticlase3.sh"
```

Este lanzador solicita 8 CPU, 64 GiB y 48 horas; exige un motor Parquet y la herramienta `flock`, verifica la huella SHA-256 de su Python y conserva guardas de taxonomía/distribución. El vínculo entre `.sh` y `.py` es parte de la configuración. Si falla la huella, revisar qué versión se está utilizando antes de cambiarla. Para iniciar otro experimento compact73, preparar otro `PROJECT_DIR`, porque la ubicación de salida se deriva de él.

## 6. Particularidades y componentes pendientes

| Lanzador o componente | Condición que debe resolverse antes de usarlo |
|---|---|
| Base binaria `waf-ml-starter/jobs/` | Varios jobs ejecutan `cd "$SLURM_SUBMIT_DIR"`, usan `.venv/bin/python3.11` y `PYTHONPATH=src`. Enviarlos desde una copia de trabajo completa de `waf-ml-starter`, con datos preparados y su entorno, conserva esas relaciones. No basta con situarse en `jobs/`. |
| README histórico de la base binaria | Referencia `waf_ml.scripts.train_ocsvm` y `waf_ml.waf.proxy`, módulos que no están presentes. `train_ocsvm_updated.py` y `optimo/ocsvmOptimo.py` existen, pero su interfaz debe revisarse antes de sustituir un comando. |
| `run_torpeda_multiclass_fixed30_optimo_sbatch_v10_normal_sharedgpu.sh` | Espera `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py`, motor que no se conserva con ese nombre. No atribuir a otra versión los resultados de esa ejecución. |
| `run_multilabel_harvard_multifamily_resume_resultsOptimo_arandu_safe_fixed30.sh` | Su nombre de motor predeterminado incluye `DEFINITIVO`; el Python conservado `train_waf_multilabel_multifamily_resume_resultsOptimo_fixed30.py` no lo incluye. Verificar interfaz/versión y configurar `TRAIN_PY` explícitamente si corresponde. |
| `run_resume_multilabel_xgb_cpu_c2.sh` y `run_resume_multilabel_xgb_cpu_c3.sh` | Aunque no solicitan GPU en sus directivas activas, conservan `USE_GPU=on` por defecto y comentarios de una variante previa. Para CPU, exportar `USE_GPU=off`, como figura en el envío histórico de 3151. |
| `run_csic_oneclass_gpu_optimo.sh` | Usa `PY_SCRIPT`, `RAW_DIR`, `PROCESSED_DIR` y `RESULTS_DIR`; no implementa `CHECK_ONLY=1`. No interpretar esa variable como una prueba sin entrenamiento para este archivo. |

El [índice de código](../05_codigo/README.md) y la [revisión de evidencia](../02_auditoria/historial_slurm/REVISION_SLURM_Y_BINARIO.md) documentan las versiones y las limitaciones de asociación histórica. Una nueva ejecución debe registrar sus propios archivos y su configuración efectiva.

## 7. Evidencia que debe acompañar a una nueva corrida

Guardar el identificador devuelto por `sbatch` y conservar los logs con `%j`. Mientras el controlador retenga el job, `scontrol show job` permite registrar su configuración. Para consultar el estado y los pasos posteriormente, usar `sacct`; su [documentación oficial](https://slurm.schedmd.com/sacct.html) describe los campos de contabilidad.

```bash
TFG_JOB_ID=12345  # Sustituir por el identificador devuelto por sbatch.
squeue -j "$TFG_JOB_ID"
scontrol show job "$TFG_JOB_ID"
sacct -j "$TFG_JOB_ID" --parsable2 \
  --format=JobID,JobName,Partition,State,ExitCode,Elapsed,NodeList,AllocCPUS,ReqMem,MaxRSS \
  > "$PROJECT_DIR/logs/sacct-$TFG_JOB_ID.psv"
```

Conservar también el commit del repositorio, SHA-256 del Python y del lanzador enviados, huellas de los datos, argumentos efectivos, `run_config.json`, estado de reanudación, versiones instaladas y salidas de métricas. Cuando se mida memoria, revisar todos los pasos de la aplicación: el pico del wrapper `.batch` puede ser distinto del pico del proceso Python. Una fila del job y sus pasos no deben sumarse como si fueran ejecuciones independientes.

Para interpretar latencia y throughput, registrar el número de filas medido y distinguir entrenamiento, extracción, evaluación y reutilización de checkpoints. Estos datos permiten comparar nuevas ejecuciones con la evidencia conservada sin atribuir a una captura posterior o a un nombre de archivo información que no demuestra.

Esta guía se basa en la lectura de código, configuración y evidencias existentes. La verificación de integridad y los análisis de resultados disponibles se describen en el [índice de reproducibilidad](README.md); no se presenta aquí una repetición ejecutada de los entrenamientos.
