from producto import Producto
import json
import os

class ProductoService:
    """
    Clase que maneja las operaciones CRUD para productos
    """
    def __init__(self, archivo_datos="productos.json"):
        self.archivo_datos = archivo_datos
        self.productos = []
        self.siguiente_id = 1
        # Cargar datos existentes o crear productos de ejemplo
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga los datos desde el archivo JSON o crea productos de ejemplo"""
        try:
            if os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self.siguiente_id = datos.get('siguiente_id', 1)
                    
                    # Recrear objetos Producto desde los datos guardados
                    for producto_data in datos.get('productos', []):
                        producto = Producto(
                            producto_data['id_producto'],
                            producto_data['nombre'],
                            producto_data['precio'],
                            producto_data['categoria'],
                            producto_data['stock']
                        )
                        self.productos.append(producto)
                
                print(f"✅ Datos cargados desde {self.archivo_datos}")
            else:
                # Si no existe el archivo, crear productos de ejemplo
                self._agregar_productos_ejemplo()
                self._guardar_datos()  # Guardar los productos de ejemplo
                print(f"📁 Archivo {self.archivo_datos} creado con productos de ejemplo")
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"⚠️  Error al cargar datos: {e}. Creando productos de ejemplo...")
            self.productos = []
            self.siguiente_id = 1
            self._agregar_productos_ejemplo()
            self._guardar_datos()
        except Exception as e:
            print(f"❌ Error inesperado al cargar datos: {e}")
            self.productos = []
            self.siguiente_id = 1
    
    def __del__(self):
        """Destructor: guarda los datos automáticamente cuando se destruye el objeto"""
        try:
            self._guardar_datos()
        except:
            pass  # Ignorar errores en el destructor
    
    def _guardar_datos(self):
        """Guarda los datos actuales en el archivo JSON"""
        try:
            datos = {
                'siguiente_id': self.siguiente_id,
                'productos': [producto.to_dict() for producto in self.productos]
            }
            
            with open(self.archivo_datos, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
    
    def _agregar_productos_ejemplo(self):
        """Agrega algunos productos de ejemplo para demostración"""
        productos_ejemplo = [
            ("Laptop Dell", 3500000, "Tecnología", 10),
            ("Mouse Logitech", 85000, "Tecnología", 25), 
            ("Teclado Mecánico", 350000, "Tecnología", 15),
            ("Monitor LG", 1200000, "Tecnología", 8),
        ]
        
        for nombre, precio, categoria, stock in productos_ejemplo:
            producto = Producto(self.siguiente_id, nombre, precio, categoria, stock)
            self.productos.append(producto)
            self.siguiente_id += 1
            
            
    #################### #########################
    def crear_producto(self, nombre, precio, categoria, stock):
        """
        Crea un nuevo producto y lo agrega a la lista
        """
        try:
            # Validar datos
            errores = Producto.validar_datos(nombre, precio, categoria, stock)
            if errores:
                raise ValueError("Errores de validación: " + "; ".join(errores))
            
            # Verificar si ya existe un producto con el mismo nombre
            if self._existe_producto_por_nombre(nombre.strip()):
                raise ValueError(f"Ya existe un producto con el nombre '{nombre.strip()}'")
            
            # Limpiar y convertir precio
            precio_limpio = str(precio).replace(',', '').replace('.', '').replace(' ', '')
            precio_float = float(precio_limpio)
            
            # Crear el producto
            producto = Producto(
                self.siguiente_id,
                nombre.strip(),
                precio_float,
                categoria.strip(),
                int(stock)
            )
            
            self.productos.append(producto)
            self.siguiente_id += 1
            
            # Guardar cambios en archivo
            self._guardar_datos()
            
            return True, f"Producto '{producto.nombre}' creado exitosamente con ID {producto.id_producto}"
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
        
    ###########################   ############################   
    def listar_productos(self):
        """
        Lista todos los productos disponibles
        """
        try:
            if not self.productos:
                return True, "No hay productos registrados"
            
            lista = "=== LISTA DE PRODUCTOS ===\n"
            for producto in self.productos:
                lista += f"{producto}\n"
            
            return True, lista
            
        except Exception as e:
            return False, f"Error al listar productos: {str(e)}"
    
    def buscar_producto_por_id(self, id_producto):
        """
        Busca un producto por su ID
        """
        try:
            id_int = int(id_producto)
            for producto in self.productos:
                if producto.id_producto == id_int:
                    return producto
            return None
        except (ValueError, TypeError):
            return None
        
        
    #############################   ############################   
    def actualizar_producto(self, id_producto, nombre=None, precio=None, categoria=None, stock=None):
        """
        Actualiza un producto existente
        """
        try:
            producto = self.buscar_producto_por_id(id_producto)
            if not producto:
                return False, f"No se encontró un producto con ID {id_producto}"
            
            # Preparar datos para validación (usar valores actuales si no se proporcionan nuevos)
            nuevo_nombre = nombre.strip() if nombre else producto.nombre
            # Limpiar precio si se proporciona uno nuevo
            if precio is not None:
                precio_limpio = str(precio).replace(',', '').replace('.', '').replace(' ', '')
                nuevo_precio = float(precio_limpio)
            else:
                nuevo_precio = producto.precio
            nueva_categoria = categoria.strip() if categoria else producto.categoria
            nuevo_stock = stock if stock is not None else producto.stock
            
            # Validar nuevos datos
            errores = Producto.validar_datos(nuevo_nombre, nuevo_precio, nueva_categoria, nuevo_stock)
            if errores:
                raise ValueError("Errores de validación: " + "; ".join(errores))
            
            # Verificar nombre duplicado (solo si el nombre cambió)
            if nuevo_nombre != producto.nombre and self._existe_producto_por_nombre(nuevo_nombre):
                raise ValueError(f"Ya existe un producto con el nombre '{nuevo_nombre}'")
            
            # Actualizar producto
            producto.nombre = nuevo_nombre
            producto.precio = nuevo_precio
            producto.categoria = nueva_categoria
            producto.stock = int(nuevo_stock)
            
            # Guardar cambios en archivo
            self._guardar_datos()
            
            return True, f"Producto ID {id_producto} actualizado exitosamente"
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    #############################   ############################   
    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por su ID
        """
        try:
            producto = self.buscar_producto_por_id(id_producto)
            
            if not producto:
                return False, f"No se encontró un producto con ID {id_producto}"
            
            nombre_producto = producto.nombre
            self.productos.remove(producto)
            
            # Guardar cambios en archivo
            self._guardar_datos()
            
            return True, f"Producto '{nombre_producto}' eliminado exitosamente"
            
        except Exception as e:
            return False, f"Error al eliminar producto: {str(e)}"
    
    def _existe_producto_por_nombre(self, nombre):
        """
        Verifica si ya existe un producto con el nombre dado
        """
        nombre_lower = nombre.lower()
        return any(producto.nombre.lower() == nombre_lower for producto in self.productos)
    
    def obtener_estadisticas(self):
        """
        Obtiene estadísticas básicas de los productos
        """
        try:
            if not self.productos:
                return "No hay productos para mostrar estadísticas"
            
            total_productos = len(self.productos)
            valor_total_inventario = sum(p.precio * p.stock for p in self.productos)
            stock_total = sum(p.stock for p in self.productos)
            
            # Categorías únicas
            categorias = set(p.categoria for p in self.productos)
            
            estadisticas = f"""
=== ESTADÍSTICAS DEL INVENTARIO ===
Total de productos: {total_productos}
Valor total del inventario: ${valor_total_inventario:.2f}
Stock total: {stock_total} unidades
Categorías disponibles: {', '.join(categorias)}
"""
            return estadisticas
            
        except Exception as e:
            return f"Error al calcular estadísticas: {str(e)}"
