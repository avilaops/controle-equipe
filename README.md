# Marketplace Ávila Ops

Fonte compartilhada de plugins, skills e controle de equipe da Ávila Ops.

- 29 plugins de desenvolvimento ligados às aplicações.
- 11 plugins operacionais e de produto.
- 1 plugin `avila-skills` com 20 workflows especializados.
- Fonte oficial e única dos plugins Ávila Ops.

Consulte o [catálogo](docs/CATALOGO.md), a [galeria](docs/GALERIA.html), a [distribuição](docs/DISTRIBUICAO.md),
a [autoria](docs/AUTORIA.md), as [integrações](docs/CONEXOES.md), os
[casos de aceite](docs/CASOS-DE-ACEITE.md), as [validações no host](docs/VALIDACOES-HOST.md),
a [plataforma própria](docs/PLATAFORMA.md) e o
[controle da equipe](PAINEL-EQUIPE.md).

## Estrutura

```text
.agents/plugins/marketplace.json  Catálogo consumido pelos clientes
plugins/                          Fontes editáveis dos plugins
scripts/fabrica.py                Validação e empacotamento
scripts/equipe.py                 Controle versionado da equipe
schemas/                          Schemas portáteis utilizados
docs/                             Catálogo e procedimentos
dist/                             Artefatos gerados, fora do Git
```

## Verificar

```powershell
py -3 -m pip install -r requirements.txt
py -3 -m unittest discover -s scripts -p "test_*.py" -v
py -3 scripts/fabrica.py validate
py -3 scripts/fabrica.py package
```

O empacotamento compara cada arquivo do ZIP com a fonte validada, extrai o pacote em ambiente
temporário e repete a descoberta estrutural. Isso não substitui autenticação nem execução
funcional dentro do host.

## Instalar pela equipe

```powershell
codex plugin marketplace add avilaops/controle-equipe --ref main
codex plugin marketplace list
```

Depois, instale os plugins necessários pelo navegador de plugins e inicie uma conversa nova.
O catálogo é público; cada MCP, API ou aplicativo conectado mantém autenticação e autorização próprias.

## Fonte oficial

Este repositório substitui o antigo `avilaops/plugins`. Novos plugins, skills, documentação,
validação, empacotamento e releases devem ser mantidos somente aqui. Cópias instaladas e caches
locais são artefatos derivados e não devem receber alterações manuais.

## Identidades semelhantes

`avila-cms` e `avila-tms` orientam desenvolvimento nos respectivos checkouts.
`avila-cms-operacoes` e `avila-tms-operacoes` fornecem workflows operacionais ligados ao MCP.
Essa separação evita que uma instalação substitua silenciosamente a outra.

## Limites

Os plugins não carregam credenciais nem concedem acesso automaticamente. MCPs e APIs precisam
estar disponíveis, autenticados e autorizados para a identidade e empresa corretas. Evidência
estrutural, instalação, conexão e resultado de negócio são estados diferentes.

Formato baseado na [documentação oficial de plugins OpenAI](https://developers.openai.com/plugins/build/plugins).
