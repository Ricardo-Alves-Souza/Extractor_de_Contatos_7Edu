def safe_str(value):
    """
    Converte um valor em uma string segura, lidando com None e removendo espaços.

    Garante que, ao trabalhar com dados de fontes externas, se evitem erros de tipo (TypeError) 
    causados por valores nulos (None) e que a string resultante seja limpa.

    Args:
        value (any): O valor de entrada a ser convertido (ex: str, int, float, None).

    Returns:
        str: Uma string limpa (sem espaços no início/fim). Retorna "" se o valor de entrada for None.
    """
    if value is None:
        return ""
    
    return str(value).strip()


def limpar_telefone_simples(telefone):
    """
    Remove todos os caracteres que não são dígitos de uma string de telefone.

    Args:
        telefone (str): A string de telefone original (ex: "(11) 9999-0000 ramal 123").

    Returns:
        str: O número de telefone limpo, contendo apenas dígitos (ex: "1199990000123").
    """
    return "".join(c for c in telefone if c.isdigit())


def adicionar_ddi_brasil(numero_limpo):
    """
    Garante que o número de telefone limpo comece com o DDI do Brasil ('55').

    Trata o caso de strings vazias para evitar a criação de prefixos inválidos.

    Args:
        numero_limpo (str): O número de telefone contendo apenas dígitos (saída de limpar_telefone_simples).

    Returns:
        str: O número de telefone com o prefixo '55' garantido. Retorna uma string vazia se o 
             número de entrada estava vazio.
    """
    if not numero_limpo:
        return ''
    
    if not numero_limpo.startswith('55'):
        return '55' + numero_limpo
    
    return numero_limpo


def _determinar_tipos(tipo_inicial, nome_pessoa, resp_legal, resp_financeiro):
    """
    Determina e retorna a lista de tipos de contato (P, M, RL, RF) para uma pessoa.

    Verifica se a pessoa também é Responsável Legal (RL) e/ou Responsável Financeiro (RF).

    Args:
        tipo_inicial (str): O tipo de contato base ("P" para Pai, "M" para Mãe).
        nome_pessoa (str): O nome da pessoa sendo avaliada.
        resp_legal (str): Nome do Responsável Legal.
        resp_financeiro (str): Nome do Responsável Financeiro.

    Returns:
        list: Uma lista de strings com os tipos de responsabilidade (ex: ["P", "RL", "RF"]).
    """
    tipos = [tipo_inicial]
    if nome_pessoa and nome_pessoa == resp_legal:
        tipos.append("RL")
    if nome_pessoa and nome_pessoa == resp_financeiro:
        tipos.append("RF")
    return tipos

def _formatar_contato(cod_turma, tipos, nome_pessoa, codigo_unidade, cod_aluno, nome_aluno, fone):
    """
    Monta a tupla final de contato no formato [string_identificacao, telefone].

    Cria a string de identificação detalhada que inclui turma, tipos de contato, unidade e dados do aluno.

    Args:
        cod_turma (str): Código da turma.
        tipos (list): Lista de tipos de contato (ex: ["M", "RL"]).
        nome_pessoa (str): Nome da pessoa de contato.
        codigo_unidade (str): Código da unidade escolar.
        cod_aluno (str): Código do aluno.
        nome_aluno (str): Nome do aluno.
        fone (str): Número de telefone limpo da pessoa.

    Returns:
        list: Uma lista contendo a string de identificação formatada e o telefone.
    """
    identificacao = f"{cod_turma} - ({' - '.join(tipos)}) {nome_pessoa} - {codigo_unidade}|{cod_aluno} - (A) {nome_aluno}"
    return [identificacao, fone]