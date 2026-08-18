## Artigo final para o LinkedIn

# O Data Lake agora precisa armazenar contexto para agentes de IA

Durante anos, a principal função de um Data Lake foi armazenar grandes volumes de dados com flexibilidade e baixo custo.

Arquivos Parquet, JSON, CSV, imagens, documentos e logs eram preservados em sua forma original. Depois, pipelines, catálogos e aplicações ficavam responsáveis por descobrir o que cada objeto representava.

Esse modelo funcionava quando o principal consumidor era um engenheiro, analista ou processo previamente programado.

Com agentes de IA, a exigência muda.

Um agente não precisa apenas encontrar um arquivo ou consultar uma tabela. Ele precisa compreender:

- o significado do dado;
- sua origem e qualidade;
- as relações com outros ativos;
- as regras de negócio;
- as permissões de acesso;
- a finalidade adequada para sua utilização.

O Data Lake está deixando de armazenar apenas dados.

Agora, sua arquitetura também precisa armazenar, governar e entregar contexto.

Quatro movimentos ajudam a compreender essa transformação:

- Amazon S3 Annotations;
- Databricks Unity Catalog;
- Google Cloud Knowledge Catalog;
- Microsoft OneLake com Fabric IQ.

Essas soluções não são produtos perfeitamente equivalentes. Cada uma aborda o contexto em uma camada diferente da arquitetura.

## O problema do dado sem contexto

Considere um arquivo chamado:

```text
customer_revenue_final_v3.parquet
```

O nome informa pouco.

Antes de utilizá-lo, um agente precisaria descobrir:

- o que “receita” significa nesse conjunto;
- se os valores são brutos ou líquidos;
- qual moeda foi utilizada;
- se cancelamentos foram descontados;
- quem é o proprietário;
- quando os dados foram atualizados;
- quais colunas contêm informações pessoais;
- se esse é o ativo oficial;
- quais filtros e regras devem ser aplicados.

Sem essas informações, o agente pode localizar o arquivo tecnicamente correto e ainda produzir uma resposta incorreta.

O contexto deixa de ser apenas documentação complementar. Ele passa a fazer parte da infraestrutura de confiabilidade da IA.

## AWS: contexto anexado diretamente ao objeto

O Amazon S3 Annotations permite anexar payloads de metadados a objetos armazenados no S3 sem modificar ou reenviar o conteúdo original.

Uma anotação pode armazenar dados estruturados em JSON, XML ou YAML:

```json
{
  "business_domain": "finance",
  "data_product": "monthly_revenue",
  "certification": "approved",
  "business_definition": "Net revenue after cancellations",
  "allowed_uses": ["analytics", "forecasting"],
  "owner": "finance-data-team"
}
```

Cada versão de um objeto pode possuir até mil anotações. Cada anotação aceita de 1 byte a 1 MiB, permitindo chegar a aproximadamente 1 GiB de contexto por versão de objeto.

As anotações podem armazenar:

- descrições de negócio;
- classificações geradas por IA;
- entidades extraídas de documentos;
- embeddings;
- resultados de processamento;
- registros de conformidade;
- informações de qualidade;
- linhagem e auditoria;
- instruções para aplicações e agentes.

O conteúdo pode ser atualizado ou removido independentemente do arquivo original.

Com o S3 Metadata, as anotações também podem ser disponibilizadas em tabelas Apache Iceberg gerenciadas e consultadas com serviços como o Athena.

A principal vantagem está na proximidade entre o contexto e o objeto físico.

Entretanto, o S3 Annotations não é, isoladamente, um catálogo semântico corporativo. A organização ainda precisa definir:

- esquemas padronizados;
- vocabulários;
- produtores autorizados;
- processos de validação;
- níveis de confiança;
- mecanismos de descoberta;
- políticas de atualização.

A AWS oferece uma capacidade poderosa para armazenar contexto junto ao objeto. Transformar esse contexto em conhecimento corporativo confiável ainda depende da arquitetura construída ao redor dele. [Documentação do S3 Annotations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/annotations-overview.html)

## Databricks: governança e semântica no lakehouse

