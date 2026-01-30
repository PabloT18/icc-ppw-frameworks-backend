# Programación y Plataformas Web

# **Spring Boot – Despliegue en Producción**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="80">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg" width="80">
</div>

## **Práctica 14 (Spring Boot): Preparación y Despliegue de APIs**

### **Autores**

**Pablo Torres**

📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

💻 GitHub: PabloT18

---

# **Introducción**

Después de implementar autenticación, autorización y validación de ownership en las prácticas anteriores, es momento de **desplegar tu API Spring Boot en producción**.

En esta práctica aprenderás:
- **Arquitectura de Spring Boot**: Cómo funciona Tomcat embebido
- **Build para producción**: Crear JAR ejecutable optimizado
- **Despliegue nativo**: Configurar systemd + Nginx
- **Despliegue con Docker**: Dockerfile multi-stage optimizado
- **PaaS**: Desplegar en Render, Railway, Heroku
- **Health checks**: Usar Spring Boot Actuator
- **Configuración por ambiente**: Profiles y variables de entorno

**Prerequisitos**:
- Proyecto funcional de las prácticas 1-13
- Conocimientos básicos de Linux y terminal
- Docker instalado (para sección Docker)
- Cuenta en servicio PaaS (opcional para despliegue cloud)

---

# **1. Arquitectura de Spring Boot en Ejecución**

## **1.1. ¿Qué es Tomcat Embebido?**

Cuando ejecutas una aplicación Spring Boot con `./gradlew bootRun` o `java -jar app.jar`, **Spring Boot inicia automáticamente un servidor Tomcat embebido**.

### **¿Qué es Tomcat?**

**Apache Tomcat** es un **contenedor de servlets** (servidor de aplicaciones Java) que:
- Recibe peticiones HTTP en un puerto (por defecto 8080)
- Las pasa a tu aplicación Spring Boot (controladores)
- Devuelve las respuestas HTTP al cliente

### **Tomcat "Embebido" vs Tomcat Externo**

| Aspecto | Tomcat Embebido (Spring Boot) | Tomcat Externo (Tradicional) |
|---------|-------------------------------|------------------------------|
| **Instalación** | Incluido en el JAR | Instalar por separado |
| **Configuración** | application.properties | server.xml, context.xml |
| **Despliegue** | `java -jar app.jar` | Copiar WAR a `/webapps` |
| **Portabilidad** | Alta (todo en un JAR) | Baja (requiere servidor) |
| **Actualizaciones** | Actualizar dependencia | Actualizar servidor |
| **Recomendado para** | Microservicios, APIs, cloud | Aplicaciones legacy |

### **¿Hay Nginx Embebido en Spring Boot?**

**NO**. Spring Boot **solo incluye Tomcat embebido** (o Jetty/Undertow si lo configuras).

- **Tomcat embebido**: Maneja peticiones HTTP de tu aplicación Java
- **Nginx**: Es un servidor web externo que se usa como **reverse proxy** (opcional, se configura por separado)

**Flujo típico en producción**:
```
Internet → Nginx (puerto 80/443) → Tomcat embebido (puerto 8080)
```

Nginx se instala **aparte**, no viene con Spring Boot.

## **1.2. Flujo de Ejecución de Spring Boot**

### **En Desarrollo Local**

```bash
./gradlew bootRun
```

**¿Qué sucede internamente?**

```
1. Gradle compila el código (.java → .class)
        ↓
2. Spring Boot inicia Tomcat embebido
        ↓
3. Tomcat abre puerto 8080 (configurable en application.properties)
        ↓
4. Spring Boot escanea @Controllers, @Services, @Repositories
        ↓
5. Inicializa beans (inyección de dependencias)
        ↓
6. Conecta a base de datos (si está configurada)
        ↓
7. Aplicación lista para recibir peticiones
        ↓
8. LOG: "Started Application in X seconds"
```

**Acceso directo**:
```
http://localhost:8080/api/products
↓ (Tomcat embebido maneja directamente)
Controlador → Servicio → Repositorio → BD
```

### **En Build (JAR)**

```bash
./gradlew build
java -jar build/libs/mi-api.jar
```

**¿Qué sucede?**

```
1. Gradle compila y empaqueta TODO en un JAR:
   - Clases compiladas
   - Dependencias (Spring, Tomcat, PostgreSQL driver)
   - application.properties
   - Tomcat embebido
        ↓
2. java -jar ejecuta el JAR
        ↓
3. Tomcat embebido se inicia (igual que en desarrollo)
        ↓
4. Aplicación escucha en puerto configurado
```

**Ventaja**: Un solo archivo ejecutable, sin instalar nada más (solo necesitas Java).

### **En Producción con Nginx**

```bash
java -jar mi-api.jar
# Tomcat escucha en localhost:8080 (interno)
```

```nginx
# Nginx configurado como reverse proxy
server {
    listen 80;
    location / {
        proxy_pass http://localhost:8080;  ← Redirige a Tomcat
    }
}
```

**Flujo completo**:
```
Cliente → Internet → Nginx (80/443) → Tomcat embebido (8080) → Tu API
                           ↓
                    (SSL, rate limiting,
                     load balancing)
```

**Ventajas de Nginx como proxy**:
- Maneja SSL/HTTPS
- Sirve archivos estáticos sin pasar por Java
- Load balancing entre múltiples instancias de Spring Boot
- Rate limiting y seguridad
- Compresión gzip

## **1.3. JAR Ejecutable vs WAR**

### **JAR (Java ARchive) - Recomendado**

