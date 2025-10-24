import os
from typing import List


class Destino:
    """Representa un destino turístico con sus características."""
    
    def __init__(self, nombre: str, tipo: str, actividades: List[str], imagen: str):
        self.nombre = nombre
        self.tipo = tipo
        self.actividades = actividades
        self.imagen = imagen
    
    def coincide_con_interes(self, interes: str) -> bool:
        """Verifica si el destino coincide con el interés del usuario."""
        return self.tipo.lower() == interes.lower()


class RecomendadorTuristico:
    """Maneja la lógica de recomendaciones turísticas."""
    
    def __init__(self):
        self.destinos = self._cargar_destinos()
    
    def _cargar_destinos(self) -> List[Destino]:
        """Carga la lista de destinos disponibles."""
        ruta_imagenes = "imagenes"
        
        datos_destinos = [
            {
                "nombre": "Cartagena",
                "tipo": "Cultura",
                "actividades": ["Ciudad amurallada", "Playas", "Museos"],
                "imagen": os.path.join(ruta_imagenes, "cartagena.jpg")
            },
            {
                "nombre": "San Andrés",
                "tipo": "Aventura",
                "actividades": ["Buceo", "Snorkel", "Kayak"],
                "imagen": os.path.join(ruta_imagenes, "isla-de-san-andres.jpg")
            },
            {
                "nombre": "Eje Cafetero",
                "tipo": "Naturaleza",
                "actividades": ["Paisajes", "Cafetales", "Senderismo"],
                "imagen": os.path.join(ruta_imagenes, "eje_cafetero.jpg")
            },
            {
                "nombre": "Villa de Leyva",
                "tipo": "Cultura",
                "actividades": ["Arquitectura colonial", "Museos", "Fósiles"],
                "imagen": os.path.join(ruta_imagenes, "villa_de_leyva.jpg")
            },
            {
                "nombre": "Santa Marta",
                "tipo": "Aventura",
                "actividades": ["Playas", "Parque Tayrona", "Senderismo"],
                "imagen": os.path.join(ruta_imagenes, "santa_marta.jpg")
            },
            {
                "nombre": "Guatapé",
                "tipo": "Naturaleza",
                "actividades": ["Escalar la piedra", "Paseos en lancha", "Fotografía"],
                "imagen": os.path.join(ruta_imagenes, "guatape.jpg")
            },
            {
                "nombre": "Caño Cristales",
                "tipo": "Naturaleza",
                "actividades": ["Senderismo", "Fotografía", "Exploración ecológica"],
                "imagen": os.path.join(ruta_imagenes, "cano_cristales.jpg")
            },
            {
                "nombre": "Barichara",
                "tipo": "Cultura",
                "actividades": ["Arquitectura colonial", "Caminatas", "Artesanías"],
                "imagen": os.path.join(ruta_imagenes, "barichara.jpg")
            },
            {
                "nombre": "Amazonas",
                "tipo": "Naturaleza",
                "actividades": ["Selva", "Fauna", "Ríos"],
                "imagen": os.path.join(ruta_imagenes, "leticia.jpg")
            },
            {
                "nombre": "Bogotá",
                "tipo": "Cultura",
                "actividades": ["Museos", "Gastronomía", "Historia"],
                "imagen": os.path.join(ruta_imagenes, "bogota.png")
            }
        ]
        
        return [Destino(**datos) for datos in datos_destinos]
    
    def obtener_recomendaciones(self, interes: str) -> List[Destino]:
        """Obtiene destinos que coinciden con el interés especificado."""
        return [destino for destino in self.destinos if destino.coincide_con_interes(interes)]
    
    def obtener_tipos_disponibles(self) -> List[str]:
        """Obtiene los tipos de turismo disponibles."""
        return list(set(destino.tipo for destino in self.destinos))