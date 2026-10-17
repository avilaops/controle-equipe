# Gateway MCP central da Ávila Ops

Plugin `avila-mcp-unificado`, proprietário único da conexão com `https://mcp.avilaops.com/mcp`.

O host descobre a autenticação OAuth pelo servidor. O pacote não contém token, segredo ou cabeçalho de autenticação. Plugins de domínio como CMS, CRM, Mail, Notas e TMS fornecem skills e usam esta conexão compartilhada quando suas ferramentas existem no gateway.

Essa separação impede conexões repetidas, colisões de nome e múltiplos fluxos OAuth para o mesmo serviço.

Validação estrutural não comprova autenticação ou acesso a dados. Consulte [CONEXOES.md](../../docs/CONEXOES.md).
