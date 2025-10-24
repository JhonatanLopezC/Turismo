import streamlit as st
from interfaz import InterfazStreamlit

# Configuración de página - DEBE ser lo primero
st.set_page_config(
    page_title="Turismo Colombia",
    page_icon="./imagenes/favicon.ico",
    initial_sidebar_state="expanded"
)

def main():
    """Función principal de la aplicación."""
    app = InterfazStreamlit()
    app.ejecutar()


if __name__ == "__main__":
    main()

#para ejecutar el codigo colocamos esto en la terminal: streamlit run app.py
