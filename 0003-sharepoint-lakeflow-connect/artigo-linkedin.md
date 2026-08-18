## Pauta de hoje: ingestão gerenciada do SharePoint no Azure Databricks agora é GA

Em **4 de agosto de 2026**, o conector gerenciado do Microsoft SharePoint no Lakeflow Connect tornou-se **Generally Available (GA)** no Azure Databricks. A distribuição é gradual e pode levar uma semana ou mais para alcançar todos os workspaces. [Notas oficiais de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)

O conector permite ingerir arquivos do SharePoint em tabelas Delta de forma incremental e gerenciada, com governança pelo Unity Catalog e orquestração por Databricks Workflows.

Antes do GA, o recurso estava em Beta. Em junho de 2026, havia recebido suporte ampliado para arquivos estruturados, metadados, filtros e evolução de esquema.

## Artigo final para o LinkedIn

# SharePoint no Azure Databricks: ingestão gerenciada agora é GA

Arquivos armazenados no SharePoint frequentemente fazem parte de processos importantes, mas integrá-los a uma plataforma de dados pode exigir autenticação, controle incremental, tratamento de formatos e monitoramento próprios.

Em 4 de agosto de 2026, o Azure Databricks tornou o conector gerenciado do SharePoint no Lakeflow Connect geralmente disponível.

A mudança representa uma alternativa mais estruturada para transformar bibliotecas de documentos corporativos em fontes governadas para engenharia de dados, analytics e inteligência artificial.

## O que o conector permite fazer?

O conector gerenciado pode ingerir arquivos do SharePoint diretamente em tabelas Delta.

Ele oferece suporte a três estratégias principais:

- carregar arquivos estruturados, como CSV, JSON, XML, Excel, Parquet, Avro e ORC;
- armazenar documentos não estruturados como dados binários;
- capturar somente os metadados dos arquivos, sem carregar seu conteúdo.

Isso possibilita trabalhar não apenas com dados tabulares, mas também com contratos, relatórios, documentos e outros conteúdos corporativos.

## Ingestão incremental e gerenciada

Um dos principais benefícios está na ingestão incremental.

Depois da carga inicial, o pipeline pode identificar novos arquivos e alterações na origem, reduzindo a necessidade de reprocessar toda a biblioteca a cada execução.

Por ser gerenciado pelo Lakeflow Connect, o fluxo também incorpora recursos como:

- sincronização incremental;
- evolução de esquema configurável;
- tentativas automáticas após falhas;
- integração com Databricks Workflows;
- governança pelo Unity Catalog;
- implantação por API ou Declarative Automation Bundles.

Na prática, isso reduz parte do código e do estado operacional que a equipe precisaria manter em uma integração personalizada.

## Conector gerenciado ou conector padrão?

O Azure Databricks oferece duas opções para o SharePoint.

O conector gerenciado é indicado quando a prioridade é manter os dados sincronizados com menor esforço operacional.

Já o conector padrão permite criar pipelines personalizados com SQL, PySpark, Auto Loader, `COPY INTO` e outras APIs. Ele oferece mais flexibilidade para aplicar transformações durante a ingestão, mas transfere mais responsabilidade de implementação e manutenção para a equipe.

Eu avaliaria a escolha desta forma:

- **Conector gerenciado:** padronização, sincronização automática e menor manutenção;
- **Conector padrão:** personalização, transformações específicas e maior controle técnico.

## Pontos de atenção antes da adoção

O status GA não significa que todas as funcionalidades possíveis estejam disponíveis.

No conector gerenciado:

- a autoria pela interface ainda não é suportada;
- a configuração deve ser feita por API ou Declarative Automation Bundles;
- SCD tipo 2 não é suportado;
- seleção individual de colunas pela API não é suportada;
- filtros de linha pela API não são suportados.

A autenticação também precisa ser planejada. O acesso utiliza OAuth e requer permissões como `Sites.Read.All` ou `Sites.Selected`.

Para ambientes mais restritivos, eu priorizaria `Sites.Selected`, concedendo à aplicação acesso apenas aos sites necessários, em vez de permitir leitura ampla de todos os sites do tenant.

## Como eu validaria em produção?

Antes de colocar o conector em uma carga crítica, eu testaria:

- comportamento com arquivos alterados, movidos e excluídos;
- evolução de esquema em planilhas e arquivos CSV;
- duplicidade e idempotência das cargas;
- volume e tamanho dos documentos;
- permissões efetivas da aplicação no SharePoint;
- tratamento de formatos inesperados;
- tempo entre a alteração na origem e sua disponibilidade no Delta;
- alertas e recuperação após falhas.

Também separaria claramente as camadas do pipeline.

A ingestão inicial preservaria o conteúdo e os metadados com o mínimo de transformação. Regras de negócio, qualidade e padronização seriam aplicadas em etapas posteriores.

## Por que essa atualização merece atenção?

Muitas organizações possuem dados relevantes em bibliotecas de documentos que permanecem fora da arquitetura analítica principal.

Ao tornar o conector gerenciado do SharePoint GA, o Azure Databricks reduz a distância entre conteúdo corporativo, tabelas Delta e governança centralizada.

Na minha visão, a principal vantagem não está apenas em “conectar o SharePoint”. Está em tornar essa ingestão incremental, implantável e governada como parte da plataforma de dados.

Na sua arquitetura, os documentos do SharePoint já fazem parte dos pipelines de dados ou ainda dependem de integrações manuais?

#AzureDatabricks #LakeflowConnect #DataEngineering #SharePoint

## Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Conector gerenciado do SharePoint](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sharepoint)
- [Comparação entre os conectores do SharePoint](https://learn.microsoft.com/en-us/azure/databricks/ingestion/sharepoint)
- [Visão geral do Lakeflow Connect](https://learn.microsoft.com/en-us/azure/databricks/ingestion/overview)

## Texto para “Conte para sua rede”

> Dados importantes nem sempre estão em bancos ou data lakes. Muitas vezes, eles estão em bibliotecas do SharePoint.
>
> O conector gerenciado do SharePoint no Azure Databricks agora é GA e permite levar arquivos e metadados para tabelas Delta com ingestão incremental, Unity Catalog e Lakeflow Connect.
>
> No artigo, explico os benefícios, as limitações atuais e o que eu avaliaria antes de utilizar o conector em produção.
>
> Sua empresa já integra documentos do SharePoint à plataforma de dados?
>
> #AzureDatabricks #LakeflowConnect #DataEngineering

## Orientação visual

A capa foi criada no formato horizontal **1,91:1**, com:

- SharePoint como origem;
- Lakeflow Connect e ingestão incremental no centro;
- Delta e Unity Catalog como destino;
- selo `GA — 4 ago. 2026`;
- fundo azul-marinho;
- margens seguras e texto legível no feed;
- assinatura `Alex Marques | Engenharia de Dados`.
