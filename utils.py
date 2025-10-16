def safe_str(value):
    """
    Garante que o valor seja retornado como uma string limpa e segura.

    Args:
        value (any): O valor a ser convertido.

    Returns:
        str: String vazia se None, ou string limpa (strip) do valor.
    """
    if value is None:
        return ""
    return str(value).strip()


def limpar_telefone_simples(telefone):
    """
    Remove todos os caracteres não numéricos de uma string de telefone.

    Args:
        telefone (str/any): O número de telefone bruto.

    Returns:
        str: String contendo apenas dígitos. Retorna '' se a entrada for falsy.
    """
    # Garante que a entrada seja string antes de iterar
    return "".join(c for c in str(telefone) if c.isdigit()) if telefone else ""


def adicionar_ddi_brasil(numero_limpo):
    """
    Adiciona o DDI brasileiro ('55') ao número, se ele ainda não estiver presente.

    Args:
        numero_limpo (str): Número de telefone limpo (somente dígitos).

    Returns:
        str: Número de telefone padronizado com DDI.
    """
    if not numero_limpo:
        return ''
    
    # Verifica se já começa com '55'
    if not numero_limpo.startswith('55'):
        return '55' + numero_limpo
        
    return numero_limpo