# LinkedIn — notícias técnicas com implementação

Trilha criada exclusivamente a partir dos artigos da tarefa **Template LinkedIn Dados**. Ela é independente do **Radar Diário de Dados**.

Cada pasta contém artigo recuperado, versão curta para LinkedIn, código relacionado, dados fictícios, testes, diagrama e tutorial. Todo conteúdo permanece como rascunho local para revisão manual.

| # | Notícia transformada em projeto | Implementação |
|---:|---|---|
| 000 | [Configuração do ambiente](000-configuracao-ambiente/README.md) | VS Code, Python, testes e fluxo editorial |
| 0001 | [Databricks Runtime 19 × 18 LTS](0001-databricks-runtime-19-vs-18-lts/README.md) | Checker de compatibilidade de migração |
| 0002 | [Custos de Materialized Views](0002-custos-materialized-views-tags/README.md) | Cobertura de alocação por tags |
| 0003 | [SharePoint no Lakeflow Connect](0003-sharepoint-lakeflow-connect/README.md) | Deduplicação incremental por versão |
| 0004 | [Metric Views e calendário fiscal](0004-metric-views-calendario-fiscal/README.md) | Média móvel por índice numérico |
| 0005 | [MCP no Unity AI Gateway](0005-mcp-unity-ai-gateway/README.md) | Allowlist de ferramentas governadas |
| 0006 | [Tag Automations](0006-tag-automations-unity-catalog/README.md) | Classificação automática de ativos |
| 0007 | [RAG em SQL com ai_search](0007-ai-search-rag-sql/README.md) | Recuperação lexical local |
| 0008 | [Contexto no Data Lake para agentes](0008-contexto-data-lake-agentes/README.md) | Score de completude de metadados |
| 0009 | [VARIANT e Variant Shredding](0009-variant-shredding-json/README.md) | Projeção colunar de JSON flexível |
| 0010 | [Fabric Native Execution Engine](0010-fabric-native-execution-engine/README.md) | Monitor de fallback para JVM |
| 0011 | [AUTO CDC parcial e bitemporal](0011-auto-cdc-partial-bitemporal/README.md) | Aplicação ordenada de eventos parciais |
| 0012 | [FILE type no Databricks](0012-file-type-databricks/README.md) | Validação de arquivos managed/external |
| 0013 | [Fabric Runtime 2.0 e Spark 4.1](0013-fabric-runtime-2-spark-4/README.md) | Compatibilidade de bibliotecas Python |
| 0014 | [Fabric Capacity Overview Events](0014-fabric-capacity-events/README.md) | Alertas preventivos de utilização |
| 0015 | [Gmail no Lakeflow Connect](0015-gmail-lakeflow-connect/README.md) | Cursor incremental e deduplicação |
| 0016 | [Workiva no Lakeflow Connect](0016-workiva-lakeflow-connect/README.md) | Estado mais recente de auditoria |
| 0017 | [Managed Iceberg Sharing](0017-iceberg-managed-sharing/README.md) | Matriz de compatibilidade de clientes |

## Executar um projeto

```bash
cd "caminho/para/linkedin-data-engineering-articles"
cd "0001-databricks-runtime-19-vs-18-lts"
python3 -m src.demo
python3 -m unittest discover -s tests -v
```

## Validar toda a coleção

```bash
python3 linkedin/scripts/validate_projects.py
```

## Visualizar como site local

```bash
cd "caminho/para/linkedin-data-engineering-articles"
source .venv/bin/activate
python3 -m pip install -r requirements-docs.txt
python3 -m mkdocs serve --config-file mkdocs.yml
```

Esse comando inicia somente um servidor local e não publica o conteúdo.

## Política de publicação

Os textos não representam publicação concluída. Datas, status GA/Preview/Beta, links e opiniões devem ser revisados antes da cópia manual para o LinkedIn. Não existe integração com a API do LinkedIn, deploy, repositório remoto ou `git push`.


## Manutenção deste repositório

Este diretório é autônomo: contém documentação, dependências do site, testes estruturais e scripts próprios. Após clonar:

```bash
cd "caminho/para/linkedin-data-engineering-articles"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-docs.txt
python3 scripts/validate_projects.py
bash scripts/build_site.sh
```

O build gera somente documentação local. Publicação, criação de repositório remoto e `git push` continuam manuais.
