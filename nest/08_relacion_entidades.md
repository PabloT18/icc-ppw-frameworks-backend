# Programación y Plataformas Web

# **NestJS – Relaciones entre Entidades TypeORM: Mapeo de Asociaciones 1:N y N:N**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 8 (NestJS): Relaciones TypeORM, Estrategias de Carga y Mapeo Objeto-Relacional**

### **Autores**

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

# **1. Introducción a las Relaciones en TypeORM**

En aplicaciones reales, las entidades **NO** son independientes. Existe información relacionada que debe ser mapeada correctamente entre el modelo orientado a objetos y el modelo relacional.

En NestJS, **TypeORM** proporciona un sistema robusto para manejar relaciones entre entidades, similar a JPA pero con la flexibilidad de TypeScript.

## **1.1. ¿Por qué son importantes las relaciones?**

* **Normalización**: Evita duplicación de datos
* **Integridad referencial**: Mantiene consistencia entre tablas
* **Consultas eficientes**: Permite JOINs optimizados con QueryBuilder
* **Dominio expresivo**: El código TypeScript refleja la realidad del negocio

## **1.2. Tipos de relaciones en TypeORM**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `@OneToOne` | 1 entidad → 1 entidad | Usuario ↔ Perfil |
| `@OneToMany` | 1 entidad → N entidades | Usuario → Productos |
| `@ManyToOne` | N entidades → 1 entidad | Productos → Usuario |
| `@ManyToMany` | N entidades ↔ N entidades | Productos ↔ Categorías |

## **1.3. Escenario de este tema**

Trabajaremos con un dominio de **e-commerce básico**:

### **Fase 1: Relaciones 1:N (One-to-Many)**
```
User 1 ──── N Product    (Un usuario puede crear muchos productos)
Category 1 ──── N Product (Una categoría puede tener muchos productos)
```

### **Fase 2: Relaciones N:N (Many-to-Many)**
```
Product N ──── N Category (Un producto puede tener múltiples categorías)
```

### **Evolución del dominio**

1. **Fase inicial**: Producto con una sola categoría
2. **Fase dos**: Producto con múltiples categorías (tags, clasificaciones)

# **2. Preparación: Entidades Base Actualizadas**

Antes de implementar relaciones, necesitamos actualizar nuestras entidades base.

## **2.1. Entidad User (sin relación bidireccional)**

Archivo: `users/entities/user.entity.ts`

```typescript
import { Entity, Column } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';

@Entity('users')
export class User extends BaseEntity {
  @Column({ nullable: false, length: 150 })
  name: string;

  @Column({ nullable: false, unique: true, length: 150 })
  email: string;

  @Column({ nullable: false })
  password: string;
}
```

### **¿Por qué NO se agrega `@OneToMany` en User?**

**Decisión de diseño**: Mantenemos la entidad `User` simple sin conocer directamente sus productos.

**Ventajas**:
* **Menor acoplamiento**: User no depende de Product
* **Rendimiento**: Se evita carga de colecciones innecesarias
* **Simplicidad**: Menos complejidad en la entidad
* **Consultas específicas**: Se consultan productos por user_id cuando sea necesario

**Alternativa bidireccional** (no recomendada para este caso):
```typescript
// NO implementar - solo ejemplo 
@OneToMany(() => Product, (product) => product.owner, { lazy: true })
products: Product[];
```

## **2.2. Entidad Category (preparada para escalarla)**

Archivo: `categories/entities/category.entity.ts`

```typescript
import { Entity, Column } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';

@Entity('categories')
export class Category extends BaseEntity {
  @Column({ nullable: false, unique: true, length: 120 })
  name: string;

  @Column({ length: 500, nullable: true })
  description: string;
}
```

**Nota**: Esta entidad se mantendrá simple inicialmente, pero evolucionará para soportar relaciones N:N más adelante.

# **3. FASE 1: Relaciones 1:N - Product con Asociaciones**

La entidad `Product` es el **propietario** de las relaciones. Aquí se define cómo se conecta con `User` y `Category`.

Archivo: `products/entities/product.entity.ts`

```typescript
import { Entity, Column, ManyToOne, JoinColumn } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';
import { User } from '../../users/entities/user.entity';
import { Category } from '../../categories/entities/category.entity';

@Entity('products')
export class Product extends BaseEntity {
  @Column({ nullable: false, length: 150 })
  name: string;

  @Column({ nullable: false, type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @Column({ length: 500, nullable: true })
  description: string;

  // ================== RELACIONES 1:N ==================

  /**
   * Relación Many-to-One con User
   * Un producto pertenece a un usuario (owner)
   * Muchos productos pueden pertenecer al mismo usuario
   */
  @ManyToOne(() => User, { nullable: false, eager: false })
  @JoinColumn({ name: 'user_id' })
  owner: User;

  /**
   * Relación Many-to-One con Category  
   * Un producto pertenece a una categoría
   * Muchos productos pueden pertenecer a la misma categoría
   */
  @ManyToOne(() => Category, { nullable: false, eager: false })
  @JoinColumn({ name: 'category_id' })
  category: Category;
}
```

## **3.1. Explicación detallada de las anotaciones**

### **@ManyToOne**
```typescript
@ManyToOne(() => User, { nullable: false, eager: false })
```

**Parámetros**:
* **función flecha**: Define la entidad relacionada de forma lazy (evita referencias circulares)
* **nullable: false**: La relación es **obligatoria**. No puede existir un producto sin user y sin category
* **eager: false**: La entidad relacionada se carga **bajo demanda**, no automáticamente

### **@JoinColumn**
```typescript
@JoinColumn({ name: 'user_id' })
```

