# Distribuição

Este repositório público é a fonte oficial do marketplace compartilhado da equipe. A leitura do
catálogo não concede acesso aos serviços conectados; cada MCP, API ou aplicativo exige suas
próprias credenciais e permissões.

## Codex e ChatGPT desktop

```powershell
codex plugin marketplace add avilaops/controle-equipe --ref main
codex plugin marketplace list
```

Abra o navegador de plugins, instale somente os pacotes necessários e inicie uma conversa
nova. Serviços conectados ainda exigem autenticação própria.

## Claude Code

O formato portátil serve como fonte, mas a instalação deve seguir o mecanismo de marketplace
suportado pela versão do Claude usada pela equipe. Não copie arquivos para o cache interno.

## Releases

Tags `v*` executam testes, empacotam todos os plugins e publicam os ZIPs e `sha256.json` numa
release do repositório. Para rollback, reinstale a versão anterior ou fixe a referência do marketplace.

## Fonte única

O antigo repositório `avilaops/plugins` foi descontinuado. Autoria, revisão, validação,
empacotamento e publicação acontecem somente em `avilaops/controle-equipe`.

## Servidor

MCPs e APIs permanecem em servidores autenticados. O repositório distribui instruções e
configurações; copiar ZIPs para um servidor não instala plugins nos clientes da equipe.
