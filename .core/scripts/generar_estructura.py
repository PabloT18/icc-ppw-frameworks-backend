#!/usr/bin/env python3
"""
Script para generar estructura de carpetas de estudiantes por framework backend.
Frameworks: Spring Boot y NestJS
Autor: Pablo Torres
"""

import os
import json
from pathlib import Path
from typing import List, Tuple

# Directorio base del proyecto (asumiendo que el script está en .core/scripts/)
BASE_DIR = Path(__file__).parent.parent.parent

# Plantilla de .gitignore para proyectos backend
GITIGNORE_TEMPLATE = """# Dependencias Node.js (NestJS)
node_modules/
package-lock.json

# Dependencias Java (Spring Boot)
target/
.gradle/
build/
*.jar
*.war
*.ear
*.class

# Archivos de compilación
dist/
out/
.next/

# Archivos de entorno
.env
.env.local
.env.*.local
application-*.properties
application-*.yml

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Base de datos local
*.db
*.sqlite
*.sqlite3

# Sistema operativo
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~
.classpath
.project
.settings/
*.iml

# Cache
.cache/
.temp/
.mvn/
"""


def crear_carpeta_estudiante(framework: str, apellido1: str, apellido2: str) -> None:
    """
    Crea una carpeta para un estudiante en el framework especificado dentro de p67/.
    
    Args:
        framework: Nombre del framework (spring-boot, nest)
        apellido1: Primer apellido del estudiante
        apellido2: Segundo apellido del estudiante
    """
    # Convertir a minúsculas y crear nombre de carpeta
    nombre_carpeta = f"{apellido1.lower()}_{apellido2.lower()}"
    
    # Ruta completa de la carpeta (dentro de p67/)
    ruta_framework = BASE_DIR / framework / "p67"
    ruta_carpeta = ruta_framework / nombre_carpeta
    
    # Verificar que el framework/p67 existe
    if not ruta_framework.exists():
        print(f"⚠️  Advertencia: La carpeta '{framework}/p67' no existe. Creándola...")
        ruta_framework.mkdir(parents=True, exist_ok=True)
    
    # Crear la carpeta del estudiante
    if ruta_carpeta.exists():
        print(f"ℹ️  La carpeta '{nombre_carpeta}' ya existe en '{framework}/p67'")
    else:
        ruta_carpeta.mkdir(parents=True, exist_ok=True)
        print(f"✅ Creada carpeta: {framework}/p67/{nombre_carpeta}")
    
    # Crear carpeta assets
    ruta_assets = ruta_carpeta / "assets"
    if not ruta_assets.exists():
        ruta_assets.mkdir(parents=True, exist_ok=True)
        print(f"   📁 Creada carpeta assets en {framework}/p67/{nombre_carpeta}")
        
        # Crear README.md en la carpeta assets
        assets_readme = ruta_assets / "README.md"
        framework_name = "Spring Boot" if framework == "spring-boot" else "NestJS"
        assets_readme_content = f"""# Assets - {apellido1.title()} {apellido2.title()}

Esta carpeta contiene todos los recursos para la documentación del framework **{framework_name}**.

## 📁 Organización Sugerida

```
assets/
├── images/              # Capturas de pantalla
│   ├── configuracion/   # Capturas del proceso de configuración
│   ├── api/             # Capturas de endpoints y Postman
│   ├── swagger/         # Capturas de documentación Swagger
│   └── database/        # Diagramas de base de datos
├── codigo/              # Archivos de código de ejemplo
└── diagramas/           # Diagramas de arquitectura
```

## 📸 Nomenclatura de Imágenes

- Usar nombres descriptivos: `01-configuracion-inicial.png`
- Incluir el tema: `03-api-rest-postman.png`
- Incluir número de práctica: `05-auth-jwt-p05.png`
- Formato preferido: PNG para capturas, JPG para fotos

## 💡 Consejos

- Mantener las imágenes organizadas por tema
- Usar tamaños razonables (máximo 2MB por imagen)
- Referenciar las imágenes en los archivos .md usando rutas relativas
- Incluir capturas de código, Postman, y resultados de API

## 🔗 Cómo Referenciar en Markdown

```markdown
![Descripción](assets/images/configuracion/setup-inicial.png)
```
"""
        with open(assets_readme, 'w', encoding='utf-8') as f:
            f.write(assets_readme_content)
        print(f"   📝 Creado README.md en assets")
    else:
        print(f"   ℹ️  Carpeta assets ya existe en {framework}/p67/{nombre_carpeta}")
    
    # Crear .gitignore dentro de la carpeta
    ruta_gitignore = ruta_carpeta / ".gitignore"
    if not ruta_gitignore.exists():
        with open(ruta_gitignore, 'w', encoding='utf-8') as f:
            f.write(GITIGNORE_TEMPLATE)
        print(f"   📄 Creado .gitignore en {framework}/p67/{nombre_carpeta}")
    else:
        print(f"   ℹ️  .gitignore ya existe en {framework}/p67/{nombre_carpeta}")


