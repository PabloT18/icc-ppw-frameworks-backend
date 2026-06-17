# Programación y Plataformas Web

# Frameworks Backend: Despliegue en Producción

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" width="80">
</div>

## Práctica 14: Preparación y Despliegue de APIs en Producción

### Autores

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

---

# **Introducción**

Después de desarrollar, probar y asegurar nuestra API, llega el momento de **desplegarla en producción**. Este documento cubre los conceptos fundamentales, las mejores prácticas y las diferentes estrategias para poner tu aplicación backend en un entorno real.

**Conceptos clave**:
- **Diferencia entre desarrollo y producción**
- **Preparación del código para producción**
- **Opciones de despliegue**: Con y sin Docker
- **Nginx como reverse proxy**
- **Variables de entorno y configuración**
- **Monitoreo y logs**

**Prerequisitos**:
- API backend funcional (Spring Boot o NestJS)
- Conocimientos básicos de Linux
- Entender conceptos de redes y HTTP
- Haber completado prácticas anteriores (1-13)

---

# **1. Desarrollo vs Producción**

## **1.1. Diferencias Fundamentales**

| Aspecto | Desarrollo | Producción |
|---------|-----------|------------|
| **Objetivo** | Facilitar desarrollo y debugging | Rendimiento, seguridad y estabilidad |
| **Base de datos** | SQLite/H2/Local PostgreSQL | PostgreSQL/MySQL en servidor dedicado |
| **Puerto** | 3000, 8080 (directo) | 80/443 (a través de Nginx) |
| **HTTPS** | HTTP (sin cifrar) | HTTPS con certificados SSL |
| **Logs** | Verbose (mucha información) | Solo errores y eventos importantes |
| **Variables de entorno** | `.env` local | Variables de sistema/secretos seguros |
| **Hot reload** | Activado (desarrollo rápido) | Desactivado |
| **Modo debug** | Activado | Desactivado |
| **CORS** | Permisivo (localhost) | Restrictivo (solo dominios permitidos) |
| **Gestión de procesos** | Manual (npm start, mvn) | PM2, systemd, Docker |
| **Errores** | Stack trace completo | Mensajes genéricos (no exponer detalles) |

## **1.2. Checklist Pre-Despliegue**

Antes de desplegar, verifica:

**Seguridad**:
- [ ] Variables sensibles en entorno (no en código)
- [ ] CORS configurado correctamente
- [ ] Helmet/seguridad headers habilitados
- [ ] Rate limiting implementado
- [ ] Autenticación JWT configurada
- [ ] HTTPS configurado

**Base de datos**:
- [ ] Migraciones probadas
- [ ] Backups configurados
- [ ] Pool de conexiones optimizado
- [ ] Índices creados

**Rendimiento**:
- [ ] Compresión habilitada (gzip)
- [ ] Caché configurado
- [ ] Archivos estáticos optimizados
- [ ] Queries optimizadas

**Monitoreo**:
- [ ] Logs configurados
- [ ] Healthcheck endpoint creado
- [ ] Métricas disponibles

---

# **2. Variables de Entorno en Producción**

## **2.1. ¿Por Qué Variables de Entorno?**

**Problema del código hardcodeado**:
```javascript
// MAL: Credenciales en código
const dbConfig = {
  host: 'mi-servidor.com',
  user: 'admin',
  password: 'secret123',  // ← Expuesto en Git
  database: 'produccion'
};
```

**Solución con variables de entorno**:
```javascript
// BIEN: Variables de entorno
const dbConfig = {
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
};
```

## **2.2. Configuración por Entorno**

```bash
# .env.development (desarrollo)
NODE_ENV=development
PORT=3000
DB_HOST=localhost
DB_PORT=5432
LOG_LEVEL=debug
CORS_ORIGIN=http://localhost:4200

# .env.production (producción)
NODE_ENV=production
PORT=3000
DB_HOST=db.miservidor.com
DB_PORT=5432
LOG_LEVEL=error
CORS_ORIGIN=https://miapp.com
```



# **3. Opciones de Despliegue**

## **3.1. Comparación General**


| Opción                              | Complejidad   | Portabilidad | Escalabilidad | Uso recomendado                                |
| ----------------------------------- | ------------- | ------------ | ------------- | ---------------------------------------------- |
| **Servidor Nativo (Linux + Nginx)** | ⭐⭐ Media      | Baja         | ⭐⭐ Media      | Aprendizaje de infraestructura, VPS controlado |
| **Docker Compose**                  | ⭐⭐ Media      | Alta         | ⭐⭐ Media      | Producción simple, entornos consistentes       |
| **Kubernetes**                      | ⭐⭐⭐⭐ Muy alta | Máxima       | ⭐⭐⭐⭐ Muy alta | Producción empresarial                         |
| **PaaS (Heroku, Railway)**          | ⭐ Baja        | Alta         | ⭐⭐⭐ Alta      | Prototipos, MVP, portafolio                    |

---

# **4. Servidor Nativo (Linux + Nginx)**

## **4.1. Arquitectura**

```
Internet
    ↓
 [Nginx :80/443]  ← Reverse proxy, SSL termination
    ↓
 [API Backend :3000]  ← Node.js/Java process
    ↓
 [PostgreSQL :5432]  ← Base de datos
```

## **4.2. Pasos para Desplegar**

### **¿Por Qué Linux?**

**Linux (especialmente Ubuntu/Debian)** es el sistema operativo estándar para servidores de producción por:

