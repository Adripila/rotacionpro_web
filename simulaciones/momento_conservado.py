
import streamlit as st

def simular():
    st.subheader("⛸️ Conservación del Momento Angular")
    m = st.slider("Masa (kg)", 10.0, 100.0, 60.0)
    r1 = st.slider("Radio inicial (m)", 0.2, 1.0, 0.8)
    r2 = st.slider("Radio final (m)", 0.05, r1, 0.3)
    w1 = st.slider("Velocidad inicial (rad/s)", 1.0, 10.0, 3.0)

    I1 = m * r1**2
    I2 = m * r2**2
    w2 = I1 * w1 / I2

    st.write(f"Velocidad final: {w2:.2f} rad/s")
    st.write(f"I₁ω₁ = I₂ω₂ ⇒ {I1:.2f}·{w1:.2f} = {I2:.2f}·{w2:.2f}")
