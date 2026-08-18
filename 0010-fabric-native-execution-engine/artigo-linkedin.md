## 1. Resumo da pauta

### Tema escolhido

**Native Execution Engine do Microsoft Fabric agora acelera Python UDFs, Scala UDFs e tipos complexos.**

Não encontrei uma novidade oficial suficientemente forte publicada em 10 ou 11 de agosto. Por isso, a pauta utiliza a atualização relevante mais recente ainda não abordada, sem apresentá-la como lançamento do dia.

Em **julho de 2026**, o suporte do Native Execution Engine a UDFs e tipos complexos passou para **Generally Available** no Fabric Data Engineering.

### Status e disponibilidade

| Componente | Status |
|---|---|
| Suporte nativo a Python UDFs | GA |
| Suporte nativo a Scala UDFs | GA |
| Suporte a `ARRAY`, `MAP` e `STRUCT` | GA |
| Fabric Runtime 1.3 — Spark 3.5 | GA e recomendado atualmente para produção |
| Fabric Runtime 2.0 — Spark 4.1 | Public Preview |
| Structured Streaming no Native Engine | Não suportado |
| Fallback automático para a JVM | Disponível para operações incompatíveis |

A aceleração não fica ativa apenas porque o suporte é GA. O Native Execution Engine precisa estar habilitado no ambiente, notebook ou Spark Job Definition.

### Fontes primárias