**Características**:
- Archivo `.jar` ejecutable standalone
- Incluye Tomcat embebido
- Se ejecuta con `java -jar app.jar`
- Ideal para microservicios y cloud

**Cuándo usar**:
- APIs REST modernas
- Despliegue en Docker
- PaaS (Heroku, Railway, Render)
- Microservicios

### **WAR (Web ARchive) - Legacy**

**Características**:
- Archivo `.war` para desplegar en servidor Tomcat externo
- No incluye Tomcat (usa el del servidor)
- Se copia a carpeta `/webapps` de Tomcat
- Ideal para aplicaciones tradicionales

**Cuándo usar**:
- Empresa con servidores Tomcat ya instalados
- Múltiples aplicaciones en el mismo servidor
- Requisitos legacy

**En esta práctica usaremos JAR** (enfoque moderno).

---

# **2. Configuración por Ambiente**

## **2.1. Profiles de Spring Boot**

Spring Boot permite configuraciones diferentes para cada ambiente usando **profiles**.

### **Estructura de Archivos**

```
src/main/resources/
├── application.yml              ← Configuración común
├── application-dev.yml          ← Desarrollo local
├── application-prod.yml         ← Producción
└── application-test.yml         ← Tests
```

### **application.yml (Base)**

Configuración compartida por todos los ambientes:

```yaml
spring:
  application:
    name: mi-api
  
  # Configuración común de JPA
  jpa:
    hibernate:
      ddl-auto: validate  # En producción NUNCA usar create/update
    properties:
      hibernate:
        format_sql: true

# Configuración común del servidor
server:
  error:
    include-message: always
    include-binding-errors: always

# Actuator (health checks)
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when-authorized
```

### **application-dev.yml (Desarrollo)**

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mi_api_db
    username: postgres
    password: postgres
  
  jpa:
    show-sql: true  # Mostrar queries en consola
    hibernate:
      ddl-auto: update  # Auto-crear tablas (solo en dev)

# Puerto de desarrollo
server:
  port: 8080

# Logs detallados
logging:
  level:
    root: INFO
    ec.edu.ups.pwp67: DEBUG  # Tu paquete base
    org.hibernate.SQL: DEBUG
    org.springframework.security: DEBUG

# JWT (valores de desarrollo)
jwt:
  secret: dev-secret-key-no-usar-en-produccion
  expiration: 3600000  # 1 hora
```

### **application-prod.yml (Producción)**

```yaml
spring:
  datasource:
    url: ${DATABASE_URL}  # Variable de entorno
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 20000
  
  jpa:
    show-sql: false  # No mostrar queries
    hibernate:
      ddl-auto: validate  # Solo validar, no modificar BD

# Puerto de producción
server:
  port: ${PORT:8080}

# Logs solo errores
logging:
  level:
    root: WARN
    ec.edu.ups.pwp67: INFO
  file:
    name: /var/log/mi-api/application.log
    max-size: 10MB
    max-history: 30

# JWT (valores desde entorno)
jwt:
  secret: ${JWT_SECRET}
  expiration: ${JWT_EXPIRATION:3600000}

# Seguridad adicional
server:
  error:
    include-stacktrace: never  # No exponer stack traces
```

## **2.2. Activar Profile**

### **Opción 1: Variable de entorno**

```bash
# Desarrollo
export SPRING_PROFILES_ACTIVE=dev
./gradlew bootRun

# Producción
export SPRING_PROFILES_ACTIVE=prod
java -jar build/libs/mi-api.jar
```

### **Opción 2: Argumento de línea de comandos**

```bash
java -jar build/libs/mi-api.jar --spring.profiles.active=prod
```

### **Opción 3: En application.yml**

```yaml
spring:
  profiles:
    active: dev  # Profile por defecto
```

### **Opción 4: En IDE (IntelliJ/Eclipse)**

**IntelliJ IDEA**:
```
Run → Edit Configurations → Active Profiles: dev
```

## **2.3. Variables de Entorno en Producción**

### **Crear archivo .env (NO versionar en Git)**

```bash
# .env.production
DATABASE_URL=jdbc:postgresql://db.miservidor.com:5432/prod_db
DB_USERNAME=prod_user
DB_PASSWORD=super-secure-password-123
JWT_SECRET=c2VjcmV0LWtleS1mb3ItcHJvZHVjdGlvbi1kb250LWV4cG9zZQ==
JWT_EXPIRATION=3600000
PORT=8080
SPRING_PROFILES_ACTIVE=prod
```

### **Cargar variables al ejecutar**

```bash
# Opción 1: Source del archivo
source .env.production
java -jar build/libs/mi-api.jar

# Opción 2: Inline
DATABASE_URL=jdbc:postgresql://... DB_USERNAME=... java -jar build/libs/mi-api.jar
```

### **En systemd (Linux)**

```ini
[Service]
EnvironmentFile=/opt/mi-api/.env.production
ExecStart=/usr/bin/java -jar /opt/mi-api/mi-api.jar
```

---

# **3. Build para Producción**

## **3.1. Configurar build.gradle.kts**

### **Verificar configuración del plugin**

```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.20"
}

group = "ec.edu.ups.pwp67"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_17
}

springBoot {
    mainClass.set("ec.edu.ups.pwp67.Application")
}

