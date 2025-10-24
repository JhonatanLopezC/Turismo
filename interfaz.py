import streamlit as st
from destinos import RecomendadorTuristico, Destino
from arbol_decisiones import ArbolDecisiones
from typing import List

class InterfazStreamlit:
    """Maneja la interfaz de usuario con Streamlit."""
    
    def __init__(self):
        self.recomendador = RecomendadorTuristico()
        self.arbol = ArbolDecisiones()
    
    def mostrar_titulo(self):
        """Muestra el título y subtítulo de la aplicación."""
        st.title("🌎 Recomendador Turístico Colombiano")
        st.subheader("Descubre destinos según tus intereses")
    
    def obtener_seleccion_usuario(self) -> str:
        """Obtiene la selección del tipo de turismo del usuario."""
        tipos_disponibles = self.recomendador.obtener_tipos_disponibles()
        return st.selectbox("¿Qué tipo de turismo te interesa?", tipos_disponibles)
    
    def mostrar_recomendaciones(self, interes: str):
        """Muestra las recomendaciones basadas en el interés del usuario."""
        recomendaciones = self.recomendador.obtener_recomendaciones(interes)
        
        st.markdown(f"### 🧭 Recomendaciones para turismo de {interes}")
        
        for destino in recomendaciones:
            self._mostrar_destino(destino)
    
    def _mostrar_destino(self, destino: Destino):
        """Muestra la información de un destino específico."""
        st.image(destino.imagen, caption=destino.nombre, use_container_width=True)
        st.markdown(f"**📍 {destino.nombre}**")
        st.write("Actividades destacadas:")
        st.write(", ".join(destino.actividades))
        st.markdown("---")
    
    def recopilar_informacion_usuario(self):
        """Recopila información personal del usuario para recomendaciones personalizadas."""
        st.markdown("### 👤 Cuéntanos sobre tu viaje")
        
        with st.form("info_usuario"):
            nombre = st.text_input("¿Cómo te llamas?", placeholder="Tu nombre")
            edad = st.slider("¿Cuál es tu edad?", 18, 80, 30)
            
            col1, col2 = st.columns(2)
            with col1:
                dias = st.number_input("¿Cuántos días planeas quedarte?", 1, 30, 3)
            with col2:
                presupuesto = st.selectbox("¿Cuál es tu presupuesto?", 
                    ["Económico ($100-300)", "Moderado ($300-600)", "Premium ($600+)"])
            
            gustos = st.multiselect("¿Qué te gusta más?", 
                ["Playas", "Montañas", "Historia", "Gastronomía", "Arte", "Naturaleza", "Aventura"])
            
            submitted = st.form_submit_button("✈️ Obtener Recomendación")
            
            if submitted and nombre and gustos:
                st.session_state.perfil_usuario = {
                    "nombre": nombre,
                    "edad": edad,
                    "dias": dias,
                    "presupuesto": presupuesto,
                    "gustos": gustos
                }
                return True
        return False
    
    def mostrar_recomendacion_personalizada(self):
        """Muestra recomendación basada en el perfil del usuario."""
        perfil = st.session_state.perfil_usuario
        
        st.markdown(f"### 🎯 Recomendación para {perfil['nombre']}")
        
        # Lógica de recomendación personalizada
        destinos_recomendados = []
        
        for destino in self.recomendador.destinos:
            puntuacion = 0
            
            # Puntuación por gustos
            if "Historia" in perfil['gustos'] and destino.tipo == "Cultura":
                puntuacion += 3
            if "Aventura" in perfil['gustos'] and destino.tipo == "Aventura":
                puntuacion += 3
            if "Naturaleza" in perfil['gustos'] and destino.tipo == "Naturaleza":
                puntuacion += 3
            
            # Puntuación por actividades específicas
            for gusto in perfil['gustos']:
                for actividad in destino.actividades:
                    if gusto.lower() in actividad.lower():
                        puntuacion += 2
            
            # Ajuste por presupuesto
            if "Económico" in perfil['presupuesto']:
                if destino.nombre in ["Villa de Leyva", "Barichara"]:
                    puntuacion += 1
            elif "Premium" in perfil['presupuesto']:
                if destino.nombre in ["San Andrés", "Cartagena"]:
                    puntuacion += 1
            
            if puntuacion > 0:
                destinos_recomendados.append((destino, puntuacion))
        
        # Ordenar por puntuación
        destinos_recomendados.sort(key=lambda x: x[1], reverse=True)
        
        if destinos_recomendados:
            mejor_destino = destinos_recomendados[0][0]
            
            st.success(f"🎉 ¡Hola {perfil['nombre']}! Basado en tus gustos, te recomendamos:")
            
            # Mostrar información personalizada
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("👤 Edad", f"{perfil['edad']} años")
                st.metric("📅 Días", perfil['dias'])
                st.metric("💰 Presupuesto", perfil['presupuesto'].split('(')[0])
            
            with col2:
                st.write("**🎯 Tus intereses:**")
                for gusto in perfil['gustos']:
                    st.write(f"• {gusto}")
            
            st.markdown("---")
            self._mostrar_destino(mejor_destino)
            
            # Mostrar alternativas
            if len(destinos_recomendados) > 1:
                st.markdown("### 🔄 Otras opciones para ti:")
                for destino, _ in destinos_recomendados[1:3]:
                    with st.expander(f"📍 {destino.nombre}"):
                        st.write(f"**Tipo:** {destino.tipo}")
                        st.write(f"**Actividades:** {', '.join(destino.actividades)}")
        else:
            st.warning("No encontramos destinos que coincidan exactamente con tus gustos.")
        
        if st.button("🔄 Nueva consulta"):
            del st.session_state.perfil_usuario
            st.rerun()
    
    def mostrar_recomendacion_arbol(self):
        """Muestra recomendación usando información del usuario o árbol de decisiones."""
        if 'perfil_usuario' not in st.session_state:
            if self.recopilar_informacion_usuario():
                st.rerun()
        else:
            self.mostrar_recomendacion_personalizada()
    
    def ejecutar(self):
        """Ejecuta la aplicación completa."""
        self.mostrar_titulo()
        
        modo = st.radio("Elige el modo de recomendación:", 
                       ["🌳 Recomendación Inteligente", "📋 Filtro por Categoría"])
        
        if modo == "🌳 Recomendación Inteligente":
            self.mostrar_recomendacion_arbol()
        else:
            interes = self.obtener_seleccion_usuario()
            if interes:
                self.mostrar_recomendaciones(interes)