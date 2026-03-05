from producto_service import ProductoService
import os
import sys

class MenuCRUD:
    """
    Clase que maneja el menú principal del sistema CRUD
    """
    def __init__(self):
        self.service = ProductoService()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("    SISTEMA CRUD DE PRODUCTOS")
        print("="*50)
        print("1. Crear producto")
        print("2. Listar productos")
        print("3. Actualizar producto") 
        print("4. Eliminar producto")
        print("5. Buscar producto por ID")
        print("6. Ver estadísticas")
        print("7. Salir")
        print("="*50)
    
    def obtener_opcion(self):
        """Obtiene y valida la opción del usuario"""
        try:
            opcion = input("Seleccione una opción (1-7): ").strip()
            if opcion in ['1', '2', '3', '4', '5', '6', '7']:
                return opcion
            else:
                print("❌ Por favor ingrese una opción válida (1-7)")
                return None
        except Exception as e:
            print(f"❌ Error al leer la opción: {e}")
            return None
    
    def crear_producto_menu(self):
        """Menú para crear un nuevo producto"""
        print("\n=== CREAR NUEVO PRODUCTO ===")
        try:
            nombre = input("Nombre del producto: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return
            
            print("💰 Ingrese el precio en pesos colombianos (COP)")
            print("   Rango válido: $1.000 - $45.000.000")
            print("   Ejemplos: 15000, 250000, 1500000")
            precio = input("Precio del producto (COP): ").strip()
            categoria = input("Categoría del producto: ").strip()
            stock = input("Stock del producto: ").strip()
            
            exito, mensaje = self.service.crear_producto(nombre, precio, categoria, stock)
            
            if exito:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ {mensaje}")
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def listar_productos_menu(self):
        """Menú para listar productos"""
        print("\n=== LISTAR PRODUCTOS ===")
        try:
            exito, mensaje = self.service.listar_productos()
            if exito:
                print(mensaje)
            else:
                print(f"❌ {mensaje}")
        except Exception as e:
            print(f"❌ Error al listar productos: {e}")
    
    def actualizar_producto_menu(self):
        """Menú para actualizar un producto"""
        print("\n=== ACTUALIZAR PRODUCTO ===")
        try:
            # Mostrar productos disponibles
            exito, lista = self.service.listar_productos()
            if exito and "No hay productos" not in lista:
                print(lista)
            else:
                print("❌ No hay productos para actualizar")
                return
            
            id_producto = input("\nIngrese el ID del producto a actualizar: ").strip()
            if not id_producto:
                print("❌ Debe ingresar un ID")
                return
            
            # Buscar el producto actual
            producto_actual = self.service.buscar_producto_por_id(id_producto)
            if not producto_actual:
                print(f"❌ No se encontró un producto con ID {id_producto}")
                return
            
            print(f"\nProducto actual: {producto_actual}")
            print("Presione Enter para mantener el valor actual")
            print("💰 Para precios: rango válido $1.000 - $45.000.000 COP")
            
            # Obtener nuevos valores
            nombre = input(f"Nuevo nombre ({producto_actual.nombre}): ").strip()
            precio_input = input(f"Nuevo precio en COP ({producto_actual.precio:,.0f}): ").strip()
            categoria = input(f"Nueva categoría ({producto_actual.categoria}): ").strip()
            stock_input = input(f"Nuevo stock ({producto_actual.stock}): ").strip()
            
            # Convertir valores vacíos a None
            precio = float(precio_input) if precio_input else None
            stock = int(stock_input) if stock_input else None
            nombre = nombre if nombre else None
            categoria = categoria if categoria else None
            
            exito, mensaje = self.service.actualizar_producto(id_producto, nombre, precio, categoria, stock)
            
            if exito:
                print(f"✅ {mensaje}")
            else:
                print(f"❌ {mensaje}")
                
        except ValueError as e:
            print(f"❌ Error en los datos ingresados: {e}")
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def eliminar_producto_menu(self):
        """Menú para eliminar un producto"""
        print("\n=== ELIMINAR PRODUCTO ===")
        try:
            # Mostrar productos disponibles
            exito, lista = self.service.listar_productos()
            if exito and "No hay productos" not in lista:
                print(lista)
            else:
                print("❌ No hay productos para eliminar")
                return
            
            id_producto = input("\nIngrese el ID del producto a eliminar: ").strip()
            if not id_producto:
                print("❌ Debe ingresar un ID")
                return
            
            # Buscar el producto antes de eliminar
            producto = self.service.buscar_producto_por_id(id_producto)
            if not producto:
                print(f"❌ No se encontró un producto con ID {id_producto}")
                return
            
            print(f"\nProducto a eliminar: {producto}")
            confirmacion = input("¿Está seguro de eliminar este producto? (s/n): ").strip().lower()
            
            if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
                exito, mensaje = self.service.eliminar_producto(id_producto)
                if exito:
                    print(f"✅ {mensaje}")
                else:
                    print(f"❌ {mensaje}")
            else:
                print("❌ Eliminación cancelada")
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def buscar_producto_menu(self):
        """Menú para buscar un producto por ID"""
        print("\n=== BUSCAR PRODUCTO POR ID ===")
        try:
            id_producto = input("Ingrese el ID del producto: ").strip()
            if not id_producto:
                print("❌ Debe ingresar un ID")
                return
            
            producto = self.service.buscar_producto_por_id(id_producto)
            if producto:
                print(f"\n✅ Producto encontrado:")
                print(f"   {producto}")
            else:
                print(f"❌ No se encontró un producto con ID {id_producto}")
                
        except KeyboardInterrupt:
            print("\n❌ Operación cancelada por el usuario")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def mostrar_estadisticas_menu(self):
        """Muestra las estadísticas del inventario"""
        print("\n=== ESTADÍSTICAS DEL INVENTARIO ===")
        try:
            estadisticas = self.service.obtener_estadisticas()
            print(estadisticas)
        except Exception as e:
            print(f"❌ Error al mostrar estadísticas: {e}")
    
    def pausar(self):
        """Pausa la ejecución hasta que el usuario presione Enter"""
        input("\nPresione Enter para continuar...")
    
    def ejecutar(self):
        """Ejecuta el bucle principal del menú"""
        print("🚀 Iniciando Sistema CRUD de Productos...")
        
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = self.obtener_opcion()
                
                if opcion is None:
                    self.pausar()
                    continue
                
                if opcion == '1':
                    self.crear_producto_menu()
                elif opcion == '2':
                    self.listar_productos_menu()
                elif opcion == '3':
                    self.actualizar_producto_menu()
                elif opcion == '4':
                    self.eliminar_producto_menu()
                elif opcion == '5':
                    self.buscar_producto_menu()
                elif opcion == '6':
                    self.mostrar_estadisticas_menu()
                elif opcion == '7':
                    print("\n👋 ¡Gracias por usar el Sistema CRUD de Productos!")
                    print("   Guardando datos...")
                    self.service._guardar_datos()  # Guardar datos antes de salir
                    print("   Saliendo del sistema...")
                    break
                
                if opcion != '7':
                    self.pausar()
                    
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupción detectada. Guardando datos...")
                self.service._guardar_datos()  # Guardar datos antes de salir
                print("👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado en el menú principal: {e}")
                self.pausar()

def main():
    """Función principal del programa"""
    try:
        menu = MenuCRUD()
        menu.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico al iniciar la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
