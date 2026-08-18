## 1. Resumo da pauta

### O que mudou desde a publicação anterior

O **Fabric Runtime 2.0 deixou de estar em Public Preview e passou para disponibilidade geral — GA**.

Na análise anterior sobre o Native Execution Engine, o Runtime 2.0 ainda precisava ser tratado como Preview. Em **12 de agosto de 2026**, a Microsoft atualizou a documentação e anunciou que ele está pronto para workloads de produção.

| Componente | Status atual |
|---|---|
| Fabric Runtime 2.0 | **Generally Available** |
| Apache Spark 4.1 no Runtime 2.0 | **GA** |
| Delta Lake 4.2 no Runtime 2.0 | **GA como componente do runtime** |
| Recursos específicos do Delta Lake 4.x | **Experimentais e restritos às experiências Spark** |
| Custom Live Pools no Runtime 2.0 | **Preview** |
| Runtime 2.0 como padrão | Planejado para o final de setembro de 2026 |
| Native Execution Engine | Suportado, mas precisa ser habilitado |

O Runtime 2.0 reúne:

- Apache Spark 4.1;
- Delta Lake 4.2;
- Python 3.13;
- Java 21;
- Scala 2.13;
- R 4.5.2;
- Azure Linux 3.0.

Apesar do GA, ele continua **opt-in**. A Microsoft planeja torná-lo o runtime padrão da interface, dos novos workspaces e dos novos ambientes somente no final de setembro de 2026.

Há uma inconsistência documental relevante: a página geral de comparação dos runtimes, atualizada em 29 de julho, ainda apresenta o Runtime 2.0 como Public Preview. O anúncio oficial e a página dedicada, ambos mais recentes, confirmam o GA.

Fontes primárias:

- [Anúncio oficial do Fabric Runtime 2.0 GA](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Fabric-Runtime-2-0-Generally-Available/ba-p/5326359)
- [Fabric Runtime 2.0 — documentação atualizada](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime-2-0)
- [Novidades do Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/whats-new)
- [Interoperabilidade de tabelas Delta no Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-interoperability)

---

## 2. Artigo final para LinkedIn

# Fabric Runtime 2.0 chega a GA: migrar para Spark 4.1 exige mais que trocar uma configuração

Equipes de engenharia de dados já podem adotar o Fabric Runtime 2.0 em produção com suporte de disponibilidade geral.

Mas esse GA não transforma uma migração de runtime em atualização automática e sem risco.

A mudança reúne, de uma só vez, Apache Spark 4.1, Delta Lake 4.2, Python 3.13, Java 21, Scala 2.13 e um novo sistema operacional. Para quem mantém notebooks, bibliotecas, JARs e tabelas consumidas por diferentes workloads do Fabric, a validação de compatibilidade passa a ser tão importante quanto os novos recursos.

## O que mudou

O Runtime 2.0 estava em Public Preview. Em 12 de agosto de 2026, a Microsoft confirmou sua disponibilidade geral e o classificou como pronto para produção.

Isso altera a recomendação anterior: ele deixa de ser apenas uma opção de laboratório e passa a poder integrar o roadmap oficial de produção.

O runtime inclui:

- Apache Spark 4.1;
- Delta Lake 4.2;
- Python 3.13;
- Java 21;
- Scala 2.13;
- R 4.5.2;
- Azure Linux 3.0.

É uma atualização substancial em comparação ao Runtime 1.3, baseado em Spark 3.5, Delta Lake 3.2, Python 3.11, Java 11 e Scala 2.12.

## GA, mas ainda opt-in

O Runtime 2.0 não se tornou imediatamente o padrão.

Ele precisa ser selecionado:

- nas configurações do workspace; ou
- em um item de Environment associado ao notebook ou Spark Job Definition.

A Microsoft planeja torná-lo a seleção padrão da interface e o runtime padrão de novos workspaces e ambientes no final de setembro de 2026.

Esse cronograma é uma previsão oficial, não uma garantia imutável. A data e o comportamento do rollout devem ser novamente verificados antes de mudanças em massa.

Eu aproveitaria esse período para migrar workloads representativos e registrar incompatibilidades antes que novas áreas passem a utilizar a versão por padrão.

## O tamanho real da migração

