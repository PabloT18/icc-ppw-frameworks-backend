# Programación y Plataformas Web

# **NestJS – Request Parameters en Consultas Relacionadas: Contexto Semántico y Filtrado**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 9 (NestJS): Request Parameters, Consultas Relacionadas y Optimización**

### **Autores**

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

# **1. Introducción a Request Parameters en Consultas Relacionadas**

En el tema anterior implementamos **relaciones entre entidades** usando TypeORM. Ahora, en aplicaciones reales, necesitamos **consultar y filtrar** datos relacionados de manera eficiente.

Los principales retos son:

* **¿Cómo diseñar endpoints que reflejen la semántica del dominio?**
* **¿Cuál es la diferencia entre navegación de relaciones y consultas explícitas?**
* **¿Cómo implementar filtros dinámicos con @Query()?**
* **¿Cómo mantener la separación de responsabilidades en consultas relacionadas?**

## **1.1. Contexto semántico en NestJS**

El **contexto semántico** define desde qué perspectiva se accede a un recurso relacionado en REST.

### **Principio fundamental**

**El endpoint debe reflejar la relación lógica del dominio**, no la estructura técnica de la base de datos.

### **Ejemplo práctico**

**Obtener productos de un usuario específico:**

```
✅ CORRECTO: /users/{id}/products
❌ INCORRECTO: /products?userId={id}
❌ INCORRECTO: /products/user/{id}
```

**¿Por qué `/users/{id}/products` es superior?**
* Los productos **pertenecen** al usuario
* El usuario es el **contexto principal**
* Se consulta una **subcolección** del usuario
* La relación es **clara e intuitiva**

## **1.2. Request Parameters para filtrado**

Los **@Query()** decorators permiten filtrar las consultas sin cambiar la semántica del endpoint.

### **Estructura básica**

```typescript
@Get(':id/products')
async getProducts(
  @Param('id', ParseIntPipe) id: number,
  @Query('name') name?: string,
  @Query('minPrice', new ParseFloatPipe({ optional: true })) minPrice?: number,
  @Query('maxPrice', new ParseFloatPipe({ optional: true })) maxPrice?: number,
  @Query('categoryId', new ParseIntPipe({ optional: true })) categoryId?: number,
): Promise<ProductResponseDto[]> {
  // Implementación
}
```

### **Ejemplos de uso**

```
// Todos los productos del usuario
GET /api/users/123/products

// Productos que contengan "laptop"
GET /api/users/123/products?name=laptop

// Productos en rango de precios
GET /api/users/123/products?minPrice=500&maxPrice=1500

// Combinación de filtros
GET /api/users/123/products?name=gaming&minPrice=800&categoryId=2
```

# **2. Navegación vs Consulta Explícita en NestJS**

## **2.1. Navegación de relaciones (problemática)**

**Concepto**: Acceder a datos relacionados navegando el grafo de objetos.

```typescript
// ❌ PROBLEMÁTICO - Navegación
async getProductsByUserId(userId: number): Promise<ProductResponseDto[]> {
  const user = await this.userRepository.findOne({
    where: { id: userId },
    relations: ['products'] // Carga todos los productos
  });
  
  if (!user) {
    throw new NotFoundException('User not found');
  }
  
  // Navegación problemática
  const products = user.products; // ← EVITAR
  
  return products.map(product => this.toResponseDto(product));
}
```

**Problemas de este enfoque**:
* **Carga masiva**: Se cargan TODOS los productos del usuario
* **Sin control de consulta**: No se pueden aplicar filtros eficientemente
* **Performance impredecible**: Con miles de productos es inviable
* **Memoria innecesaria**: Carga datos que podrían no usarse
* **Filtros en memoria**: Aplicar filtros después de cargar todo

## **2.2. Consulta explícita (recomendada)**

**Concepto**: Usar el repositorio correspondiente para consultas directas con TypeORM.

```typescript
// ✅ RECOMENDADO - Consulta explícita
async getProductsByUserId(userId: number): Promise<ProductResponseDto[]> {
  // 1. Validar que el usuario existe
  const userExists = await this.userRepository.findOne({ where: { id: userId } });
  if (!userExists) {
    throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
  }
  
  // 2. Consulta explícita al repositorio correcto
  const products = await this.productRepository.findByOwnerId(userId);
  
  // 3. Mapear a DTOs
  return products.map(product => this.toResponseDto(product));
}
```

