## Pauta de hoje: Tag Automations no Unity Catalog

Em **7 de agosto de 2026**, o Azure Databricks anunciou o recurso **Tag Automations**, que aplica ou remove governed tags automaticamente em tabelas e volumes do Unity Catalog conforme regras definidas pela organização.

As condições podem considerar metadados como:

- proprietário;
- descrição;
- nome do ativo;
- tags existentes;
- tags das colunas;
- quantidade de leituras ou gravações;
- última consulta;
- data de criação ou atualização.

O recurso pode ser usado para certificar dados confiáveis, identificar ativos desatualizados, elevar classificações de sensibilidade e encontrar ativos sem as tags obrigatórias.

**Status:** Beta. Não é classificado como pronto para produção, não possui SLA e pode exigir habilitação na página de previews do workspace. [Notas oficiais de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)

## Artigo final para o LinkedIn

# Governed tags agora podem acompanhar as mudanças dos dados no Azure Databricks

Criar uma política de tags é relativamente simples.

O desafio aparece depois: manter milhares de tabelas e volumes classificados corretamente enquanto proprietários, utilização, descrições e estados dos dados continuam mudando.

Em 7 de agosto de 2026, o Azure Databricks anunciou Tag Automations, um recurso que aplica e remove governed tags automaticamente com base em regras sobre os metadados do Unity Catalog.

## O que são Tag Automations?

Uma automação possui quatro componentes principais:

1. um escopo;
2. um conjunto de condições;
3. uma ação de adicionar ou remover tag;
4. uma execução manual ou recorrente.

Quando um ativo corresponde às condições, a automação pode atribuir ou remover uma governed tag.

Como são governed tags, os valores aplicados continuam respeitando as políticas e permissões definidas pela organização.

## Quais condições podem ser utilizadas?

As regras podem considerar diferentes características dos ativos:

- tag ou valor de tag existente;
- governed tags presentes nas colunas;
- número de consultas de leitura ou gravação nos últimos 30 dias;
- quantidade de dias desde a última consulta;
- data de criação ou última atualização;
- proprietário;
- existência de descrição;
- trecho presente no nome do ativo.

Essas condições podem ser combinadas com as opções “corresponder a todas” ou “corresponder a qualquer uma”.

A automação trabalha com regras determinísticas sobre metadados. Ela não substitui a Data Classification, que examina dados e identifica conteúdos sensíveis nas colunas.

## Exemplos de utilização

Um primeiro cenário seria certificar tabelas prontas para consumo.

A regra poderia exigir que a tabela:

- pertença a uma equipe responsável por dados de produção;
- tenha uma descrição;
- tenha recebido mais de 100 consultas de leitura nos últimos 30 dias.

Quando todos os critérios forem atendidos, a automação atribuiria:

```text
system.certification_status = certified
```

Outro cenário seria identificar dados desatualizados:

- última atualização superior a 90 dias;
- nenhuma leitura nos últimos 30 dias;
- nome sem indicação de tabela histórica.

A ação poderia aplicar uma tag de revisão ou marcar o ativo como `deprecated`, dependendo da política adotada pela organização.

## Sensibilidade da coluna para a tabela

A automação também pode elevar a classificação das colunas para o nível da tabela.

Por exemplo, se qualquer coluna possuir uma tag como:

```text
class.us_ssn
class.credit_card
class.email_address
```

uma regra pode atribuir uma tag de sensibilidade à tabela inteira.

Isso ajuda processos de descoberta e revisão. Entretanto, não significa que a automação detectará dados sensíveis diretamente. A identificação das colunas depende da Data Classification ou de tags previamente existentes.

## O dry run reduz o risco

Toda nova automação começa com um dry run.

Essa execução mostra quais ativos seriam encontrados, mas não adiciona nem remove tags.

O administrador pode revisar:

- ativos correspondentes;
- abrangência das condições;
- resultados inesperados;
- permissões envolvidas;
- impacto da ação configurada.