- [Microsoft Fabric — novidades](https://learn.microsoft.com/en-us/fabric/fundamentals/whats-new)
- [Native Execution Engine no Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-overview)
- [UDFs e tipos complexos no Native Execution Engine](https://learn.microsoft.com/en-us/fabric/data-engineering/native-execution-engine-udf-complex-types)
- [Runtimes Apache Spark no Fabric](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime)
- [Fabric Runtime 2.0](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime-2-0)

---

## 2. Artigo final para LinkedIn

# O Spark do Fabric ficou mais nativo — mas o fallback para a JVM ainda precisa ser monitorado

Python UDFs, Scala UDFs e estruturas aninhadas estão presentes em muitos pipelines Spark.

Também são pontos frequentes de perda de desempenho.

Uma consulta pode começar em execução colunar, encontrar uma operação incompatível e retornar ao caminho tradicional da JVM. O resultado continua correto, mas parte do ganho esperado desaparece.

Em julho de 2026, o Microsoft Fabric tornou geralmente disponível o suporte do Native Execution Engine a Python UDFs, Scala UDFs e tipos complexos.

A mudança amplia o conjunto de workloads que pode utilizar execução vetorizada sem exigir a reescrita dos notebooks e jobs existentes.

Mas “sem alterar o código” não significa “todo o código será acelerado”.

## O que é o Native Execution Engine

O Native Execution Engine, ou NEE, é o mecanismo de execução vetorizada utilizado pelo Fabric Data Engineering para workloads Apache Spark.

Ele utiliza componentes como Apache Gluten e Velox para deslocar operadores compatíveis do caminho tradicional baseado na JVM para uma execução colunar em C++.

O Spark continua responsável por:

- analisar o código;
- criar o plano lógico;
- otimizar o plano físico;
- distribuir o processamento;
- coordenar estágios e tarefas.

A diferença está na execução dos operadores compatíveis.

Em vez de processar os dados predominantemente no caminho tradicional da JVM, o NEE pode utilizar operações vetorizadas, processamento colunar e instruções SIMD.

A integração preserva recursos importantes do Spark, como:

- Adaptive Query Execution;
- column pruning;
- predicate pushdown;
- otimizações baseadas em custo;
- leitura de arquivos Parquet e tabelas Delta.

## O que mudou para as UDFs

Antes dessa ampliação, uma UDF podia interromper parte da execução nativa e provocar a volta ao mecanismo tradicional.

O suporte GA contempla:

- Python Scalar UDFs;
- Pandas UDFs vetorizadas;
- Scala UDFs;
- operações compatíveis ao redor dessas funções.

As Pandas UDFs tendem a se beneficiar mais porque já trabalham com lotes colunares e Apache Arrow.

Um exemplo simples permanece igual:

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

@pandas_udf("double")
def apply_discount(value: pd.Series) -> pd.Series:
    return value * 0.90

result = (
    spark.table("sales.orders")
         .withColumn(
             "discounted_amount",
             apply_discount("order_amount")
         )
)
```

Não é necessário criar uma API de UDF específica para o Native Execution Engine.

Depois que o NEE está habilitado, o Fabric tenta executar os componentes compatíveis pelo caminho nativo.

Entretanto, a função Python não é magicamente convertida em C++. O ganho vem da redução de transições desnecessárias, do transporte colunar e da execução nativa dos operadores compatíveis que participam do plano.

Bibliotecas que dependem de serialização arbitrária de objetos Python ainda podem provocar fallback.

## Tipos complexos entram no caminho nativo

O suporte também foi ampliado para:

- `ARRAY`;
- `MAP`;
- `STRUCT`;
- combinações aninhadas compatíveis.

Entre as operações documentadas estão:

```text
explode
array_contains
size
flatten
transform
map_keys
map_values
element_at
getField
```

Isso é importante para pipelines que trabalham com:

- eventos de aplicações;
- telemetria;
- informações de dispositivos;
- atributos de produtos;
- documentos aninhados;
- estruturas provenientes de APIs;
- dados de IoT.

Antes, equipes podiam achatar documentos principalmente para evitar penalidades de execução.

Agora, estruturas hierárquicas compatíveis podem permanecer em seu formato natural por mais tempo, sem abandonar automaticamente o caminho nativo.

Ainda assim, estruturas profundamente aninhadas, como arrays de maps contendo structs, podem apresentar operações não suportadas e retornar à JVM.

## Como habilitar

O Native Execution Engine pode ser configurado no ambiente ou diretamente no notebook e no Spark Job Definition.

Em um notebook:

```python
%%configure
{
  "conf": {
    "spark.native.enabled": "true"
  }
}
```

Essa configuração deve ser colocada no início da execução.

Uma vez habilitado o mecanismo, o suporte a UDFs e tipos complexos não exige uma segunda configuração.

Isso não quer dizer que todos os operadores do plano serão executados nativamente. O Fabric avalia a compatibilidade durante a execução.

## O fallback evita falhas, mas pode esconder desempenho perdido

Quando um operador não é suportado pelo NEE, o Spark retorna automaticamente à execução tradicional baseada na JVM.

Esse comportamento é importante para compatibilidade: o pipeline não precisa falhar simplesmente porque determinada operação não possui implementação nativa.

O problema é operacional.

Um notebook pode continuar entregando o resultado correto e, ao mesmo tempo:

- executar mais lentamente;
- consumir mais capacidade;
- aumentar a duração de estágios;
- realizar conversões entre formatos;
- perder parte da vetorização;
- apresentar variações entre versões.

Por isso, eu não consideraria suficiente apenas habilitar:

```text
spark.native.enabled = true
```

Também verificaria quanto do plano foi realmente executado pelo mecanismo nativo.

## Como confirmar a execução

O primeiro recurso é o plano físico:

```python
result.explain("formatted")
```

No plano, elementos como estes ajudam a identificar a execução nativa:

```text
Transformer
NativeFileScan
VeloxColumnarToRowExec
```

O Fabric também disponibiliza informações na Spark UI e no Spark History Server.

Na visualização do plano:

- verde identifica operadores executados pelo Native Execution Engine;
- azul-claro identifica execução pelo mecanismo JVM;
- transições mostram os pontos de fallback.

A página `Gluten SQL / DataFrame` permite inspecionar quantos nós do plano foram executados de maneira nativa e quantos voltaram para a JVM.

Essa observabilidade deve fazer parte do teste de desempenho, principalmente em notebooks que utilizam UDFs ou transformações aninhadas.

## Limitações atuais

A disponibilidade geral não elimina as restrições do mecanismo.

### Structured Streaming

O Native Execution Engine ainda não suporta Structured Streaming.

Um pipeline pode utilizar Spark normalmente, mas não receberá a aceleração nativa nessa parte do processamento.

### Formatos de arquivo

O NEE acelera principalmente workloads sobre:

- Parquet;
- Delta;
- CSV pelo parser vetorizado mais recente.

Leituras diretas de JSON e XML retornam ao mecanismo JVM.

Isso reforça uma prática conhecida: ingerir o formato bruto e convertê-lo para Delta antes de executar transformações analíticas repetidas.

### ANSI SQL

No Runtime 1.3, baseado em Spark 3.5, o modo ANSI não é suportado pelo NEE. Quando habilitado, a execução volta ao Spark tradicional.

No Runtime 2.0, baseado em Spark 4.1, o modo ANSI recebe suporte no caminho nativo. Entretanto, o Runtime 2.0 permanece em Public Preview e não deve ser tratado como a opção padrão de produção.

### Comparações de datas

Os dois lados de uma comparação devem possuir tipos compatíveis.

Em vez de depender de conversões implícitas:

```sql
WHERE order_date = '2026-08-11'
```

eu preferiria tornar o tipo explícito:

```sql
WHERE CAST(order_date AS DATE) = DATE '2026-08-11'
```

Incompatibilidades podem impedir a aceleração, mesmo que a consulta continue correta.

## GA não torna o Runtime 2.0 GA

Essa distinção é importante.

O suporte do Native Execution Engine a UDFs e tipos complexos está GA.

O Fabric Runtime 1.3, com Apache Spark 3.5, também está GA e continua sendo a recomendação atual da Microsoft para produção.

Já o Runtime 2.0, com Spark 4.1, permanece em Public Preview.

Portanto, não é correto concluir que todos os recursos e correções disponíveis no Runtime 2.0 estejam prontos para workloads críticos.

Eu separaria as validações:

- produção no Runtime 1.3;
- laboratório de compatibilidade no Runtime 2.0;
- comparação de resultados entre JVM e NEE;
- teste de bibliotecas e dependências;
- validação de comportamento ANSI;
- análise de regressões do plano.

## E o ganho de desempenho?

A Microsoft apresenta benchmarks de até seis vezes mais desempenho em determinados cenários TPC-DS, com potencial de redução de aproximadamente 83% no consumo computacional de um cluster fixo.

Esses são números de benchmark do fornecedor.

Não representam uma expectativa universal.

O ganho depende de:

- formato dos dados;
- operadores utilizados;
- porcentagem nativa do plano;
- quantidade de fallback;
- volume processado;
- seletividade dos filtros;
- custo das UDFs;
- distribuição das partições;
- tamanho dos arquivos;
- configuração da capacidade.

Em conjuntos pequenos, o custo de inicialização e distribuição do Spark também pode superar o benefício do processamento nativo.

Eu utilizaria o benchmark apenas como justificativa para testar, não como estimativa financeira pronta.

## Como eu avaliaria em produção

Eu selecionaria notebooks representativos de três grupos:

1. SQL e DataFrames sem UDF;
2. Pandas e Python UDFs;
3. estruturas aninhadas com arrays, maps e structs.

Para cada workload, compararia:

- duração total;
- duração por estágio;
- capacidade consumida;
- volume lido;
- quantidade de shuffle;
- operadores nativos;
- pontos de fallback;
- consistência dos resultados;
- comportamento em cargas concorrentes.

Também manteria um conjunto de testes de regressão.

Uma atualização do Runtime pode ampliar o suporte nativo, mas também modificar bibliotecas, dependências e planos físicos.

## Sem reescrita não significa sem engenharia

A ampliação do Native Execution Engine é relevante porque reduz a necessidade de alterar código apenas para alcançar o caminho vetorizado.

Python UDFs, Scala UDFs e tipos complexos deixam de representar automaticamente uma barreira para a execução nativa.

Mas o ganho não deve ser presumido.

O pipeline precisa ser medido, o plano precisa ser inspecionado e o fallback precisa ser acompanhado.

Na minha visão, o principal avanço não é apenas o suporte a mais operadores.

É a possibilidade de otimizar workloads Spark existentes sem substituir a API, abandonar os notebooks ou reconstruir a arqu
