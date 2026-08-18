Segue a versão final, já organizada para você copiar e colar no artigo do LinkedIn:

# Databricks Runtime 19 ou Runtime 18 LTS: qual escolher?

Uma atualização de runtime pode trazer novos recursos e ganhos importantes, mas também introduzir incompatibilidades silenciosas nos pipelines.

Em 23 de julho de 2026, o Databricks Runtime 19 tornou-se geralmente disponível, baseado no Apache Spark 4.2.0. Com isso, surge uma decisão importante: adotar a versão mais recente ou permanecer em uma versão LTS?

## O que mudou com o Databricks Runtime 19?

O novo runtime incorpora avanços do Apache Spark 4.2 em áreas como CDC, Data Source V2, Spark Connect, processamento de streaming, Spark SQL e integração com o ecossistema Python por meio do Apache Arrow.

Um dos destaques é que as Python UDFs passam a utilizar serialização baseada em Arrow por padrão, sem exigir a reescrita do código.

Essas evoluções podem melhorar a integração entre Python e Spark e abrir novas possibilidades para pipelines de engenharia de dados.

## Principais pontos de atenção antes da atualização

Uma nova versão também traz mudanças que precisam ser avaliadas cuidadosamente:

- Suporte exclusivo ao JDK 21;
- Remoção de aproximadamente 90 pacotes Python do runtime padrão;
- Possíveis diferenças na conversão de tipos em Python UDFs;
- Restrições adicionais em determinadas configurações de clusters standard.

Na prática, isso significa que pipelines que atualmente funcionam podem depender de bibliotecas, comportamentos ou configurações que foram alterados na nova versão.

## O que avaliar antes de migrar um ambiente de produção?

Na minha visão, a atualização de um runtime não deve ser tratada apenas como uma simples troca de versão.

Antes de migrar um ambiente de produção, eu avaliaria:

- Testes de regressão dos pipelines;
- Dependências Python instaladas implicitamente;
- Compatibilidade de UDFs, bibliotecas e conectores;
- Desempenho antes e depois da migração;
- Comportamento de cargas batch e streaming;
- Estratégia de rollback em caso de incompatibilidade.

Também considero importante realizar a validação inicialmente em um ambiente controlado, monitorando tempo de execução, consumo de recursos, falhas e possíveis alterações nos resultados.

## Runtime 19 ou Runtime 18 LTS: qual escolher?

O Runtime 19 representa o caminho mais recente, oferecendo acesso às novidades do Apache Spark 4.2 e às evoluções mais atuais da plataforma.

Por outro lado, o Runtime 18 LTS oferece maior previsibilidade e um período prolongado de correções de estabilidade e segurança.

Por isso, não existe uma resposta única para todos os ambientes.

Para projetos que precisam explorar funcionalidades recentes, o Runtime 19 pode ser a escolha mais interessante. Já para cargas críticas, que priorizam estabilidade, compatibilidade e previsibilidade operacional, uma versão LTS pode ser mais adequada.

A escolha deve considerar os objetivos do projeto, a criticidade dos dados, as dependências existentes e a capacidade da equipe de testar e acompanhar a migração.

Na sua equipe, o que pesa mais na escolha de um runtime: novos recursos, desempenho ou estabilidade?

#DataEngineering #AzureDatabricks #ApacheSpark

## Referências oficiais

- [Apache Spark 4.2.0](https://spark.apache.org/releases/spark-release-4-2-0.html)
- [Novidades do Azure Databricks — julho de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/july)
- [Notas de versão do Databricks Runtime 19](https://learn.microsoft.com/en-us/azure/databricks/release-notes/runtime/19)

Essa é a versão que eu publicaria. Ela apresenta a novidade, demonstra seu conhecimento técnico e mostra aos recrutadores como você avalia uma atualização em um ambiente real de produção.
