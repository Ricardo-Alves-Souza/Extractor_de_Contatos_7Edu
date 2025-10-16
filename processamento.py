import pandas as pd
from io import BytesIO
from datetime import datetime
from utils import safe_str, limpar_telefone_simples, adicionar_ddi_brasil


# ===============================
# 🧩 Funções auxiliares
# ===============================
def validar_schema(df):
    """Verifica se todas as colunas obrigatórias estão presentes no DataFrame."""
    colunas_obrigatorias = [
        'Nome Completo',
        'Identificador Estudante',
        'Turma',
        'Pai', 'Telefone do Pai',
        'Mãe', 'Telefone da Mãe',
        'Responsável Legal', 'Telefone do Responsável Legal',
        'Responsável Financeiro', 'Telefone do Responsável Financeiro'
    ]
    faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
    if faltantes:
        raise ValueError(f"Coluna(s) obrigatória(s) ausente(s): {', '.join(faltantes)}")


def limpar_dados_responsavel(nome, telefone):
    """Limpa nome e telefone de um responsável."""
    return safe_str(nome), limpar_telefone_simples(telefone)


def processar_responsavel(tipo_base, nome, telefone, nome_rl, nome_rf, usuarios_sem_telefone, total_sem_telefone, validados, invalidos):
    """Valida um responsável e adiciona aos contatos válidos, se aplicável."""
    if not nome:
        return total_sem_telefone

    if not telefone:
        usuarios_sem_telefone.append({'usuario': nome, 'motivo': f'⚠️ {tipo_base} sem telefone cadastrado'})
        return total_sem_telefone + 1

    if len(telefone) < 8 or telefone[0] == '0':
        invalidos.append((tipo_base, telefone))
        return total_sem_telefone

    tipos = [tipo_base[0]]  # P, M, RL, RF
    if nome == nome_rl and "RL" not in tipos:
        tipos.append("RL")
    if nome == nome_rf and "RF" not in tipos:
        tipos.append("RF")

    validados.append((tipos, adicionar_ddi_brasil(telefone), nome))
    return total_sem_telefone


def montar_identificacao(tipos, titular, cod_turma, cod_aluno, nome_aluno, codigo_unidade):
    """Monta a string final de identificação do contato."""
    return (
        f"{cod_turma} - ({' - '.join(tipos)}) {titular or nome_aluno} - "
        f"{codigo_unidade}|{cod_aluno} - (A) {nome_aluno}"
    )


# ===============================
# 🧠 Função principal
# ===============================
def processar_planilha(uploaded_file, codigo_unidade):
    """
    Processa um arquivo Excel contendo dados de alunos e responsáveis.
    Retorna DataFrame de contatos válidos + estatísticas.
    """
    df = pd.read_excel(uploaded_file)
    validar_schema(df)

    contatos = []
    usuarios_erro = []
    usuarios_sem_telefone = []
    sucessos = erros = total_sem_telefone = 0
    contagem_tipos = {'P': 0, 'M': 0, 'RL': 0, 'RF': 0}
    seen = set()

    for i, row in df.iterrows():
        nome_aluno = safe_str(row.get('Nome Completo'))
        turma_valor = safe_str(row.get('Turma'))
        cod_turma = turma_valor.split('-', 1)[1] if '-' in turma_valor else turma_valor
        cod_aluno = safe_str(row.get('Identificador Estudante'))

        if not nome_aluno or not turma_valor:
            erros += 1
            usuarios_erro.append({
                'usuario': nome_aluno or f'Linha {i+1}',
                'motivo': 'Dados incompletos (Nome ou Turma)'
            })
            continue

        nome_pai, tel_pai = limpar_dados_responsavel(row.get('Pai'), row.get('Telefone do Pai'))
        nome_mae, tel_mae = limpar_dados_responsavel(row.get('Mãe'), row.get('Telefone da Mãe'))
        nome_rl, tel_rl = limpar_dados_responsavel(row.get('Responsável Legal'), row.get('Telefone do Responsável Legal'))
        nome_rf, tel_rf = limpar_dados_responsavel(row.get('Responsável Financeiro'), row.get('Telefone do Responsável Financeiro'))

        validados, invalidos = [], []
        total_sem_telefone = processar_responsavel("Pai", nome_pai, tel_pai, nome_rl, nome_rf, usuarios_sem_telefone, total_sem_telefone, validados, invalidos)
        total_sem_telefone = processar_responsavel("Mãe", nome_mae, tel_mae, nome_rl, nome_rf, usuarios_sem_telefone, total_sem_telefone, validados, invalidos)

        if nome_rl and nome_rl not in [nome_pai, nome_mae]:
            total_sem_telefone = processar_responsavel("RL", nome_rl, tel_rl, nome_rl, nome_rf, usuarios_sem_telefone, total_sem_telefone, validados, invalidos)
        if nome_rf and nome_rf not in [nome_pai, nome_mae, nome_rl]:
            total_sem_telefone = processar_responsavel("RF", nome_rf, tel_rf, nome_rl, nome_rf, usuarios_sem_telefone, total_sem_telefone, validados, invalidos)

        if not validados or invalidos:
            erros += 1
            motivo = '🔴 Nenhum telefone válido encontrado' if not invalidos else '🔴 Telefone inválido'
            usuarios_erro.append({'usuario': nome_aluno, 'motivo': motivo})
            continue

        contatos_inseridos = 0
        for tipos, telefone, titular in validados:
            identificacao = montar_identificacao(tipos, titular, cod_turma, cod_aluno, nome_aluno, codigo_unidade)
            key = (identificacao, telefone)
            if key in seen:
                usuarios_erro.append({'usuario': nome_aluno, 'motivo': f'Contato duplicado removido: {titular}'})
                continue

            seen.add(key)
            contatos.append([identificacao, telefone])
            contatos_inseridos += 1

            if "P" in tipos: contagem_tipos["P"] += 1
            if "M" in tipos: contagem_tipos["M"] += 1
            if "RL" in tipos and "P" not in tipos and "M" not in tipos: contagem_tipos["RL"] += 1
            if "RF" in tipos and all(t not in tipos for t in ["P", "M", "RL"]): contagem_tipos["RF"] += 1

            sucessos += 1 if contatos_inseridos > 0 else 0

    df_contatos = pd.DataFrame(contatos, columns=['name', 'phone']).drop_duplicates()
    return df_contatos, contagem_tipos, usuarios_erro, sucessos, erros, usuarios_sem_telefone, total_sem_telefone


def gerar_csv_download(df, codigo_unidade):
    """Gera buffer CSV com nome de arquivo formatado."""
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    data = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"Lista_de_Contatos_{codigo_unidade}_{data}.csv"
    return buffer, nome_arquivo


def gerar_xlsx_erros(usuarios_erro, usuarios_sem_telefone, codigo_unidade):
    """Gera XLSX com relatório de erros e avisos."""
    erros_data = usuarios_erro + usuarios_sem_telefone
    df = pd.DataFrame(erros_data)
    
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    
    data = datetime.now().strftime("%Y%m%d_%H%M")
    nome_arquivo = f"Relatorio_Erros_{codigo_unidade}_{data}.xlsx"
    return buffer, nome_arquivo

