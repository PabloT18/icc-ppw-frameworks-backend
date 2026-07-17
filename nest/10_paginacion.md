# Programación y Plataformas Web

# **NestJS – Paginación de Datos con TypeORM: Optimización y User Experience**

<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-original.svg" width="95">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="95">
</div>

## **Práctica 10 (NestJS): Paginación, Metadatos y QueryBuilder con Request Parameters**

### **Autores**

**Pablo Torres**

 [ptorresp@ups.edu.ec](mailto:ptorresp@ups.edu.ec)

GitHub: PabloT18

# **1. Introducción a la Paginación en NestJS**

En el tema anterior implementamos **filtros con Request Parameters** en consultas relacionadas usando TypeORM. Ahora necesitamos **paginar los resultados** para manejar grandes volúmenes de datos eficientemente.

Los principales problemas sin paginación son:

* **Consultas masivas**: Devolver 100,000 productos consume excesiva memoria
* **Tiempo de respuesta lento**: Transferir todos los datos a la vez
* **Sobrecarga de red**: Grandes payloads JSON
* **Experiencia de usuario deficiente**: Largos tiempos de espera
* **Problemas de escalabilidad**: El sistema no funciona con millones de registros

## **1.1. TypeORM Pagination**

TypeORM proporciona varias estrategias para paginación:

* **take/skip**: Métodos básicos para limitar y saltar registros
* **getManyAndCount()**: Obtiene datos y count total en una operación optimizada
* **QueryBuilder**: Control total sobre la consulta de paginación
* **Offset/Limit**: SQL estándar con OFFSET y LIMIT

### **Ejemplo conceptual**

```typescript
// Parámetros de entrada
const page = 0;
const size = 10;
const skip = page * size;

// Resultado paginado
const [products, total] = await this.productRepository
  .createQueryBuilder('product')
  .take(size)
  .skip(skip)
  .getManyAndCount();
```

## **1.2. Ventajas de TypeORM Pagination**

* **Flexible**: Control total sobre la consulta
* **Type-safe**: Completamente tipado con TypeScript
* **Optimizado**: Consultas SQL eficientes con QueryBuilder
* **Integrado**: Funciona perfectamente con el ecosistema NestJS
* **Customizable**: Se adapta a cualquier necesidad de filtrado

# **2. Tipos de Paginación en NestJS/TypeORM**

## **2.1. Paginación Simple vs Paginación con Metadatos**

### **Paginación Simple (solo datos)**

**Características**:
* Solo devuelve **array de datos**
* **Más rápida** (una consulta)
* Ideal para **feeds infinitos**
* **Menos información** para el frontend

```typescript
async findProducts(page: number, size: number): Promise<Product[]> {
  return this.productRepository
    .createQueryBuilder('product')
    .take(size)
    .skip(page * size)
    .getMany(); // Solo una consulta
}
```

### **Paginación con Metadatos (información completa)**

**Características**:
* Devuelve **datos + metadatos**
* Incluye **count total**
* Permite **navegación a cualquier página**
* **Más completa** para interfaces complejas

```typescript
async findProductsWithMeta(page: number, size: number): Promise<PaginatedResponse<Product>> {
  const [products, total] = await this.productRepository
    .createQueryBuilder('product')
    .take(size)
    .skip(page * size)
    .getManyAndCount(); // Datos + count en una operación optimizada
  
  return {
    data: products,
    meta: {
      page,
      size,
      total,
      totalPages: Math.ceil(total / size),
      hasNext: (page + 1) * size < total,
      hasPrevious: page > 0
    }
  };
}
```

### **¿Cuándo usar cada tipo?**

| Escenario | Paginación Simple | Paginación con Metadatos |
|-----------|------------------|--------------------------|
| **Navegación con números de página** | ❌ | ✅ SÍ |
| **Necesitas mostrar "Página X de Y"** | ❌ | ✅ SÍ |
| **Feeds de redes sociales** | ✅ SÍ | ❌ |
| **Performance crítica** | ✅ SÍ | ⚠️ Depende |
| **Scroll infinito** | ✅ SÍ | ❌ |
| **Reportes con totales** | ❌ | ✅ SÍ |

## **2.2. Estrategias de Ordenamiento en TypeORM**

```typescript
// Ordenamiento simple
.orderBy('product.name', 'ASC')

// Ordenamiento múltiple
.orderBy('product.categoryId', 'ASC')
.addOrderBy('product.price', 'DESC')

// Ordenamiento dinámico
.orderBy(`product.${sortField}`, sortOrder as 'ASC' | 'DESC')

// Ordenamiento por relaciones
.leftJoinAndSelect('product.category', 'category')
.orderBy('category.name', 'ASC')
.addOrderBy('product.name', 'ASC')
```

# **3. DTOs para Paginación en NestJS**

## **3.1. DTO de Request para Paginación**

Archivo: `shared/dto/pagination-query.dto.ts`

