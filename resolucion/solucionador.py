import re
import streamlit as st
from fpdf import FPDF
import json
from datetime import datetime

HISTORIAL_PATH = "rotacion_pro_1000/resolucion/historial.json"

def resolver_problema(enunciado):
    st.subheader("🧾 Análisis del Problema Escrito")

    datos = {
        "masa": buscar_valor(enunciado, [
            (r"(\d+(\.\d+)?)\s*(kg)", 1),
            (r"(\d+(\.\d+)?)\s*(g)", 0.001)
        ]),
        "radio": buscar_valor(enunciado, [
            (r"(\d+(\.\d+)?)\s*(m)", 1),
            (r"(\d+(\.\d+)?)\s*(cm)", 0.01)
        ]),
        "velocidad": buscar_valor(enunciado, [
            (r"(\d+(\.\d+)?)\s*(rad/s)", 1)
        ]),
        "torque": buscar_valor(enunciado, [
            (r"(\d+(\.\d+)?)\s*(Nm)", 1)
        ]),
        "tiempo": buscar_valor(enunciado, [
            (r"(\d+(\.\d+)?)\s*(s)", 1),
            (r"(\d+(\.\d+)?)\s*(ms)", 0.001)
        ])
    }

    for clave, valor in datos.items():
        st.write(f"{clave.capitalize()}: {valor if valor is not None else 'No encontrado'}")

    pasos = []
    tipo = ""
    resultado = ""

    # CASO 1
    if all(datos[k] is not None for k in ["masa", "radio", "torque", "tiempo"]):
        tipo = "Velocidad angular final"
        m = datos["masa"]
        r = datos["radio"]
        tau = datos["torque"]
        t = datos["tiempo"]

        I = 0.5 * m * r**2
        alpha = tau / I
        omega = alpha * t

        pasos = [
            f"I = 0.5 * {m} * {r}^2 = {I:.4f} kg·m²",
            f"α = {tau} / {I:.4f} = {alpha:.4f} rad/s²",
            f"ω = {alpha:.4f} * {t} = {omega:.4f} rad/s"
        ]
        resultado = f"{omega:.4f} rad/s"
        st.success(f"✅ Velocidad angular final: {resultado}")

    # CASO 2
    elif all(datos[k] is not None for k in ["masa", "radio", "velocidad"]):
        tipo = "Energía cinética rotacional"
        m = datos["masa"]
        r = datos["radio"]
        w = datos["velocidad"]

        I = 0.5 * m * r**2
        K = 0.5 * I * w**2

        pasos = [
            f"I = 0.5 * {m} * {r}^2 = {I:.4f} kg·m²",
            f"K = 0.5 * {I:.4f} * {w}^2 = {K:.4f} J"
        ]
        resultado = f"{K:.4f} J"
        st.success(f"✅ Energía cinética rotacional: {resultado}")

    # CASO 3
    elif all(datos[k] is not None for k in ["masa", "radio", "velocidad"]):
        tipo = "Momento angular"
        m = datos["masa"]
        r = datos["radio"]
        w = datos["velocidad"]

        I = m * r**2
        L = I * w

        pasos = [
            f"I = {m} * {r}^2 = {I:.4f} kg·m²",
            f"L = {I:.4f} * {w} = {L:.4f} kg·m²·rad/s"
        ]
        resultado = f"{L:.4f} kg·m²·rad/s"
        st.success(f"✅ Momento angular: {resultado}")

    else:
        st.warning("⚠️ No se identificó un tipo de problema compatible.")

    if pasos:
        guardar_historial(enunciado, tipo, pasos, resultado)

        if st.button("📥 Descargar solución en PDF"):
            generar_pdf(pasos, "solucion_rotacion.pdf")
            with open("solucion_rotacion.pdf", "rb") as file:
                st.download_button(label="Descargar PDF", data=file, file_name="solucion_rotacion.pdf")

    if st.button("📚 Ver historial de problemas"):
        mostrar_historial()

def buscar_valor(texto, patrones):
    for patron, factor in patrones:
        match = re.search(patron, texto)
        if match:
            return float(match.group(1)) * factor
    return None

def guardar_historial(enunciado, tipo, pasos, resultado):
    try:
        with open(HISTORIAL_PATH, "r") as f:
            historial = json.load(f)
    except:
        historial = []

    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "enunciado": enunciado,
        "tipo": tipo,
        "pasos": pasos,
        "resultado": resultado
    })

    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f, indent=4)

def mostrar_historial():
    try:
        with open(HISTORIAL_PATH, "r") as f:
            historial = json.load(f)
        st.markdown("### 📖 Historial de Problemas")
        for h in reversed(historial[-5:]):  # muestra últimos 5
            st.markdown(f"**{h['fecha']}** - *{h['tipo']}*")
            st.markdown(f"> {h['enunciado']}")
            for paso in h["pasos"]:
                st.code(paso)
            st.success(f"Resultado: {h['resultado']}")
            st.markdown("---")
    except:
        st.info("No hay historial guardado.")

def generar_pdf(pasos, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Solución de Problema de Rotación", ln=1, align='C')
    pdf.ln(5)
    for paso in pasos:
        pdf.multi_cell(0, 10, paso)
    pdf.output(filename)
