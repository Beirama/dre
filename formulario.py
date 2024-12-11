import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import io

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
if "midia_investimento_data" not in st.session_state:
    st.session_state.midia_investimento_data = load_data("midia_investimento_data.csv")
if "midia_investimento_semanal_data" not in st.session_state:
    st.session_state.midia_investimento_semanal_data = load_data("midia_investimento_semanal_data.csv")
if "custos_data" not in st.session_state:
    st.session_state.custos_data = load_data("custos_data.csv")
if "site_beirama_data" not in st.session_state:
    st.session_state.site_beirama_data = load_data("site_beirama_data.csv")
if "site_beirama_semanal_data" not in st.session_state:
    st.session_state.site_beirama_semanal_data = load_data("site_beirama_semanal_data.csv")
if "resultados_google_data" not in st.session_state:
    st.session_state.resultados_google_data = load_data("resultados_google_data.csv")
if "resultados_meta_beirama_data" not in st.session_state:
    st.session_state.resultados_meta_beirama_data = load_data("resultados_meta_beirama_data.csv")
if "performance_data" not in st.session_state:
    st.session_state.performance_data = load_data("performance_data.csv")
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
    if st.button("Investimentos em mídia"):
        st.session_state.selected_network = "Investimento em Mídia"
    if st.button("Custos"):
        st.session_state.selected_network = "Custos"
    if "site_beirama_data" not in st.session_state:
        st.session_state.site_beirama_data = load_data("site_beirama_data.csv")
    if st.button("Site Beirama"):
        st.session_state.selected_network = "Site Beirama"
    if st.button("Resultados Google"):
        st.session_state.selected_network = "Resultados Google"
    if st.button("Resultados Meta BEIRAMA"):
        st.session_state.selected_network = "Resultados Meta BEIRAMA"
    if st.button("Performance"):
        st.session_state.selected_network = "Performance"

with st.expander("Formulários Semanais"):
    st.write("Selecione um formulário semanal abaixo:")

    if st.button("Site Beirama (Semanal)"):
        st.session_state.selected_network = "Site Beirama (Semanal)"
    if st.button("Investimentos em mídia (semanal)"):
        st.session_state.selected_network = "Investimento em Mídia (Semanal)"

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

def show_investimento_graficos():
    st.title("Gráficos de Investimento em Mídia")
    
    if not st.session_state.midia_investimento_data:
        st.info("Nenhum dado disponível para gerar gráficos. Preencha o formulário primeiro.")
        return

    df = pd.DataFrame(st.session_state.midia_investimento_data)
    df['Data'] = pd.to_datetime(df['Data'])
    df.sort_values('Data', inplace=True)

    # Converte colunas para numéricas
    cols_to_numeric = [
        "Google(Display)", "Google(Search)", "Google(Youtube)", 
        "Meta Ads", "LinkedIn ADS"
    ]
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove linhas com valores inválidos
    df.dropna(subset=cols_to_numeric, inplace=True)

    # Adiciona uma coluna para o total de gastos
    df['Total Gastos'] = df[cols_to_numeric].sum(axis=1)

    # Agrupa os dados por mês
    df['Mês'] = pd.Categorical(df['Mês'], categories=[
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ], ordered=True)

    total_por_mes = df.groupby('Mês')['Total Gastos'].sum().reindex(df['Mês'].cat.categories)

    # Paleta de cores personalizada
    color_total = "#FF5733"  # Vermelho para Total

    ### GRÁFICO DE BARRAS ###
    st.subheader("Total de Gastos por Mês")
    fig_bar_total = go.Figure()
    fig_bar_total.add_trace(go.Bar(
        x=total_por_mes.index,
        y=total_por_mes.values,
        name="Total de Gastos",
        marker_color=color_total
    ))
    fig_bar_total.update_layout(
        title="Total de Gastos por Mês",
        xaxis_title="Mês",
        yaxis_title="Total (R$)",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_bar_total)

    # Mostra o total acumulado
    total_acumulado = total_por_mes.sum()
    st.markdown(f"### Total Geral de Investimentos: **R$ {total_acumulado:,.2f}**")

    ### GRÁFICO DE LINHAS ###
    st.subheader("Distribuição de Gastos por Mídia ao Longo do Tempo")
    fig_line = go.Figure()
    for col in cols_to_numeric:
        gastos_por_mes = df.groupby('Mês')[col].sum().reindex(df['Mês'].cat.categories)
        fig_line.add_trace(go.Scatter(
            x=gastos_por_mes.index,
            y=gastos_por_mes.values,
            mode='lines+markers',
            name=col,
            line=dict(width=2.5),
            marker=dict(size=8)
        ))
    fig_line.update_layout(
        title="Gastos por Tipo de Mídia",
        xaxis_title="Mês",
        yaxis_title="Gastos (R$)",
        xaxis=dict(tickangle=-45),
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_line)


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

            # Botão para exportar os dados para Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name=title)
            buffer.seek(0)

            st.download_button(
                label="Exportar para Excel",
                data=buffer,
                file_name=f"{title}_dados.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

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
        if title == "Investimento em Mídia":
            show_investimento_graficos()




# Exibe as abas das redes
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
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Instagram",
        file_path="instagram_data.csv"
    )

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
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Facebook",
        file_path="facebook_data.csv"
    )

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
                {"name": "Observação", "label": "Observação:", "type": "text"},
            ],
            title="LinkedIn",
            file_path="linkedin_data.csv"
        )
    
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
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="E-mail MKT",
        file_path="email_mkt_data.csv"
    )

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
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="YouTube Orgânico",
        file_path="youtube_data.csv"
    )