```typescript
import { IsOptional, IsInt, Min, Max, IsString, IsIn } from 'class-validator';
import { Transform, Type } from 'class-transformer';

export class PaginationQueryDto {
  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'La página debe ser un número entero' })
  @Min(0, { message: 'La página debe ser mayor o igual a 0' })
  page?: number = 0;

  @IsOptional()
  @Type(() => Number)
  @IsInt({ message: 'El tamaño debe ser un número entero' })
  @Min(1, { message: 'El tamaño debe ser mayor a 0' })
  @Max(100, { message: 'El tamaño no puede ser mayor a 100' })
  size?: number = 10;

  @IsOptional()
  @IsString({ message: 'El campo de ordenamiento debe ser una cadena' })
  sortBy?: string = 'id';

  @IsOptional()
  @IsIn(['ASC', 'DESC', 'asc', 'desc'], { 
    message: 'La dirección debe ser ASC o DESC' 
  })
  @Transform(({ value }) => value?.toUpperCase())
  sortOrder?: 'ASC' | 'DESC' = 'DESC';

  // ============== MÉTODOS HELPER ==============

  /**
   * Calcula el offset para la consulta
   */
  get skip(): number {
    return (this.page || 0) * (this.size || 10);
  }

  /**
   * Obtiene el limit para la consulta
   */
  get take(): number {
    return this.size || 10;
  }

  /**
   * Valida que el campo de ordenamiento sea seguro
   */
  isValidSortField(allowedFields: string[]): boolean {
    return allowedFields.includes(this.sortBy || 'id');
  }
}
```

## **3.2. DTO de Response Paginado**

Archivo: `shared/dto/paginated-response.dto.ts`

```typescript
export class PaginationMetaDto {
  page: number;
  size: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;

  constructor(page: number, size: number, total: number) {
    this.page = page;
    this.size = size;
    this.total = total;
    this.totalPages = Math.ceil(total / size);
    this.hasNext = (page + 1) * size < total;
    this.hasPrevious = page > 0;
  }
}

export class PaginatedResponseDto<T> {
  data: T[];
  meta: PaginationMetaDto;

  constructor(data: T[], page: number, size: number, total: number) {
    this.data = data;
    this.meta = new PaginationMetaDto(page, size, total);
  }

  /**
   * Factory method para crear respuesta paginada
   */
  static create<T>(
    data: T[], 
    page: number, 
    size: number, 
    total: number
  ): PaginatedResponseDto<T> {
    return new PaginatedResponseDto(data, page, size, total);
  }

  /**
   * Mapea los datos manteniendo la paginación
   */
  map<U>(mapFn: (item: T) => U): PaginatedResponseDto<U> {
    return new PaginatedResponseDto(
      this.data.map(mapFn), 
      this.meta.page, 
      this.meta.size, 
      this.meta.total
    );
  }
}
```

## **3.3. DTO para Filtros + Paginación**

Archivo: `products/dto/product-filter-query.dto.ts`

```typescript
import { IsOptional, IsString, IsNumber, IsPositive, Min, Length } from 'class-validator';
import { Transform, Type } from 'class-transformer';
import { PaginationQueryDto } from '../../shared/dto/pagination-query.dto';

export class ProductFilterQueryDto extends PaginationQueryDto {
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
  maxPrice?: number;

  @IsOptional()
  @Type(() => Number)
  @IsNumber({}, { message: 'El ID de categoría debe ser un número válido' })
  @IsPositive({ message: 'El ID de categoría debe ser positivo' })
  categoryId?: number;

  // ============== VALIDACIONES PERSONALIZADAS ==============

  /**
   * Lista de campos permitidos para ordenamiento
   */
  static readonly ALLOWED_SORT_FIELDS = [
    'id', 'name', 'price', 'createdAt', 'updatedAt', 'category.name'
  ];

  /**
   * Valida que el rango de precios sea coherente
   */
  validatePriceRange(): boolean {
    if (this.minPrice !== undefined && this.maxPrice !== undefined) {
      return this.maxPrice >= this.minPrice;
    }
    return true;
  }

  /**
   * Valida que el campo de ordenamiento sea permitido
   */
  isValidSortField(): boolean {
    return super.isValidSortField(ProductFilterQueryDto.ALLOWED_SORT_FIELDS);
  }
}
```

# **4. Implementación de Paginación en UserController**

Continuando con los endpoints del tema anterior, agregaremos paginación a los productos de usuarios.

## **4.1. UserController - Endpoints con Paginación**

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
  ValidationPipe,
  HttpStatus,
  HttpCode,
  BadRequestException,
} from '@nestjs/common';
import { UserService } from '../services/user.service';
import { CreateUserDto } from '../dto/create-user.dto';
import { UpdateUserDto } from '../dto/update-user.dto';
import { UserResponseDto } from '../dto/user-response.dto';
import { ProductResponseDto } from '../../products/dto/product-response.dto';
import { PaginatedResponseDto } from '../../shared/dto/paginated-response.dto';
import { ProductFilterQueryDto } from '../../products/dto/product-filter-query.dto';
import { PaginationQueryDto } from '../../shared/dto/pagination-query.dto';

