# API de Consulta de Livros - Tech Challenge FIAP

![Status](https://img.shields.io/badge/status-concluído-green)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)
![Docker](https://img.shields.io/badge/Docker-gray.svg?logo=docker)

Este repositório contém o projeto desenvolvido para o **Tech Challenge da Pós-Graduação em Arquitetura de Software da FIAP**. Trata-se de uma API pública para consulta de livros, com funcionalidades de web scraping, análise de dados e um dashboard interativo.

## 🎥 Vídeo de Apresentação

[<img src="https://img.youtube.com/vi/ID_DO_VIDEO/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=ID_DO_VIDEO)

> **Clique na imagem acima para assistir à apresentação do projeto.**

##  Autores

- [Luca](https://github.com/lucapoit)
- [Luciana](https://github.com/Lucca-26)
- [Gabriel](https://github.com/gabrieljordan23/)
- [Márcio](https://github.com/marciojolima)

---

## 📋 Tabela de Conteúdos

1.  [Visão Geral do Projeto](#-1-visão-geral-do-projeto)
2.  [Arquitetura, Cenário de Uso e Features](#%EF%B8%8F-2-arquitetura-cen%C3%A1rio-de-uso-e-features)
3.  [Stack Tecnológica](#-3-stack-tecnológica)
4.  [Estrutura do Projeto](#-4-estrutura-do-projeto)
5.  [Instalação e Execução](#%EF%B8%8F-5-instalação-e-execução)
    - [Pré-requisitos](#pré-requisitos)
    - [Opção 1: Docker (Recomendado)](#opção-1-docker-recomendado)
    - [Opção 2: Poetry](#opção-2-poetry)
    - [Opção 3: Pip](#op%C3%A7%C3%A3o-3-pip)
    - [Dicas para execução](#Dicas-para-execução)
6.  [Documentação da API](#-6-documentação-da-api)
    - [Endpoints](#endpoints)
    - [Exemplos de Uso](#-exemplos-de-uso)
7.  [Dashboard Interativo](#-7-dashboard-interativo)
8.  [Sistema de Web Scraping](#%EF%B8%8F-8-sistema-de-web-scraping)
9.  [Testes](#-9-testes)
10. [Deploy](#%EF%B8%8F-10-deploy)

---

## 📘 1. Visão Geral do Projeto

Este projeto consiste em uma **API RESTful** pública para consulta de informações sobre livros. Os dados são extraídos do site [books.toscrape.com](https://books.toscrape.com/) através de um script de web scraping automatizado. As informações coletadas são processadas, armazenadas em um arquivo CSV e, em seguida, replicadas para um banco de dados SQLite para garantir consultas rápidas e eficientes.

A solução foi projetada para ser uma fonte de dados robusta e confiável, ideal para ser consumida por cientistas de dados, sistemas de recomendação ou qualquer aplicação que necessite de um catálogo de livros.

## 🏗️ 2. Arquitetura, Cenário de Uso e Features

### Plano Arquitetural

#### Arquitetura atual
![Arquitetura Atual](./docs/arquitetura_atual.png)


#### Arquitetura futura
![Arquitetura Futura](./docs/arquitetura_futura.png)



### Cenário de Uso para cientista de dados
➡️ **[Descrição de um cenário de uso da api-books](./docs/use_case.md)**


### Features

-   **API Robusta**: Construída com **FastAPI** para alta performance e documentação automática.
-   **Autenticação Segura**: Implementação de **JWT (JSON Web Tokens)** para proteger endpoints sensíveis.
-   **Web Scraping Automatizado**: Script para extração de dados, com persistência em CSV e banco de dados.
-   **Banco de Dados**: **SQLite** usando ORM (SqlAlchemy), com migrações gerenciadas pelo **Alembic** (Facilidade de alteração para Banco de Dados mais robusto).
-   **Dashboard Interativo**: Painel de visualização de dados e insights criado com **Streamlit**.
-   **Testes Automatizados**: Cobertura de testes para os principais endpoints da API utilizando **Pytest**.
-   **Containerização**: Aplicação totalmente conteinerizada com **Docker** e **Docker Compose** para fácil deploy e escalabilidade.
-   **Monitoramento**: Estrutura para logs preparada para futura implementação.

## 🚀 3. Stack Tecnológica

| Ferramenta | Descrição |
| :--- | :--- |
| **Python** | Linguagem principal do projeto. |
| **FastAPI** | Framework web para construção da API. |
| **Streamlit** | Framework para criação do dashboard interativo. |
| **SQLite** | Banco de dados relacional para armazenamento dos dados. |
| **Alembic** | Ferramenta para gerenciamento de migrações do banco de dados. |
| **Pydantic** | Validação de dados da API. |
| **SQLAlchemy** | ORM para interação com o banco de dados. |
| **BeautifulSoup4** | Biblioteca para extração de dados de páginas HTML (web scraping). |
| **Loguru** | Registro de cada requisição da api com [loguru](https://github.com/Delgan/loguru). |
| **Pytest** | Framework para execução dos testes automatizados. |
| **Docker** | Plataforma de containerização da aplicação. |
| **Poetry** | Gerenciador de dependências e pacotes. |

## 📁 4. Estrutura do Projeto

```
TECH CHALLENGE_FASE1/
├── README.md
├── alembic.ini
├── compose.yaml
├── pyproject.toml
├── data/
├── dockerfiles/
│   ├── Dockerfile.api
│   └── Dockerfile.dashboard
├── docs/
│   ├── arquitetura_atual.png
│   ├── arquitetura_futura.png
│   ├── script_scraper.md
│   └── use_case_md
├── logs/
├── migrations/
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── api_books/
│   └── dashboard/
└── tests/

```

---

## ⚙️ 5. Instalação e Execução

Siga os passos abaixo para executar o projeto localmente.

### Pré-requisitos
-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [Python 3.11+](https://www.python.org/) (para execução sem Docker)
-   [Poetry](https://python-poetry.org/)

### ⚙️ Variáveis de Ambiente
Para que o projeto funcione corretamente, você precisa criar dois arquivos de variáveis de ambiente na raiz do projeto: um para a **API** e outro para o **Dashboard**.
Eles definem informações sensíveis ou específicas do ambiente, como URLs, caminhos e chaves de segurança.


**IMPORTANTE: Seguem os valores de atribuição da variáveis de ambiente utilizadas no projeto para facilitar a instalação, ressaltando, no entanto, que não é uma boa prática a exposição delas fora do escopo do projeto.**

#### 📁 `.env.api` – Configuração da API
Crie um arquivo chamado `.env.api` na raiz do projeto e defina as seguintes variáveis:
```env
DATABASE_URL="sqlite:///data/books.db" # atribuído para fins didáticos. Não é uma boa prática
CSV_PATH="data/books.csv" # atribuído para fins didáticos. Não é um boa prática
SCRAPING_TARGET_URL="https://books.toscrape.com/" # atribuído para fins didáticos. Não é uma boa prática
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
SECRET_KEY="seu-segredo-nao-divulgue"  # atribuído para fins didáticos. Não é uma boa prática

```
#### 📁 `.env.dashboard` – Configuração da API
Crie um arquivo chamado `.env.dashboard` na raiz do projeto e defina as seguintes variáveis:
``` env
API_INTERNAL_URL=http://localhost:8000
API_EXTERNAL_URL=http://localhost:8000
```

### Opção 1: Docker (Recomendado)

Esta é a forma mais simples e recomendada para executar a aplicação completa (API e Dashboard).

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/marciojolima/tc_fiap_fase1.git
    cd tc_fiap_fase1
    ```
    
    ```
    #### 📁 `.env.docker.dashboard` – para o docker
    Crie um arquivo chamado `.env.docker.dashboard` na raiz do projeto e defina as seguintes variáveis:
    ``` env
    API_URL=http://api:8000
    ```


2.  **Inicie os containers com Docker Compose:**
    ```bash
    docker-compose up --build
    ```

3.  **Acesse os serviços:**
    -   **API:** [http://localhost:8000](http://localhost:8000)
    -   **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Dashboard:** [http://localhost:8501](http://localhost:8501)

### Opção 2: Poetry

Para executar a API localmente utilizando Poetry.

1.  **Clone o repositório e navegue até a pasta:**
    ```bash
    git clone https://github.com/marciojolima/tc_fiap_fase1.git
    cd tc_fiap_fase1
    ```

2.  **Instale as dependências:**
    ```bash
    poetry install
    ```

3.  **Execute as migrações do banco de dados:**
    ```bash
    poetry run alembic upgrade head
    ```

4.  **Inicie o servidor da API:**
    ```bash
    poetry run uvicorn src.api_books.main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Opção 3: Pip

1.  **Clone o repositório e crie um ambiente virtual:**
    ```bash
    git clone https://github.com/marciojolima/tc_fiap_fase1.git
    cd tc_fiap_fase1
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Inicie o servidor da API:**
    ```bash
    uvicorn src.api_books.main:app --host 0.0.0.0 --port 8000 --reload
    ```

### Dicas para execução

Como se trata de um projeto com fins educativos, os endpoints de usuários não contemplam todas as funcionalidades necessárias para um gerenciamento completo.

Recomenda-se criar um usuário (padrão admin) por meio do endpoint `POST /api/v1/users/`. Em seguida, utilize o Swagger para autenticar-se clicando no ícone de cadeado, e então acione o endpoint `POST /api/v1/scraping/trigger` para realizar o carregamento de todos os livros.

---

## 📖 6. Documentação da API

A API possui documentação interativa gerada automaticamente pelo FastAPI, disponível nos seguintes endpoints:

-   **Swagger UI:** `https://api-books.fly.dev/docs`
-   **ReDoc:** `https://api-books.fly.dev/redoc`

### Endpoints

A seguir, a lista completa de endpoints disponíveis:

| Método HTTP | Endpoint                       | Descrição                                         | Autenticação Necessária? |
| :---------- | :----------------------------- | :------------------------------------------------ | :----------------------- |
| `GET`       | `/`                            | Página inicial da API.                            | Não                      |
| `GET`       | `/api/v1/health`               | Verifica a saúde da API.                          | Não                      |
| `POST`      | `/api/v1/auth/login`           | Autentica um usuário e retorna um **access_token** JWT.      | Não                      |
| `POST`      | `/api/v1/auth/login`           | Gera um novo **access_token** usando um **refresh_token**      | Sim                      |
| `GET`       | `/api/v1/users/`               | Lista todos os usuários.                          | Sim (Admin)              |
| `POST`      | `/api/v1/users/`               | Cria um novo usuário.                             | Não                      |
| `GET`       | `/api/v1/books/`               | Lista todos os livros (com filtros opcionais).    | Não                      |
| `GET`       | `/api/v1/books/{book_id}`      | Busca um livro pelo seu ID.                       | Não                      |
| `GET`       | `/api/v1/categories/`          | Lista todas as categorias de livros.              | Não                      |
| `POST`      | `/api/v1/scraping/trigger`     | Inicia o processo de web scraping.                | Sim (Admin)              |
| `GET`       | `/api/v1/stats/overview/`      | Fornece um resumo estatístico da coleção.         | Não                      |
| `GET`       | `/api/v1/stats/top-rated/`     | Lista os livros ordenados pela melhor avaliação.  | Não                      |
| `GET`       | `/api/v1/stats/price-range/`   | Retorna a distribuição de preços por categoria.   | Não                      |
| `GET`       | `/api/v1/ml/features/`   | Extrai features prontas para modelos de Machine Learning.   | Não                      |
| `GET`       | `/api/v1/ml/training-data/`   | Fornece um conjunto de dados de treinamento (features + label).   | Não                      |
| `POST`      | `/api/v1/ml/predictions/`   | Prevê o preço de um livro com base em suas features (modelo fake).   | Não                      |
| `GET`       | `/api/v1/download/books/`   | Faz download automático de arquivo .csv com todos os livros registrados.   | Não                      |

### ✨ Exemplos de Uso

#### Obter Estatísticas Gerais

**Request:**

```http
GET https://api-books.fly.dev/api/v1/stats/overview/
```

**Response:**

```json
{
  "total_books": 1000,
  "average_price": 35.07,
  "count_categories": 50,
  "rating_distribuition": {
    "1.0": 226,
    "2.0": 196,
    "3.0": 203,
    "4.0": 179,
    "5.0": 196
  }
}
```

#### Buscar Livro por ID

**Request:**

```http
GET https://api-books.fly.dev/api/v1/books/345
```

**Response:**

```json
{
  "title": "A Study in Scarlet (Sherlock Holmes #1)",
  "price": 16.73,
  "rating": 2,
  "availability": true,
  "category": "Mystery",
  "image_url": "https://books.toscrape.com/media/cache/27/40/274003f2720f82844873945b87af6c19.jpg",
  "id": 345
}
```

#### Predição

Usado um modelo fake com função que simula um modelo ML usando uma fórmula matemática simples:

(Atribuição de pesos e valores "ideais".)
Preço = 25 (base) + (availability × 2) + (rating × 10)
Confiança baseada no rating (quanto maior o rating, maior a confiança)

**Request:**

```http
POST https://api-books.fly.dev/api/v1/ml/predictions/
```

```json
{
  "x1_availability": 15,
  "x2_rating": 4.3
}
```

**Response:**

```json
{
  "predicted_price": 98,
  "confidence": 0.86
}
```

---

## 📊 7. Dashboard Interativo

O projeto inclui um dashboard desenvolvido com **Streamlit** para visualização e análise dos dados coletados. Ele consome a própria API para exibir insights.

-   **Acesso Local (via Docker):** [http://localhost:8501](http://localhost:8501)
-   **Acesso Público:** [https://dashboard-books.fly.dev](https://dashboard-books.fly.dev)

## 🕷️ 8. Sistema de Web Scraping

O processo de coleta de dados é realizado por um script que navega pelo site [books.toscrape.com](https://books.toscrape.com/), extrai as informações relevantes de cada livro e as armazena em um arquivo `data/books.csv`. Este processo pode ser acionado manualmente através de um endpoint protegido da API.

Para mais detalhes sobre a implementação do script, consulte a documentação específica:
➡️ **[Documentação do Script de Scraping](./docs/script_scraper.md)**

## 🧪 9. Testes

A aplicação possui uma suíte de testes automatizados para garantir a qualidade e o funcionamento correto dos endpoints da API. Para executá-los:

1.  Certifique-se de que as dependências de desenvolvimento estão instaladas (via Poetry ou Pip).
2.  Execute o Pytest na raiz do projeto:

```bash
# Com Poetry
poetry run pytest

# Ou com Pip/Venv
pytest
```

## ☁️ 10. Deploy

A aplicação foi implantada na plataforma **Fly.io** e está publicamente acessível nos seguintes links:

-   **API em Produção:** [https://api-books.fly.dev](https://api-books.fly.dev)
-   **Documentação (Swagger):** [https://api-books.fly.dev/docs](https://api-books.fly.dev/docs)
-   **Documentação (Redoc):** [https://api-books.fly.dev/redoc](https://api-books.fly.dev/redoc)
-   **Dashboard:** [https://dashboard-books.fly.dev/](https://dashboard-books.fly.dev)
