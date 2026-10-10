# Tesis: detección y clasificación de ataques en tráfico HTTP

Archivo organizado del trabajo **Detección y clasificación de ataques en tráfico HTTP mediante enfoques binario, multiclase y multietiqueta**. La estructura sigue el libro `08282026v4.pdf` y la presentación `cambiosAndres.pptx` aportados por el autor. La auditoría, la evolución experimental y la procedencia de los resultados son partes centrales del repositorio.

## Por dónde empezar

| Carpeta | Contenido y propósito |
| --- | --- |
| [01_documentacion](01_documentacion/README.md) | Libro, presentación, catálogos de referencias y antecedentes documentales. |
| [02_auditoria](02_auditoria/README.md) | Duplicados y conflictos, particiones, evidencia Slurm, relación entre código y resultados, hashes y decisiones de limpieza. |
| [03_datasets](03_datasets/README.md) | Cuatro corpus, alias, universos, taxonomías CAPEC y esquemas ordenados de variables. |
| [04_experimentos](04_experimentos/README.md) | Una carpeta por etapa B1–B2, M1–M8 y L1–L2; variantes, antecedentes y extensión de 73 variables identificados aparte. |
| [05_codigo](05_codigo/README.md) | Base binaria histórica y scripts/lanzadores de las demás etapas, con sus nombres y contenido originales. |
| [06_resultados_consolidados](06_resultados_consolidados/README.md) | Catálogo de corridas y métricas extraídas de los artefactos, conservando campo, unidad y procedencia. |
| [07_reproducibilidad](07_reproducibilidad/README.md) | Verificación de integridad, comprobación de resultados y catálogo de archivos externos. |
| [90_artefactos_pesados](90_artefactos_pesados/README.md) | Datos, modelos y predicciones que se conservan en Drive y se excluyen de Git. |

## Cómo se refleja la contribución de auditoría

La [guía de auditoría](02_auditoria/README.md) relaciona cada afirmación con el libro, la presentación y los archivos que la sostienen. Distingue las repeticiones de eventos completos, las coincidencias bajo la huella de quince campos HTTP, los conflictos de etiquetas y la separación efectiva de los bloques de L2. Incluye también la reconstrucción del historial de Slurm y las diferencias entre un nombre de script compatible y una identidad de código demostrada por hash.

El [inventario](02_auditoria/integridad_y_procedencia/inventario_archivos.csv) conserva **fuente, ruta original, ruta organizada, tamaño, SHA-256, corrida, corpus y decisión de conservación**. Una copia con distinto contenido se trata como variante, aunque su nombre coincida. Los descartes y las fusiones exactas tienen registros separados. La documentación de esta organización está fechada el **10 de octubre de 2026**; no sustituye las fechas históricas de ejecución.

Las tablas y particiones identificadas como `verificacion_20261010` fueron reconstruidas durante la revisión. Las fuentes históricas conservan sus bytes. No se ejecutaron entrenamientos ni se cargaron modelos serializados durante la organización.

## Corridas y límites que deben acompañar a sus cifras

El [historial experimental](04_experimentos/README.md) explica qué cambió en cada etapa. **B1/B2, las etapas multiclase y L1 mantienen el carácter exploratorio descrito por la tesis.** Hubo consultas a prueba durante el desarrollo y cambios de atributos o taxonomías. L2 usa grupos de peticiones y bloques separados de entrenamiento, tuning, calibración y prueba; su resultado no equivale a una validación temporal o a transferencia entre corpus.

Los [README de L1](04_experimentos/multietiqueta/L1_fixed30/README.md) y [L2](04_experimentos/multietiqueta/L2_request90/README.md) presentan las métricas recalculadas desde predicciones y sus denominadores. El antecedente GPU job2625 se conserva separado del principal L1/job3151. La extensión de 73 atributos/job3361 queda en `04_experimentos/extensiones/EXP_73_atributos`, porque el libro y la presentación documentan hasta M8.

Las metas por clase o etiqueta se conservan junto a los promedios globales. En L2, el recall de NORMAL es 33.925/34.270 (98,9933%); CAPEC-153 y CAPEC-272 quedan por debajo de F1 0,85. La [auditoría](02_auditoria/README.md) explica su alcance sin modificar los resultados originales.

## Uso como repositorio de GitHub

La copia preparada para Git contiene documentación, código, configuraciones, métricas y evidencia liviana. Se adopta un umbral de organización de **20 MiB por archivo**; los modelos serializados y la bibliografía de consulta también se mantienen fuera del repositorio. Este umbral es una decisión de este archivo, no un límite oficial de GitHub.

`.gitignore` excluye los datos y modelos de `90_artefactos_pesados`, los entornos y las cachés. Conserva el README de esa carpeta como índice de los artefactos externos. `.gitattributes` evita conversiones automáticas de saltos de línea para que los hashes originales sigan siendo verificables. El [catálogo externo](07_reproducibilidad/artefactos_externos.csv) permite recuperar los datos y modelos desde su ubicación en Drive. La [guía de reproducibilidad](07_reproducibilidad/README.md) explica cómo comprobar los archivos y qué se puede repetir con la evidencia conservada.

Cada sección de la carpeta puede reutilizarse por separado, pero la raíz completa conserva los enlaces relativos entre auditoría, código y corridas. El inventario y los manifiestos deben acompañar cualquier subconjunto publicado. La organización no publica automáticamente el contenido en GitHub.

<!-- cierre_documental_20261010:inicio -->
## Acta y verificación final

El [acta de organización y auditoría](02_auditoria/integridad_y_procedencia/ACTA_DE_ORGANIZACION_20261010.md) reúne el alcance de la revisión, las decisiones de conservación, los límites de las comprobaciones y la disposición final de las fuentes.

La [verificación final de la entrega](07_reproducibilidad/verificacion_drive_20261010.json) registra la integridad de los archivos locales y el cotejo de identidades, estructura y tamaños en Drive. Distingue esas comprobaciones de una comparación de hashes remotos.
<!-- cierre_documental_20261010:fin -->