@Controller('api/users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  // ============== ENDPOINTS BÁSICOS (ya implementados) ==============
  
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

  // ============== PRODUCTOS DEL USUARIO (del tema 09) ==============

  /**
   * Obtiene todos los productos de un usuario (sin paginación - tema 09)
   * Ejemplo: GET /api/users/123/products
   */
  @Get(':id/products')
  async getProducts(
    @Param('id', ParseIntPipe) id: number,
  ): Promise<ProductResponseDto[]> {
    return this.userService.getProductsByUserId(id);
  }

  // ============== NUEVOS ENDPOINTS CON PAGINACIÓN ==============

  /**
   * Obtiene productos de un usuario con paginación básica
   * Ejemplo: GET /api/users/1/products-paginated?page=0&size=5&sortBy=name&sortOrder=ASC
   */
  @Get(':id/products-paginated')
  async getProductsPaginated(
    @Param('id', ParseIntPipe) id: number,
    @Query(ValidationPipe) pagination: PaginationQueryDto,
  ): Promise<PaginatedResponseDto<ProductResponseDto>> {
    
    // Validar que el campo de ordenamiento sea seguro
    const allowedFields = ['id', 'name', 'price', 'createdAt', 'updatedAt'];
    if (!pagination.isValidSortField(allowedFields)) {
      throw new BadRequestException(
        `Campo de ordenamiento no válido. Permitidos: ${allowedFields.join(', ')}`
      );
    }

    return this.userService.getProductsByUserIdPaginated(
      id, 
      pagination.page || 0, 
      pagination.size || 10,
      pagination.sortBy || 'id',
      pagination.sortOrder || 'DESC'
    );
  }

  /**
   * Obtiene productos de un usuario con filtros y paginación completa
   * Ejemplo: GET /api/users/1/products-filtered?name=laptop&minPrice=500&page=0&size=5&sortBy=price&sortOrder=DESC
   */
  @Get(':id/products-filtered')
  async getProductsFiltered(
    @Param('id', ParseIntPipe) id: number,
    @Query(ValidationPipe) filters: ProductFilterQueryDto,
  ): Promise<PaginatedResponseDto<ProductResponseDto>> {
    
    // Validar campo de ordenamiento
    if (!filters.isValidSortField()) {
      throw new BadRequestException(
        `Campo de ordenamiento no válido. Permitidos: ${ProductFilterQueryDto.ALLOWED_SORT_FIELDS.join(', ')}`
      );
    }

    // Validar rango de precios
    if (!filters.validatePriceRange()) {
      throw new BadRequestException(
        'El precio máximo debe ser mayor o igual al precio mínimo'
      );
    }

    return this.userService.getProductsByUserIdWithFiltersAndPagination(id, filters);
  }

  /**
   * Obtiene productos de un usuario con scroll infinito (sin count total)
   * Ejemplo: GET /api/users/1/products-infinite?page=0&size=10&sortBy=createdAt&sortOrder=DESC
   */
  @Get(':id/products-infinite')
  async getProductsInfiniteScroll(
    @Param('id', ParseIntPipe) id: number,
    @Query(ValidationPipe) pagination: PaginationQueryDto,
  ): Promise<{
    data: ProductResponseDto[];
    hasNext: boolean;
    nextPage?: number;
  }> {
    
    // Validar campo de ordenamiento
    const allowedFields = ['id', 'name', 'price', 'createdAt', 'updatedAt'];
    if (!pagination.isValidSortField(allowedFields)) {
      throw new BadRequestException(
        `Campo de ordenamiento no válido. Permitidos: ${allowedFields.join(', ')}`
      );
    }

    const result = await this.userService.getProductsByUserIdInfiniteScroll(
      id,
      pagination.page || 0,
      pagination.size || 10,
      pagination.sortBy || 'createdAt',
      pagination.sortOrder || 'DESC'
    );

    return result;
  }
}
```

### **Aspectos clave del controlador**

1. **DTOs de validación**: Uso de DTOs especializados para paginación y filtros
2. **Validaciones explícitas**: Campo de ordenamiento y rango de precios
3. **Múltiples estrategias**: Paginación básica, con filtros, y scroll infinito
4. **Error handling**: Validaciones claras con mensajes descriptivos
5. **Consistencia**: Mantiene los endpoints del tema 09 y agrega nuevos

# **5. Implementación del UserService con Paginación**

## **5.1. Actualización de UserService**

Archivo: `users/services/user.service.ts`

```typescript
import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { UserRepository } from '../repositories/user.repository';
import { ProductRepository } from '../../products/repositories/product.repository';
import { CreateUserDto } from '../dto/create-user.dto';
import { UpdateUserDto } from '../dto/update-user.dto';
import { UserResponseDto } from '../dto/user-response.dto';
import { ProductResponseDto } from '../../products/dto/product-response.dto';
import { PaginatedResponseDto } from '../../shared/dto/paginated-response.dto';
import { ProductFilterQueryDto } from '../../products/dto/product-filter-query.dto';