- **Estabilidad**: Diseñado para estar corriendo 24/7 sin reiniciar
- **Seguridad**: Menos vulnerable que otros sistemas, actualizaciones constantes
- **Recursos**: Consume menos memoria y CPU que Windows
- **Gratuito**: Sin costos de licencias
- **Comunidad**: Documentación extensa y soporte
- **Compatibilidad**: La mayoría de herramientas backend están optimizadas para Linux

**Ubuntu Server** o **Debian** son las distribuciones más populares para hosting web.

### **Paso 1: Preparar el Servidor (Ubuntu/Debian)**

**Comandos de instalación básicos**:

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias según framework
# Para Node.js:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Para Java (Spring Boot):
sudo apt install -y openjdk-17-jdk

# Instalar PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Instalar Nginx
sudo apt install -y nginx
```

**Explicación de cada instalación**:

1. **Actualizar sistema**: Garantiza que todos los paquetes estén al día con parches de seguridad

2. **Runtime del framework**:
   - **Node.js**: Para aplicaciones NestJS (runtime JavaScript)
   - **Java JDK**: Para aplicaciones Spring Boot (compilador + runtime Java)

3. **PostgreSQL**: Sistema de base de datos relacional robusto para producción

4. **Nginx**: Servidor web que actuará como reverse proxy (explicado en sección 6)

### **Paso 2: Configurar Base de Datos**

**Objetivo**: Crear una base de datos específica para la aplicación con su propio usuario.

**Pasos conceptuales**:
1. **Conectar a PostgreSQL** como administrador
2. **Crear base de datos** dedicada para la API
3. **Crear usuario** con contraseña segura
4. **Otorgar permisos** completos al usuario sobre la base de datos

**Buenas prácticas**:
- Usuario específico por aplicación (no usar `postgres` directamente)
- Contraseñas fuertes (mínimo 16 caracteres, aleatorias)
- Principio de mínimo privilegio (solo permisos necesarios)

> Ver módulos específicos de frameworks para comandos SQL exactos.

### **Paso 3: Desplegar Aplicación**

**Proceso general de despliegue**:

#### **3.1. Obtener el Código**
- **Clonar repositorio** desde Git en directorio del servidor (ej: `/opt/mi-api`)
- Verificar que estés en la rama correcta (main/production)

#### **3.2. Instalar Dependencias**
- **NestJS**: Instalar paquetes npm solo de producción (sin dev dependencies)
- **Spring Boot**: Descargar dependencias Maven/Gradle

#### **3.3. Compilar/Build**
- **NestJS**: Transpilar TypeScript a JavaScript optimizado
- **Spring Boot**: Compilar código Java a archivo JAR ejecutable

#### **3.4. Configurar Variables de Entorno**
- Crear archivo con variables de producción (`.env.production`)
- Incluir: credenciales BD, JWT secret, puertos, URLs
- **NUNCA** versionar este archivo en Git

#### **3.5. Crear Servicio del Sistema (systemd)**

**¿Qué es systemd?**
Gestor de servicios de Linux que:
- Inicia la aplicación automáticamente al arrancar el servidor
- Reinicia la aplicación si se cae
- Gestiona logs del sistema
- Permite control fácil (start/stop/restart)

**Configuración del servicio incluye**:
- **Descripción** del servicio
- **Dependencias** (esperar a que red y BD estén disponibles)
- **Usuario** que ejecuta la aplicación (no root por seguridad)
- **Comando de inicio** (node dist/main.js o java -jar app.jar)
- **Variables de entorno** cargadas desde archivo
- **Política de reinicio** (always restart)

#### **3.6. Activar y Gestionar el Servicio**
- **Recargar systemd** para detectar nuevo servicio
- **Habilitar** inicio automático al arrancar servidor
- **Iniciar** el servicio
- **Verificar estado** y logs

> Los comandos específicos y archivos de configuración están en los módulos de cada framework.

### **Paso 4: Configurar Nginx**

#### **¿Qué es Nginx en este Contexto?**

**Nginx** es un servidor web que actúa como **intermediario** (reverse proxy) entre Internet y tu aplicación backend. En lugar de exponer directamente tu aplicación, Nginx recibe las peticiones y las redirige internamente.

#### **¿Para Qué Sirve Configurarlo?**

**Funciones clave de Nginx en producción**:

1. **Reverse Proxy**:
   - Cliente hace petición a `https://api.midominio.com/products`
   - Nginx recibe en puerto 443 (HTTPS)
   - Nginx redirige internamente a `http://localhost:3000/products`
   - Backend responde a Nginx
   - Nginx devuelve respuesta al cliente

2. **Terminación SSL/HTTPS**:
   - Nginx maneja los certificados SSL
   - Conexión segura (HTTPS) entre cliente y Nginx
   - Conexión interna HTTP simple entre Nginx y backend
   - Backend no necesita preocuparse por SSL

3. **Seguridad**:
   - Oculta el puerto real del backend (3000, 8080)
   - Rate limiting (limitar peticiones por IP)
   - Firewall a nivel de aplicación
   - Bloquear patrones de ataque

4. **Performance**:
   - Compresión gzip de respuestas
   - Caché de contenido estático
   - Servir archivos estáticos sin pasar por backend

#### **Configuración Conceptual**

**Archivos a crear**:
- **Archivo de configuración del sitio**: Define cómo Nginx maneja las peticiones
- **Ubicación**: `/etc/nginx/sites-available/mi-api`

**Elementos clave de la configuración**:

1. **Server blocks**:
   - Uno para puerto 80 (HTTP) → Redirige a HTTPS
   - Uno para puerto 443 (HTTPS) → Maneja peticiones reales