**Función**: Define la **Foreign Key** en la tabla `products`
* **name: 'user_id'**: Nombre de la columna FK en PostgreSQL
* TypeORM automáticamente hace la FK NOT NULL si nullable: false

### **Resultado en PostgreSQL**

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Foreign Keys generadas por TypeORM
    user_id INTEGER NOT NULL REFERENCES users(id),
    category_id INTEGER NOT NULL REFERENCES categories(id)
);
```

# **4. Estrategias de Carga: eager vs lazy**

## **4.1. ¿Qué es el Loading Strategy?**

Determina **cuándo** se cargan las entidades relacionadas desde la base de datos.

### **eager: false (Carga Perezosa) - RECOMENDADO**

```typescript
@ManyToOne(() => User, { eager: false })
owner: User;
```

**Comportamiento**:
* La entidad `User` **NO** se carga automáticamente
* Se carga solo cuando se accede a ella o se especifica en consultas
* Genera consulta SQL adicional o JOIN explícito

**Ventajas**:
* **Performance inicial**: Consulta más rápida
* **Memoria eficiente**: No carga datos innecesarios
* **Escalabilidad**: Funciona bien con grandes volúmenes

### **eager: true (Carga Inmediata) - USAR CON CUIDADO**

```typescript
@ManyToOne(() => User, { eager: true })
owner: User;
```

**Comportamiento**:
* `User` se carga automáticamente con `Product`
* Una sola consulta con JOIN
* Datos disponibles inmediatamente

**Desventajas**:
* **N+1 Problem**: Puede generar muchas consultas innecesarias
* **Memoria**: Carga datos que tal vez no se usen
* **Performance**: Consultas más pesadas

## **4.2. Ejemplo práctico de carga lazy**

```typescript
@Injectable()
export class ProductService {
  constructor(
    @InjectRepository(Product)
    private productRepository: Repository<Product>,
  ) {}

  async findById(id: number): Promise<ProductResponseDto> {
    // Sin relaciones cargadas
    const product = await this.productRepository.findOne({
      where: { id },
      relations: ['owner', 'category'], // Carga explícita
    });

    if (!product) {
      throw new NotFoundException(`Producto no encontrado con ID: ${id}`);
    }
    
    return this.toResponseDto(product);
  }
}
```

## **4.3. ¿Cuándo usar cada estrategia?**

| Escenario | Usar lazy (eager: false) | Usar eager (eager: true) |
|-----------|-----------|------------|
| Relación siempre necesaria | ❌ | ✅ Considerar |
| Relación opcional en uso | ✅ SÍ | ❌ |
| Listados con muchos elementos | ✅ SÍ | ❌ |
| Operaciones batch/masivas | ✅ SÍ | ❌ |
| APIs REST (DTOs) | ✅ SÍ | ❌ |

**Recomendación general**: Usar **lazy por defecto** y optimizar casos específicos con consultas personalizadas usando `relations`.

# **5. Repositorios con Consultas Relacionales**

Los repositorios deben incluir consultas que aprovechen las relaciones definidas.

## **5.1. UserRepository (sin cambios)**

Archivo: `users/repositories/user.repository.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from '../entities/user.entity';

@Injectable()
export class UserRepository {
  constructor(
    @InjectRepository(User)
    private readonly repository: Repository<User>,
  ) {}

  async findByEmail(email: string): Promise<User | null> {
    return this.repository.findOne({ where: { email } });
  }

  async findById(id: number): Promise<User | null> {
    return this.repository.findOne({ where: { id } });
  }

  async save(user: Partial<User>): Promise<User> {
    return this.repository.save(user);
  }
}
```

## **5.2. CategoryRepository**

Archivo: `categories/repositories/category.repository.ts`

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Category } from '../entities/category.entity';

@Injectable()
export class CategoryRepository {
  constructor(
    @InjectRepository(Category)
    private readonly repository: Repository<Category>,
  ) {}

  /**
   * Verifica si ya existe una categoría con ese nombre
   * @param name - Nombre de la categoría
   */
  async existsByName(name: string): Promise<boolean> {
    const count = await this.repository.count({ where: { name } });
    return count > 0;
  }

  /**
   * Busca categoría por nombre (case insensitive)
   */
  async findByName(name: string): Promise<Category | null> {
    return this.repository
      .createQueryBuilder('category')
      .where('LOWER(category.name) = LOWER(:name)', { name })
      .getOne();
  }

  async findById(id: number): Promise<Category | null> {
    return this.repository.findOne({ where: { id } });
  }

  async save(category: Partial<Category>): Promise<Category> {
    return this.repository.save(category);
  }
}
```

