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

O pacote não declara `mcp.json`: a identidade testada não estava vinculada a uma loja específica, portanto nenhuma leitura tenant-scoped foi aprovada.

Dependência para o aceite: host, MCP central autenticado e ferramentas específicas autorizadas. O contrato está em [docs/CONEXOES.md](../../docs/CONEXOES.md).

## Exemplo de leitura ou análise

> Consulte somente a loja autorizada e apresente os campos de catálogo ausentes, sem salvar.

## Validação e limites

Auditoria no Codex CLI: realizada. Caso de aceite: `BLOQUEADO_TENANT` em 18/10/2026. As ferramentas Lojas foram descobertas, mas a chave administrativa da sessão não está vinculada a uma loja específica. O backend recusou corretamente as leituras e nenhuma escrita foi tentada.

Para concluir o aceite, use uma credencial individual limitada à loja do cliente no fluxo protegido do host. Nunca reutilize a chave administrativa genérica neste pacote.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de exportação fica no README.md do acervo central. Os ZIPs são privados/locais e não representam submissão pública.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do acervo central, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/acervo.py validate
```

Esse comando pertence ao acervo central, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