**Ventajas de este enfoque**:
* **Control total**: Se especifica exactamente qué traer
* **Filtros eficientes**: Se aplican a nivel de base de datos
* **Performance predecible**: Una consulta, resultado conocido
* **Escalable**: Funciona con cualquier volumen de datos
* **Mantenible**: Lógica clara y explícita

### **Comparación práctica**

| Aspecto | Navegación | Consulta Explícita |
|---------|------------|-------------------|
| **Performance** | ⚠️ Impredecible | ✅ Controlada |
| **Escalabilidad** | ❌ Limitada | ✅ Excelente |
| **Filtros** | ❌ En memoria | ✅ En BD |
| **Mantenimiento** | ⚠️ Dependencias ocultas | ✅ Lógica explícita |
| **Testing** | ❌ Complejo | ✅ Directo |

# **3. Principio de Responsabilidad en NestJS**

## **3.1. Regla fundamental**

**El repositorio correcto es el del agregado consultado, independientemente del contexto del endpoint.**

## **3.2. Patrón de implementación**

```
@Controller
UserController.getProducts(userId, filters)
        ↓
@Injectable  
UserService.getProductsByUserId(userId, filters)
        ↓
@Injectable
ProductRepository.findByOwnerIdWithFilters(userId, filters) ← Repositorio correcto
```

**¿Por qué ProductRepository y no UserRepository?**
* Los **datos consultados son productos**
* Product es el **agregado raíz** de los datos retornados
* ProductRepository tiene **conocimiento especializado** sobre consultas de productos
* Permite **optimizaciones específicas** (índices, QueryBuilder, etc.)

# **4. Actualización de Entidades para Consultas Relacionadas**

## **4.1. User con relación bidireccional (solo para modelo)**

Archivo: `users/entities/user.entity.ts`

```typescript
import { Entity, Column, OneToMany } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';
import { Product } from '../../products/entities/product.entity';

@Entity('users')
export class User extends BaseEntity {
  @Column({ nullable: false, length: 150 })
  name: string;

  @Column({ nullable: false, unique: true, length: 150 })
  email: string;

  @Column({ nullable: false })
  password: string;

  // ================== RELACIÓN BIDIRECCIONAL ==================

  /**
   * Relación One-to-Many con Products
   * IMPORTANTE: Esta relación existe solo para consistencia del modelo
   * NO debe usarse para consultas desde el servicio
   */
  @OneToMany(() => Product, (product) => product.owner, { lazy: true })
  products: Product[];
}
```

### **¿Por qué agregar la relación si no la vamos a usar?**

**Razones**:
* **Consistencia del modelo**: Refleja la relación real en el dominio
* **Documentación**: Otros desarrolladores entienden la relación
* **TypeORM**: Facilita algunas operaciones internas del ORM
* **Flexibilidad futura**: Si eventualmente se necesita navegar (con cuidado)

**IMPORTANTE**: La relación existe a nivel de modelo, pero **NO debe usarse como mecanismo de consulta** desde los servicios.

# **5. Implementación de Request Parameters**

## **5.1. UserController - Endpoints con contexto semántico**

Archivo: `users/controllers/user.controller.ts`