Alterar a versão do Spark é apenas uma parte do processo.

O salto envolve mudanças em várias camadas:

| Runtime 1.3 | Runtime 2.0 |
|---|---|
| Spark 3.5 | Spark 4.1 |
| Delta Lake 3.2 | Delta Lake 4.2 |
| Python 3.11 | Python 3.13 |
| Java 11 | Java 21 |
| Scala 2.12 | Scala 2.13 |
| Mariner 2.0 | Azure Linux 3.0 |

Isso pode afetar:

- bibliotecas Python com dependências nativas;
- wheels compilados para versões anteriores;
- JARs que dependem de Java, Scala ou Spark;
- conectores de terceiros;
- funções que dependem de comportamentos antigos do Spark SQL;
- configurações renomeadas ou removidas;
- serialização;
- tratamento ANSI;
- schemas inferidos;
- testes que dependem de ordenação não garantida.

GA significa que a versão possui suporte para produção. Não significa que todo código criado para o Runtime 1.3 seja automaticamente compatível.

## Atenção aos ambientes Python

A documentação registra uma alteração incompatível relacionada à atualização da base Python.

Ambientes com bibliotecas Python ou wheels podem apresentar mensagens como `LibraryManagementError`, informando que houve uma atualização do ambiente Spark Python.

A ação indicada pela Microsoft é:

1. remover as bibliotecas do Environment;
2. publicar o ambiente;
3. adicionar novamente as bibliotecas;
4. publicar outra vez.

Esse processo recria o ambiente sobre a nova base Python.

Eu também validaria:

- disponibilidade de wheels para Python 3.13;
- bibliotecas que compilam extensões em C ou C++;
- versões de pandas, NumPy, PyArrow e bibliotecas de ML;
- dependências transitivas;
- imports executados apenas em caminhos menos frequentes;
- tempo de inicialização do Environment.

Um notebook iniciar corretamente não comprova que todas as dependências estejam funcionando.

## JARs precisam de atenção adicional

A documentação geral do Fabric alerta que JARs possuem uma probabilidade relevante de incompatibilidade quando Java, Scala, Spark e sistema operacional mudam.

Nesse caso, a migração envolve simultaneamente:

- Java 11 para Java 21;
- Scala 2.12 para Scala 2.13;
- Spark 3.5 para Spark 4.1.

Uma biblioteca publicada para Scala 2.12, por exemplo, não deve ser presumida como compatível com Scala 2.13.

Antes de migrar, eu levantaria:

- coordenadas Maven;
- sufixo da versão Scala;
- dependências fornecidas pelo runtime;
- conflitos de classes;
- conectores JDBC;
- bibliotecas internas;
- código que utiliza APIs removidas ou modificadas.

## Delta Lake 4.2 exige uma ressalva

O Runtime 2.0 inclui Delta Lake 4.2, mas isso não significa que todos os recursos do Delta 4.x devam ser habilitados em tabelas compartilhadas por qualquer workload do Fabric.

A Microsoft informa que recursos específicos do Delta Lake 4.2 são experimentais e funcionam apenas em experiências Spark, como:

- notebooks;
- Spark Job Definitions.

Se a mesma tabela também for consumida por SQL analytics endpoint, Power BI, Dataflow Gen2, Eventstream ou outros mecanismos, habilitar determinados table features pode quebrar a interoperabilidade.

Esse é um dos pontos mais importantes da migração.

Uma tabela pode continuar sendo Delta e, ainda assim, adotar um protocolo ou feature que determinado leitor não entende.

Também é preciso lembrar que upgrades explícitos de protocolo podem ser irreversíveis. Antes de atualizar uma tabela, eu verificaria todos os leitores e escritores atuais e futuros.

## Native Execution Engine

O Runtime 2.0 oferece suporte ao Native Execution Engine, que pode levar operadores compatíveis para uma execução colunar em C++ baseada em Apache Gluten e Velox.

Entretanto, o mecanismo precisa ser habilitado no Environment.

Mesmo habilitado, ele não transforma todo o plano em execução nativa. Operadores incompatíveis retornam ao mecanismo tradicional da JVM.

Portanto, eu monitoraria:

- operadores nativos;
- pontos de fallback;
- conversões entre execução colunar e por linhas;
- duração dos estágios;
- consumo de capacidade;
- consistência dos resultados.

