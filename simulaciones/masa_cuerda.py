
import streamlit as st
import numpy as np
import plotly.graph_objects as go

def simular():
    st.subheader("🏋️ Masa colgante que hace girar cilindro")
    m = st.slider("Masa colgante (kg)", 0.1, 10.0, 2.0)
    M = st.slider("Masa del cilindro (kg)", 0.1, 10.0, 3.0)
    R = st.slider("Radio del cilindro (m)", 0.05, 0.5, 0.1)
    t_total = st.slider("Tiempo (s)", 1, 20, 5)
    g = 9.81

    I = 0.5 * M * R**2
    a = (m * g) / (m + I / R**2)
    t = np.linspace(0, t_total, 300)
    v = a * t
    y = 0.5 * a * t**2

    st.write(f"Aceleración: {a:.4f} m/s²")
    st.write(f"Distancia recorrida: {y[-1]:.2f} m")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='y(t)', line=dict(color='orange')))
    fig.update_layout(title='Desplazamiento vs tiempo', xaxis_title='t (s)', yaxis_title='y (m)')
    st.plotly_chart(fig)