```typescript
import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Body,
  Param,
  Query,
  ParseIntPipe,
  ParseFloatPipe,
  ValidationPipe,
  HttpStatus,
  HttpCode,
} from '@nestjs/common';
import { UserService } from '../services/user.service';
import { CreateUserDto } from '../dto/create-user.dto';
import { UpdateUserDto } from '../dto/update-user.dto';
import { UserResponseDto } from '../dto/user-response.dto';
import { ProductResponseDto } from '../../products/dto/product-response.dto';

@Controller('api/users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  // ============== ENDPOINT BÁSICO: PRODUCTOS DE USUARIO ==============

  /**
   * Obtiene todos los productos de un usuario específico
   * Ejemplo: GET /api/users/123/products
   */
  @Get(':id/products')
  async getProducts(
    @Param('id', ParseIntPipe) id: number,
  ): Promise<ProductResponseDto[]> {
    return this.userService.getProductsByUserId(id);
  }

  // ============== ENDPOINT AVANZADO: PRODUCTOS CON FILTROS ==============

  /**
   * Obtiene productos de un usuario con filtros opcionales
   * Ejemplo: GET /api/users/5/products-v2?name=laptop&minPrice=500&maxPrice=2000&categoryId=3
   */
  @Get(':id/products-v2')
  async getProductsWithFilters(
    @Param('id', ParseIntPipe) id: number,
    @Query('name') name?: string,
    @Query('minPrice', new ParseFloatPipe({ optional: true })) minPrice?: number,
    @Query('maxPrice', new ParseFloatPipe({ optional: true })) maxPrice?: number,
    @Query('categoryId', new ParseIntPipe({ optional: true })) categoryId?: number,
  ): Promise<ProductResponseDto[]> {
    return this.userService.getProductsByUserIdWithFilters(
      id, 
      name, 
      minPrice, 
      maxPrice, 
      categoryId
    );
  }

  // ============== OTROS ENDPOINTS EXISTENTES ==============
  
  @Post()
  @HttpCode(HttpStatus.CREATED)
  async create(
    @Body(ValidationPipe) createUserDto: CreateUserDto,
  ): Promise<UserResponseDto> {
    return this.userService.create(createUserDto);
  }

  @Get()
  async findAll(): Promise<UserResponseDto[]> {
    return this.userService.findAll();
  }

  @Get(':id')
  async findById(
    @Param('id', ParseIntPipe) id: number,
  ): Promise<UserResponseDto> {
    return this.userService.findById(id);
  }

  @Put(':id')
  async update(
    @Param('id', ParseIntPipe) id: number,
    @Body(ValidationPipe) updateUserDto: UpdateUserDto,
  ): Promise<UserResponseDto> {
    return this.userService.update(id, updateUserDto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  async delete(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return this.userService.delete(id);
  }
}
```

### **Aspectos clave del controlador**

1. **Contexto semántico claro**: Los endpoints están bajo `/users/{id}/` porque el contexto es el usuario
2. **Pipes de validación**: `ParseIntPipe`, `ParseFloatPipe` con `optional: true` para filtros
3. **Separación de responsabilidades**: El controlador solo expone endpoints, delega al servicio
4. **Convenciones REST**: Se mantiene la semántica REST correcta

## **5.2. Validación avanzada con DTOs**

Para validaciones más robustas, se puede usar un DTO de filtros:

Archivo: `users/dto/product-filter.dto.ts`

```typescript
import {
  IsOptional,
  IsString,
  IsNumber,
  IsPositive,
  Min,
  Max,
  Length,
  ValidateIf,
} from 'class-validator';
import { Transform, Type } from 'class-transformer';

export class ProductFilterDto {
  @IsOptional()
  @IsString()
  @Length(2, 100, { message: 'El nombre debe tener entre 2 y 100 caracteres' })
  name?: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El precio mínimo debe ser un número válido' })
  @Min(0, { message: 'El precio mínimo debe ser mayor o igual a 0' })
  minPrice?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El precio máximo debe ser un número válido' })
  @Min(0, { message: 'El precio máximo debe ser mayor o igual a 0' })
  @ValidateIf(o => o.minPrice !== undefined)
  @Min(0, { message: 'El precio máximo debe ser mayor o igual al precio mínimo' })
  maxPrice?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El ID de categoría debe ser un número válido' })
  @IsPositive({ message: 'El ID de categoría debe ser positivo' })
  categoryId?: number;

  // ============== VALIDACIONES PERSONALIZADAS ==============

  /**
   * Valida que maxPrice sea mayor o igual a minPrice
   */
  @ValidateIf(o => o.minPrice !== undefined && o.maxPrice !== undefined)
  validatePriceRange(): boolean {
    if (this.minPrice !== undefined && this.maxPrice !== undefined) {
      return this.maxPrice >= this.minPrice;
    }
    return true;
  }
}
```

### **Controlador alternativo con DTO de filtros**

