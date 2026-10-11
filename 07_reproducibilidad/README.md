# Reproducibilidad, entorno e integridad

## 1. Preparar una ejecución en Slurm

La [guía de Arandu y Slurm](ENTORNO_SLURM.md) relaciona la infraestructura registrada, los entornos Python y los lanzadores publicados. Incluye ejemplos de comprobación previa y envío para L2, multiclase fixed30 y la extensión de 73 atributos.

Los datos se obtienen desde las [fuentes públicas](../03_datasets/README.md). Cada ficha explica el formato original, la entrada que espera el código y las transformaciones que deben registrarse. Las matrices procesadas, predicciones, checkpoints y modelos son artefactos de una corrida; no forman parte de la descarga original del dataset.

## 2. Verificar el contenido del repositorio

Desde la raíz, con Python 3.11 o posterior:

```bash
python 07_reproducibilidad/scripts/verificar_integridad.py --root .
```

El comando compara tamaño y SHA-256 de los archivos enumerados en [manifest_repositorio.json](manifest_repositorio.json). Ese manifiesto describe la revisión publicada. Excluye su propio contenido y el informe de verificación para evitar referencias circulares; las exclusiones quedan declaradas. Los archivos adicionales que genere una nueva corrida no se incorporan automáticamente a esta comprobación.

El [informe de integridad](verificacion_integridad_local.json) conserva el resultado de la revisión del repositorio. Para producir otro informe sin sobrescribirlo:

```bash
python 07_reproducibilidad/scripts/verificar_integridad.py \
  --root . --output verificaciones_nuevas/integridad.json
```

Códigos de salida: `0` si coinciden los archivos comprobados, `1` si hay faltantes o diferencias, y `2` ante errores de configuración o formato. Esta comprobación no ejecuta entrenamientos ni deserializa modelos.

## 3. Catálogos de evidencia histórica

Los identificadores S01–S14 representan [colecciones de evidencia](../02_auditoria/integridad_y_procedencia/fuentes_originales.csv). Permiten relacionar versiones, resultados, informes y registros del clúster.

| Archivo | Función |
| --- | --- |
| [Inventario de evidencia](../02_auditoria/integridad_y_procedencia/inventario_archivos.json) | Mantiene las identidades por colección: ruta original, tamaño, SHA-256, corrida, dataset y decisiones documentadas. |
| [Catálogo de identidades](catalogo_archivos.json) | Registra los archivos experimentales catalogados y distingue sus copias publicadas de las referencias sin archivo publicado. |
| [Artefactos externos](artefactos_externos.csv) | Identifica entradas y resultados adicionales requeridos por los análisis; incluye fuentes públicas de datos cuando corresponde. |
| [Catálogo de corridas](../06_resultados_consolidados/catalogo_corridas.csv) | Relaciona cada etapa con sus auditorías y muestra la disponibilidad de sus artefactos. |

`repository_path` señala una copia publicada con el mismo SHA-256 registrado. Un valor nulo y `availability=referenciado_no_publicado` indican que la identidad está documentada, pero que sus bytes no están en el repositorio. Las referencias `Sxx:ruta` identifican elementos de una colección; no son rutas del sistema de archivos ni enlaces de descarga.

Las rutas relativas del inventario permiten colocar archivos requeridos en un almacenamiento experimental aparte. Si se dispone de todos los artefactos históricos, se puede ampliar la comprobación:

```bash
python 07_reproducibilidad/scripts/verificar_integridad.py \
  --root . --include-external --external-root /ruta/a/artefactos
```

Esta opción exige todos los archivos del catálogo histórico. Su ausencia genera un fallo de la comprobación ampliada y no se considera un defecto del manifiesto de archivos publicados. Las fuentes públicas enlazadas permiten obtener los datasets; no se presentan como descargas de predicciones o modelos históricos.

## 4. Recalcular resultados multietiqueta

El [auditor L1/L2](VERIFICACION_MULTIETIQUETA.md) resuelve las entradas por nombre, colección, corrida y SHA-256. Requiere los CSV de predicciones y métricas, configuraciones, umbrales, tablas de grupos, datos de entrada y modelos finales indicados en el inventario. Los modelos sólo se verifican como archivos: no se cargan para inferencia.

Una vez disponibles las entradas:

```bash
python -m pip install -r 07_reproducibilidad/requirements_auditoria.txt
python 07_reproducibilidad/scripts/verificar_multietiqueta.py \
  --root . --external-root /ruta/a/artefactos \
  --output verificaciones_nuevas
```

`--output` debe ser una carpeta nueva o vacía. El auditor no descarga archivos y se detiene con un mensaje concreto si falta una entrada o no coincide su huella. No basta con clonar el repositorio y descargar el corpus para repetir el análisis de predicciones históricas.

Las [verificaciones L1/L2 publicadas](../02_auditoria/particiones_y_multietiqueta/verificacion_20261010) registran cálculos derivados. Sus particiones NPZ están identificadas como reconstrucciones de las reglas y semillas preservadas. En L2 se comprobaron índices, orden, etiquetas, soportes y seis intersecciones de huellas iguales a cero. En L1, separar índices no acredita ausencia de peticiones repetidas entre bloques.

## 5. Identidad de una nueva corrida

Una ejecución nueva debe registrar su commit, lanzador y Python, versiones instaladas, hashes de entrada, transformaciones, semillas, particiones, configuración, identificador de job y salidas. Usar un directorio de resultados propio y conservar los estados de reanudación que correspondan al mismo experimento.

La evidencia del entorno capturada el 03/08/2026 y las verificaciones derivadas de octubre tienen fechas y alcances distintos. Los registros históricos de Slurm y el código experimental mantienen su identidad; los cambios de documentación y catálogos se registran en Git. Consultar el [alcance de auditoría](../02_auditoria/integridad_y_procedencia/ALCANCE_DE_AUDITORIA.md) para interpretar qué se comprobó y qué requiere evidencia adicional.
