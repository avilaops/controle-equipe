# Gateway MCP central da Ávila Ops

Plugin `avila-mcp-unificado`, proprietário único da conexão com `https://mcp.avilaops.com/mcp`.

O host descobre a autenticação OAuth pelo servidor. O pacote não contém token, segredo ou cabeçalho de autenticação. Plugins de domínio como CMS, CRM, Mail, Notas e TMS fornecem skills e usam esta conexão compartilhada quando suas ferramentas existem no gateway.

O OAuth também é a fonte da autorização humana: o gateway conserva `papel` e
`apps` retornados pelo `auth.avilaops.com`, e ferramentas `admin_*` exigem
`papel=ADMIN`. Tokens internos entre gateway, n8n e sistemas de destino apenas
autenticam o salto técnico; eles não substituem a permissão do usuário logado.

Essa separação impede conexões repetidas, colisões de nome e múltiplos fluxos OAuth para o mesmo serviço.

Validação estrutural não comprova autenticação ou acesso a dados. Consulte [CONEXOES.md](../../docs/CONEXOES.md).
