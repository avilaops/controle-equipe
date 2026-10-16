# Fabrica de plugins e skills Avila Ops

Os destinos e commits desta entrega estao em [Publicacao Git](PUBLICACAO-GIT.md).
O repositorio central e privado. `projetos-locais/` preserva somente a estrutura
de equipe dos projetos que nao tinham remoto Git acessivel na publicacao.

## Controle da equipe nos repositorios

Cada uma das 29 aplicacoes tem agora `.agents/equipe/` com contexto, registro de
pessoas, tarefas, decisoes e integracoes, alem de uma skill local em `.agents/skills/`.
O AGENTS.md de cada raiz aponta para essa estrutura. As regras anteriores foram preservadas.

Consulte o [painel consolidado](PAINEL-EQUIPE.md). Os registros iniciais estao vazios:
nao foram informados nomes, atribuicoes ou demandas reais para cadastrar.

```powershell
python scripts/equipe.py --help
python scripts/equipe.py painel
python scripts/equipe.py exportar
python scripts/fabrica.py package
```

Os repositorios sao a origem das skills de equipe. `exportar` atualiza apenas as
skills correspondentes nos pacotes centrais. Atualize o painel para refletir alteracoes
nos registros. O controle e local e versionavel; nao e um servico de acompanhamento em tempo real.

Base de autoria local para as aplicacoes encontradas em `D:\Projetos`.
O acervo anterior da central e os repositorios originais permanecem preservados.

## Estrutura

```text
desenvolvimento/
  .agents/plugins/marketplace.json  Catalogo para distribuicao local
  catalogo/aplicacoes.json         Aplicacoes, evidencias e classificacoes
  plugins/<nome>/                  Fonte editavel de cada plugin
    plugin.json                   Manifesto portavel Agent Plugins 1.0
    .codex-plugin/plugin.json      Manifesto de compatibilidade Codex
    skills/<nome>/SKILL.md         Workflow e criterio de uso
    skills/<nome>/references/      Contexto especifico da aplicacao
  scripts/fabrica.py               Gerador, validador e empacotador
  docs/                           Autoria, conexoes e verificacao
  reports/validacao.json           Evidencia de validacao estrutural
  dist/                           Um ZIP por plugin e hashes SHA-256
```

## Usar

No PowerShell, a partir desta pasta:

```powershell
python -m pip install -r requirements.txt
python scripts/fabrica.py inventory D:\Projetos
python scripts/fabrica.py validate
python scripts/fabrica.py package
python -m unittest discover -s scripts -p test_fabrica.py -v
```

O inventario preserva pacotes existentes. Ele cobre as pastas imediatas do workspace,
classifica terceiros e artefatos e registra pastas ainda sem classificacao.
Nao representa inventario recursivo de produtos internos nem de sistemas apenas remotos.

Para uma nova aplicacao ou subaplicacao:

```powershell
python scripts/fabrica.py create avila-nova-aplicacao --source D:\Projetos\MinhaAplicacao --description 'Minha aplicacao'
python scripts/fabrica.py validate
python scripts/fabrica.py package
```

O gerador recusa sobrescrever pacotes existentes. Registre novas aplicacoes recorrentes
no mapa `APPLICATIONS` para integra-las ao inventario. Skills existentes em outros
locais nao sao importadas automaticamente: revise escopo, dependencias e licenca antes.

## Disponibilidade

Os pacotes iniciais oferecem desenvolvimento local orientado ao checkout de cada aplicacao.
Ainda nao fornecem ferramentas de negocio, acesso remoto ou operacoes de producao.
O catalogo nao instala nem ativa plugins. Para registrar a fonte local, com uma versao
do Codex que ofereca esse comando:

```powershell
codex plugin marketplace add D:\Projetos\central-integracoes\desenvolvimento
```

Depois instale o plugin escolhido no diretorio de plugins e verifique-o em uma nova conversa.
Para web e mobile, um checkout local nao fica acessivel por instalar o pacote; workflows
remotos exigem uma conexao suportada e testada. Consulte [Autoria](docs/AUTORIA.md)
e [Conexoes](docs/CONEXOES.md).

Formato conferido em 15/10/2026 com a [documentacao oficial de pacotes](https://developers.openai.com/plugins/build/plugins).