@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly productRepository: ProductRepository,
  ) {}

  // ============== MÉTODOS BÁSICOS EXISTENTES (del tema anterior) ==============
  
  async create(createUserDto: CreateUserDto): Promise<UserResponseDto> {
    // Implementación existente...
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

  // ============== MÉTODOS DE PRODUCTOS SIN PAGINACIÓN (del tema 09) ==============

  async getProductsByUserId(userId: number): Promise<ProductResponseDto[]> {
    // Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // Consulta explícita al repositorio correcto
    const products = await this.productRepository.findByOwnerId(userId);
    
    // Mapear a DTOs
    return products.map(product => this.toProductResponseDto(product));
  }

  async getProductsByUserIdWithFilters(
    userId: number,
    name?: string,
    minPrice?: number,
    maxPrice?: number,
    categoryId?: number,
  ): Promise<ProductResponseDto[]> {
    
    // Validar usuario
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // Validar filtros
    this.validateFilterParameters(minPrice, maxPrice);
    
    // Consulta con filtros
    const products = await this.productRepository.findByOwnerIdWithFilters(
      userId, name, minPrice, maxPrice, categoryId
    );
    
    return products.map(product => this.toProductResponseDto(product));
  }

  // ============== NUEVOS MÉTODOS CON PAGINACIÓN ==============

  async getProductsByUserIdPaginated(
    userId: number,
    page: number,
    size: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<PaginatedResponseDto<ProductResponseDto>> {
    
    // 1. Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // 2. Validar parámetros de paginación
    this.validatePaginationParameters(page, size);
    
    // 3. Consulta paginada
    const [products, total] = await this.productRepository.findByOwnerIdPaginated(
      userId, 
      page * size, // skip
      size,        // take
      sortBy,
      sortOrder
    );
    
    // 4. Mapear y crear respuesta paginada
    const productDtos = products.map(product => this.toProductResponseDto(product));
    return PaginatedResponseDto.create(productDtos, page, size, total);
  }

  async getProductsByUserIdWithFiltersAndPagination(
    userId: number,
    filters: ProductFilterQueryDto
  ): Promise<PaginatedResponseDto<ProductResponseDto>> {
    
    // 1. Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // 2. Validar parámetros
    this.validatePaginationParameters(filters.page || 0, filters.size || 10);
    this.validateFilterParameters(filters.minPrice, filters.maxPrice);
    
    // 3. Consulta con filtros y paginación
    const [products, total] = await this.productRepository.findByOwnerIdWithFiltersAndPagination(
      userId,
      filters.skip,
      filters.take,
      filters.sortBy || 'id',
      filters.sortOrder || 'DESC',
      filters.name,
      filters.minPrice,
      filters.maxPrice,
      filters.categoryId
    );
    
    // 4. Mapear y crear respuesta paginada
    const productDtos = products.map(product => this.toProductResponseDto(product));
    return PaginatedResponseDto.create(
      productDtos, 
      filters.page || 0, 
      filters.size || 10, 
      total
    );
  }

  async getProductsByUserIdInfiniteScroll(
    userId: number,
    page: number,
    size: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<{
    data: ProductResponseDto[];
    hasNext: boolean;
    nextPage?: number;
  }> {
    
    // 1. Validar que el usuario existe
    const userExists = await this.userRepository.findById(userId);
    if (!userExists) {
      throw new NotFoundException(`Usuario no encontrado con ID: ${userId}`);
    }
    
    // 2. Validar parámetros
    this.validatePaginationParameters(page, size);
    
    // 3. Obtener uno más de lo solicitado para saber si hay siguiente
    const products = await this.productRepository.findByOwnerIdForInfiniteScroll(
      userId,
      page * size, // skip
      size + 1,    // take (uno extra)
      sortBy,
      sortOrder
    );
    
    // 4. Determinar si hay siguiente página
    const hasNext = products.length > size;
    
    // 5. Remover el elemento extra si existe
    const actualProducts = hasNext ? products.slice(0, size) : products;
    
    // 6. Mapear a DTOs
    const productDtos = actualProducts.map(product => this.toProductResponseDto(product));
    
    return {
      data: productDtos,
      hasNext,
      nextPage: hasNext ? page + 1 : undefined
    };
  }

  // ============== MÉTODOS HELPER ==============

  private validatePaginationParameters(page: number, size: number): void {
    if (page < 0) {
      throw new BadRequestException('La página debe ser mayor o igual a 0');
    }
    
    if (size < 1 || size > 100) {
      throw new BadRequestException('El tamaño debe estar entre 1 y 100');
    }
  }

  private validateFilterParameters(minPrice?: number, maxPrice?: number): void {
    if (minPrice !== undefined && minPrice < 0) {
      throw new BadRequestException('El precio mínimo no puede ser negativo');
    }
    
    if (maxPrice !== undefined && maxPrice < 0) {
      throw new BadRequestException('El precio máximo no puede ser negativo');
    }
    
    if (minPrice !== undefined && maxPrice !== undefined && maxPrice < minPrice) {
      throw new BadRequestException('El precio máximo debe ser mayor o igual al precio mínimo');
    }
  }

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

1. **Separación de responsabilidades**: Validaciones en el servicio, consultas en el repositorio
2. **PaginatedResponseDto.create()**: Factory method para crear respuestas consistentes
3. **Scroll infinito optimizado**: Obtiene N+1 elementos para verificar hasNext
4. **Validaciones robustas**: Parámetros de paginación y filtros
5. **Manejo de errores**: Excepciones específicas con mensajes claros

# **6. Actualización del ProductRepository con Paginación**

## **6.1. ProductRepository - Consultas con TypeORM**

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

  // ============== CONSULTAS BÁSICAS SIN PAGINACIÓN (del tema 09) ==============
  
  async findByOwnerId(userId: number): Promise<Product[]> {
    return this.repository.find({
      where: { owner: { id: userId } },
      relations: ['owner', 'category'],
    });
  }

  async findByOwnerIdWithFilters(
    userId: number,
    name?: string,
    minPrice?: number,
    maxPrice?: number,
    categoryId?: number,
  ): Promise<Product[]> {
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('owner.id = :userId', { userId });

    // Aplicar filtros del tema 09
    if (name) {
      queryBuilder.andWhere('LOWER(product.name) LIKE LOWER(:name)', {
        name: `%${name}%`
      });
    }

    if (minPrice !== undefined) {
      queryBuilder.andWhere('product.price >= :minPrice', { minPrice });
    }

    if (maxPrice !== undefined) {
      queryBuilder.andWhere('product.price <= :maxPrice', { maxPrice });
    }

    if (categoryId !== undefined) {
      queryBuilder.andWhere('category.id = :categoryId', { categoryId });
    }

    return queryBuilder
      .orderBy('product.createdAt', 'DESC')
      .getMany();
  }

  // ============== NUEVAS CONSULTAS CON PAGINACIÓN ==============

  /**
   * Encuentra productos de un usuario con paginación básica
   */
  async findByOwnerIdPaginated(
    userId: number,
    skip: number,
    take: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<[Product[], number]> {
    
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('owner.id = :userId', { userId });

    // Aplicar ordenamiento dinámico
    if (sortBy === 'category.name') {
      queryBuilder.orderBy('category.name', sortOrder);
    } else {
      queryBuilder.orderBy(`product.${sortBy}`, sortOrder);
    }

    // Aplicar paginación
    queryBuilder
      .skip(skip)
      .take(take);

    // Obtener datos y count total
    return queryBuilder.getManyAndCount();
  }

  /**
   * Encuentra productos de un usuario con filtros y paginación
   */
  async findByOwnerIdWithFiltersAndPagination(
    userId: number,
    skip: number,
    take: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC',
    name?: string,
    minPrice?: number,
    maxPrice?: number,
    categoryId?: number
  ): Promise<[Product[], number]> {
    
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('owner.id = :userId', { userId });

    // Aplicar filtros (misma lógica del tema 09)
    if (name) {
      queryBuilder.andWhere('LOWER(product.name) LIKE LOWER(:name)', {
        name: `%${name}%`
      });
    }

    if (minPrice !== undefined) {
      queryBuilder.andWhere('product.price >= :minPrice', { minPrice });
    }

    if (maxPrice !== undefined) {
      queryBuilder.andWhere('product.price <= :maxPrice', { maxPrice });
    }

    if (categoryId !== undefined) {
      queryBuilder.andWhere('category.id = :categoryId', { categoryId });
    }

    // Aplicar ordenamiento
    if (sortBy === 'category.name') {
      queryBuilder.orderBy('category.name', sortOrder);
    } else {
      queryBuilder.orderBy(`product.${sortBy}`, sortOrder);
    }

    // Aplicar paginación
    queryBuilder
      .skip(skip)
      .take(take);

    return queryBuilder.getManyAndCount();
  }

  /**
   * Encuentra productos para scroll infinito (sin count total)
   */
  async findByOwnerIdForInfiniteScroll(
    userId: number,
    skip: number,
    take: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<Product[]> {
    
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('owner.id = :userId', { userId });

    // Aplicar ordenamiento
    if (sortBy === 'category.name') {
      queryBuilder.orderBy('category.name', sortOrder);
    } else {
      queryBuilder.orderBy(`product.${sortBy}`, sortOrder);
    }

    // Aplicar paginación (sin count)
    return queryBuilder
      .skip(skip)
      .take(take)
      .getMany();
  }

  // ============== CONSULTAS GENERALES CON PAGINACIÓN ==============

  /**
   * Encuentra todos los productos con paginación
   */
  async findAllPaginated(
    skip: number,
    take: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<[Product[], number]> {
    
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category');

    // Aplicar ordenamiento
    if (sortBy === 'owner.name') {
      queryBuilder.orderBy('owner.name', sortOrder);
    } else if (sortBy === 'category.name') {
      queryBuilder.orderBy('category.name', sortOrder);
    } else {
      queryBuilder.orderBy(`product.${sortBy}`, sortOrder);
    }

    return queryBuilder
      .skip(skip)
      .take(take)
      .getManyAndCount();
  }

  /**
   * Búsqueda global con filtros y paginación
   */
  async searchWithPagination(
    searchTerm: string,
    skip: number,
    take: number,
    sortBy: string,
    sortOrder: 'ASC' | 'DESC'
  ): Promise<[Product[], number]> {
    
    const queryBuilder = this.repository
      .createQueryBuilder('product')
      .leftJoinAndSelect('product.owner', 'owner')
      .leftJoinAndSelect('product.category', 'category')
      .where('LOWER(product.name) LIKE LOWER(:search)', { search: `%${searchTerm}%` })
      .orWhere('LOWER(product.description) LIKE LOWER(:search)', { search: `%${searchTerm}%` })
      .orWhere('LOWER(category.name) LIKE LOWER(:search)', { search: `%${searchTerm}%` })
      .orWhere('LOWER(owner.name) LIKE LOWER(:search)', { search: `%${searchTerm}%` });

    // Aplicar ordenamiento
    if (sortBy === 'owner.name') {
      queryBuilder.orderBy('owner.name', sortOrder);
    } else if (sortBy === 'category.name') {
      queryBuilder.orderBy('category.name', sortOrder);
    } else {
      queryBuilder.orderBy(`product.${sortBy}`, sortOrder);
    }

    return queryBuilder
      .skip(skip)
      .take(take)
      .getManyAndCount();
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

### **Aspectos técnicos importantes**

1. **getManyAndCount()**: Optimización de TypeORM que ejecuta consulta y count en una sola operación
2. **QueryBuilder dinámico**: Ordenamiento condicional según el campo solicitado
3. **Filtros + paginación**: Combinación eficiente de ambas funcionalidades
4. **Scroll infinito**: Solo usa getMany() para mejor performance
5. **Búsqueda global**: Consulta en múltiples campos con OR logic

### **SQL generado por TypeORM**

```sql
-- Para getManyAndCount() (paginación con metadatos)
SELECT 
    product.*, owner.*, category.*
FROM products product 
LEFT JOIN users owner ON product.user_id = owner.id 
LEFT JOIN categories category ON product.category_id = category.id 
WHERE owner.id = $1 
  AND (product.name ILIKE '%' || $2 || '%' OR $2 IS NULL)
  AND (product.price >= $3 OR $3 IS NULL)
  AND (product.price <= $4 OR $4 IS NULL)
  AND (category.id = $5 OR $5 IS NULL)
ORDER BY product.created_at DESC 
LIMIT $6 OFFSET $7;

-- Count query automática
SELECT COUNT(DISTINCT(product.id)) FROM products product 
LEFT JOIN users owner ON product.user_id = owner.id 
LEFT JOIN categories category ON product.category_id = category.id 
WHERE [...same conditions...];

-- Para getMany() (scroll infinito)
SELECT product.*, owner.*, category.* FROM products product 
[...same query without count...] 
LIMIT $6 OFFSET $7;  -- Sin count separado
```

# **7. Respuestas JSON con Metadatos de Paginación**

## **7.1. Estructura de Respuesta Paginada Completa**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Laptop Gaming MSI",
      "price": 1299.99,
      "description": "Laptop para gaming de alta gama",
      "createdAt": "2024-01-15T10:30:00.000Z",
      "updatedAt": "2024-01-15T10:30:00.000Z",
      "user": {
        "id": 1,
        "name": "Pablo Torres",
        "email": "pablo@example.com"
      },
      "category": {
        "id": 2,
        "name": "Gaming",
        "description": "Productos gaming"
      }
    },
    // ... más productos ...
  ],
  "meta": {
    "page": 0,
    "size": 10,
    "total": 156,
    "totalPages": 16,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

## **7.2. Estructura de Respuesta para Scroll Infinito**

```json
{
  "data": [
    // ... productos ...
  ],
  "hasNext": true,
  "nextPage": 1
}
```

## **7.3. Interceptor para Respuestas Consistentes**

Archivo: `shared/interceptors/pagination.interceptor.ts`

```typescript
import {
  Injectable,
  NestInterceptor,
  ExecutionContext,
  CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { PaginatedResponseDto } from '../dto/paginated-response.dto';

@Injectable()
export class PaginationInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map((data) => {
        // Si es una respuesta paginada, agregar metadatos adicionales
        if (data instanceof PaginatedResponseDto) {
          const request = context.switchToHttp().getRequest();
          const baseUrl = `${request.protocol}://${request.get('host')}${request.url.split('?')[0]}`;
          
          return {
            ...data,
            links: {
              first: data.meta.page === 0 ? null : `${baseUrl}?page=0&size=${data.meta.size}`,
              previous: data.meta.hasPrevious 
                ? `${baseUrl}?page=${data.meta.page - 1}&size=${data.meta.size}` 
                : null,
              next: data.meta.hasNext 
                ? `${baseUrl}?page=${data.meta.page + 1}&size=${data.meta.size}` 
                : null,
              last: `${baseUrl}?page=${data.meta.totalPages - 1}&size=${data.meta.size}`,
            }
          };
        }
        
        return data;
      }),
    );
  }
}
```

# **8. Optimizaciones y Consideraciones de Performance**

## **8.1. Índices de Base de Datos**

Para consultas paginadas eficientes en PostgreSQL:

```sql
-- Índices básicos para ordenamiento
CREATE INDEX idx_products_id ON products(id);
CREATE INDEX idx_products_created_at ON products(created_at DESC);
CREATE INDEX idx_products_updated_at ON products(updated_at DESC);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_price ON products(price);

