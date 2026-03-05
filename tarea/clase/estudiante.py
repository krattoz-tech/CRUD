class Estudiante:
    """Clase que representa a un estudiante.
    """    
    def __init__(self, id, nombre, correo, promedio):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.promedio = promedio

    def calcular_estado(self):
        """Calcula el estado de 

        Returns
        -------
        _type_
            _description_
        """        
        if self.promedio >= 3.0:
            return "Aprobado"
        else:
            return "Reprobado"

    def mostrar_info(self):
        print(f"ID: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
        print(f"Promedio: {self.promedio}")
        print(f"Estado: {self.calcular_estado()}")