def formatar_br(numero):
    """Uma função simples para formatar números no padrão brasileiro."""
    # Formata com separador de milhar americano (,) e decimal (.)
    s = f'{numero:,.2f}'
    # Inverte os separadores
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    # Remove os decimais se o número for inteiro
    if numero == int(numero):
        return s[:-3]
    return s
