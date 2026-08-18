## Pauta de hoje: Metric Views agora suportam janelas sobre índices numéricos

Em **5 de agosto de 2026**, o Azure Databricks adicionou suporte a `offset`, `trailing` e `leading` numéricos nas window measures das Metric Views.

A melhoria permite calcular período anterior, médias móveis e comparações em calendários que não seguem datas convencionais, incluindo:

- semanas fiscais;
- calendários 4-4-5;
- períodos comerciais internos;
- sequências operacionais numeradas.

**Status:** window measures continuam classificadas como **Experimental**. Segundo a política oficial do Azure Databricks, recursos experimentais não são indicados para produção, não possuem SLA e podem sofrer alterações de interface. A novidade requer **Databricks Runtime 19 ou superior** e especificação **YAML 1.1 ou superior**. [Notas de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august) e [técnicas avançadas para Metric Views](https://learn.microsoft.com/en-us/azure/databricks/uc-semantics/metric-views/advanced-techniques)

## Artigo final para o LinkedIn

# Metric Views agora entendem calendários fiscais no Azure Databricks

Nem todo período importante para uma empresa começa no primeiro dia do mês ou termina em 31 de dezembro.

Varejo, finanças, logística e outras áreas frequentemente trabalham com semanas fiscais, calendários 4-4-5 e períodos internos que não podem ser representados corretamente apenas com operações sobre datas.

Em 5 de agosto de 2026, o Azure Databricks ampliou as window measures das Metric Views para permitir janelas ordenadas por índices numéricos consecutivos.

## O problema dos calendários não convencionais

Uma operação como:

```yaml
offset: -1 month
```

funciona quando o objetivo é acessar o mês civil anterior.

Entretanto, ela não representa necessariamente o período anterior em um calendário fiscal. Em um calendário 4-4-5, por exemplo, os períodos possuem quatro, quatro e cinco semanas.

A nova abordagem permite criar um índice numérico que represente a sequência real desses períodos:

| Período fiscal | Índice |
|---|---:|
| 2026-P01 | 101 |
| 2026-P02 | 102 |
| 2026-P03 | 103 |
| 2026-P04 | 104 |

A Metric View pode avançar ou retroceder nessa sequência, independentemente do calendário civil.

## Como funciona?

O índice é utilizado no campo `order` da window measure.

Um `offset` sem unidade movimenta a janela pela sequência numérica:

```yaml
- order: fiscal_period_index
  range: current
  offset: -1
  semiadditive: last
```

Nesse caso, `offset: -1` significa “posição anterior”, e não “um dia” ou “um mês atrás”.

Também é possível definir uma janela móvel:

```yaml
- order: fiscal_period_index
  range: trailing 3
  semiadditive: last
```

Por padrão, `trailing 3` considera as três posições anteriores e exclui o período atual. Para incluir o período atual, é necessário usar `trailing 3 inclusive`.

## Onde isso pode ser aplicado?

A capacidade atende cenários como:

- vendas do período fiscal atual versus o anterior;
- médias móveis em calendários 4-4-5;
- comparação entre ciclos produtivos;
- acompanhamento sequencial de lotes;
- métricas de semanas comerciais;
- indicadores sobre etapas operacionais numeradas.

A regra temporal fica centralizada na camada semântica, evitando que diferentes dashboards implementem versões próprias do mesmo cálculo.

## O índice precisa ser confiável

Este é o principal ponto de atenção.

Para produzir resultados corretos, a coluna utilizada como índice deve ser:

- integral: `TINYINT`, `SMALLINT`, `INT` ou `BIGINT`;
- monotônica;
- consecutiva e sem lacunas;
- compatível com a granularidade da comparação.

Um campo de semana fiscal que volta para `1` no início de cada ano não pode ser utilizado diretamente. É necessário construir uma sequência contínua que atravesse corretamente a mudança de ano.

Para calendários com anos de 52 ou 53 semanas, a documentação recomenda utilizar uma tabela calendário que associe cada período a um número inteiro denso. Uma fórmula simplista como `ano * 53 + semana` pode criar lacunas nos anos com apenas 52 semanas.

## O risco dos erros silenciosos

A documentação destaca uma limitação importante: o Databricks valida se o tipo da coluna é integral, mas não valida completamente se o índice é consecutivo e está alinhado à granularidade.

Isso significa que um índice com lacunas ou valores repetidos pode produzir números incorretos sem gerar uma exceção.

Na minha visão, esse comportamento exige controles explícitos de qualidade antes de usar o índice:

```sql
SELECT
    fiscal_period_index,
    COUNT(*) AS occurrences
FROM dim_fiscal_period
GROUP BY fiscal_period_index
HAVING COUNT(*) <> 1;
```

Eu também validaria a diferença entre cada índice e seu antecessor, garantindo que ela seja sempre igual a `1`.

## Ainda é um recurso experimental

Apesar da utilidade, as window measures estão classificadas como Experimental.

O recurso:

- não é recomendado para cargas de produção;
- não possui SLA;
- pode sofrer mudanças;
- exige Databricks Runtime 19+;
- exige YAML 1.1+.

Eu utilizaria a novidade inicialmente em protótipos e ambientes controlados, comparando os resultados com cálculos SQL já validados.

O recurso resolve um problema real de modelagem semântica. Mas, antes da adoção produtiva, a confiabilidade do índice e a maturidade da funcionalidade precisam ter o mesmo peso que a simplicidade da sintaxe.

Sua empresa trabalha apenas com o calendário civil ou também possui semanas e períodos fiscais próprios?

#AzureDatabricks #DataEngineering #MetricViews #DataModeling

## Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Técnicas avançadas para Metric Views](https://learn.microsoft.com/en-us/azure/databricks/uc-semantics/metric-views/advanced-techniques)
- [Disponibilidade dos recursos de Metric Views](https://learn.microsoft.com/en-us/azure/databricks/uc-semantics/metric-views/feature-availability)
- [Classificações de versões do Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types)

## Texto para “Conte para sua rede”

> Comparar períodos nem sempre significa voltar um mês no calendário.
>
> O Azure Databricks adicionou suporte a janelas com índices numéricos nas Metric Views, permitindo representar semanas fiscais, calendários 4-4-5 e outras sequências de negócio.
>
> No artigo, mostro como funciona, o risco dos índices com lacunas e por que o status Experimental ainda exige cautela.
>
> Sua empresa utiliza calendário civil ou períodos fiscais próprios?
>
> #AzureDatabricks #DataEngineering #MetricViews

## Orientação visual

A capa foi criada no formato horizontal **1,91:1**, mostrando:

- um calendário fiscal 4-4-5;
- sua transformação em índice consecutivo;
- o período anterior;
- uma janela móvel de três períodos;
- selo claramente identificado como `Experimental`;
- margens seguras e assinatura discreta.
