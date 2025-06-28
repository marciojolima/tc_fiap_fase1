# Classes de Exceção Personalizadas
class ScraperException(Exception):
    """Exceção base para o scraper."""

    pass


class PaginatorNotFoundException(ScraperException):
    """Lançada quando o paginador não é encontrado na página."""

    pass


class ParsingException(ScraperException):
    """Lançada quando há um erro ao extrair dados de um elemento."""

    pass