```typescript
@Get(':id/products-v3')
async getProductsWithFiltersDto(
  @Param('id', ParseIntPipe) id: number,
  @Query(ValidationPipe) filters: ProductFilterDto,
): Promise<ProductResponseDto[]> {
  
  // Validación adicional de negocio si es necesario
  if (!filters.validatePriceRange()) {
    throw new BadRequestException('El precio máximo debe ser mayor o igual al precio mínimo');
  }
  
  return this.userService.getProductsByUserIdWithFilters(
    id, 
    filters.name, 
    filters.minPrice, 
    filters.maxPrice, 
    filters.categoryId
  );
}
```

# **6. Implementación del UserService**

## **6.1. Actualización del UserService con consultas relacionadas**

Archivo: `users/services/user.service.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { UserRepository } from '../repositories/user.repository';
import { ProductRepository } from '../../products/repositories/product.repository';
import { CreateUserDto } from '../dto/create-user.dto';
import { UpdateUserDto } from '../dto/update-user.dto';
import { UserResponseDto } from '../dto/user-response.dto';
import { ProductResponseDto } from '../../products/dto/product-response.dto';
import { NotFoundException } from '../../../exceptions/domain/not-found.exception';
import { BadRequestException } from '../../../exceptions/domain/bad-request.exception';

@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly productRepository: ProductRepository, // ← Inyección del repositorio correcto
  ) {}

  // ============== MÉTODOS BÁSICOS EXISTENTES ==============
  
  async create(createUserDto: CreateUserDto): Promise<UserResponseDto> {
    // Implementación existente...
    // (código ya implementado en temas anteriores)
  }

  async findAll(): Promise<UserResponseDto[]> {
    // Implementación existente...
  }

  async findById(id: number): Promise<UserResponseDto> {
    // Implementación existente...
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<UserResponseDto> {
    // Implementación existente...
  }

  async delete(id: number): Promise<void> {
    // Implementación existente...
  }

  // ============== NUEVOS MÉTODOS PARA CONSULTAS RELACIONADAS ==============

  async getProductsByUserId(userId: number): Promise<ProductResponseDto[]> {
    // 1. Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // 2. Consulta explícita al repositorio correcto
    const products = await this.productRepository.findByOwnerId(userId);
    
    // 3. Mapear a DTOs
    return products.map(product => this.toProductResponseDto(product));
  }

  async getProductsByUserIdWithFilters(
    userId: number,
    name?: string,
    minPrice?: number,
    maxPrice?: number,
    categoryId?: number,
  ): Promise<ProductResponseDto[]> {
    
    // 1. Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // 2. Validaciones de filtros
    if (minPrice !== undefined && minPrice < 0) {
      throw new BadRequestException('El precio mínimo no puede ser negativo');
    }
    
    if (maxPrice !== undefined && maxPrice < 0) {
      throw new BadRequestException('El precio máximo no puede ser negativo');
    }
    
    if (minPrice !== undefined && maxPrice !== undefined && maxPrice < minPrice) {
      throw new BadRequestException('El precio máximo debe ser mayor o igual al precio mínimo');
    }
    
    // 3. Consulta con filtros al repositorio correcto
    const products = await this.productRepository.findByOwnerIdWithFilters(
      userId, 
      name, 
      minPrice, 
      maxPrice, 
      categoryId
    );
    
    // 4. Mapear a DTOs
    return products.map(product => this.toProductResponseDto(product));
  }

  // ============== MÉTODO HELPER ==============

  /**
   * Convierte Product a ProductResponseDto
   * NOTA: Este método podría estar en un mapper separado para mejor organización
   */
  private toProductResponseDto(product: any): ProductResponseDto {
    const dto = new ProductResponseDto();
    
    dto.id = product.id;
    dto.name = product.name;
    dto.price = product.price;
    dto.description = product.description;
    dto.createdAt = product.createdAt;
    dto.updatedAt = product.updatedAt;
    
    // Información del usuario (owner)
    dto.user = new ProductResponseDto.UserSummaryDto();
    dto.user.id = product.owner.id;
    dto.user.name = product.owner.name;
    dto.user.email = product.owner.email;
    
    // Información de la categoría
    dto.category = new ProductResponseDto.CategoryResponseDto();
    dto.category.id = product.category.id;
    dto.category.name = product.category.name;
    dto.category.description = product.category.description;
    
    return dto;
  }
}
```