if st.session_state.selected_network == "Investimento em Mídia":
    show_tabs(
        data_key="midia_investimento_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Google(Display)", "label": "Google (Display):", "type": "text"},
            {"name": "Google(Search)", "label": "Google (Search):", "type": "text"},
            {"name": "Google(Youtube)", "label": "Google (YouTube):", "type": "text"},
            {"name": "Meta Ads", "label": "Meta Ads:", "type": "text"},
            {"name": "LinkedIn ADS", "label": "LinkedIn ADS:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Investimento em Mídia",
        file_path="midia_investimento_data.csv"
    )

if st.session_state.selected_network == "Custos":
    show_tabs(
        data_key="custos_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Beicast Aluguel espaço", "label": "Beicast Aluguel espaço:", "type": "text"},
            {"name": "Shopify", "label": "Shopify:", "type": "text"},
            {"name": "Custo Ramper MKT", "label": "Custo Ramper MKT:", "type": "text"},
            {"name": "Alex Gestor de tráfego", "label": "Alex Gestor de tráfego:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Custos",
        file_path="custos_data.csv"
    )

if st.session_state.selected_network == "Site Beirama":
    show_tabs(
        data_key="site_beirama_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Sessões", "label": "Sessões:", "type": "text"},
            {"name": "Taxa de Rejeição (%)", "label": "Taxa de Rejeição (%):", "type": "text"},
            {"name": "Duração Média da Sessão", "label": "Duração Média da Sessão (min):", "type": "text"},
            {"name": "Taxa de Conversão (%)", "label": "Taxa de Conversão (%):", "type": "text"},
            {"name": "Páginas Mais Acessadas", "label": "Páginas Mais Acessadas:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Site Beirama",
        file_path="site_beirama_data.csv"
    )

if st.session_state.selected_network == "Resultados Google":

    show_tabs(
        data_key="resultados_google_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Cliques (Search)", "label": "Cliques (Google Search):", "type": "text"},
            {"name": "Cliques (Display)", "label": "Cliques (Google Display):", "type": "text"},
            {"name": "Contatos", "label": "Contatos (Cadastros/Conversões):", "type": "text"},
            {"name": "Negócios/Propostas", "label": "Negócios/Propostas (Volume):", "type": "text"},
            {"name": "Fechamento", "label": "Fechamento:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Resultados Google",
        file_path="resultados_google_data.csv"
    )

if st.session_state.selected_network == "Resultados Meta BEIRAMA":

    show_tabs(
        data_key="resultados_meta_beirama_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Cliques (Search)", "label": "Cliques (Google Search):", "type": "text"},
            {"name": "Cliques (Display)", "label": "Cliques (Google Display):", "type": "text"},
            {"name": "Contatos", "label": "Contatos (Cadastros/Conversões):", "type": "text"},
            {"name": "Negócios/Propostas", "label": "Negócios/Propostas (Volume):", "type": "text"},
            {"name": "Fechamento", "label": "Fechamento:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Resultados Meta BEIRAMA",
        file_path="resultados_meta_beirama_data.csv"
    )

if st.session_state.selected_network == "Performance":
    show_tabs(
        data_key="performance_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Margem de Contribuição", "label": "Margem de Contribuição (%):", "type": "text"},
            {"name": "Ticket Médio", "label": "Ticket Médio (R$):", "type": "text"},
            {"name": "ROI", "label": "ROI (%):", "type": "text"},
            {"name": "ROAS", "label": "ROAS:", "type": "text"},
            {"name": "CPV", "label": "CPV (R$):", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Performance",
        file_path="performance_data.csv"
    )

if st.session_state.selected_network == "Site Beirama (Semanal)":
    show_tabs(
        data_key="site_beirama_semanal_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Sessões", "label": "Sessões:", "type": "text"},
            {"name": "Taxa de Rejeição", "label": "Taxa de Rejeição (%):", "type": "text"},
            {"name": "Duração Média da Sessão", "label": "Duração Média da Sessão (min):", "type": "text"},
            {"name": "Taxa de Conversão", "label": "Taxa de Conversão (%):", "type": "text"},
            {"name": "Páginas mais Acessadas", "label": "Páginas mais Acessadas:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Site Beirama (Semanal)",
        file_path="site_beirama_semanal_data.csv"
    )

if st.session_state.selected_network == "Investimento em Mídia (Semanal)":
    show_tabs(
        data_key="midia_investimento_semanal_data",
        fields=[
            {"name": "Data", "label": "Data:", "type": "date"},
            {"name": "Mês", "label": "Mês:", "type": "select", "options": [
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ]},
            {"name": "Google(Display)", "label": "Google (Display):", "type": "text"},
            {"name": "Google(Search)", "label": "Google (Search):", "type": "text"},
            {"name": "Google(Youtube)", "label": "Google (YouTube):", "type": "text"},
            {"name": "Meta Ads", "label": "Meta Ads:", "type": "text"},
            {"name": "LinkedIn ADS", "label": "LinkedIn ADS:", "type": "text"},
            {"name": "Observação", "label": "Observação:", "type": "text"},
        ],
        title="Investimento em Mídia",
        file_path="midia_investimento_semanal_data.csv"
    )