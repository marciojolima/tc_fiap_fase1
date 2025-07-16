import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.dashboard')
API_BASE_URL = os.getenv('API_URL', 'http://localhost:8000')


# @st.cache_data(ttl=3600)  # Cache de 1 hora para dados que não mudam frequentemente
def get_categories(name: str = '') -> list:
    """Busca a lista de categorias da API."""
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/categories/', params={'name': name})
        response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx
        data = response.json()
        return ['Todas'] + data.get('categories', [])
    except requests.RequestException as e:
        st.error(f'Erro ao buscar categorias: {e}')
        return ['Todas']


# @st.cache_data(ttl=60)  # Cache de 1 minuto para dados que podem mudar
def get_books(offset: int = 0, limit: int = 30, title: str = '', category: str = '') -> dict:
    """Busca livros com filtros."""
    params = {'offset': offset, 'limit': limit, 'title': title}
    if category and category != 'Todas':
        params['category'] = category

    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/books/', params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f'Erro ao buscar livros: {e}')
        return {'total': 0, 'books': []}


def get_health_status() -> dict:
    """Verifica o status da API."""
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/health')
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {
            'api_status': 'down',
            'database': {'status': 'down', 'error': 'Could not connect to API'},
            'internet_connectivity': {'status': 'down', 'error': 'Could not connect to API'},
        }


# @st.cache_data(ttl=3600)
def get_overview_stats() -> dict:
    """Busca as estatísticas gerais."""
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/stats/overview/')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f'Erro ao buscar estatísticas gerais: {e}')
        return {}


# @st.cache_data(ttl=60)
def get_top_rated_books(limit: int = 5) -> dict:
    """Busca os livros mais bem avaliados."""
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/stats/top-rated/', params={'limit': limit})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f'Erro ao buscar livros mais bem avaliados: {e}')
        return {'total': 0, 'books': []}


# @st.cache_data(ttl=60)
def get_books_by_price_range(min_price: float, max_price: float) -> dict:
    """Busca livros por faixa de preço."""
    try:
        response = requests.get(
            f'{API_BASE_URL}/api/v1/stats/price-range/',
            params={'min_price': min_price, 'max_price': max_price},
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f'Erro ao buscar livros por preço: {e}')
        return {'total': 0, 'books': []}


# @st.cache_data(ttl=3600)
def get_category_stats() -> dict:
    """Busca estatísticas de categorias."""
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/stats/categories/')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f'Erro ao buscar estatísticas de categorias: {e}')
        return {}
