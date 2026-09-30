# O Contexto do Alienista

## Download

Baixe o arquivo `.zip` disponibilizado na Release do projeto no GitHub e extraia seu conteúdo em uma pasta de sua preferência.

## Configuração do ambiente

Abra um terminal dentro da pasta do projeto e crie um ambiente virtual Python:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No Windows utilizando PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

No Windows utilizando CMD:

```cmd
.venv\Scripts\activate.bat
```

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

## Execução

O projeto utiliza uma arquitetura cliente-servidor. Para testar o jogo, é necessário executar o servidor e o cliente em **dois terminais diferentes**.

### 1. Iniciar o servidor

No primeiro terminal, execute:

```bash
python servidor.py
```

Mantenha esse terminal aberto durante a execução do jogo.

### 2. Iniciar a interface

Abra um segundo terminal na pasta do projeto, ative o mesmo ambiente virtual e execute:

```bash
python interface_main.py
```

A interface gráfica será iniciada e o cliente realizará a comunicação com o servidor por meio de XML-RPC.

Para utilizar o jogo, os dois processos devem permanecer em execução simultaneamente.
