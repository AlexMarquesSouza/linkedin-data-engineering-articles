## 1. Resumo da pauta

Não há uma publicação oficial datada de 8 ou 9 de agosto nas notas consultadas. A atualização mais recente ainda não abordada pelo radar é a função SQL `ai_search()`, anunciada em **7 de agosto de 2026** no Azure Databricks.

**Status:** Beta.

Recursos Beta:

- ficam desativados por padrão e precisam ser habilitados por um administrador;
- não são recomendados para produção;
- não possuem SLA nem interface estável;
- podem não estar disponíveis imediatamente em todos os workspaces.

A função recebe uma consulta em linguagem natural, pesquisa até dez índices do Databricks AI Search configurados como fontes de conhecimento, deduplica e reranqueia os resultados. Por padrão, também produz uma resposta fundamentada nos documentos recuperados.

**Requisitos principais:**

- Databricks Runtime 18.2 ou superior;
- ambiente serverless versão 3 ou superior, quando usado;
- ao menos um índice do AI Search previamente criado;
- habilitação do recurso na página de previews.

Fontes: [notas de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august), [documentação da função ai_search](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_search) e [classificação dos releases](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types).

---

## 2. Artigo final para LinkedIn

# RAG em SQL no Azure Databricks: o que muda com ai_search()?

Construir um pipeline de RAG normalmente exige integrar busca, filtros, deduplicação, reranking e geração de respostas.

No Azure Databricks, parte desse fluxo agora pode ser executada a partir de uma única função SQL.

Em 7 de agosto de 2026, o Azure Databricks anunciou a função `ai_search()`, atualmente em Beta. Ela permite consultar índices do AI Search usando linguagem natural e utilizar os resultados em notebooks, jobs, workflows e pipelines.

## Da consulta aos documentos relevantes

A função recebe uma pergunta e uma lista de fontes de conhecimento.

Essas fontes precisam ser índices do Databricks AI Search previamente configurados. Atualmente, a função não pesquisa diretamente tabelas Delta, volumes ou documentos brutos.

Durante a execução, ela:

- transforma a pergunta em consultas de busca otimizadas;
- consulta um ou mais índices;
- deduplica resultados recuperados de fontes diferentes;
- aplica reranking por relevância;
- retorna os documentos mais relevantes;
- gera, por padrão, uma resposta fundamentada nesses documentos.

O resultado é um valor `VARIANT` com duas estruturas principais:

- `document`: documentos recuperados, metadados e URI da fonte;
- `answer`: resposta em linguagem natural baseada no conteúdo encontrado.

## Uma chamada SQL para diferentes cenários

A sintaxe principal é:

```sql
ai_search(
  query,
  knowledge_sources,
  instructions,
  options
)
```

Uma utilização possível seria enriquecer chamados de suporte com documentação relacionada:

```sql
SELECT
  ticket_id,
  ai_search(
    customer_description,
    PARSE_JSON('[{
      "type": "vector_search",
      "config": {
        "index_name": "support.docs.knowledge_base",
        "text_col": "content",
        "doc_uri_col": "document_url"
      }
    }]')
  ):answer::STRING AS suggested_resolution
FROM support.open_tickets;
```

Nesse exemplo, cada descrição é utilizada como consulta, e a resposta fundamentada pode ser incorporada ao resultado do processamento.

A função também pode ser usada em:

- enriquecimento de registros operacionais;
- classificação assistida por contexto;
- processamento em lote de perguntas;
- pipelines de RAG;
- ferramentas de recuperação para agentes;
- análise de incidentes e chamados.

Ela está disponível em notebooks, SQL Editor, Lakeflow Jobs, Workflows e Spark Declarative Pipelines.

## Mais de uma fonte de conhecimento

Uma chamada pode consultar até dez índices.

Isso permite combinar, por exemplo:

- documentação pública;
- base interna de suporte;
- políticas operacionais;
- catálogo de produtos;
- procedimentos de troubleshooting.

O argumento opcional `instructions` orienta a geração das consultas, os filtros de metadados e o reranking.

É possível solicitar que a função priorize documentação oficial ou determinados tipos de conteúdo. Entretanto, esse argumento possui limite de 4.000 caracteres.

## Resposta automática ou somente recuperação?

A geração da resposta fica habilitada por padrão.

Quando o objetivo é ter maior controle sobre o modelo, o formato ou as instruções de geração, a opção `generate_answer` pode ser definida como `false`.

Nesse caso, a função retorna somente os documentos recuperados. O conteúdo pode então ser enviado separadamente para `ai_query()` ou para outro componente do pipeline.

Na minha visão, essa separação é importante em soluções mais rigorosas. Ela permite avaliar individualmente:

- qualidade da recuperação;
- relevância do reranking;
- documentos utilizados;
- comportamento do modelo gerador;
- consistência da resposta final.

## Os índices continuam sendo uma dependência

