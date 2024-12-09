import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go

# Função para carregar os dados de um arquivo CSV
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            data = pd.read_csv(file_path)
            if data.empty:
                return []  # Retorna lista vazia se o arquivo estiver vazio
            return data.to_dict(orient="records")
        except pd.errors.EmptyDataError:
            return []  # Retorna lista vazia se não houver dados
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


def show_instagram_graphs():
    st.title("Gráficos do Instagram")
    
    if not st.session_state.instagram_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.instagram_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    df['Seguidores'] = pd.to_numeric(df['Seguidores'], errors='coerce')
    df['Alcance'] = pd.to_numeric(df['Alcance'], errors='coerce')
    df['Engajamento'] = pd.to_numeric(df['Engajamento'], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=['Seguidores', 'Alcance', 'Engajamento'], inplace=True)

    # Paleta de cores personalizada
    color_1 = "#FFA936"  # Laranja
    color_2 = "#12239E"  # Azul

    ### GRÁFICO DE LINHA ###
    st.subheader("Crescimento de Seguidores ao Longo do Tempo")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Seguidores'],
        mode='lines+markers',
        name='Seguidores',
        line=dict(color=color_2, width=2.5),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        title="Crescimento de Seguidores",
        xaxis_title="Data",
        yaxis_title="Seguidores",
        xaxis=dict(tickformat='%d/%m/%Y'),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_line)

     ### GRÁFICO DE BARRAS ###
    st.subheader("Comparação do Alcance por Mês")
    # Atualizando dinamicamente as categorias de meses com base nos dados disponíveis
    unique_months = df['Mês'].dropna().unique()
    sorted_months = sorted(unique_months, key=lambda x: [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ].index(x))

    df['Mês'] = pd.Categorical(df['Mês'], categories=sorted_months, ordered=True)
    alcance_por_mes = df.groupby('Mês')['Alcance'].sum().reindex(sorted_months)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=alcance_por_mes.index,
        y=alcance_por_mes.values,
        name="Alcance",
        marker_color=color_1
    ))
    fig_bar.update_layout(
        title="Alcance por Mês",
        xaxis_title="Mês",
        yaxis_title="Alcance",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar)

    ### GRÁFICO DE PIZZA ###
    st.subheader("Proporção de Engajamento")
    total_engajamento = df['Engajamento'].sum()
    proporcao_engajamento = (
        df.groupby('Mês')['Engajamento'].sum() / total_engajamento
    ).reindex(sorted_months)

    fig_pizza = go.Figure(data=[go.Pie(
        labels=proporcao_engajamento.index,
        values=proporcao_engajamento.values,
        hole=0.4,  # Criação de um gráfico de pizza em formato de anel
        hoverinfo="label+percent+value",  # Exibe o rótulo, porcentagem e valor ao passar o mouse
        textinfo="percent",  # Exibe apenas a porcentagem dentro do gráfico
        textfont=dict(size=16, color="white"),  # Formatação do texto interno
        marker=dict(
            colors=[color_1, color_2, "#FFD700", "#90EE90", "#FF69B4"],  # Paleta de cores
            line=dict(color="white", width=2)  # Contorno branco entre os segmentos
        )
    )])

    fig_pizza.update_layout(
        title=dict(
            text="Proporção de Engajamento por Mês",
            font=dict(size=18, color="#12239E"),  # Título estilizado com a cor da empresa
            x=0.5  # Centraliza o título
        ),
        annotations=[dict(
            text="Engajamento",  # Texto central no anel
            x=0.5, y=0.5, font_size=20, showarrow=False, font_color=color_2
        )],
        showlegend=True,  # Exibe a legenda abaixo do gráfico
        legend=dict(
            orientation="h",  # Legenda em formato horizontal
            yanchor="bottom", y=-0.2, xanchor="center", x=0.5  # Posiciona a legenda abaixo do gráfico
        )
    )

    st.plotly_chart(fig_pizza)

