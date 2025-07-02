Com certeza! Aqui está o arquivo Markdown atualizado para refletir o novo código e incluir as observações sobre a estratégia de retry e as boas práticas para não sobrecarregar o servidor.

---

# Fluxo do Script de Scraping - AsyncBookScraper

O fluxo está organizado de forma hierárquica, mostrando cada etapa do processo de extração de dados. Os pontos principais são:

**🔧 Setup → 📊 Descoberta → 🌐 Busca Paralela → 🔍 Parsing Detalhado → 💾 Persistência**

A grande vantagem do script é o **duplo paralelismo**: primeiro, busca todas as páginas de listagem simultaneamente; depois, faz o parsing detalhado de cada livro, que inclui uma nova requisição à página de detalhes de cada livro, também em paralelo. Isso resulta em uma performance excelente.

## 📋 Resumo

Script assíncrono em Python que extrai dados de livros do site `books.toscrape.com`, gerencia a concorrência de requisições, implementa uma estratégia de retry e salva os dados consolidados em um arquivo CSV.

## 🌳 Estrutura do Fluxo

### 📦 `AsyncBookScraper.run()`

*   **🔧 Configuração Inicial**
    *   Criar semáforo (`asyncio.Semaphore`) para controlar a concorrência.
    *   Configurar sessão HTTP (`aiohttp`) com a biblioteca `aiohttp-retry`, definindo uma estratégia de **retry exponencial**.
    *   Definir `HEADERS` para simular um navegador real.

*   **📊 Descoberta de Estrutura**
    *   `_get_total_pages()`
        *   Acessar a página inicial.
        *   Encontrar o elemento de paginação (`li.current`).
        *   Extrair o número total de páginas via regex.
        *   Lançar exceção customizada (`PaginatorNotFoundException`) se o paginador não for encontrado.

*   **🔗 Geração de URLs**
    *   `_generate_page_urls()`
        *   Criar uma lista de URLs para todas as páginas de catálogo.
        *   Formato: `/catalogue/page-{N}.html`

*   **🌐 Busca Assíncrona de Páginas de Listagem**
    *   `_fetch_all_pages()`
        *   Criar uma `task` para cada URL de página de listagem.
        *   Executar todas as requisições simultaneamente usando `asyncio.gather`.
        *   Filtrar respostas que falharam, garantindo a robustez.

*   **📚 Extração de Elementos de Livros**
    *   `_extract_books_from_pages()`
        *   Para cada página HTML, encontrar todos os elementos `<article class="product_pod">`.
        *   Consolidar uma lista única com todos os elementos de livros encontrados.

*   **🔍 Parsing Detalhado (Assíncrono)**
    *   `_parse_all_books()` -> Para cada livro → `_parse_book()`
        *   **1. Extrair dados básicos da lista:**
            *   Título, Preço, Disponibilidade e Rating.
        *   **2. Acessar página individual do livro (nova requisição assíncrona):**
            *   Chama `_get_image_path_and_category()`, que faz uma nova requisição para a URL de detalhes do livro.
        *   **3. Extrair dados detalhados:**
            *   Categoria e URL da Imagem.

*   **💾 Salvamento**
    *   `_save_to_csv()`
        *   Criar arquivo `books.csv` no local definido.
        *   Escrever o cabeçalho e os dados de todos os livros.
        *   Confirmar a conclusão da escrita no console.

## ⚡ Características Técnicas

### Concorrência
*   **Semáforo:** Limita o número máximo de requisições simultâneas (padrão: 15) para não sobrecarregar o servidor.
*   **Async/Await:** Utiliza operações de I/O não-bloqueantes para máxima eficiência.
*   **Gather:** Executa múltiplas `tasks` (busca de páginas e parsing de livros) em paralelo.

### Robustez e Respeito ao Servidor
*   **Estratégia de Retry:**
    *   Utiliza a biblioteca `aiohttp-retry` com uma política de `ExponentialRetry`.
    *   **Tentativas:** Tenta novamente até 5 vezes em caso de erros de servidor (status `500`, `502`, `503`, `504`).
    *   **Backoff:** O tempo de espera entre as tentativas aumenta exponencialmente, uma prática recomendada para dar tempo ao servidor de se recuperar.
*   **Timeout:** Define um timeout de 5 segundos por requisição para evitar que o script fique preso.
*   **Tratamento de Erro:** Exceções customizadas (`ScraperException`) para falhas críticas e tratamento de erros de requisição individuais, permitindo que o script continue a processar os dados válidos.
*   **User-Agent:** Define um `User-Agent` comum para identificar o scraper como um cliente web padrão, uma prática de boa vizinhança.

### Performance
*   **2 Níveis de Paralelismo:**
    1.  **Busca de páginas de listagem:** Todas as 50 páginas de catálogo são baixadas em paralelo.
    2.  **Parsing de livros:** O parsing de cada um dos 1000 livros, que inclui uma requisição à sua página de detalhes, também ocorre em paralelo.
*   **Filtros:** Remove páginas ou dados inválidos para garantir a qualidade do resultado final.

## 📈 Fluxo de Dados

`URL Base → Páginas de Lista → Elementos HTML → Requisições de Detalhe → Dados Estruturados → CSV`

```
books.toscrape.com
        ↓
   50 páginas de listagem HTML (em paralelo)
        ↓
   ~1000 elementos <article>
        ↓
   ~1000 requisições para páginas de detalhe (em paralelo)
        ↓
   Dados extraídos por livro:
   • ID, Título, Preço, Disponibilidade
   • Rating, Categoria, URL da Imagem
        ↓
   books.csv
```

## 🎯 Resultado Final

*   **Arquivo:** `books.csv`
*   **Localização:** Diretório definido nas configurações (ex: `data/`).
*   **Conteúdo:** Dados de todos os livros encontrados no site.
*   **Formato:** CSV com cabeçalhos (`id`, `title`, `price`, etc.).