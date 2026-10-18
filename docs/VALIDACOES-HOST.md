# Validações das skills nos hosts

Este registro separa instalação, descoberta, execução e resultado de negócio. Uma
skill presente no catálogo não está aprovada até um pedido realista ser executado
no host indicado e produzir evidência verificável.

## Host Codex CLI

- Host: Codex CLI `0.162.1`, Linux, em 18/10/2026.
- Marketplace: `avilaops-desenvolvimento`, fonte local apontando para este acervo.
- Escopo instalado: os 29 plugins-base de aplicações, versão `0.2.0`.
- Descoberta: `codex plugin list` informou os 29 pacotes como
  `installed, enabled`; cada pacote expôs uma skill `*-desenvolver` e uma
  `*-equipe` no cache protegido do host.
- Limite: instalação e descoberta não comprovam comportamento. Os estados da
  matriz abaixo resultam das execuções descritas, não apenas da presença no host.

## Cenário de aceite

Para cada aplicação:

1. localizar o checkout e confirmar sua identidade;
2. carregar `AGENTS.md`, contexto da aplicação e estado do Git;
3. consultar `.agents/equipe/controle.json` sem inventar pessoas ou tarefas;
4. em uma cópia descartável, cadastrar uma identidade real confirmada e uma
   demanda de teste com objetivo e aceite;
5. comprovar que conclusão sem evidência e bloqueio sem motivo são recusados;
6. atualizar a demanda com motivo/evidência, reler o registro e confirmar que o
   checkout original não mudou;
7. registrar falhas de checkout, dependência ou acesso em vez de simular sucesso.

## Resultado por aplicação

| Aplicação | Instalada | Desenvolvimento | Equipe | Evidência |
| --- | --- | --- | --- | --- |
| `avila-arxisbim-com-br` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-auth-avilaops-com` | sim | aprovado | reprovado | tarefa publicada usa estado `in_progress` e responsável `codex` não cadastrado |
| `avila-avilaops-site` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-cms` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-crm-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-engops-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-erp` | sim | aprovado | reprovado | tarefas publicadas não possuem responsável cadastrado |
| `avila-extension-brave` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-ferramentas` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-gerador-3d` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-infra` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-investigacao` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-lojas-avilaops-com` | sim | aprovado | reprovado | tarefas publicadas não seguem o campo `owner` nem os estados do schema central |
| `avila-ludusequipamentos-website` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-mail-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-mcp-unificado` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-mcp-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-mellotransportesriopreto-com-br` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-motor-web` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-n8n-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-notas-integracao` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-notas-avilaops-com` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-painel-wifi` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-pentest` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-saudepet-app-br` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-scrapper` | sim | aprovado | aprovado | clone descartável do branch padrão; origem limpa e inalterada |
| `avila-sinapsemed` | sim | aprovado | aprovado | clone descartável de `feat/controle-equipe-20261016`; origem limpa e inalterada |
| `avila-tagflow` | sim | bloqueado | aprovado | checkout preservado contém somente estrutura de controle; fluxo descartável validado |
| `avila-tms` | sim | aprovado | reprovado | tarefas publicadas não possuem responsável cadastrado |

## Evidência: checkouts preservados localmente

- Aplicações: `avila-avilaops-site`, `avila-extension-brave`,
  `avila-ferramentas`, `avila-mcp-unificado`, `avila-notas-integracao`,
  `avila-painel-wifi` e `avila-tagflow`.
- Skills: os pares `*-desenvolver` e `*-equipe` foram lidos integralmente dos
  respectivos pacotes instalados `0.2.0`.
- Entrada: localizar o checkout, consultar o controle e cadastrar em cópia
  descartável a demanda `Validar skills no host Codex`, atribuída a
  `nicolas-rosa`, identidade confirmada no Linear.
- Saída de desenvolvimento: `BLOQUEADO`. O destino preservado registra a
  estrutura histórica da aplicação, mas não contém o código descrito no contexto;
  portanto não há base para executar lint, build ou afirmar estado técnico.
- Saída de equipe: `APROVADO` nas sete aplicações. Em cada cópia, a demanda
  `T-0001` percorreu `a-fazer`, `em-andamento`, `bloqueada` e `concluida`, com
  quatro entradas de histórico.
- Controles negativos: `Conclusao exige evidencia` e
  `Bloqueio exige motivo` foram devolvidos nos estados inválidos.
- Integridade: a releitura de cada cópia passou pelo validador e os sete
  `controle.json` de origem permaneceram equivalentes aos dados iniciais.
- Publicação: nenhuma. O teste não alterou repositório remoto, produção ou
  registro compartilhado.

## Evidência: checkouts remotos

- Entrada de desenvolvimento: identificar o checkout, carregar `AGENTS.md` e o
  contexto, conferir o Git e derivar os manifestos disponíveis sem executar
  deploy, migração ou escrita de dados.
- Saída de desenvolvimento: `APROVADO` nas 22 aplicações. Todos os clones rasos
  continham regras, contexto e ao menos um manifesto ou README; o Git permaneceu
  limpo antes e depois da consulta.
- Entrada de equipe: repetir o cenário controlado acima em clone descartável,
  mantendo a demanda fora do `controle.json` original.
- Saída de equipe: `APROVADO` em 18 aplicações. A demanda percorreu quatro
  estados, os dois controles negativos foram exigidos e a origem permaneceu
  inalterada.
- Reprovações: Auth usa `in_progress` e o responsável inexistente `codex`; ERP e
  TMS possuem tarefas sem responsável cadastrado; Lojas usa outro contrato de
  tarefa, sem `owner` e com estado `em_revisao`. Esses registros não podem ser
  atualizados com segurança pelo workflow atual até migração explícita.
- SinapseMed: a estrutura de equipe ainda existe apenas no branch
  `feat/controle-equipe-20261016`; o branch padrão não contém o controle.

