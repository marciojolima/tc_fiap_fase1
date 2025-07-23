
## Caso de uso

### Estratégia TF-IDF

Tanto a frase digitada quanto os livros do catálogo são transformados em vetores numéricos usando o algoritmo TF-IDF (Term Frequency-Inverse Document Frequency).

O que o TF-IDF faz:
Dá mais peso para palavras relevantes da frase (por exemplo, "humanidade", "poesia").
Ignora palavras comuns como “o”, “de”, “em” (as chamadas stopwords).

Essa transformação permite que a consulta do usuário seja comparada matematicamente com os livros do banco de dados, com base no conteúdo textual de cada um (título + categoria).

### Resumo

Você escreve o que está buscando, como ‘livro sobre poesia’ ou ‘história da humanidade’. O sistema entende as palavras que você usou, procura os livros mais parecidos com essa ideia, e mostra primeiro os que têm nota melhor. Não precisa acertar o nome exato de um livro — ele entende o assunto que você quer.

### Resutaldo esperado:
* Semântica e textualmente próximos da pesquisa.
* Prioridade para os mais bem avaliados.

### Código

```
# 1. imports e bibliotecas necessárias
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
```

#### dowload a partir do endpoint `/api/v1/download/books/`

```
# 2. Carrega dos dados
df = pd.read_csv('books.csv')
```

```
# 3. Cria uma coluna combinando título + categoria
df["text"] = df["title"] + " " + df["category"]
```


```
# 4. Cria uma coluna combinando título + categoria
df["text"] = df["title"] + " " + df["category"]
```

```
# 5. Vetorização com TF-IDF
#vectorizer = TfidfVectorizer(stop_words='english')
vectorizer = TfidfVectorizer(stop_words=stopwords_pt)
tfidf_matrix = vectorizer.fit_transform(df["text"])
```

```
# 6. Calcula similaridade do cosseno entre todos os livros
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
```

```
# 7. Cria um índice mapeando título → linha do dataframe
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()
```

```
# 8. Função para fazer a recomendação
def recomendar_livros(consulta, top_n=5):
    # Vetoriza a consulta usando o mesmo vectorizer treinado com os livros
    consulta_vec = vectorizer.transform([consulta])

    # Calcula similaridade entre a consulta e todos os livros
    sim_scores = cosine_similarity(consulta_vec, tfidf_matrix).flatten()

    # Combina com os ratings
    scores_ajustados = sim_scores * (df["rating"] / 5.0)

    # Pega os top_n índices com maior score
    top_indices = scores_ajustados.argsort()[::-1][:top_n]

    recomendacoes = df.iloc[top_indices][["title", "category", "price", "rating"]]
    return recomendacoes.reset_index(drop=True)
```
```
# 9 Exemplo: recomendar parecidos com "Sapiens: A Brief History of Humankind"
recomendar_livros("book about humankind")
```