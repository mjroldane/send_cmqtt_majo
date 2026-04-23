import streamlit as st
import json
import paho.mqtt.client as paho
import platform

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Controlmajo MQTT", layout="centered")

# --- ESTILOS CSS: MORADO PASTEL ---
st.markdown("""
    <style>
    /* Fondo morado pastel suave */
    .stApp {
        background-color: #F3E5F5;
    }
    
    /* Contenedores */
    .css-1r6slp0, .css-170nql5, .stMarkdown {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #D1C4E9;
    }

    /* Botones morados */
    div.stButton > button {
        background-color: #7E57C2 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #5E35B1 !important;
    }
    
    h1, h2 { color: #4A148C !important; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA MQTT ---
broker = "157.230.214.127"
port = 1883

# Inicializamos el cliente una sola vez para mantener la sesión
if "client" not in st.session_state:
    st.session_state.client = paho.Client("Controlmajo")
    try:
        st.session_state.client.connect(broker, port)
        st.session_state.client.loop_start()
    except Exception as e:
        st.error(f"Error de conexión: {e}")

def publicar(topic, msg_dict):
    msg = json.dumps(msg_dict)
    st.session_state.client.publish(topic, msg)

# --- INTERFAZ ---
st.title("💜 MQTT Control - Controlmajo")
st.caption(f"Versión de Python: {platform.python_version()}")

st.subheader("Control Digital")
col1, col2 = st.columns(2)

with col1:
    if st.button('🟢 ON'):
        publicar("cmqtt_s", {"Act1": "ON"})
        st.success("Enviado: ON")

with col2:
    if st.button('🔴 OFF'):
        publicar("cmqtt_s", {"Act1": "OFF"})
        st.error("Enviado: OFF")

st.markdown("---")

st.subheader("Control Analógico")
values = st.slider('Selecciona el rango de valores', 0.0, 100.0, 50.0)
st.write(f'Valor actual: **{values}**')

if st.button('🚀 Enviar valor analógico'):
    publicar("cmqtt_a", {"Analog": float(values)})
    st.info(f"Valor {values} enviado correctamente.")
