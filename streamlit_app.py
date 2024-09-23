import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
pip install streamlit pandas
import streamlit as st
import pandas as pd
import math

# Función para calcular Fitness, Fatiga y Forma (modelos simples basados en el tiempo total de entrenamiento)
def calculate_fitness_fatigue_forma(training_data):
    # Fitness: Media del tiempo de entrenamiento en los últimos 30 días
    fitness = training_data['Tiempo (min)'].rolling(window=30).mean().fillna(0)
    
    # Fatiga: Media del tiempo de entrenamiento en los últimos 7 días
    fatiga = training_data['Tiempo (min)'].rolling(window=7).mean().fillna(0)
    
    # Forma: Diferencia entre fitness y fatiga
    forma = fitness - fatiga
    
    return fitness, fatiga, forma

# Configuración de la aplicación en Streamlit
st.title("App de Entrenamientos de Ciclismo")

# Input para los datos del entrenamiento
st.header("Inserta tus datos de entrenamiento")
tiempo = st.number_input("Tiempo (min)", min_value=0, value=60)
distancia = st.number_input("Distancia (km)", min_value=0.0, value=20.0)
velocidad_promedio = st.number_input("Velocidad promedio (km/h)", min_value=0.0, value=25.0)
fc_promedio = st.number_input("Frecuencia cardiaca promedio (bpm)", min_value=0, value=140)
fc_maxima = st.number_input("Frecuencia cardiaca máxima (bpm)", min_value=0, value=180)

# Botón para agregar datos
if st.button("Agregar entrenamiento"):
    # Crear o cargar los datos
    if 'training_data' not in st.session_state:
        st.session_state['training_data'] = pd.DataFrame(columns=['Tiempo (min)', 'Distancia (km)', 'Velocidad promedio (km/h)', 
                                                                  'FC Promedio (bpm)', 'FC Máxima (bpm)'])

    # Agregar los datos nuevos
    st.session_state['training_data'] = st.session_state['training_data'].append({
        'Tiempo (min)': tiempo,
        'Distancia (km)': distancia,
        'Velocidad promedio (km/h)': velocidad_promedio,
        'FC Promedio (bpm)': fc_promedio,
        'FC Máxima (bpm)': fc_maxima
    }, ignore_index=True)

# Mostrar datos registrados
st.header("Historial de Entrenamientos")
if 'training_data' in st.session_state:
    st.write(st.session_state['training_data'])

    # Cálculo de Fitness, Fatiga y Forma
    fitness, fatiga, forma = calculate_fitness_fatigue_forma(st.session_state['training_data'])

    st.subheader("Indicadores")
    st.line_chart(pd.DataFrame({'Fitness': fitness, 'Fatiga': fatiga, 'Forma': forma}))
else:
    st.write("Aún no hay entrenamientos registrados.")

# Correr la aplicación con: streamlit run cycling_app.py