tasks.bootJar {
    archiveFileName.set("mi-api.jar")
}
```

### **Dependencias opcionales para producción**

```kotlin
dependencies {
    // Spring Boot Actuator para health checks
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    
    // Micrometer para métricas (opcional)
    implementation("io.micrometer:micrometer-registry-prometheus")
    
    // Resto de dependencias...
}
```

## **3.2. Compilar JAR Ejecutable**

### **Paso 1: Limpiar builds anteriores**

```bash
./gradlew clean
```

### **Paso 2: Compilar y empaquetar**

```bash
./gradlew build -x test
# -x test para omitir tests (ejecutar tests antes en otro paso)
```

**Salida**:
```
BUILD SUCCESSFUL
Generated JAR: build/libs/mi-api.jar
```

### **Paso 3: Verificar JAR**

```bash
ls -lh build/libs/
# Deberías ver: mi-api.jar (aproximadamente 50-100 MB)

# Ver contenido del JAR
jar -tf build/libs/mi-api.jar | head -20
```

### **Paso 4: Probar JAR localmente**

```bash
java -jar build/libs/mi-api.jar --spring.profiles.active=dev

# Ver logs de inicio
# Deberías ver: "Started Application in X seconds"
```

### **Paso 5: Verificar que funciona**

```bash
# En otra terminal
curl http://localhost:8080/api/products

# O health check
curl http://localhost:8080/actuator/health
```

## **3.3. Optimizar Tamaño del JAR**

### **Excluir dependencias no usadas**

```kotlin
dependencies {
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    
    // Resto de dependencias...
}
```

### **Usar build optimizado**

```bash
# Crear JAR optimizado
./gradlew bootJar --stacktrace

# Tamaño típico:
# Sin optimización: 80-100 MB
# Con optimización: 50-70 MB
```

---

# **4. Despliegue Nativo (Sin Docker)**

## **4.1. Preparar Servidor Linux (Ubuntu/Debian)**

### **Paso 1: Instalar Java**

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Java 17 (o versión que uses en tu proyecto)
sudo apt install -y openjdk-17-jdk

# Verificar instalación
java -version
# Debería mostrar: openjdk version "17.X.X"
```

### **Paso 2: Crear usuario para la aplicación**

```bash
# Crear usuario sin shell (seguridad)
sudo useradd -r -s /bin/false miapi

# Crear directorio de la aplicación
sudo mkdir -p /opt/mi-api
sudo chown miapi:miapi /opt/mi-api
```

### **Paso 3: Subir JAR al servidor**

```bash
# Desde tu máquina local
scp build/libs/mi-api.jar usuario@servidor:/opt/mi-api/

# O clonar repositorio y hacer build en servidor
cd /opt/mi-api
git clone https://github.com/tu-usuario/tu-api.git .
./gradlew build -x test
```

## **4.2. Configurar Variables de Entorno**

### **Crear archivo de configuración**

```bash
sudo nano /opt/mi-api/.env
```

```bash
# Configuración de producción
DATABASE_URL=jdbc:postgresql://localhost:5432/prod_db
DB_USERNAME=miapi_user
DB_PASSWORD=secure-password-here
JWT_SECRET=your-super-secret-jwt-key-here-min-256-bits
JWT_EXPIRATION=3600000
SPRING_PROFILES_ACTIVE=prod
```

```bash
# Proteger archivo (solo lectura para el usuario de la app)
sudo chown miapi:miapi /opt/mi-api/.env
sudo chmod 600 /opt/mi-api/.env
```

## **4.3. Configurar systemd Service**

### **Crear archivo de servicio**

```bash
sudo nano /etc/systemd/system/mi-api.service
```

```ini
[Unit]
Description=Spring Boot Mi API
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=miapi
Group=miapi
WorkingDirectory=/opt/mi-api

# Cargar variables de entorno
EnvironmentFile=/opt/mi-api/.env

# Comando para ejecutar
ExecStart=/usr/bin/java \
    -Xms256m \
    -Xmx512m \
    -jar /opt/mi-api/mi-api.jar \
    --spring.profiles.active=prod

# Reiniciar automáticamente si falla
Restart=always
RestartSec=10

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=mi-api

# Seguridad adicional
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### **Explicación de parámetros JVM**

| Parámetro | Significado | Valor recomendado |
|-----------|-------------|-------------------|
| `-Xms` | Memoria inicial heap | 256m (ajustar según servidor) |
| `-Xmx` | Memoria máxima heap | 512m-1g (ajustar según carga) |
| `-jar` | Ejecutar JAR | Ruta al JAR |

**Para servidores con más recursos**:
```
-Xms512m -Xmx2g
```

### **Activar y gestionar el servicio**

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Habilitar inicio automático
sudo systemctl enable mi-api

# Iniciar servicio
sudo systemctl start mi-api

# Ver estado
sudo systemctl status mi-api

# Ver logs en tiempo real
sudo journalctl -u mi-api -f

# Reiniciar
sudo systemctl restart mi-api

# Detener
sudo systemctl stop mi-api
```

### **Verificar que funciona**

```bash
# Esperar unos segundos para que inicie
sleep 10

# Probar endpoint
curl http://localhost:8080/api/products

# Health check
curl http://localhost:8080/actuator/health
```

## **4.4. Configurar Nginx como Reverse Proxy**

### **Instalar Nginx**

```bash
sudo apt install -y nginx
```

### **Crear configuración del sitio**

```bash
sudo nano /etc/nginx/sites-available/mi-api
```

