import streamlit as st
from datetime import datetime
from processamento import processar_planilha, gerar_csv_download, gerar_xlsx_erros
from ui import aplicar_estilo, sidebar_ajuda, cabecalho_principal, titulo_secao
from config import UNIDADES

st.set_page_config(
    page_title="Extractor de Contatos - 7Edu",
    page_icon="📞",
    layout="wide"
)

aplicar_estilo()
sidebar_ajuda()
cabecalho_principal()

st.markdown("---")
titulo_secao("Upload e Unidade Escolar")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📤 Selecione o arquivo Excel", type=["xlsx", "xls"])
with col2:
    codigo_unidade = st.selectbox("🏫 Unidade Escolar", ["Selecione..."] + UNIDADES).split('-')[0]

# Estado inicial (session_state)
for key, value in {
    "usuarios_com_erro": [],
    "usuarios_sem_telefone": [],
    "cont_sucesso": 0,
    "cont_erro": 0,
    "cont_sem_telefone": 0,
    "contatos_por_tipo": {'P':0,'M':0,'RL':0,'RF':0}
}.items():
    if key not in st.session_state:
        st.session_state[key] = value


def limpar_log():
    st.session_state.usuarios_com_erro = []
    st.session_state.usuarios_sem_telefone = []
    st.session_state.cont_sucesso = 0
    st.session_state.cont_erro = 0
    st.session_state.cont_sem_telefone = 0
    st.session_state.contatos_por_tipo = {'P':0,'M':0,'RL':0,'RF':0}


# =====================================
# 🧾 Função para exibir log na tela
# =====================================
def exibir_resumo_e_log():
    if st.session_state.cont_sucesso == 0 and st.session_state.cont_erro == 0 and all(v == 0 for v in st.session_state.contatos_por_tipo.values()):
        return

    st.markdown(f"""
    <div class="card" style="margin-top:1rem; margin-bottom:0.6rem;">
        <div style="display:flex; flex-direction:column; gap:6px; text-align:center;">
            <div style="font-weight:700; font-size:16px;">📊 Resultado do Processamento</div>
            <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap; text-align:center;">
                <div style="background:#e6fff0; padding:10px 12px; border-radius:8px; min-width:220px;">
                    <div style="font-size:14px; color:#16a34a; font-weight:700;">✅ Usuários válidos </div>
                    <div style="font-size:18px; font-weight:700;">{st.session_state.cont_sucesso}</div>
                </div>
                <div style="background:#fff6e1; padding:10px 12px; border-radius:8px; min-width:220px;">
                    <div style="font-size:14px; color:#ffb000; font-weight:700;">⚠️ Usuários sem telefone cadastrado </div>
                    <div style="font-size:18px; font-weight:700;">{st.session_state.cont_sem_telefone}</div>
                </div>
                <div style="background:#fff3f3; padding:10px 12px; border-radius:8px; min-width:220px;">
                    <div style="font-size:14px; color:#dc2626; font-weight:700;">🔴 Usuários com erro </div>
                    <div style="font-size:18px; font-weight:700;">{st.session_state.cont_erro}</div>
                </div>  
            </div>
            <div style="margin-top:6px; font-size:14px; color:#374151; text-align:center;">
                👨 Pais: {st.session_state.contatos_por_tipo.get('P',0)} &nbsp; | &nbsp;
                👩 Mães: {st.session_state.contatos_por_tipo.get('M',0)} &nbsp; | &nbsp;
                👤 RL: {st.session_state.contatos_por_tipo.get('RL',0)} &nbsp; | &nbsp;
                💰 RF: {st.session_state.contatos_por_tipo.get('RF',0)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bloco da lista de erros
    if st.session_state.usuarios_com_erro or st.session_state.usuarios_sem_telefone:
        st.markdown("""
            <div class="card" style="margin-top:0.6rem; padding:0.4rem;">
                <div style="font-weight:700; margin-bottom:6px;">🧾 Lista de erros</div>
        """, unsafe_allow_html=True)

        rows = []
        for e in st.session_state.usuarios_com_erro:
            usuario = e.get('usuario','')
            motivo = e.get('motivo','')
            rows.append(f"<div style='display:flex; gap:12px; padding:8px 10px; border-bottom:1px solid #f3f4f6;'><div style='flex:1; font-weight:600;'>{usuario}</div><div style='flex:2; color:#6b7280;'>{motivo}</div></div>")

        for e in st.session_state.usuarios_sem_telefone:
            usuario = e.get('usuario','')
            motivo = e.get('motivo','')
            rows.append(f"<div style='display:flex; gap:12px; padding:8px 10px; border-bottom:1px solid #f3f4f6;'><div style='flex:1; font-weight:600;'>{usuario}</div><div style='flex:2; color:#6b7280;'>{motivo}</div></div>")

        st.markdown("<div style='border:1px solid #eef2f6; border-radius:8px; background:#ffffff; padding:4px; height:260px; overflow:auto;'>" + ''.join(rows) + "</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        col_log = st.columns([1,1])
        with col_log[0]:
            if st.button("🧹 Limpar log"):
                limpar_log()
        with col_log[1]:
            if st.session_state.usuarios_com_erro or st.session_state.usuarios_sem_telefone:
                erro_buffer, nome_erro = gerar_xlsx_erros(
                    st.session_state.usuarios_com_erro,
                    st.session_state.usuarios_sem_telefone,
                    codigo_unidade
                )
                st.download_button(
                    label="🧾 Baixar Relatório de Erros",
                    data=erro_buffer,
                    file_name=nome_erro,
                    mime="text/csv",
                    use_container_width=True
                )


# =====================================
# ⚡ Fluxo principal
# =====================================
if uploaded_file and codigo_unidade != "Selecione...":
    if st.button("🚀 Processar arquivo", use_container_width=True):
        try:
            with st.spinner("⏳ Processando contatos..."):
                contatos_df, contagem_tipos, usuarios_erro, total_sucesso, total_erros, usuarios_sem_telefone, total_sem_telefone = processar_planilha(uploaded_file, codigo_unidade)

            st.session_state.contatos_por_tipo = contagem_tipos
            st.session_state.usuarios_com_erro = usuarios_erro
            st.session_state.usuarios_sem_telefone = usuarios_sem_telefone
            st.session_state.cont_sucesso = total_sucesso
            st.session_state.cont_erro = total_erros
            st.session_state.cont_sem_telefone = total_sem_telefone

            buffer, nome_arquivo = gerar_csv_download(contatos_df, codigo_unidade)
            st.success("✅ Arquivo gerado com sucesso!")
            st.download_button(
                label="📥 Baixar CSV de Contatos",
                data=buffer,
                file_name=nome_arquivo,
                mime="text/csv",
                use_container_width=True
            )

            exibir_resumo_e_log()
            st.dataframe(contatos_df, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {e}")
            st.exception(e)

elif uploaded_file and codigo_unidade == "Selecione...":
    st.info("🏫 Selecione uma unidade escolar para habilitar o processamento.")
else:
    st.info("⬆️ Envie um arquivo e selecione a unidade para começar.")

st.markdown(f"""
<div style='text-align: center; color: gray; font-size: 13px; margin-top: 2rem;'>
    Desenvolvido por <b>Ricardo Alves de Souza</b> · {datetime.now().year}<br>
    <span style='font-size: 12px;'>Extractor de Contatos - Versão 2.0</span>
</div>
""", unsafe_allow_html=True)
