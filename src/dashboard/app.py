import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard import api_client
from dashboard.custom_locale import formatar_br

# --- Configuração da Página ---
st.set_page_config(page_title='Dashboard de Livros', page_icon='📚', layout='wide')

col1, col2 = st.columns([3, 1])

with col1:
    st.title('📚 Dashboard de Análise de Livros')

with col2:
    st.markdown(
        f"""
        <div style="padding-top: 20px;">
            <a href="{api_client.API_BASE_URL}/docs"
                target="_blank"
                style="display: inline-block; padding: 10px 15px;
                background-color: #0068c9; color: white; text-align: center;
                text-decoration: none; border-radius: 5px; font-weight: bold;">
                Acesse a documentação da API
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('Use este dashboard para explorar dados da API de Livros.')

st.markdown(
    """
    <style>
    div[data-testid="stMarkdownContainer"] {
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Abas de Navegação ---
tab1, tab2, tab3, tab4 = st.tabs([
    'Visão Geral e Estatística',
    'Busca Detalhada',
    'Análise de Categorias',
    'Status da API',
])

# =================================================================================================
# --- Aba 1: VISÃO GERAL ---
# =================================================================================================


with tab1:
    st.header('Visão Geral e Estatísticas do Catálogo')

    # Busca os dados de overview
    overview_data = api_client.get_overview_stats()

    if overview_data:
        st.markdown(
            """
        <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            padding: 1rem !important;
            font-weight: 600 !important;
            font-size: 20px !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
        # --- Métricas Principais ---
        col1, col2, col3 = st.columns(3)
        total_livros = overview_data.get('total_books', 0)
        col1.metric('Total de Livros', f'{formatar_br(total_livros)}', border=True)
        preco_medio = overview_data.get('average_price', 0)
        col2.metric('Preço Médio', f'R$ {formatar_br(preco_medio)}', border=True)
        col3.metric(
            'Total de Categorias', f'{overview_data.get("count_categories")}', border=True
        )  # Assumindo 5 ratings como categorias

        st.markdown('---')

        col_pie, col_top_rated = st.columns([2, 3])

        # --- Gráfico de Pizza: Distribuição de Avaliações ---
        with col_pie:
            st.subheader('Distribuição de Avaliações (Rating)')
            rating_data = overview_data.get('rating_distribuition', {})
            if rating_data:
                df_ratings = pd.DataFrame(
                    list(rating_data.items()), columns=['Avaliação', 'Quantidade']
                )
                df_ratings['Avaliação'] = (
                    df_ratings['Avaliação'].astype(float).astype(int).astype(str) + ' Estrelas'
                )

                fig = px.pie(
                    df_ratings,
                    names='Avaliação',
                    values='Quantidade',
                    title='Proporção de Livros por Avaliação',
                    hole=0.3,
                    color_discrete_sequence=px.colors.sequential.RdBu,
                )
                fig.update_layout(legend_title_text='Avaliação')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('Não foi possível carregar os dados de avaliação.')

        # --- Top Livros Mais Bem Avaliados ---
        with col_top_rated:
            st.subheader('Top Livros por Avaliação')

            top_n = st.slider(
                'Selecione o número de livros para exibir:',
                min_value=3,
                max_value=20,
                value=5,
                key='top_rated_slider',
            )

            top_rated_data = api_client.get_top_rated_books(limit=top_n)
            if top_rated_data and top_rated_data.get('books'):
                df_top_rated = pd.DataFrame(top_rated_data['books'])
                # Exibindo com imagens e detalhes
                for index, row in df_top_rated.iterrows():
                    cols = st.columns([1, 4])
                    with cols[0]:
                        st.image(row['image_url'], width=80)
                    with cols[1]:
                        st.markdown(f'**{row["title"]}**')
                        full_stars = int(row['rating'])
                        partial_star = '⭐' if row['rating'] % 1 >= 0.5 else ''  # noqa
                        stars = '⭐' * full_stars + partial_star
                        st.markdown(
                            f'**Preço:** R$ {row["price"]:.2f} | \
                            ****Avaliação:** {stars}'
                        )
                    st.markdown('---')
            else:
                st.warning('Não foi possível carregar os livros mais bem avaliados.')

# =================================================================================================
# --- Aba 2: BUSCA DETALHADA ---
# =================================================================================================
with tab2:
    st.header('🔎 Ferramenta de Busca e Filtro')

    # --- Filtros ---
    with st.expander('Clique para expandir os filtros', expanded=True):
        col_filter1, col_filter2 = st.columns(2)

        with col_filter1:
            # Filtro por Título
            title_query = st.text_input('Buscar por título:')

            # Filtro por Categoria
            all_categories = api_client.get_categories()
            category_query = st.selectbox('Filtrar por categoria:', options=all_categories)

        with col_filter2:
            # Filtro por Faixa de Preço
            st.write('Filtrar por faixa de preço:')
            price_range = st.slider(
                'Preço (R$):', min_value=0.0, max_value=100.0, value=(0.0, 100.0), step=1.0
            )
            use_price_filter = st.checkbox('Ativar filtro por preço')

    # --- Lógica de Busca ---
    if use_price_filter:
        books_data = api_client.get_books_by_price_range(
            min_price=price_range[0], max_price=price_range[1]
        )
    else:
        books_data = api_client.get_books(
            title=title_query, category=category_query, limit=100
        )  # Limite de 100 para a busca

    # --- Exibição dos Resultados ---
    total_books = books_data.get('total', 0)
    st.success(f'Encontrados **{total_books}** livros com os filtros aplicados.')

    if books_data and books_data.get('books'):
        df_books = pd.DataFrame(books_data['books'])
        df_books_display = df_books[['title', 'price', 'rating', 'availability', 'category']]

        # Formatando o DataFrame para exibição
        st.dataframe(
            df_books_display,
            use_container_width=True,
            column_config={
                'title': st.column_config.TextColumn('Título', width='large'),
                'price': st.column_config.NumberColumn('Preço (R$)', format='R$ %.2f'),
                'rating': st.column_config.NumberColumn('Avaliação', format='%d ⭐'),
                'availability': st.column_config.CheckboxColumn('Disponível?'),
                'category': 'Categoria',
            },
            hide_index=True,
        )
    else:
        st.info('Nenhum livro encontrado para os filtros selecionados.')


# =================================================================================================
# --- Aba 3: ANÁLISE DE CATEGORIAS ---
# =================================================================================================
with tab3:
    st.header('📊 Análise por Categoria')

    category_stats = api_client.get_category_stats()

    if category_stats:
        st.metric(
            'Total de Categorias Analisadas',
            category_stats.get('total_categories', 0),
            border=True,
        )

        count_dist = category_stats.get('categories_count_distribution', {})
        price_dist = category_stats.get('categories_avg_price_distribution', {})

        if count_dist and price_dist:
            df_count = pd.DataFrame(
                list(count_dist.items()), columns=['Categoria', 'Quantidade de Livros']
            ).sort_values('Quantidade de Livros', ascending=False)
            df_price = pd.DataFrame(
                list(price_dist.items()), columns=['Categoria', 'Preço Médio']
            ).sort_values('Preço Médio', ascending=False)

            # --- Gráfico de Barras: Quantidade de Livros por Categoria ---
            st.subheader('Top 20 Categorias por Quantidade de Livros')
            fig_count = px.bar(
                df_count.head(20),  # Mostra as top 20 para não poluir
                x='Categoria',
                y='Quantidade de Livros',
                labels={'Quantidade de Livros': 'Nº de Livros', 'Categoria': 'Categoria'},
                color='Quantidade de Livros',
                color_continuous_scale=px.colors.sequential.Viridis,
            )
            st.plotly_chart(fig_count, use_container_width=True)

            # --- Gráfico de Barras: Preço Médio por Categoria ---
            st.subheader('Top 20 Categorias por Preço Médio')
            fig_price = px.bar(
                df_price.head(20),  # Mostra as top 20
                x='Categoria',
                y='Preço Médio',
                labels={'Preço Médio': 'Preço Médio (R$)', 'Categoria': 'Categoria'},
                color='Preço Médio',
                color_continuous_scale=px.colors.sequential.Plasma,
            )
            st.plotly_chart(fig_price, use_container_width=True)

        else:
            st.warning('Dados de distribuição de categorias não encontrados.')
    else:
        st.error('Não foi possível carregar as estatísticas de categorias.')


# =================================================================================================
# --- Aba 4: STATUS DA API ---
# =================================================================================================
with tab4:
    st.header('🩺 Status de Saúde da API')

    if st.button('Verificar Status Agora'):
        health_status = api_client.get_health_status()

        api_status = health_status.get('api_status', 'down')
        db_status = health_status.get('database', {}).get('status', 'down')

        if api_status == 'up' and db_status == 'up':
            st.success('✅ **API e Banco de Dados estão operacionais!**')
        else:
            st.error('🚨 **Atenção! Foi detectado um problema.**')

        st.json(health_status)
