import streamlit as st
import pandas as pd
import time

# 1. Configuración de Marca y Estética Profesional
st.set_page_config(
    page_title="ControlQuest - Dominio de Sistemas Dinámicos", 
    page_icon="⚙️", 
    layout="centered"
)

# Estilo CSS personalizado para una interfaz limpia y motivadora
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stButton>button { 
        width: 100%; 
        border-radius: 25px; 
        background-color: #1E8449; 
        color: white; 
        font-weight: bold;
        height: 3em;
        border: none;
    }
    .stButton>button:hover {
        background-color: #145A32;
        border: none;
    }
    .rank-card { 
        padding: 25px; 
        border-radius: 20px; 
        background-color: white; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .metric-text {
        font-size: 1.1em;
        color: #2C3E50;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestión del Estado de la Sesión (Persistencia local)
if 'points' not in st.session_state:
    st.session_state.points = 0
    st.session_state.streak = 7  # Ejemplo de racha activa
    st.session_state.answered = 0
    st.session_state.correct = 0

# Lógica de Determinación de Rangos y Promedio Académico
def calculate_status(points):
    # Simulación de promedio basada en el desempeño de los retos
    avg = min(points / 12, 100) 
    if avg < 60: return "Bronce", "🥉", "#CD7F32", avg
    if avg < 80: return "Plata", "🥈", "#A9A9A9", avg
    if avg < 90: return "Oro", "🥇", "#F1C40F", avg
    if avg < 95: return "Platino", "🛡️", "#3498DB", avg
    return "Diamante", "💎", "#1ABC9C", avg

rank_name, rank_emoji, rank_color, current_avg = calculate_status(st.session_state.points)

# 3. Estructura de Navegación por Pestañas
tab_lesson, tab_leader, tab_rank, tab_rewards = st.tabs([
    "📖 Lección", "🏆 Tabla de Posiciones", "🎖️ Mi Rango", "🎁 Recompensas"
])

# ------------------------------------------------------------------
# PESTAÑA 1: LECCIÓN DE MICROAPRENDIZAJE (Reto Diario)
# ------------------------------------------------------------------
with tab_lesson:
    st.header("⚡ Reto de Ingeniería del Día")
    st.write("Demuestra tu dominio teórico para acumular puntos de rango.")
    
    # Banco de preguntas representativo del Módulo 1 y 2
    questions = [
        {
            "q": "¿Cuál es la principal ventaja de utilizar la Regla de Mason sobre el álgebra de bloques convencional?",
            "options": [
                "Permite calcular la ganancia sin reducciones paso a paso",
                "Funciona solo para sistemas no lineales",
                "Reduce el tiempo muerto del sistema",
                "Elimina la necesidad de la transformada de Laplace"
            ],
            "correct": "Permite calcular la ganancia sin reducciones paso a paso"
        },
        {
            "q": "En un sistema de segundo orden, si el factor de amortiguamiento ζ es mayor a 1, el sistema es:",
            "options": ["Subamortiguado", "Críticamente amortiguado", "Sobreamortiguado", "Inestable"],
            "correct": "Sobreamortiguado"
        },
        {
            "q": "La técnica de linealización mediante la Serie de Taylor es válida únicamente:",
            "options": ["Para frecuencias infinitas", "Cerca del punto de operación (equilibrio)", "En sistemas puramente mecánicos", "Si la ganancia K es unitaria"],
            "correct": "Cerca del punto de operación (equilibrio)"
        }
    ]

    q_idx = st.session_state.answered % len(questions)
    
    with st.container():
        st.subheader(f"Misión {st.session_state.answered + 1}")
        st.info(questions[q_idx]["q"])
        
        user_choice = st.radio("Selecciona el fundamento correcto:", questions[q_idx]["options"], key=f"q_{st.session_state.answered}")
        
        if st.button("Validar Respuesta"):
            if user_choice == questions[q_idx]["correct"]:
                st.success("✅ ¡Análisis Correcto! +150 puntos de experiencia.")
                st.session_state.points += 150
                st.session_state.correct += 1
            else:
                st.error(f"❌ Error en el análisis. La respuesta correcta era: {questions[q_idx]['correct']}")
            
            st.session_state.answered += 1
            time.sleep(1.5)
            st.rerun()

# ------------------------------------------------------------------
# PESTAÑA 2: LEADERBOARD Y RACHA
# ------------------------------------------------------------------
with tab_leader:
    st.header(f"🔥 Racha de Estudio: {st.session_state.streak} Días")
    st.markdown("---")
    st.subheader("Cuadro de Honor - Ingeniería de Control")
    
    # Datos simulados para el contexto competitivo
    leader_df = pd.DataFrame({
        "Ingeniero/a": ["Erika M.", "Carlos R.", "Roberto C. (Tú)", "Luis F.", "Ana G."],
        "Puntos XP": [1550, 1400, st.session_state.points, 900, 750],
        "Rango": ["Platino", "Platino", rank_name, "Plata", "Plata"]
    }).sort_values(by="Puntos XP", ascending=False)
    
    st.table(leader_df)
    st.caption("La tabla se actualiza cada vez que completas una misión diaria.")

# ------------------------------------------------------------------
# PESTAÑA 3: RANGO OBTENIDO Y PROGRESO
# ------------------------------------------------------------------
with tab_rank:
    st.header("🎖️ Estatus del Sistema")
    
    st.markdown(f"""
    <div class="rank-card" style="border-left: 10px solid {rank_color};">
        <h2 style="color: {rank_color}; margin-top: 0;">{rank_emoji} Rango {rank_name}</h2>
        <p class="metric-text"><b>Promedio Acumulado:</b> {current_avg:.1f} / 100</p>
        <p class="metric-text"><b>Precisión de Misión:</b> {((st.session_state.correct / max(1, st.session_state.answered)) * 100):.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Progreso hacia el siguiente nivel")
    st.progress(current_avg / 100)
    
    if rank_name != "Diamante":
        st.write(f"Sigue así, estás a pocos puntos de alcanzar el nivel superior.")

# ------------------------------------------------------------------
# PESTAÑA 4: RECOMPENSAS Y PRIVILEGIOS ISA
# ------------------------------------------------------------------
with tab_rewards:
    st.header("🎁 Beneficios y Privilegios Académicos")
    st.write("Tu rango define tus libertades dentro del ecosistema de aprendizaje.")

    recompensas_list = [
        {"nivel": "Bronce", "desc": "☕ Bebidas permitidas en el salón de clases.", "min": 0},
        {"nivel": "Plata", "desc": "🌐 Sesión sincrónica vía Teams (1 cada 2 semanas).", "min": 70},
        {"nivel": "Oro", "desc": "🕒 Una sesión completamente asincrónica semanal.", "min": 80},
        {"nivel": "Platino", "desc": "🍕 Alimentos permitidos en el salón de clases.", "min": 90},
        {"nivel": "Diamante", "desc": "🎓 Asistencia opcional. Contenido 100% asincrónico.", "min": 95},
    ]

    for item in recompensas_list:
        esta_bloqueado = current_avg < item["min"]
        icono = "🔒" if esta_bloqueado else "🔓"
        estado = "Bloqueado" if esta_bloqueado else "Activo"
        
        with st.expander(f"{item['nivel']} - {icono} {estado}"):
            texto_color = "#7F8C8D" if esta_bloqueado else "#27AE60"
            st.markdown(f"<p style='color: {texto_color}; font-size: 1.1em;'>{item['desc']}</p>", unsafe_allow_html=True)
            if item['nivel'] == rank_name and not esta_bloqueado:
                st.info("💡 Este es tu beneficio actual. ¡Mantenlo!")

    st.divider()
    st.markdown("""
    **Regla del Lanyard:** Aquellos estudiantes que mantengan su rango hasta el cierre del ciclo escolar recibirán el **Lanyard Oficial de ControlQuest** con su distinción grabada. *Perder el rango implica la devolución de la insignia física.*
    """)