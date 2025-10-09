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


def _determinar_tipos(tipo_inicial, nome_pessoa, resp_legal, resp_financeiro):
    """
    Função auxiliar para identificar múltiplos papéis (RL, RF) de um contato.

    Args:
        tipo_inicial (str): O papel principal ('P' ou 'M').
        nome_pessoa (str): O nome da pessoa sendo analisada.
        resp_legal (str): Nome do Responsável Legal.
        resp_financeiro (str): Nome do Responsável Financeiro.

    Returns:
        list: Lista de tipos de responsabilidade que a pessoa possui.
    """
    tipos = [tipo_inicial]
    
    # Adiciona 'RL' se o nome corresponder ao Responsável Legal
    if nome_pessoa and nome_pessoa == resp_legal:
        tipos.append("RL")
        
    # Adiciona 'RF' se o nome corresponder ao Responsável Financeiro
    if nome_pessoa and nome_pessoa == resp_financeiro:
        tipos.append("RF")
        
    return tipos


def _formatar_contato(cod_turma, tipos, nome_pessoa, codigo_unidade, cod_aluno, nome_aluno, fone):
    """
    Função auxiliar para construir a chave de identificação completa do contato.

    Args:
        cod_turma (str): Código da turma.
        tipos (list): Lista de tipos de responsabilidade.
        nome_pessoa (str): Nome do titular do contato.
        codigo_unidade (str): Código da unidade escolar.
        cod_aluno (str): Identificador do estudante.
        nome_aluno (str): Nome do aluno.
        fone (str): Telefone padronizado.

    Returns:
        list: [identificacao_completa, telefone]
    """
    # Cria a string de identificação formatada
    identificacao = (
        f"{cod_turma} - ({' - '.join(tipos)}) {nome_pessoa} - "
        f"{codigo_unidade}|{cod_aluno} - (A) {nome_aluno}"
    )
    return [identificacao, fone]