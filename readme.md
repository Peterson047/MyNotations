# 🧰 Meu Gerenciador de Ferramentas Web

Um sistema simples e inteligente para anotar, categorizar e organizar ferramentas da web que você encontra por aí. Utilize o poder da IA do Google Gemini para categorizar, resumir e até mesmo encontrar links para suas ferramentas automaticamente\!

-----

## 🚀 Funcionalidades

  * **Anotação Inteligente**: Descreva uma ferramenta e o Google Gemini irá automaticamente:
      * Sugerir um **título** conciso.
      * Atribuir um **emoji** relevante.
      * **Categorizar** a ferramenta (Ex: Desenvolvimento, Design, Produtividade, Marketing, Segurança).
      * Fornecer uma **descrição resumida** de sua função.
      * Tentar encontrar o **URL oficial** da ferramenta.
  * **Autenticação Simples**: Um campo de senha inicial controla o acesso. Sem a senha, o usuário tem acesso apenas de leitura; com a senha, pode adicionar e excluir ferramentas.
  * **Busca e Filtro**: Encontre facilmente suas ferramentas por título, descrição ou texto original, e filtre por categoria. A busca exige `Enter` para filtrar os resultados.
  * **Persistência de Dados**: Todas as ferramentas são salvas em um arquivo JSON (`tools.json`) na raiz do projeto.
  * **Interface Intuitiva**: Desenvolvido com Streamlit para uma experiência de usuário simples e eficaz.
  * **Gestão Segura de Chaves**: Utiliza variáveis de ambiente (`.env`) para gerenciar sua chave da API do Gemini e a senha do aplicativo.

-----

## ⚙️ Como Configurar e Executar

Siga os passos abaixo para colocar o projeto em funcionamento na sua máquina.

### Pré-requisitos

  * Python 3.9+
  * Uma chave da API do Google Gemini. Obtenha a sua em [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1\. Clone o Repositório (ou crie a estrutura)

Se você estiver usando Git:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd meu-gerenciador-ferramentas-web # Ou o nome da sua pasta
```

Caso contrário, crie a seguinte estrutura de pastas e arquivos:

```
meu-gerenciador-ferramentas-web/
├── app.py
├── .env
└── tools.json
```

### 2\. Configure as Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do seu projeto (na mesma pasta de `app.py`) e adicione suas chaves:

```
# .env
GEMINI_API_KEY="SUA_CHAVE_DA_API_GEMINI_AQUI"
APP_PASSWORD="SUA_SENHA_SEGURA_AQUI"
```

**Importante**: Nunca compartilhe seu arquivo `.env` publicamente. Se estiver usando Git, adicione `.env` ao seu arquivo `.gitignore`.

### 3\. Instale as Dependências

Abra seu terminal na pasta raiz do projeto e execute:

```bash
pip install streamlit google-generativeai python-dotenv
```

### 4\. Inicialize o Arquivo de Dados

Certifique-se de que o arquivo `tools.json` exista e esteja inicializado como uma lista JSON vazia `[]`. Se ele não existir, ou se estiver vazio/corrompido, crie-o ou edite-o para que contenha apenas:

```json
[]
```

### 5\. Execute o Aplicativo

No terminal, na pasta raiz do projeto, execute o Streamlit:

```bash
streamlit run app.py
```

O aplicativo será aberto no seu navegador padrão (geralmente `http://localhost:8501`).

-----

## 🤝 Contribuição

Sinta-se à vontade para sugerir melhorias, reportar bugs ou contribuir com o código.

-----

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

-----

-----