2. **SSL/TLS**:
   - Ruta a certificados (fullchain.pem, privkey.pem)
   - Protocolos seguros (TLS 1.2, 1.3)
   - Ciphers modernos

3. **Proxy pass**:
   - Dirección interna del backend (`http://localhost:3000`)
   - Headers a preservar (IP real del cliente, protocolo HTTPS)
   - Timeouts apropiados

4. **Security headers**:
   - HSTS (forzar HTTPS)
   - X-Frame-Options (prevenir clickjacking)
   - Content Security Policy

5. **Logs**:
   - Access log: Registra todas las peticiones
   - Error log: Solo errores de Nginx

#### **Activación del Sitio**

**Pasos conceptuales**:
1. Crear enlace simbólico de `sites-available` a `sites-enabled`
2. Probar configuración (validar sintaxis)
3. Recargar Nginx para aplicar cambios

**Verificación**:
- Nginx acepta peticiones en puerto 80/443
- Redirige correctamente al backend
- HTTPS funciona correctamente

> Para configuración completa de Nginx específica de tu framework:
> - **NestJS**: `nest/p67/a_dodente/14_despliegue_produccion.md`
> - **Spring Boot**: `spring-boot/p67/a_dodente/14_despliegue_produccion.md`

### **Paso 5: Configurar SSL con Let's Encrypt**

#### **¿Qué es SSL/TLS?**

**SSL/TLS** son protocolos de seguridad que cifran la comunicación entre el navegador del usuario y tu servidor.

- **HTTP** → Datos viajan en texto plano (inseguro)
- **HTTPS** → Datos cifrados (seguro)

**Certificado SSL**:
- Archivo digital que verifica la identidad de tu servidor
- Permite que navegadores confíen en tu sitio
- Necesario para HTTPS (el candado verde 🔒)

#### **¿Qué es Let's Encrypt?**

**Let's Encrypt** es una autoridad certificadora (CA) que proporciona:
- Certificados SSL **gratuitos**
- Válidos por 90 días
- Renovación automática
- Reconocidos por todos los navegadores

**Alternativas comerciales** (de pago):
- DigiCert, Comodo, GoDaddy
- Ventaja: Soporte dedicado, garantías
- Let's Encrypt es suficiente para la mayoría de casos

#### **¿Cómo se Vincula con Nginx?**

**Let's Encrypt necesita comprobar que controlas el dominio**:

```
1. Tú ejecutas Certbot
        ↓
2. Certbot contacta servidores de Let's Encrypt
        ↓
3. Let's Encrypt pide: "Demuestra que controlas api.midominio.com"
        ↓
4. Certbot crea archivo temporal en tu servidor
        ↓
5. Let's Encrypt hace petición HTTP a api.midominio.com/.well-known/...
        ↓
6. Nginx (que ya está configurado) sirve ese archivo
        ↓
7. Let's Encrypt verifica: "Sí, controla el dominio"
        ↓
8. Certbot recibe certificado
        ↓
9. Certbot instala certificado en configuración de Nginx
```

**Por eso el comando usa `--nginx`**:
- Certbot detecta tu configuración de Nginx existente
- Modifica automáticamente los archivos de configuración
- Agrega las rutas a los certificados
- Configura redirección HTTP → HTTPS

#### **Proceso de Configuración**

**Herramienta: Certbot**
- Cliente oficial de Let's Encrypt
- Automatiza obtención e instalación de certificados
- Se integra con Nginx (o Apache)

**Pasos conceptuales**:

1. **Instalar Certbot**:
   - Cliente Let's Encrypt
   - Plugin para Nginx

2. **Obtener certificado**:
   - Certbot se comunica con Let's Encrypt
   - Verifica que controlas el dominio
   - Descarga certificado

3. **Instalar certificado**:
   - Certbot modifica configuración de Nginx
   - Agrega rutas a certificados
   - Configura protocolos SSL seguros

4. **Renovación automática**:
   - Certificados expiran en 90 días
   - Sistema cron automático los renueva
   - Sin intervención manual

#### **Archivos Generados**

**Ubicación**: `/etc/letsencrypt/live/api.midominio.com/`

- **fullchain.pem**: Certificado completo (tu sitio + cadena de confianza)
- **privkey.pem**: Clave privada (mantener secreta)
- **cert.pem**: Solo tu certificado
- **chain.pem**: Cadena de autoridades certificadoras

**Nginx usa**:
- `fullchain.pem` para el certificado
- `privkey.pem` para la clave privada

#### **Renovación Automática**

**Timer de systemd**:
- Servicio que corre automáticamente
- Verifica cada 12 horas si hay que renovar
- Renueva cuando faltan 30 días
- Recarga Nginx automáticamente

**Ventaja**: Una vez configurado, certificados siempre válidos sin intervención.

#### **Verificación**

**Después de configurar**:
- `https://api.midominio.com` funciona
- Candado verde en navegador
- HTTP redirige automáticamente a HTTPS
- Certificado válido por 90 días
- Renovación automática activa

> Para comandos específicos de instalación de tu framework:
> - **NestJS**: `nest/p67/a_dodente/14_despliegue_produccion.md`
> - **Spring Boot**: `spring-boot/p67/a_dodente/14_despliegue_produccion.md`

## **4.3. Gestión de Procesos con PM2 (Alternativa a systemd)**

### **¿Qué es PM2?**

**PM2 (Process Manager 2)** es un gestor de procesos avanzado específico para aplicaciones **Node.js**. Es la alternativa más popular a systemd para aplicaciones JavaScript/TypeScript.

### **¿Para Qué Sirve?**

**Funciones principales**:

1. **Mantener app corriendo**:
   - Inicia aplicación automáticamente al arrancar servidor
   - Reinicia automáticamente si la app se cae
   - Monitoreo de salud de la aplicación

2. **Modo Cluster**:
   - Ejecutar múltiples instancias de tu app
   - Aprovechar todos los núcleos del CPU
   - Load balancing automático entre instancias
   - Ejemplo: 1 servidor con 4 cores → 4 instancias de la app

3. **Logs integrados**:
   - Ver logs en tiempo real
   - Rotación automática de logs
   - Separar logs de error y output normal

4. **Recarga sin downtime**:
   - Actualizar app sin interrumpir el servicio
   - Reinicio gradual de instancias

5. **Monitoreo**:
   - Uso de CPU y memoria
   - Uptime de la aplicación
   - Número de reinici os

### **PM2 vs systemd**

| Característica | systemd | PM2 |
|----------------|---------|-----|
| **Plataforma** | Cualquier aplicación Linux | Específico Node.js |
| **Cluster mode** | No nativo | Sí (fácil) |
| **Logs** | journalctl (complejo) | Integrados (simple) |
| **Monitoreo** | Básico | Dashboard incluido |
| **Recarga sin downtime** | No | Sí |
| **Configuración** | Archivo .service | Archivo ecosystem.config.js |
| **Mejor para** | Aplicaciones Java, multi-lenguaje | Aplicaciones Node.js |

### **Conceptos Clave de PM2**

#### **1. Modo de Ejecución**

**Fork mode** (default):
- Una sola instancia de la aplicación
- Simple, para apps pequeñas

**Cluster mode**:
- Múltiples instancias (workers)
- Load balancing automático
- Aprovechar multi-core
- Recomendado para producción

#### **2. Ecosystem File**

**Archivo de configuración** (`ecosystem.config.js`):
- Define cómo PM2 ejecuta tu app
- Múltiples aplicaciones en un archivo
- Variables de entorno
- Configuración de logs
- Límites de memoria

**Elementos típicos**:
- **name**: Nombre de la aplicación
- **script**: Archivo a ejecutar
- **instances**: Número de instancias (o "max" para usar todos los cores)
- **exec_mode**: "fork" o "cluster"
- **env_production**: Variables para producción
- **error_file/out_file**: Rutas de logs
- **max_memory_restart**: Reiniciar si excede memoria

#### **3. Startup Script**

**Inicio automático al arrancar servidor**:
- PM2 genera script para systemd
- Se ejecuta automáticamente
- Restaura todas las apps guardadas

#### **4. Gestión de Logs**

**Características**:
- Logs separados por tipo (error vs output)
- Rotación automática (evita archivos gigantes)
- Ver logs en tiempo real
- Buscar en logs históricos

### **Casos de Uso**

**Usa PM2 si**:
- Tu aplicación es Node.js/NestJS
- Quieres modo cluster fácilmente
- Necesitas monitoreo simple
- Quieres gestión de logs integrada
- Despliegues frecuentes con zero-downtime

**Usa systemd si**:
- Aplicación Spring Boot (Java)
- Quieres usar herramientas estándar Linux
- Una sola instancia es suficiente
- Integración con otras herramientas systemd

### **Comandos Conceptuales**

**Operaciones principales**:
- **Iniciar** aplicación con configuración
- **Listar** aplicaciones corriendo
- **Ver logs** en tiempo real
- **Reiniciar** aplicación
- **Detener** aplicación
- **Guardar** configuración para startup
- **Monitorear** recursos en tiempo real

### **Ventajas en Producción**

1. **Resiliencia**:
   - App se reinicia automáticamente si falla
   - Múltiples instancias (si una falla, otras siguen)

2. **Performance**:
   - Usar todos los cores del CPU
   - Load balancing incorporado

3. **Mantenimiento**:
   - Actualizar sin downtime
   - Logs fáciles de acceder
   - Monitoreo simple

4. **Productividad**:
   - Comandos simples
   - Dashboard visual (PM2 Plus opcional)
   - Gestión remota posible

### **Flujo de Trabajo Típico**

```
1. Instalar PM2 globalmente en servidor
        ↓
2. Crear archivo ecosystem.config.js
        ↓
3. Iniciar app con PM2
        ↓
4. Verificar que funciona
        ↓
5. Configurar startup automático
        ↓
6. Guardar configuración
        ↓
7. App corre 24/7 con monitoreo
```

> Para configuración completa de PM2 con ejemplos:
> - **NestJS**: `nest/p67/a_dodente/14_despliegue_produccion.md`

**Nota**: PM2 es específico para Node.js. Para Spring Boot, usa systemd (Paso 3.5).

---

# **5. Despliegue Con Docker**

## **5.1. ¿Por Qué Docker?**

**Ventajas**:
- **Portabilidad**: Funciona igual en desarrollo, staging y producción
- **Aislamiento**: Cada contenedor es independiente
- **Versionado**: Imágenes con tags específicos
- **Escalabilidad**: Fácil replicar contenedores
- **Consistencia**: Elimina "en mi máquina funciona"

**Desventajas**:
- Curva de aprendizaje
- Overhead de recursos (mínimo)
- Complejidad adicional para proyectos simples

## **5.2. Arquitectura Con Docker**

```
Internet
    ↓
 [Nginx Container :80/443]  ← Reverse proxy
    ↓
 [API Container :3000]  ← Backend
    ↓
 [PostgreSQL Container :5432]  ← Base de datos
    ↑
 [Docker Network]  ← Comunicación entre contenedores
```

## **5.3. Dockerfile para Backend**

