## 1. Resumo da pauta

### Tema escolhido

**AUTO CDC avança no Databricks com Partial Updates em GA e histórico bitemporal em Beta.**

Em **11 de agosto de 2026**, a Databricks publicou uma atualização do AUTO CDC voltada a problemas encontrados em pipelines reais:

- atualizações que contêm somente os campos alterados;
- eventos que chegam fora de ordem;
- reconstrução do histórico por tempo de negócio e tempo de sistema;
- auditabilidade que não depende da retenção física do Delta Lake.

### Status dos recursos

| Capacidade | Status |
|---|---|
| AUTO CDC para SCD Tipo 1 e Tipo 2 | Disponível no Lakeflow |
| Partial Updates | Generally Available |
| Bitemporal AUTO CDC | Beta |
| API Python do AUTO CDC Tipo 1 no Apache Spark 4.2 | Open source |
| Paridade completa do AUTO CDC no Spark open source | Ainda não disponível |

O Bitemporal AUTO CDC exige o canal `PREVIEW` e funciona em pipelines serverless ou nas edições Pro e Advanced. Por estar em Beta, não deve ser tratado como pronto para produção irrestrita.

### Fontes primárias

- [Databricks — anúncio de 11 de agosto de 2026](https://www.databricks.com/blog/taking-auto-cdc-next-level-solving-hardest-real-world-use-cases)
- [Azure Databricks — visão geral do AUTO CDC](https://learn.microsoft.com/en-us/azure/databricks/ldp/cdc)
- [Azure Databricks — tópicos avançados e modo bitemporal](https://learn.microsoft.com/en-us/azure/databricks/ldp/cdc-advanced)
- [Azure Databricks — referência SQL do AUTO CDC](https://learn.microsoft.com/en-us/azure/databricks/ldp/developer/ldp-sql-ref-apply-changes-into)
- [Apache Spark 4.2 — Declarative Pipelines](https://spark.apache.org/docs/latest/declarative-pipelines-programming-guide.html)

---

## 2. Artigo final para LinkedIn

# AUTO CDC avança no Databricks: atualizações parciais em GA e histórico bitemporal em Beta

Implementar Change Data Capture raramente termina no primeiro `MERGE`.

Depois dos inserts, updates e deletes, surgem os casos difíceis:

- eventos chegam fora de ordem;
- atualizações contêm somente os campos alterados;
- valores nulos podem significar coisas diferentes;
- correções retroativas modificam o histórico;
- auditorias exigem reconstruir o que o sistema sabia em determinada data.

Em 11 de agosto de 2026, a Databricks detalhou a expansão do AUTO CDC para lidar com parte desses desafios sem depender de grandes blocos de lógica imperativa.

A atualização combina duas capacidades com níveis diferentes de maturidade:

- Partial Updates, agora em disponibilidade geral;
- Bitemporal AUTO CDC, ainda em Beta.

Essa distinção é essencial antes de considerar adoção em produção.

## Por que substituir o MERGE manual

Um pipeline CDC tradicional precisa resolver várias questões separadamente:

- identificar a chave do registro;
- ordenar os eventos;
- remover duplicidades;
- ignorar alterações atrasadas quando necessário;
- aplicar deletes;
- distinguir SCD Tipo 1 e Tipo 2;
- manter intervalos históricos;
- lidar com reprocessamentos;
- evitar resultados diferentes após uma nova tentativa.

O AUTO CDC leva essas decisões para uma definição declarativa.

Um fluxo SCD Tipo 2 pode ser definido assim:

```sql
CREATE OR REFRESH STREAMING TABLE customers_history;

CREATE FLOW apply_customer_cdc
AS AUTO CDC INTO customers_history
FROM STREAM(bronze.customer_changes)
KEYS (customer_id)
APPLY AS DELETE WHEN operation = 'DELETE'
SEQUENCE BY sequence_number
COLUMNS * EXCEPT (operation, sequence_number)
STORED AS SCD TYPE 2;
```

A declaração informa:

- qual é a origem;
- qual é a chave;
- como ordenar os eventos;
- como reconhecer deletes;
- quais colunas devem chegar ao destino;
- qual comportamento histórico deve ser mantido.

O pipeline assume a implementação operacional desse contrato.

## Partial Updates estão GA

Nem todas as fontes CDC enviam uma linha completa a cada atualização.

Considere o estado atual:

```text
(1, "A", 20)
```

A fonte envia:

```text
(1, NULL, 30)
```

Esse evento pode ter dois significados.

O primeiro é:

> substitua o campo de nome por `NULL` e altere o valor para 30.

O segundo é:

> o nome não foi enviado porque não mudou; altere somente o valor para 30.

Sem uma regra explícita, um pipeline pode transformar:

```text
(1, "A", 20)
```

em:

```text
(1, NULL, 30)
```

e apagar involuntariamente uma informação válida.

Com Partial Updates, o `NULL` pode ser interpretado como “não atualize esta coluna”, preservando o valor existente:

```text
(1, "A", 30)
```

Esse comportamento agora está em disponibilidade geral.

## Três formas de controlar a atualização

O AUTO CDC oferece três estratégias principais.

### Ignorar nulos em determinadas colunas

```sql
IGNORE NULL UPDATES ON (name, address)
```

Nessas colunas, um `NULL` recebido preserva o valor existente.

Isso é útil quando a fonte envia somente os campos alterados e representa atributos ausentes como nulos.

### Ignorar nulos em todas, exceto algumas

```sql
IGNORE NULL UPDATES ON * EXCEPT (status)
```

Nesse caso, o comportamento de atualização parcial é aplicado amplamente, mas a coluna `status` ainda aceita um `NULL` explícito.

### Informar as colunas alteradas por registro

```sql
COLUMNS TO UPDATE changed_columns
```

A coluna de controle contém um `ARRAY<STRING>` com os nomes que devem ser atualizados em cada evento.

Essa opção resolve uma ambiguidade importante: permite distinguir um atributo ausente de um atributo que deve receber explicitamente `NULL`.

Se `name` estiver na lista, o valor será aplicado mesmo quando for nulo. Se não estiver, o valor existente será preservado.

## NULL não é um contrato CDC

Na minha visão, esse é o principal cuidado ao adotar Partial Updates.

Interpretar `NULL` como “campo não informado” pode ser correto para determinada fonte, mas incorreto para outra.

Em bancos e APIs, `NULL` normalmente pode representar:

- valor desconhecido;
- valor removido;
- campo não aplicável;
- atributo não enviado;
- tentativa explícita de limpar o valor.

Por isso, eu não habilitaria `IGNORE NULL UPDATES` sem documentar o contrato do produtor.

Quando a fonte consegue informar quais campos foram alterados, `COLUMNS TO UPDATE` tende a ser mais preciso.

Também consideraria:

- testes para remoção explícita de valores;
- validação de campos obrigatórios;
- métricas de eventos parciais;
- quarentena para operações ambíguas;
- versionamento do contrato CDC.

Um recurso automático não consegue resolver uma semântica que a fonte nunca definiu.

## Dois tempos para a mesma história

O segundo avanço é o Bitemporal AUTO CDC.

Uma tabela SCD Tipo 2 normalmente registra quando determinado estado era válido. O modelo bitemporal adiciona outra dimensão: quando o sistema conheceu esse estado.

As duas linhas do tempo são:

- **tempo de negócio:** quando o fato era verdadeiro no mundo real;
- **tempo de sistema:** quando o fato foi recebido ou registrado pela plataforma.

Considere uma alteração válida a partir de 1º de agosto, mas recebida pelo pipeline em 5 de agosto.

Depois, em 10 de agosto, chega uma correção retroativa informando que o valor válido em 1º de agosto estava errado.

Perguntas diferentes podem exigir respostas diferentes:

- Qual é hoje a verdade corrigida sobre 1º de agosto?
- O que o sistema acreditava em 3 de agosto?
- Qual informação estava disponível no momento de determinada decisão?
- Quando a correção passou a fazer parte do sistema?

Uma única linha do tempo não responde corretamente a todas essas perguntas.

## Como o histórico bitemporal é armazenado

O AUTO CDC tradicional para SCD Tipo 2 utiliza:

```text
__START_AT
__END_AT
```

O modo bitemporal acrescenta:

```text
__SYSTEM_START_AT
__SYSTEM_END_AT
```

A configuração SQL utiliza os dois critérios:

```sql
CREATE OR REFRESH STREAMING TABLE customer_history;

CREATE FLOW apply_bitemporal_cdc
AS AUTO CDC INTO customer_history
FROM STREAM(bronze.customer_changes)
KEYS (customer_id)
SEQUENCE BY business_timestamp
SYSTEM SEQUENCE BY ingestion_timestamp
STORED AS BITEMPORAL;
```

A grafia correta é:

```sql
STORED AS BITEMPORAL
```

Não se utiliza `SCD TYPE BITEMPORAL`.

As colunas de sequência precisam utilizar tipos ordenáveis e não podem possuir valores nulos.

Quando uma correção atrasada afeta um intervalo já processado, o mecanismo reorganiza o histórico correspondente em vez de apenas anexar uma nova linha no final.

## Histórico lógico não é Time Travel

O histórico bitemporal também ajuda a separar dois conceitos frequentemente confundidos.

O Delta Lake Time Travel utiliza versões e arquivos históricos da tabela:

```sql
SELECT *
FROM customer_history
TIMESTAMP AS OF '2026-08-01';
```

Entretanto, esses arquivos não são permanentes.

Após o prazo de retenção, o `VACUUM` pode removê-los fisicamente. Uma consulta antiga que funcionava anteriormente pode deixar de ser resolvida.

No modelo bitemporal, o histórico relevante permanece armazenado como linhas atuais da tabela.

O `OPTIMIZE` pode reorganizar arquivos e o `VACUUM` pode remover arquivos antigos, mas os intervalos lógicos continuam presentes no conjunto de dados.

Isso é relevante para:

- auditoria;
- relatórios regulatórios;
- reprodução de decisões;
- investigação de incidentes;
- reconstrução de features usadas no treinamento de modelos.

Ainda assim, uma tabela bitemporal não substitui automaticamente políticas de retenção, imutabilidade e arquivamento exigidas por regulamentações específicas.

## Reprodução de dados para ML

Um uso interessante é registrar no MLflow as duas referências temporais utilizadas na criação do conjunto de treinamento:

```text
business_as_of = 2026-07-31T23:59:59Z
system_as_of   = 2026-08-05T10:30:00Z
```

Com isso, o conjunto pode ser reconstruído segundo:

- a validade do dado no negócio;
- o estado de conhecimento da plataforma naquele momento.

Essa estratégia é mais robusta que depender somente de uma versão física do Delta sujeita ao `VACUUM`.

Mas a reprodutibilidade ainda depende de outros componentes:

- código de transformação;
- versão das bibliotecas;
- parâmetros;
- fontes externas;
- modelo;
- ambiente de execução;
- permissões;
- qualidade histórica dos dados.

Bitemporalidade resolve a dimensão temporal do dado. Não resolve sozinha todo o ciclo de reprodução.

## O que está realmente GA

A atualização possui diferentes níveis de maturidade.

### Generally Available

Partial Updates estão GA.

Isso inclui mecanismos para:

- ignorar nulos em colunas determinadas;
- definir exceções;
- informar dinamicamente as colunas alteradas.

### Beta

O Bitemporal AUTO CDC permanece em Beta.

A Databricks informa como requisitos:

- pipeline serverless ou edição Pro/Advanced;
- canal do pipeline configurado como `PREVIEW`;
- `SEQUENCE BY`;
- `SYSTEM SEQUENCE BY`;
- colunas de sequência ordenáveis e não nulas.

Recursos Beta não devem ser interpretados como possuindo o mesmo compromisso de estabilidade de uma funcionalidade GA.

Eu começaria por um conjunto controlado, comparando o histórico produzido com resultados esperados antes de utilizá-lo em processos regulatórios.

## Limitações de combinação

O comando `COLUMNS TO UPDATE` não pode ser utilizado junto com `IGNORE NULL UPDATES`.

Ele também não é suportado em tabelas bitemporais.

Isso significa que os dois avanços anunciados não podem ser combinados livremente em todos os cenários.

Se a fonte exige:

- histórico com duas linhas do tempo;
- atualizações parciais diferentes em cada evento;
- aplicação explícita de valores nulos;

pode ser necessário normalizar os eventos antes do AUTO CDC ou aguardar uma ampliação do suporte.

A documentação precisa ser verificada contra o desenho exato, e não apenas contra o nome geral do recurso.

## E o Apache Spark 4.2?

A Databricks também começou a levar o AUTO CDC para o Apache Spark Declarative Pipelines.

A contribuição inicial inclui a API Python para AUTO CDC Tipo 1.

Segundo a publicação oficial:

- a interface SQL foi integrada ao branch principal para uma versão futura;
- SCD Tipo 2 completo c
