import streamlit as st


def aplicar_estilo():
    """
    Aplica estilos CSS globais e customizados à aplicação Streamlit
    para garantir um visual padronizado e moderno.
    """
    st.markdown("""
    <style>
    /* Definição de Variáveis de Cor */
    :root{
        --bg:#f5f7fa;
        --card:#ffffff;
        --muted:#6b7280;
        --accent:#2c3e50;
        --success:#16a34a;
        --danger:#dc2626;
    }
    /* Estilos Globais de Layout */
    .block-container{ 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
        max-width: 1200px; 
    }
    /* Estilos de Tipografia */
    .titulo-principal{ 
        text-align: center; 
        color: var(--accent); 
        font-size: 1.95rem; 
        font-weight: 800; 
        margin-bottom: 0.3rem; 
    }
    .subtitulo{ 
        text-align: center; 
        color: var(--muted); 
        font-size: 1rem; 
        margin-bottom: 1.4rem; 
    }
    .card{ 
        background: var(--card); 
        border-radius: 12px; 
        padding: 1rem; 
        box-shadow: 0 8px 22px rgba(44,62,80,0.06); 
        border: 1px solid #eef2f6; 
    }
    .titulo-secao{ 
        font-weight: 700; 
        font-size: 1.15rem; 
        margin-bottom: 0.6rem; 
    }
    /* Estilos de Botões Customizados */
    .stButton>button{ 
        background: linear-gradient(180deg, var(--accent), #22303a); 
        color: white; 
        border-radius: 8px; 
        padding: 0.6rem 1rem; 
    }
    .stButton>button:hover{ 
        transform: translateY(-2px); 
        box-shadow: 0 8px 24px rgba(34,48,58,0.12); 
    }
    div.stDownloadButton > button{ 
        background: linear-gradient(180deg, #198754, #157347); /* Verde para Download/Sucesso */
        color: white; 
        border-radius: 8px; 
        padding: 0.6rem 1rem; 
    }
    </style>
    """, unsafe_allow_html=True)


def sidebar_ajuda():
    """
    Cria a barra lateral de ajuda, incluindo o logo, instruções de uso
    e a lista de colunas obrigatórias da planilha.
    """
    with st.sidebar:
        # Logo
        st.markdown("""
            <div style='text-align: center; margin-bottom: 1rem;'>
                <img src="https://7edu-br.educadventista.org/assets/customs/img/educacao.png" width="100">
            </div>
        """, unsafe_allow_html=True)
        
        # Instruções
        st.markdown("## 📘 Como usar")
        st.markdown("""
        1️⃣ Faça upload do arquivo Excel (.xlsx)  
        2️⃣ Selecione a unidade escolar  
        3️⃣ Clique em **Processar arquivo** 4️⃣ Baixe o CSV gerado ✅
        """)
        
        # Alerta e Colunas Obrigatórias
        st.info("⚠️ Certifique-se de que o arquivo contém todas as colunas obrigatórias.")
        st.markdown("#### 📄 Colunas obrigatórias")
        st.markdown("""
        - Nome Completo (Aluno)  
        - Turma  
        - Identificador Estudante  
        - Pai / Telefone do Pai  
        - Mãe / Telefone da Mãe  
        - Responsável Legal / Telefone do Responsável Legal  
        - Responsável Financeiro / Telefone do Responsável Financeiro
        """)


def cabecalho_principal():
    """
    Renderiza o título e o subtítulo principais da aplicação no corpo da página.
    """
    st.markdown("""
        <div style="margin-top: 2.4rem; margin-bottom: 0.6rem;">
            <div class="titulo-principal">Extractor de Contatos 📇</div>
            <div class="subtitulo">Gere rapidamente listas de contatos a partir de planilhas do 7Edu.</div>
        </div>
    """, unsafe_allow_html=True)


def titulo_secao(texto):
    """
    Aplica o estilo padronizado de título de seção (classe .titulo-secao) ao texto.

    Args:
        texto (str): O texto a ser formatado como título de seção.
    """
    st.markdown(f"<div class='titulo-secao'>{texto}</div>", unsafe_allow_html=True)