```nginx
# Upstream (backend Spring Boot)
upstream spring_backend {
    server 127.0.0.1:8080 max_fails=3 fail_timeout=30s;
}

# HTTP (redirigir a HTTPS)
server {
    listen 80;
    server_name api.midominio.com;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name api.midominio.com;

    # Certificados SSL (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/api.midominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.midominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Logs
    access_log /var/log/nginx/mi-api-access.log;
    error_log /var/log/nginx/mi-api-error.log;

    # Tamaño máximo de request
    client_max_body_size 10M;

    # Health check (sin logs)
    location /actuator/health {
        proxy_pass http://spring_backend;
        access_log off;
    }

    # API endpoints
    location /api {
        proxy_pass http://spring_backend;
        proxy_http_version 1.1;
        
        # Headers importantes
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts para operaciones largas
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # WebSocket support (si usas)
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Servir documentación estática (si tienes)
    location /docs {
        alias /opt/mi-api/docs;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
}
```

### **Activar configuración**

```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/mi-api /etc/nginx/sites-enabled/

# Probar configuración
sudo nginx -t

# Recargar Nginx
sudo systemctl reload nginx
```

### **Configurar SSL con Let's Encrypt**

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado (Nginx debe estar corriendo)
sudo certbot --nginx -d api.midominio.com

# Renovación automática ya está configurada
sudo systemctl status certbot.timer
```

---

# **5. Despliegue con Docker**

## **5.1. Dockerfile Multi-Stage Optimizado**

### **¿Por qué Multi-Stage?**

**Problema**: Si compilas dentro del contenedor, la imagen final incluye Maven, código fuente, etc. (imagen pesada y menos segura).

**Solución**: Usar dos etapas:
1. **Build Stage**: Imagen con Maven para compilar
2. **Runtime Stage**: Imagen ligera solo con JRE y JAR

**Resultado**: Imagen final más pequeña (150-200 MB vs 500+ MB)

### **Dockerfile (enfoque completo)**

```dockerfile
# ============================================
# ETAPA 1: BUILD
# ============================================
# Imagen base con Gradle y JDK para compilar
FROM gradle:8.5-eclipse-temurin-17 AS builder

# Directorio de trabajo
WORKDIR /build

# Copiar archivos de Gradle primero (aprovechar caché de Docker)
# Si build.gradle.kts no cambia, Docker reutiliza esta capa
COPY build.gradle.kts gradle.properties settings.gradle.kts ./
COPY gradle ./gradle

# Descargar dependencias (se cachea si build.gradle.kts no cambia)
RUN gradle dependencies --no-daemon

# Copiar código fuente
COPY src ./src

# Compilar aplicación (sin tests para producción)
RUN gradle build -x test --no-daemon

# Verificar que JAR existe
RUN ls -lh build/libs/

# ============================================
# ETAPA 2: RUNTIME
# ============================================
# Imagen ligera solo con JRE (sin Maven, sin código fuente)
FROM eclipse-temurin:17-jre-alpine

# Crear usuario no-root (seguridad)
RUN addgroup -S spring && adduser -S spring -G spring

# Directorio de trabajo
WORKDIR /app