## **5.3. ProductRepository - Consultas con Relaciones**

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

  /**
   * Encuentra todos los productos de un usuario específico
   * @param userId - ID del usuario
   */
  async findByOwnerId(userId: number): Promise<Product[]> {
    return this.repository.find({
      where: { owner: { id: userId } },
      relations: ['owner', 'category'],
    });
  }

  /**
   * Encuentra todos los productos de una categoría específica
   * @param categoryId - ID de la categoría
   */
  async findByCategoryId(categoryId: number): Promise<Product[]> {
    return this.repository.find({
      where: { category: { id: categoryId } },
      relations: ['owner', 'category'],
    });
  }

  /**
   * Encuentra productos por nombre de usuario usando QueryBuilder
   * @param ownerName - Nombre del usuario
   */
  async findByOwnerName(ownerName: string): Promise<Product[]> {
    return this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('owner.name ILIKE :name', { name: `%${ownerName}%` })
      .getMany();
  }

  /**
   * Encuentra productos por nombre de categoría
   * @param categoryName - Nombre de la categoría
   */
  async findByCategoryName(categoryName: string): Promise<Product[]> {
    return this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('category.name ILIKE :name', { name: `%${categoryName}%` })
      .getMany();
  }

  /**
   * Encuentra productos con precio mayor a X de una categoría específica
   * @param categoryId - ID de la categoría
   * @param minPrice - Precio mínimo
   */
  async findByCategoryAndPriceGreaterThan(
    categoryId: number,
    minPrice: number,
  ): Promise<Product[]> {
    return this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('product.category.id = :categoryId', { categoryId })
      .andWhere('product.price > :minPrice', { minPrice })
      .getMany();
  }

  async findById(id: number): Promise<Product | null> {
    return this.repository.findOne({
      where: { id },
      relations: ['owner', 'category'],
    });
  }

  async findAll(): Promise<Product[]> {
    return this.repository.find({
      relations: ['owner', 'category'],
    });
  }

  async save(product: Partial<Product>): Promise<Product> {
    return this.repository.save(product);
  }

  async remove(product: Product): Promise<void> {
    await this.repository.remove(product);
  }
}
```

### **Ventajas de TypeORM QueryBuilder y Repository**

* **QueryBuilder**: Permite consultas SQL complejas de forma type-safe
* **Relations**: Especifica qué relaciones cargar automáticamente
* **Type-safe**: Verificación en tiempo de compilación
* **Legible**: El código describe claramente la consulta
* **Optimizado**: TypeORM genera SQL eficiente

# **6. DTOs Actualizados para Relaciones**

Los DTOs deben incluir información de las entidades relacionadas.

## **6.1. CreateProductDto**

Archivo: `products/dto/create-product.dto.ts`

```typescript
import {
  IsNotEmpty,
  IsNumber,
  IsPositive,
  IsString,
  Length,
  IsOptional,
} from 'class-validator';

export class CreateProductDto {
  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @IsString({ message: 'El nombre debe ser un texto' })
  @Length(3, 150, { message: 'El nombre debe tener entre 3 y 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El precio es obligatorio' })
  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'El precio debe ser un número válido' })
  @IsPositive({ message: 'El precio debe ser mayor a 0' })
  price: number;

  @IsOptional()
  @IsString({ message: 'La descripción debe ser un texto' })
  @Length(0, 500, { message: 'La descripción no puede superar 500 caracteres' })
  description?: string;

  // ============== RELACIONES ==============

  @IsNotEmpty({ message: 'El ID del usuario es obligatorio' })
  @IsNumber({}, { message: 'El ID del usuario debe ser un número' })
  @IsPositive({ message: 'El ID del usuario debe ser mayor a 0' })
  userId: number;

  @IsNotEmpty({ message: 'El ID de la categoría es obligatorio' })
  @IsNumber({}, { message: 'El ID de la categoría debe ser un número' })
  @IsPositive({ message: 'El ID de la categoría debe ser mayor a 0' })
  categoryId: number;
}
```

## **6.2. ProductResponseDto - Estructura Anidada vs Plana**

### **Opción 1: Estructura Anidada (RECOMENDADA)**

En esta opción se pueden crear DTOs específicos para los modelos relacionados, o se puede usar los DTOs de cada modelo específico, 
es decir, `UserResponseDto` y `CategoryResponseDto`, pero para simplicidad se crean DTOs internos simples como `UserSummaryDto` y `CategorySummaryDto`.

Archivo: `products/dto/product-response.dto.ts`

```typescript
export class ProductResponseDto {
  id: number;
  name: string;
  price: number;
  description: string;

  // ============== OBJETOS ANIDADOS ==============
  
  user: UserSummaryDto;
  category: CategoryResponseDto;

  // ============== AUDITORÍA ==============
  
  createdAt: Date;
  updatedAt: Date;

  // ============== DTOs INTERNOS ==============
  
  static UserSummaryDto = class {
    id: number;
    name: string;
    email: string;
  };

  static CategoryResponseDto = class {
    id: number;
    name: string;
    description: string;
  };
}

// Para facilitar el uso, exportamos los tipos internos
export type UserSummaryDto = InstanceType<typeof ProductResponseDto.UserSummaryDto>;
export type CategoryResponseDto = InstanceType<typeof ProductResponseDto.CategoryResponseDto>;
```

**Respuesta JSON resultante:**
```json
{
  "id": 1,
  "name": "Laptop Gaming",
  "price": 1200.00,
  "description": "Laptop de alto rendimiento",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@email.com"
  },
  "category": {
    "id": 2,
    "name": "Electrónicos",
    "description": "Dispositivos electrónicos"
  },
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

### **Opción 2: Estructura Plana (alternativa)**

```typescript
export class ProductResponseDto {
  id: number;
  name: string;
  price: number;
  description: string;

  // ============== INFORMACIÓN PLANA ==============
  
  userId: number;
  userName: string;
  userEmail: string;
  
  categoryId: number;
  categoryName: string;
  categoryDescription: string;

  createdAt: Date;
  updatedAt: Date;
}
```

**Respuesta JSON resultante:**
```json
{
  "id": 1,
  "name": "Laptop Gaming",
  "price": 1200.00,
  "description": "Laptop de alto rendimiento",
  "userId": 1,
  "userName": "Juan Pérez",
  "userEmail": "juan@email.com",
  "categoryId": 2,
  "categoryName": "Electrónicos",
  "categoryDescription": "Dispositivos electrónicos",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

### **Comparación de enfoques**

| Aspecto | Estructura Anidada | Estructura Plana |
|---------|-------------------|------------------|
| **Semántica** | ✅ Clara y expresiva | ⚠️ Confusa con muchos campos |
| **Legibilidad** | ✅ Fácil de entender | ❌ Difícil con muchas relaciones |
| **Frontend** | ✅ `product.user.name` | ❌ `product.userName` |
| **Reutilización** | ✅ DTOs internos reutilizables | ❌ Duplicación |
| **Escalabilidad** | ✅ Fácil agregar campos | ⚠️ Contamina DTO principal |
| **Tipado** | ✅ Fuertemente tipado | ⚠️ Propenso a errores |

### **Recomendación: Estructura Anidada**

Para este tema usaremos la **estructura anidada** porque:
* Es más **expresiva** del dominio
* Facilita el trabajo del **frontend**
* Es una **mejor práctica** en APIs modernas
* Prepara para **futuras extensiones**

## **6.3. UpdateProductDto**

Archivo: `products/dto/update-product.dto.ts`

```typescript
import {
  IsNotEmpty,
  IsNumber,
  IsPositive,
  IsString,
  Length,
  IsOptional,
} from 'class-validator';

