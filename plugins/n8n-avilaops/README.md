# avila-n8n

![Ícone de avila-n8n](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `n8n-avilaops`.
- Nome funcional: `avila-n8n`.
- Função: Conexao MCP autenticada com o n8n, sem skills no pacote.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

Nenhuma skill empacotada.

## Conexão e dependências

Endpoint declarado: `https://n8n.avilaops.com/mcp-server/http`, transporte `streamable-http`. O manifesto não fixa um tipo de autenticação; a conexão exige a autorização aceita pelo n8n.

Dependência para o aceite: Host e autorização do MCP n8n. Consulte a [plataforma própria](../../docs/PLATAFORMA.md).

## Exemplo de leitura ou análise

> Mostre os workflows disponíveis no meu n8n, sem executá-los.

## Validação e limites

Instalação local no host `hp`: realizada em 2026-10-17. Descoberta e leitura mínima do conector: `APROVADO`. Evidência sanitizada em [ACEITE-2026-10-17.md](../../docs/ACEITE-2026-10-17.md).

Uma consulta à ferramenta n8n `search_workflows` respondeu na sessão de auditoria; isso não equivale à instalação ou ao teste deste pacote no host.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de distribuição fica no [README do marketplace](../../README.md). Os ZIPs não concedem acesso aos serviços conectados.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do marketplace, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/fabrica.py validate
```

Esse comando pertence ao marketplace, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

