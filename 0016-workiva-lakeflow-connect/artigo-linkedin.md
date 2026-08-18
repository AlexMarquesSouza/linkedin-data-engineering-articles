## 1. Resumo da pauta

**Tema:** conector gerenciado do Workiva no Azure Databricks Lakeflow Connect
**Data do anúncio:** 14 de agosto de 2026
**Status:** **Beta**

A documentação não classifica o recurso como Private Preview ou Public Preview. O status oficial é **Beta**, com ativação pelo administrador na página **Previews**. Portanto, ainda não está em disponibilidade geral.

O conector ingere três conjuntos de dados:

| Tabela | Conteúdo | Modo |
|---|---|---|
| `activities` | Eventos da trilha de auditoria | Incremental |
| `users` | Usuários da organização | Snapshot completo |
| `roles` | Funções da organização | Snapshot completo |

O recurso utiliza OAuth 2.0 machine-to-machine e pode ser configurado pela interface, API, notebook ou Declarative Automation Bundles.

Fontes primárias:

- [Release notes de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Visão geral do conector Workiva](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva)
- [Referência das tabelas e schemas](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-reference)
- [Limitações oficiais](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-limits)

## 2. Artigo final para LinkedIn

# Workiva chega ao Lakeflow Connect: auditoria corporativa como pipeline governado

Trilhas de auditoria, usuários e funções corporativas podem deixar de depender de extrações manuais ou integrações mantidas inteiramente pela equipe de dados.

O novo conector gerenciado do Workiva no Azure Databricks Lakeflow Connect transforma essas informações em tabelas governadas pelo Unity Catalog.

O benefício não está apenas em movimentar dados. Está em criar uma base centralizada para auditoria, monitoramento de acessos e análise de atividades corporativas.

## O escopo real

O conector disponibiliza três tabelas no schema de origem `default`:

- `activities`;
- `users`;
- `roles`.

A tabela `activities` contém eventos da trilha de auditoria. Entre seus campos estão:

- identificador do evento;
- data e hora da atividade;
- resumo;
- resultado da operação;
- ação executada;
- responsável pela ação;
- objetos afetados;
- contexto da organização e do workspace.

Objetos aninhados, como `action`, `performer`, `targets`, `licenses` e `workspaceMemberships`, são ingeridos como colunas `VARIANT`.

Isso preserva a estrutura sem exigir que o conector antecipe toda a modelagem. Por outro lado, a equipe ainda precisa transformar esses objetos em entidades analíticas downstream.

## Incremental apenas para atividades

A tabela `activities` usa ingestão incremental baseada no campo `activityDateTime`.

Quando `start_datetime` não é configurado, a primeira execução carrega os eventos dos 365 dias anteriores. Eventos mais antigos ficam fora da carga inicial padrão.

As tabelas `users` e `roles` seguem um comportamento diferente: ambas são ingeridas como snapshots completos em todas as execuções.

Portanto, “conector incremental” não significa que todas as entidades usam processamento incremental.

Se a organização precisa reconstruir o histórico de usuários, licenças, associações e funções, será necessário acumular e comparar os snapshots em uma camada posterior.

## Sem SCD Tipo 2 nativo

O conector não oferece SCD Tipo 2.

A tabela de atividades é considerada append-only. Já os snapshots de usuários e funções representam o estado observado em cada atualização, sem manter automaticamente versões históricas.

Uma arquitetura possível seria:

```text
Workiva
   ↓
Lakeflow Connect
   ├── activities — incremental
   ├── users — snapshot
   └── roles — snapshot
           ↓
Camada bronze governada
           ↓
Spark Declarative Pipelines
   ├── normalização de VARIANT
   ├── histórico de usuários e funções
   ├── regras de qualidade
   └── indicadores de auditoria
```

Nesse desenho, a ingestão gerenciada resolve o acesso à fonte e a movimentação. A semântica histórica continua sendo responsabilidade do produto de dados.

## Autenticação para automação

A única autenticação suportada é OAuth 2.0 com client credentials, no modelo machine-to-machine.

A aplicação criada no Workiva precisa receber:

- `activity:read`, para a trilha de atividades;
- `organization:read`, para usuários e funções.

Não há suporte a usuário e senha, API key ou OAuth interativo U2M.

O client ID, o client secret e o identificador da organização são usados para criar uma conexão no Unity Catalog. Depois disso, usuários com `USE CONNECTION` podem criar pipelines sem receber acesso direto ao segredo.

Para produção, eu manteria:

- aplicação exclusiva para a integração;
- escopos mínimos;
- rotação planejada do client secret;
- separação entre conexões de desenvolvimento e produção;
- auditoria sobre quem possui `USE CONNECTION`.

## Engenharia como código

O pipeline pode ser criado pela interface, API ou notebook. Também há suporte a Declarative Automation Bundles.

Isso permite versionar:

- definição do pipeline;
- tabelas selecionadas;
- catálogo e schema de destino;
- configuração de `start_datetime`;
- job responsável pela frequência;
- ambientes de desenvolvimento, homologação e produção.

O suporte a Bundles é especialmente relevante para evitar que uma integração de auditoria dependa apenas de configurações manuais no workspace.

