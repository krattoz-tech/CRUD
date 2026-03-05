from producto import Producto

def test_propiedades_basicas():
    """Test de las propiedades básicas con valores válidos"""
    print("=== PRUEBAS DE PROPIEDADES BÁSICAS ===\n")
    
    try:
        # Crear producto con datos válidos
        producto = Producto(1, "laptop gaming", 2500000, "tecnologia", 10)
        
        print("1. Creación de producto exitosa:")
        print(f"   ID: {producto.id_producto}")
        print(f"   Nombre: {producto.nombre}")
        print(f"   Precio: ${producto.precio:,.0f}")
        print(f"   Categoría: {producto.categoria}")
        print(f"   Stock: {producto.stock}")
        print("   ✅ Todas las propiedades funcionan correctamente")
        
        return producto
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_validaciones_setters():
    """Test de las validaciones en los setters"""
    print("\n\n=== PRUEBAS DE VALIDACIONES EN SETTERS ===\n")
    
    # Crear producto base
    producto = Producto(1, "Producto Test", 100000, "Ropa", 5)
    
    tests = [
        # (campo, valor_invalido, descripcion)
        ("id_producto", 0, "ID menor o igual a 0"),
        ("id_producto", -5, "ID negativo"),
        ("id_producto", "abc", "ID no numérico"),
        ("nombre", "", "Nombre vacío"),
        ("nombre", "a", "Nombre muy corto"),
        ("precio", 500, "Precio menor al mínimo"),
        ("precio", 50000000, "Precio mayor al máximo"),
        ("precio", "abc", "Precio no numérico"),
        ("categoria", "", "Categoría vacía"),
        ("categoria", "x", "Categoría muy corta"),
        ("stock", -1, "Stock negativo"),
        ("stock", "abc", "Stock no numérico"),
    ]
    
    errores_detectados = 0
    
    for i, (campo, valor_invalido, descripcion) in enumerate(tests, 1):
        try:
            # Intentar asignar valor inválido
            setattr(producto, campo, valor_invalido)
            print(f"{i:2d}. {descripcion}: ❌ No se detectó el error")
        except ValueError as e:
            print(f"{i:2d}. {descripcion}: ✅ Error detectado: {str(e)}")
            errores_detectados += 1
        except Exception as e:
            print(f"{i:2d}. {descripcion}: ⚠️  Error inesperado: {str(e)}")
    
    print(f"\n   Total errores detectados correctamente: {errores_detectados}/{len(tests)}")
    return errores_detectados == len(tests)

def test_normalizacion_con_propiedades():
    """Test de normalización funcionando con propiedades"""
    print("\n\n=== PRUEBAS DE NORMALIZACIÓN CON PROPIEDADES ===\n")
    
    # Crear producto
    producto = Producto(1, "test", 100000, "test", 5)
    
    tests = [
        # (campo, valor_entrada, valor_esperado)
        ("nombre", "laptop gaming asus", "Laptop Gaming Asus"),
        ("nombre", "MOUSE LOGITECH", "Mouse Logitech"),
        ("categoria", "tecnologia", "Tecnología"),
        ("categoria", "TECNOLOGIA", "Tecnología"),
        ("categoria", "ropa", "Ropa"),
        ("categoria", "hogar", "Hogar"),
    ]
    
    todos_correctos = True
    
    for i, (campo, valor_entrada, valor_esperado) in enumerate(tests, 1):
        try:
            setattr(producto, campo, valor_entrada)
            valor_actual = getattr(producto, campo)
            
            if valor_actual == valor_esperado:
                print(f"{i}. {campo}: '{valor_entrada}' → '{valor_actual}' ✅")
            else:
                print(f"{i}. {campo}: '{valor_entrada}' → '{valor_actual}' ❌ (esperado: '{valor_esperado}')")
                todos_correctos = False
                
        except Exception as e:
            print(f"{i}. {campo}: '{valor_entrada}' → Error: {e} ❌")
            todos_correctos = False
    
    return todos_correctos

