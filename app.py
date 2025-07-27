import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# --- Configurações Iniciais ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD") # Carrega a senha do .env

if not GEMINI_API_KEY:
    st.error("Chave da API do Gemini não encontrada. Por favor, crie um arquivo .env na raiz do projeto com GEMINI_API_KEY='SUA_CHAVE_AQUI'.")
    st.stop()

if not APP_PASSWORD:
    st.error("Senha do aplicativo não configurada. Por favor, adicione APP_PASSWORD='sua_senha_segura_aqui' ao seu arquivo .env.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-1.5-flash"
TOOLS_FILE = "tools.json"

# Inicializa o estado da sessão para a busca e autenticação
if 'search_query_submitted' not in st.session_state:
    st.session_state.search_query_submitted = ""
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False # Define o estado inicial de autenticação como Falso

def update_search_query():
    """Função para atualizar a query de busca quando o Enter for pressionado."""
    st.session_state.search_query_submitted = st.session_state.search_input_widget

def check_password():
    """Verifica a senha digitada pelo usuário."""
    if st.session_state.password_input == APP_PASSWORD:
        st.session_state.authenticated = True
        st.success("Autenticação bem-sucedida!")
    else:
        st.session_state.authenticated = False
        st.error("Senha incorreta. Você terá acesso somente de leitura.")

# --- Funções Auxiliares (mantidas as mesmas) ---

def load_tools():
    """Carrega as ferramentas salvas do arquivo JSON."""
    if os.path.exists(TOOLS_FILE):
        with open(TOOLS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_tools(tools):
    """Salva as ferramentas no arquivo JSON."""
    with open(TOOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(tools, f, indent=4, ensure_ascii=False)

def process_tool_with_gemini(tool_text):
    """
    Envia o texto da ferramenta para a API do Gemini para categorização,
    formatação de título, descrição resumida, um emoji e, se possível, um link.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"""
        Você é um assistente especializado em ferramentas da web.
        Dada a seguinte descrição de uma ferramenta da web, por favor:
        1. Sugira um título conciso e claro.
        2. Sugira um emoji relevante para a ferramenta.
        3. Categorize a ferramenta (Ex: Desenvolvimento, Design, Produtividade, Marketing, Segurança, etc. Escolha a mais relevante).
        4. Forneça uma descrição resumida da sua principal função em uma ou duas frases.
        5. Tente encontrar o URL oficial da ferramenta na web. A URL deve ser a URL bruta, sem nenhum texto adicional ou formatação, apenas o link. Se não encontrar, retorne uma string vazia para a URL.
        6. O formato de saída deve ser um JSON válido com as chaves "titulo", "emoji", "categoria", "descricao" e "url".

        Exemplo de entrada: "uma ferramenta online para criar protótipos de interface de usuário chamada Figma"
        Example output: {{"titulo": "Figma", "emoji": "🎨", "categoria": "Design", "descricao": "Cria protótipos e designs de interface de usuário de forma colaborativa na nuvem.", "url": "https://www.figma.com/"}}

        Exemplo de entrada: "Uma ferramenta para gerenciar tarefas e projetos."
        Exemplo de saída: {{"titulo": "Gerenciador de Tarefas", "emoji": "✅", "categoria": "Produtividade", "descricao": "Ajuda a organizar tarefas diárias e projetos complexos.", "url": ""}}

        Now, process the following tool:
        "{tool_text}"
        """
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith("```json") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()
        
        data = json.loads(response_text)
        if "emoji" not in data or not isinstance(data["emoji"], str):
            data["emoji"] = "💡"
        if "url" not in data or not isinstance(data["url"], str):
            data["url"] = ""
        if data["url"] and not (data["url"].startswith("http://") or data["url"].startswith("https://")):
            data["url"] = ""
            
        return data
    except Exception as e:
        st.error(f"Erro ao processar com Gemini: {e}. Verifique o formato da resposta da API.")
        return None

# --- Interface Streamlit ---

st.set_page_config(layout="centered", page_title="Minhas Ferramentas Web", page_icon="🧰")
st.title("🧰 Minhas Ferramentas da Web")
st.write("Anote e organize suas descobertas de ferramentas online!")

# Carrega as ferramentas existentes
tools = load_tools()

# --- Seção de Autenticação ---
if not st.session_state.authenticated:
    st.subheader("🔒 Autenticação Necessária")
    st.text_input("Digite a senha para acesso total:", type="password", on_change=check_password, key="password_input")
    st.info("Sem a senha, você terá acesso somente de leitura às ferramentas.")
    st.markdown("---") # Separador para organizar visualmente

# Formulário para adicionar nova ferramenta (somente se autenticado)
if st.session_state.authenticated:
    st.subheader("➕ Adicionar Nova Ferramenta")
    with st.form("new_tool_form", clear_on_submit=True):
        tool_input = st.text_area("✍️ Descreva a ferramenta (ex: 'Uma ferramenta para desenhar diagramas UML online'):", height=100, key="new_tool_text_area")
        submitted = st.form_submit_button("Analisar e Adicionar")

        if submitted and tool_input:
            with st.spinner("Processando com a inteligência do Gemini..."):
                processed_data = process_tool_with_gemini(tool_input)
                if processed_data:
                    processed_data["original_text"] = tool_input
                    tools.append(processed_data)
                    save_tools(tools)
                    st.success("Ferramenta adicionada com sucesso!")
                    st.rerun()
                else:
                    st.error("Não foi possível processar a ferramenta. Tente novamente.")
        elif submitted and not tool_input:
            st.warning("Por favor, digite a descrição da ferramenta.")
    st.markdown("---")

# Exibir ferramentas salvas
st.subheader("Ferramentas Anotadas")

if not tools:
    st.info("Nenhuma ferramenta anotada ainda. Use o formulário acima para adicionar uma (se autenticado)!")
else:
    # Opções de filtragem e busca usando colunas
    col1, col2 = st.columns([2, 1])

    with col1:
        search_input = st.text_input(
            "Buscar por título, descrição ou texto original:",
            value=st.session_state.search_query_submitted,
            key="search_input_widget",
            on_change=update_search_query,
            help="Pressione Enter para filtrar os resultados."
        )
        search_query = st.session_state.search_query_submitted

    with col2:
        categories = sorted(list(set([tool.get("categoria", "Outros") for tool in tools])))
        selected_category = st.selectbox("Filtrar por Categoria:", ["Todas"] + categories, help="Selecione uma categoria para filtrar.")

    filtered_tools = tools
    
    if selected_category != "Todas":
        filtered_tools = [tool for tool in filtered_tools if tool.get("categoria") == selected_category]

    if search_query:
        search_query = search_query.lower()
        filtered_tools = [
            tool for tool in filtered_tools 
            if search_query in tool.get("titulo", "").lower() or 
               search_query in tool.get("descricao", "").lower() or
               search_query in tool.get("original_text", "").lower()
        ]

    if not filtered_tools:
        st.info("Nenhuma ferramenta encontrada com os critérios de busca/filtro.")
    else:
        filtered_tools.sort(key=lambda x: x.get("titulo", "").lower())
        
        for i, tool in enumerate(filtered_tools):
            emoji = tool.get('emoji', '💡')
            with st.expander(f"{emoji} **{tool.get('titulo', 'Título não disponível')}** - *{tool.get('categoria', 'Sem Categoria')}*"):
                st.write(f"**Descrição:** {tool.get('descricao', 'Nenhuma descrição.')}")
                
                tool_url = tool.get('url')
                if tool_url:
                    st.markdown(f"**Link:** [{tool_url}]({tool_url})", unsafe_allow_html=True)
                else:
                    st.info("Link não disponível ou não encontrado pelo Gemini.")
                
                st.write(f"**Texto Original:** {tool.get('original_text', 'Não disponível.')}")
                
                # Botão de excluir (somente se autenticado)
                if st.session_state.authenticated:
                    delete_col, _ = st.columns([0.1, 0.9])
                    with delete_col:
                        if st.button("🗑️", key=f"delete_button_{i}", help="Excluir esta ferramenta"):
                            tools.remove(tool)
                            save_tools(tools)
                            st.success("Ferramenta excluída!")
                            st.rerun()
                else:
                    # Opcional: mostrar um aviso de que não pode excluir sem autenticação
                    st.caption("Faça login para excluir itens.")