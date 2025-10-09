import pandas as pd
from io import BytesIO
from datetime import datetime
from utils import safe_str, limpar_telefone_simples, adicionar_ddi_brasil


def processar_planilha(uploaded_file, codigo_unidade):
    """
    Processa um arquivo Excel contendo dados de alunos e responsáveis,
    validando, limpando e formatando os contatos para exportação.

    Args:
        uploaded_file (obj): Arquivo Excel carregado.
        codigo_unidade (str): Código identificador da unidade escolar.

    Returns:
        tuple: (df_contatos, contagem_tipos, usuarios_erro, sucessos, erros)
    
    Raises:
        ValueError: Se colunas obrigatórias estiverem ausentes no arquivo.
    """
    # 1. Leitura e Validação de Schema
    df = pd.read_excel(uploaded_file)
    
    colunas_obrigatorias = [
        'Pai', 'Mãe', 'Responsável Legal', 'Responsável Financeiro',
        'Turma', 'Nome Completo', 'Identificador Estudante',
        'Telefone da Mãe', 'Telefone do Pai', 'Série', 'Telefone do Responsável Legal'
    ]

    faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
    if faltantes:
        raise ValueError(f"Coluna(s) obrigatória(s) ausente(s): {', '.join(faltantes)}")

    # 2. Inicialização de Contadores e Estruturas
    contatos = []       
    usuarios_erro = []  
    sucessos = 0
    erros = 0
    contagem_tipos = {'P': 0, 'M': 0, 'RL': 0, 'RF': 0}
    seen = set()        # Set para desduplicação (identificação, telefone)

    # 3. Iteração e Processamento por Aluno
    for i, row in df.iterrows():
        nome_aluno = safe_str(row.get('Nome Completo'))
        turma_valor = safe_str(row.get('Turma'))
        # Extrai o código da turma, assumindo o formato 'PREFIXO-CODIGO'
        cod_turma = turma_valor.split('-', 1)[1] if '-' in turma_valor else turma_valor
        cod_aluno = safe_str(row.get('Identificador Estudante'))

        # Validação de dados mínimos
        if not nome_aluno or not turma_valor:
            erros += 1
            usuarios_erro.append({'usuario': nome_aluno or f'Linha {i+1}', 'motivo': 'Dados incompletos (Nome ou Turma)'})
            continue

        # Limpeza inicial dos telefones
        raw_mae = limpar_telefone_simples(row.get('Telefone da Mãe'))
        raw_pai = limpar_telefone_simples(row.get('Telefone do Pai'))
        raw_resp = limpar_telefone_simples(row.get('Telefone do Responsável Legal'))

        validados = []  # Lista de contatos válidos a serem inseridos
        invalidos = []  # Lista para rastrear telefones inválidos (opcional)

        # Processamento: PAI
        if raw_pai:
            if len(raw_pai) < 8:
                invalidos.append(('Pai', raw_pai))
            else:
                validados.append(('P', adicionar_ddi_brasil(raw_pai), safe_str(row.get('Pai'))))

        # Processamento: MÃE
        if raw_mae:
            if len(raw_mae) < 8:
                invalidos.append(('Mãe', raw_mae))
            else:
                validados.append(('M', adicionar_ddi_brasil(raw_mae), safe_str(row.get('Mãe'))))

        # Processamento: RESPONSÁVEL LEGAL
        resp_legal_nome = safe_str(row.get('Responsável Legal'))
        if raw_resp and len(raw_resp) >= 8:
            # Verifica se o RL não é duplicado como Pai ou Mãe
            if resp_legal_nome not in [safe_str(row.get('Pai')), safe_str(row.get('Mãe'))]:
                validados.append(('RL', adicionar_ddi_brasil(raw_resp), resp_legal_nome))

        # Processamento: RESPONSÁVEL FINANCEIRO
        resp_financeiro_nome = safe_str(row.get('Responsável Financeiro'))
        if resp_financeiro_nome:
            # Verifica se o RF não é duplicado como Pai, Mãe ou RL
            if resp_financeiro_nome not in [
                safe_str(row.get('Pai')),
                safe_str(row.get('Mãe')),
                safe_str(row.get('Responsável Legal'))
            ]:
                # Busca o telefone do RF se a coluna existir
                fone_fin = (
                    limpar_telefone_simples(row.get('Telefone do Responsável Financeiro'))
                    if 'Telefone do Responsável Financeiro' in df.columns else ''
                )
                if fone_fin and len(fone_fin) >= 8:
                    validados.append(('RF', adicionar_ddi_brasil(fone_fin), resp_financeiro_nome))

        # 4. Tratamento de Casos sem Contato Válido
        if not validados:
            motivo = 'Nenhum contato válido encontrado' if not invalidos else 'Telefone inválido'
            erros += 1
            usuarios_erro.append({'usuario': nome_aluno, 'motivo': motivo})
            continue

        # 5. Geração e Inserção dos Contatos Finais
        contatos_inseridos = 0
        for tipo, telefone, titular in validados:
            tipos = [tipo]
            # Formatação da chave de identificação única
            identificacao = (
                f"{cod_turma} - ({' - '.join(tipos)}) {titular or nome_aluno} - "
                f"{codigo_unidade}|{cod_aluno} - (A) {nome_aluno}"
            )
            key = (identificacao, telefone)
            
            if key in seen:
                usuarios_erro.append({'usuario': nome_aluno, 'motivo': f'Contato duplicado removido: {titular}'})
                continue
                
            seen.add(key)
            contatos.append([identificacao, telefone])
            contatos_inseridos += 1
            
            if tipo in contagem_tipos:
                contagem_tipos[tipo] += 1

        # 6. Atualização dos Contadores de Sucesso/Erro
        if contatos_inseridos > 0:
            sucessos += 1
        else:
            erros += 1
            usuarios_erro.append({'usuario': nome_aluno, 'motivo': 'Nenhum contato válido encontrado (duplicidade/filtro)'})

    # 7. Retorno final (garante desduplicação no DF final)
    df_contatos = pd.DataFrame(contatos, columns=['name', 'phone'])
    return df_contatos.drop_duplicates(), contagem_tipos, usuarios_erro, sucessos, erros


def gerar_csv_download(df, codigo_unidade):
    """
    Prepara o DataFrame processado para download, gerando um buffer BytesIO e
    o nome de arquivo formatado.

    Args:
        df (pd.DataFrame): DataFrame com os contatos finais (name, phone).
        codigo_unidade (str): Código da unidade escolar.

    Returns:
        tuple: (buffer_bytesio, nome_arquivo_str)
    """
    buffer = BytesIO()
    # Converte para CSV no buffer em memória
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    
    # Gera o timestamp para o nome do arquivo
    data = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"Lista_de_Contatos_{codigo_unidade}_{data}.csv"
    
    return buffer, nome_arquivo