# Copiar JAR desde la etapa de build
COPY --from=builder /build/build/libs/*.jar app.jar

# Cambiar ownership
RUN chown spring:spring app.jar

# Cambiar a usuario no-root
USER spring:spring

# Exponer puerto (documentación, no abre el puerto)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

# Variables de entorno por defecto (se sobreescriben en runtime)
ENV SPRING_PROFILES_ACTIVE=prod

# Comando de inicio
ENTRYPOINT ["java", \
    "-Djava.security.egd=file:/dev/./urandom", \
    "-Xms256m", \
    "-Xmx512m", \
    "-jar", \
    "app.jar"]
```

### **Explicación línea por línea**

```dockerfile
FROM gradle:8.5-eclipse-temurin-17 AS builder
```
- Imagen base para compilar
- `AS builder`: Nombra esta etapa para referenciarla después
- Incluye Gradle y JDK 17

```dockerfile
COPY build.gradle.kts gradle.properties settings.gradle.kts ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon
```
- Descargar dependencias antes de copiar código
- Si `build.gradle.kts` no cambia, Docker reutiliza esta capa (build más rápido)

```dockerfile
FROM eclipse-temurin:17-jre-alpine
```
- Imagen ligera con solo JRE (sin JDK ni Gradle)
- `alpine`: Distribución Linux minimalista (5 MB base)

```dockerfile
RUN addgroup -S spring && adduser -S spring -G spring
USER spring:spring
```
- Crear usuario no-root
- Ejecutar aplicación con usuario limitado (seguridad)

```dockerfile
COPY --from=builder /build/build/libs/*.jar app.jar
```
- Copiar JAR compilado desde la etapa `builder`
- Solo el JAR, no todo el código fuente

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s ...
```
- Docker verifica cada 30s que la app esté healthy
- Si falla 3 veces, marca contenedor como unhealthy

```dockerfile
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", ...]
```
- `-Djava.security.egd`: Mejora performance de generación de números aleatorios en Docker
- `-Xms256m -Xmx512m`: Limitar memoria heap

### **Construir imagen**

```bash
# Desde el directorio del proyecto
docker build -t mi-api:1.0 .

# Ver tamaño de imagen
docker images mi-api:1.0
# REPOSITORY   TAG   SIZE
# mi-api       1.0   180MB  ← Mucho más pequeña que 500+ MB sin multi-stage
```

### **Ejecutar contenedor**

```bash
# Ejecutar con variables de entorno
docker run -d \
  --name mi-api \
  -p 8080:8080 \
  -e DATABASE_URL=jdbc:postgresql://host.docker.internal:5432/prod_db \
  -e DB_USERNAME=postgres \
  -e DB_PASSWORD=postgres \
  -e JWT_SECRET=my-secret-key \
  -e SPRING_PROFILES_ACTIVE=prod \
  mi-api:1.0

# Ver logs
docker logs -f mi-api

# Ver estado de salud
docker inspect mi-api | grep -A 10 Health
```

## **5.2. Docker Compose Completo**

### **docker-compose.yml**

```yaml
version: '3.8'

services:
  # ============================================
  # POSTGRESQL
  # ============================================
  postgres:
    image: postgres:15-alpine
    container_name: mi-api-postgres
    restart: always
    environment:
      POSTGRES_DB: mi_api_db
      POSTGRES_USER: api_user
      POSTGRES_PASSWORD: secure-password-123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U api_user -d mi_api_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # ============================================
  # SPRING BOOT API
  # ============================================
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mi-api
    restart: always
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
      DATABASE_URL: jdbc:postgresql://postgres:5432/mi_api_db
      DB_USERNAME: api_user
      DB_PASSWORD: secure-password-123
      JWT_SECRET: your-super-secret-jwt-key-change-this-in-production
      JWT_EXPIRATION: 3600000
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - app-network

  # ============================================
  # NGINX REVERSE PROXY
  # ============================================
  nginx:
    image: nginx:alpine
    container_name: mi-api-nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx
    depends_on:
      - api
    networks:
      - app-network

# ============================================
# VOLUMES
# ============================================
volumes:
  postgres_data:
    driver: local
  nginx_logs:
    driver: local

# ============================================
# NETWORKS
# ============================================
networks:
  app-network:
    driver: bridge
```

### **nginx/nginx.conf**

```nginx
user nginx;
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    sendfile on;
    keepalive_timeout 65;
    gzip on;

    upstream spring_backend {
        server api:8080 max_fails=3 fail_timeout=30s;
    }

    server {
        listen 80;
        server_name localhost;

        client_max_body_size 10M;

        location /actuator/health {
            proxy_pass http://spring_backend;
            access_log off;
        }

        location / {
            proxy_pass http://spring_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

### **Comandos Docker Compose**

```bash
# Construir y levantar todos los servicios
docker-compose up -d --build

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs solo de API
docker-compose logs -f api

# Ver estado
docker-compose ps

# Reiniciar solo API
docker-compose restart api

# Detener todo
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: borra BD)
docker-compose down -v

# Ejecutar comando en contenedor
docker-compose exec api bash
docker-compose exec postgres psql -U api_user -d mi_api_db
```

### **Verificar que funciona**

```bash
# Esperar a que inicien todos los servicios
sleep 30

# Health check
curl http://localhost/actuator/health

# API endpoint
curl http://localhost/api/products

# Ver logs de inicio
docker-compose logs api | grep "Started"
```

## **5.3. .dockerignore**

Crear archivo `.dockerignore` para no copiar archivos innecesarios:

```
# Gradle
build/
.gradle/
gradle-app.setting
.gradletasknamecache

# IDE
.idea/
.vscode/
*.iml
*.ipr
*.iws
.project
.classpath
.settings/

# Git
.git/
.gitignore
.gitattributes

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Docs
README.md
docs/
```

---

# **6. Despliegue en PaaS (Platform as a Service)**

## **6.1. Render**

### **Ventajas**:
- Free tier generoso (750 horas/mes)
- PostgreSQL incluido
- SSL automático
- Deploy desde Git
- Health checks automáticos

### **Pasos de despliegue**:

#### **1. Crear `render.yaml` en raíz del proyecto**

```yaml
services:
  # Base de datos PostgreSQL
  - type: pserv
    name: mi-api-db
    env: docker
    plan: free
    databases:
      - name: mi_api_db
        user: api_user

  # Spring Boot API
  - type: web
    name: mi-api
    env: java
    plan: free
    buildCommand: ./gradlew build -x test
    startCommand: java -jar build/libs/mi-api.jar
    healthCheckPath: /actuator/health
    envVars:
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: DATABASE_URL
        fromDatabase:
          name: mi-api-db
          property: connectionString
      - key: JWT_SECRET
        generateValue: true
      - key: JWT_EXPIRATION
        value: 3600000
```

#### **2. Conectar repositorio Git**

1. Hacer commit y push a GitHub/GitLab
2. Ir a [Render Dashboard](https://dashboard.render.com)
3. "New +" → "Blueprint"
4. Conectar repositorio
5. Render detecta `render.yaml` automáticamente
6. Deploy

#### **3. Variables de entorno adicionales**

En Dashboard de Render:
- Settings → Environment
- Agregar variables no versionadas:
  - `JWT_SECRET`: (generar secreto seguro)
  - `SPRING_DATASOURCE_URL`: (autocompletado desde BD)

#### **4. Ver logs**

```
Render Dashboard → Tu servicio → Logs
```

## **6.2. Railway**

### **Ventajas**:
- $5 gratis/mes
- Muy fácil configuración
- PostgreSQL con un click
- Deploy automático desde Git

### **Pasos**:

#### **1. Crear proyecto en Railway**

1. Ir a [Railway](https://railway.app)
2. "New Project"
3. "Deploy from GitHub repo"
4. Seleccionar tu repositorio

#### **2. Agregar PostgreSQL**

1. En proyecto → "New" → "Database" → "PostgreSQL"
2. Railway genera automáticamente:
   - `DATABASE_URL`
   - `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`

#### **3. Configurar variables**

En tu servicio → Variables:

```
SPRING_PROFILES_ACTIVE=prod
DATABASE_URL=${{Postgres.DATABASE_URL}}
JWT_SECRET=your-secret-here
JWT_EXPIRATION=3600000
```

#### **4. Configurar start command**

Settings → Deploy → Start Command:

```bash
java -Xms256m -Xmx512m -jar build/libs/*.jar
```

#### **5. Deploy automático**

Railway detecta push a GitHub y despliega automáticamente.

## **6.3. Heroku (Clásico)**

### **Ventajas**:
- Plataforma madura
- Muchos add-ons
- Documentación extensa

### **Nota**: Heroku eliminó free tier en 2022, ahora mínimo $7/mes.

### **Pasos**:

#### **1. Crear `Procfile` en raíz**

```
web: java -Xmx512m -jar build/libs/mi-api.jar --server.port=$PORT
```

#### **2. Crear `system.properties`**

```properties
java.runtime.version=17
```

#### **3. Deploy con Heroku CLI**

```bash
# Login
heroku login

# Crear app
heroku create mi-api

# Agregar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variables
heroku config:set SPRING_PROFILES_ACTIVE=prod
heroku config:set JWT_SECRET=your-secret

# Deploy (Heroku detecta Gradle automáticamente)
git push heroku main

# Ver logs
heroku logs --tail

# Abrir app
heroku open
```

## **6.4. Comparación de PaaS**

| PaaS | Free Tier | PostgreSQL | SSL | Deploy desde Git | Mejor para |
|------|-----------|------------|-----|------------------|------------|
| **Render** | 750h/mes | Incluido | Auto | Sí | Portafolio, demos |
| **Railway** | $5 crédito | 1 click | Auto | Sí | Proyectos personales |
| **Heroku** | ❌ Desde $7/mes | Add-on | Auto | Sí | Producción seria |
| **Fly.io** | Limitado | Sí | Auto | Sí | Apps globales |

---

# **7. Spring Boot Actuator (Health Checks)**

## **7.1. ¿Qué es Actuator?**

**Spring Boot Actuator** proporciona endpoints de monitoreo y gestión listos para producción:
- `/actuator/health`: Estado de salud de la aplicación
- `/actuator/info`: Información de la aplicación
- `/actuator/metrics`: Métricas (memoria, threads, requests)
- `/actuator/env`: Variables de entorno (cuidado en producción)

## **7.2. Configuración**

### **1. Agregar dependencia**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### **2. Configurar en application-prod.yml**

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics  # Solo exponer endpoints necesarios
      base-path: /actuator
  
  endpoint:
    health:
      show-details: when-authorized  # Detalles solo para usuarios autenticados
      probes:
        enabled: true  # Para Kubernetes liveness/readiness
  
  health:
    db:
      enabled: true  # Verificar conexión a BD
    defaults:
      enabled: true

# Información de la app
info:
  app:
    name: Mi API
    description: API de gestión de productos
    version: '@project.version@'
    encoding: '@project.build.sourceEncoding@'
    java:
      version: '@java.version@'
```

### **3. Proteger endpoints con Security**

```java
@Configuration
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // ... configuración existente
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()  // Health público
                .requestMatchers("/actuator/**").hasRole("ADMIN")  // Resto solo ADMIN
                .anyRequest().authenticated()
            );
        return http.build();
    }
}
```

## **7.3. Endpoints Importantes**

### **/actuator/health (Público)**

