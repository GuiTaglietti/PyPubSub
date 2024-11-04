# Projeto de Comunicação entre Cliente e Servidor com Sockets e Threads (PubSub)

Este projeto implementa uma comunicação entre clientes e servidores utilizando sockets TCP e UDP em Python. Os clientes se inscrevem em tópicos de interesse e recebem mensagens distribuídas pelo servidor conforme a categoria selecionada.

## Estrutura do Projeto

O projeto está dividido em três principais componentes:
- **Consumer**: Representa o cliente que se conecta ao servidor TCP e recebe mensagens conforme sua inscrição em categorias.
- **Distributor**: Representa o servidor que gerencia as conexões dos clientes e distribui as mensagens conforme os tópicos de interesse.
- **Generator**: Gera e envia dados aleatórios para o servidor através de UDP, que então distribui essas informações para os clientes inscritos.

### Arquivos do Projeto

- `Info.py`: Classe `Info` que encapsula os dados de uma mensagem.
- `Consumer.py`: Código do cliente que recebe mensagens do servidor.
- `Distributor.py`: Código do servidor que distribui mensagens para os clientes.
- `Generator.py`: Código que gera e envia mensagens para o servidor.

## Pré-requisitos

Para rodar este projeto, você precisa de:

- Python 3.7 ou superior

## Como Rodar o Projeto

### Passo 1: Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd `NOME_DO_DIRETORIO>
```

### Passo 2: Inicie o servidor de distribuição
O servidor de distribuição gerencia as conexões dos clientes e recebe os dados dos geradores. Em um terminal, execute:

```bash
python3 Distributor.py
```

### Passo 3: Inicie o gerador de dados
O gerador cria mensagens aleatórias e envia para o servidor. Abra outro terminal e execute:

```bash
python3 Generator.py
```

### Passo 4: Inicie o cliente consumidor
O cliente consumidor se conecta ao servidor e recebe mensagens das categorias selecionadas. Abra outro terminal e execute:

```bash
python3 Consumer.py
```

Ao iniciar, você poderá se inscrever em uma ou mais categorias (digite os números separados por espaço).

## Exemplo de Uso

Este exemplo demonstra como utilizar o projeto completo:

1. Inicie o `Distributor.py` para configurar o servidor de distribuição.
2. Em um segundo terminal, execute o `Generator.py` e defina o número de geradores que você deseja criar.
3. Em um terceiro terminal, inicie o `Consumer.py`. Inscreva-se nas categorias desejadas digitando os números correspondentes, separados por espaço.
4. Observe as mensagens recebidas no terminal do consumidor, que correspondem às categorias nas quais ele está inscrito.

Dessa forma, cada componente desempenha seu papel na comunicação e na distribuição de dados entre geradores e consumidores.

## Observação

- Para encerrar qualquer processo, pressione Enter no respectivo terminal.
- As mensagens serão distribuídas para os clientes inscritos nas categorias, de acordo com os dados gerados aleatoriamente.

## Estrutura de Código

Cada arquivo possui uma função específica dentro do projeto:

- **Info.py**: Define a classe `Info`, que encapsula os dados de uma mensagem. Os atributos `sequence`, `category`, e `value` representam cada mensagem enviada e recebida entre os geradores e consumidores.

- **Consumer.py**: Cria um cliente TCP, permitindo ao usuário inscrever-se em categorias de interesse e exibindo as mensagens recebidas do servidor.

- **Distributor.py**: Gerencia as conexões TCP dos clientes, organiza as filas de categorias e distribui as mensagens, recebidas via UDP dos geradores, para os clientes inscritos em cada categoria.

- **Generator.py**: Gera mensagens aleatórias associadas a diferentes categorias e as envia ao servidor através de UDP, para serem distribuídas conforme os interesses dos consumidores.

## Créditos

Este projeto foi desenvolvido por:

- Guilherme M. Taglietti (@GuiTaglietti)
- José P. R. Pereira (@JosePRP1)