Os benchmarks de até seis vezes mais desempenho apresentados pela Microsoft são resultados de cenários específicos. Eles justificam testes, mas não representam uma previsão automática para qualquer pipeline.

O suporte a parsing vetorizado de JSON e a Structured Streaming no caminho nativo continuam indicados como melhorias futuras.

## Novos recursos do Spark

Com Spark 4.1, o Runtime 2.0 disponibiliza uma base mais moderna para SQL, DataFrames, PySpark e streaming.

Entre os recursos destacados estão:

- tipo `VARIANT`;
- funções SQL definidas pelo usuário;
- variáveis de sessão;
- pipe syntax;
- collations;
- Python Data Source API;
- Python UDTFs;
- profiling unificado de UDFs PySpark;
- Arbitrary State API v2;
- State Data Source para depuração de streaming.

Nem todos esses recursos terão o mesmo nível de compatibilidade entre os workloads do Fabric. O fato de uma função estar disponível no Spark não significa que a tabela resultante será consumida sem restrições por todas as demais experiências.

## Como eu faria a migração

Eu evitaria alterar imediatamente o runtime padrão de todo o workspace.

Começaria criando um Environment específico com Runtime 2.0 e associando workloads selecionados.

A primeira onda incluiria:

- notebook somente com Spark SQL;
- pipeline PySpark com bibliotecas públicas;
- job com wheel interno;
- workload com JAR;
- processamento de tabelas Delta compartilhadas;
- Structured Streaming;
- pipeline com Native Execution Engine.

Para cada workload, compararia:

- resultado funcional;
- schema produzido;
- duração total;
- consumo de capacidade;
- plano físico;
- quantidade de fallback;
- logs e warnings;
- bibliotecas carregadas;
- protocolo das tabelas;
- leitura por outros workloads;
- reprocessamento e idempotência.

Depois, promoveria o Environment pelos ambientes de desenvolvimento, homologação e produção.

## Minha avaliação profissional

Como engenheiro de dados, vejo o GA do Runtime 2.0 como um avanço importante para o Microsoft Fabric.

Spark 4.1, Python 3.13, Java 21 e Delta Lake 4.2 modernizam a base da plataforma e abrem espaço para novos recursos, desempenho e melhor experiência de desenvolvimento.

O ponto mais relevante, porém, não é apenas adotar versões recentes.

É fazer isso preservando compatibilidade entre notebooks, bibliotecas, pipelines e as diferentes experiências que consomem as tabelas no OneLake.

Na minha visão, o GA é o sinal para iniciar a migração estruturada — não para trocar a configuração de todos os workspaces sem testes.

Sua equipe já possui uma matriz de compatibilidade para migrar Spark, Python, Java, Scala e Delta Lake ao mesmo tempo?

#MicrosoftFabric #ApacheSpark #DeltaLake #DataEngineering

### Referências oficiais

- [Fabric Runtime 2.0 — Generally Available](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Fabric-Runtime-2-0-Generally-Available/ba-p/5326359)
- [Fabric Runtime 2.0 — Microsoft Learn](https://learn.microsoft.com/en-us/fabric/data-engineering/runtime-2-0)
- [Novidades do Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/whats-new)
- [Interoperabilidade de tabelas Delta no Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-interoperability)
- [Guia oficial de migração do Apache Spark](https://spark.apache.org/docs/latest/core-migration-guide.html)

---

## 3. Conte para sua rede qual é o tópico do seu artigo

O Fabric Runtime 2.0 saiu de Public Preview e agora está GA.

A mudança libera uma base com Spark 4.1, Delta Lake 4.2 e Python 3.13 para produção. Mas bibliotecas, JARs e table features do Delta ainda precisam ser validados — principalmente quando a mesma tabela é consumida por diferentes workloads do Fabric.

GA é sinal para migrar com método, não para alterar todos os workspaces de uma vez.

Sua equipe está preparada para testar todo esse salto de versões?

#MicrosoftFabric #ApacheSpark #DataEngineering

---

## 4. Orientação visual da capa

- **Formato:** PNG.
- **Dimensões:** 1920 × 1080 px.
- **Proporção:** 16:9.
- **Fundo:** grafite, ro
