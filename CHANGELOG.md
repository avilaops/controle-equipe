# Changelog

## 1.0.3 - 2026-10-17

- Consolidado o gateway central no plugin `avila-mcp-unificado`.
- Mantido o endpoint de Lojas somente no plugin `avila-lojas`.
- Removidos registros e fluxos OAuth duplicados dos plugins de domínio.
- Adicionada validação que rejeita nomes de servidores MCP duplicados no marketplace.

## 1.0.2 - 2026-10-17

- Corrigidos sete manifestos MCP rejeitados pelo Codex por usarem `extensions` fora do contrato.
- Alterados os plugins de Lojas para o endpoint dedicado com OAuth e escolha explícita de tenant.
- Adicionado teste de regressão para compatibilidade real dos manifestos MCP.
- Executados os aceites de Apple, Design, Engenharia, CMS e Notas; CRM, Mail e TMS ficaram bloqueados por ausência de ferramentas próprias.

## 1.0.1 - 2026-10-17

- Removido o pacote sem identidade funcional `dev-6ad0a0086b188191928c20e0cf70d6fe`.
- Confirmada a instalação local dos 11 plugins operacionais e de produto.
- Validados OAuth e leitura real nos conectores Ávila Ops, Lojas e n8n.
- Registrado o aceite sanitizado dos conectores no host `hp`.

## 1.0.0 - 2026-10-17

- Consolidado o marketplace oficial de desenvolvimento e operações.
- Adicionados 12 plugins operacionais e uma biblioteca com 20 skills.
- Separadas as identidades `avila-cms-operacoes` e `avila-tms-operacoes`.
- Adicionados ícones, documentação, validação de links, CI e releases.
- Definido `avilaops/controle-equipe` como fonte única, substituindo `avilaops/plugins`.
- Reforçada a validação de arquivos, manifestos, MCPs e integridade dos ZIPs.
