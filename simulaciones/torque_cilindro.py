
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def simular():
    st.subheader("🌀 Cilindro con Torque Aplicado")
    masa = st.slider("Masa del cilindro (kg)", 0.1, 10.0, 2.0)
    radio = st.slider("Radio del cilindro (m)", 0.05, 0.5, 0.1)
    torque = st.slider("Torque aplicado (Nm)", 0.1, 10.0, 1.0)
    tiempo = st.slider("Tiempo (s)", 1, 20, 5)

    I = 0.5 * masa * radio**2
    alpha = torque / I
    t = np.linspace(0, tiempo, 300)
    omega = alpha * t
    theta = 0.5 * alpha * t**2

    st.write(f"Momento de inercia: {I:.4f} kg·m²")
    st.write(f"Aceleración angular: {alpha:.4f} rad/s²")
    st.write(f"Velocidad final: {omega[-1]:.2f} rad/s")
    st.write(f"Ángulo girado: {theta[-1]:.2f} rad")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=omega, mode='lines', name='ω(t)'))
    fig.update_layout(title='Velocidad angular vs tiempo', xaxis_title='t (s)', yaxis_title='ω (rad/s)')
    st.plotly_chart(fig)