O Unity Catalog opera em uma camada diferente.

Em vez de concentrar a proposta em payloads anexados a arquivos individuais, ele organiza e governa ativos de dados e IA dentro do lakehouse, incluindo:

- catálogos, schemas e tabelas;
- volumes e arquivos;
- views e Metric Views;
- dashboards;
- funções e ferramentas;
- modelos;
- aplicações;
- agentes;
- servidores MCP.

O contexto é construído por descrições, tags, domínios, propriedade, classificações, linhagem, métricas, relacionamentos e controles de acesso.

As Metric Views acrescentam uma camada semântica ao permitir a definição centralizada de:

- medidas;
- dimensões;
- filtros;
- relacionamentos;
- regras de agregação;
- nomes de exibição;
- formatos;
- sinônimos.

Uma medida chamada `net_revenue`, por exemplo, pode ser acompanhada de metadados como:

```yaml
display_name: "Receita líquida"
synonyms:
  - faturamento líquido
  - vendas líquidas
  - receita após cancelamentos
```

Esses metadados ajudam ferramentas de linguagem natural, como os Genie Agents, a relacionar a pergunta do usuário ao conceito correto.

A principal vantagem do Unity Catalog está na proximidade entre:

- os dados;
- a semântica;
- as permissões;
- a linhagem;
- o mecanismo de consulta;
- os modelos e agentes consumidores.

O agente não encontra apenas uma tabela. Ele pode encontrar um ativo governado, com identidade, definição, propriedade e regras compartilhadas.

