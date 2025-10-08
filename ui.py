import streamlit as st

def aplicar_estilo():
    """Aplica estilos CSS customizados para uma aparência mais moderna e temática na interface Streamlit."""
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(145deg, #f7f8fa, #eef1f5);
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #0061a8;
            color: white;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #004f8a;
            transform: scale(1.03);
        }
        .block-container {
            padding-top: 2rem;
        }
        .log-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            height: 280px;
            overflow-y: auto;
            font-size: 0.9rem;
            border: 1px solid #dce3ec;
        }
        </style>
    """, unsafe_allow_html=True)


def sidebar_ajuda():
    """
    Configura e exibe o menu lateral (sidebar) da aplicação Streamlit.

    Inclui um logotipo, instruções de uso e a lista de colunas obrigatórias
    esperadas no arquivo Excel.
    """
    with st.sidebar:
        st.markdown(
            """
            <div style='text-align: center;'>
                <img src="https://7edu-br.educadventista.org/assets/customs/img/educacao.png" width="100">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("## 💬 Ajuda")
        st.markdown("""
        **Como usar:**
        1. Faça upload do arquivo Excel (`.xlsx`);
        2. Digite o código da unidade;
        3. Clique em **Processar arquivo**;
        4. Baixe o CSV gerado.
        """)
        st.info("⚠️ Certifique-se de que o arquivo contém todas as colunas obrigatórias.\n")

        st.markdown("""
        **Colunas obrigatórias no Excel:**
         * Nome Completo (Aluno)
         * Turma
         * Identificador Estudante 
         * Pai (Nome)
         * Telefone do Pai
         * Mãe (Nome)
         * Telefone da Mãe
         * Responsável Legal 
         * Telefone do Responsável Legal
         * Responsável Financeiro
        """)