export class UpdateProductDto {
  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @IsString({ message: 'El nombre debe ser un texto' })
  @Length(3, 150, { message: 'El nombre debe tener entre 3 y 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El precio es obligatorio' })
  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'El precio debe ser un número válido' })
  @IsPositive({ message: 'El precio debe ser mayor a 0' })
  price: number;

  @IsOptional()
  @IsString({ message: 'La descripción debe ser un texto' })
  @Length(0, 500, { message: 'La descripción no puede superar 500 caracteres' })
  description?: string;

  // ============== ACTUALIZACIÓN DE RELACIONES ==============

  @IsNotEmpty({ message: 'El ID de la categoría es obligatorio' })
  @IsNumber({}, { message: 'El ID de la categoría debe ser un número' })
  @IsPositive({ message: 'El ID de la categoría debe ser mayor a 0' })
  categoryId: number;

  // Nota: No se permite cambiar el owner de un producto una vez creado
  // Si fuera necesario, sería una operación de negocio especial
}
```

# **7. Servicio ProductService - Orquestación de Relaciones**

El servicio es responsable de validar y gestionar las relaciones entre entidades.

Archivo: `products/services/product.service.ts`

El `ProductService` conoce todos los repositorios necesarios para validar y gestionar las relaciones.
La clase `ProductService` es la que orquestiona la creación, actualización y consulta de productos con sus relaciones, por eso 
no debe tener los otros servicios inyectados, sino solo los repositorios.

Ya que un servicio que dependEr de otro servicio puede generar:
* acoplamiento horizontal entre servicios
* dependencia circular potencial
* dificultad para testear
* propagación de lógica que no le corresponde al caso de uso actual

En clean architecture, los servicios deben ser lo más independientes posibles entre sí y no llamarse entre estos.

```typescript
import { Injectable } from '@nestjs/common';
import { ProductRepository } from '../repositories/product.repository';
import { UserRepository } from '../../users/repositories/user.repository';
import { CategoryRepository } from '../../categories/repositories/category.repository';
import { CreateProductDto } from '../dto/create-product.dto';
import { UpdateProductDto } from '../dto/update-product.dto';
import { ProductResponseDto, UserSummaryDto, CategoryResponseDto } from '../dto/product-response.dto';
import { Product } from '../entities/product.entity';
import { NotFoundException } from '../../../exceptions/domain/not-found.exception';
import { ConflictException } from '../../../exceptions/domain/conflict.exception';

@Injectable()
export class ProductService {
  constructor(
    private readonly productRepository: ProductRepository,
    private readonly userRepository: UserRepository,
    private readonly categoryRepository: CategoryRepository,
  ) {}

  // ============== CREACIÓN CON RELACIONES ==============

  async create(createProductDto: CreateProductDto): Promise<ProductResponseDto> {
    // 1. Validar que el usuario existe
    const owner = await this.userRepository.findById(createProductDto.userId);
    if (!owner) {
      throw new NotFoundException(
        `Usuario no encontrado con ID: ${createProductDto.userId}`,
      );
    }

    // 2. Validar que la categoría existe
    const category = await this.categoryRepository.findById(createProductDto.categoryId);
    if (!category) {
      throw new NotFoundException(
        `Categoría no encontrada con ID: ${createProductDto.categoryId}`,
      );
    }

    // 3. Crear el producto con las entidades relacionadas
    const product = new Product();
    product.name = createProductDto.name;
    product.price = createProductDto.price;
    product.description = createProductDto.description;
    product.owner = owner; // Asignar entidad completa
    product.category = category; // Asignar entidad completa

    // 4. Persistir
    const savedProduct = await this.productRepository.save(product);

    // 5. Retornar DTO con relaciones
    return this.toResponseDto(savedProduct);
  }

  // ============== CONSULTAS CON RELACIONES ==============

  async findAll(): Promise<ProductResponseDto[]> {
    const products = await this.productRepository.findAll();
    return products.map((product) => this.toResponseDto(product));
  }

  async findById(id: number): Promise<ProductResponseDto> {
    const product = await this.productRepository.findById(id);
    
    if (!product) {
      throw new NotFoundException(`Producto no encontrado con ID: ${id}`);
    }
    
    return this.toResponseDto(product);
  }

  // ============== ACTUALIZACIÓN CON RELACIONES ==============

  async update(id: number, updateProductDto: UpdateProductDto): Promise<ProductResponseDto> {
    // 1. Verificar que el producto existe
    const product = await this.productRepository.findById(id);
    if (!product) {
      throw new NotFoundException(`Producto no encontrado con ID: ${id}`);
    }

    // 2. Si se está cambiando la categoría, validar que existe
    if (updateProductDto.categoryId !== product.category.id) {
      const category = await this.categoryRepository.findById(updateProductDto.categoryId);
      if (!category) {
        throw new NotFoundException(
          `Categoría no encontrada con ID: ${updateProductDto.categoryId}`,
        );
      }
      product.category = category;
    }

    // 3. Actualizar campos básicos
    product.name = updateProductDto.name;
    product.price = updateProductDto.price;
    product.description = updateProductDto.description;

    // 4. Persistir cambios
    const updatedProduct = await this.productRepository.save(product);

    // 5. Retornar DTO actualizado
    return this.toResponseDto(updatedProduct);
  }