### **Aspectos clave del servicio**

1. **Inyección correcta**: Se inyecta `ProductRepository` porque los datos consultados son productos
2. **Validación proactiva**: Se valida que el usuario exista antes de consultar
3. **Consulta explícita**: Se usa `productRepository.findByOwnerId()` en lugar de navegar relaciones
4. **Validaciones de negocio**: Se validan los filtros antes de aplicarlos
5. **Separación de responsabilidades**: El servicio orquesta, el repositorio consulta

# **7. Actualización del ProductRepository**

## **7.1. ProductRepository con consultas especializadas**

Archivo: `products/repositories/product.repository.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Product } from '../entities/product.entity';

@Injectable()
export class ProductRepository {
  constructor(
    @InjectRepository(Product)
    private readonly repository: Repository<Product>,
  ) {}

  // ============== CONSULTAS BÁSICAS DE RELACIONES (ya implementadas) ==============
  
  async findByOwnerId(userId: number): Promise<Product[]> {
    return this.repository.find({
      where: { owner: { id: userId } },
      relations: ['owner', 'category'],
    });
  }

  async findByCategoryId(categoryId: number): Promise<Product[]> {
    return this.repository.find({
      where: { category: { id: categoryId } },
      relations: ['owner', 'category'],
    });
  }

  async findByOwnerName(ownerName: string): Promise<Product[]> {
    return this.repository
      .createQueryBuilder('product')
      .innerJoinAndSelect('product.owner', 'owner')
      .innerJoinAndSelect('product.category', 'category')
      .where('owner.name ILIKE :name', { name: `%${ownerName}%` })
      .getMany();
  }

  async findByCategoryName(categoryName: string): Promise<Product[]> {
    return this.repository
      .createQueryBuilder('product')
      .innerJoinAndSelect('product.owner', 'owner')
      .innerJoinAndSelect('product.category', 'category')
      .where('category.name ILIKE :name', { name: `%${categoryName}%` })
      .getMany();
  }

  // ============== NUEVA CONSULTA CON FILTROS DINÁMICOS ==============

  /**
   * Encuentra productos de un usuario con filtros opcionales
   * Usa QueryBuilder para manejar filtros dinámicos
   */
  async findByOwnerIdWithFilters(
    userId: number,
    name?: string,
    minPrice?: number,
    maxPrice?: number,
    categoryId?: number,
  ): Promise<Product[]> {
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .innerJoinAndSelect('product.owner', 'owner')
      .innerJoinAndSelect('product.category', 'category')
      .where('owner.id = :userId', { userId });

    // Filtro por nombre (búsqueda parcial, insensible a mayúsculas)
    if (name) {
      queryBuilder.andWhere('LOWER(product.name) LIKE LOWER(:name)', { 
        name: `%${name}%` 
      });
    }

    // Filtro por precio mínimo
    if (minPrice !== undefined) {
      queryBuilder.andWhere('product.price >= :minPrice', { minPrice });
    }

    // Filtro por precio máximo
    if (maxPrice !== undefined) {
      queryBuilder.andWhere('product.price <= :maxPrice', { maxPrice });
    }

    // Filtro por categoría
    if (categoryId !== undefined) {
      queryBuilder.andWhere('category.id = :categoryId', { categoryId });
    }

    // Ordenar por fecha de creación (más recientes primero)
    queryBuilder.orderBy('product.createdAt', 'DESC');

    return queryBuilder.getMany();
  }

  // ============== MÉTODOS BÁSICOS EXISTENTES ==============

  async findById(id: number): Promise<Product | null> {
    return this.repository.findOne({
      where: { id },
      relations: ['owner', 'category'],
    });
  }

  async save(product: Partial<Product>): Promise<Product> {
    return this.repository.save(product);
  }

  async delete(id: number): Promise<void> {
    await this.repository.delete(id);
  }
}
```

### **Explicación del QueryBuilder**

