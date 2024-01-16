# Seed

Aqui são criados alguns dados para facilitar o desenvolvimento
e alguns testes manuais. Dados como universidade, unidades consumidoras, 
contratos e etc. Leia o script para entender como eles se relacionam.

O seed de demonstração popula o banco com dados da UNB e da
UFMG.

Os comandos a seguir também devem ser executados dentro do container da api 
(mec-energia-api).

## Comandos

Super User + Seed Demo:
```sh
./scripts/seed.sh
```

Super User:
```sh
./scripts/create-superuser.sh
```

Seed Demo:
```sh
./scripts/seed_demo.sh
```

Apagar os dados do banco de dados:

```sh
./scripts/dbflush.sh
```