### **¿Qué es un Dockerfile?**

**Dockerfile** es un archivo de texto que contiene instrucciones para construir una **imagen Docker**. Es como una "receta" que define:
- El sistema operativo base
- Las dependencias a instalar
- El código de la aplicación
- Cómo ejecutar la aplicación

### **¿Cómo se Usa?**

**Flujo de trabajo**:
```
Dockerfile → docker build → Imagen Docker → docker run → Contenedor corriendo
```

1. **Escribir** Dockerfile con instrucciones
2. **Construir** imagen: `docker build -t mi-api:1.0 .`
3. **Ejecutar** contenedor: `docker run mi-api:1.0`

### **¿Por Qué se Usa?**

**Ventajas del Dockerfile**:

| Beneficio | Explicación |
|-----------|-------------|
| **Reproducibilidad** | La misma imagen funciona en cualquier máquina |
| **Versionado** | Cada cambio genera nueva versión de imagen |
| **Aislamiento** | Dependencias encapsuladas, no afectan al host |
| **Documentación** | El Dockerfile documenta el entorno de ejecución |
| **CI/CD** | Fácil integrar en pipelines de despliegue automatizado |


### **Elementos Clave de un Dockerfile**

1. **FROM**: Imagen base (ej: `node:20-alpine`, `eclipse-temurin:17`)
2. **WORKDIR**: Directorio de trabajo dentro del contenedor
3. **COPY**: Copiar archivos del host al contenedor
4. **RUN**: Ejecutar comandos (instalar dependencias, compilar)
5. **EXPOSE**: Documentar qué puerto usa la aplicación
6. **CMD/ENTRYPOINT**: Comando para iniciar la aplicación
7. **USER**: Usuario que ejecuta la aplicación (seguridad)

### **Mejores Prácticas**

- Usar imágenes base oficiales y ligeras (`alpine`)
- Multi-stage build para reducir tamaño
- Copiar `package.json` antes del código (aprovechar caché de Docker)
- Ejecutar como usuario no-root
- `.dockerignore` para no copiar archivos innecesarios
- Especificar versiones exactas de imágenes

> Para Dockerfiles completos y optimizados de tu framework específico, consulta:
> - **NestJS**: `nest/p67/a_dodente/14_despliegue_produccion.md`
> - **Spring Boot**: `spring-boot/p67/a_dodente/14_despliegue_produccion.md`


# **6. Nginx: El Reverse Proxy**

## **6.1. ¿Qué es Nginx?**

**Nginx** es un servidor web y reverse proxy de alto rendimiento.

**Funciones en producción**:
- **Reverse Proxy**: Redirige peticiones al backend
- **SSL Termination**: Maneja certificados HTTPS
- **Load Balancing**: Distribuye carga entre instancias
- **Compresión**: Gzip para reducir tamaño de respuestas
- **Caché**: Cachea respuestas estáticas
- **Archivos estáticos**: Sirve assets sin pasar por backend
- **Rate Limiting**: Limita peticiones por IP

## **6.2. ¿Dónde se Usa Nginx?**

**Escenario típico**:
```
Cliente → Nginx (puerto 80/443) → Backend (puerto 3000/8080)
```

**Sin Nginx**:
```http
https://api.midominio.com:3000/api/products  Puerto visible
```

**Con Nginx**:
```http
https://api.midominio.com/api/products  Puerto oculto
```

## **6.3. Configuración de Nginx**