```bash
curl http://localhost:8080/actuator/health
```

**Respuesta cuando todo está bien**:
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL",
        "validationQuery": "isValid()"
      }
    },
    "diskSpace": {
      "status": "UP"
    },
    "ping": {
      "status": "UP"
    }
  }
}
```

**Respuesta cuando BD está caída**:
```json
{
  "status": "DOWN",
  "components": {
    "db": {
      "status": "DOWN",
      "details": {
        "error": "Cannot create PoolableConnectionFactory"
      }
    }
  }
}
```

### **/actuator/info**

```bash
curl http://localhost:8080/actuator/info
```

```json
{
  "app": {
    "name": "Mi API",
    "description": "API de gestión de productos",
    "version": "1.0.0",
    "java": {
      "version": "17"
    }
  }
}
```

### **/actuator/metrics**

```bash
# Lista de métricas disponibles
curl http://localhost:8080/actuator/metrics

# Métrica específica
curl http://localhost:8080/actuator/metrics/jvm.memory.used
```

```json
{
  "name": "jvm.memory.used",
  "measurements": [
    {
      "statistic": "VALUE",
      "value": 234567890
    }
  ]
}
```

## **7.4. Health Check Personalizado**

### **Crear HealthIndicator personalizado**

```java
@Component
public class CustomHealthIndicator implements HealthIndicator {

    @Autowired
    private ProductRepository productRepository;

    @Override
    public Health health() {
        try {
            // Verificar que podemos consultar la BD
            long count = productRepository.count();
            
            return Health.up()
                    .withDetail("products", count)
                    .withDetail("message", "Database connection OK")
                    .build();
        } catch (Exception e) {
            return Health.down()
                    .withDetail("error", e.getMessage())
                    .build();
        }
    }
}
```

**Resultado**:
```json
{
  "status": "UP",
  "components": {
    "custom": {
      "status": "UP",
      "details": {
        "products": 42,
        "message": "Database connection OK"
      }
    }
  }
}
```

---

# **8. Aplicación Práctica: Continuando tu Proyecto**

## **8.1. Preparar tu Proyecto Actual**

### **Paso 1: Configurar Profiles y build.gradle.kts**

**Crear estructura**:
```
src/main/resources/
├── application.yml              ← Base
├── application-dev.yml          ← Desarrollo
└── application-prod.yml         ← Producción
```

**Configurar build.gradle.kts**:
```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.20"
}

