# Padrão didático dos radares de projetos

Este documento é o contrato editorial dos projetos Azure, AWS e GCP. Ele foi inspirado na organização dos treinamentos Databricks de configuração de ambiente e nível júnior.

## Jornada obrigatória

Cada projeto deve conduzir a pessoa nesta ordem:

1. **Entenda o problema:** contexto, consumidor e resultado esperado.
2. **Conheça as ferramentas:** nome, função no projeto, necessidade de instalação e custo possível.
3. **Prepare o ambiente:** o projeto `000-configuracao-ambiente` da cloud é pré-requisito.
4. **Faça comigo:** comandos exatos, pasta correta e resultado esperado.
5. **Leia o código:** entrada, regra central, saída e ponto de extensão cloud.
6. **Valide:** teste automatizado, inspeção da saída e interpretação do exit code.
7. **Pratique:** uma alteração pequena, segura e local.
8. **Registre evidência:** comando executado, teste aprovado e conclusão técnica.
9. **Resolva problemas:** erros comuns sem recomendar credenciais no código.
10. **Evolua com segurança:** integrações cloud permanecem opcionais e não são executadas automaticamente.

## Regra para novas ferramentas

Uma ferramenta nova não pode aparecer apenas em um comando. O primeiro projeto que a utilizar deve documentar:

- o que ela é e por que foi escolhida;
- onde obter a versão oficial;
- como verificar a instalação;
- como configurar apenas o necessário;
- quais arquivos ela lê ou cria;
- autenticação e permissões, quando existirem;
- custos e recursos externos possíveis;
- como desinstalar, desativar ou trabalhar sem ela;
- erros comuns e como validar o funcionamento.

## Segurança e publicação

- Nunca versionar senha, token, chave, arquivo `.env`, cache ou saída sensível.
- Preferir execução local e dados fictícios.
- Comandos cloud devem ser opcionais e claramente marcados.
- Nenhum projeto cria recursos, faz deploy, cria repositório remoto ou executa `git push` sem aprovação manual.

## Critério de conclusão

Um projeto está pronto para revisão quando código, dados, testes, README, diagrama, referências oficiais e checklist didático estão coerentes e quando os comandos locais foram executados com sucesso.


## Aplicação neste repositório

Este contrato vale para todos os projetos de `linkedin-data-engineering-articles`.