-- Índices para relaciones (FK)
CREATE INDEX idx_products_user_id ON products(user_id);
CREATE INDEX idx_products_category_id ON products(category_id);

-- Índices compuestos para consultas frecuentes
CREATE INDEX idx_products_user_created ON products(user_id, created_at DESC);
CREATE INDEX idx_products_user_price ON products(user_id, price DESC);
CREATE INDEX idx_products_category_created ON products(category_id, created_at DESC);

-- Índice para búsqueda de texto (opcional con PostgreSQL)
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
```

## **8.2. Configuración y Límites**

Archivo: `shared/constants/pagination.constants.ts`

```typescript
export const PAGINATION_CONSTANTS = {
  DEFAULT_PAGE: 0,
  DEFAULT_SIZE: 10,
  MIN_SIZE: 1,
  MAX_SIZE: 100,
  MAX_PAGE: 1000, // Prevenir páginas muy altas
  
  // Campos de ordenamiento permitidos por defecto
  DEFAULT_SORT_FIELDS: ['id', 'createdAt', 'updatedAt'],
  
  // Configuraciones específicas
  PRODUCTS: {
    ALLOWED_SORT_FIELDS: [
      'id', 'name', 'price', 'createdAt', 'updatedAt', 
      'owner.name', 'category.name'
    ],
    DEFAULT_SORT: 'createdAt',
    DEFAULT_ORDER: 'DESC' as const,
  },
  
  USERS: {
    ALLOWED_SORT_FIELDS: ['id', 'name', 'email', 'createdAt', 'updatedAt'],
    DEFAULT_SORT: 'createdAt',
    DEFAULT_ORDER: 'DESC' as const,
  }
};
```

## **8.3. Estrategias según el Caso de Uso**

### **Para Administración (metadatos completos)**
```typescript
// Usar PaginatedResponseDto con count total
async getProductsForAdmin(filters: ProductFilterQueryDto): Promise<PaginatedResponseDto<ProductResponseDto>> {
  const [products, total] = await this.productRepository.findAllWithFilters(filters);
  const productDtos = products.map(product => this.toResponseDto(product));
  return PaginatedResponseDto.create(productDtos, filters.page, filters.size, total);
}
```

### **Para Feeds de Usuario (performance)**
```typescript
// Usar scroll infinito sin count
async getProductsFeed(pagination: PaginationQueryDto): Promise<{data: ProductResponseDto[], hasNext: boolean}> {
  const products = await this.productRepository.findForFeed(
    pagination.skip, 
    pagination.take + 1  // +1 para verificar hasNext
  );
  
  return {
    data: products.slice(0, pagination.take).map(p => this.toResponseDto(p)),
    hasNext: products.length > pagination.take
  };
}
```

### **Para Búsquedas (híbrido)**
```typescript
// Usar count solo cuando el usuario lo necesite
async searchProducts(
  searchTerm: string, 
  pagination: PaginationQueryDto,
  includeCount: boolean = false
): Promise<PaginatedResponseDto<ProductResponseDto> | ProductResponseDto[]> {
  
  if (includeCount) {
    const [products, total] = await this.productRepository.searchWithCount(searchTerm, pagination);
    const productDtos = products.map(p => this.toResponseDto(p));
    return PaginatedResponseDto.create(productDtos, pagination.page, pagination.size, total);
  } else {
    const products = await this.productRepository.search(searchTerm, pagination);
    return products.map(p => this.toResponseDto(p));
  }
}
```

## **8.4. Cache de Count Total**

Para queries frecuentes con count costoso:

```typescript
import { Injectable } from '@nestjs/common';
import { Cache } from 'cache-manager';

