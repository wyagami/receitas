import streamlit as st
import requests
import json

# ... (seu código anterior: importar bibliotecas, título do app) ...
st.title("CHEF IA")

with st.sidebar:
    st.sidebar.header("Chef ia")
    st.sidebar.write("""
    INDIQUE OS INGREDIENTES E OBTENHA UMA RECEITA
                                          
    - Caso tenha alguma idéia para publicarmos, envie uma mensagem para: 11-990000425 (Willian)
    - Contribua com qualquer valor para mantermos a pagina no ar. PIX (wpyagami@gmail.com)
    """)



def extract_ingredient_list(receita):
    """
    Extrai a lista de ingredientes da receita. Essa função precisará ser adaptada
    para o formato específico das receitas geradas pela sua IA.
    """
    # Implemente a lógica para analisar a string da receita e extrair a lista de ingredientes.
    # Isso pode envolver o uso de expressões regulares ou outras técnicas de processamento de texto.
    # Exemplo simplificado (adapte à sua necessidade):
    lines = receita.split('\n')
    ingredients = []
    ingredient_section_started = False
    for line in lines:
        line = line.strip()
        if line.lower().startswith("ingredientes"):
            ingredient_section_started = True
            continue
        if ingredient_section_started and line:
            ingredients.append(line) # Adiciona cada linha como um ingrediente (melhorar)
    return ingredients


# ... (seu código anterior: função gerar_receita) ...

def gerar_receita(ingredientes, preferencias):
    """Gera a receita e calcula o valor nutricional."""
    # ... (seu código anterior para gerar a receita usando a API OpenRouter) ...

    try:
        # Gerar receita usando a API OpenRouter
        user_input = f"Gere uma receita detalhada utilizando os seguintes ingredientes: {ingredientes}.  Considere as seguintes preferências alimentares e restrições: {preferencias}.  Inclua o nome da receita, lista de ingredientes com quantidades, instruções passo a passo, tempo estimado de preparo e separe cada parte da receita com um delimitador consistente, por exemplo, '---'. Forneça a receita em português. Utilize somente os ingredientes fornecidos, nada mais. Liste no final as informações nutricionais."
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer " + st.secrets["qwen_key"],
                "Content-Type": "application/json",
                "HTTP-Referer": "https://seu-dominio.com",
                "X-Title": "Chef IA",
            },
            data=json.dumps({
                "model": "qwen/qwen2.5-vl-72b-instruct:free",
                "messages": [
                    {"role": "system", "content": "Você é um chef de cozinha virtual que gera receitas detalhadas e criativas em português."},
                    {"role": "user", "content": user_input},
                ],
            })
        )
        response.raise_for_status()
        data = response.json()
        receita = data["choices"][0]["message"]["content"].strip()

        # Extrair lista de ingredientes da receita
        ingredient_list = extract_ingredient_list(receita)

    except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
            return None, None
    return receita

# ... (seu código anterior: interface Streamlit) ...

# Interface Streamlit
ingredientes = st.text_input("Digite os ingredientes que você tem:", "frango, arroz, tomate")
preferencias = st.text_input("Suas preferências alimentares (ex: vegetariano, sem glúten, com glúten):", "sem glúten")

if st.button("Gerar Receita"):
    if not ingredientes or not preferencias:
        st.warning("Por favor, preencha os ingredientes e as preferências.")
    else:
        with st.spinner("Gerando sua receita e calculando informações nutricionais..."):
            receita = gerar_receita(ingredientes, preferencias)

        if receita:
            st.subheader("Sua Receita:")
            st.write(receita)

        else:
            st.error("Não foi possível gerar a receita. Por favor, tente novamente mais tarde.")