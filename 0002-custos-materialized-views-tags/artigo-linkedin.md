Radar diário executado para a pauta de hoje, 4 de agosto de 2026. A novidade foi confirmada nas notas oficiais do Azure Databricks.

## Pauta validada

Em 3 de agosto de 2026, as atualizações de Materialized Views e Streaming Tables criadas no Databricks SQL passaram a herdar automaticamente as tags personalizadas do SQL Warehouse.

Essas tags são propagadas para `system.billing.usage`, permitindo associar o consumo ao projeto, equipe ou centro de custo responsável. A nota oficial não classifica a melhoria como Preview. [Azure Databricks — agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)

## Artigo pronto para o LinkedIn

# Custos de Materialized Views mais rastreáveis no Azure Databricks

Materialized Views e Streaming Tables facilitam a construção de pipelines declarativos. Entretanto, em ambientes compartilhados por diferentes equipes e projetos, ainda existe uma pergunta importante:

**Quem está gerando cada custo?**

Em 3 de agosto de 2026, o Azure Databricks anunciou uma melhoria que torna essa resposta mais acessível.

## O que mudou?

As atualizações de Materialized Views e Streaming Tables criadas no Databricks SQL agora herdam automaticamente as tags personalizadas do SQL Warehouse no qual estão configuradas.

Essas informações são propagadas para a coluna `custom_tags` da tabela:

```sql
system.billing.usage
```

Isso permite relacionar o consumo das atualizações serverless ao SQL Warehouse de origem, reduzindo a necessidade de procedimentos adicionais para identificar o responsável pelo custo.

## Por que essa mudança é importante?

Em organizações com múltiplos projetos, apenas conhecer o custo total do ambiente não é suficiente. É necessário identificar como esse consumo está distribuído.

Com as tags disponíveis nos registros de cobrança, torna-se mais fácil:

- atribuir DBUs a projetos e centros de custo;
- construir dashboards de FinOps;
- acompanhar o crescimento do consumo por equipe;
- definir budgets e alertas;
- investigar cargas com custo acima do esperado;
- aproximar engenharia, governança e gestão financeira.

Na minha visão, otimização de custos não começa somente ajustando clusters ou reescrevendo consultas. Ela começa garantindo que o consumo possa ser corretamente identificado.

## Como eu aplicaria essa melhoria?

Eu adotaria uma convenção mínima de tags nos SQL Warehouses:

- `environment`: produção, homologação ou desenvolvimento;
- `project`: nome do projeto;
- `team`: equipe responsável;
- `cost_center`: centro de custo;
- `owner`: área ou pessoa responsável.

Depois, acompanharia sua propagação em `system.billing.usage`:

```sql
SELECT
    usage_date,
    workspace_id,
    sku_name,
    custom_tags,
    SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY
    usage_date,
    workspace_id,
    sku_name,
    custom_tags
ORDER BY total_dbus DESC;
```

A consulta pode ser adaptada para produzir dashboards por projeto, ambiente, equipe ou centro de custo.

## Pontos de atenção

A melhoria está relacionada às atualizações de Materialized Views e Streaming Tables no Databricks SQL que possuem um SQL Warehouse de origem.

Ela não elimina a necessidade de:

- estabelecer uma convenção corporativa de tags;
- validar se os warehouses existentes estão corretamente identificados;
- controlar quem pode criar ou alterar tags;
- acompanhar registros sem classificação;
- revisar periodicamente a qualidade da atribuição financeira.

Também é importante diferenciar essa melhoria das serverless usage policies. Essas políticas oferecem outra forma de atribuir tags ao consumo serverless e permanecem em Public Preview. [Configuração de pipelines serverless](https://learn.microsoft.com/en-us/azure/databricks/ldp/serverless)

## Engenharia de dados também envolve responsabilidade financeira

Um pipeline pode estar tecnicamente correto e ainda gerar um custo difícil de explicar.

Ao propagar as tags do SQL Warehouse para os registros de cobrança, o Azure Databricks facilita a ligação entre arquitetura, operação e responsabilidade financeira.

É uma mudança pequena na interface da plataforma, mas relevante para ambientes que precisam amadurecer suas práticas de FinOps e governança.

Sua equipe já consegue atribuir com clareza os custos de cada pipeline ou o consumo ainda aparece de maneira agregada?

#AzureDatabricks #DataEngineering #FinOps #DataGovernance

## Referências oficiais

- [Azure Databricks — notas de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Monitoramento dos custos de computação serverless](https://learn.microsoft.com/en-us/azure/databricks/admin/system-tables/serverless-billing)
- [Configuração de pipelines serverless](https://learn.microsoft.com/en-us/azure/databricks/ldp/serverless)

## Texto para “Conte para sua rede”

> Materialized Views e Streaming Tables simplificam pipelines declarativos, mas identificar quem está gerando cada custo nem sempre é simples.
>
> Uma atualização do Azure Databricks passou a propagar as tags do SQL Warehouse para os registros de cobrança dessas atualizações.
>
> No artigo, explico o impacto dessa mudança e como ela pode apoiar FinOps, governança e atribuição de custos.
>
> Sua equipe já consegue identificar o custo de cada pipeline?
>
> #AzureDatabricks #DataEngineering #FinOps

## Capa horizontal

A versão final apresenta Materialized View e Streaming Table como fluxos paralelos e mostra as tags chegando corretamente a `system.billing.usage`.


A pauta já consta no histórico do radar e não será repetida como novidade nas próximas execuções.
