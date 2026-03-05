class Producto:
    """
    Clase que representa un producto en el sistema CRUD
    """
    def __init__(self, id_producto, nombre, precio, categoria, stock):
        # Usar los setters para validar al crear el objeto
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
    
    # Propiedades para id_producto
    @property
    def id_producto(self):
        return self._id_producto
    
    @id_producto.setter
    def id_producto(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("El ID debe ser un número entero mayor que 0")
        self._id_producto = value
    
    # Propiedades para nombre
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not value or len(str(value).strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        self._nombre = self._normalizar_nombre(value)
    
    # Propiedades para precio
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, value):
        try:
            # Convertir a string para procesamiento
            precio_str = str(value).strip()
            
            # Detectar si es un decimal verdadero o formato colombiano
            if '.' in precio_str and precio_str.count('.') == 1:
                parts = precio_str.split('.')
                # Si la parte decimal tiene 1-2 dígitos, es decimal verdadero
                # Si tiene exactamente 3 dígitos, es formato colombiano de miles
                if len(parts) == 2 and parts[0].replace(',', '').replace(' ', '').isdigit() and parts[1].isdigit():
                    if len(parts[1]) <= 2:
                        # Es un decimal válido (ej: 25000.5, 1500.50)
                        precio_float = float(precio_str.replace(',', '').replace(' ', ''))
                    else:
                        # Formato colombiano (ej: 1.000, 10.000)
                        precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                        precio_float = float(precio_limpio)
                else:
                    # Formato colombiano (múltiples puntos o casos especiales)
                    precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                    precio_float = float(precio_limpio)
            else:
                # Sin punto o múltiples puntos - limpiar formato colombiano
                precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                precio_float = float(precio_limpio)
            
            # Validar rango de precios en pesos colombianos (COP)
            if precio_float < 1000:
                raise ValueError("El precio debe ser mínimo $1.000 COP")
            elif precio_float > 45000000:
                raise ValueError("El precio debe ser máximo $45.000.000 COP")
            
            self._precio = precio_float
        except (ValueError, TypeError) as e:
            if "precio debe ser" in str(e):
                raise e
            else:
                raise ValueError("El precio debe ser un número válido (ej: 15000 o 1500000)")
    
    # Propiedades para categoria
    @property
    def categoria(self):
        return self._categoria
    
    @categoria.setter
    def categoria(self, value):
        if not value or len(str(value).strip()) < 2:
            raise ValueError("La categoría debe tener al menos 2 caracteres")
        self._categoria = self._normalizar_categoria(value)
    
    # Propiedades para stock
    @property
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, value):
        try:
            # Validar que no sea un decimal
            value_str = str(value).strip()
            if '.' in value_str and not value_str.endswith('.0'):
                # Si tiene decimales que no sean .0, rechazar
                raise ValueError("El stock debe ser un número entero, no decimal")
            
            stock_int = int(float(value))  # Usar float primero para manejar "5.0"
            if stock_int < 0:
                raise ValueError("El stock no puede ser negativo")
            self._stock = stock_int
        except (ValueError, TypeError) as e:
            if "stock" in str(e).lower():
                raise e
            else:
                raise ValueError("El stock debe ser un número entero válido")
    
    def _normalizar_nombre(self, nombre):
        """
        Normaliza el nombre para que tenga el formato correcto
        - Cada palabra con la primera letra en mayúscula
        - Limpia espacios múltiples
        """
        if not nombre:
            return nombre
        
        # Limpiar espacios múltiples y convertir a mayúscula inicial
        nombre_limpio = ' '.join(nombre.strip().split())
        
        # Manejar casos especiales
        palabras = []
        for palabra in nombre_limpio.split(' '):
            if palabra:
                # Para palabras que empiezan con número o símbolo especial
                if palabra[0].isdigit() or palabra[0] in '%$#@':
                    # Para casos como "100%" - preservar tal como está
                    palabras.append(palabra)
                # Para palabras con apostrofes como "Niño's", manejar especialmente
                elif "'" in palabra:
                    partes = palabra.split("'")
                    palabra_normalizada = "'".join([partes[0].capitalize()] + [p.lower() if len(p) <= 2 else p.capitalize() for p in partes[1:]])
                    palabras.append(palabra_normalizada)
                # Para palabras con guiones, capitalizar cada parte
                elif "-" in palabra:
                    partes_guion = palabra.split("-")
                    palabra_normalizada = "-".join([parte.capitalize() for parte in partes_guion if parte])
                    palabras.append(palabra_normalizada)
                else:
                    palabras.append(palabra.capitalize())
        
        return ' '.join(palabras)
    
    def _normalizar_categoria(self, categoria):
        """
        Normaliza la categoría para que tenga el formato correcto
        - Convierte 'tecnologia' (sin tilde) a 'Tecnología' (con tilde)
        - Formatea la primera letra en mayúscula
        """
        if not categoria:
            return categoria
        
        # Limpiar espacios
        categoria = categoria.strip()
        
        # Normalizar específicamente "tecnología" sin importar mayúsculas/minúsculas o tildes
        categoria_lower = categoria.lower()
        if categoria_lower in ['tecnologia', 'tecnología']:
            return 'Tecnología'
        
        # Para otras categorías, solo formatear la primera letra en mayúscula
        return categoria.capitalize()
    
    def __str__(self):
        # Formatear precio con puntos como separadores de miles (formato colombiano)
        precio_formateado = f"{self._precio:,.0f}".replace(',', '.')
        return f"ID: {self._id_producto}, Nombre: {self._nombre}, Precio: ${precio_formateado} COP, Categoría: {self._categoria}, Stock: {self._stock}"
    
    def __repr__(self):
        return f"Producto({self._id_producto}, '{self._nombre}', {self._precio}, '{self._categoria}', {self._stock})"
    
    def to_dict(self):
        """Convierte el producto a diccionario para facilitar el manejo"""
        return {
            'id_producto': self._id_producto,
            'nombre': self._nombre,
            'precio': self._precio,
            'categoria': self._categoria,
            'stock': self._stock
        }
    
    @staticmethod
    def validar_datos(nombre, precio, categoria, stock):
        """
        Valida los datos del producto antes de crear/actualizar
        Usa las mismas validaciones que los setters
        """
        errores = []
        
        # Validar nombre
        if not nombre or len(str(nombre).strip()) < 2:
            errores.append("El nombre debe tener al menos 2 caracteres")
        
        # Validar precio
        try:
            precio_str = str(precio).strip()
            if '.' in precio_str and precio_str.count('.') == 1:
                parts = precio_str.split('.')
                if len(parts) == 2 and parts[0].replace(',', '').replace(' ', '').isdigit() and parts[1].isdigit():
                    if len(parts[1]) <= 2:
                        precio_float = float(precio_str.replace(',', '').replace(' ', ''))
                    else:
                        precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                        precio_float = float(precio_limpio)
                else:
                    precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                    precio_float = float(precio_limpio)
            else:
                precio_limpio = precio_str.replace(',', '').replace('.', '').replace(' ', '')
                precio_float = float(precio_limpio)
            
            if precio_float < 1000:
                errores.append("El precio debe ser mínimo $1.000 COP")
            elif precio_float > 45000000:
                errores.append("El precio debe ser máximo $45.000.000 COP")
        except (ValueError, TypeError):
            errores.append("El precio debe ser un número válido")
        
        # Validar categoria
        if not categoria or len(str(categoria).strip()) < 2:
            errores.append("La categoría debe tener al menos 2 caracteres")
        
        # Validar stock
        try:
            stock_int = int(stock)
            if stock_int < 0:
                errores.append("El stock no puede ser negativo")
        except (ValueError, TypeError):
            errores.append("El stock debe ser un número entero válido")
        
        return errores