group = "ec.edu.ups.pwp67"
version = "1.0.0"

java {
    sourceCompatibility = JavaVersion.VERSION_17
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    
    runtimeOnly("org.postgresql:postgresql")
    developmentOnly("org.springframework.boot:spring-boot-devtools")
}

springBoot {
    mainClass.set("ec.edu.ups.pwp67.Application")
}

tasks.bootJar {
    archiveFileName.set("mi-api.jar")
}
```

**application.yml**:
```yaml
spring:
  application:
    name: pwp67-api
  
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        format_sql: true

server:
  error:
    include-message: always

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
```

**application-dev.yml**:
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/pwp67_dev
    username: postgres
    password: postgres
  
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: update

server:
  port: 8080

logging:
  level:
    ec.edu.ups.pwp67: DEBUG

jwt:
  secret: dev-secret-not-for-production
  expiration: 3600000
```

**application-prod.yml**:
```yaml
spring:
  datasource:
    url: ${DATABASE_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
  
  jpa:
    show-sql: false
    hibernate:
      ddl-auto: validate

server:
  port: ${PORT:8080}
  error:
    include-stacktrace: never

logging:
  level:
    root: WARN
    ec.edu.ups.pwp67: INFO
  file:
    name: /var/log/pwp67-api/application.log

jwt:
  secret: ${JWT_SECRET}
  expiration: ${JWT_EXPIRATION:3600000}
```

### **Paso 2: Actuator ya está incluido**

Ya está incluido en el `build.gradle.kts` anterior:
```kotlin
implementation("org.springframework.boot:spring-boot-starter-actuator")
```

### **Paso 3: Proteger Actuator**

**SecurityConfig.java**:
```java
@Configuration
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                // Públicos
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                
                // Solo ADMIN
                .requestMatchers("/actuator/**").hasRole("ADMIN")
                
                // Resto autenticado
                .anyRequest().authenticated()
            )
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .addFilterBefore(jwtAuthenticationFilter, 
                UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
}
```

### **Paso 4: Crear Dockerfile**

```dockerfile
# ETAPA 1: BUILD
FROM gradle:8.5-eclipse-temurin-17 AS builder
WORKDIR /build
COPY build.gradle.kts gradle.properties settings.gradle.kts ./
COPY gradle ./gradle
RUN gradle dependencies --no-daemon
COPY src ./src
RUN gradle build -x test --no-daemon

# ETAPA 2: RUNTIME
FROM eclipse-temurin:17-jre-alpine
RUN addgroup -S spring && adduser -S spring -G spring
WORKDIR /app
COPY --from=builder /build/build/libs/*.jar app.jar
RUN chown spring:spring app.jar
USER spring:spring
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1
ENV SPRING_PROFILES_ACTIVE=prod
ENTRYPOINT ["java", \
    "-Djava.security.egd=file:/dev/./urandom", \
    "-Xms256m", \
    "-Xmx512m", \
    "-jar", \
    "app.jar"]
```

### **Paso 5: Crear docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: pwp67_db
      POSTGRES_USER: pwp67_user
      POSTGRES_PASSWORD: pwp67_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pwp67_user -d pwp67_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    restart: always
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
      DATABASE_URL: jdbc:postgresql://postgres:5432/pwp67_db
      DB_USERNAME: pwp67_user
      DB_PASSWORD: pwp67_password
      JWT_SECRET: your-jwt-secret-change-this
      JWT_EXPIRATION: 3600000
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
```

### **Paso 6: Crear .dockerignore**

```
build/
.gradle/
.git/
.idea/
*.iml
README.md
.env
.gradle/
gradle-app.setting
.gradletasknamecache
```

## **8.2. Probar Localmente**

### **Con Gradle (desarrollo)**

```bash
# Compilar
./gradlew build -x test

# Ejecutar
./gradlew bootRun --args='--spring.profiles.active=dev'

# O directamente el JAR
java -jar build/libs/mi-api.jar --spring.profiles.active=dev
```

### **Con Docker Compose**

```bash
# Build y levantar
docker-compose up -d --build

# Ver logs
docker-compose logs -f api

# Esperar inicio (ver "Started Application")

# Probar health check
curl http://localhost:8080/actuator/health

# Probar login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ups.edu.ec","password":"admin123"}'

# Ver productos
curl http://localhost:8080/api/products

# Detener
docker-compose down
```

## **8.3. Desplegar en Render**

### **Paso 1: Preparar repositorio**

```bash
# Asegúrate de tener todos los archivos (incluido build.gradle.kts)
git add .
git commit -m "feat(spring-boot): configurar despliegue producción con Gradle"
git push origin main
```

### **Paso 2: Crear render.yaml**

```yaml
services:
  - type: pserv
    name: pwp67-db
    env: docker
    plan: free
    databases:
      - name: pwp67_db
        user: pwp67_user

  - type: web
    name: pwp67-api
    env: java
    plan: free
    buildCommand: ./gradlew build -x test
    startCommand: java -Xms256m -Xmx512m -jar build/libs/pwp67-api.jar
    healthCheckPath: /actuator/health
    envVars:
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: DATABASE_URL
        fromDatabase:
          name: pwp67-db
          property: connectionString
      - key: JWT_SECRET
        generateValue: true
      - key: JWT_EXPIRATION
        value: 3600000