A simplicidade da chamada SQL não elimina o trabalho necessário para preparar a base de conhecimento.

Antes de utilizar `ai_search()`, ainda é preciso:

- extrair o conteúdo dos documentos;
- dividir textos em partes adequadas;
- preservar metadados e URLs;
- criar o índice do AI Search;
- configurar embeddings quando aplicável;
- garantir que o índice esteja atualizado;
- definir permissões e governança.

Documentos brutos podem ser preparados com funções como `ai_parse_document()` e `ai_prep_search()`. Depois, os segmentos resultantes podem alimentar um índice criado sobre uma tabela Delta.

Se a fragmentação, os metadados ou o conteúdo do índice forem inadequados, a nova função apenas tornará mais simples consultar uma base de conhecimento ruim.

## O que eu validaria antes de escalar

Como engenheiro de dados, eu avaliaria o recurso em camadas.

Primeiro, mediria a recuperação:

- documentos relevantes entre os primeiros resultados;
- comportamento com termos técnicos e identificadores;
- qualidade dos filtros de metadados;
- duplicidade entre índices;
- rastreabilidade por meio de `doc_uri`.

Depois, avaliaria a resposta gerada:

- aderência aos documentos recuperados;
- presença de afirmações sem suporte;
- comportamento quando nenhum documento é encontrado;
- consistência em consultas semelhantes;
- necessidade de revisão humana.

Por fim, analisaria a operação:

- latência por registro;
- custo dos índices e da geração;
- impacto de consultas em lote;
- atualização das fontes;
- controles de acesso;
- observabilidade e tratamento de falhas.

Eu também manteria um conjunto de perguntas com respostas esperadas para comparar versões da base, configurações e instruções.

## Beta exige cautela

Apesar da utilidade, `ai_search()` ainda está em Beta.

Segundo a classificação oficial do Azure Databricks, recursos Beta não são recomendados para produção, não possuem SLA e podem sofrer mudanças de interface.

O recurso também apresenta limitações atuais:

- aceita somente índices do AI Search como fontes;
- permite no máximo dez fontes por chamada;
- exige Runtime 18.2 ou superior;
- exige ambiente serverless versão 3 ou superior quando usado nesse tipo de compute;
- precisa ser habilitado pelo administrador.

Por isso, eu começaria com protótipos, processamento controlado e casos sem decisão automática de alto impacto.

## SQL reduz a integração, não a responsabilidade

A principal contribuição de `ai_search()` é aproximar a recuperação contextual dos pipelines de dados.

Equipes que já trabalham com SQL podem combinar registros estruturados com documentação relevante sem implementar todo o fluxo de busca em uma aplicação separada.

Mas a confiabilidade continuará dependendo da preparação dos documentos, da atualização dos índices, das permissões e da avaliação dos resultados.

Uma única função pode reduzir bastante o código de integração. Ela não elimina a necessidade de engenharia, governança e observabilidade.

Na sua arquitetura, a busca para RAG deve permanecer em uma aplicação separada ou faz sentido incorporá-la diretamente aos pipelines SQL?

#AzureDatabricks #DataEngineering #RAG #AISearch

## Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Função SQL ai_search](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/functions/ai_search)
- [Visão geral do Databricks AI Search](https://learn.microsoft.com/en-us/azure/databricks/ai-search/ai-search)
- [Classificações de releases e previews](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types)

---

## 3. Texto para “Conte para sua rede”

> Um pipeline de RAG normalmente combina várias etapas de recuperação, deduplicação, reranking e geração.
>
> A nova função `ai_search()` do Azure Databricks leva parte desse fluxo para o SQL, permitindo enriquecer dados operacionais e construir processamentos em lote sobre índices do AI Search.
>
> No artigo, explico como a função trabalha, seus requisitos e por que o status Beta ainda exige cautela.
>
> Na sua arquitetura, a recuperação para RAG deveria fazer parte dos pipelines SQL?
>
> #AzureDatabricks #DataEngineering #RAG

---

## 4. Orientação visual da capa

**Formato:** horizontal 1,91:1, gerado em 1736 × 906 px.

**Título:**

> RAG em SQL no Azure Databricks

**Subtítulo:**

> ai_search() busca, deduplica e reranqueia

**Composição:**

- fundo azul-marinho em sangria completa, sem faixas brancas;
- consulta em linguagem natural à esquerda;
- `ai_search()` como elemento central;
- dois índices configurados abaixo da função;
- deduplicação e reranking como etapas separadas;
- documentos relevantes e resposta fundamentada à direita;
- aviso visual de que a função não consulta tabelas brutas;
- selo `Beta — 7 ago. 2026`;
- margem segura superior a 8%;
- assinatura discreta `Alex Marques | Engenharia de Dados`.

A proporção, a grafia, o status Beta e o fluxo técnico foram revisados.

## 5. Imagem final