O limite é que o contexto disponível continua dependendo dos ativos integrados e dos metadados cadastrados ou inferidos. Parte importante do conhecimento empresarial pode permanecer espalhada em documentos, sistemas SaaS, códigos e pessoas. [Metadados para agentes nas Metric Views](https://docs.databricks.com/aws/en/uc-semantics/agent-metadata)

## Google Cloud: um mecanismo corporativo de contexto

O Google Cloud Knowledge Catalog se apresenta de maneira mais explícita como um mecanismo de contexto para agentes.

Ele agrega metadados provenientes de:

- serviços do Google Cloud;
- modelos semânticos;
- fontes externas;
- catálogos parceiros;
- dados estruturados;
- coleções de dados não estruturados.

Sua proposta pode ser compreendida em três etapas:

1. agregação;
2. enriquecimento;
3. pesquisa e recuperação.

A agregação reúne metadados técnicos e semânticos distribuídos pela organização.

O enriquecimento utiliza schemas, consultas, linhagem, modelos de BI e conteúdo não estruturado para gerar descrições, classificações e relações.

A recuperação permite que aplicações e agentes encontrem contexto por meio de pesquisa semântica, APIs e ferramentas MCP.

Em vez de retornar apenas o identificador de uma tabela, o catálogo pode entregar um bloco de contexto preparado para utilização por modelos, contendo:

- finalidade do ativo;
- campos e tipos;
- termos empresariais;
- relações com outros ativos;
- qualidade;
- linhagem;
- consultas confiáveis;
- regras e orientações de utilização.

A proposta é construir um grafo dinâmico de contexto que represente os dados e seus significados dentro da organização.

Sua principal vantagem é a abrangência corporativa. O desafio também está nessa amplitude.

Quanto mais fontes são agregadas, maior é a necessidade de controlar:

- definições conflitantes;
- atualização dos metadados;
- qualidade do enriquecimento automático;
- proveniência;
- permissões herdadas;
- custos de processamento;
- autoridade de cada fonte.

O catálogo deixa de ser apenas um inventário e passa a atuar como uma camada de recuperação para agentes. [Visão geral do Knowledge Catalog](https://docs.cloud.google.com/dataplex/docs/introduction), [Knowledge Catalog para agentes](https://docs.cloud.google.com/dataplex/docs/ai-overview)

## Microsoft: do OneLake ao modelo operacional do negócio

No ecossistema Microsoft, o contexto não fica concentrado em um único produto.

A arquitetura reúne diferentes componentes:

- OneLake como base unificada de dados;
- OneLake Catalog para descoberta;
- Microsoft Purview para governança, qualidade e conformidade;
- Fabric IQ para contexto empresarial;
- Fabric Data Agents e Microsoft Foundry para consumo pelos agentes.

O OneLake unifica dados do Fabric, de ambientes locais e de outras nuvens por meio de recursos como shortcuts e mirroring.

Sobre essa base, o Fabric IQ combina modelos semânticos e ontologias para criar uma camada compartilhada de contexto empresarial.

Uma ontologia pode representar:

- clientes;
- produtos;
- lojas;
- equipamentos;
- pedidos;
- propriedades dessas entidades;
- relacionamentos;
- regras empresariais;
- ações permitidas;
- vínculos com as fontes físicas no OneLake.

Com isso, o agente deixa de enxergar somente tabelas, colunas e registros.

Ele passa a raciocinar sobre conceitos e relações do negócio.

Por exemplo, uma tabela de vendas, uma tabela de clientes e um fluxo de eventos podem ser apresentados ao agente como uma estrutura conectada:

```text
Cliente → realiza → Pedido
Pedido → contém → Produto
Pedido → pertence → Loja
Produto → possui → Estoque
```

A mesma ontologia pode fundamentar diferentes experiências:

- Fabric Operations Agent;
- Fabric Data Agent;
- Foundry IQ;
- Copilot Studio;
- agentes personalizados conectados por MCP.

O Microsoft Purview complementa essa arquitetura com catalogação, domínios de governança, produtos de dados, classificação, qualidade, controles e conformidade.

A distinção é importante: o Purview governa o patrimônio de dados, enquanto a Ontology do Fabric IQ cria um modelo compartilhado que pode ser utilizado no raciocínio e nas ações dos agentes.

A proposta da Microsoft talvez seja a demonstração mais explícita de que metadados técnicos não são suficientes. Agentes também precisam de entidades, relacionamentos e regras operacionais.

A Ontology do Fabric IQ, entretanto, continua em Preview. Isso exige cautela antes de utilizá-la como dependência crítica em produção. [Visão geral do Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview), [Ontology no Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview), [integração com agentes](https://learn.microsoft.com/en-us/fabric/iq/ontology/concepts-agent-integration)

## Quatro estratégias para disponibilizar contexto

| Plataforma | Solução analisada | Estratégia principal |
|---|---|---|
| AWS | S3 Annotations | Anexa contexto estruturado diretamente ao objeto |
| Databricks | Unity Catalog | Governa dados, semântica, linhagem e ativos de IA |
| Google Cloud | Knowledge Catalog | Agrega, enriquece e recupera contexto corporativo |
| Microsoft | OneLake + Fabric IQ | Converte dados em entidades, relações, regras e ações |

Uma visão mais detalhada evidencia as diferenças:

| Critério | AWS | Databricks | Google Cloud | Microsoft |
|---|---|---|---|---|
| Unidade principal | Objeto e versão | Ativo de dados ou IA | Ativo e contexto relacionado | Entidade e processo do negócio |
| Proximidade com o arquivo | Muito alta | Alta no lakehouse | Variável | Alta no OneLake |
| Semântica empresarial | Definida pela aplicação | Metric Views e metadados | Glossários, aspectos e grafo de contexto | Semantic Models e Ontology |
| Linhagem | Registrada como anotação ou integração | Nativa na plataforma | Integrada ao catálogo | Fabric e Purview |
| Governança central | Parcial | Forte | Forte | Distribuída entre Fabric e Purview |
| Consumo por agentes | APIs e arquitetura própria | Genie e ecossistema Databricks | APIs, busca semântica e MCP | Fabric Agents, Foundry e MCP |
| Principal vantagem | Contexto junto ao objeto | Dados e IA sob a mesma governança | Contexto corporativo abrangente | Modelo operacional do negócio |
| Principal risco | Anotações sem padrão | Contexto limitado ao ambiente integrado | Conflitos entre múltiplas fontes | Complexidade entre componentes |

Não existe um vencedor absoluto porque as soluções atuam em camadas diferentes.

Uma arquitetura pode inclusive combinar estratégias semelhantes:

- o objeto carrega seu contexto
