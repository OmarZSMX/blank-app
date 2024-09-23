pip install plotly
import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Función para calcular Fitness, Fatiga y Forma
def calculate_fitness_fatigue_forma(training_data):
    fitness = training_data['Tiempo (hrs)'].rolling(window=30).mean().fillna(0)
    fatiga = training_data['Tiempo (hrs)'].rolling(window=7).mean().fillna(0)
    forma = fitness - fatiga
    return fitness, fatiga, forma

# Configuración de la aplicación
st.title("App de Entrenamientos de Ciclismo")

# Input para los datos del entrenamiento
st.header("Inserta tus datos de entrenamiento")
tiempo = st.number_input("Tiempo (hrs)", min_value=0.0, value=1.0, step=0.1)
distancia = st.number_input("Distancia (km)", min_value=0.0, value=20.0)
velocidad_promedio = st.number_input("Velocidad promedio (km/h)", min_value=0.0, value=25.0)
fc_promedio = st.number_input("Frecuencia cardiaca promedio (bpm)", min_value=0, value=140)
fc_maxima = st.number_input("Frecuencia cardiaca máxima (bpm)", min_value=0, value=180)

# Botón para agregar datos
if st.button("Agregar entrenamiento"):
    # Crear o cargar los datos
    if 'training_data' not in st.session_state:
        st.session_state['training_data'] = pd.DataFrame(columns=['Tiempo (hrs)', 'Distancia (km)', 'Velocidad promedio (km/h)', 
                                                                  'FC Promedio (bpm)', 'FC Máxima (bpm)'])

    # Crear un nuevo DataFrame con el entrenamiento actual
    new_row = pd.DataFrame({
        'Tiempo (hrs)': [tiempo],
        'Distancia (km)': [distancia],
        'Velocidad promedio (km/h)': [velocidad_promedio],
        'FC Promedio (bpm)': [fc_promedio],
        'FC Máxima (bpm)': [fc_maxima]
    })

    # Agregar los datos nuevos usando pd.concat()
    st.session_state['training_data'] = pd.concat([st.session_state['training_data'], new_row], ignore_index=True)

# Mostrar datos registrados
st.header("Historial de Entrenamientos")
if 'training_data' in st.session_state:
    st.write(st.session_state['training_data'])

    # Solo mostrar el gráfico si hay suficientes datos
    if len(st.session_state['training_data']) >= 7:
        # Cálculo de Fitness, Fatiga y Forma
        fitness, fatiga, forma = calculate_fitness_fatigue_forma(st.session_state['training_data'])

        # Crear el gráfico con Plotly
        fig = go.Figure()

        # Fitness (línea azul)
        fig.add_trace(go.Scatter(
            x=st.session_state['training_data'].index, 
            y=fitness, 
            mode='lines', 
            name='Fitness', 
            line=dict(color='blue', width=3)
        ))

        # Fatiga (línea roja)
        fig.add_trace(go.Scatter(
            x=st.session_state['training_data'].index, 
            y=fatiga, 
            mode='lines', 
            name='Fatiga', 
            line=dict(color='red', width=3)
        ))

        # Forma (línea verde)
        fig.add_trace(go.Scatter(
            x=st.session_state['training_data'].index, 
            y=forma, 
            mode='lines', 
            name='Forma', 
            line=dict(color='green', width=3)
        ))

        # Ajustes del layout (parecido a Strava)
        fig.update_layout(
            title="Fitness, Fatiga y Forma",
            xaxis_title="Entrenamientos",
            yaxis_title="Valor",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(fig)
    else:
        st.write("Necesitas al menos 7 entrenamientos para ver el gráfico de Fatiga, Fitness y Forma.")
else:
    st.write("Aún no hay entrenamientos registrados.")
