
# Programación y Plataformas Web

# Frameworks Backend: NestJS – Servicios, Lógica de Negocio e Inyección de Dependencias

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="110" alt="Nest Logo">
</div>



# Práctica 4 (NestJS): Controladores + Servicios + Lógica de Negocio

### Autores

**Pablo Torres**

 📧 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

 💻 GitHub: PabloT18

---


# 1. Introducción

En la práctica anterior (Práctica 3) se construyó un CRUD REST completo colocando **toda la lógica dentro del controlador**, incluyendo:

* almacenamiento del arreglo en memoria
* creación
* consulta
* actualizaciones
* eliminación
* manejo del ID incremental

Ese enfoque es útil para comprender cómo funciona un controlador, pero **no es sostenible** en una aplicación real.

En NestJS, la arquitectura estándar es:

```
Controller → Service → Repository / Data Source
```

En esta práctica se introduce:

* servicios con `@Injectable()`
* inyección de dependencias
* separación de responsabilidades (SRP)
* traslado de la lógica desde el controlador hacia el servicio
* uso correcto del patrón MVCS en NestJS

El módulo trabajado será **users/**.
En la parte práctica se replica la estructura para **products/**.



# 2. Estructura del módulo con servicios

Carpeta destino:

```
src/users/
```

Ahora se utilizará:

```
users/
 ├── controllers/
 │     └── users.controller.ts
 ├── services/
 │     ├── users.service.ts
 ├── entities/
 ├── dtos/
 ├── mappers/
 └── users.module.ts
```

En este tema:

* el controlador solo enruta solicitudes
* la lógica del CRUD se traslada a `UsersService`
* la lista en memoria vive dentro del servicio
* NestJS inyecta automáticamente el servicio en el controlador



# 3. Servicio (UsersService)

## Generación del servicio

Para crear el servicio se utiliza el CLI de NestJS:

```bash
nest generate service users/services/users --flat
```

O en su forma abreviada:

```bash
nest g s users/services/users --flat
```

Este comando:
* Crea el archivo `users.service.ts` en `src/users/services/`
* Genera la clase con el decorador `@Injectable()`
* Incluye un archivo de pruebas `.spec.ts`
* Registra automáticamente el servicio en el módulo

## El decorador @Injectable()

```ts
@Injectable()
export class UsersService {
  // ...
}
```

`@Injectable()` es un decorador que marca la clase como un **proveedor** que puede ser inyectado en otros componentes.

Características:

* **Inyección de dependencias**: permite que NestJS cree una instancia del servicio y la inyecte donde sea necesaria
* **Singleton por defecto**: NestJS crea una única instancia compartida en toda la aplicación
* **Gestión automática**: el framework controla el ciclo de vida del servicio
* **Testeable**: facilita la creación de mocks para pruebas unitarias

Sin este decorador, la clase no puede ser inyectada en controladores u otros servicios.

## Implementación del servicio

Archivo:
`services/users.service.ts`

La lógica que antes estuvo en el controlador se coloca en el servicio:

```ts

@Injectable()
export class UsersService {

  private users: User[] = [];
  private currentId = 1;

  findAll() {
    return this.users.map(u => UserMapper.toResponse(u));
  }

  findOne(id: number) {
    const user = this.users.find(u => u.id === id);
    if (!user) return { error: 'User not found' };
    return UserMapper.toResponse(user);
  }

  create(dto: CreateUserDto) {
    const entity = UserMapper.toEntity(this.currentId++, dto);
    this.users.push(entity);
    return UserMapper.toResponse(entity);
  }

  update(id: number, dto: UpdateUserDto) {
    const user = this.users.find(u => u.id === id);
    if (!user) return { error: 'User not found' };

    user.name = dto.name;
    user.email = dto.email;

    return UserMapper.toResponse(user);
  }

  partialUpdate(id: number, dto: PartialUpdateUserDto) {
    const user = this.users.find(u => u.id === id);
    if (!user) return { error: 'User not found' };

    if (dto.name !== undefined) user.name = dto.name;
    if (dto.email !== undefined) user.email = dto.email;

    return UserMapper.toResponse(user);
  }

  delete(id: number) {
    const exists = this.users.some(u => u.id === id);
    if (!exists) return { error: 'User not found' };

    this.users = this.users.filter(u => u.id !== id);
    return { message: 'Deleted successfully' };
  }
}
```



# 4. Registro del servicio en el módulo

Archivo:
`users.module.ts`

El módulo debe exponer el servicio para ser inyectado:

```ts
@Module({
  controllers: [UsersController],
  providers: [UsersService],
})
export class UsersModule {}
```

Con esto NestJS sabe:

* qué servicio debe crear
* cuándo debe inyectarlo
* dónde debe usarlo



# 5. Controlador usando el servicio

## Inyección de dependencias

La inyección de dependencias (DI) es un patrón de diseño donde una clase recibe sus dependencias desde el exterior en lugar de crearlas internamente.

En NestJS, la inyección se realiza a través del **constructor**:

```ts
constructor(private readonly service: UsersService) {}
```

### ¿Cómo funciona?

1. **Declaración en el constructor**
   * Se define el tipo de servicio que se necesita
   * `private readonly` crea automáticamente una propiedad de clase
   * NestJS detecta la dependencia por el tipo

2. **Resolución automática**
   * NestJS busca el servicio registrado en el módulo (`providers: [UsersService]`)
   * Crea o reutiliza la instancia del servicio (singleton)
   * Inyecta la instancia en el controlador

3. **Uso en métodos**
   * El servicio está disponible como `this.service`
   * Se pueden llamar sus métodos directamente

### Beneficios de la inyección de dependencias

* **Desacoplamiento**: el controlador no sabe cómo se crea el servicio
* **Testabilidad**: se puede reemplazar el servicio real con un mock
* **Reutilización**: el mismo servicio se inyecta en múltiples lugares
* **Mantenibilidad**: cambios en el servicio no afectan al controlador
* **Ciclo de vida gestionado**: NestJS controla cuándo crear y destruir instancias

### Ejemplo visual del flujo

```
NestJS Container
├── Crea UsersService
│   └── Instancia única (singleton)
├── Inyecta en UsersController
│   └── constructor(private service: UsersService)
└── UsersController usa this.service.findAll()
```

## Implementación del controlador

Archivo:
`controllers/users.controller.ts`

El controlador ya no contiene lógica. Solo enruta:

```ts
@Controller('api/users')
export class UsersController {

  constructor(private readonly service: UsersService) {}

  @Get()
  findAll() {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.service.findOne(Number(id));
  }

  @Post()
  create(@Body() dto: CreateUserDto) {
    return this.service.create(dto);
  }

  @Put(':id')
  update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    return this.service.update(Number(id), dto);
  }

  @Patch(':id')
  partialUpdate(@Param('id') id: string, @Body() dto: PartialUpdateUserDto) {
    return this.service.partialUpdate(Number(id), dto);
  }

  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.service.delete(Number(id));
  }
}
```

Esto permite que:

* el controlador sea mínimo
* el servicio sea el centro de la lógica
* la prueba unitaria del servicio sea directa
* el cambio futuro hacia una base de datos no afecte al controlador



# 6. ¿Por qué se implementa así?

### Separación fuerte entre capas

Un controlador solo:

* recibe
* valida mínimamente
* enruta

Un servicio:

* contiene reglas de negocio
* administra datos
* aplica validaciones complejas
* prepara información antes del repositorio

### Inyección de dependencias

NestJS crea el servicio y se lo entrega al controlador automáticamente.

Esto permite:

* pruebas unitarias sin servidor
* reemplazar implementaciones con facilidad
* mantenimiento claro y ordenado

### Preparación para persistencia real

En una práctica posterior:

```
this.users = []
```

se reemplazará por:

```
UserRepository (TypeORM / Mongo / Prisma)
```

y el controlador seguirá funcionando sin cambios.



# 7. Flujo interno después de aplicar servicios

```
Cliente
  ↓
Controlador (DTO)
  ↓ llama →
Servicio (lógica, reglas, validaciones)
  ↓ usa →
Entidad + Mapper
  ↓
Controlador (Response DTO)
  ↓
Cliente
```

Este es el modelo MVCS aplicado correctamente en NestJS.



# 8. Endpoints disponibles

| Método | Ruta             | Descripción                |
| ------ | ---------------- | -------------------------- |
| GET    | `/api/users`     | Lista usuarios             |
| GET    | `/api/users/:id` | Obtiene usuario            |
| POST   | `/api/users`     | Crea usuario               |
| PUT    | `/api/users/:id` | Reemplaza usuario completo |
| PATCH  | `/api/users/:id` | Actualiza parcialmente     |
| DELETE | `/api/users/:id` | Elimina usuario            |



# 9. Actividad práctica

Los estudiantes deben replicar la estructura para:

```
src/products/
```

Creando:

```
controllers/
dtos/
entities/
mappers/
services/
    products.service.ts
```

Y deben:

1. Implementar los 6 endpoints REST
2. Colocar toda la lógica en `ProductsService`
3. Dejar el controlador limpio usando inyección de dependencias



# 10. Resultados y evidencias

Cada estudiante debe entregar:

### 1. Captura del `constructor` de `ProductsController`



### 2. Captura completa de

`products.service.ts`

### 3. Explicación breve:

* por qué se utiliza un servicio
* cómo funciona la inyección de dependencias
* por qué el controlador debe ser mínimo
* cómo esto beneficia al modelo MVCS

