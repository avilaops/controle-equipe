# Integracoes MCP e conexoes

Os pacotes iniciais nao precisam de MCP para orientar desenvolvimento local.
Adicione `mcp.json` na raiz de um plugin somente depois de verificar o endpoint,
transporte, autenticacao e ferramentas. Cada servidor deve ter um unico plugin
proprietario. Skills de dominio usam a conexao compartilhada sem registrar
novamente o mesmo nome ou endpoint.

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
O host descobre a autenticacao compativel pelo servidor. Credenciais pertencem
ao fluxo protegido do host ou ao cofre da aplicacao.
Nao inclua `.env`, tokens, chaves JSON, cabecalhos secretos ou IDs de apps inventados.

## Validar acesso

Uma conexao usa as permissoes da identidade autenticada. Confirme a conta e teste
um recurso conhecido pela superficie que executara o workflow. Disponibilidade
do plugin, autenticacao e acesso aos dados sao verificacoes distintas.

Hooks, MCP Apps e extensoes de UI devem ser adicionados apenas para necessidades
concretas, com implementacao e testes proprios. Esta fabrica nao adiciona scripts
de lifecycle nem servicos ficticios.

## Conexoes validadas

### avila-cms-operacoes

- Ambiente e host: producao, Codex CLI `0.162.1`, em 18/10/2026.
- Finalidade: consultar sites, paginas, posts e midia do CMS da plataforma propria.
- Endpoint e transporte: `https://mcp.avilaops.com/mcp`, `streamable-http`.
- Autenticacao: OAuth descoberto pelo gateway central e concluido no fluxo
  protegido do host; nenhum segredo fica no pacote.
- Identidade e tenant: sessao autenticada; o tenant foi escolhido somente entre
  os sites devolvidos por `cms_listar_sites`, que tambem informou o papel efetivo.
- Permissao minima validada: leitura. Escrita nao foi necessaria nem executada.
- Descoberta: 36 ferramentas `cms_*` anunciadas no host, sendo 14 de leitura ou
  validacao e 22 com efeito de escrita.
- Leitura comprovada: `cms_listar_sites`, `cms_listar_documentos` e
  `cms_ver_documento`; a ultima confirmou identificador, titulo e estado de uma
  pagina existente sem criar rascunho ou alterar publicacao.
- Limite: o resultado comprova somente a identidade, o tenant e o host usados no
  teste. Outro host, conta ou tenant exige nova validacao. Escritas exigem uma
  necessidade concreta, autorizacao e releitura do registro quando suportada.
- Revogacao e falhas: revogue o consentimento OAuth ou remova a conexao no host.
  Em erro de autenticacao ou resultado incerto, nao repita gravacoes nao idempotentes.

### n8n-avilaops

- Ambiente e host: producao, Codex CLI `0.162.1`, em 18/10/2026.
- Finalidade: consultar projetos e workflows da instancia n8n da Avila Ops.
- Endpoint e transporte: `https://n8n.avilaops.com/mcp-server/http`,
  `streamable-http`.
- Autenticacao: conexao autenticada pelo fluxo protegido do host e do n8n. O
  mecanismo e a credencial nao sao expostos a conversa nem fixados no pacote.
- Identidade e escopo: a sessao encontrou um projeto pessoal acessivel; projetos
  de equipe nao estao habilitados na instancia. Identificadores e dados pessoais
  nao sao registrados no pacote.
- Permissao minima validada: leitura. Escrita e execucao nao foram necessarias
  nem executadas.
- Descoberta: o host anunciou ferramentas de consulta e administracao do n8n.
  A presenca de ferramentas com escrita nao amplia a autorizacao do workflow.
- Leitura comprovada: `search_projects` confirmou o projeto acessivel e
  `search_workflows` devolveu 82 workflows, com metadados de cinco resultados na
  primeira pagina, sem carregar dados de execucao.
- Limite: outro host ou outra identidade exige nova validacao. Antes de executar
  um workflow, leia seus detalhes e obtenha autorizacao especifica; publicar,
  despublicar, instalar nodes e alterar credenciais exigem confirmacao propria.