def show_facebook_graphs():
    st.title("Gráficos do Facebook")

    if not st.session_state.facebook_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.facebook_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    df['Cliques'] = pd.to_numeric(df['Cliques'], errors='coerce')
    df['Engajamento'] = pd.to_numeric(df['Engajamento'], errors='coerce')
    df['Alcance'] = pd.to_numeric(df['Alcance'], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=['Cliques', 'Engajamento', 'Alcance'], inplace=True)

    # Paleta de cores personalizada
    color_1 = "#FFA936"  # Laranja
    color_2 = "#12239E"  # Azul

    ### GRÁFICO DE BARRAS EMPILHADAS ###
    st.subheader("Cliques e Engajamento por Mês")

    # Atualizar dinamicamente os meses com base nos dados disponíveis
    unique_months = df['Mês'].dropna().unique()
    sorted_months = sorted(unique_months, key=lambda x: [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ].index(x))

    df['Mês'] = pd.Categorical(df['Mês'], categories=sorted_months, ordered=True)
    cliques_por_mes = df.groupby('Mês')['Cliques'].sum().reindex(sorted_months)
    engajamento_por_mes = df.groupby('Mês')['Engajamento'].sum().reindex(sorted_months)

    fig_bar_stacked = go.Figure()
    fig_bar_stacked.add_trace(go.Bar(
        x=cliques_por_mes.index,
        y=cliques_por_mes.values,
        name="Cliques",
        marker_color=color_1
    ))
    fig_bar_stacked.add_trace(go.Bar(
        x=engajamento_por_mes.index,
        y=engajamento_por_mes.values,
        name="Engajamento",
        marker_color=color_2
    ))
    fig_bar_stacked.update_layout(
        barmode="stack",
        title="Cliques e Engajamento Empilhados por Mês",
        xaxis_title="Mês",
        yaxis_title="Valores",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar_stacked)


    ### GRÁFICO DE DISPERSÃO ###
    st.subheader("Relação entre Alcance e Engajamento")
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=df['Alcance'],
        y=df['Engajamento'],
        mode='markers',
        marker=dict(size=10, color=color_2, opacity=0.8),
        name="Dados"
    ))
    fig_scatter.update_layout(
        title="Alcance vs Engajamento",
        xaxis_title="Alcance",
        yaxis_title="Engajamento",
        hovermode="closest",
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter)

    ### GRÁFICO DE LINHA ###
    st.subheader("Cliques ao Longo do Tempo")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Cliques'],
        mode='lines+markers',
        name='Cliques',
        line=dict(color=color_1, width=2.5),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        title="Cliques ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Cliques",
        xaxis=dict(tickformat='%d/%m/%Y'),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_line)

def show_linkedin_graphs():
    st.title("Gráficos do LinkedIn")
    
    if not st.session_state.linkedin_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.linkedin_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    df['Alcance'] = pd.to_numeric(df['Alcance'], errors='coerce')
    df['Cliques'] = pd.to_numeric(df['Cliques'], errors='coerce')
    df['Engajamento'] = pd.to_numeric(df['Engajamento'], errors='coerce')
    df['Seguidores'] = pd.to_numeric(df['Seguidores'], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=['Alcance', 'Cliques', 'Engajamento', 'Seguidores'], inplace=True)

    # Paleta de cores personalizada
    color_1 = "#FFA936"  # Laranja
    color_2 = "#12239E"  # Azul

    ### GRÁFICO DE BARRAS ###
    st.subheader("Comparação de Alcance e Cliques por Mês")
    df['Mês'] = pd.Categorical(df['Mês'], categories=[
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ], ordered=True)

    alcance_por_mes = df.groupby('Mês')['Alcance'].sum().reindex(df['Mês'].cat.categories)
    cliques_por_mes = df.groupby('Mês')['Cliques'].sum().reindex(df['Mês'].cat.categories)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=alcance_por_mes.index,
        y=alcance_por_mes.values,
        name="Alcance",
        marker_color=color_1
    ))
    fig_bar.add_trace(go.Bar(
        x=cliques_por_mes.index,
        y=cliques_por_mes.values,
        name="Cliques",
        marker_color=color_2
    ))
    fig_bar.update_layout(
        barmode="group",
        title="Comparação de Alcance e Cliques por Mês",
        xaxis_title="Mês",
        yaxis_title="Valores",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar)

    ### GRÁFICO DE ÁREA ###
    st.subheader("Crescimento Acumulado de Seguidores")
    df['Seguidores Acumulados'] = df['Seguidores'].cumsum()
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Seguidores Acumulados'],
        mode='lines',
        fill='tozeroy',
        line=dict(color=color_2, width=2),
        name="Seguidores Acumulados"
    ))
    fig_area.update_layout(
        title="Crescimento Acumulado de Seguidores",
        xaxis_title="Data",
        yaxis_title="Seguidores Acumulados",
        xaxis=dict(tickformat='%d/%m/%Y'),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_area)

    ### GRÁFICO DE DISPERSÃO ###
    st.subheader("Relação entre Cliques e Engajamento")
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=df['Cliques'],
        y=df['Engajamento'],
        mode='markers',
        marker=dict(size=10, color=color_1, opacity=0.8),
        name="Dados"
    ))
    fig_scatter.update_layout(
        title="Cliques vs Engajamento",
        xaxis_title="Cliques",
        yaxis_title="Engajamento",
        hovermode="closest",
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter)

