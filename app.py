import streamlit as st
from simulaciones import torque_cilindro, masa_cuerda, momento_conservado
from resolucion import solucionador

st.set_page_config(page_title="Rotación Pro 1000", layout="wide")
st.title("🔁 Rotación Pro 1000 - Simulaciones y Resolución de Problemas")

menu = st.sidebar.selectbox("Selecciona módulo", [
    "Cilindro con Torque",
    "Masa Colgante y Cilindro",
    "Conservación de Momento Angular",
    "Resolver problema escrito"
])

if menu == "Cilindro con Torque":
    torque_cilindro.simular()
elif menu == "Masa Colgante y Cilindro":
    masa_cuerda.simular()
elif menu == "Conservación de Momento Angular":
    momento_conservado.simular()
elif menu == "Resolver problema escrito":
    texto = st.text_area("✍️ Escribe tu problema aquí:")
    if texto:
        solucionador.resolver_problema(texto)
