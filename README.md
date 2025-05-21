📨 Validador de E-mails com Threads
Este projeto é um robô de validação de e-mails a partir de um arquivo CSV de entrada, utilizando múltiplas threads para acelerar o processo. A validação é feita via API externa (https://api.mails.so/), e os resultados são salvos em um novo arquivo CSV.

📌 Funcionalidades
Lê dados de CPF e e-mail de um arquivo CSV.

Verifica quais CPFs ainda não foram processados.

Divide os dados em várias threads para melhorar a performance.

Realiza requisições à API da Mails.so para validação de e-mails.

Armazena os resultados em um arquivo de saída CSV.

🛠️ Tecnologias Utilizadas
Python 3

requests

csv, io, json

threading

API pública Mails.so

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

WhatsApp Verifier Bot
Este é um robô automatizado que utiliza o Selenium para verificar se números de telefone estão ativos no WhatsApp Web. Ele lê uma lista de contatos de um arquivo CSV e registra os resultados (número válido, inválido ou fixo) em outro arquivo de saída.
⚙️ Pré-requisitos
Python 3.8+

Google Chrome instalado

ChromeDriver compatível com sua versão do Chrome

Dependências Python:
pip install selenium
