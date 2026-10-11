# Auditoría portable de L1/L2

El script publicado es `07_reproducibilidad/scripts/verificar_multietiqueta.py`. Recalcula resultados a partir de artefactos experimentales identificados por el inventario. Las entradas que no están publicadas deben estar disponibles en el almacenamiento de la corrida antes de ejecutar la auditoría.

## Uso

Desde la raíz del repositorio:

```bash
python 07_reproducibilidad/scripts/verificar_multietiqueta.py \
  --root . \
  --output ./verificaciones_nuevas
```

`--output` debe ser una carpeta nueva o vacía, para conservar los resultados de verificaciones anteriores. Si la ruta es relativa, se interpreta respecto del directorio desde el que se ejecuta el comando. El script deja allí JSON, CSV y NPZ derivados, incluidos los nombres `particiones_reconstruidas` y la lista de fuentes utilizadas con sus hashes.

Cuando el repositorio documental y los archivos pesados están separados:

```bash
python 07_reproducibilidad/scripts/verificar_multietiqueta.py \
  --root . \
  --external-root /ruta/a/artefactos \
  --output ./verificaciones_nuevas
```

`--external-root` conserva las rutas relativas del inventario y se puede repetir. No descarga archivos: los originales referidos por el inventario deben estar disponibles localmente. `--inventory` permite indicar otra ubicación del inventario JSON; una ruta relativa se interpreta respecto de `--root`.

## Resolución e integridad

El inventario predeterminado es `02_auditoria/integridad_y_procedencia/inventario_archivos.json`, esquema con lista `entries`. Los artefactos L1/L2 se buscan por `source_code=S06`, `run_id` y nombre original; el CSV raw compartido por `source_code=S11` y nombre. La ubicación física sale de `organized_path`/`logical_path`. Para copias consolidadas, se aceptan alias del inventario con el mismo SHA-256. Las referencias de colección y las rutas históricas del clúster documentan la evidencia; la resolución usa rutas relativas del inventario.

Antes de utilizar una fuente se comparan su tamaño y SHA-256 con el inventario. Las ubicaciones resueltas, el hash esperado y el observado quedan en `fuentes_resueltas_y_verificadas.json`. Si un archivo no está disponible o cambió, el programa explica qué entrada lo requiere y termina con código 2.

## Requisitos reales

- Python **3.11 o posterior** para las versiones incluidas en requisitos: los metadatos instalados de NumPy 2.3.5 y scikit-learn 1.8.0 declaran `Requires-Python >=3.11`. El entorno de la auditoría completa anterior usa **Python 3.12.14**.
- NumPy, pandas y scikit-learn. La auditoría completa anterior corrió con **NumPy 2.3.5**, **pandas 2.2.3** y **scikit-learn 1.8.0**; se incluye un archivo de requisitos con esas versiones.
- Los CSV de predicciones L1/L2, latencias, configuraciones y métricas; el CSV procesado L2 y sus tablas de grupos/tuning; el CSV raw `data_capec_multilabel.csv`; y los dos modelos finales para verificar bytes, hash y tamaño.
- Espacio para las salidas derivadas y memoria para las columnas de etiquetas/identidad de los conjuntos de auditoría. No se midió el pico de memoria del auditor portable, por lo que no se fija una cifra mínima no comprobada.

No necesita GPU, XGBoost, joblib, pyarrow ni fastparquet. Los modelos no se deserializan y L1 obtiene las doce columnas CAPEC directamente del CSV raw en bloques de 100.000 filas, conservando su orden; no necesita un NPY temporal ni decodifica el Parquet L1.

## Alcance de la comprobación

Recalcula las métricas desde las predicciones ya guardadas; reconstruye las particiones y verifica su correspondencia con los índices, orden, identidad, etiquetas y soportes preservados. En L2 calcula las seis intersecciones de huellas y concilia los grupos procesados con el catálogo de duplicados. No reentrena, no ejecuta extractores experimentales, no vuelve a calcular todas las huellas raw ni OR por todos sus miembros y no reconstruye el porcentaje histórico de solapamiento L1.

Conserva la lectura de scores con `float_precision="round_trip"` y la comparación en `float32` que reproduce los umbrales originales. Distingue filas L1 de grupos L2. Las metas de rendimiento —como NORMAL ≥ 99%— se informan como métricas; incumplir una meta no significa que haya fallado la verificación de integridad o correspondencia.

Código de salida: **0** si las comprobaciones efectuadas coinciden, **1** si hay discrepancias de resultados, **2** si faltan entradas, archivos o dependencias, o hay errores de formato/integridad. Si una ejecución falla después de comenzar, puede haber salidas parciales; el resumen final existe únicamente cuando se completó el recorrido de ambas corridas.

## Validación de esta adaptación

La adaptación publicada se comprueba mediante sintaxis, ayuda y resolución de entradas. **No se repitió el análisis completo de los CSV** durante la revisión de esta documentación. Los cálculos principales son los ya verificados en el auditor anterior, con rutas resueltas mediante inventario y lectura raw incorporada para quitar la dependencia del NPY temporal.
