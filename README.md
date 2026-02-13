# Yahoo Finance Equity Crawler

Projeto desenvolvido em Python para coletar dados do Yahoo Finance utilizando Selenium, BeautifulSoup e Programação Orientada a Objetos. O crawler acessa o screener de equities do Yahoo Finance, aplica filtro por região e exporta os dados coletados para um arquivo CSV.

----------------------------------------
FUNCIONALIDADES
----------------------------------------

- Coleta Symbol, Name e Price (Intraday)
- Permite filtrar ativos por região
- Exporta os dados para arquivo CSV
- Estrutura modular e orientada a objetos
- Possui testes unitários para validação do parser
- Separação clara entre crawler e parser para facilitar manutenção e testes

----------------------------------------
TECNOLOGIAS UTILIZADAS
----------------------------------------

- Python 3.8+
- Selenium
- BeautifulSoup4
- Pandas
- Unittest (biblioteca nativa do Python)

----------------------------------------
FONTE DOS DADOS
----------------------------------------

https://finance.yahoo.com/research-hub/screener/equity/

----------------------------------------
ESTRUTURA DO PROJETO
----------------------------------------

yahoo_crawler/

    crawler/
        __init__.py
        yahoo_crawler.py
        parser.py

    tests/
        __init__.py
        test_parser.py

    crawler.py
    sample.html
    requirements.txt
    README.md
    output.csv (gerado após execução)
    venv/

----------------------------------------
PRÉ-REQUISITOS
----------------------------------------

- Python 3.8 ou superior
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome

----------------------------------------
INSTALAÇÃO DO PROJETO
----------------------------------------

1 - Clonar ou baixar o repositório

git clone <URL_DO_REPOSITORIO>
cd yahoo_crawler

----------------------------------------

2 - Criar ambiente virtual

python -m venv venv

----------------------------------------

3 - Ativar ambiente virtual

Windows CMD:
venv\Scripts\activate

Windows PowerShell:
venv\Scripts\Activate.ps1

Linux ou Mac:
source venv/bin/activate

----------------------------------------

4 - Instalar dependências

pip install -r requirements.txt

----------------------------------------

5 - Instalar ChromeDriver

Verifique a versão do Chrome acessando:
chrome://settings/help

Baixe a versão correspondente do ChromeDriver em:
https://chromedriver.chromium.org/downloads

Coloque o executável do ChromeDriver na pasta do projeto ou configure no PATH do sistema.

----------------------------------------
EXECUTANDO O PROJETO
----------------------------------------

python crawler.py

O programa solicitará a região desejada.

Exemplo:
Digite a região:
Argentina

----------------------------------------
SAÍDA DO PROJETO
----------------------------------------

Será gerado o arquivo output.csv contendo:

symbol,name,price

Exemplo:

AMX.BA,América Móvil, S.A.B. de C.V.,2089.00
NOKA.BA,Nokia Corporation,557.50

----------------------------------------
COMO O SISTEMA FUNCIONA
----------------------------------------

1 - Selenium acessa o site e aplica o filtro de região
2 - O HTML renderizado é capturado
3 - BeautifulSoup faz o parsing dos dados
4 - Pandas gera o arquivo CSV
5 - Parser é testado isoladamente com testes unitários

----------------------------------------
EXECUTANDO OS TESTES UNITÁRIOS
----------------------------------------

Com o ambiente virtual ativado, execute:

python -m unittest discover tests

Saída esperada:

Ran 3 tests
OK

----------------------------------------
OBSERVAÇÕES
----------------------------------------

O Yahoo Finance pode alterar a estrutura da página a qualquer momento. Caso isso ocorra, pode ser necessário atualizar os seletores do crawler ou ajustes no parser.

----------------------------------------
POSSÍVEIS MELHORIAS FUTURAS
----------------------------------------

- Paginação automática
- Execução headless
- Sistema de logs estruturado
- Exportação para banco de dados
- Parâmetros via linha de comando
- Dockerização do projeto
- Integração contínua com pipeline CI/CD
- Testes automatizados com Pytest
- Métricas de cobertura de testes

----------------------------------------
AUTOR
----------------------------------------

Projeto desenvolvido para fins educacionais e avaliação técnica.