## Limitações importantes

O recurso ainda está em **Beta**. Eu não o trataria como substituto imediato de uma integração crítica sem piloto e estratégia de contingência.

As limitações incluem:

- somente três recursos do Workiva são disponibilizados;
- SCD Tipo 2 não é suportado;
- seleção de colunas e filtros de linhas por API não são suportados;
- alteração de tipo de dado não possui evolução automática;
- renomear uma coluna exige full refresh;
- novas colunas selecionadas após o início não recebem backfill automático;
- usuários e funções são sempre snapshots completos;
- o conector entrega dados brutos, sem transformações;
- renomear tabelas pode tornar o pipeline editável apenas por API;
- alertas de pipelines agendados são processados durante a atualização seguinte, não imediatamente.

O workspace também precisa ter Unity Catalog e compute serverless habilitados.

## Cuidados com evolução de schema

Novas colunas e colunas removidas possuem evolução automática. Alterações de tipo e renomeações não têm o mesmo tratamento.

A ressalva é importante: evolução automática não significa compatibilidade automática com todas as tabelas downstream.

Uma nova propriedade dentro de uma coluna `VARIANT`, por exemplo, pode não quebrar a ingestão, mas ainda pode exigir:

- atualização das consultas;
- novos testes de qualidade;
- revisão da camada semântica;
- adequação dos dashboards;
- análise de dados sensíveis recém-expostos.

Eu criaria contratos e testes na camada refinada, em vez de permitir que consumidores dependam diretamente do schema bruto.

## Aplicação em produção

Começaria com um piloto voltado a uma pergunta concreta:

- quais atividades falharam;
- quem realizou ações críticas;
- quais usuários permanecem ativos;
- quais funções estão atribuídas;
- quando ocorreu a última autenticação;
- quais mudanças precisam de revisão.

O piloto deveria medir:

- duração da carga inicial;
- volume diário de atividades;
- custo dos snapshots;
- atraso entre origem e destino;
- comportamento na rotação do segredo;
- consistência dos identificadores;
- mudanças de schema;
- qualidade das estruturas `VARIANT`;
- capacidade de reprocessamento.

Também separaria a tabela bruta de usuários das visões liberadas para análise, pois ela pode conter e-mail, identificador SAML, licenças e associações a workspaces.

## Minha avaliação profissional

Como engenheiro de dados, considero a novidade interessante porque aproxima compliance e engenharia de dados.

O conector reduz o trabalho necessário para autenticar, paginar e manter chamadas à API do Workiva. Além disso, coloca conexão, tabelas e permissões sob a governança do Unity Catalog.

Mas o valor real surgirá na arquitetura downstream.

Será necessário transformar estruturas `VARIANT`, construir histórico para snapshots, aplicar controles de acesso e definir indicadores que façam sentido para auditoria e gestão de riscos.

Eu usaria o Beta para validar o fluxo completo e os requisitos de governança. Para processos regulatórios ou evidências críticas, manteria uma alternativa documentada até que o recurso alcance maior maturidade.

Sua empresa já transforma trilhas de auditoria em produtos de dados ou elas ainda ficam isoladas dentro de cada plataforma?

#AzureDatabricks #LakeflowConnect #EngenhariaDeDados #GovernançaDeDados

### Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Workiva connector](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva)
- [Referência do conector](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-reference)
- [Criar pipeline de ingestão](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-pipeline)
- [Limitações do conector](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-limits)
- [Configuração do OAuth](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/workiva-source-setup)

## 3. Conte para sua rede qual é o tópico do seu artigo

Trilhas de auditoria também podem ser tratadas como produtos de dados.

O novo conector Workiva no Lakeflow Connect ingere atividades, usuários e funções para tabelas governadas no Azure Databricks. Porém, somente as atividades são incrementais; usuários e funções chegam como snapshots completos.

Como sua equipe centraliza e analisa os eventos de auditoria das plataformas corporativas?

#AzureDatabricks #LakeflowConnect #GovernançaDeDados

## 4. Orientação visual da capa

- **Dimensões:** 1920 × 1080 px.
- **Proporção:** 16:9.
- **Formato:** PNG em sRGB.
- **Fundo:** grafite com gradientes vinho e verde-petróleo.
- **Texto principal:** “WORKIVA NO LAKEFLOW CONNECT”.
- **Texto secundário:** “AUDITORIA GERENCIADA • BETA”.
- **Lado esquerdo:** documentos e trilha de eventos com relógio e validação.
- **Centro:** fluxo incremental de dados.
- **Lado direito:** três tabelas governadas e um escudo.
- **Margens seguras:** mínimo de 140 px.
- **Assinatura:** “Alex Marques | Engenharia de Dados”.
- **Paleta:** grafite, cobre, âmbar, verde-esmeralda e roxo.
- **Restrições:** sem logotipos, faixas brancas, molduras, marcas-d’água ou textos adicionais.

## 5. Imagem final

A capa foi revisada quanto à grafia, status Beta, legibilidade, coerência técnica e margens. O arquivo final está em PNG, sRGB e possui exatamente **1920 × 1080 px**.
