## 1. Resumo da pauta

### Tema escolhido

**VARIANT e Variant Shredding no Azure Databricks: flexibilidade para JSON com leitura colunar otimizada.**

O tipo `VARIANT` e o Variant Shredding tornaram-se **Generally Available em 22 de julho de 2026**. Em **3 de agosto de 2026**, a Databricks publicou uma explicação técnica ampliada sobre desempenho, integração e casos de uso.

O tema ainda não havia sido apresentado neste radar.

### Status e disponibilidade

- **Status:** disponibilidade geral — GA.
- `VARIANT` exige Databricks Runtime 15.4 LTS ou superior para tabelas Delta.
- O shredding automático em novas tabelas exige Databricks Runtime 17.3 ou superior.
- Para estatísticas sobre campos internos e data skipping, a recomendação é Databricks Runtime 18.1 ou superior.
- O anúncio original indicou um rollout separado para workspaces com Compliance Security Profile. A disponibilidade deve ser confirmada no workspace antes da implantação.
- No Delta Lake, habilitar `VARIANT` atualiza o protocolo da tabela e pode afetar leitores externos incompatíveis.
- Apache Iceberg v2 não aceita colunas `VARIANT`; o suporte está no Iceberg v3.

### Fontes primárias

- [Azure Databricks — notas de julho de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/july)
- [Databricks — anúncio técnico de 3 de agosto](https://www.databricks.com/blog/ingest-semi-structured-data-faster-and-more-efficiently-variant-now-generally-available)
- [Ingestão de dados como VARIANT](https://learn.microsoft.com/en-us/azure/databricks/ingestion/variant)
- [Variant Shredding](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant-shredding)
- [Compatibilidade com Delta Lake e Iceberg](https://learn.microsoft.com/en-us/azure/databricks/tables/features/variant)

---

## 2. Artigo final para LinkedIn

# JSON flexível sem condenar as consultas: VARIANT chega à disponibilidade geral no Azure Databricks

Dados semiestruturados sempre impuseram uma escolha difícil à engenharia de dados.

Podemos armazenar o JSON praticamente como chegou, preservando flexibilidade, mas pagando o custo da interpretação durante as consultas.

Ou podemos transformar cada campo em uma estrutura rígida, obtendo melhor desempenho, mas assumindo pipelines mais complexos e sensíveis às mudanças do produtor.

O `VARIANT`, agora em disponibilidade geral no Azure Databricks, tenta reduzir essa escolha.

Ele permite armazenar documentos semiestruturados preservando tipos, estruturas aninhadas e variações de schema. Com o Variant Shredding, os campos relevantes também podem ser organizados de maneira colunar nos arquivos Parquet.

A proposta não é abandonar a modelagem. É adiar parte dela com mais segurança e melhorar o desempenho enquanto o uso real dos dados é descoberto.

## O problema do JSON como string

Uma prática comum na camada de ingestão é armazenar todo o payload em uma coluna `STRING`.

Essa abordagem é simples e preserva o conteúdo original, mas apresenta consequências:

- os valores internos não mantêm tipos nativos;
- cada consulta precisa interpretar novamente o texto;
- filtros sobre campos internos podem exigir mais CPU;
- o mecanismo pode ler mais dados do que o necessário;
- estatísticas e data skipping ficam limitados;
- mudanças no formato precisam ser tratadas em funções de extração.

A alternativa tradicional é definir antecipadamente um `STRUCT`.

O desempenho tende a ser melhor, mas a ingestão fica mais dependente do schema. Se uma API mudar um campo de inteiro para texto ou passar a enviar novas estruturas aninhadas, o pipeline pode precisar de evolução de schema, tratamento de dados resgatados ou reprocessamento.

O `VARIANT` ocupa um espaço intermediário.

## O que o VARIANT armazena

`VARIANT` é um tipo destinado a dados semiestruturados.

Diferentemente de uma string contendo JSON, ele preserva a estrutura e os tipos dos valores internos.

Um registro pode ser ingerido desta forma:

```sql
CREATE TABLE bronze.api_events (
  ingestion_time TIMESTAMP,
  source STRING,
  payload VARIANT
);
```

Depois, um JSON pode ser convertido com `parse_json()`:

```sql
INSERT INTO bronze.api_events
SELECT
  current_timestamp(),
  'orders_api',
  parse_json(json_payload)
FROM landing.raw_events;
```

Os campos internos podem ser acessados com a notação de caminho:

```sql
SELECT
  payload:eventId::STRING AS event_id,
  payload:customer.id::BIGINT AS customer_id,
  payload:order.total::DECIMAL(18,2) AS order_total,
  payload:eventType::STRING AS event_type
FROM bronze.api_events;
```

Isso permite receber documentos com estruturas diferentes sem transformar cada atributo em uma coluna durante a chegada.

## Ingestão com Auto Loader

O Auto Loader pode armazenar o registro completo em uma única coluna `VARIANT` por meio da opção `singleVariantColumn`.

```python
(
    spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("singleVariantColumn", "payload")
        .load("/Volumes/landing/events/")
        .writeStream
        .option("checkpointLocation", "/Volumes/checkpoints/events/")
        .toTable("bronze.api_events")
)
```

Nesse modo, a ingestão não executa a evolução tradicional do schema para cada campo do documento.

Isso pode ser útil para:

- eventos de aplicações;
- respostas de APIs;
- telemetria e observabilidade;
- mensagens Kafka;
- documentos com muitos atributos opcionais;
- fontes schemaless;
- integrações com mudanças frequentes.

Existe, porém, uma ressalva: como o registro completo fica dentro de uma coluna `VARIANT`, a `rescuedDataColumn` não é utilizada nesse padrão.

Registros malformados também não podem ser codificados como `VARIANT`. Eles precisam ser encaminhados para tratamento de registros corrompidos.

## Como funciona o Variant Shredding

Armazenar um documento em formato binário estruturado melhora a manipulação, mas não resolve sozinho todo o custo das consultas.

É aí que entra o Variant Shredding.

O mecanismo identifica campos recorrentes dentro do `VARIANT` e os armazena separadamente na estrutura física dos arquivos Parquet.

Em termos simplificados, um documento como este:

```json
{
  "eventId": "E-901",
  "eventType": "purchase",
  "customer": {
    "id": 8402,
    "segment": "premium"
  },
  "timestamp": "2026-08-10T08:30:00Z"
}
```

continua sendo apresentado logicamente como um valor `VARIANT`, mas campos frequentemente utilizados podem receber representação colunar na camada física.

Isso produz dois benefícios principais:

- a consulta lê somente os campos necessários;
- valores semelhantes podem obter melhor compressão colunar.

Com estatísticas sobre esses campos, o mecanismo também pode evitar arquivos que não correspondem ao filtro.

A Databricks afirma ter medido leituras próximas de quatro vezes mais rápidas em relação ao `VARIANT` sem shredding e até 30 vezes mais rápidas que JSON armazenado como string.

Esses números são resultados divulgados pelo fornecedor. Não devem ser interpretados como garantia para qualquer pipeline.

O ganho real depende de:

- profundidade dos documentos;
- seletividade dos filtros;
- quantidade de campos acessados;
- repetição dos caminhos;
- distribuição dos valores;
- tamanho dos arquivos;
- versão do Runtime;
- perfil das consultas.

Eu validaria o benefício com dados e consultas representativos do ambiente antes de projetar capacidade ou justificar custos.

## Quando o shredding é automático

A partir do Databricks Runtime 17.3, novas tabelas criadas com colunas `VARIANT` habilitam o shredding automaticamente.

```sql
CREATE TABLE bronze.events (
  payload VARIANT
);
```

Isso não significa que qualquer alteração em uma tabela antiga ativa o recurso.

`CREATE OR REPLACE TABLE` e `ALTER TABLE` não habilitam o shredding automaticamente em tabelas existentes. A decisão precisa ser explícita:

```sql
ALTER TABLE bronze.events
SET TBLPROPERTIES (
  'delta.enableVariantShredding' = 'true'
);
```

A configuração afeta as novas gravações. Ela não converte automaticamente os dados existentes.

Para reescrever o histórico no formato otimizado:

```sql
REORG TABLE bronze.events
APPLY (SHRED VARIANT);
```

Essa operação deve ser tratada como uma reescrita de dados: precisa de planejamento de custo, duração, concorrência e janela operacional.

## Predictive Optimization e acesso aos campos

Nas Unity Catalog managed tables, o Predictive Optimization pode observar o padrão das consultas para identificar campos relevantes, coletar estatísticas e melhorar o data skipping.

Isso não elimina a necessidade de modelagem.

A própria documentação recomenda extrair atributos frequentemente consultados e armazená-los em colunas tipadas.

Uma estrutura híbrida costuma ser mais adequada:

```sql
CREATE TABLE bronze.events (
  event_id STRING,
  event_date DATE,
  source STRING,
  payload VARIANT
);
```

Nesse desenho:

- identificadores operacionais ficam tipados;
- a data pode apoiar filtros e manutenção;
- campos de governança permanecem explícitos;
- o payload completo preserva atributos variáveis.

Eu evitaria esconder dentro do `VARIANT` tudo aquilo que já possui significado estável e uso recorrente.

## VARIANT não substitui as camadas refinadas

A disponibilidade de um tipo flexível pode incentivar um erro arquitetural: manter indefinidamente todos os dados em documentos semiestruturados.

Para mim, o melhor uso está principalmente na borda da plataforma.

Na camada Bronze, o `VARIANT` ajuda a receber dados rapidamente e absorver mudanças do produtor.

Nas camadas Silver e Gold, os atributos relevantes ainda devem ser:

- validados;
- tipados;
- documentados;
- classificados;
- normalizados quando necessário;
- apresentados por contratos estáveis.

O `VARIANT` reduz o acoplamento da ingestão. Ele não elimina contratos de dados nem a necessidade de produtos confiáveis.

## Limitações importantes

Existem restrições que precisam entrar no desenho.

Uma coluna `VARIANT` não pode ser utilizada diretamente como:

- chave de particionamento;
- chave de liquid clustering;
- chave de Z-Order;
- expressão de `GROUP BY`;
- expressão de `ORDER BY`;
- entrada direta de `DISTINCT`;
- operando de `INTERSECT`, `UNION` ou `EXCEPT`.

Para essas operações, o valor necessário deve ser extraído e convertido para um tipo SQL apropriado.

Também existem limites por registro. Na ingestão com Auto Loader documentada atualmente, registros acima de 16 MB são tratados como corrompidos. A documentação geral registra limites diferentes conforme versão e caminho de processamento, chegando a 128 MiB nos Runtimes mais novos. Por isso, eu validaria o limite específico do método de ingestão utilizado.

O shredding também:

- adiciona algum custo às gravações;
- não reescreve automaticamente o histórico;
- atua sobre colunas `VARIANT` no nível superior ou dentro de `STRUCT`;
- não otimiza valores `VARIANT` armazenados dentro de arrays ou maps.

## Compatibilidade exige atenção

Em tabelas Delta existentes, habilitar `VARIANT` atualiza o protocolo da tabela.

Clientes externos precisam compreender o recurso para continuar lendo e gravando corretamente.

Antes da adoção, eu inventariaria:

- engines que consultam a tabela;
- versões dos conectores;
- leitores Delta externos;
- compartilhamentos existentes;
- ferramentas de BI;
- processos de exportação;
- requisitos de Iceberg.

O Apache Iceberg v2 não suporta colunas `VARIANT`. O suporte está presente no Iceberg v3.

A disponibilidade geral dentro do Databricks não significa compatibilidade universal em todo o ecossistema de dados.

## Onde eu utilizaria em produção

Eu começaria por fontes nas quais a variabilidade realmente representa custo operacional:

- APIs de terceiros;
- eventos de produtos digitais;
- telemetria;
- logs de segurança;
- integrações com MongoDB ou PostgreSQL JSON;
- payloads de aplicações independentes;
- documentos com muitos atributos esparsos.

A validação incluiria:

1. comparação entre JSON string, `STRUCT` e `VARIAN
