# Plataforma própria Ávila Ops

## Fonte das regras

A Ávila Ops usa sua própria plataforma para ERP, lojas e operações. Odoo e Medusa não são
dependências padrão. Automações e sincronizações devem partir dos contratos encontrados nos
projetos e das ferramentas realmente disponibilizadas pelo host.

Não presuma tabelas, endpoints, autenticação, módulos ou regras de negócio. Leia o código e a
documentação do sistema envolvido antes de propor ou executar uma integração.

## Responsabilidades

A skill orienta o trabalho. O plugin distribui instruções e configurações. O servidor MCP ou a
API executa operações e deve impor autorização, isolamento por empresa e regras de negócio.

Uma configuração de conexão não concede acesso. Preços, estoque, clientes, pedidos e dados
fiscais devem vir da fonte autorizada. Indisponibilidade e dados ausentes devem aparecer no
resultado.

## Critério de integração concluída

1. Identificar usuário, empresa e recurso autorizado.
2. Confirmar a ferramenta ou contrato real e a autenticação do host.
3. Executar uma leitura mínima sem alteração de dados.
4. Registrar resultado, data e limitações sem expor credenciais.
5. Testar gravações somente quando solicitadas e conferir o estado persistido.

Validação estrutural, instalação, conexão autenticada e resultado operacional são evidências
distintas. Consulte também [Conexões](CONEXOES.md) e [Casos de aceite](CASOS-DE-ACEITE.md).
