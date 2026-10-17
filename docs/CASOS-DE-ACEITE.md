# Casos de aceite

Cada plugin contém um exemplo de uso e suas dependências no próprio `README.md`. Esses cenários
devem ser executados em um host compatível; a validação estrutural não executa prompts nem
comprova acesso aos serviços.

## Registro obrigatório

Para cada execução, registre:

- plugin e versão;
- data e host;
- identidade e empresa autorizadas;
- entrada utilizada;
- evidência sanitizada da saída;
- resultado: `APROVADO`, `REPROVADO` ou `BLOQUEADO`;
- limitações encontradas.

Não registre tokens, credenciais, dados pessoais ou conteúdo de clientes.

## Critérios

Um caso é `APROVADO` quando o plugin é descoberto pelo host, aplica as instruções esperadas,
respeita o escopo autorizado e produz a saída descrita em seu README. Ausência de ferramenta,
autenticação ou autorização resulta em `BLOQUEADO`. Saída incorreta ou ação fora do escopo
resulta em `REPROVADO`.

Pacotes com MCP devem começar por uma leitura mínima. Gravações, publicações, mensagens e
operações de infraestrutura exigem pedido explícito e verificação posterior do resultado.
