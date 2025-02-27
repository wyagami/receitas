import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

with st.sidebar:
    st.sidebar.header("CALCULADORA DE JUROS COMPOSTOS")
    st.sidebar.write("""
                     
    - Caso tenha alguma idéia para publicarmos, envie uma mensagem para: 11-990000425 (Willian)
    - Contribua com qualquer valor para mantermos a pagina no ar. PIX (wpyagami@gmail.com)
    """)


def calcular_juros_compostos(principal, taxa, periodo, tempo):
    """Calcula o montante final com juros compostos."""
    montantes = [principal * (1 + taxa / periodo) ** (periodo * t) for t in range(tempo + 1)]
    return montantes

# Configuração da interface do Streamlit
st.title("Calculadora de Juros Compostos")

# Entradas do usuário
principal = st.number_input("Capital Inicial (R$):", min_value=0.0, value=1000.0, step=100.0)
taxa = st.number_input("Taxa de Juros (% ao ano):", min_value=0.0, value=5.0, step=0.1) / 100
periodo = st.selectbox("Número de capitalizações por ano:", [1, 4, 12, 365], index=2)
tempo = st.slider("Tempo de investimento (anos):", min_value=1, max_value=50, value=10)

if st.button("Calcular"):
    montantes = calcular_juros_compostos(principal, taxa, periodo, tempo)
    
    # Criando DataFrame para exibição
    df = pd.DataFrame({"Ano": list(range(tempo + 1)), "Montante (R$)": montantes})
    st.dataframe(df)
    
    # Plotando gráfico
    fig, ax = plt.subplots()
    ax.plot(df["Ano"], df["Montante (R$)"], marker='o', linestyle='-', color='b')
    ax.set_title("Crescimento do Investimento ao Longo do Tempo")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Montante (R$)")
    ax.grid(True)
    st.pyplot(fig)