@Injectable()
export class ProductService {
  constructor(
    private readonly cacheManager: Cache,
    private readonly productRepository: ProductRepository
  ) {}

  async getProductsWithCachedCount(
    userId: number, 
    filters: ProductFilterQueryDto
  ): Promise<PaginatedResponseDto<ProductResponseDto>> {
    
    // Crear clave de cache basada en filtros
    const cacheKey = `products:count:${userId}:${JSON.stringify(filters)}`;
    
    // Intentar obtener count del cache
    let total = await this.cacheManager.get<number>(cacheKey);
    
    if (total === undefined) {
      // Si no está en cache, calcularlo y guardarlo
      total = await this.productRepository.countByUserIdWithFilters(userId, filters);
      await this.cacheManager.set(cacheKey, total, 300); // Cache por 5 minutos
    }
    
    // Obtener solo los datos (sin count)
    const products = await this.productRepository.findByUserIdWithFilters(userId, filters);
    const productDtos = products.map(p => this.toResponseDto(p));
    
    return PaginatedResponseDto.create(productDtos, filters.page, filters.size, total);
  }
}
```

# **9. Actividad Práctica Completa**

## **9.1. Implementación requerida**

Se debe  implementar:

1. **Crear DTOs de paginación**:
   - `PaginationQueryDto` con validaciones
   - `PaginatedResponseDto` con metadatos
   - `ProductFilterQueryDto` extendiendo paginación

2. **Actualizar UserController** con endpoints paginados:
   - `GET /api/users/{id}/products-paginated` (paginación básica)
   - `GET /api/users/{id}/products-filtered` (filtros + paginación)
   - `GET /api/users/{id}/products-infinite` (scroll infinito)

3. **Implementar métodos** en `UserService`:
   - `getProductsByUserIdPaginated()` con metadatos
   - `getProductsByUserIdWithFiltersAndPagination()` combinando todo
   - `getProductsByUserIdInfiniteScroll()` para performance

4. **Actualizar ProductRepository** con consultas TypeORM:
   - `findByOwnerIdPaginated()` usando getManyAndCount()
   - `findByOwnerIdWithFiltersAndPagination()` con QueryBuilder
   - `findByOwnerIdForInfiniteScroll()` solo con getMany()

5. **Validaciones robustas**:
   - Límites de página y tamaño
   - Lista blanca de campos de ordenamiento
   - Validación de filtros

## **9.2. Casos de prueba específicos**

**Probar los siguientes casos**:

```bash
# 1. Paginación básica
GET /api/users/1/products-paginated?page=0&size=5

