# Scripts de Utilidad - PRW-P67 Frameworks Backend

Esta carpeta contiene scripts de utilidad para la gestión del proyecto de frameworks backend.

## 📦 Contenido

- `generar_estructura.py` - Script para generar automáticamente la estructura de carpetas de estudiantes
- `estudiantes.json` - Archivo de configuración con la lista de estudiantes

## 🚀 Uso del Script de Generación de Estructura

### Descripción

El script `generar_estructura.py` genera automáticamente carpetas para estudiantes en los frameworks backend **Spring Boot** y **NestJS** dentro de la carpeta `p67/`, y crea un archivo `.gitignore` apropiado para proyectos backend en cada carpeta.

### Prerequisitos

- Python 3.6 o superior

### Configuración

Edita el archivo `estudiantes.json` con la lista de estudiantes. El formato es:

```json
{
  "estudiantes": [
    ["apellido1", "apellido2"],
    ["apellido1", "apellido2"]
  ]
}
```

**Ejemplo:**

```json
{
  "estudiantes": [
    ["avila", "cabrera"],
    ["calle", "torres"],
    ["fernandez", "chuquipoma"],
    ["gomez", "valarezo"]
  ]
}
```

### Frameworks Backend

Este proyecto trabaja con:

- **`spring-boot`** - Framework Java para aplicaciones enterprise
- **`nest`** - Framework Node.js/TypeScript para aplicaciones escalables

**Importante:** Todos los estudiantes tendrán carpetas en **ambos frameworks** dentro de `p67/`.

### Ejecutar el Script

Desde la raíz del proyecto:

```bash
python3 .core/scripts/generar_estructura.py
```

O desde cualquier ubicación:

```bash
python3 /ruta/completa/.core/scripts/generar_estructura.py
```

### Resultado

El script creará:

```
spring-boot/
└── p67/
    ├── avila_cabrera/
    │   ├── assets/
    │   │   └── README.md
    │   └── .gitignore
    ├── calle_torres/
    │   ├── assets/
    │   │   └── README.md
    │   └── .gitignore
    └── ...

nest/
└── p67/
    ├── avila_cabrera/
    │   ├── assets/
    │   │   └── README.md
    │   └── .gitignore
    ├── calle_torres/
    │   ├── assets/
    │   │   └── README.md
    │   └── .gitignore
    └── ...
```

### Características

- ✅ Crea carpetas con el formato `apellido1_apellido2` dentro de `p67/`
- ✅ Genera carpetas para **Spring Boot** y **NestJS** para cada estudiante
- ✅ Crea automáticamente un `.gitignore` apropiado para proyectos backend
- ✅ Crea carpeta `assets/` con README de organización
- ✅ Verifica si las carpetas ya existen (no las sobrescribe)
- ✅ Crea las carpetas de framework si no existen
- ✅ Mensajes informativos durante la ejecución
- ✅ Genera archivo `ESTUDIANTES.md` con índice de todos los estudiantes

### Contenido del .gitignore

El script incluye automáticamente un `.gitignore` completo para proyectos backend que ignora:

**Para NestJS:**
- `node_modules/` y dependencias Node.js
- Carpetas de build/dist
- Archivos de entorno (.env)

**Para Spring Boot:**
- `target/` y `.gradle/`
- Archivos compilados (*.jar, *.war, *.class)
- Configuraciones específicas de Maven/Gradle

**General:**
- Logs
- Base de datos locales (*.db, *.sqlite)
- Archivos del sistema (.DS_Store)
- Configuraciones de IDEs (.idea/, .vscode/, *.iml)
- Archivos de cache

### Notas

- Los nombres de las carpetas se crean siempre en **minúsculas**
- Todos los estudiantes tienen carpetas en **Spring Boot** y **NestJS**
- Las carpetas se crean dentro de `p67/` para cada framework
- Si una carpeta ya existe, el script lo indica pero no la sobrescribe
- Si un framework no existe, se crea automáticamente
- Se genera automáticamente un archivo `ESTUDIANTES.md` con enlaces a todas las carpetas

## 🔧 Personalización

Puedes modificar:

1. **Plantilla del .gitignore**: Edita la variable `GITIGNORE_TEMPLATE` en `generar_estructura.py`
2. **Formato del nombre de carpeta**: Modifica la función `crear_carpeta_estudiante()`
3. **Lista de estudiantes**: Edita `estudiantes.json`
4. **Contenido del README de assets**: Modifica la variable `assets_readme_content` en la función `crear_carpeta_estudiante()`

## 📝 Ejemplo Completo

```bash
# 1. Editar estudiantes.json con tu lista
# 2. Ejecutar el script
python3 .core/scripts/generar_estructura.py

# Salida esperada:
# ============================================================
#   GENERADOR DE ESTRUCTURA DE CARPETAS PARA ESTUDIANTES
# ============================================================
#
# 📂 Cargando configuración desde: estudiantes.json
#
# 🚀 Iniciando generación de carpetas...
#
# ✅ Creada carpeta: spring-boot/p67/avila_cabrera
#    📁 Creada carpeta assets en spring-boot/p67/avila_cabrera
#    📝 Creado README.md en assets
#    📄 Creado .gitignore en spring-boot/p67/avila_cabrera
# ✅ Creada carpeta: nest/p67/avila_cabrera
#    📁 Creada carpeta assets en nest/p67/avila_cabrera
#    📝 Creado README.md en assets
#    📄 Creado .gitignore en nest/p67/avila_cabrera
# ...
#
# ✨ Proceso completado!
#
# 📋 Generando tabla de estudiantes...
# 📋 Tabla de estudiantes guardada en: ESTUDIANTES.md
# 🔗 Contiene enlaces a 12 estudiantes
#
# 📊 Resumen:
#    Total de carpetas procesadas: 12
#    Ubicación: /ruta/al/proyecto
#    Tabla guardada en: ESTUDIANTES.md
```

## ⚠️ Importante

Este script está diseñado para ser ejecutado desde la raíz del proyecto. Asegúrate de estar en el directorio correcto antes de ejecutarlo.

## 📚 Estructura Generada

Cada estudiante tendrá la siguiente estructura en ambos frameworks:

```
spring-boot/p67/apellido1_apellido2/
├── assets/
│   ├── images/
│   │   ├── configuracion/
│   │   ├── api/
│   │   ├── swagger/
│   │   └── database/
│   └── README.md
├── 01_configuracion.md
├── 02_api_rest.md
└── .gitignore

nest/p67/apellido1_apellido2/
├── assets/
│   ├── images/
│   │   ├── configuracion/
│   │   ├── api/
│   │   ├── swagger/
│   │   └── database/
│   └── README.md
├── 01_configuracion.md
├── 02_modulos_controladores.md
└── .gitignore
```
