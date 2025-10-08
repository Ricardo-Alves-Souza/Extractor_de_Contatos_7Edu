import pandas as pd
import streamlit as st
from io import BytesIO
from datetime import datetime
from utils import safe_str, limpar_telefone_simples, adicionar_ddi_brasil, _determinar_tipos, _formatar_contato


def processar_planilha(uploaded_file, codigo_unidade, log_area):
    """
    Lê o arquivo Excel, valida as colunas e gera um DataFrame de contatos formatados.

    O processamento itera sobre cada linha do DataFrame de entrada para extrair e formatar
    os dados de contato do Pai, Mãe e Responsável Legal, garantindo que o número
    de telefone esteja limpo e contenha o DDI do Brasil ('55'). Contatos duplicados
    (nome e telefone) são removidos.

    Args:
        uploaded_file (UploadedFile): O arquivo Excel enviado pelo usuário via Streamlit.
        codigo_unidade (str): O código da unidade escolar a ser incluído na identificação.
        log_area (streamlit.container): Contêiner Streamlit para exibir logs de status.

    Returns:
        pd.DataFrame: Um DataFrame com duas colunas ('name', 'phone') contendo os
                      contatos formatados e únicos.

    Raises:
        ValueError: Se alguma coluna obrigatória estiver faltando no arquivo Excel.
    """
    df = pd.read_excel(uploaded_file)
    colunas_obrigatorias = [
        'Pai', 'Mãe', 'Responsável Legal', 'Responsável Financeiro',
        'Turma', 'Nome Completo', 'Identificador Estudante',
        'Telefone da Mãe', 'Telefone do Pai', 'Série', 'Telefone do Responsável Legal'
    ]

    for col in colunas_obrigatorias:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória não encontrada: '{col}'")
            

    contatos = []
    total = len(df)
    status_text = st.empty()

    for i, row in df.iterrows():
        nome_pai = safe_str(row.get('Pai'))
        nome_mae = safe_str(row.get('Mãe'))
        resp_legal = safe_str(row.get('Responsável Legal'))
        resp_financeiro = safe_str(row.get('Responsável Financeiro'))
        turma_valor = safe_str(row.get('Turma'))
        cod_turma = turma_valor.split('-', 1)[1] if '-' in turma_valor else turma_valor
        nome_aluno = safe_str(row.get('Nome Completo'))
        cod_aluno = safe_str(row.get('Identificador Estudante'))
        
        fone_mae = adicionar_ddi_brasil(limpar_telefone_simples(row.get('Telefone da Mãe')) )
        fone_pai = adicionar_ddi_brasil(limpar_telefone_simples(row.get('Telefone do Pai')))
        fone_responsavel_legal = adicionar_ddi_brasil(limpar_telefone_simples(row.get('Telefone do Responsável Legal')))

        # Adicionar Contato do Pai
        if nome_pai and fone_pai:
            tipos_pai = _determinar_tipos("P", nome_pai, resp_legal, resp_financeiro)
            contato_pai = _formatar_contato(cod_turma, tipos_pai, nome_pai, codigo_unidade, cod_aluno, nome_aluno, fone_pai)
            contatos.append(contato_pai)

        # Adicionar Contato da Mãe
        if nome_mae and fone_mae:
            tipos_mae = _determinar_tipos("M", nome_mae, resp_legal, resp_financeiro)
            contato_mae = _formatar_contato(cod_turma, tipos_mae, nome_mae, codigo_unidade, cod_aluno, nome_aluno, fone_mae)
            contatos.append(contato_mae)

        # Adicionar Contato do Responsável Legal Secundário (se não for o Pai ou a Mãe)
        if (nome_pai != resp_legal) and (nome_mae != resp_legal) and resp_legal and fone_responsavel_legal:
            tipo_responsavel = ["RL"]
            
            if resp_legal == resp_financeiro: 
                tipo_responsavel.append("RF")
                
            contato_rl = _formatar_contato(cod_turma, tipo_responsavel, resp_legal, codigo_unidade, cod_aluno, nome_aluno, fone_responsavel_legal)
            contatos.append(contato_rl)

        status_text.text(f"🔄 Processando contatos... ({i + 1}/{total})")

    contatos_df = pd.DataFrame(contatos, columns=['name', 'phone']).drop_duplicates()
    status_text.text("✅ Processamento concluído!")
    return contatos_df


def gerar_csv_download(df, codigo_unidade):
    """
    Gera um arquivo CSV a partir do DataFrame de contatos e retorna o buffer e nome do arquivo para download.

    Args:
        df (pd.DataFrame): O DataFrame de contatos processado.
        codigo_unidade (str): O código da unidade escolar para ser usado no nome do arquivo.

    Returns:
        tuple: Uma tupla contendo (buffer, nome_arquivo), onde:
               - buffer (BytesIO): O buffer de memória contendo o conteúdo CSV.
               - nome_arquivo (str): O nome formatado do arquivo CSV.
    """
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    data = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"Lista_de_Contatos_{codigo_unidade}_{data}.csv"
    return buffer, nome_arquivo