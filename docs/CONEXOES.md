# Integracoes MCP e conexoes

Os pacotes iniciais nao precisam de MCP para orientar desenvolvimento local.
Adicione `mcp.json` na raiz de um plugin somente depois de verificar o endpoint,
transporte, autenticacao e ferramentas. Nao conecte todos os plugins ao mesmo
gateway sem avaliar as permissoes reais de cada identidade.

## Contrato de integracao

Registre junto ao pacote, sem credenciais:

- Aplicacao, ambiente, dono e finalidade.
- Endpoint comprovado e transporte suportado.
- Identidade utilizada, empresa/tenant e recursos permitidos.
- Autenticacao suportada e scopes efetivamente necessarios.
- Ferramentas anunciadas, schemas e classificacao leitura/escrita.
- Evidencia de inicializacao, descoberta e chamada de leitura inocua.
- Evidencia de escrita apenas quando exigida e autorizada para o destino escolhido.
- Revogacao, falhas esperadas e tratamento de operacoes com resultado incerto.

Use o schema `https://agent-plugins.org/schemas/1.0.0/mcp.schema.json`.
Configuracoes OpenAI de autenticacao ficam em `extensions.com.openai` de cada servidor.
Credenciais pertencem ao fluxo protegido do host ou ao cofre da aplicacao.
Nao inclua `.env`, tokens, chaves JSON, cabecalhos secretos ou IDs de apps inventados.

## Validar acesso

Uma conexao usa as permissoes da identidade autenticada. Confirme a conta e teste
um recurso conhecido pela superficie que executara o workflow. Disponibilidade
do plugin, autenticacao e acesso aos dados sao verificacoes distintas.

Hooks, MCP Apps e extensoes de UI devem ser adicionados apenas para necessidades
concretas, com implementacao e testes proprios. Esta fabrica nao adiciona scripts
de lifecycle nem servicos ficticios.
