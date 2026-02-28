import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("AC Circuit Lab Simulator")

st.sidebar.header("Experiment Selection")
experiment = st.sidebar.radio("Choose an experiment:", ["① RC/RL Time Constant", "② Filter Frequency Response", "③ RLC Resonance"])

if experiment == "① RC/RL Time Constant":
    st.header("① RC or RL Time Constant Measurement")
    circuit_type = st.radio("Select Circuit:", ["RC Circuit", "RL Circuit"])

    if circuit_type == "RC Circuit":
        R = st.slider("Resistance R (Ω)", 100, 5000, 1000)
        C = st.slider("Capacitance C (μF)", 1, 100, 10) * 1e-6
        tau = R * C
    else:
        R = st.slider("Resistance R (Ω)", 10, 1000, 100)
        L = st.slider("Inductance L (mH)", 1, 100, 10) * 1e-3
        tau = L / R

    t = np.linspace(0, 5 * tau, 500)
    v = 1 - np.exp(-t / tau)

    st.write(f"**Time Constant τ = {tau * 1000:.2f} ms**")

    fig, ax = plt.subplots()
    ax.plot(t * 1000, v)
    ax.axhline(0.63, color='r', linestyle='--', label='63% Level')
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Normalized Voltage")
    ax.set_title("Charging Curve (Normalized)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

elif experiment == "② Filter Frequency Response":
    st.header("② High-pass / Low-pass Filter Response")
    filter_type = st.radio("Filter Type:", ["LPF (Low-pass)", "HPF (High-pass)"])
    R = st.slider("Resistance R (Ω)", 100, 5000, 1000)
    C = st.slider("Capacitance C (μF)", 0.1, 10.0, 1.0) * 1e-6
    f = np.logspace(2, 5, 500)
    w = 2 * np.pi * f

    if filter_type == "LPF (Low-pass)":
        H = 1 / np.sqrt(1 + (w * R * C)**2)
    else:
        H = (w * R * C) / np.sqrt(1 + (w * R * C)**2)

    fig, ax = plt.subplots()
    ax.semilogx(f, 20 * np.log10(H))
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Gain (dB)")
    ax.set_title("Filter Frequency Response")
    ax.grid(True, which='both')
    st.pyplot(fig)

elif experiment == "③ RLC Resonance":
    st.header("③ RLC Circuit Resonance Measurement")
    R = st.slider("Resistance R (Ω)", 10, 1000, 100)
    L = st.slider("Inductance L (mH)", 1, 100, 10) * 1e-3
    C = st.slider("Capacitance C (μF)", 0.1, 10.0, 0.1) * 1e-6

    f = np.linspace(1000, 10000, 1000)
    w = 2 * np.pi * f
    Z = np.sqrt(R**2 + (w*L - 1/(w*C))**2)
    I = 1 / Z

    fr = 1 / (2 * np.pi * np.sqrt(L * C))
    st.write(f"**Resonant Frequency f₀ ≈ {fr:.1f} Hz**")

    fig, ax = plt.subplots()
    ax.plot(f, I / max(I))
    ax.axvline(fr, color='r', linestyle='--', label='Resonant Frequency')
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Normalized Current")
    ax.set_title("RLC Circuit Resonance")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