  // ============== ELIMINACIÓN ==============

  async remove(id: number): Promise<void> {
    const product = await this.productRepository.findById(id);
    
    if (!product) {
      throw new NotFoundException(`Producto no encontrado con ID: ${id}`);
    }
    
    await this.productRepository.remove(product);
  }

  // ============== CONSULTAS ESPECIALIZADAS ==============

  async findByOwnerId(userId: number): Promise<ProductResponseDto[]> {
    const products = await this.productRepository.findByOwnerId(userId);
    return products.map((product) => this.toResponseDto(product));
  }

  async findByCategoryId(categoryId: number): Promise<ProductResponseDto[]> {
    const products = await this.productRepository.findByCategoryId(categoryId);
    return products.map((product) => this.toResponseDto(product));
  }

  async findByOwnerName(ownerName: string): Promise<ProductResponseDto[]> {
    const products = await this.productRepository.findByOwnerName(ownerName);
    return products.map((product) => this.toResponseDto(product));
  }

  // ============== MÉTODO HELPER ==============

  /**
   * Convierte entidad a DTO con relaciones cargadas
   * @param product - Entidad Product con relaciones
   */
  private toResponseDto(product: Product): ProductResponseDto {
    const dto = new ProductResponseDto();
    
    // Datos básicos del producto
    dto.id = product.id;
    dto.name = product.name;
    dto.price = product.price;
    dto.description = product.description;
    dto.createdAt = product.createdAt;
    dto.updatedAt = product.updatedAt;
    
    // Información del usuario (owner)
    dto.user = {
      id: product.owner.id,
      name: product.owner.name,
      email: product.owner.email,
    };
    
    // Información de la categoría
    dto.category = {
      id: product.category.id,
      name: product.category.name,
      description: product.category.description,
    };
    
    return dto;
  }
}
```

### **Aspectos clave del servicio**

1. **Validación proactiva**: Se valida que las entidades relacionadas existan antes de crear/actualizar
2. **Manejo de errores**: Se lanzan excepciones específicas que serán capturadas por el AllExceptionsFilter
3. **Carga controlada**: Se especifica `relations` en el repositorio para cargar relaciones cuando sea necesario
4. **Separación de responsabilidades**: El servicio orquesta, las entidades definen relaciones, el repositorio persiste

# **8. Controlador ProductController**

Archivo: `products/controllers/product.controller.ts`

```typescript
import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  Delete,
  Put,
  ParseIntPipe,
} from '@nestjs/common';
import { ProductService } from '../services/product.service';
import { CreateProductDto } from '../dto/create-product.dto';
import { UpdateProductDto } from '../dto/update-product.dto';
import { ProductResponseDto } from '../dto/product-response.dto';

@Controller('api/products')
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Post()
  async create(
    @Body() createProductDto: CreateProductDto,
  ): Promise<ProductResponseDto> {
    return this.productService.create(createProductDto);
  }

  @Get()
  async findAll(): Promise<ProductResponseDto[]> {
    return this.productService.findAll();
  }

  @Get(':id')
  async findById(
    @Param('id', ParseIntPipe) id: number,
  ): Promise<ProductResponseDto> {
    return this.productService.findById(id);
  }

  @Put(':id')
  async update(
    @Param('id', ParseIntPipe) id: number,
    @Body() updateProductDto: UpdateProductDto,
  ): Promise<ProductResponseDto> {
    return this.productService.update(id, updateProductDto);
  }

  @Delete(':id')
  async remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return this.productService.remove(id);
  }

  // ============== ENDPOINTS ESPECIALIZADOS ==============

  @Get('owner/:userId')
  async findByOwnerId(
    @Param('userId', ParseIntPipe) userId: number,
  ): Promise<ProductResponseDto[]> {
    return this.productService.findByOwnerId(userId);
  }

  @Get('category/:categoryId')
  async findByCategoryId(
    @Param('categoryId', ParseIntPipe) categoryId: number,
  ): Promise<ProductResponseDto[]> {
    return this.productService.findByCategoryId(categoryId);
  }
}
```

# **9. FASE 2: Evolución a Relaciones Many-to-Many (N:N)**

### **¿Cuándo necesitamos relaciones N:N?**

**Escenario**: Un producto puede pertenecer a múltiples categorías simultáneamente.

**Ejemplos**:
* Laptop → ["Electrónicos", "Oficina", "Gaming"]
* Manual de Laptop → ["Libros", "Oficina", "Electrónicos"]
* Teclado → ["Electrónicos", "Gaming"] 

### **Evolución del esquema**

```
ANTES (1:N):
Product N ──── 1 Category

DESPUÉS (N:N):
Product N ──── N Category
```

## **9.1. Nueva entidad Product con relación N:N**

```typescript
import { Entity, Column, ManyToOne, ManyToMany, JoinColumn, JoinTable } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';
import { User } from '../../users/entities/user.entity';
import { Category } from '../../categories/entities/category.entity';

@Entity('products')
export class Product extends BaseEntity {
  @Column({ nullable: false, length: 150 })
  name: string;

