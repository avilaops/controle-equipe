# avila-mail

![Ícone de avila-mail](assets/plugin-icon.svg)

## Identificação e função

- ID técnico preservado: `avila-mail`.
- Nome funcional: `avila-mail`.
- Função: E-mail corporativo; a skill registra integracao nao confirmada.

O manifesto portátil fica em [plugin.json](plugin.json); o manifesto de compatibilidade fica em [.codex-plugin/plugin.json](.codex-plugin/plugin.json). O nome funcional não substitui o ID técnico.

## Skills incluídas

- [avila-mail](skills/avila-mail/SKILL.md).

## Conexão e dependências

Endpoint declarado: `https://mcp.avilaops.com/mcp`, transporte `streamable-http` e autenticação OAuth descoberta pelo servidor. Autorize a conta individual no host; o pacote não contém token.

Dependência para o aceite: Host, MCP central autenticado e ferramentas específicas autorizadas. Consulte a [plataforma própria](../../docs/PLATAFORMA.md).

## Exemplo de leitura ou análise

> Verifique as ferramentas de avila-mail disponíveis e apresente o que é possível consultar sem alterar dados.

## Validação e limites

Instalação local no host `hp`: realizada em 2026-10-17. Caso de aceite: `BLOQUEADO`, pois o gateway central autenticado não expõe ferramentas próprias deste módulo. Consulte a evidência sanitizada em [ACEITE-2026-10-17.md](../../docs/ACEITE-2026-10-17.md).

A configuração aponta para o MCP central, mas a inspeção do grafo central não identificou nós específicos deste módulo. É necessário descobrir e testar suas ferramentas antes de declarar integração operacional.

A presença de arquivos, ícone ou configuração não comprova disponibilidade de ferramentas nem autorização. Use dados de teste e respeite o escopo do usuário. A documentação de distribuição fica no [README do marketplace](../../README.md). Os ZIPs não concedem acesso aos serviços conectados.


## Plataforma própria e verificação local

A Ávila Ops usa plataforma própria. Não adote Odoo ou Medusa como dependência padrão. Descubra os contratos e ferramentas reais; não presuma stack, endpoints, dados ou permissões. O servidor deve impor autorização e isolamento por empresa.

Na raiz do marketplace, execute a validação estrutural antes de exportar:

```powershell
py -3 scripts/fabrica.py validate
```

Esse comando pertence ao marketplace, não ao ZIP isolado. Para o aceite deste pacote, a resposta ao prompt deve usar somente as fontes fornecidas ou ferramentas disponíveis, explicitar bloqueios e não realizar gravações. Validação estrutural não substitui essa execução no host.

