import streamlit as st
import pandas as pd
import os

# Função para carregar os dados de um arquivo CSV
def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path).to_dict(orient="records")
    return []

# Função para salvar os dados em um arquivo CSV
def save_data(file_path, data):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

# Inicializa as listas para armazenar os dados e o estado de seleção
if "instagram_data" not in st.session_state:
    st.session_state.instagram_data = load_data("instagram_data.csv")
if "facebook_data" not in st.session_state:
    st.session_state.facebook_data = load_data("facebook_data.csv")
if "linkedin_data" not in st.session_state:
    st.session_state.linkedin_data = load_data("linkedin_data.csv")
if "email_mkt_data" not in st.session_state:
    st.session_state.email_mkt_data = load_data("email_mkt_data.csv")
if "youtube_data" not in st.session_state:
    st.session_state.youtube_data = load_data("youtube_data.csv")
if "selected_network" not in st.session_state:
    st.session_state.selected_network = None

# Título da página
st.title("Menus")

# Bloco suspenso para Redes Sociais
with st.expander("Redes Sociais"):
    st.write("Selecione uma rede social abaixo:")

    if st.button("Instagram"):
        st.session_state.selected_network = "Instagram"
    if st.button("Facebook"):
        st.session_state.selected_network = "Facebook"
    if st.button("LinkedIn"):
        st.session_state.selected_network = "LinkedIn"
    if st.button("E-mail MKT"):
        st.session_state.selected_network = "E-mail MKT"
    if st.button("YouTube Orgânico"):
        st.session_state.selected_network = "YouTube Orgânico"

# Função para exibir e manipular tabelas
def show_tabs(data_key, fields, title, file_path):
    abas = st.tabs(["Formulário", "Tabela"])

    with abas[0]:
        st.title(f"Formulário de {title}")
        with st.form(key=f"{data_key}_form"):
            form_data = {}
            for field in fields:
                if field["type"] == "text":
                    form_data[field["name"]] = st.text_input(field["label"])
                elif field["type"] == "date":
                    form_data[field["name"]] = st.date_input(field["label"])
                elif field["type"] == "select":
                    form_data[field["name"]] = st.selectbox(field["label"], field["options"])
            
            submit = st.form_submit_button("Enviar")
            if submit:
                form_data["Data"] = str(form_data.get("Data", ""))
                st.session_state[data_key].append(form_data)
                save_data(file_path, st.session_state[data_key])
                st.success("Dados enviados com sucesso!")

    with abas[1]:
        st.title(f"Tabela de Dados de {title}")
        if st.session_state[data_key]:
            df = pd.DataFrame(st.session_state[data_key])
            st.table(df)

            # Seleção de linha para exclusão
            selected_index = st.selectbox(
                f"Selecione o número da linha para apagar da tabela {title}",
                options=range(len(df)),
                format_func=lambda x: f"Linha {x + 1}"
            )

            if st.button(f"Apagar linha selecionada da tabela {title}"):
                st.session_state[data_key].pop(selected_index)
                save_data(file_path, st.session_state[data_key])
                st.success(f"Linha {selected_index + 1} apagada com sucesso!")
                st.experimental_rerun()
        else:
            st.info("Nenhum dado disponível. Preencha o formulário na aba 'Formulário'.")

# Exibe as abas para cada rede social
if st.session_state.selected_network == "Instagram":
    show_tabs(
        data_key="instagram_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Alcance", "label": "Alcance:", "type": "text"},
            {"name": "Engajamento", "label": "Engajamento:", "type": "text"},
            {"name": "Seguidores", "label": "Seguidores:", "type": "text"},
        ],
        title="Instagram",
        file_path="instagram_data.csv"
    )

elif st.session_state.selected_network == "Facebook":
    show_tabs(
        data_key="facebook_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Alcance", "label": "Alcance:", "type": "text"},
            {"name": "Engajamento", "label": "Engajamento:", "type": "text"},
            {"name": "Seguidores", "label": "Seguidores:", "type": "text"},
            {"name": "Cliques", "label": "Cliques:", "type": "text"},
        ],
        title="Facebook",
        file_path="facebook_data.csv"
    )

elif st.session_state.selected_network == "LinkedIn":
    show_tabs(
        data_key="linkedin_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Alcance", "label": "Alcance:", "type": "text"},
            {"name": "Cliques", "label": "Cliques:", "type": "text"},
            {"name": "Engajamento", "label": "Engajamento:", "type": "text"},
            {"name": "Seguidores", "label": "Seguidores:", "type": "text"},
        ],
        title="LinkedIn",
        file_path="linkedin_data.csv"
    )

elif st.session_state.selected_network == "E-mail MKT":
    show_tabs(
        data_key="email_mkt_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Taxa de Abertura", "label": "Taxa de Abertura:", "type": "text"},
            {"name": "Cliques", "label": "Cliques:", "type": "text"},
            {"name": "Descadastro", "label": "Descadastro:", "type": "text"},
            {"name": "Receita Gerada", "label": "Receita Gerada:", "type": "text"},
        ],
        title="E-mail MKT",
        file_path="email_mkt_data.csv"
    )

elif st.session_state.selected_network == "YouTube Orgânico":
    show_tabs(
        data_key="youtube_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Visualizações", "label": "Visualizações:", "type": "text"},
            {"name": "Duração Média da Visualização", "label": "Duração Média da Visualização:", "type": "text"},
            {"name": "Inscritos", "label": "Inscritos:", "type": "text"},
        ],
        title="YouTube Orgânico",
        file_path="youtube_data.csv"
    )
