# avila-tms

![Ícone de avila-tms](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `avila-tms`.
- Nome funcional: `avila-tms`.
- Função: Transportes; a skill registra adaptador pendente.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

- [avila-tms](skills/avila-tms/SKILL.md).

## Conexão e dependências

O pacote não declara `mcp.json`: nenhuma ferramenta específica de TMS foi descoberta no endpoint central durante o aceite.

Dependência para o aceite: host, MCP central autenticado e ferramentas específicas autorizadas. O contrato está em [docs/CONEXOES.md](../../docs/CONEXOES.md).

## Exemplo de leitura ou análise

> Verifique as ferramentas de avila-tms disponíveis e apresente o que é possível consultar sem alterar dados.

## Validação e limites

Auditoria no Codex CLI: realizada. Caso de aceite: `BLOQUEADO_SEM_FERRAMENTAS` em 18/10/2026. O host autenticado não anunciou ferramentas específicas de TMS por nome, esquema ou finalidade. Ferramentas fiscais ou de pedidos da Lojas não comprovam acesso ao TMS.

Para concluir o aceite, o MCP central precisa expor ferramentas do TMS com escopo mínimo e permitir uma leitura inocente com identidade e empresa confirmadas. Nenhuma ferramenta de outro módulo deve ser tratada como substituta.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de exportação fica no README.md do acervo central. Os ZIPs são privados/locais e não representam submissão pública.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do acervo central, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/acervo.py validate
```

Esse comando pertence ao acervo central, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

