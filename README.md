# 📞 Extractor de Contatos - 7Edu

O **Extractor de Contatos - 7Edu** é uma ferramenta de processamento de dados desenvolvida em **Python** e **Streamlit**.  
Sua finalidade é automatizar a **ingestão, limpeza e padronização** de listas de contatos de responsáveis extraídas de planilhas do sistema **7Edu**, gerando um arquivo **CSV** limpo e pronto para integração com plataformas de comunicação (ex: CRMs, sistemas de disparo de mensagens).

A aplicação garante a conformidade dos dados de telefone, inserindo o **DDI (+55)** e provendo uma **identificação granular** de cada responsável.

---

## ✨ Recursos Chave

| Recurso | Descrição |
|----------|------------|
| **Padrão de Telefone** | Limpeza automatizada de números de telefone, remoção de caracteres não numéricos e padronização com o prefixo internacional **+55 (DDI Brasil)**. |
| **Identificação Detalhada** | Geração de uma string de identificação completa que inclui **Turma, Unidade, Nome do Responsável, Tipos de Responsabilidade** (Pai, Mãe, RL, RF) e **Nome do Aluno**. |
| **Validação de Entrada** | Verificação obrigatória das colunas de origem do arquivo Excel para evitar falhas no processamento. |
| **Gestão de Duplicatas** | Utiliza o **Pandas** para remover contatos duplicados (baseados em nome e telefone) antes da exportação. |
| **Interface Web** | Utiliza o **Streamlit** para fornecer uma interface gráfica intuitiva e acessível para o upload e download de arquivos. |

---

## 📑 Uso da Aplicação

### 1. Colunas de Entrada (Requisito)

O arquivo Excel de origem deve conter as seguintes colunas **com a grafia exata** para que o processamento seja bem-sucedido:

Nome Completo
Turma
Identificador Estudante
Pai
Telefone do Pai
Mãe
Telefone da Mãe
Responsável Legal
Telefone do Responsável Legal
Responsável Financeiro
Série

---

### 2. Fluxo de Trabalho

1. Faça o **Upload** do arquivo Excel (`.xlsx` ou `.xls`) na interface.  
2. Insira o **Código da Unidade Escolar**.  
3. Clique em **🚀 Processar arquivo** e acompanhe o log de status.  
4. Baixe o **arquivo CSV final**, nomeado com o código da unidade e a data/hora do processamento.

---

## 📂 Estrutura do Projeto

O código é organizado em módulos Python com responsabilidades bem definidas:

| Arquivo | Responsabilidade |
|----------|------------------|
| **main.py** | Ponto de entrada da aplicação. Gerencia o layout principal, a configuração de página e a orquestração do fluxo de trabalho (upload → processamento → download). |
| **processamento.py** | Contém a lógica de negócios: validação do dataset, iteração linha a linha para extração, limpeza e formatação de contatos, e gestão de buffers para download CSV. |
| **utils.py** | Módulo de funções auxiliares (*helpers*) para tratamento de strings, limpeza de telefones e determinação dos tipos de responsáveis. |
| **ui.py** | Responsável pela customização da interface **Streamlit**, aplicando estilos CSS customizados e definindo o conteúdo do menu lateral (*sidebar*). |

---

## 🧩 Exportar para as Planilhas

Desenvolvido por **Ricardo Alves de Souza**  
**Versão 1.0 - [2025]*