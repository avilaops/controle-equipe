# avila-notas

![Ícone de avila-notas](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `avila-notas`.
- Nome funcional: `avila-notas`.
- Função: Consulta e organizacao de documentos e colecoes.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

- [avila-notas](skills/avila-notas/SKILL.md).

## Conexão e dependências

Endpoint declarado: `https://mcp.avilaops.com/mcp`, transporte `streamable-http`, autenticação `api_key` com esquema `bearer`. Configure a credencial individual no host; o pacote não contém token.

Dependência para o aceite: host, MCP central autenticado e ferramentas específicas autorizadas. O contrato está em [docs/CONEXOES.md](../../docs/CONEXOES.md).

## Exemplo de leitura ou análise

> Verifique as ferramentas de avila-notas disponíveis e apresente o que é possível consultar sem alterar dados.

## Validação e limites

Instalação local no Codex CLI: realizada. Execução do pacote por modelo/host: `TESTADO`. Caso de aceite de leitura: `APROVADO` em 18/10/2026. A sessão autenticada confirmou a identidade atual e listou uma coleção autorizada, sem criar, editar, mover, arquivar ou excluir conteúdo.

O teste comprova apenas o fluxo de leitura no host e nas permissões da identidade usada. Operações de escrita continuam fora do aceite até serem necessárias e autorizadas.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de exportação fica no README.md do acervo central. Os ZIPs são privados/locais e não representam submissão pública.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do acervo central, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/acervo.py validate
```

Esse comando pertence ao acervo central, não ao ZIP isolado. Para repetir o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui a execução no host. O contrato e a evidência sanitizada ficam em [docs/CONEXOES.md](../../docs/CONEXOES.md).