```sql
-- SQL generado aproximadamente:
SELECT 
    product.*, 
    owner.id as owner_id, owner.name as owner_name, owner.email as owner_email,
    category.id as category_id, category.name as category_name, category.description as category_description
FROM products product 
INNER JOIN users owner ON product.user_id = owner.id 
INNER JOIN categories category ON product.category_id = category.id
WHERE owner.id = $1 
  AND ($2::text IS NULL OR LOWER(product.name) LIKE LOWER($2))
  AND ($3::numeric IS NULL OR product.price >= $3)
  AND ($4::numeric IS NULL OR product.price <= $4)
  AND ($5::integer IS NULL OR category.id = $5)
ORDER BY product.created_at DESC
```

**Ventajas de este enfoque**:
* **Filtros opcionales**: Si un parámetro es `undefined`, no se aplica el filtro
* **Performance**: Filtros aplicados en base de datos con QueryBuilder
* **Flexibilidad**: Se pueden combinar filtros de forma dinámica
* **Búsqueda parcial**: `LIKE` permite buscar por nombre parcial
* **Case-insensitive**: `LOWER()` hace la búsqueda insensible a mayúsculas
* **Type-safe**: TypeORM QueryBuilder es completamente tipado

## **7.2. Alternativa con QueryBuilder más avanzado**

Para casos más complejos, se puede crear un QueryBuilder helper:

```typescript
// Clase helper para QueryBuilder dinámico
export class ProductQueryBuilder {
  private queryBuilder: SelectQueryBuilder<Product>;

  constructor(private repository: Repository<Product>) {
    this.queryBuilder = this.repository
      .createQueryBuilder('product')
      .innerJoinAndSelect('product.owner', 'owner')
      .innerJoinAndSelect('product.category', 'category');
  }

  whereOwner(userId: number): ProductQueryBuilder {
    this.queryBuilder.where('owner.id = :userId', { userId });
    return this;
  }

  whereName(name?: string): ProductQueryBuilder {
    if (name) {
      this.queryBuilder.andWhere('LOWER(product.name) LIKE LOWER(:name)', { 
        name: `%${name}%` 
      });
    }
    return this;
  }

  wherePriceRange(minPrice?: number, maxPrice?: number): ProductQueryBuilder {
    if (minPrice !== undefined) {
      this.queryBuilder.andWhere('product.price >= :minPrice', { minPrice });
    }
    if (maxPrice !== undefined) {
      this.queryBuilder.andWhere('product.price <= :maxPrice', { maxPrice });
    }
    return this;
  }

  whereCategory(categoryId?: number): ProductQueryBuilder {
    if (categoryId !== undefined) {
      this.queryBuilder.andWhere('category.id = :categoryId', { categoryId });
    }
    return this;
  }

  orderByCreated(order: 'ASC' | 'DESC' = 'DESC'): ProductQueryBuilder {
    this.queryBuilder.orderBy('product.createdAt', order);
    return this;
  }

  async getMany(): Promise<Product[]> {
    return this.queryBuilder.getMany();
  }
}
```

### **Uso del QueryBuilder helper**

```typescript
async findByOwnerIdWithFilters(
  userId: number,
  name?: string,
  minPrice?: number,
  maxPrice?: number,
  categoryId?: number,
): Promise<Product[]> {
  return new ProductQueryBuilder(this.repository)
    .whereOwner(userId)
    .whereName(name)
    .wherePriceRange(minPrice, maxPrice)
    .whereCategory(categoryId)
    .orderByCreated('DESC')
    .getMany();
}
```


# **8. Configuración del Módulo User**

Para que todo funcione correctamente, el módulo debe importar todas las dependencias:

Archivo: `users/user.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserController } from './controllers/user.controller';
import { UserService } from './services/user.service';
import { UserRepository } from './repositories/user.repository';
import { User } from './entities/user.entity';

// Importar entidades relacionadas
import { Product } from '../products/entities/product.entity';

// Importar repositorios de dependencias
import { ProductRepository } from '../products/repositories/product.repository';

@Module({
  imports: [
    TypeOrmModule.forFeature([User, Product]), // Registrar ambas entidades
  ],
  controllers: [UserController],
  providers: [
    UserService,
    UserRepository,
    ProductRepository, // Inyectar repositorio de productos
  ],
  exports: [UserService, UserRepository],
})
export class UserModule {}
```

# **9. Actividad Práctica Completa**

## **9.1. Implementación requerida**

El estudiante debe implementar:

1. **Actualizar User entity** con relación `@OneToMany` hacia productos
2. **Implementar endpoints** en `UserController`:
   - `GET /api/users/{id}/products` (básico)
   - `GET /api/users/{id}/products-v2` (con filtros)
3. **Implementar métodos** en `UserService`:
   - `getProductsByUserId(userId: number)`
   - `getProductsByUserIdWithFilters(userId, name, minPrice, maxPrice, categoryId)`
4. **Crear consulta personalizada** en `ProductRepository`:
   - `findByOwnerIdWithFilters()` usando TypeORM QueryBuilder
5. **Escribir tests** unitarios e integración

## **9.2. Casos de prueba específicos**

**Probar los siguientes casos**:

```bash
# 1. Productos de usuario existente
GET /api/users/1/products

# 2. Productos con filtro de nombre
GET /api/users/1/products-v2?name=laptop

# 3. Productos en rango de precio
GET /api/users/1/products-v2?minPrice=500&maxPrice=1500

# 4. Productos por categoría
GET /api/users/1/products-v2?categoryId=2

# 5. Filtros combinados
GET /api/users/1/products-v2?name=gaming&minPrice=800&categoryId=2

# 6. Usuario inexistente (debe retornar 404)
GET /api/users/999/products

# 7. Rango de precios inválido (debe retornar 400)
GET /api/users/1/products-v2?minPrice=1500&maxPrice=500
```

## **9.3. Verificaciones técnicas**

1. **SQL generado**: Verificar en logs que se generen consultas eficientes con QueryBuilder
2. **Lazy loading**: Confirmar que NO se use navegación de relaciones directas
3. **Validaciones**: Probar casos de error (usuario inexistente, filtros inválidos)
4. **Performance**: Medir tiempos de respuesta con datasets grandes

# **10. Resultados y Evidencias Requeridas**

## **10.1. Evidencias de implementación**
1. **Captura de user.entity.ts** con relación `@OneToMany` agregada
2. **Captura de user.controller.ts** con ambos endpoints implementados
3. **Captura de user.service.ts** con métodos de consulta relacionada
4. **Captura de product.repository.ts** con consulta QueryBuilder personalizada

## **10.2. Evidencias de funcionamiento**
1. **Request básico**: `GET /api/users/1/products` con respuesta exitosa
2. **Request con filtros**: `GET /api/users/1/products-v2?name=laptop&minPrice=500` con productos filtrados
3. **Request combinado**: `GET /api/users/1/products-v2?name=gaming&categoryId=2` mostrando múltiples filtros
4. **Error handling**: `GET /api/users/999/products` mostrando error 404

## **10.3. Evidencias técnicas**
1. **SQL queries**: Captura de logs mostrando SQL generado por QueryBuilder con filtros
2. **Tests unitarios**: Capturas de tests pasando para ambos métodos del servicio
3. **Validation**: Captura de error 400 con filtros inválidos (ej: minPrice > maxPrice)

## **10.4. Datos para revisión**

**Usar los productos creados en el tema anterior**:
- Usuario 1 con productos: "Laptop Gaming", "Mouse Inalámbrico", "Monitor 4K"
- Usuario 2 con productos: "Teclado Mecánico", "Libro TypeScript"
- Categorías: "Electrónicos", "Gaming", "Oficina", "Libros"

**Consultas de prueba**:
1. Todos los productos del usuario 1
2. Productos del usuario 1 que contengan "gaming"
3. Productos del usuario 1 entre $500 y $1500
4. Productos del usuario 1 de categoría "Electrónicos"
5. Combinación: productos "gaming" + precio > $800 + categoría "Gaming"

# **11. Conclusiones**

Esta implementación en NestJS demuestra:

* **Contexto semántico correcto**: `/users/{id}/products` refleja la relación del dominio
* **Separación de responsabilidades**: UserController → UserService → ProductRepository
* **Consultas explícitas**: Uso directo de TypeORM QueryBuilder 
* **Filtrado eficiente**: @Query() parameters aplicados en base de datos
* **Escalabilidad**: Solución que funciona con grandes volúmenes de datos
* **Mantenibilidad**: Código claro, testeable y extensible
* **Type-safety**: Completamente tipado con TypeScript