**Archivo completo** (`nginx.conf`):
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Formato de logs
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Compresión Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # Rate limiting (prevenir abuso)
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    # Upstream (backend)
    upstream api_backend {
        least_conn;  # Balanceo por menos conexiones
        server api:3000 max_fails=3 fail_timeout=30s;
        # Para múltiples instancias:
        # server api-1:3000 max_fails=3 fail_timeout=30s;
        # server api-2:3000 max_fails=3 fail_timeout=30s;
    }

    server {
        listen 80;
        server_name api.midominio.com;

        # Redirigir a HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name api.midominio.com;

        # Certificados SSL
        ssl_certificate /etc/nginx/ssl/fullchain.pem;
        ssl_certificate_key /etc/nginx/ssl/privkey.pem;

        # Configuración SSL moderna
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
        ssl_prefer_server_ciphers off;

        # HSTS (HTTP Strict Transport Security)
        add_header Strict-Transport-Security "max-age=63072000" always;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Límite de tamaño de request
        client_max_body_size 10M;

        # API endpoints
        location /api {
            # Rate limiting
            limit_req zone=api_limit burst=20 nodelay;

            # Proxy pass
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            
            # Headers
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Buffering
            proxy_buffering off;
        }

        # Health check (sin rate limit)
        location /health {
            proxy_pass http://api_backend/health;
            access_log off;
        }

        # Servir archivos estáticos directamente (si aplica)
        location /static {
            alias /var/www/static;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## **6.4. Load Balancing con Nginx**

Para **múltiples instancias** del backend:

```nginx
upstream api_backend {
    least_conn;  # Estrategia de balanceo
    
    server api-1:3000 weight=3;  # Más peso = más peticiones
    server api-2:3000 weight=2;
    server api-3:3000 weight=1;
    
    # Health checks
    server api-4:3000 max_fails=3 fail_timeout=30s;
}
```

**Estrategias de balanceo**:
- `round-robin`: Por turnos (default)
- `least_conn`: Al servidor con menos conexiones
- `ip_hash`: Mismo cliente → mismo servidor (sticky sessions)
- `random`: Aleatorio

---

# **7. Mejores Prácticas de Despliegue**

## **7.1. Configuración para Producción**

**Características de una API lista para producción**:

| Característica | Implementación |
|----------------|----------------|
| **Logs estructurados** | JSON logs con niveles (error, warn, info) |
| **Healthcheck endpoint** | `/health` que verifica BD, servicios externos |
| **Graceful shutdown** | Cerrar conexiones antes de apagar |
| **CORS restrictivo** | Solo dominios permitidos |
| **Rate limiting** | Limitar peticiones por IP/usuario |
| **Compression** | Gzip habilitado |
| **Security headers** | Helmet.js o equivalente |
| **Validación de entrada** | DTOs con validación estricta |
| **Manejo de errores** | No exponer stack traces |

## **7.2. Healthcheck Endpoint**

### **¿Qué es un Healthcheck?**

**Healthcheck** (verificación de salud) es un endpoint HTTP que indica si tu aplicación está funcionando correctamente. Es fundamental para:

- **Monitoring**: Sistemas de monitoreo verifican constantemente este endpoint
- **Load Balancers**: Dejan de enviar tráfico a instancias no saludables
- **Container Orchestration**: Docker/Kubernetes reinician contenedores con fallas
- **Alertas**: Notifican al equipo cuando algo va mal

### **Niveles de Health Check**

| Nivel | Qué verifica | Respuesta | Uso |
|-------|--------------|-----------|-----|
| **Básico** | Aplicación responde | 200 OK | Mínimo necesario |
| **Intermedio** | App + Base de datos | 200 OK / 503 Error | Recomendado |
| **Avanzado** | App + BD + Redis + APIs externas | 200 OK / 503 Error / 200 Degraded | Producción robusta |

### **Estados de Salud**

- **200 OK** (`healthy`): Todo funciona correctamente
- **503 Service Unavailable** (`unhealthy`): Servicio no disponible (ej: BD caída)
- **200 OK con status "degraded"**: Funcionando parcialmente (ej: Redis caído pero app sigue)

### **Estructura de Respuesta**

```json
{
  "status": "ok",              // ok | degraded | error
  "timestamp": "2026-01-27T10:30:00Z",
  "uptime": 3600,              // Segundos que lleva corriendo
  "checks": {
    "database": "ok",          // Estado de cada dependencia
    "redis": "ok",
    "externalAPI": "degraded"
  }
}
```

### **Implementación Conceptual**

**Pasos para implementar**:

1. **Crear endpoint** `/health` (sin autenticación)
2. **Verificar aplicación** está corriendo (responde)
3. **Verificar base de datos** puede ejecutar query simple
4. **Verificar servicios externos** (opcional: Redis, APIs)
5. **Retornar estado** con código HTTP apropiado

**Consideraciones**:
- **Rápido**: Debe responder en < 1 segundo
- **Sin autenticación**: Debe ser público
- **Ligero**: No ejecutar operaciones pesadas
- **Sin logs excesivos**: No llenar logs con health checks
- **Información útil**: Incluir qué está fallando
- **No exponer**: Información sensible (contraseñas, IPs internas)

**Ejemplo de uso en Nginx**:
```nginx
location /health {
    proxy_pass http://api_backend/health;
    access_log off;  # No llenar logs con health checks
}
```

> Para implementación específica de tu framework, consulta los módulos correspondientes.

## **7.3. Logs en Producción**

**Estructura de logs**:
```json
{
  "timestamp": "2026-01-27T10:30:00.123Z",
  "level": "error",
  "message": "Database connection failed",
  "context": {
    "userId": 123,
    "endpoint": "/api/products",
    "method": "GET",
    "ip": "192.168.1.100"
  },
  "error": {
    "name": "DatabaseError",
    "message": "Connection timeout",
    "stack": "..."
  }
}
```

**Niveles de log recomendados**:
- **ERROR**: Solo errores críticos que necesitan atención
- **WARN**: Situaciones anormales pero manejables
- **INFO**: Eventos importantes (startup, shutdown)
- **DEBUG**: Solo en desarrollo

**Rotación de logs**:
```bash
# Instalar logrotate
sudo apt install -y logrotate

# Configurar rotación
sudo nano /etc/logrotate.d/mi-api
```

```
/var/log/mi-api/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 www-data www-data
}
```

## **7.4. Monitoreo y Alertas**

**Métricas a monitorear**:
- **Disponibilidad**: Uptime del servicio
- **Latencia**: Tiempo de respuesta promedio
- **Tasa de errores**: % de requests con error 5xx
- **Throughput**: Requests por segundo
- **Uso de recursos**: CPU, memoria, disco

**Herramientas populares**:
- **Prometheus + Grafana**: Métricas y dashboards
- **ELK Stack**: Logs centralizados (Elasticsearch, Logstash, Kibana)
- **Sentry**: Tracking de errores
- **UptimeRobot**: Monitoreo simple de uptime
- **PM2 Plus**: Monitoreo para Node.js

## **7.5. Backups Automáticos**

**Script de backup para PostgreSQL**:
```bash
#!/bin/bash
# backup-db.sh

DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/backups/postgres"
DB_NAME="mi_api_db"

# Crear directorio si no existe
mkdir -p $BACKUP_DIR

# Backup
pg_dump -U api_user -h localhost $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Eliminar backups antiguos (más de 7 días)
find $BACKUP_DIR -type f -name "*.sql.gz" -mtime +7 -delete

echo "Backup completado: backup_$DATE.sql.gz"
```

**Configurar cron para backups diarios**:
```bash
# Editar crontab
crontab -e

# Agregar línea (backup diario a las 2 AM)
0 2 * * * /opt/scripts/backup-db.sh >> /var/log/backup.log 2>&1
```

---

# **8. Estrategias de Despliegue**

## **8.1. CI/CD: Integración y Despliegue Continuo**

### **¿Qué es CI/CD?**

**CI/CD** son prácticas de desarrollo que automatizan el proceso desde que escribes código hasta que llega a producción.

- **CI (Continuous Integration)**: Integración Continua
  - Integrar cambios de código frecuentemente (varias veces al día)
  - Ejecutar tests automáticamente en cada cambio
  - Detectar problemas temprano

- **CD (Continuous Deployment/Delivery)**: Despliegue Continuo
  - **Delivery**: Código siempre listo para desplegar (manual)
  - **Deployment**: Despliegue automático a producción

### **¿Por Qué Usar CI/CD?**

**Problemas sin CI/CD**:
```
Desarrollador → Commit → Esperar días → Deploy manual → Errores descubiertos en producción
```

**Beneficios con CI/CD**:
```
Desarrollador → Commit → Tests automáticos → Build automático → Deploy automático → Producción
                          ↓ (si falla)
                       Notificación inmediata
```

| Beneficio | Explicación |
|-----------|-------------|
| **Velocidad** | De días a minutos para desplegar |
| **Confiabilidad** | Tests automáticos previenen errores |
| **Consistencia** | Mismo proceso cada vez, sin errores humanos |
| **Feedback rápido** | Sabes inmediatamente si algo falló |
| **Rollback fácil** | Volver a versión anterior automáticamente |

### **Pipeline Típico de CI/CD**

**Flujo completo**:

```
1. COMMIT
   Developer hace git push
        ↓
2. CI: BUILD
   - Clonar repositorio
   - Instalar dependencias
   - Compilar código
        ↓
3. CI: TEST
   - Tests unitarios
   - Tests de integración
   - Análisis de código (linting)
   - Escaneo de seguridad
        ↓
4. CI: PACKAGE
   - Crear JAR/build
   - Construir imagen Docker
   - Etiquetar versión
        ↓
5. CD: DEPLOY STAGING
   - Desplegar en entorno de pruebas
   - Tests E2E automáticos
   - Aprobación manual (opcional)
        ↓
6. CD: DEPLOY PRODUCTION
   - Desplegar a producción
   - Smoke tests
   - Monitoreo activo
        ↓
7. MONITORING
   - Verificar métricas
   - Alertas si hay problemas
   - Rollback automático si falla
```

### **Comparación de Enfoques**

| Aspecto | Despliegue Manual | Con Scripts | CI/CD |
|---------|------------------|-------------|-------|
| **Velocidad** | 30-60 min | 10-20 min | 5-10 min |
| **Errores humanos** | Alto | Medio | Muy bajo |
| **Reproducibilidad** | Baja | Media | Alta |
| **Tests automáticos** | No | Opcional | Siempre |
| **Rollback** | Manual, lento | Manual | Automático |
| **Documentación** | Externa | En scripts | En pipeline |
| **Aprendizaje** | Fácil | Medio | Complejo |
| **Mejor para** | Proyectos pequeños | Equipos pequeños | Producción profesional |

### **Herramientas Populares de CI/CD**

| Herramienta | Tipo | Mejor para | Características |
|-------------|------|------------|----------------|
| **GitHub Actions** | Cloud | Proyectos en GitHub | Gratis para repos públicos, integrado |
| **GitLab CI/CD** | Cloud/Self-hosted | Equipos completos | Pipeline visual, Docker registry incluido |
| **Jenkins** | Self-hosted | Empresas grandes | Muy flexible, muchos plugins |
| **CircleCI** | Cloud | Startups | Rápido, fácil configuración |
| **Travis CI** | Cloud | Open source | Gratis para proyectos públicos |

### **Conceptos Clave**

**Pipeline as Code**:
- La configuración del pipeline está en un archivo versionado
- Ejemplos: `.github/workflows/deploy.yml`, `.gitlab-ci.yml`
- Ventaja: Revisar cambios como código normal

**Ambientes/Stages**:
- **Development**: Desarrollo local
- **Staging/QA**: Réplica de producción para pruebas
- **Production**: Ambiente real con usuarios

**Triggers (Disparadores)**:
- Push a rama específica (`main`, `develop`)
- Pull Request
- Tag de versión (`v1.2.3`)
- Programado (cron)
- Manual

**Artifacts**:
- Archivos generados en el pipeline (JAR, Docker images)
- Se guardan para usar en pasos posteriores
- Permiten separar build de deploy

### **Mejores Prácticas**

- **Fast feedback**: Pipeline rápido (< 10 min ideal)
- **Fail fast**: Detectar errores lo antes posible
- **Tests primero**: No desplegar si tests fallan
- **Ambientes idénticos**: Staging = Producción
- **Rollback plan**: Siempre poder volver atrás
- **Monitoreo post-deploy**: Verificar que funcione
- **Notificaciones**: Alertar al equipo de éxitos/fallos
- **Seguridad en secrets**: Usar variables cifradas

### **Cuándo Implementar CI/CD**

**Sí, implementa CI/CD si**:
- Equipo de 2+ desarrolladores
- Despliegas frecuentemente (semanal o más)
- Tienes tests automatizados
- Proyecto a largo plazo

**Puedes esperar si**:
- Proyecto muy pequeño (1 dev, pocas features)
- Prototipo rápido
- No tienes tests aún
- Despliegas muy ocasionalmente

> Los módulos específicos de frameworks incluyen ejemplos de pipelines:
> - **NestJS**: `nest/p67/a_dodente/14_despliegue_produccion.md`
> - **Spring Boot**: `spring-boot/p67/a_dodente/14_despliegue_produccion.md`


# **9. Proveedores de Hosting**

## **9.1. Comparación de Opciones**

| Proveedor | Tipo | Precio | Complejidad | Mejor para |
|-----------|------|--------|-------------|------------|
| **DigitalOcean** | VPS | $5-10/mes | Media | Aplicaciones personalizadas |
| **AWS EC2** | VPS Cloud | Variable | Alta | Escalabilidad empresarial |
| **Heroku** | PaaS | $7-25/mes | Baja | Prototipado rápido |
| **Railway** | PaaS | $5-20/mes | Muy baja | Proyectos estudiantiles |
| **Vercel** | PaaS (serverless) | Gratis-$20/mes | Baja | APIs ligeras, Next.js |
| **Render** | PaaS | $7-25/mes | Baja | Full-stack moderno |
| **Google Cloud Run** | Serverless | Pay-per-use | Media | Microservicios containerizados |

## **9.2. Recomendaciones por Caso de Uso**

**Proyecto académico/portafolio**:
- Railway (gratis hasta $5/mes)
- Render (gratis con limitaciones)
- Vercel (para APIs serverless)

**Startup MVP**:
- Heroku o Railway (rápido setup)
- DigitalOcean App Platform (balance precio/features)

**Producción empresarial**:
- AWS ECS/EKS (escalabilidad máxima)
- Google Cloud Run (serverless, eficiente)
- DigitalOcean + Kubernetes (costo-efectivo)

**Aprendizaje/experimentación**:
- DigitalOcean VPS ($5/mes)
- Oracle Cloud (free tier generoso)
- Google Cloud (free tier + $300 créditos)



# **10. Troubleshooting Común**

## **10.1. Problemas Frecuentes**

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| **502 Bad Gateway** | Backend no responde | Verificar que proceso esté corriendo |
| **500 Internal Error** | Error en código | Revisar logs del backend |
| **Connection refused** | Puerto bloqueado | Verificar firewall y configuración |
| **SSL certificate error** | Certificado inválido/expirado | Renovar con certbot |
| **CORS error** | Origen no permitido | Agregar dominio a CORS config |
| **Database connection timeout** | BD no accesible | Verificar host, puerto, credenciales |

## **10.2. Comandos Útiles de Debugging**

```bash
# Ver procesos corriendo
ps aux | grep node
ps aux | grep java

# Ver puertos en uso
sudo netstat -tulpn | grep :3000

# Probar conexión a BD
psql -h localhost -U api_user -d mi_api_db

# Ver logs en tiempo real
tail -f /var/log/mi-api/error.log
journalctl -u mi-api -f

# Probar Nginx config
sudo nginx -t

# Reiniciar servicios
sudo systemctl restart mi-api
sudo systemctl restart nginx

# Verificar salud del sistema
htop
df -h  # Espacio en disco
free -h  # Memoria RAM
```

---

# **11. Conclusión**

Has aprendido los conceptos fundamentales de despliegue en producción:

**Preparación para producción**: Variables de entorno, configuración segura  
**Opciones de despliegue**: Docker vs nativo, cada uno con sus ventajas  
**Nginx como reverse proxy**: SSL, load balancing, seguridad  
**Mejores prácticas**: Logs, monitoring, backups, healthchecks  
**Estrategias robustas**: Blue-green, rolling deployments  

**Flujo completo de despliegue**:
```
Desarrollo → Tests → Build → Deploy → Monitor → Mantener
```

**Recuerda**:
- No exponer información sensible
- Siempre usar HTTPS en producción
- Configurar backups automáticos
- Monitorear métricas continuamente
- Tener plan de rollback

---

# **Aplicación en Frameworks**

Estos conceptos se implementan en los módulos específicos:

### Spring Boot

📄 `spring-boot/p67/a_dodente/14_despliegue_produccion.md`

- Compilación de JAR ejecutable
- application.properties por perfil
- Despliegue con systemd
- Docker multi-stage build

### NestJS

📄 `nest/p67/a_dodente/14_despliegue_produccion.md`

- Build para producción
- ConfigModule para entornos
- PM2 para gestión de procesos
- Dockerfile optimizado

---

# **Recursos Adicionales**

**Documentación oficial**:
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [PM2 Documentation](https://pm2.keymetrics.io/)

**Guías recomendadas**:
- [The Twelve-Factor App](https://12factor.net/) - Metodología para apps modernas
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Hardening Guide](https://www.nginx.com/blog/mitigating-ddos-attacks-with-nginx-and-nginx-plus/)

**Herramientas útiles**:
- [Portainer](https://www.portainer.io/) - Gestión visual de Docker
- [Watchtower](https://containrrr.dev/watchtower/) - Auto-actualización de contenedores
- [Prometheus + Grafana](https://prometheus.io/) - Monitoreo y dashboards

---

# **Resumen Final**

| Concepto | Sin Docker | Con Docker |
|----------|-----------|------------|
| **Setup** | Instalar dependencias en servidor | Dockerfile |
| **Reproducibilidad** | Media | Alta |
| **Portabilidad** | Baja | Muy alta |
| **Escalabilidad** | Manual | Fácil (replicas) |
| **Complejidad** | Baja | Media |
| **Mejor para** | VPS simple, equipo pequeño | Equipos medianos/grandes |

**Decisión final**:
- **Proyecto pequeño/aprendizaje**: Sin Docker (systemd/PM2)
- **Proyecto medio/producción**: Docker Compose
- **Empresa/microservicios**: Kubernetes

