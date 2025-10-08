import streamlit as st
            @st.cache_data
from datetime import datetime
from processamento import processar_planilha, gerar_csv_download
from ui import aplicar_estilo, sidebar_ajuda



st.set_page_config(
    page_title="Extractor de Contatos - 7Edu",
    page_icon="📞",
    layout="wide"
)

aplicar_estilo()
sidebar_ajuda()

st.markdown("""
    <div style="text-align: center;">
        <h1>Geração de Lista de Contatos 📇</h1>
        <p style="color: gray; font-size:16px;">
            Criação de lista de contatos a partir da extração de dados do 7Edu.
        </p>
    </div>
""", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div style='text-align: center; font-weight: 600;'>📤 Selecione o arquivo Excel</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["xlsx", "xls"])

with col2:
    st.markdown("<div style='text-align: center; font-weight: 600;'>🏫 Código da unidade escolar</div>", unsafe_allow_html=True)
    codigo_unidade = st.text_input("", "")

st.divider()

st.markdown("### 🔄 Log de processamento")
log_area = st.container()
with log_area:
    log_box = st.empty()

if uploaded_file and codigo_unidade.strip():
    if st.button("🚀 Processar arquivo", use_container_width=True):
        try:
            with st.spinner("Processando contatos..."):
                contatos_df = processar_planilha(uploaded_file, codigo_unidade, log_area)

            buffer, nome_arquivo = gerar_csv_download(contatos_df, codigo_unidade)

            st.markdown(
                """
                <style>
                div.stDownloadButton > button {
                    background-color: #ff5722;
                    color: white;
                    font-size: 16px;
                    font-weight: 600;
                    padding: 0.75rem 1.5rem;
                    border-radius: 12px;
                    transition: transform 0.2s ease, filter 0.2s ease;
                }
                div.stDownloadButton > button:hover {
                    transform: scale(1.05);
                    filter: brightness(1.1);
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                label="📥 Baixar CSV Gerado",
                data=buffer,
                file_name=nome_arquivo,
                mime="text/csv",
                use_container_width=True
            )

            st.dataframe(contatos_df, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {e}")

elif uploaded_file and not codigo_unidade.strip():
    st.info("⬆️ Digite o código da unidade para habilitar o botão de processar.")

else:
    st.info("⬆️ Envie um arquivo e informe o código da unidade para começar.")

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: gray; font-size: 14px; margin-top: 20px;'>
        Desenvolvido por <b>Ricardo Alves de Souza</b> · {datetime.now().year}<br>
        <span style='font-size: 13px;'>Extractor de Contatos - Versão 1.0</span>
    </div>
    """,
    unsafe_allow_html=True
)