def procesar_lista_estudiantes(estudiantes: List[List[str]]) -> None:
    """
    Procesa una lista de estudiantes y crea sus carpetas correspondientes.
    Cada estudiante tendrá carpeta en Spring Boot Y NestJS.
    
    Args:
        estudiantes: Lista de listas [apellido1, apellido2]
    """
    print("\n🚀 Iniciando generación de estructura de carpetas...\n")
    
    for estudiante in estudiantes:
        if len(estudiante) < 2:
            print(f"⚠️  Entrada inválida (se esperan al menos 2 elementos): {estudiante}")
            continue
        
        apellido1, apellido2 = estudiante[0], estudiante[1]
        
        # Crear carpeta en Spring Boot para todos los estudiantes
        crear_carpeta_estudiante("spring-boot", apellido1, apellido2)
        
        # Crear carpeta en NestJS para todos los estudiantes
        crear_carpeta_estudiante("nest", apellido1, apellido2)
    
    print("\n✨ Proceso completado!\n")


def cargar_desde_json(ruta_json: str) -> List[List[str]]:
    """
    Carga la lista de estudiantes desde un archivo JSON.
    
    Args:
        ruta_json: Ruta al archivo JSON
        
    Returns:
        Lista de estudiantes
    """
    with open(ruta_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('estudiantes', [])


def generar_tabla_estudiantes(estudiantes: List[List[str]]) -> str:
    """
    Genera una tabla en Markdown con enlaces a las carpetas de estudiantes
    
    Args:
        estudiantes: Lista de estudiantes [apellido1, apellido2]
        
    Returns:
        String con la tabla en formato Markdown
    """
    # Organizar estudiantes por nombre (para evitar duplicados)
    estudiantes_dict = {}
    
    for estudiante in estudiantes:
        if len(estudiante) < 2:
            continue
        apellido1, apellido2 = estudiante[0], estudiante[1]
        nombre_completo = f"{apellido1.title()} - {apellido2.title()}"
        nombre_carpeta = f"{apellido1.lower()}_{apellido2.lower()}"
        
        if nombre_completo not in estudiantes_dict:
            estudiantes_dict[nombre_completo] = {
                'nombre_carpeta': nombre_carpeta
            }
    
    # Generar tabla
    tabla = "## 👥 Estudiantes y Proyectos Backend\n\n"
    tabla += "| Estudiante | Spring Boot | NestJS | Estado |\n"
    tabla += "|------------|-------------|--------|--------|\n"
    
    for nombre_completo, info in sorted(estudiantes_dict.items()):
        nombre_carpeta = info['nombre_carpeta']
        
        # Enlaces a carpetas
        enlace_spring = f"[Spring Boot](spring-boot/p67/{nombre_carpeta}/)"
        enlace_nest = f"[NestJS](nest/p67/{nombre_carpeta}/)"
        
        # Verificar si las carpetas existen para mostrar estado
        ruta_spring = BASE_DIR / "spring-boot" / "p67" / nombre_carpeta
        ruta_nest = BASE_DIR / "nest" / "p67" / nombre_carpeta
        
        if ruta_spring.exists() and ruta_nest.exists():
            estado = "✅ Completo"
        elif ruta_spring.exists() or ruta_nest.exists():
            estado = "⚠️ Parcial"
        else:
            estado = "❌ Pendiente"
        
        tabla += f"| {nombre_completo} | {enlace_spring} | {enlace_nest} | {estado} |\n"
    
    # Agregar información adicional
    tabla += f"\n### 📊 Estadísticas\n\n"
    tabla += f"- **Total de estudiantes:** {len(estudiantes_dict)}\n"
    tabla += f"- **Total de proyectos:** {len(estudiantes_dict) * 2} (Spring Boot + NestJS)\n"
    
    tabla += f"\n---\n"
    tabla += f"*Tabla generada automáticamente el {os.popen('date').read().strip()}*\n"
    
    return tabla


def guardar_tabla_readme(tabla_md: str) -> None:
    """
    Guarda la tabla en un archivo README o la agrega al existente
    
    Args:
        tabla_md: Contenido de la tabla en Markdown
    """
    readme_path = BASE_DIR / "ESTUDIANTES.md"
    
    # Crear contenido completo del archivo
    contenido_completo = f"""# 📚 Índice de Estudiantes - PRW-P67 Frameworks Backend

Este archivo contiene el índice de todos los estudiantes y enlaces directos a sus carpetas de trabajo en **Spring Boot** y **NestJS**.

{tabla_md}

## 📋 Instrucciones para Estudiantes

1. **Haz clic en "Spring Boot"** para acceder a tu carpeta de Spring Boot
2. **Haz clic en "NestJS"** para acceder a tu carpeta de NestJS
3. **Verifica que tu estado sea "✅ Completo"** - si no, ejecuta el script de generación
4. **Todos los estudiantes** deben trabajar en ambos frameworks

## 🔧 Para Generar/Actualizar esta Tabla

```bash
python3 .core/scripts/generar_estructura.py
```

## 📁 Estructura Esperada por Estudiante

Cada estudiante debe tener:

```
spring-boot/p67/apellido1_apellido2/
├── assets/
│   └── images/
│       ├── configuracion/
│       ├── api/
│       └── swagger/
├── 01_configuracion.md
├── 02_api_rest.md
├── 03_base_datos.md
└── .gitignore

nest/p67/apellido1_apellido2/
├── assets/
│   └── images/
│       ├── configuracion/
│       ├── api/
│       └── swagger/
├── 01_configuracion.md
├── 02_modulos_controladores.md
├── 03_base_datos.md
└── .gitignore
```

## 🎯 Temas de Documentación

Los temas se documentan según lo indicado en [`/docs`](../../docs/):

| Archivo | Descripción |
|---------|-------------|
| `01_configuracion.md` | Instalación y configuración inicial del framework |
| `02_api_rest.md` | Implementación de API REST y controladores |
| `03_base_datos.md` | Conexión y configuración de base de datos |

---

*Este archivo es generado automáticamente. No editarlo manualmente.*
"""
    
    # Escribir el archivo
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(contenido_completo)
    
    print(f"📋 Tabla de estudiantes guardada en: ESTUDIANTES.md")
    print(f"🔗 Contiene enlaces a {len([line for line in tabla_md.split('\n') if '|' in line and '---' not in line]) - 1} estudiantes")


def main():
    """Función principal del script."""
    print("=" * 60)
    print("  GENERADOR DE ESTRUCTURA DE CARPETAS PARA ESTUDIANTES")
    print("=" * 60)
    
    # Buscar archivo de configuración
    config_file = BASE_DIR / '.core' / 'scripts' / 'estudiantes.json'
    
    if config_file.exists():
        print(f"\n📂 Cargando configuración desde: {config_file.name}\n")
        estudiantes = cargar_desde_json(config_file)
    else:
        print("\n⚠️  No se encontró archivo 'estudiantes.json'")
        print("   Usando datos de ejemplo...\n")
        # Datos de ejemplo
        estudiantes = [
            ["torres", "garcia"],
            ["gonzalez", "marca"],
        ]
    
    # Procesar estudiantes
    procesar_lista_estudiantes(estudiantes)
    
    # Generar y guardar tabla de estudiantes
    print("\n📋 Generando tabla de estudiantes...")
    tabla_md = generar_tabla_estudiantes(estudiantes)
    guardar_tabla_readme(tabla_md)
    
    # Resumen
    print("\n📊 Resumen:")
    print(f"   Total de carpetas procesadas: {len(estudiantes)}")
    print(f"   Ubicación: {BASE_DIR}")
    print(f"   Tabla guardada en: ESTUDIANTES.md")
    print()


if __name__ == "__main__":
    main()
