import os
from typing import List, Tuple

import pandas as pd

from api_books_tc.models import Book
from api_books_tc.settings import Settings


class DataBaseManager:
    def __init__(self):
        self.csv_path = Settings().CSV_PATH
        breakpoint()

    def load_books_from_csv(self) -> Tuple[List[Book], int]:
        """
        Carrega livros a partir de um arquivo CSV e retorna uma lista de dicionários
        e o número de livros carregados.

        Retorna:
            Tuple[List[Dict], int]:
            Uma tupla contendo uma lista de dicionários, onde cada dicionário representa um livro,
            e um inteiro indicando a quantidade de livros carregados.
            Retorna ([], 0) em caso de erro ou se o arquivo não existir.
        """
        try:
            if not os.path.exists(self.csv_path):
                return []
            df = pd.read_csv(self.csv_path)

            breakpoint()
            return df.to_dict('records'), len(df.index)
        except Exception:
            return []


db_manager = DataBaseManager()
