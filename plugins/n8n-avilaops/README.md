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

Dependência para o aceite: host e autorização do MCP n8n. O contrato está em [docs/CONEXOES.md](../../docs/CONEXOES.md).

## Exemplo de leitura ou análise

> Mostre os workflows disponíveis no meu n8n, sem executá-los.

## Validação e limites

Conexão no host Codex: `TESTADO`. Caso de aceite de leitura: `APROVADO` em 18/10/2026. A sessão autenticada identificou o projeto pessoal acessível e consultou os workflows por esse projeto, sem executar ou alterar automações.

O teste comprova a conexão e as permissões da identidade usada no host. O método de autenticação permanece administrado pelo fluxo protegido do n8n e não é exposto à conversa nem fixado no manifesto. Operações de escrita e execução continuam fora do aceite até serem necessárias e autorizadas.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de exportação fica no README.md do acervo central. Os ZIPs são privados/locais e não representam submissão pública.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do acervo central, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/acervo.py validate
```

Esse comando pertence ao acervo central, não ao ZIP isolado. Para repetir o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui a execução no host. O contrato e a evidência sanitizada ficam em [docs/CONEXOES.md](../../docs/CONEXOES.md).