- Revogacao e falhas: revogue a conexao no host ou no n8n. Se uma escrita ou
  execucao retornar resultado incerto, consulte o recurso antes de tentar de novo.

### avila-notas

- Ambiente e host: producao, Codex CLI `0.162.1`, em 18/10/2026.
- Finalidade: consultar documentos e colecoes do Notas da plataforma propria.
- Endpoint e transporte: `https://mcp.avilaops.com/mcp`, `streamable-http`.
- Autenticacao: OAuth descoberto pelo gateway central e concluido no fluxo
  protegido do host; nenhum segredo fica no pacote.
- Identidade e tenant: `notas_fetch` com `current_user` confirmou a identidade
  autenticada e seu papel administrativo. Dados pessoais nao sao registrados.
- Permissao minima validada: leitura. Escrita nao foi necessaria nem executada.
- Descoberta: 19 ferramentas `notas_*`, sendo 7 de leitura e 12 de escrita.
- Leitura comprovada: `notas_fetch` confirmou a identidade e
  `notas_list_collections` devolveu uma colecao acessivel, sem carregar ou alterar
  seu conteudo.
- Limite: outro host ou outra identidade exige nova validacao. Criacao, edicao,
  movimentacao, arquivamento e exclusao permanecem fora deste aceite.
- Revogacao e falhas: revogue o consentimento OAuth ou remova a conexao no host.
  Em erro de autenticacao ou resultado incerto, nao repita gravacoes nao idempotentes.

### avila-lojas

- Ambiente e host: producao, Codex, em 17/10/2026.
- Finalidade: consultar a loja e o catalogo autorizados pelo lojista.
- Endpoint e transporte: `https://lojas.avilaops.com/api/mcp`,
  `streamable-http`, registrado como `avilaops-lojas` pelo plugin proprietario
  `avila-lojas`.
- Autenticacao, identidade e tenant: OAuth descoberto pelo servidor, com escolha
  explicita da loja e dos escopos no navegador; nenhum token fica no pacote.
- Permissao minima validada: leitura. Escrita nao foi necessaria nem executada.
- Leitura comprovada: a conexao confirmou plano, estado da loja e acesso ao
  catalogo do tenant escolhido sem registrar dados do cliente no pacote.
- Compartilhamento: `lojas-clientes` usa esta conexao sem registrar outro
  servidor MCP; sua leitura minima tambem foi aprovada no mesmo aceite.
- Limite: outro host, identidade ou loja exige nova validacao. Alteracoes de
  produto, pedido, estoque ou configuracao exigem autorizacao especifica e
  verificacao posterior.
- Revogacao e falhas: revogue o consentimento OAuth ou remova a conexao no host.
  Em resultado incerto, releia o recurso antes de repetir qualquer gravacao.

## Conexoes pendentes

### avila-crm

- Endpoint testado, mas nao empacotado: `https://mcp.avilaops.com/mcp`,
  `streamable-http`.
- Resultado: nenhuma ferramenta especifica de CRM foi anunciada no host por
  nome, esquema ou finalidade.
- Acao necessaria: expor o modulo CRM no MCP central, autenticar identidade com
  tenant definido e comprovar uma leitura inocente antes de aprovar o pacote.

### avila-mail

- Endpoint testado, mas nao empacotado: `https://mcp.avilaops.com/mcp`,
  `streamable-http`.
- Resultado: nenhuma ferramenta especifica do Avila Mail foi anunciada. As
  ferramentas Gmail disponiveis pertencem a outro provedor e nao sao evidencia.
- Acao necessaria: expor o modulo Mail no MCP central, autenticar identidade com
  tenant definido e comprovar uma leitura inocente antes de aprovar o pacote.

### avila-tms-operacoes

- Endpoint testado, mas nao empacotado: `https://mcp.avilaops.com/mcp`,
  `streamable-http`.
- Resultado: nenhuma ferramenta especifica de TMS foi anunciada por nome,
  esquema ou finalidade. Ferramentas fiscais e da Lojas nao substituem o TMS.
- Acao necessaria: expor o modulo TMS no MCP central, autenticar identidade com
  empresa definida e comprovar uma leitura inocente antes de aprovar o pacote.
