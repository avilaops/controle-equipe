# avila-engenharia-operacoes

![Ícone de avila-engenharia-operacoes](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `avila-ops-skills`.
- Nome funcional: `avila-engenharia-operacoes`.
- Função: Cinco skills de engenharia, design, infraestrutura e integracoes.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

- [avila-agent-ready](skills/avila-agent-ready/SKILL.md).
- [avila-coder](skills/avila-coder/SKILL.md).
- [avila-design-system](skills/avila-design-system/SKILL.md).
- [avila-infra-coolify](skills/avila-infra-coolify/SKILL.md).
- [avila-vigia-integracoes](skills/avila-vigia-integracoes/SKILL.md).

## Conexão e dependências

Este pacote não declara servidor MCP. As integrações dependem das ferramentas e autorizações realmente disponíveis no host.

Dependência para o aceite: Host, skills carregadas e insumos de teste. Consulte a [plataforma própria](../../docs/PLATAFORMA.md).

## Exemplo de leitura ou análise

> Analise este repositório de teste e proponha verificações sem modificar ou implantar.

## Validação e limites

Instalação local no host `hp`: realizada em 2026-10-17. A skill foi descoberta e aplicada a uma entrada sintética em modo somente leitura. Caso de aceite: `APROVADO`. Consulte a evidência sanitizada em [ACEITE-2026-10-17.md](../../docs/ACEITE-2026-10-17.md).

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de distribuição fica no [README do marketplace](../../README.md). Os ZIPs não concedem acesso aos serviços conectados.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do marketplace, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/fabrica.py validate
```

Esse comando pertence ao marketplace, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