  @Column({ nullable: false, type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @Column({ length: 500, nullable: true })
  description: string;

  // ================== RELACIONES ACTUALIZADAS ==================

  /**
   * Relación Many-to-One con User (se mantiene igual)
   * Un producto pertenece a un usuario (owner)
   */
  @ManyToOne(() => User, { nullable: false, eager: false })
  @JoinColumn({ name: 'user_id' })
  owner: User;

  /**
   * Relación Many-to-Many con Categories (NUEVA)
   * Un producto puede tener múltiples categorías
   * Una categoría puede tener múltiples productos
   */
  @ManyToMany(() => Category, { eager: false })
  @JoinTable({
    name: 'product_categories',
    joinColumn: { name: 'product_id', referencedColumnName: 'id' },
    inverseJoinColumn: { name: 'category_id', referencedColumnName: 'id' },
  })
  categories: Category[];

  // ============== MÉTODOS DE CONVENIENCIA ==============

  /**
   * Agrega una categoría al producto
   */
  addCategory(category: Category): void {
    if (!this.categories) {
      this.categories = [];
    }
    
    // Evitar duplicados
    const exists = this.categories.some(c => c.id === category.id);
    if (!exists) {
      this.categories.push(category);
    }
  }

  /**
   * Remueve una categoría del producto
   */
  removeCategory(category: Category): void {
    if (!this.categories) {
      return;
    }
    
    this.categories = this.categories.filter(c => c.id !== category.id);
  }

  /**
   * Limpia todas las categorías
   */
  clearCategories(): void {
    this.categories = [];
  }
}
```

## **9.2. Explicación de @ManyToMany**

### **@ManyToMany**
```typescript
@ManyToMany(() => Category, { eager: false })
```
* Configura una relación bidireccional N:N
* `eager: false`: Las categorías se cargan bajo demanda

### **@JoinTable**
```typescript
@JoinTable({
  name: 'product_categories',
  joinColumn: { name: 'product_id', referencedColumnName: 'id' },
  inverseJoinColumn: { name: 'category_id', referencedColumnName: 'id' },
})
```

**Función**: Define la **tabla intermedia** que almacena la relación

**Resultado en PostgreSQL**:
```sql
CREATE TABLE product_categories (
    product_id INTEGER NOT NULL REFERENCES products(id),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    PRIMARY KEY (product_id, category_id)
);
```

### **¿Por qué Category[] y no Set<Category>?**

En TypeORM, se usa **arrays** (`Category[]`) en lugar de `Set`:
* **TypeORM**: Nativamente soporta arrays para relaciones N:N
* **Array**: Mantiene orden y es más familiar en JavaScript/TypeScript
* **Duplicados**: Se previenen mediante métodos de conveniencia
* **Serialización**: Los arrays se serializan automáticamente a JSON

## **9.3. Category actualizada (lado inverso)**

```typescript
import { Entity, Column, ManyToMany } from 'typeorm';
import { BaseEntity } from '../../shared/entities/base.entity';
import { Product } from '../../products/entities/product.entity';

@Entity('categories')
export class Category extends BaseEntity {
  @Column({ nullable: false, unique: true, length: 120 })
  name: string;

  @Column({ length: 500, nullable: true })
  description: string;

  // ================== RELACIÓN BIDIRECCIONAL (OPCIONAL) ==================

  /**
   * Relación inversa Many-to-Many con Products
   * No define JoinTable porque Product es el propietario de la relación
   */
  @ManyToMany(() => Product, (product) => product.categories)
  products: Product[];
}
```

### **Parámetro mappedBy alternativo**

```typescript
@ManyToMany(() => Product, (product) => product.categories)
```

* **mappedBy alternativo**: En TypeORM usamos la función flecha para referenciar
* La tabla intermedia se define solo en `Product`
* `Category` no genera tabla adicional
* Mantiene sincronización bidireccional

## **9.4. DTOs actualizados para relación N:N**

### **CreateProductDto con múltiples categorías**

```typescript
import {
  IsNotEmpty,
  IsNumber,
  IsPositive,
  IsString,
  Length,
  IsOptional,
  IsArray,
  ArrayNotEmpty,
} from 'class-validator';

export class CreateProductDto {
  @IsNotEmpty({ message: 'El nombre es obligatorio' })
  @IsString({ message: 'El nombre debe ser un texto' })
  @Length(3, 150, { message: 'El nombre debe tener entre 3 y 150 caracteres' })
  name: string;

  @IsNotEmpty({ message: 'El precio es obligatorio' })
  @IsNumber({ maxDecimalPlaces: 2 }, { message: 'El precio debe ser un número válido' })
  @IsPositive({ message: 'El precio debe ser mayor a 0' })
  price: number;

  @IsOptional()
  @IsString({ message: 'La descripción debe ser un texto' })
  @Length(0, 500, { message: 'La descripción no puede superar 500 caracteres' })
  description?: string;

  // ============== RELACIONES ==============

  @IsNotEmpty({ message: 'El ID del usuario es obligatorio' })
  @IsNumber({}, { message: 'El ID del usuario debe ser un número' })
  @IsPositive({ message: 'El ID del usuario debe ser mayor a 0' })
  userId: number;

  @IsNotEmpty({ message: 'Las categorías son obligatorias' })
  @IsArray({ message: 'Las categorías deben ser un array' })
  @ArrayNotEmpty({ message: 'Debe especificar al menos una categoría' })
  @IsNumber({}, { each: true, message: 'Cada ID de categoría debe ser un número' })
  @IsPositive({ each: true, message: 'Los IDs de categorías deben ser mayores a 0' })
  categoryIds: number[]; // Múltiples categorías
}
```

### **ProductResponseDto con lista de categorías (N:N)**

Actualizamos el DTO de respuesta para incluir una lista de categorías.

```typescript
export class ProductResponseDto {
  id: number;
  name: string;
  price: number;
  description: string;

  // ============== OBJETOS ANIDADOS ==============
  
  user: UserSummaryDto;
  categories: CategoryResponseDto[]; // Array de categorías

  // ============== AUDITORÍA ==============
  
  createdAt: Date;
  updatedAt: Date;

  // ============== DTOs INTERNOS ==============
  
  static UserSummaryDto = class {
    id: number;
    name: string;
    email: string;
  };

  static CategoryResponseDto = class {
    id: number;
    name: string;
    description: string;
  };
}

// Exportar tipos internos
export type UserSummaryDto = InstanceType<typeof ProductResponseDto.UserSummaryDto>;
export type CategoryResponseDto = InstanceType<typeof ProductResponseDto.CategoryResponseDto>;
```

**Respuesta JSON con múltiples categorías:**
```json
{
  "id": 1,
  "name": "Laptop Gaming",
  "price": 1200.00,
  "description": "Laptop de alto rendimiento",
  "user": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@email.com"
  },
  "categories": [
    {
      "id": 2,
      "name": "Electrónicos",
      "description": "Dispositivos electrónicos"
    },
    {
      "id": 5,
      "name": "Gaming",
      "description": "Productos para gamers"
    },
    {
      "id": 8,
      "name": "Oficina",
      "description": "Equipos de oficina"
    }
  ],
  "createdAt": "2024-01-15T10:30:00.000Z",
  "updatedAt": "2024-01-15T10:30:00.000Z"
}
```

## **9.5. ProductRepository actualizado para N:N**

Modificamos el repositorio para consultas basadas en categorías múltiples.

Eliminar los métodos antiguos que asumen relación 1:N y agregar nuevos:

```typescript
/**
 * Encuentra productos que tengan alguna de las categorías especificadas
 */
async findByAnyCategory(categoryIds: number[]): Promise<Product[]> {
  return this.repository
    .createQueryBuilder('product')
    .leftJoinAndSelect('product.owner', 'owner')
    .leftJoinAndSelect('product.categories', 'category')
    .where('category.id IN (:...categoryIds)', { categoryIds })
    .getMany();
}

/**
 * Encuentra productos que tengan TODAS las categorías especificadas
 */
async findByAllCategories(categoryIds: number[]): Promise<Product[]> {
  return this.repository
    .createQueryBuilder('product')
    .leftJoinAndSelect('product.owner', 'owner')
    .leftJoinAndSelect('product.categories', 'category')
    .where('category.id IN (:...categoryIds)', { categoryIds })
    .groupBy('product.id, owner.id')
    .having('COUNT(DISTINCT category.id) = :count', { count: categoryIds.length })
    .getMany();
}

/**
 * Cuenta productos por categoría (para estadísticas)
 */
async countByCategory(categoryId: number): Promise<number> {
  return this.repository
    .createQueryBuilder('product')
    .leftJoin('product.categories', 'category')
    .where('category.id = :categoryId', { categoryId })
    .getCount();
}
```

## **9.6. Servicio actualizado para manejar N:N**

```typescript
// ============== CREACIÓN CON MÚLTIPLES CATEGORÍAS ==============

async create(createProductDto: CreateProductDto): Promise<ProductResponseDto> {
  // 1. Validar que el usuario existe
  const owner = await this.userRepository.findById(createProductDto.userId);
  if (!owner) {
    throw new NotFoundException(
      `Usuario no encontrado con ID: ${createProductDto.userId}`,
    );
  }

  // 2. Validar y obtener todas las categorías
  const categories = await this.validateAndGetCategories(createProductDto.categoryIds);

  // 3. Crear el producto con las entidades relacionadas
  const product = new Product();
  product.name = createProductDto.name;
  product.price = createProductDto.price;
  product.description = createProductDto.description;
  product.owner = owner;
  product.categories = categories; // Asignar array de categorías

  // 4. Persistir
  const savedProduct = await this.productRepository.save(product);

  // 5. Cargar relaciones completas para el DTO
  const productWithRelations = await this.productRepository.findById(savedProduct.id);
  
  return this.toResponseDto(productWithRelations);
}

// ============== MÉTODO HELPER PARA VALIDAR CATEGORÍAS ==============

private async validateAndGetCategories(categoryIds: number[]): Promise<Category[]> {
  const categories: Category[] = [];
  
  for (const categoryId of categoryIds) {
    const category = await this.categoryRepository.findById(categoryId);
    
    if (!category) {
      throw new NotFoundException(
        `Categoría no encontrada con ID: ${categoryId}`,
      );
    }
    
    categories.push(category);
  }
  
  return categories;
}

// ============== MÉTODO HELPER ACTUALIZADO ==============

private toResponseDto(product: Product): ProductResponseDto {
  const dto = new ProductResponseDto();
  
  // Datos básicos del producto
  dto.id = product.id;
  dto.name = product.name;
  dto.price = product.price;
  dto.description = product.description;
  dto.createdAt = product.createdAt;
  dto.updatedAt = product.updatedAt;
  
  // Información del usuario (owner)
  dto.user = {
    id: product.owner.id,
    name: product.owner.name,
    email: product.owner.email,
  };
  
  // Información de las categorías (N:N)
  dto.categories = product.categories.map(category => ({
    id: category.id,
    name: category.name,
    description: category.description,
  }));
  
  return dto;
}
```

# **10. Flujo de Consultas SQL Generadas**

## **10.1. Crear producto con múltiples categorías**

**SQL generado por TypeORM**:

```sql
-- 1. Insertar producto
INSERT INTO products (name, price, description, user_id, created_at, updated_at) 
VALUES ('Laptop Gaming', 1200.00, 'Alta performance', 1, NOW(), NOW()) 
RETURNING id;

-- 2. Insertar relaciones en tabla intermedia
INSERT INTO product_categories (product_id, category_id) VALUES (1, 2); -- Electrónicos
INSERT INTO product_categories (product_id, category_id) VALUES (1, 5); -- Gaming  
INSERT INTO product_categories (product_id, category_id) VALUES (1, 8); -- Oficina
```

## **10.2. Consultar producto con categorías**

```sql
-- Consulta con relaciones cargadas explícitamente
SELECT 
    product.id, product.name, product.price, product.description,
    product.created_at, product.updated_at,
    owner.id as owner_id, owner.name as owner_name, owner.email as owner_email,
    category.id as category_id, category.name as category_name, category.description as category_description
FROM products product
LEFT JOIN users owner ON owner.id = product.user_id
LEFT JOIN product_categories pc ON pc.product_id = product.id
LEFT JOIN categories category ON category.id = pc.category_id
WHERE product.id = $1;
```

# **11. Comparación: 1:N vs N:N en TypeORM**

| Aspecto | Relación 1:N | Relación N:N |
|---------|-------------|-------------|
| **Tabla intermedia** | ❌ No necesaria | ✅ Requerida (`@JoinTable`) |
| **Flexibilidad** | ⚠️ Limitada | ✅ Alta |
| **Complejidad** | ✅ Simple | ⚠️ Media |
| **Performance** | ✅ Mejor | ⚠️ Más consultas |
| **Uso de memoria** | ✅ Menos | ⚠️ Más (arrays) |
| **Casos de uso** | Relaciones fijas | Clasificaciones, tags |
| **Decorador** | `@ManyToOne` | `@ManyToMany` + `@JoinTable` |

## **11.1. ¿Cuándo usar cada tipo?**

### **Usar 1:N cuando:**
* La relación es **naturalmente jerárquica**
* Un elemento pertenece a **una sola categoría padre**
* La estructura es **estable** y no cambiará frecuentemente

### **Usar N:N cuando:**
* Necesitas **clasificación múltiple**
* Los elementos pueden tener **múltiples etiquetas**
* Requieres **flexibilidad** en la categorización

# **12. Configuración del Módulo Product**

Para que todo funcione correctamente, el módulo debe importar todas las dependencias:

Archivo: `products/product.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProductController } from './controllers/product.controller';
import { ProductService } from './services/product.service';
import { ProductRepository } from './repositories/product.repository';
import { Product } from './entities/product.entity';

