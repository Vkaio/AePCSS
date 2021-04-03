# App flask basic

## Projeto
Dependências:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [MySQL](https://www.mysql.com/)
- [Bootstrap](https://getbootstrap.com/)


## Ambiente de desenvolvimento

Abaixo está descrito como instalar e configurar as dependencias de desenvolvimento para cada um dos SOs, caso haja alguma dúvida, recomendo ver o [tutorial](https://code.visualstudio.com/docs/remote/containers) na página do Visual Studio Code.

### Windows

Dependências:
- [Docker Desktop](https://www.docker.com/)
- [WSL back-end 2](https://aka.ms/vscode-remote/containers/docker-wsl2)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

Baixe e instale o [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows) para Windows e o [Visual Studio Code](https://code.visualstudio.com/download). Siga as instruções de instalação do [WSL back-end 2](https://docs.microsoft.com/pt-br/windows/wsl/install-win10#manual-installation-steps) da etapa 1 a 5,  após isso, abra o Visual Studio Code e vá na aba de extensõens do Code ou pressione `Ctrl+Shift+X` e procure por "Remote Development" e instale a extensão. Instale o [git](https://git-scm.com/download/win), logo após clone esse repositório e abra a pasta no Visual Studio Code, pressione `Ctrl+Shift+P` e digite "reopen in container" e confirme. Dentro de alguns minutos o ambiente de desenvolvimento será configurado.

Obs: O Docker Desktop só pode ser instalado no Windows 10, infelizmente =(.

### Linux

Dependências:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

Se você está utilizando Ubuntu, Debian ou alguma distribuição baseada em alguma dessas duas basta executar o comando abaixo:

```shell
sudo apt-get install --no-install-recommends docker.io docker-compose git
```

Será necessário adicionar seu usuário ao grupo do Docker, para isso basta executar o comando abaixo.

```shell
sudo usermod -aG docker $USER
```

Após isso faça logout ou reinicie seu computador.

Para instalar o Visual Studio Code baixe e o pacote `.deb` no [site oficial](https://code.visualstudio.com/). Algumas distros contam com utilitarios para instalar pacotes `.deb`, precisando apenas dois cliques no arquivo `.deb` e digitar a senha de usuário. Se sua distro não contar com um desses utilitários abra um terminal na pasta onde o pacote foi baixado e digite os comandos abaixo.

```shel
sudo dpkg -i code*.deb
sudo apt install --fix-broken
```

Após isso, abra o Visual Studio Code e vá na aba de extensõens do Code ou pressione `Ctrl+Shift+X` e procure por "Remote Development" e instale a extensão. Clone esse repositório e abra a pasta no Visual Studio Code, pressione `Ctrl+Shift+P` e digite "reopen in container" e confirme. Dentro de alguns minutos o ambiente de desenvolvimento será configurado.

### MacOS

Dependências:
- [Docker Desktop](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Git](https://git-scm.com/)

Baixe e instale o [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-mac) para MacOS e o [Visual Studio Code](https://code.visualstudio.com/download). Após isso, abra o Visual Studio Code e vá na aba de extensõens do Code ou pressione `Command+Shift+X` e procure por "Remote Development" e instale a extensão.

Instale o git, via instalação do Xcode, logo após clone esse repositório e abra a pasta no Visual Studio Code, pressione `Command+Shift+p` e digite "reopen in container" e confirme. Dentro de alguns minutos o ambiente de desenvolvimento será configurado.

## Uso

### Iniciar a aplicação

Para executar a aplicação basta abrir o barra de comandos via `Ctrl+Shift+P` ou `Command+Shift+P` e digitar `Run task`, depois selecione a opção `Run app`, logo após selecione a opção `Continue without scanning task output`. Se tudo correr bem o Visual Studio Code mostrará um popup com a opção de abrir a aplicação no navegador padrão ou ter um preview no próprio editor.

Para verificar se o banco de dados foi instalado corretamente, acesse a página `http://localhost:5000/db_test`. A segunte mensagem deve ser exibida.

```
Banco de dados inicializado com sucesso!
```

Para parar a execução da aplicação basta clicar no terminal do Visual Studio Code e pressionar `Ctrl+C` e depois `Enter`.

### Parar o container de desenvolvimento

Para interromper a execução do container de desenvolvimento basta abrir a barra de comandos com `Ctrl+Shift+P` ou `Command+Shift+P` e digitar `close remote connection` e pressionar `Enter`
