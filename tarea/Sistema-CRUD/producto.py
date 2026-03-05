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
            # Limpiar el precio de posibles caracteres no numéricos
            precio_limpio = str(value).replace(',', '').replace('.', '').replace(' ', '')
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
            stock_int = int(value)
            if stock_int < 0:
                raise ValueError("El stock no puede ser negativo")
            self._stock = stock_int
        except (ValueError, TypeError) as e:
            if "stock no puede" in str(e):
                raise e
            else:
                raise ValueError("El stock debe ser un número entero válido")
    
    def _normalizar_nombre(self, nombre):
        """
        Normaliza el nombre para que tenga el formato correcto
        - Cada palabra con la primera letra en mayúscula
        """
        if not nombre:
            return nombre
        
        # Limpiar espacios y convertir a title case
        return nombre.strip().title()
    
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
        return f"ID: {self._id_producto}, Nombre: {self._nombre}, Precio: ${self._precio:,.0f} COP, Categoría: {self._categoria}, Stock: {self._stock}"
    
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
            precio_limpio = str(precio).replace(',', '').replace('.', '').replace(' ', '')
            precio_float = float(precio_limpio)
            
            if precio_float < 1000:
                errores.append("El precio debe ser mínimo $1.000 COP")
            elif precio_float > 45000000:
                errores.append("El precio debe ser máximo $45.000.000 COP")
        except (ValueError, TypeError):
            errores.append("El precio debe ser un número válido (ej: 15000 o 1500000)")
        
        # Validar categoría
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
    
    @staticmethod
    def _normalizar_nombre_estatico(nombre):
        """
        Versión estática del método de normalización de nombres
        """
        if not nombre:
            return nombre
        
        # Limpiar espacios y convertir a title case
        return nombre.strip().title()
    
    @staticmethod
    def _normalizar_categoria_estatica(categoria):
        """
        Versión estática del método de normalización para usar en validaciones
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
