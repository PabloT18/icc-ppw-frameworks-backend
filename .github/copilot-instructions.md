# GitHub Copilot – Instrucciones para Mensajes de Commit
**Proyecto académico: PRW-P67 Frameworks Backend**

Estas reglas indican cómo GitHub Copilot debe generar mensajes de commit en este repositorio.  
Los commits deben ser consistentes, claros y alineados con la estructura académica del proyecto, basado en documentación y prácticas backend.

---

## 1. Formato general del commit

El mensaje principal debe seguir esta estructura:

```
<tipo>(<alcance>): <descripción breve>

[detalles opcionales]
```

Ejemplo:

```
update(docs): mejorar explicación de API REST en 03_api_rest_conceptos
```

---

## 2. Tipos permitidos

Copilot solo debe usar los siguientes tipos de commit:

- feat → cuando se agrega un archivo nuevo o una sección nueva  
- update → cuando se amplía, mejora o reestructura contenido existente  
- fix → correcciones menores (ortografía, formato, enlaces rotos)  
- docs → documentación general (README, índices, descripciones meta)  
- assets → agregar o actualizar imágenes, capturas o diagramas  
- scripts → creación o mejora de scripts internos  
- init → creación de nuevas carpetas o estructura base para estudiantes  
- config → cambios en configuración del repositorio  
- structure → reorganización de carpetas o estructura interna  

Copilot no debe usar tipos distintos a estos.

---

## 3. Alcances permitidos

El commit debe especificar el área afectada usando uno de estos alcances:

- docs → contenido teórico dentro de `/docs`  
- spring-boot → documentación dentro de `/spring-boot/p67/...`  
- nest → documentación dentro de `/nest/p67/...`  
- assets → modificaciones dentro de carpetas `/assets/`  
- scripts → archivos dentro de `/scripts` o herramientas internas  
- readme → cambios en `README.md`  
- repo → ajustes generales de configuración o estructura  

Ejemplo:

```
assets(spring-boot): agregar capturas de instalación
```

---

## 4. Reglas especiales según el contenido modificado

### Para `/docs`

- Archivo nuevo → feat(docs)  
- Ampliación de contenido → update(docs)  
- Corrección menor → fix(docs)  

Ejemplos:

```
feat(docs): crear 10_documentacion_openapi.md
update(docs): ampliar sección MVC en 02_arquitectura_backend
fix(docs): corregir tabla en 01_conceptos_backend
```


### Para `/spring-boot/p67/a_docente` y `/nest/p67/a_docente`

- Archivo nuevo → feat(spring-boot) o feat(nest)  
- Ampliación de contenido → update(spring-boot) o update(nest)  
- Corrección menor → fix(spring-boot) o fix(nest)
- Creación de carpeta de estudiante → init(spring-boot) o init(nest)

Ejemplos:

```
feat(spring-boot): crear 10_documentacion_openapi.md
update(spring-boot): ampliar sección MVC en 02_arquitectura_backend
fix(spring-boot): corregir tabla en 01_conceptos_backend
```

---

### Para carpetas de estudiantes

Rutas: `/spring-boot/p67/*` y `/nest/p67/*`

Este proyecto documenta prácticas; no se escriben APIs ni código backend real.

- Crear carpeta de estudiante → init(<framework>)  
- Agregar contenido nuevo → feat(<framework>)  
- Mejorar explicaciones o agregar capturas → update(<framework>)  
- Corrección menor → fix(<framework>)  

Ejemplo:

```
feat(spring-boot): documentar instalación en 01_configuracion.md
```

---

### Para assets

Formato:

```
assets(<framework>): <descripción>
```

Ejemplo:

```
assets(nest): añadir capturas de instalación para perez_torres
```

---

### Para scripts internos

Formato:

```
scripts: <descripción>
```

Ejemplo:

```
scripts: mejorar generador de carpetas p67
scripts: ejecutar validación de nombres de estudiantes
```

---

## 5. Reglas obligatorias que Copilot debe respetar

- No generar commits genéricos como “update files” o “fix stuff”.  
- Siempre incluir tipo y alcance.  
- La descripción breve debe estar en modo imperativo.  
- Ajustar el mensaje al archivo realmente modificado.  
- La primera línea debe ser breve.  
- Detalles opcionales solo si aportan claridad.

---

## 6. Ejemplos válidos para Copilot

```
init(spring-boot): crear carpeta p67/ortiz_taco con 01_configuracion.md
feat(nest): documentación inicial en 01_configuracion.md para perez_torres
update(spring-boot): añadir explicación del árbol del proyecto en 01_configuracion.md
assets(spring-boot): subir capturas de instalación
fix(docs): corregir enlaces rotos en tabla de contenidos
update(docs): ampliar ejemplos de arquitectura en 02_arquitectura_backend
```

---

## 7. Resumen para Copilot

Cuando generes un mensaje de commit:

1. Identifica qué archivos cambiaron.  
2. Selecciona el alcance correspondiente: `docs`, `spring-boot`, `nest`, `assets`, `scripts`, `readme`, `repo`.  
3. Selecciona un tipo válido: `feat`, `update`, `fix`, `docs`, `assets`, `init`, `scripts`, `config`, `structure`.  
4. Escribe un mensaje claro y breve en imperativo.  
5. Usa el formato:

```
<tipo>(<alcance>): <descripción>
<tipo>(<framework>): <descripción>

```
