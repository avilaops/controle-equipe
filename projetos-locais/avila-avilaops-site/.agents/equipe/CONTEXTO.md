# Contexto verificavel

- Identificador: `avila-avilaops-site`.
- Origem: raiz deste checkout; nao depende de um caminho absoluto.
- Fontes encontradas: `README.md`, `package.json`, `AGENTS.md`.
- Gerenciador declarado: nao declarado no package.json; conferir lockfile e regras locais.

## Estrutura observada

- `artifacts/`
- `caddy/`
- `config/`
- `content/`
- `data/`
- `docs/`
- `marketing/`
- `nginx/`
- `out/`
- `public/`
- `resources/`
- `scripts/`
- `src/`

## Scripts de verificacao declarados

- `lint`: `eslint`
- `headers:check`: `node scripts/gerar-headers.mjs --conferir`
- `verificar`: `npm run lint && npm run editorial:test && npm run build && npm run seo:validate:export && npm run editorial:validate && npm run links:validate && npm run headers:validate && npm run contraste:validate && npm run tabelas:validate`
- `editorial:test`: `tsx scripts/testar-contrato-editorial.mts`

Esta lista e um retrato de 15/10/2026, nao uma prova de que os comandos passaram.
Confirme os comandos e seus efeitos antes de executa-los. Alguns testes dependem de servicos externos.
Nao execute deploy, migracao ou envio como parte de uma consulta de status.
