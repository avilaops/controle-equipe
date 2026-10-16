# Autoria de plugins Avila Ops

- Esta pasta e a fonte dos novos pacotes; o acervo legado no diretorio pai permanece separado.
- Nao edite caches de plugins instalados. Nao mova os repositorios das aplicacoes.
- Use `scripts/fabrica.py create` para iniciar um pacote. Preserve nomes e incremente a versao ao alterar uma entrega.
- Cada skill deve resolver uma tarefa concreta, definir quando se aplica e verificar o resultado.
- Contexto extenso fica em referencias dentro do proprio pacote. Nunca empacote segredos ou dados de clientes.
- Leia as instrucoes do checkout antes de trabalhar nele. Nao replique arquivos AGENTS.md para evitar divergencia.
- MCP, apps, hooks e interfaces sao opcionais. Adicione apenas capacidades implementadas e verificadas.
- Nao declare endpoint, OAuth, ferramenta ou identificador sem evidencia. Nao use hooks executaveis por padrao.
- Antes de entregar: execute validacao e empacotamento. Instalacao, acesso remoto e publicacao sao etapas separadas.
