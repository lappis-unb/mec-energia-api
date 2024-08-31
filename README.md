![Coverage Testes](https://gitlab.com/lappis-unb/projects/mec-energia/mec-energia-api/badges/develop/coverage.svg)

# MEC-Energia API

Este repositório contém a implementação da API do sistema MEC-Energia.

O sistema MEC-Energia tem por objetivo auxiliar as instituições de ensino superior (IES) a gerenciar e avaliar a adequação de contratos de conta de energia elétrica a partir do registro das faturas mensais de energia, gerando relatórios de recomendações de ajustes nos contratos visando economia de recursos.

A documentação online do sistema está disponível em [Documentação](https://lappis-unb.gitlab.io/projects/mec-energia/documentacao)


## Como executar o serviço


### Pré-requisitos
- Docker: Certifique-se de que o Docker e Docker compose estão instalados e funcionando.
- Make: Certifique-se de ter o make instalado.
- Arquivo .env: Preencha o .env correspondente ao ambiente (.env.dev, .env.test, e .env.prod).

### Ambiente de desenvolvimento
O ambiente de desenvolvimento utiliza Docker para executar containers da API e do PostgreSQL, 
configurados em modo debug com hot reload. Para garantir a consistência com os ambientes de teste 
e produção, é recomendável evitar rodar o ambiente fora do Docker.

##### Construir e iniciar os serviços com Make:

```bash
make build && make up
# ou 
make build-up
```
Alternativamente, usando somente o docker compose:

```bash
# Copiar o arquivo .env apropriado para o diretório raiz:
cp .envs/.env.dev .env

# Construir e levantar os serviços:
docker compose up --build
```

o servidor será iniciado em [http://localhost:8000](http://localhost:8000), se a porta padrão não foi alterada no arquivo **.env.dev**

##### Derrubar o ambiente:
```bash
# com make
make down

# sem make
docker compose down
```

### Ambiente de testes
O ambiente de testes é configurado para replicar o ambiente de produção localmente, facilitando a simulação de 
cenários reais. Ele utiliza o mesmo servidor de produção, Gunicorn, e serve arquivos estáticos com Whitenoise. 
Todo o ambiente é pré-configurado em modo de produção, mas com ajustes nos ALLOWED_HOSTS, CSRF, e CORS
para permitir a execução local junto ao frontend, sem necessidade de configuração adicional.

O ambiente também inclui Debug Toolbar e está configurado para testes automatizados com Pytest, utilizando um 
banco de dados em memória para maior rapidez. Todas as configurações estão no arquivo .envs/.env.test.

##### Construir e iniciar os serviços com Make:
```bash
make build-test && make up-test
# ou 
make build-up-test
```

Alternativamente, usando somente o docker compose:

```bash
# Copiar o arquivo .env apropriado para o diretório raiz:
cp .envs/.env.test .env

# Construir e levantar os serviços:
docker compose -f compose-test.yml up --build
```

o servidor será iniciado em [http://localhost:8000](http://localhost:8000), se a porta padrão não foi alterada no arquivo **.env.test**

##### derrubar o ambiente:
```bash
# com make
make down-test

# sem make
docker compose -f compose-test.yml down
```

### Ambiente de produção

O ambiente de produção ainda está em desenvolvimento e requer configurações de outros repositórios, como 
infraestrutura e frontend, além de serviços como Nginx ou Traefik. Rodar este ambiente localmente não é viável 
sem grandes ajustes.

O ambiente de testes simula o ambiente de produção, usando as mesmas configurações de servidor e ajustes para 
rodar localmente com o frontend, garantindo testes confiáveis.


### Observações
Os comandos de up (**up, build-up**) iniciam os containers no modo **-detach** ou **-d** (background), permitindo 
que os logs sejam acessados separadamente. Execute os comandos de build (**build, build-nc**) sempre que houver 
mudanças no código ou na configuração que necessitem recompilação das imagens Docker.

O comando **build-nc** é utilizado para construir as imagens Docker sem usar o cache, garantindo que todas as 
dependências sejam baixadas novamente. Isso é útil para garantir que a imagem final esteja atualizada e livre de 
possíveis inconsistências de cache.

Este comando funciona para todos os ambientes:
- Desenvolvimento: **make build-nc**
- Produção: make **build-nc-prod**
- Teste: make **build-nc-test**



## Código de Conduta e Políticas

* Leia o [Código de Conduta](/CODE_OF_CONDUCT.md) do projeto;
* Veja as [Políticas](docs/politicas/branches-commits.md) do projeto.


## Documentação Extra de Configuração

Para saber mais sobre configuração de ambiente de desenvolvimento e 
outras coisas, acesse os seguintes links:

- **Comece aqui:** [ambiente de desenvolvimento](docs/ambiente-desenvolvimento.md)
- [Seed/popular](docs/seed.md)
- [Testes](docs/testes.md)
- [Depuração](docs/depuracao.md)
