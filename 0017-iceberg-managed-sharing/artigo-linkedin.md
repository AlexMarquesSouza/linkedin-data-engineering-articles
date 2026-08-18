## 1. Resumo da pauta

**Tema:** compartilhamento de tabelas Apache Iceberg gerenciadas no Azure Databricks
**Data do anúncio:** 14 de agosto de 2026
**Status:** **Generally Available — GA**

O Azure Databricks anunciou que tabelas Iceberg gerenciadas pelo Unity Catalog agora podem ser compartilhadas por:

- Databricks-to-Databricks sharing;
- OpenSharing;
- clientes externos compatíveis com Iceberg REST Catalog.

Essa pauta é diferente do anúncio de 4 de agosto sobre tabelas **Delta com Iceberg reads**. Agora, a origem é uma tabela nativamente criada como **managed Iceberg** no Unity Catalog.

### Mapa de disponibilidade

| Recurso | Status |
|---|---|
| Tabelas Iceberg gerenciadas no Unity Catalog | **GA** |
| Compartilhamento de managed Iceberg | **GA desde 14/08/2026** |
| Compartilhamento para clientes Iceberg externos | Incluído no anúncio mais recente |
| Compartilhamento de foreign Iceberg tables | **Public Preview** |
| Materialized Views managed Iceberg | **Public Preview** |
| Transações gravando em managed Iceberg | **Private Preview** |

### Divergência documental

A nota de versão, atualizada em 18 de agosto, confirma o GA e informa que provedores também podem compartilhar com clientes Iceberg externos.

Entretanto, a página operacional de criação de shares ainda exibe o texto anterior, classificando o recurso como Public Preview e dizendo que clientes Iceberg externos não são suportados.

Por ser uma inconsistência entre fontes oficiais, o status utilizado aqui é o da nota de versão mais recente, mas a habilitação deve ser validada no workspace antes de uma implantação.

Fontes primárias:

