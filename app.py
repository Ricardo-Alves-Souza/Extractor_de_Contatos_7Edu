import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Analisador de Excel para CSV", layout="wide")
st.title("📊 Ferramenta de Análise de Base de Dados")
st.write("Faça o upload do seu arquivo Excel (.xlsx) para realizar a análise e baixar o resultado em CSV.")

# 1. Widget de Upload de Arquivo
uploaded_file = st.file_uploader("Selecione o arquivo Excel", type=['xlsx'])

if uploaded_file is not None:
    # Lendo o arquivo para um DataFrame do Pandas
    try:
        # Usar st.cache_data garante que o Streamlit não recarregue o arquivo 
        # e não refaça a análise desnecessariamente se o usuário interagir com a página.
        @st.cache_data
        def load_data(file):
            return pd.read_excel(file)

        df = load_data(uploaded_file)
        st.success(f"Arquivo carregado com sucesso! Total de {len(df)} linhas.")
        
        # 2. Análise Simples em Pandas
        
        # EXEMPLO DE ANÁLISE: Contagem de valores únicos na primeira coluna
        coluna_para_analise = st.selectbox(
            "Escolha a coluna para análise:", 
            options=df.columns
        )
        
        # Certifica-se de que a coluna foi selecionada e não está vazia
        if coluna_para_analise and not df.empty:
            st.subheader(f"Contagem de Ocorrências por '{coluna_para_analise}'")
            
            # Executa o value_counts
            resultado_analise = df[coluna_para_analise].value_counts().reset_index()
            resultado_analise.columns = [coluna_para_analise, 'Contagem']
            
            st.dataframe(resultado_analise)

            # 3. Preparando o Download do CSV
            
            # Função para converter o DataFrame para string CSV
            @st.cache_data
            def convert_df_to_csv(df_to_convert):
                return df_to_convert.to_csv(index=False).encode('utf-8')

            csv_data = convert_df_to_csv(resultado_analise)
            
            st.download_button(
                label="📥 Baixar Resultado da Análise em CSV",
                data=csv_data,
                file_name=f'analise_{coluna_para_analise}.csv',
                mime='text/csv',
            )
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")
        st.warning("Verifique se o arquivo está no formato .xlsx e se as colunas estão corretas.")