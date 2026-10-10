# Acta de organización y auditoría del archivo de tesis

**Trabajo:** Detección y clasificación de ataques en tráfico HTTP mediante enfoques binario, multiclase y multietiqueta.  
**Fecha de organización:** 10 de octubre de 2026.  
**Carpeta intervenida:** [metricasTesis](https://drive.google.com/drive/folders/1MJnJrRTM7yHJCx_W4D05iQkKT18ZbGIo).

## 1. Resultado de la organización

Se inspeccionaron y descomprimieron los **13 ZIP** que contenía la carpeta, se incorporó la planilla independiente y se usaron como guía el libro `08282026v4.pdf` y la presentación de 71 diapositivas aportados por el autor. La estructura se aplicó en la carpeta original de Drive. El archivo resultante permite entrar por documentación, auditoría, dataset, corrida, código o resultado.

La revisión registró **1.972 ocurrencias de archivos fuente**: 1.969 miembros de ZIP, la planilla independiente y los dos documentos aportados. Quedaron **1.798 archivos originales físicos**: se excluyeron 166 archivos según criterios documentados y se consolidaron ocho ocurrencias idénticas. Los archivos retenidos mantienen sus bytes y su SHA-256. Las explicaciones, tablas e índices nuevos se identifican como productos de esta organización.

La entrega completa contiene **1906 archivos**, incluidos **108 documentos y productos derivados de organización**. De ellos, **1677 archivos** forman el paquete preparado para Git; los **229 artefactos externos** suman **4.681.494.653 bytes** y permanecen en Drive con enlaces individuales, tamaños y hashes. El paquete conserva el README del directorio externo para que esa parte del archivo siga siendo localizable.

Los trece ZIP originales, cuyo contenido ya quedó clasificado y verificado, se enviaron a la papelera de Drive. Sus identificadores, nombres, tamaños y hashes permanecen en el inventario de fuentes. La papelera no se vació. El Excel independiente se movió a su carpeta temática conservando el identificador original.

**Evidencia del alcance:** [inventario de archivos](https://drive.google.com/file/d/16HQRKoMWOOQNcG85Y1xpI1fYOyTnG0Id/view?usp=drivesdk), [fuentes originales](https://drive.google.com/file/d/1aoL5dq8asPdbdJgx2b-X5Gt9H6pFYCxL/view?usp=drivesdk), [catálogo externo con enlaces Drive](https://drive.google.com/file/d/1WfPNljPf6k-LRB-QQD1shFunXOBvq8OQ/view?usp=drivesdk) y el manifiesto final `07_reproducibilidad/verificacion_drive_20261010.json`.

## 2. Estructura y navegación

| Carpeta | Contenido y propósito |
| --- | --- |
| [01_documentacion](https://drive.google.com/drive/folders/12LXyWCuckR-QpKvMaokzEEHk4-vaKhzG) | Libro, presentación y antecedentes; referencias bibliográficas identificadas por separado. |
| [02_auditoria](https://drive.google.com/drive/folders/1fOIGHyxfIz0jv1NALTDmsC5kMvBiGNtd) | Duplicados y conflictos, particiones, evolución experimental, Slurm, hashes, procedencia y decisiones de limpieza. |
| [03_datasets](https://drive.google.com/drive/folders/1VwMCk9thGZi8dLCZb-7hbiT-8Kjmh2aK) | CSIC2010, TorpEda, SRBH2020/Harvard y DS-Augmented-v2; diccionarios, taxonomías CAPEC, análisis y representaciones. |
| [04_experimentos](https://drive.google.com/drive/folders/1CJzlFDiHMYd1n7rQrkwudlg_U8-Ajw--) | Carpetas por etapa B1–B2, M1–M8 y L1–L2, con antecedentes, variantes y extensión posterior identificados. |
| [05_codigo](https://drive.google.com/drive/folders/1namfc8q9Lty5KZss0cFrCfDw9TfjPvA8) | Código y lanzadores originales. La base binaria histórica conserva su estructura de proyecto. |
| [06_resultados_consolidados](https://drive.google.com/drive/folders/1V5Yh6kU4vVPT_d_Kq7gKHDJ1_19UcE_M) | Catálogo de corridas y métricas con fuente, campo y unidad de medida. |
| [07_reproducibilidad](https://drive.google.com/drive/folders/11Ny_2zd4K3bU3hgu5N1S8xZp0C-pTii3) | Comprobación de integridad, auditor de resultados, requisitos y catálogo enlazado de archivos externos. |
| [90_artefactos_pesados](https://drive.google.com/drive/folders/1Fvw7nl9jddjrnivyKqayYMrntOZyAG0I) | Datos, modelos, predicciones y documentos de consulta que se conservan en Drive fuera del paquete Git. |

Cada corrida dispone de `README.md` y `corrida.json`. Esos documentos indican el papel de la etapa, los corpus, los archivos conservados, las fuentes y el vínculo con el libro o la presentación. Las rutas históricas y nombres originales se mantienen dentro de `artefactos` para conservar su contexto. El índice de cada corrida permite encontrar los archivos externos sin confundirlos con una ejecución distinta.

Las matrices procesadas y los modelos pesados siguen una estructura equivalente dentro de `90_artefactos_pesados`. Cada dataset tiene una entrada propia con disponibilidad de fuentes, análisis, taxonomías, representaciones y corridas relacionadas. Los nombres Harvard, SR-BH y SRBH2020 se relacionan explícitamente; el alias `egipcios` se identifica con DS-Augmented-v2 cuando corresponde a los artefactos inspeccionados.

La raíz completa funciona como un repositorio coherente porque conserva los enlaces entre secciones. Se pueden reutilizar secciones por separado, acompañándolas de su inventario y de los archivos a los que remiten. La organización no creó ni publicó un repositorio externo de GitHub.

## 3. Catálogo de etapas, variantes y antecedentes

| Identificador | Etapa conservada | Ubicación |
| --- | --- | --- |
| B1 | Ablación binaria RF en CSIC | [Abrir carpeta](https://drive.google.com/drive/folders/1VBl40xm5B50Ct0Xlc_tyMFAFnMqP16xc) |
| B2 | Comparación binaria por corpus | [Abrir carpeta](https://drive.google.com/drive/folders/1HjM5SsWjDwmyiAoxpD8LC82A54yr3dkx) |
| M1 | Modelo base de 30 atributos; Harvard 9 familias y TorpEda 10 clases | [Abrir carpeta](https://drive.google.com/drive/folders/1cmCfCYGoKkhadC6-cLF06tEFsKisI8ln) |
| M2 | Top-14 de combinaciones CAPEC y 30 atributos | [Abrir carpeta](https://drive.google.com/drive/folders/1_fhgHMzuNaC-df74zdUd8NvlJX6YtrD7) |
| M3 | Expansión a 84 atributos | [Abrir carpeta](https://drive.google.com/drive/folders/1V0B5tlQGwqA4EPCcoq4hEchpQGW5M_3l) |
| M4 | Poda a 58 atributos y Top-14 | [Abrir carpeta](https://drive.google.com/drive/folders/1CAqtyAUFL2Q0wfchaBA8XDFMrjPyDPxe) |
| M5 | Taxonomía operativa de 11 clases | [Abrir carpeta](https://drive.google.com/drive/folders/1ljXeyyAUc-4glqnGiRUlflOhcZQWIZfm) |
| M6 | 10 clases con Request Manipulation | [Abrir carpeta](https://drive.google.com/drive/folders/1suWR0jAHUciNd6NpIwjtkefZnY2BupXX) |
| M7 | Tres corpus y 58 atributos | [Abrir carpeta](https://drive.google.com/drive/folders/1fdeEfXvgKFa45O8UbGPKYuCMjYOThAFW) |
| M8 | Tres corpus y 72 atributos | [Abrir carpeta](https://drive.google.com/drive/folders/1IHFqbLvPRBOES5Bwr5f79qiyCPhQ4XUo) |
| L1 | Multietiqueta fixed30; resultado principal job 3151 | [Abrir carpeta](https://drive.google.com/drive/folders/1SMs3OlFX8U1Evpt9PzMpxU9pJF7Nx_xW) |
| L1_2625 | Variante previa GPU de L1; job 2625 | [Abrir carpeta](https://drive.google.com/drive/folders/1XXCeDLBGO0AOLvXmwliAckkNgUqoSfcO) |
| L2 | Multietiqueta request90 por grupos; job 3315 | [Abrir carpeta](https://drive.google.com/drive/folders/1_IerUGyDR6Sv7YgdWU44yAr7KxWyW97Y) |
| EXP73 | Extensión posterior de 73 atributos; job 3361 | [Abrir carpeta](https://drive.google.com/drive/folders/1OcBa2xyrAgaXiPNhdhGNhdoOgqnu0yxk) |
| OC | Antecedentes one-class en CSIC | [Abrir carpeta](https://drive.google.com/drive/folders/1gcW-CGFHEnHtcW0geME9G_RHdDYmbz_J) |
| PRE_MC | Selección multiclase preliminar resultsOptimo | [Abrir carpeta](https://drive.google.com/drive/folders/1tr5Vxg9HVNODy2S6zW01MsTdpM8djm0I) |
| PRE_XGB | Selección multietiqueta preliminar; ganador local XGBoost sin ponderación | [Abrir carpeta](https://drive.google.com/drive/folders/1M-TDERhshDfZBX9cpsPGmC9k1AS_i3kb) |
| PRE_LGBM | Selección multietiqueta LightGBM sin ponderación | [Abrir carpeta](https://drive.google.com/drive/folders/1A2EkM21pO_ki09G0S6BHpgyDT8riy5BW) |
| PRE_LGBM_W | Selección multietiqueta LightGBM con ponderaciones; ganador local cuberoot | [Abrir carpeta](https://drive.google.com/drive/folders/1Jcmqvp83MmvW3u5niAnu4WWdssi8escQ) |

M1–M8 reflejan la evolución multiclase documentada por el libro y la presentación. La ampliación de 73 variables y job3361 se conserva como **EXP73**, una extensión posterior; no se presenta como una etapa M9 de la tesis. Los informes PDF 01 y 02 se relacionan con el mismo tramo inicial M1, por lo que la numeración de los archivos documentales no se convirtió automáticamente en numeración de corridas.

En multietiqueta se distinguen el **L1 principal, job3151**, su **variante previa job2625** y **L2, job3315**. El nombre heredado de un archivo que contiene `gpu` no acredita por sí solo el hardware utilizado. Las configuraciones y logs se conservan junto a cada resultado. También se distinguen la selección preliminar y los resultados finales, incluso cuando sus archivos tienen nombres parecidos.

**Evidencia:** [catálogo de corridas](https://drive.google.com/file/d/1aEuoxq6A5PM0lyIL_Qd-Z1fh7cuXKLuW/view?usp=drivesdk) y los README de las corridas enlazados en la tabla.

## 4. Cómo queda reflejada la contribución de auditoría

### 4.1. Procedencia y decisiones de conservación

El inventario registra fuente, ruta original, destino organizado, tamaño, SHA-256, corrida, corpus y decisión. No se fusionaron archivos por semejanza de nombre. Una copia con contenido diferente se conserva como variante si aporta contexto; las fusiones registradas se basan en identidad de bytes. El historial Slurm conserva su captura original y una revisión derivada que explica discrepancias sin cambiar los registros históricos.

La documentación relaciona las contribuciones declaradas en el libro —esquema común, representaciones HTTP, auditoría de datos, historia experimental y evaluación de las tres formulaciones— con los artefactos que permiten revisarlas. Las referencias PDF usan la página física; las referencias a página impresa y a diapositiva se identifican por separado.

### 4.2. Duplicados, conflictos y particiones

La auditoría distingue **eventos completos de 38 columnas** de **peticiones agrupadas por la huella de quince campos HTTP**. Estas definiciones producen universos diferentes y se documentan junto a cada recuento. El bruto Harvard conservado contiene 907.815 eventos. L2 excluye dos peticiones vacías y consolida los 907.813 eventos restantes en 542.990 grupos.

La revisión de S10 recontó las columnas de auditoría de su Excel: 27.624 grupos repetidos con los vacíos incluidos, 392.448 eventos dentro de esos grupos y 364.824 excedentes. Se identifican 288 grupos con variación de etiquetas y 284 con presencia normal/ataque. La unión OR usada en L2 preserva las etiquetas observadas en un grupo; no decide mediante revisión humana cuál era la etiqueta correcta.

Se reconstruyeron las cuatro particiones L2 mediante las reglas y semillas conservadas: 347.513 grupos de entrenamiento, 43.439 de selección, 43.440 de calibración y 108.598 de prueba. Coinciden índices y orden de prueba, etiquetas, huellas y soportes; las seis intersecciones entre particiones dan cero bajo esa identidad. Los NPZ están identificados como **reconstrucciones de esta revisión**, porque no se encontraron listas históricas completas de los cuatro bloques.

Para L1 se verificaron índices, orden y soportes. El porcentaje histórico de coincidencias por huella entre prueba y desarrollo, 42,3908 %, se conserva con la atribución al libro; no se presenta como un nuevo recálculo completo del bruto. Separar índices de fila no demuestra independencia del contenido.

**Evidencia:** [revisión de datasets](https://drive.google.com/file/d/1OglQ6iivNgyC4ghOwj-YDnqTkyVoKD36/view?usp=drivesdk), [verificación S10](https://drive.google.com/file/d/1x_a0Cp9a4yqoqohYdwttyYKfqG0rW6j9/view?usp=drivesdk), [verificación L1](https://drive.google.com/file/d/1TCvWcwHDrERj5ShxFf6I2vLpwgBAVsI-/view?usp=drivesdk) y [verificación L2](https://drive.google.com/file/d/188Tp8Jyfp7rn2UsfErOIxH4my518-IU6/view?usp=drivesdk).

### 4.3. Coherencia de resultados y unidades

Las métricas de L1 y L2 se recalcularon desde las predicciones guardadas, sus scores y umbrales, sin reentrenar ni cargar modelos serializados. Para M4/M5 se recalcularon accuracy, balanced accuracy, F1 macro y MCC sobre cuatro CSV de predicciones: las dieciséis comparaciones coinciden. En otras etapas se contrastaron configuraciones, métricas y logs; esa lectura no se declara como repetición de todos los experimentos.

L2 obtiene F1 micro 0,976042922, F1 macro 0,939399314 y exactitud de conjunto 0,969198328. El detalle por etiqueta permanece visible: CAPEC-153 alcanza F1 0,80863039 y CAPEC-272 0,58035034, por debajo de la meta 0,85. NORMAL reconoce 33.925 de 34.270 casos, es decir 98,9932886 %; faltan tres aciertos para cumplir estrictamente el 99 %. El redondeo a 99,0 % no se presenta como cumplimiento exacto de la meta.

Los benchmarks separan modelo, preparación y predicción, procesamiento por lotes, ejecución Slurm y trabajo reanudado. En L2, las mediciones corresponden a **grupos de peticiones**, aunque campos históricos se llamen `req_s`. Los tiempos heredados de checkpoints L1 no se suman como si todo el entrenamiento hubiera ocurrido dentro del job3151. En M8, las curvas de Harvard y DS-Augmented-v2 utilizan muestras de 50.000 eventos, mientras las tablas globales evalúan sus conjuntos de prueba completos. En TorpEda, la curva utiliza los 14.827 eventos del test completo y comparte el universo de la tabla global.

Las etapas históricas B1/B2, multiclase y L1 mantienen el alcance exploratorio explicado por la tesis: hubo consultas a prueba y evolución de atributos o taxonomías. L2 verifica separación por grupos bajo su regla documentada, pero no equivale a evaluación temporal, transferencia entre corpus ni rendimiento de un WAF desplegado en producción.

**Evidencia:** [guía de auditoría](https://drive.google.com/file/d/1rQpFfblOfIdN1EAK9BXKdvJLJIn7UW93/view?usp=drivesdk), [métricas M4/M5 recalculadas](https://drive.google.com/file/d/1yZMIYYEVqrtQhvtj80njByDWdWk6Uab2/view?usp=drivesdk) y [revisión multietiqueta](https://drive.google.com/file/d/1jljyd3TG5cVkfLKMND42q_njhFCCOlz_/view?usp=drivesdk).

### 4.4. Historia Slurm y código

La captura S01 cubre 133 jobs seleccionados y contiene logs de 26. La tabla histórica de recuperación batch dice `recuperado`, pero los 133 archivos `.err` asociados informan que la recuperación del script falló. Se conservaron tanto la tabla original como la corrección de su interpretación. El commit HEAD y el entorno capturado en agosto describen esa captura, sin acreditar automáticamente el código o entorno exactos de cada ejecución anterior.

Se verificaron los manifiestos originales disponibles: 167 de 167 hashes del proyecto y 389 de 390 del manifiesto global. La excepción global se explica por 187 bytes de cierre añadidos a un log: el hash histórico coincide con su prefijo anterior. El archivo fuente se conserva completo con esa anotación.

Las vinculaciones de configuración, job y script indican su grado de evidencia. Un basename compatible, una copia de código posterior y un hash anclado en el log son formas distintas de acreditación. La revisión de S13 añadió configuraciones y logs directos para M1/job2534, M2/job2657 y M3/job2687.

**Evidencia:** [revisión Slurm](https://drive.google.com/file/d/1LZsFkMYfvgj4gfBIvM7hkwnyVwJoUu9W/view?usp=drivesdk) y [evidencia de M1–M3 en S13](https://drive.google.com/file/d/1_YhCMmLY2bnE2d7MOHVOZHLhCY9x0XRL/view?usp=drivesdk).

## 5. Limpieza aplicada

| Decisión | Cantidad | Criterio |
| --- | ---: | --- |
| Archivos excluidos | 166 | 16 auxiliares de compilación LaTeX, un `.pyc`, un lock vacío regenerable y 148 pesos de candidatos no seleccionados o incompletos de S13. |
| Ocurrencias idénticas consolidadas | 8 | Igualdad de contenido y SHA-256, preservando todas las procedencias y una copia física. |
| Contenedores ZIP retirados de la raíz | 13 | Contenido descomprimido, clasificado y verificado; traslado recuperable a la papelera. |

Los 166 descartes suman **5.851.709.924 bytes descomprimidos**. Las ocho ocurrencias fusionadas suman **264.731.327 bytes**. Estos valores corresponden a los miembros fuente y no son una medición del espacio liberado en Drive. Los trece ZIP son contenedores comprimidos; tampoco se suman esas magnitudes como si fueran archivos físicos disjuntos.

Se conservaron los modelos finales, los candidatos ganadores documentados, las configuraciones, métricas, predicciones, logs y estados necesarios para explicar las selecciones. En particular, permanecen los **51 checkpoints L1/L2 de S06** —26 y 25 respectivamente— con sus estados de progreso, además de la variante histórica job2625 conservada en S13. No se eliminaron por parecer archivos intermedios: sostienen la reanudación y la trazabilidad.

**Evidencia:** [criterios de limpieza](https://drive.google.com/file/d/1BIzmImkkSOE3rVibLiy3YBr2cflaggQ_/view?usp=drivesdk), [archivos descartados](https://drive.google.com/file/d/1ZKgRJsR0aGLxwXxTk5nUwFYcypv6BT8C/view?usp=drivesdk), [fusiones exactas](https://drive.google.com/file/d/1zQYNWgdVhvbUejOKwrurns2329yjIaI6/view?usp=drivesdk) y [selección y limpieza S13](https://drive.google.com/file/d/1gun7CP8j3SbPqmNbXeJNO-QXbxxPIilD/view?usp=drivesdk). Los registros permiten reconstruir qué ocurrió con cada ocurrencia original.

## 6. Comprobaciones y alcance técnico

Los trece ZIP se leyeron completos y sus miembros se verificaron mediante CRC y SHA-256. La última revisión local volvió a calcular las huellas de los **1.798 originales retenidos**, que suman **4.904.750.553 bytes**: todos coinciden. La fecha y el alcance de esa revisión se incorporan al manifiesto de cierre.

En Drive se cotejaron identificadores, nombres, tipos, carpetas de destino y tamaños exactos con el inventario. Los listados de las carpetas permiten detectar archivos faltantes, nombres duplicados o elementos inesperados. Los cuatro archivos originales vacíos se preservaron y verificaron como archivos de cero bytes. La planilla independiente se trasladó conservando su identificador original.

El SHA-256 documentado es el calculado sobre el archivo local conservado. El servicio no expuso un SHA-256 remoto; el cotejo remoto acredita la estructura, identidad y tamaño, y no se describe como comparación de hashes del servidor. El manifiesto final excluye su propio contenido para evitar una referencia circular y registra esa exclusión expresamente; su carga se verifica por separado.

El paquete Git se construye desde una lista explícita de archivos. Se comprueba que ningún archivo previsto quede excluido por `.gitignore`; luego se vuelve a leer cada entrada del ZIP para contrastar tamaño y SHA-256. No se incorporan copias temporales, directorios de sincronización ni archivos ajenos a esa lista.

## 7. Qué se puede reproducir y qué falta

La guía incluye un verificador de integridad y un auditor de resultados multietiqueta que usa las predicciones, etiquetas y umbrales preservados. El catálogo externo permite recuperar las entradas pesadas por archivo o descargando la carpeta `90_artefactos_pesados` junto a las secciones 01–07.

Se encontró el bruto Harvard/SRBH2020. **No se encontraron los datos crudos de CSIC, TorpEda ni DS-Augmented-v2** en ninguno de los trece paquetes inspeccionados. Se conservan sus matrices procesadas y evidencia disponible, con esta diferencia anotada en cada README de dataset.

Tampoco aparecieron dos basenames exactos referenciados por lanzadores preliminares: `train_waf_multiclass_fixed30_resultsOptimo_sbatch_v10.py` y `train_waf_multilabel_DEFINITIVO_multifamily_resume_resultsOptimo_fixed30.py`. Se preservaron las referencias y la ausencia comprobada. Un entrenador con nombre similar no se presenta como sustituto exacto.

Una nueva ejecución requiere adaptar las rutas históricas, disponer de las entradas correspondientes y registrar código, dependencias, semillas y particiones. Debe guardarse como una corrida nueva, sin sobrescribir las históricas. La organización acredita integridad y coherencia de la evidencia disponible; no promete reconstruir byte por byte todos los entrenamientos originales.

**Guía de uso y comandos:** [reproducibilidad](https://drive.google.com/file/d/1CLNCVfylI3HxBdpaZzqF2jNg_6cmnwqM/view?usp=drivesdk). El archivo `requirements_auditoria.txt` describe las dependencias del auditor entregado; las capturas históricas de entorno se mantienen como evidencia separada.
