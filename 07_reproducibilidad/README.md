# Reproducibilidad y verificación

## 1. Verificar el archivo conservado

Desde la raíz del repositorio:

```bash
python 07_reproducibilidad/scripts/verificar_integridad.py --root .
```

La comprobación usa el catálogo de archivos originales y sus SHA-256. En la copia Git se omiten los artefactos externos; el informe los cuenta de forma separada. Con el espejo pesado disponible se puede usar `--include-external` para verificarlos también. El programa devuelve un error ante un archivo faltante requerido o un hash distinto.

`inventario_archivos.csv/json` registra todas las ocurrencias originales. `catalogo_archivos.json` registra una fila por archivo físico conservado. `archivos_descartados.csv` y `duplicados_fusionados.csv` explican las decisiones de limpieza. Los manifiestos originales de Slurm siguen dentro de su captura; el análisis registra su única diferencia explicada por un cierre de log añadido después de calcular el hash.

## 2. Restaurar datos y modelos externos

Descargue `90_artefactos_pesados` desde la carpeta de Drive y colóquela junto a las carpetas 01–07. El [catálogo de artefactos externos](artefactos_externos.csv) contiene las rutas, tamaños, hashes, identificadores y enlaces individuales de los 229 archivos conservados en Drive. Su estructura reproduce las rutas lógicas de los datasets y corridas, de modo que ningún modelo o procesado pierda su asociación experimental.

Se conservan los estados de reanudación L1/L2 porque la ejecución principal de L1 reutilizó artefactos previos y el tuning L2 utiliza estimadores intermedios junto a sus archivos de progreso. La ubicación externa reduce el tamaño de Git y mantiene la evidencia disponible.

## 3. Repetir la comprobación de resultados multietiqueta

```bash
python -m pip install -r 07_reproducibilidad/requirements_auditoria.txt
python 07_reproducibilidad/scripts/verificar_multietiqueta.py --root . --output verificaciones_locales
```

El auditor usa CSV guardados, etiquetas, índices y umbrales. Resuelve las rutas con el inventario; no carga modelos ni ejecuta los entrenadores. Produce resultados derivados en la carpeta elegida. La verificación realizada durante la organización está en `02_auditoria/particiones_y_multietiqueta/verificacion_20261010`.

Las particiones NPZ allí incluidas fueron reconstruidas con las reglas y semillas preservadas. Están identificadas como reconstrucciones de esta revisión, no como manifiestos históricos completos de particiones encontrados. Para L2 se verificaron índices, orden, etiquetas, soportes y las seis intersecciones de huellas. Para L1, separar índices no demuestra ausencia de contenido repetido entre bloques.

## 4. Alcance de una nueva ejecución de entrenamiento

El archivo conserva scripts, lanzadores, configuraciones, salidas y evidencia de entorno. Las rutas históricas se mantienen literalmente y requieren adaptación al equipo de destino. Los paquetes capturados en agosto de 2026 no certifican el entorno exacto de cada trabajo anterior; las copias del código tampoco equivalen siempre a un commit histórico del job.

La organización verifica integridad y coherencia de resultados existentes. Una ejecución nueva debe identificarse con otra carpeta, fecha, código y hashes de entradas, semillas, particiones, entorno, modelo y salida. No se debe sobrescribir una corrida histórica para presentar una reproducción como si fuera el archivo original.

## 5. GitHub

El umbral local de 20 MiB, los modelos serializados y la bibliografía de consulta determinan el espejo externo. GitHub advierte sobre archivos de más de 50 MiB y bloquea los superiores a 100 MiB en Git ordinario. Documentación oficial consultada el 10/10/2026: [archivos grandes](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github), [límites de repositorios](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

El paquete preparado conserva el README del espejo externo; los datos, modelos y ZIP originales ya representados por el inventario permanecen fuera del paquete Git. `.gitignore` conserva estas exclusiones. El contenido se entrega organizado para revisión y uso por el autor.

<!-- cierre_documental_20261010:inicio -->
## 6. Acta y verificación final de la entrega

El [acta de organización y auditoría](../02_auditoria/integridad_y_procedencia/ACTA_DE_ORGANIZACION_20261010.md) describe el archivo entregado, las decisiones de conservación y el alcance de la revisión. La [verificación final](verificacion_drive_20261010.json) reúne los registros de cierre y la disposición real de los contenedores fuente.

Los SHA-256 documentados corresponden a los archivos locales conservados. En Drive se cotejan identificadores, nombres, tipos, carpetas de destino y tamaños; el servicio no expuso un SHA-256 remoto y no se atribuye a este cotejo una comparación de hashes del servidor.

El manifiesto final excluye su propio contenido para evitar una referencia circular. Su carga y su tamaño se verifican por separado.
<!-- cierre_documental_20261010:fin -->
