
# Guías de Commits – PRW-P67 Frameworks Backend

# COMMIT Lunes 15
## MENSAJE DEL COMMIT DEL PUSH A SU RAMA 

### feat(spring-boot): 02_estructura_proyecto (nest): 02_estructura_proyecto - Lunes 15/12









___
___
___
___
___

**Repositorio académico basado en documentación, prácticas y material teórico.**

Este archivo define convenciones para escribir mensajes de commit **claros, consistentes y adecuados al tipo de repositorio**, cuyo objetivo principal es:

* Documentar conceptos en `/docs`
* Registrar el avance de prácticas en Markdown
* Gestionar assets (capturas, diagramas)
* Mantener scripts de automatización para carpetas de estudiantes
* Mantener orden y trazabilidad en los avances

---

# 1. **Estructura General del Mensaje de Commit**

```
<tipo>(<alcance>): <descripción breve>

[explicación opcional]
```

Ejemplo:

```
feat(docs): agregar sección 03_api_rest_conceptos
```

---

# 2. **Tipos de Commit Permitidos en ESTE proyecto**

| Tipo        | Cuándo usarlo                                                         | Ejemplo adaptado a tu repositorio                         |
| ----------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| `feat`      | Agregar un archivo nuevo o una sección importante                     | `feat(docs): crear 07_conexion_bd.md`                     |
| `update`    | Cuando se modifica un archivo ya existente                            | `update(docs): mejorar ejemplos en 03_api_rest_conceptos` |
| `fix`       | Correcciones menores, errores tipográficos, enlaces rotos             | `fix(docs): corregir enlace a 05_controladores_servicios` |
| `docs`      | Cambios pequeños de documentación general (README, índices)           | `docs: actualizar tabla de contenidos en README.md`       |
| `assets`    | Cuando se añaden o modifican imágenes, diagramas, capturas o recursos | `assets(spring-boot): agregar capturas de instalación`    |
| `structure` | Cambios en la organización del repositorio (carpetas, rutas)          | `structure: reorganizar carpetas de estudiantes`          |
| `scripts`   | Añadir o actualizar scripts automáticos                               | `scripts: mejorar generador de carpetas p67`              |
| `init`      | Crear nuevas carpetas para estudiantes o nueva práctica               | `init(nest): añadir carpeta p67/torres_garcia`            |
| `config`    | Ajustes del repositorio (gitignore, configuración interna)            | `config: agregar reglas para ignorar imágenes locales`    |

---

# 3. **Alcances Permitidos**

Como el proyecto contiene solo **Markdown + assets + scripts**, los alcances se adaptan:

| Alcance       | Uso                                                     |
| ------------- | ------------------------------------------------------- |
| `docs`        | Cambios en el módulo teórico `/docs`                    |
| `spring-boot` | Avances en prácticas documentadas en `/spring-boot/...` |
| `nest`        | Avances en prácticas documentadas en `/nest/...`        |
| `core`        | Cambios en `.core/` (si existe)                         |
| `assets`      | Archivos dentro de cualquier carpeta `/assets/`         |
| `scripts`     | Generadores de carpetas u otros scripts internos        |
| `readme`      | Cambios en el README principal                          |
| `repo`        | Cambios estructurales globales                          |

---

# 4. **Reglas Especiales para cada framework**

Cada tema teórico se encuentra en:

```
/spring-boot/p#/01_conceptos_backend.md
/nest/p#/02_arquitectura_backend.md
...
```

### **Cuando agregas un tema nuevo:**

```
feat(nest): agregar archivo 04_estructura_servidor.md
```

### **Cuando amplías un tema existente:**

```
update(nest): extender explicación de MVC en 02_arquitectura_backend
```

### **Cuando haces correcciones menores en teoría:**

```
fix(nest): corregir diagrama en 01_conceptos_backend
```

---

# 5. **Reglas para Commits de Estudiantes (Spring Boot y NestJS)**

Los estudiantes NO programan APIs aquí; documentan conceptos aplicados.

Cada archivo se llama `01_configuracion.md`, `02_practica.md`, etc.

### **Cuando crean la carpeta personal y archivo de práctica:**

```
init(spring-boot): crear carpeta p67/perez_torres con 01_configuracion.md
```

### **Cuando agregan contenido nuevo significativo:**

```
feat(spring-boot): documentación de instalación de Spring Boot en 01_configuracion.md
```

### **Cuando mejoran o reestructuran el archivo existente:**

```
update(spring-boot): añadir explicación del árbol del proyecto en 01_configuracion.md
```

### **Cuando agregan capturas en assets:**

```
assets(spring-boot): agregar capturas de instalación para perez_torres
```

---

# 6. **Reglas para Scripts Automáticos**

Si se modifica o crea un script de generación de carpetas:

```
scripts: agregar generador de estructura p67 para spring-boot y nest
```

Si se mejora:

```
scripts: optimizar validación de nombres de estudiantes
```

---


# 7. **Buenas Prácticas**

### ✔ Hacer

* Commits atómicos
* Mensajes en imperativo
* Explicar el “qué” y “por qué”
* Mantener orden en assets
* Mantener consistencia en nombres `01_configuracion.md`, `02_...`

### ✘ Evitar

* “update files”, “misc changes”, “arreglos varios”
* Commits enormes sin relación
* Cambiar archivos de otro estudiante
* Subir imágenes pesadas sin optimizar

---

# 8. **Plantillas listas para copiar**

### **Nuevo tema teórico**

```
feat(sprin): agregar <numero>_<titulo>.md
```

### **Modificar un tema**

```
update(docs): mejorar <título> en <archivo>
```

### **Nueva práctica en Spring Boot**

```
feat(spring-boot): documentación de <tema> en <archivo>.md
```

### **Agregar imágenes**

```
assets(<framework>): agregar capturas para <estudiante>
```

### **Correcciones pequeñas**

```
fix(<alcance>): corregir formato en <archivo>
```

---

# 10. **Cómo se verán los commits reales de tus estudiantes**

Ejemplo realista:

```
init(spring-boot): crear carpeta p67/ortiz_taco con 01_configuracion.md
feat(spring-boot): agregar instalación de Java y Spring Boot en 01_configuracion
assets(spring-boot): subir capturas de instalación para ortiz_taco
update(spring-boot): añadir explicación del árbol del proyecto
```

Ejemplo en Nest:

```
feat(nest): documentación inicial en 01_configuracion.md para perez_torres
assets(nest): agregar capturas de instalación de Nest CLI
```

Ejemplo en `/docs`:

```
update(docs): ampliar ejemplos de arquitectura en 02_arquitectura_backend
```

