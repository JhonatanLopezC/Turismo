from typing import Dict, List, Optional
from destinos import Destino, RecomendadorTuristico


class NodoDecision:
    """Nodo del árbol de decisiones."""
    
    def __init__(self, pregunta: str, opciones: Dict[str, 'NodoDecision'] = None, destino: str = None):
        self.pregunta = pregunta
        self.opciones = opciones or {}
        self.destino = destino
    
    def es_hoja(self) -> bool:
        """Verifica si el nodo es una hoja (tiene destino)."""
        return self.destino is not None


class ArbolDecisiones:
    """Implementa un árbol de decisiones para recomendar destinos."""
    
    def __init__(self):
        self.recomendador = RecomendadorTuristico()
        self.raiz = self._construir_arbol()
        self.historial_respuestas = []
    
    def _construir_arbol(self) -> NodoDecision:
        """Construye el árbol de decisiones."""
        # Nodos hoja (destinos finales)
        cartagena = NodoDecision("", destino="Cartagena")
        bogota = NodoDecision("", destino="Bogotá")
        san_andres = NodoDecision("", destino="San Andrés")
        santa_marta = NodoDecision("", destino="Santa Marta")
        eje_cafetero = NodoDecision("", destino="Eje Cafetero")
        amazonas = NodoDecision("", destino="Amazonas")
        
        # Nodos de decisión nivel 2
        cultura_historia = NodoDecision(
            "¿Prefieres arquitectura colonial o museos modernos?",
            {"Colonial": cartagena, "Moderno": bogota}
        )
        
        aventura_agua = NodoDecision(
            "¿Prefieres actividades en el mar o montaña?",
            {"Mar": san_andres, "Montaña": santa_marta}
        )
        
        naturaleza_tipo = NodoDecision(
            "¿Te gusta más el café o la selva?",
            {"Café": eje_cafetero, "Selva": amazonas}
        )
        
        # Nodo raíz
        raiz = NodoDecision(
            "¿Qué tipo de experiencia buscas?",
            {
                "Cultura": cultura_historia,
                "Aventura": aventura_agua,
                "Naturaleza": naturaleza_tipo
            }
        )
        
        return raiz
    
    def obtener_pregunta_actual(self, nodo: NodoDecision = None) -> str:
        """Obtiene la pregunta del nodo actual."""
        if nodo is None:
            nodo = self.raiz
        return nodo.pregunta
    
    def obtener_opciones(self, nodo: NodoDecision = None) -> List[str]:
        """Obtiene las opciones disponibles del nodo actual."""
        if nodo is None:
            nodo = self.raiz
        return list(nodo.opciones.keys())
    
    def navegar(self, respuesta: str, nodo_actual: NodoDecision = None) -> NodoDecision:
        """Navega por el árbol según la respuesta del usuario."""
        if nodo_actual is None:
            nodo_actual = self.raiz
        
        self.historial_respuestas.append(respuesta)
        return nodo_actual.opciones.get(respuesta)
    
    def obtener_recomendacion(self, nodo: NodoDecision) -> Optional[Destino]:
        """Obtiene el destino recomendado si llegamos a una hoja."""
        if nodo and nodo.es_hoja():
            destinos = self.recomendador.destinos
            for destino in destinos:
                if destino.nombre == nodo.destino:
                    return destino
        return None
    
    def reiniciar(self):
        """Reinicia el árbol de decisiones."""
        self.historial_respuestas = []