Somente depois da revisão a automação é habilitada.

Na minha visão, essa etapa é fundamental. Uma regra de governança incorreta aplicada em escala pode ser tão prejudicial quanto a ausência de tags.

## Permissões necessárias

A criação da automação exige, no catálogo definido como escopo:

- `USE CATALOG`;
- `USE SCHEMA`;
- `APPLY TAG`;
- `MANAGE`.

O responsável também precisa de `ASSIGN` para todas as governed tags que a automação adicionará ou removerá.

Um detalhe importante é que essas permissões são verificadas no nível do catálogo. Limitar a regra a determinados schemas não reduz os privilégios exigidos.

Eu evitaria concentrar essas permissões em usuários individuais. Preferiria grupos administrativos específicos, com responsabilidade documentada e revisão periódica dos acessos.

## Limitações do Beta

A versão atual possui limites importantes:

- cada automação atua somente sobre tabelas ou somente sobre volumes;
- o escopo fica restrito a um único catálogo;
- não é possível selecionar tipos específicos de tabela;
- resultados recorrentes normalmente aparecem em até 24 horas;
- não existem gatilhos personalizados ou baseados em eventos;
- escopo e ação não podem ser alterados após a criação;
- cada execução processa até 500 ativos correspondentes;
- cada automação pode adicionar ou remover no máximo cinco tags.

Também é necessário considerar que a automação abrange todos os tipos de tabela dentro do escopo, incluindo managed, external, views, materialized views, streaming tables e foreign tables.

## Cuidado com informações sensíveis

As tags são armazenadas como texto simples e podem ser replicadas globalmente.

Por isso, nomes e valores de tags não devem conter:

- dados pessoais;
- credenciais;
- informações confidenciais;
- identificadores sensíveis;
- detalhes que possam comprometer a segurança do recurso.

A tag deve representar uma classificação, e não armazenar o conteúdo sensível que motivou essa classificação.

## Automação não elimina governança humana

A possibilidade de escrever a regra em linguagem natural com o Genie facilita a configuração, mas não transfere a responsabilidade pela decisão.

Eu ainda definiria:

- proprietário de cada automação;
- justificativa para a regra;
- frequência de execução;
- processo de aprovação;
- procedimento de rollback;
- revisão periódica dos resultados;
- alertas para alterações inesperadas.

Automatizar tags pode reduzir divergências e trabalho manual. Mas o verdadeiro ganho aparece quando as regras refletem uma política de governança clara e verificável.

Sua organização consegue manter as tags atualizadas ou elas ficam obsoletas pouco depois de serem criadas?

#AzureDatabricks #UnityCatalog #DataGovernance #DataEngineering

## Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Automatizar a atribuição de tags](https://learn.microsoft.com/en-us/azure/databricks/admin/governed-tags/automate-tag-assignment)
- [Governed tags no Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/admin/governed-tags/)
- [Classificações de versões do Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types)

## Texto para “Conte para sua rede”

> Criar tags é fácil. O difícil é mantê-las corretas enquanto os dados e metadados continuam mudando.
>
> O Azure Databricks anunciou Tag Automations, permitindo aplicar ou remover governed tags em tabelas e volumes conforme regras de propriedade, utilização, descrição, sensibilidade e atualização.
>
> No artigo, explico o dry run, as permissões exigidas e as limitações atuais do Beta.
>
> As tags do seu ambiente permanecem atualizadas ou se tornam obsoletas com o tempo?
>
> #AzureDatabricks #UnityCatalog #DataGovernance

## Orientação visual

A capa final foi corrigida para representar uma automação exclusiva de tabelas, respeitando a limitação atual do recurso. Ela apresenta:

- tabelas como ativos de entrada;
- condições determinísticas;
- etapa de dry run;
- aplicação das governed tags;
- exemplos `Certified`, `Deprecated` e `Sensitivity`;
- selo `Beta — 7 ago. 2026`;
- proporção horizontal 1,91:1 e margens seguras.