```

### **Paso 3: Deploy en Render**

1. Ir a [Render Dashboard](https://dashboard.render.com)
2. New → Blueprint
3. Conectar GitHub repo
4. Render detecta `render.yaml` (basado en Gradle)
5. Deploy automático con `./gradlew build -x test`

### **Paso 4: Probar en producción**

```bash
# URL de Render (ejemplo)
API_URL=https://pwp67-api.onrender.com

# Health check
curl $API_URL/actuator/health

# Login
curl -X POST $API_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ups.edu.ec","password":"admin123"}'

# Usar token en requests
TOKEN="<token-obtenido>"
curl $API_URL/api/products \
  -H "Authorization: Bearer $TOKEN"
```

---

# **9. Troubleshooting Común**

## **9.1. Problemas de Build**

### **Error: "Failed to execute goal on project"**

```bash
# Limpiar cache de Gradle
./gradlew clean
rm -rf ~/.gradle/caches

# Volver a build
./gradlew build -x test
```

### **Error: "No main manifest attribute"**

**Solución**: Verificar configuración en `build.gradle.kts`:

```kotlin
springBoot {
    mainClass.set("ec.edu.ups.pwp67.Application")
}

tasks.bootJar {
    archiveFileName.set("mi-api.jar")
}
```

## **9.2. Problemas de Ejecución**

### **Error: "Port 8080 already in use"**

```bash
# Ver qué usa el puerto
lsof -i :8080

# Matar proceso
kill -9 <PID>

# O cambiar puerto
java -jar app.jar --server.port=8081
```

### **Error: "Cannot create PoolableConnectionFactory"**

**Causas**:
- PostgreSQL no está corriendo
- Credenciales incorrectas
- Host/puerto incorrecto

**Solución**:
```bash
# Verificar PostgreSQL
systemctl status postgresql

# Verificar conexión
psql -U usuario -h host -d base_datos
```

## **9.3. Problemas de Docker**

### **Error: "Cannot connect to Docker daemon"**

```bash
# Iniciar Docker
sudo systemctl start docker

# Verificar
docker ps
```

### **Error: "Health check unhealthy"**

```bash
# Ver logs del contenedor
docker logs <container-id>

# Entrar al contenedor
docker exec -it <container-id> sh

# Probar health check manualmente
wget -O- http://localhost:8080/actuator/health
```

## **9.4. Comandos de Diagnóstico**

```bash
# Ver procesos Java corriendo
ps aux | grep java

# Ver memoria de JVM
jstat -gc <pid>

# Ver threads
jstack <pid>

# Ver logs de systemd
journalctl -u mi-api -f

# Verificar variables de entorno
docker exec mi-api env | grep DATABASE

# Test de conectividad a BD
telnet postgres-host 5432
```

---

# **10. Best Practices de Producción**

## **10.1. Configuración**

**Usar profiles** (`dev`, `prod`)  
**Variables de entorno** para secretos  
**No versionar** `.env` en Git  
**Validar configuración** antes de deploy  
**Logs estructurados** (JSON en producción)

## **10.2. Seguridad**

**No exponer** stack traces  
**Rate limiting** en Nginx  
**HTTPS obligatorio**  
**Actualizar dependencias** regularmente  
**Escanear vulnerabilidades** (usar herramientas como OWASP Dependency-Check)

## **10.3. Performance**

**Pool de conexiones** optimizado  
**Índices** en BD  
**Caché** para queries frecuentes  
**Compresión gzip**  
**Limitar memoria JVM** (`-Xmx`)

## **10.4. Monitoreo**

**Health checks** con Actuator  
**Logs centralizados**  
**Alertas** para errores 5xx  
**Métricas** de rendimiento  
**Backups automáticos** de BD

---

# **11. Conclusiones**

Has aprendido a:

**Entender** arquitectura de Spring Boot (Tomcat embebido)  
**Configurar** profiles y variables de entorno  
**Compilar** JAR ejecutable optimizado  
**Desplegar nativamente** con systemd + Nginx  
**Dockerizar** con multi-stage build  
**Usar Docker Compose** para stack completo  
**Desplegar en PaaS** (Render, Railway, Heroku)  
**Monitorear** con Spring Boot Actuator  
**Aplicar best practices** de producción

**Próximos pasos**:
- Implementar CI/CD con GitHub Actions
- Configurar monitoreo avanzado (Prometheus/Grafana)
- Implementar caché con Redis
- Optimizar queries con JPA
- Deploy en Kubernetes (avanzado)

---

# **12. Recursos Adicionales**

**Documentación oficial**:
- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Nginx Documentation](https://nginx.org/en/docs/)

**Tutoriales**:
- [Deploying Spring Boot Apps](https://spring.io/guides/gs/spring-boot-docker/)
- [Spring Boot with Docker](https://spring.io/guides/topicals/spring-boot-docker/)

**Herramientas**:
- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [Docker Hub](https://hub.docker.com/)

---

# **Resumen Final**

| Opción | Configuración | Portabilidad | Escalabilidad | Mejor para |
|--------|---------------|--------------|---------------|------------|
| **JAR + systemd** | Media | Baja | Media | Aprendizaje, VPS |
| **Docker Compose** | Media | Alta | Media | Producción simple |
| **PaaS (Render/Railway)** | Baja | Alta | Alta | Portafolio, MVP |
| **Kubernetes** | Muy alta | Máxima | Máxima | Empresarial |

**Para tu proyecto académico**: Recomendamos **Docker local** + **Render/Railway para demo online**.