- [Release notes de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Criar shares no OpenSharing](https://learn.microsoft.com/en-us/azure/databricks/opensharing/create-share)
- [Apache Iceberg no Databricks](https://docs.databricks.com/aws/en/iceberg/)
- [Acesso por clientes Iceberg](https://docs.databricks.com/aws/en/external-access/iceberg)

## 2. Artigo final para LinkedIn

# Azure Databricks leva tabelas Iceberg gerenciadas ao compartilhamento GA

Compartilhar uma tabela aberta entre diferentes plataformas não deveria exigir exportações recorrentes, duplicação de dados ou entrega de credenciais permanentes de armazenamento.

O Azure Databricks colocou em disponibilidade geral o compartilhamento de tabelas Apache Iceberg gerenciadas pelo Unity Catalog.

Com isso, uma tabela Iceberg administrada no Databricks pode participar de compartilhamentos Databricks-to-Databricks, OpenSharing e, conforme o anúncio mais recente, ser consumida por clientes externos compatíveis com o Iceberg REST Catalog.

## O que realmente mudou

Tabelas Iceberg gerenciadas já estavam em GA desde maio de 2026.

A mudança de 14 de agosto está na camada de compartilhamento. O recurso, anteriormente apresentado como Preview, passou para GA.

Isso permite compartilhar uma managed Iceberg table usando um objeto de share:

```sql
ALTER SHARE dados_parceiros
ADD TABLE catalogo.schema.tabela_iceberg
AS dados.vendas;
```

O alias é opcional e define o nome apresentado ao destinatário.

O compartilhamento é voltado à leitura. Ele não concede ao destinatário o direito de modificar a tabela original.

## Delta com Iceberg não é managed Iceberg

Existem dois cenários que podem parecer equivalentes, mas não são.

### Delta com Iceberg reads

A tabela continua sendo Delta Lake. O Databricks gera metadados compatíveis com Iceberg para permitir que determinados clientes a leiam como uma tabela Iceberg.

### Managed Iceberg

A tabela é criada nativamente no formato Apache Iceberg e seu ciclo de vida é administrado pelo Unity Catalog.

Essa diferença afeta:

- formato da tabela;
- metadados;
- compatibilidade de recursos;
- operações de manutenção;
- comportamento de leitores e escritores;
- estratégia de interoperabilidade.

O anúncio atual trata do segundo cenário.

## OpenSharing e Iceberg REST

OpenSharing permite conceder acesso de leitura a parceiros e plataformas externas sem transferir a propriedade da tabela.

Clientes compatíveis com Iceberg REST Catalog podem incluir mecanismos baseados em:

- Apache Spark;
- Apache Flink;
- Trino;
- Snowflake;
- outras implementações compatíveis com a API.

Entretanto, “compatível com Apache Iceberg” não significa automaticamente “compatível com todos os recursos usados pela tabela”.

Antes da liberação, eu validaria:

- versão do cliente Iceberg;
- suporte à versão da especificação da tabela;
- autenticação aceita;
- suporte a deletion vectors do Iceberg v3;
- tipos de dados utilizados;
- evolução de schema;
- comportamento de deletes;
- conectividade com o armazenamento.

## Compartilhar não é liberar escrita

Existe outra distinção arquitetural importante.

O Iceberg REST Catalog do Unity Catalog pode ser utilizado, em uma integração direta e devidamente autorizada, para leitura e escrita em managed Iceberg tables.

OpenSharing possui outra finalidade: distribuição governada e somente leitura para destinatários.

Portanto, não se deve concluir que um consumidor de um share poderá realizar commits na tabela do provedor. Escrita externa exige outra configuração, outros privilégios e coordenação de commits pelo Unity Catalog.

## Governança continua no centro

O Unity Catalog administra:

- registro da tabela;
- permissões;
- compartilhamentos;
- credenciais temporárias em integrações compatíveis;
- auditoria;
- expiração de snapshots;
- compactação;
- otimizações de manutenção.

Isso evita distribuir credenciais estáticas do storage para cada consumidor.

Mesmo assim, políticas internas não devem ser presumidas como automaticamente propagadas para o destinatário. Ao compartilhar dados protegidos por filtros, máscaras ou políticas ABAC, é necessário verificar quais controles são avaliados no provedor e quais dados efetivamente aparecem no share.

Eu criaria uma visão ou tabela específica para compartilhamento quando o contrato externo exigir:

- remoção de colunas;
- pseudonimização;
- redução de granularidade;
- filtro por cliente;
- schema estável;
- política própria de retenção.

## Requisitos das tabelas gerenciadas

Para trabalhar com managed Iceberg tables no Azure Databricks, a documentação exige:

- workspace com Unity Catalog;
- Databricks Runtime 16.4 LTS ou superior;
- compute serverless disponível;
- conectividade do serverless com o storage;
- predictive optimization habilitado para manutenção.

O formato de arquivos suportado é Parquet.

Algumas limitações atuais incluem:

- ausência de branches e tags do Iceberg;
- tipos `UUID`, `TIME` e `Fixed(L)` não suportados;
- restrições para estruturas aninhadas com campos obrigatórios;
- ausência de AI Search em managed Iceberg;
- particionamento por expressões com suporte limitado;
- codec de compressão administrado pela plataforma;
- recursos específicos do Delta, como generated columns, não disponíveis automaticamente no Iceberg.

GA não elimina essas diferenças de formato.

## Nem tudo relacionado a Iceberg está GA

A classificação precisa ser feita por capacidade.

O compartilhamento de managed Iceberg está GA, mas:

- foreign Iceberg sharing permanece em Public Preview;
- managed Iceberg materialized views permanecem em Public Preview;
- transações com escrita em managed Iceberg permanecem em Private Preview.

Uma arquitetura não deve herdar o status GA de uma funcionalidade para todas as outras capacidades Iceberg utilizadas no mesmo fluxo.

## A documentação ainda precisa convergir

Há uma inconsistência oficial relevante.

A nota de versão mais recente confirma o GA e menciona clientes Iceberg externos. A página detalhada de criação de shares ainda apresenta a classificação antiga e a limitação anterior.

Eu trataria isso como um sinal para:

1. verificar se o recurso aparece no workspace;
2. testar com um destinatário controlado;
3. confirmar o comportamento com o cliente externo escolhido;
4. validar armazenamento padrão, autenticação e rede;
5. acompanhar a atualização da documentação operacional;
6. evitar compromissos contratuais antes dessa validação.

Isso não invalida o anúncio. Apenas impede que uma atualização de status seja confundida com compatibilidade universal e rollout simultâneo para todas as contas.

## Como eu aplicaria em produção

Eu começaria com uma tabela sem dados altamente sensíveis e um único destinatário.

O piloto deveria validar:

- tempo entre uma atualização e sua visibilidade;
- revogação do acesso;
- alteração de schema;
- leitura de snapshots;
- desempenho do cliente;
- custos de rede;
- acesso ao storage;
- logs de auditoria;
- comportamento diante de deletes;
- recuperação após falhas do consumidor.

Também documentaria separadamente:

- quem é o proprietário da tabela;
- quem administra o share;
- quais dados podem sair do domínio;
- quais clientes são homologados;
- como o contrato de schema será versionado;
- qual é o procedimento de revogação.

## Minha avaliação profissional

Como engenheiro de dados, vejo esse GA como mais um avanço importante na aproximação entre Unity Catalog e formatos de tabela abertos.

O principal ganho não é apenas “usar Iceberg”. É conseguir administrar uma tabela no Unity Catalog e distribuí-la para outros mecanismos por uma interface aberta e governada.

Isso pode reduzir cópias, integrações específicas e dependência de um único motor de consulta.

Ao mesmo tempo, eu não trataria interoperabilidade como uma propriedade binária. Formato, catálogo, protocolo, autenticação, storage e recursos de tabela precisam ser compatíveis no mesmo fluxo.

Na sua arquitetura, o compartilhamento entre plataformas ainda depende de cópias ou já utiliza contratos baseados em formatos e APIs abertas?

#AzureDatabricks #ApacheIceberg #DataEngineering #OpenSharing

### Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Criar e administrar shares](https://learn.microsoft.com/en-us/azure/databricks/opensharing/create-share)
- [Apache Iceberg no Databricks](https://docs.databricks.com/aws/en/iceberg/)
- [Acesso pelo Iceberg REST Catalog](https://docs.databricks.com/aws/en/external-access/iceberg)
- [Unity Catalog managed tables](https://docs.databricks.com/aws/en/tables/managed)
- [Credential vending para sistemas externos](https://docs.databricks.com/aws/en/external-access/credential-vending)

## 3. Conte para sua rede qual é o tópico do seu artigo

Tabelas Apache Iceberg gerenciadas pelo Unity Catalog agora podem ser compartilhadas em GA no Azure Databricks.

A evolução amplia o acesso por OpenSharing e clientes externos compatíveis com Iceberg, mas não transforma o compartilhamento em permissão de escrita nem garante compatibilidade com qualquer engine.

Sua plataforma compartilha tabelas abertas diretamente ou ainda cria cópias para cada consumidor?

#AzureDatabricks #ApacheIceberg #DataEngineering

## 4. Orientação visual da capa

- **Dimensões:** 1920 × 1080 px.
- **Proporção:** 16:9.
- **Formato:** PNG em sRGB.
- **Margem segura:** mínimo de 140 px.
- **Fundo:** grafite com gradientes verde-petróleo, vinho e roxo.
- **Título:** “ICEBERG COMPARTILHADO”.
- **Subtítulo:** “MANAGED TABLES • GA”.
- **Elemento central:** tabela tridimensional com camadas cristalinas inspiradas em gelo.
- **Governança:** escudo envolvendo a tabela.
- **Compartilhamento:** três fluxos de leitura para mecanismos externos abstratos.
- **Paleta:** grafite, ciano-gelo moderado, coral, âmbar e roxo.
- **Assinatura:** “Alex Marques | Engenharia de Dados”.
- **Restrições:** sem logotipos, nomes de engines, faixas brancas, molduras ou textos adicionais.

## 5. Imagem final

A imagem foi revisada quanto à grafia, legibilidade, status GA, margens e coerência técnica. O arquivo final está em PNG, sRGB e possui exatamente **1920 × 1080 px**.
