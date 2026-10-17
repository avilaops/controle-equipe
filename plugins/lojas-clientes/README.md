# avila-lojas-clientes

![Ícone de avila-lojas-clientes](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `lojas-clientes`.
- Nome funcional: `avila-lojas-clientes`.
- Função: Preenchimento de loja e catalogo pelo cliente autorizado.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

- [preencher-loja](skills/preencher-loja/SKILL.md).

## Conexão e dependências

Endpoint declarado: `https://lojas.avilaops.com/api/mcp`, transporte `streamable-http` e autenticação OAuth descoberta pelo servidor. O lojista escolhe a loja e os escopos no navegador; o pacote não contém token.

Dependência para o aceite: Host, MCP central autenticado e ferramentas específicas autorizadas. Consulte a [plataforma própria](../../docs/PLATAFORMA.md).

## Exemplo de leitura ou análise

> Consulte somente a loja autorizada e apresente os campos de catálogo ausentes, sem salvar.

## Validação e limites

Instalação local no host `hp`: realizada em 2026-10-17. Descoberta e leitura mínima do conector: `APROVADO`. Evidência sanitizada em [ACEITE-2026-10-17.md](../../docs/ACEITE-2026-10-17.md).

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de distribuição fica no [README do marketplace](../../README.md). Os ZIPs não concedem acesso aos serviços conectados.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do marketplace, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/fabrica.py validate
```

Esse comando pertence ao marketplace, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

