# Criar e evoluir um pacote

1. Identifique a aplicacao, checkout, dono e uma tarefa recorrente concreta.
2. Gere o pacote com `fabrica.py create` ou edite sua fonte em `plugins/`.
3. Crie cada workflow em `skills/<nome>/SKILL.md` com frontmatter YAML `name` e `description`.
4. Defina entradas necessarias, passos verificaveis, saida esperada e tratamento de erros.
5. Mantenha schemas, exemplos e templates especificos em referencias internas ao pacote.
6. Derive operacoes e nomes de ferramentas da implementacao real; leia a origem antes de documentar.
7. Valide, teste a skill com um pedido realista, incremente a versao e reempacote.

## Formato da skill

```markdown
---
name: consultar-pedidos
description: Use quando o usuario pedir a consulta de pedidos da aplicacao.
---

# Consultar pedidos

1. Identifique a empresa e os filtros solicitados.
2. Descubra a ferramenta de consulta disponivel e confira seu schema.
3. Execute a consulta com os filtros autorizados.
4. Apresente os pedidos encontrados e a origem; informe filtros e ausencia de resultados.
```

Este exemplo e material de autoria; nao esta incluido como uma skill funcional nos pacotes.
Uma skill independente pode usar o mesmo diretorio da skill do plugin em uma origem de
skills suportada pelo host. Evite manter duas copias editaveis da mesma skill.

## Verificacao de release

- O manifesto portavel usa o schema Agent Plugins 1.0; metadados OpenAI ficam em `extensions.com.openai`.
- O overlay Codex deve manter nome, versao e apresentacao sincronizados.
- O validador local verifica estrutura, frontmatter, referencias, nomes e arquivos proibidos.
- O manifesto portavel e conferido com uma copia do schema oficial obtida em 15/10/2026. Metadados OpenAI e MCP recebem verificacoes locais adicionais, sem promessa de cobertura integral.
- O validador nao substitui revisao de segredos nem teste no host.
- Confira o ZIP final, com manifesto na raiz e um unico plugin. `package` verifica CRC e gera SHA-256.
- Para workflows com escrita, teste em destino controlado e leia o resultado antes de repetir uma tentativa.
- Publicacao no workspace ou diretorio publico exige o fluxo proprio da plataforma; ZIP local nao equivale a publicacao.