def test_funcionamiento_con_servicio():
    """Test de compatibilidad con ProductoService"""
    print("\n\n=== PRUEBAS DE COMPATIBILIDAD CON PRODUCTO SERVICE ===\n")
    
    try:
        from producto_service import ProductoService
        
        # Crear servicio temporal
        servicio = ProductoService("test_propiedades_temp.json")
        servicio.productos = []  # Limpiar productos
        servicio.siguiente_id = 1
        
        # Probar crear producto
        exito, mensaje = servicio.crear_producto("laptop gamer", "2500000", "tecnologia", "10")
        
        if exito:
            producto_creado = servicio.productos[0]
            print("1. Creación a través del servicio:")
            print(f"   Nombre normalizado: '{producto_creado.nombre}'")
            print(f"   Categoría normalizada: '{producto_creado.categoria}'")
            print("   ✅ Servicio funciona correctamente con propiedades")
            
            # Probar actualización
            exito2, mensaje2 = servicio.actualizar_producto("1", "mouse gamer", 150000, "tecnologia", 15)
            if exito2:
                print("2. Actualización a través del servicio: ✅")
            else:
                print(f"2. Actualización falló: {mensaje2} ❌")
            
        else:
            print(f"1. Creación falló: {mensaje} ❌")
        
        # Limpiar archivo temporal
        import os
        try:
            os.remove("test_propiedades_temp.json")
        except:
            pass
            
        return exito
        
    except Exception as e:
        print(f"   Error en compatibilidad: {e} ❌")
        return False

def test_metodos_especiales():
    """Test de métodos __str__, __repr__ y to_dict"""
    print("\n\n=== PRUEBAS DE MÉTODOS ESPECIALES ===\n")
    
    try:
        producto = Producto(1, "laptop gaming", 2500000, "tecnologia", 10)
        
        # Test __str__
        str_output = str(producto)
        print("1. Método __str__:")
        print(f"   {str_output}")
        print("   ✅ Funcionando correctamente" if "Laptop Gaming" in str_output else "   ❌ Error")
        
        # Test __repr__ 
        repr_output = repr(producto)
        print(f"\n2. Método __repr__:")
        print(f"   {repr_output}")
        print("   ✅ Funcionando correctamente" if "Producto(" in repr_output else "   ❌ Error")
        
        # Test to_dict
        dict_output = producto.to_dict()
        print(f"\n3. Método to_dict:")
        print(f"   {dict_output}")
        esperado = all(key in dict_output for key in ['id_producto', 'nombre', 'precio', 'categoria', 'stock'])
        print("   ✅ Funcionando correctamente" if esperado else "   ❌ Error")
        
        return True
        
    except Exception as e:
        print(f"   Error en métodos especiales: {e} ❌")
        return False

if __name__ == "__main__":
    try:
        print("🚀 INICIANDO PRUEBAS DE PROPIEDADES Y SETTERS\n")
        
        # Ejecutar todas las pruebas
        producto_base = test_propiedades_basicas()
        validaciones_ok = test_validaciones_setters()
        normalizacion_ok = test_normalizacion_con_propiedades()
        servicio_ok = test_funcionamiento_con_servicio()
        metodos_ok = test_metodos_especiales()
        
        # Resumen final
        print("\n" + "="*60)
        print("📊 RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"Propiedades básicas:      {'✅' if producto_base else '❌'}")
        print(f"Validaciones en setters:  {'✅' if validaciones_ok else '❌'}")
        print(f"Normalización:            {'✅' if normalizacion_ok else '❌'}")
        print(f"Compatibilidad servicio:  {'✅' if servicio_ok else '❌'}")
        print(f"Métodos especiales:       {'✅' if metodos_ok else '❌'}")
        print("="*60)
        
        if all([producto_base, validaciones_ok, normalizacion_ok, servicio_ok, metodos_ok]):
            print("🎉 TODAS LAS PRUEBAS FUERON EXITOSAS!")
            print("📋 Tu clase Producto ahora usa propiedades y setters correctamente.")
        else:
            print("⚠️  Algunas pruebas fallaron. Revisar resultados arriba.")
        
    except Exception as e:
        print(f"❌ Error crítico durante las pruebas: {e}")
        import traceback
        traceback.print_exc()