// Importar entidades relacionadas
import { User } from '../users/entities/user.entity';
import { Category } from '../categories/entities/category.entity';

// Importar repositorios de dependencias
import { UserRepository } from '../users/repositories/user.repository';
import { CategoryRepository } from '../categories/repositories/category.repository';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      Product,
      User,        // Para las consultas con relaciones
      Category,    // Para las consultas con relaciones
    ]),
  ],
  controllers: [ProductController],
  providers: [
    ProductService,
    ProductRepository,
    UserRepository,     // Inyección en ProductService
    CategoryRepository, // Inyección en ProductService
  ],
  exports: [ProductService, ProductRepository],
})
export class ProductModule {}
```

# **13. Actividad Práctica Completa**

Se debe  implementar **ambos enfoques** para entender las diferencias.

## **13.1. PARTE A: Implementar relación 1:N (básica)**

1. **Crear Category básica**
2. **Actualizar Product con @ManyToOne**
3. **Implementar ProductService con validación de relaciones**
4. **Crear endpoints**:
   - `POST /api/products` (con userId y categoryId)
   - `GET /api/products/:id` (con relaciones cargadas)
   - `GET /api/products/category/:categoryId`
5. **Probar con datos reales en PostgreSQL**

## **13.2. PARTE B: Evolucionar a N:N (avanzada)**

1. **Actualizar Product con @ManyToMany**
2. **Actualizar Category con relación bidireccional**
3. **Modificar DTOs para múltiples categorías**
4. **Actualizar ProductService para manejar Category[]**
5. **Probar creación de productos con múltiples categorías**

## **13.3. PARTE C: Consultas avanzadas**

1. **Implementar endpoints adicionales**:
   - `GET /api/categories/:id/products/count` (contar productos por categoría)
2. **Agregar consultas personalizadas con QueryBuilder**
3. **Implementar filtros complejos**

# **14. Resultados y Evidencias Requeridas**

## **14.1. Evidencias de implementación**
1. **Captura de Product entity** (con ambas versiones: 1:N y N:N)
2. **Captura de ProductService** (métodos create y update)

## **14.2. Evidencias de funcionamiento**
1. **Producto creado con una categoría** (versión 1:N)
2. **Producto creado con múltiples categorías** (versión N:N)
3. **Consulta SQL en consola** mostrando tabla intermedia `product_categories`
4. **Respuesta JSON** de un producto con múltiples categorías

## **14.3. Evidencias de base de datos**
1. **Captura del consumo de** `/api/categories/{id}/products/count`

## **14.4. Datos para revisión**

**Crear los siguientes productos de prueba**:

1. **Laptop Gaming** → Categorías: ["Electrónicos", "Gaming", "Oficina"]
2. **Mouse Inalámbrico** → Categorías: ["Electrónicos", "Oficina"]
3. **Monitor 4K** → Categorías: ["Electrónicos", "Gaming", "Diseño"]
4. **Teclado Mecánico** → Categorías: ["Gaming", "Oficina"]
5. **Libro TypeScript** → Categorías: ["Libros", "Programación", "Educación"]

# **15. Conclusiones**

Las relaciones TypeORM en NestJS proporcionan:

* **Mapeo objeto-relacional robusto** similar a JPA
* **Type-safety** completo con TypeScript
* **Flexibilidad** para evolucionar de 1:N a N:N
* **Consultas optimizadas** con QueryBuilder
* **Integración perfecta** con el ecosistema NestJS

