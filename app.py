import streamlit as st
import json
import paho.mqtt.client as paho
import platform

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="MQTT Control", layout="centered")

# --- ESTILOS CSS: PALETA MORADO PASTEL ---
st.markdown("""
    <style>
    /* Fondo morado pastel muy suave */
    .stApp {
        background-color: #F3E5F5;
    }
    
    /* Tarjetas blancas para contraste */
    .css-1r6slp0, .css-170nql5, .stMarkdown {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #D1C4E9;
    }

    /* Estilo de botones morados */
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
    
    h1 { color: #4A148C !important; }
    h2, h3 { color: #5E35B1 !important; }
    </style>
""", unsafe_allow_html=True)

# --- LÓGICA MQTT ---
broker = "157.230.214.127"
port = 1883
client_id = "TON_ESPCliente_majoRol"

# Usamos session_state para mantener la conexión y no saturar el broker
if "mqtt_client" not in st.session_state:
    st.session_state.mqtt_client = paho.Client(client_id)
    try:
        st.session_state.mqtt_client.connect(broker, port)
        st.session_state.mqtt_client.loop_start()
    except Exception as e:
        st.error(f"Error al conectar: {e}")

def publicar(topic, message_dict):
    msg = json.dumps(message_dict)
    st.session_state.mqtt_client.publish(topic, msg)

# --- UI PRINCIPAL ---
st.title("💜 MQTT Control Panel")
st.caption(f"Versión de Python: {platform.python_version()} | ID: {client_id}")

# Control Digital (ON/OFF)
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

# Control Analógico (Slider)
st.subheader("Control Analógico")
values = st.slider('Ajuste de valor', 0.0, 100.0, 50.0)
st.write(f"Valor seleccionado: **{values}**")

if st.button('🚀 Enviar valor analógico'):
    publicar("cmqtt_a", {"Analog": float(values)})
    st.info(f"Valor {values} enviado correctamente.")