# 2. Paginación con ordenamiento
GET /api/users/1/products-paginated?page=1&size=3&sortBy=price&sortOrder=DESC

# 3. Filtros con paginación
GET /api/users/1/products-filtered?name=laptop&minPrice=500&page=0&size=3&sortBy=name

# 4. Scroll infinito
GET /api/users/1/products-infinite?page=0&size=10&sortBy=createdAt&sortOrder=DESC

# 5. Ordenamiento por relaciones
GET /api/users/1/products-filtered?page=0&size=5&sortBy=category.name&sortOrder=ASC

# 6. Casos de error
GET /api/users/1/products-paginated?page=-1&size=0  # Error de validación
GET /api/users/1/products-paginated?sortBy=invalidField  # Campo no permitido
GET /api/users/999/products-paginated  # Usuario inexistente
```

## **9.3. Verificaciones técnicas**

1. **SQL generado**: Verificar LIMIT, OFFSET y COUNT en logs de TypeORM
2. **Metadatos**: Confirmar que respuesta incluye page, size, total, totalPages, hasNext, hasPrevious
3. **Performance**: Comparar tiempos con y sin count total
4. **Validaciones**: Probar límites y campos de ordenamiento inválidos
5. **Scroll infinito**: Verificar que hasNext funcione correctamente

# **10. Resultados y Evidencias Requeridas**

## **10.1. Evidencias de implementación**
1. **Captura de DTOs** (PaginationQueryDto, PaginatedResponseDto, ProductFilterQueryDto)
2. **Captura de user.controller.ts** con endpoints paginados implementados
3. **Captura de user.service.ts** con métodos de paginación
4. **Captura de product.repository.ts** con consultas TypeORM paginadas
5. **Captura de logs SQL** mostrando LIMIT, OFFSET y COUNT queries

## **10.2. Evidencias de funcionamiento**
1. **Respuesta paginada**: `GET /api/users/1/products-paginated?page=0&size=3` mostrando metadatos completos
2. **Filtros + paginación**: `GET /api/users/1/products-filtered?name=laptop&page=0&size=2&sortBy=price`
3. **Scroll infinito**: `GET /api/users/1/products-infinite?page=0&size=5` mostrando hasNext
4. **Ordenamiento**: `GET /api/users/1/products-paginated?sortBy=category.name&sortOrder=ASC`
5. **Error handling**: Capturas de validaciones fallando con mensajes descriptivos

## **10.3. Evidencias de performance**
1. **Índices**: Captura de `EXPLAIN ANALYZE` mostrando uso de índices
2. **Comparación**: Tiempos de respuesta con y sin count total
3. **Consultas optimizadas**: Logs mostrando getManyAndCount() vs getMany()

## **10.4. Datos para revisión**

**Usar un dataset de al menos 50 productos**:
- Usuario 1: 20+ productos variados
- Usuario 2: 15+ productos diferentes  
- Precios: $10 - $3000
- Categorías: "Gaming", "Oficina", "Electrónicos", "Libros"
- Nombres: productos buscables ("Laptop Gaming", "Mouse Inalámbrico", etc.)

**Consultas de prueba con volumen**:
1. Primera página de productos (page=0, size=5)
2. Página intermedia (page=2, size=5) para verificar offset
3. Última página para verificar hasNext=false
4. Búsquedas con filtros y pocos/muchos resultados
5. Ordenamiento por precio, nombre, fecha, categoría

# **11. Configuración del Módulo User**

Para que todo funcione correctamente:

Archivo: `users/user.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserController } from './controllers/user.controller';
import { UserService } from './services/user.service';
import { UserRepository } from './repositories/user.repository';
import { User } from './entities/user.entity';

// Importar entidades relacionadas para paginación
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
    ProductRepository, // Inyectar repositorio de productos para paginación
  ],
  exports: [UserService, UserRepository],
})
export class UserModule {}
```

# **12. Conclusiones**

Esta implementación de paginación en NestJS demuestra:

* **Paginación flexible**: Múltiples estrategias (completa, scroll infinito, solo datos)
* **TypeORM QueryBuilder**: Control total sobre consultas SQL generadas
* **DTOs robustos**: Validaciones completas con class-validator
* **Performance optimizada**: getManyAndCount() y getMany() según necesidades
* **Integración completa**: Filtros + paginación + ordenamiento en una sola API
* **Escalabilidad**: Funciona eficientemente con grandes volúmenes de datos
* **Type safety**: Completamente tipado con TypeScript
* **Mantenibilidad**: Código claro, testeable y extensible

El enfoque implementado proporciona una base sólida para aplicaciones NestJS que requieren manejar grandes volúmenes de datos de manera eficiente, manteniendo una excelente experiencia de usuario y siguiendo las mejores prácticas de NestJS y TypeORM.