def show_email_mkt_graphs():
    st.title("Gráficos do E-mail MKT")
    
    if not st.session_state.email_mkt_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.email_mkt_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    df['Taxa de Abertura'] = pd.to_numeric(df['Taxa de Abertura'], errors='coerce')
    df['Cliques'] = pd.to_numeric(df['Cliques'], errors='coerce')
    df['Descadastro'] = pd.to_numeric(df['Descadastro'], errors='coerce')
    df['Receita Gerada'] = pd.to_numeric(df['Receita Gerada'], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=['Taxa de Abertura', 'Cliques', 'Descadastro'], inplace=True)

    # Paleta de cores personalizada
    color_1 = "#FFA936"  # Laranja
    color_2 = "#12239E"  # Azul

    ### GRÁFICO DE LINHA ###
    st.subheader("Taxa de Abertura ao Longo do Tempo")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Taxa de Abertura'],
        mode='lines+markers',
        name='Taxa de Abertura',
        line=dict(color=color_2, width=2.5),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        title="Taxa de Abertura ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Taxa de Abertura (%)",
        xaxis=dict(tickformat='%d/%m/%Y'),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_line)

    ### GRÁFICO DE BARRAS ###
    st.subheader("Comparação de Cliques e Descadastros por Mês")
    df['Mês'] = pd.Categorical(df['Mês'], categories=[
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ], ordered=True)

    cliques_por_mes = df.groupby('Mês')['Cliques'].sum().reindex(df['Mês'].cat.categories)
    descadastros_por_mes = df.groupby('Mês')['Descadastro'].sum().reindex(df['Mês'].cat.categories)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=cliques_por_mes.index,
        y=cliques_por_mes.values,
        name="Cliques",
        marker_color=color_1
    ))
    fig_bar.add_trace(go.Bar(
        x=descadastros_por_mes.index,
        y=descadastros_por_mes.values,
        name="Descadastros",
        marker_color=color_2
    ))
    fig_bar.update_layout(
        barmode="group",
        title="Cliques e Descadastros por Mês",
        xaxis_title="Mês",
        yaxis_title="Valores",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar)

    ### GRÁFICO DE ROSCA ###
    st.subheader("Distribuição Percentual de Cliques e Descadastros")
    total_cliques_descadastros = df[['Cliques', 'Descadastro']].sum()
    fig_donut = go.Figure(data=[go.Pie(
        labels=total_cliques_descadastros.index,
        values=total_cliques_descadastros.values,
        hole=0.4,
        hoverinfo="label+percent+value",
        textinfo="percent",
        textfont=dict(size=16, color="white"),
        marker=dict(
            colors=[color_1, color_2],
            line=dict(color="white", width=2)
        )
    )])

    fig_donut.update_layout(
        title=dict(
            text="Distribuição Percentual de Cliques e Descadastros",
            font=dict(size=18, color="#12239E"),
            x=0.5
        ),
        annotations=[dict(
            text="Cliques vs Descadastros",
            x=0.5, y=0.5, font_size=20, showarrow=False, font_color=color_2
        )],
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=-0.2, xanchor="center", x=0.5
        )
    )
    st.plotly_chart(fig_donut)

