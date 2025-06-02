# 🧾 Sistema Especialista - Chatterbot desenvolvido com Python e Flask e NLP (Processamento de Linguagem Natural) com nltk

Este chatterbot é capaz de reponder perguntas sobre a CIPA (Comissão Interna de Prevenção de Acidentes). Por Exemplo: "O que é a CIPA?", "Quando ocorrem as reuniões da CIPA", "Como fazer parte da CIPA" e etc...

Além de responder perguntas, o robô fornece atas das últimas reuniões, por meio de pesquisas. Para tal, é realizado um processamento das últimas atas, aplicado a tokenização e remoção de palavras de parada (stopwords) para extração de palavras-chave.

Este projeto foi desenvolvido com base no projeto "Bibliotecário" elaborado pelo **Professor Dr. Luis Paulo da Silva Carvalho**, disponível [aqui](https://gitlab.com/luiscarvalho1/sistemas_especialistas/-/blob/main/2025/bibliotecario-parcial.zip).

---

## 🚀 Tecnologias Utilizadas

- 🐍 **Python**
- 🌐 **Flask**
- 🔌 **REST APIs**

## 📚 Bibliotecas
- 🤖 **Chatterbot**
- 🔤 **Nltk**
- **Chatterbot-corpus**

---

## 🛠️ Passos para preparação do ambiente

1. Clone este repositório e acesse a pasta do projeto:
```bash
git clone https://github.com/marcoantoniossilva/chatterbot-cipa-python-nltk-flask.git 
cd chatterbot-cipa-python-nltk-flask
```

2. Crie um ambiente virtual com o comando:
```bash
python3 -m venv venv
```
3. Ative o ambiente virtual:

- No Linux/Mac:
    ```bash
    source venv/bin/activate
    ```

- No Windows (cmd):
    ```cmd
    venv\Scripts\activate
    ```

- No Windows (PowerShell):
    ```ps1
    venv\Scripts\Activate.ps1
    ```

4. Instale as dependências com:

```bash
pip3 install -r requirements.txt
```

5. Instale as dependências da nltk rodando o script [init_nltk.py](init_nltk.py):

```bash
python3 init_nltk.py
```

---

## ⚙️ Passos para treinamento do bot

1. Execute o script de treinamento do robô:

```bash
python3 train.py
```

2. Execute o script de extração de palavras-chave:

```bash
python3 process_meeting_reports.py
```

---

## ⚙️ Passos para execução do bot

1. Execute o script do serviço do bot (back-end):

```bash
python3 bot_service.py
```

2. Execute o script do serviço do chat (front-end)

```bash
python3 chat/chat.py
```

---

## Conversando com o bot

1. Abra o link do bot no navegador:
> http://localhost:5001/

Faça perguntas na caixa de mensagem e clique em "Enviar", ou ative a busca por atas clicando no botão "🔍".

Ao pesquisar e encontrar uma ata, a mesma pode sr baixada clicando no seu nome, ou o nome dos membros presentes pode ser consultado clicando no botão "👬👭".

## 🔁 Rotas (back-end)

**GET** "localhost:5000/"  
> Informações sobre o serviço

**GET** "localhost:5000/alive"  
> Informações sobre o estado do bot

**POST** "localhost:5000/answer"  
> Envia uma pergunta ao bot no seguinte formato JSON:
```json
{
    "question" : "como reportar um acidente de trabalho?"
}
```

**POST** "localhost:5000/meeting_reports"  
> Pesquisa por atas de reuniões da CIPA no seguinte formato JSON:
```json
{
	"key1" : "acidente",
	"key2" : "cipa",
	"key3" : "risco",
	"key4" : "brigada",
	"key5" : "treinamento"
}
```

---
## 🎥 Vídeo de demonstração

Youtube: https://youtu.be/l-6IofWCfxY

---
## 👨‍💻 Autor

**Marco Antonio S. Silva**  
[LinkedIn](https://www.linkedin.com/in/marcosilva95) • [GitHub](https://github.com/marcoantoniossilva) • [YouTube](https://www.youtube.com/@MarcoAntonioSSilvaDev)
