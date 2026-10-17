# Distribuição privada

Este repositório é o marketplace compartilhado da equipe. Os pacotes permanecem privados;
somente membros autorizados da organização conseguem cloná-los ou adicioná-los pelo GitHub.

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
release privada. Para rollback, reinstale a versão anterior ou fixe a referência do marketplace.

## Servidor

MCPs e APIs permanecem em servidores autenticados. O repositório distribui instruções e
configurações; copiar ZIPs para um servidor não instala plugins nos clientes da equipe.