def show_youtube_graphs():
    st.title("Gráficos do YouTube Orgânico")
    
    if not st.session_state.youtube_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.youtube_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    df['Visualizações'] = pd.to_numeric(df['Visualizações'], errors='coerce')
    df['Duração Média da Visualização'] = pd.to_numeric(df['Duração Média da Visualização'], errors='coerce')
    df['Inscritos'] = pd.to_numeric(df['Inscritos'], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=['Visualizações', 'Duração Média da Visualização', 'Inscritos'], inplace=True)

    # Paleta de cores personalizada
    color_1 = "#FFA936"  # Laranja
    color_2 = "#12239E"  # Azul

    ### GRÁFICO DE LINHA ###
    st.subheader("Crescimento de Inscritos ao Longo do Tempo")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Inscritos'],
        mode='lines+markers',
        name='Inscritos',
        line=dict(color=color_2, width=2.5),
        marker=dict(size=8)
    ))
    fig_line.update_layout(
        title="Crescimento de Inscritos",
        xaxis_title="Data",
        yaxis_title="Inscritos",
        xaxis=dict(tickformat='%d/%m/%Y'),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_line)

    ### GRÁFICO DE BARRAS ###
    st.subheader("Visualizações por Mês")
    df['Mês'] = pd.Categorical(df['Mês'], categories=[
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ], ordered=True)
    visualizacoes_por_mes = df.groupby('Mês')['Visualizações'].sum().reindex(df['Mês'].cat.categories)
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=visualizacoes_por_mes.index,
        y=visualizacoes_por_mes.values,
        name="Visualizações",
        marker_color=color_1
    ))
    fig_bar.update_layout(
        title="Visualizações por Mês",
        xaxis_title="Mês",
        yaxis_title="Visualizações",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar)

    ### GRÁFICO DE DISPERSÃO ###
    st.subheader("Relação entre Duração Média e Visualizações")
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=df['Duração Média da Visualização'],
        y=df['Visualizações'],
        mode='markers',
        marker=dict(size=10, color=color_2, opacity=0.8),
        name="Dados"
    ))
    fig_scatter.update_layout(
        title="Duração Média vs Visualizações",
        xaxis_title="Duração Média da Visualização (minutos)",
        yaxis_title="Visualizações",
        hovermode="closest",
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter)


# Função para exibir tabelas e formulários
def show_tabs(data_key, fields, title, file_path):
    abas = st.tabs(["Formulário", "Tabela", "Gráficos"])

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
                f"Selecione o registro para apagar da tabela {title}",
                options=range(len(df)),
                format_func=lambda x: f"Linha {x + 1}"
            )

            if st.button(f"Apagar linha selecionada da tabela {title}"):
                st.session_state[data_key].pop(selected_index)
                save_data(file_path, st.session_state[data_key])
                st.success("Registro apagado com sucesso!")
                st.experimental_rerun()  # Atualiza a interface
        else:
            st.info("Nenhum dado disponível. Preencha o formulário na aba 'Formulário'.")

    with abas[2]:
        if title == "Instagram":
            show_instagram_graphs()
        if title == "Facebook":
            show_facebook_graphs()
        if title == "LinkedIn":
            show_linkedin_graphs()
        if title == "E-mail MKT":
            show_email_mkt_graphs()
        if title == "YouTube Orgânico":
            show_youtube_graphs()


# Exibe as abas para o Instagram
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

# Exibe as abas para o Facebook
if st.session_state.selected_network == "Facebook":
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

# Exibe as abas para o LinkedIn
if st.session_state.selected_network == "LinkedIn":
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
    
# Exibe as abas para o E-mail MKT
if st.session_state.selected_network == "E-mail MKT":
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


# Exibe as abas para o YouTube Orgânico
if st.session_state.selected_network == "YouTube Orgânico":
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

