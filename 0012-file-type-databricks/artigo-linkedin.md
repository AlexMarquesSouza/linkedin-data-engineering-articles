## 1. Resumo da pauta

**Tema:** `FILE` type no Azure Databricks: arquivos não estruturados como colunas governadas em tabelas Delta.

**Anúncio oficial:** 10 de agosto de 2026.
**Documentação atualizada:** 11 de agosto de 2026.
**Status:** **Beta**, com ativação pelo administrador na página de Previews. Não está em disponibilidade geral e a documentação não o classifica como Private Preview ou Public Preview — o status oficial utilizado pela Databricks é Beta.

O recurso permite representar documentos, imagens, áudio e vídeo por meio de referências acompanhadas de metadados como URI, tamanho, tipo de conteúdo e checksum. O conteúdo binário permanece no armazenamento e só é lido quando uma função ou UDF realmente precisa processá-lo.

Requisitos e escopo:

- Databricks SQL ou Databricks Runtime 18 LTS ou superior.
- Unity Catalog.
- Somente tabelas Delta Lake.
- Não suportado em notebooks serverless.
- Disponível em notebooks conectados a SQL warehouses serverless.
- Ativação explícita por um administrador.
- Pipelines Lakeflow que utilizem o recurso devem usar o canal Preview.

A pauta é diferente dos temas recentes sobre AUTO CDC, execução nativa do Fabric, VARIANT e Unity Catalog.

Fontes primárias:

- [Anúncio do FILE type — Databricks, 10/08/2026](https://www.databricks.com/blog/introducing-file-type-native-column-type-multimodal-data)
- [Visão geral do FILE type — Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/unstructured/file)
- [Referência técnica do tipo FILE — Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/data-types/file-type)
- [Tutorial de pipeline com FILE — Microsoft Learn](https://learn.microsoft.com/en-us/azure/databricks/ldp/tutorial-file-pipelines)

---

## 2. Artigo final para LinkedIn

# FILE type no Azure Databricks: arquivos multimodais entram no modelo governado do lakehouse

Documentos, imagens, gravações e vídeos sempre fizeram parte dos dados corporativos. O problema é que eles normalmente permanecem fora do modelo de governança aplicado às tabelas.

O `FILE` type, anunciado pela Databricks em 10 de agosto de 2026, tenta reduzir essa separação. Em vez de manter apenas um caminho em uma coluna `STRING` ou carregar o objeto inteiro como `BINARY`, agora podemos representar um arquivo como uma referência governada dentro de uma tabela Delta.

O recurso está em Beta. Ainda não é uma funcionalidade que eu adotaria indiscriminadamente em cargas críticas, mas seu desenho aponta para uma mudança relevante na arquitetura de dados multimodais.

## O que muda tecnicamente

Uma coluna `FILE` armazena uma referência ao arquivo e metadados associados:

- `uri`;
- `offset`;
- `size`;
- `content_type`;
- `checksum`.

Consultar esses metadados não exige a leitura completa do conteúdo. Os bytes são acessados somente quando uma função de IA ou uma UDF precisa processar o arquivo.

Isso é importante porque evita dois padrões problemáticos:

- armazenar arquivos grandes diretamente em colunas `BINARY`;
- representar arquivos apenas por caminhos `STRING`, sem uma relação governada entre a linha, o arquivo e seu ciclo de vida.

O `FILE` pode ser passado para funções como `ai_parse_document` e para UDFs em Python, Scala ou SQL.

## Managed ou External

Existem duas modalidades de coluna.

### FILE MANAGED

O arquivo é copiado para um `FileSpace`, definido em um volume do Unity Catalog, e passa a ter seu ciclo de vida associado à tabela.

Esse modelo é indicado quando a aplicação deve acessar o arquivo por meio da tabela, como em:

- pipelines de documentos;
- treinamento de modelos;
- soluções de RAG;
- processamento de conteúdo recebido de fontes externas;
- aplicações que precisam de controles de acesso mais próximos da linha.

Excluir ou atualizar uma linha torna o arquivo antigo elegível para limpeza.

A ressalva é importante: durante o Beta, a coleta automática desses arquivos sem referência ainda não é suportada. A exclusão da linha não significa que o objeto será removido imediatamente do armazenamento.

### FILE EXTERNAL

A coluna aponta para um arquivo que já existe em um volume do Unity Catalog. O objeto não é copiado e seu ciclo de vida continua independente da tabela.

Esse desenho atende melhor a cenários nos quais:

- outras ferramentas precisam manter acesso ao caminho original;
- mover ou duplicar os objetos não é aceitável;
- o processo de retenção já é controlado externamente.

Um `SELECT` na tabela pode expor os metadados da referência, mas a leitura dos bytes também exige `READ VOLUME` no volume subjacente. A Databricks recomenda trabalhar com arquivos imutáveis nesse modelo.

## Um pipeline possível

A documentação oficial apresenta uma arquitetura medallion para documentos:

- Bronze: ingestão incremental com Auto Loader como `FILE MANAGED`;
- Silver: parsing e classificação dos documentos;
- Gold: extração de campos estruturados por categoria.

Uma definição simplificada da camada Bronze pode seguir este formato:

```sql
CREATE OR REFRESH STREAMING TABLE raw_documents (
  path STRING,
  size BIGINT,
  modification_time TIMESTAMP,
  file FILE MANAGED
)
TBLPROPERTIES (
  'databricks.filespace-preview' =
  '/Volumes/catalog/schema/filespace/'
)
AS
SELECT *
FROM STREAM read_files(
  '/Volumes/catalog/schema/source/',
  format => 'file'
);
```

O Auto Loader captura a referência e os metadados. A coluna `FILE MANAGED` determina que o conteúdo seja copiado para o `FileSpace` governado.

Essa combinação aproxima ingestão incremental, processamento multimodal e governança, mas cada função de IA utilizada continua tendo requisitos próprios de região, compute, disponibilidade e custo.

## Pontos de atenção

Antes de considerar produção, eu validaria pelo menos os seguintes aspectos:

- O recurso está em Beta e precisa ser habilitado por um administrador.
- É suportado apenas em tabelas Delta Lake.
- Exige Databricks Runtime 18 LTS ou superior, ou Databricks SQL.
- Não funciona em notebooks serverless.
- Um pipeline Lakeflow com `FILE` precisa utilizar o canal Preview.
- `FILE MANAGED` exige a propriedade experimental `databricks.filespace-preview`.
- Acesso a arquivos managed depende das permissões da tabela e do volume que sustenta o `FileSpace`.
- A coleta automática de arquivos sem referência ainda não está disponível.
- O checksum nem sempre é preenchido; `list_files` e `read_files`, por exemplo, não o populam.
- A coluna `FILE` não pode ser usada como chave de junção, agrupamento, particionamento ou clustering. Para algumas operações, será necessário usar `file.uri` ou outro identificador derivado.
- O processamento por UDF requer compute no Azure Databricks e não está disponível diretamente no cliente do Databricks Connect.
- Arquivos vindos de SharePoint, OneDrive, Google Drive ou SFTP precisam ser ingeridos como managed antes do processamento por determinadas funções e UDFs.

A Databricks também informa que está trabalhando com a comunidade para levar esse conceito a Parquet, Delta Lake, Iceberg e Apache Spark. Isso deve ser interpretado como direção de desenvolvimento, não como compatibilidade aberta já entregue.

## Como eu avaliaria em produção

Eu começaria por um domínio controlado: contratos, laudos, manuais técnicos ou imagens de inspeção.

O piloto deveria medir:

- custo de armazenamento das cópias managed;
- custo de parsing e inferência;
- latência para leitura dos arquivos;
- comportamento de atualização e exclusão;
- rastreabilidade entre arquivo original e resultado estruturado;
- impacto das permissões de tabela e volume;
- procedimentos manuais de limpeza;
- estratégia de saída enquanto o tipo permanecer em Beta.

Também manteria uma chave de negócio independente da URI. Caminhos de armazenamento não deveriam assumir o papel de identidade permanente do documento.

## Minha avaliação profissional

Como engenheiro de dados que trabalha com Azure e Databricks, considero o `FILE` type uma evolução arquitetural mais importante do que apenas uma nova sintaxe SQL.

Ele cria uma abstração consistente para relacionar tabelas, arquivos e processamento multimodal. Isso pode reduzir soluções improvisadas baseadas em caminhos, tabelas auxiliares e regras de segurança desconectadas.

Ao mesmo tempo, o status Beta e as limitações operacionais impedem que a governança seja tratada como totalmente automática. Em especial, a ausência de garbage collection automático exige controles adicionais de retenção, custo e conformidade.

Eu usaria o recurso em provas de conceito e cargas controladas, sempre com uma alternativa de arquitetura documentada. Para cargas reguladas ou críticas, aguardaria maturidade operacional maior ou realizaria uma avaliação formal de risco antes da adoção.

Na sua arquitetura, documentos e imagens já são tratados como ativos governados ou ainda permanecem apenas como caminhos no armazenamento?

#AzureDatabricks #DataEngineering #UnityCatalog #Lakehouse

### Referências oficiais

- [Introducing FILE type: a native column type for multimodal data](https://www.databricks.com/blog/introducing-file-type-native-column-type-multimodal-data)
- [FILE type and unstructured data](https://learn.microsoft.com/en-us/azure/databricks/unstructured/file)
- [Referência SQL do FILE type](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/data-types/file-type)
- [Process files with UDFs](https://learn.microsoft.com/en-us/azure/databricks/unstructured/file-udfs)
- [Tutorial de pipeline com FILE](https://learn.microsoft.com/en-us/azure/databricks/ldp/tutorial-file-pipelines)

---

## 3. Conte para sua rede qual é o tópico do seu artigo

Arquivos não estruturados estão entrando no modelo governado do lakehouse.

O novo `FILE` type do Azure Databricks permite representar documentos, imagens, áudio e vídeo como referências nativas em tabelas Delta. A proposta é aproximar ingestão, Unity Catalog e processamento multimodal — mas o recurso ainda está em Beta e possui limitações relevantes para produção.

Sua plataforma governa os arquivos junto com as tabelas ou ainda depende de caminhos e controles paralelos?

#AzureDatabricks #DataEngineering #Lakehouse

---

## 4. Orientação visual da capa

- **Tamanho:** 1920 × 1080 px.
- **Proporção:** 16:9.
- **Formato:** PNG.
- **Margem segura:** pelo menos 140 px em todos os lados.
- **Fundo:** gradiente integral de grafite para vinho profundo, com brilhos coral e magenta; sem predominância azul.
- **Elemento central:** tabela lakehouse conectada a ícones de documento, imagem e vídeo, protegidos por símbolos discretos de governança.
- **Texto principal:** “FILE TYPE”.
- **Texto secundário:** “ARQUIVOS GOVERNADOS NO LAKEHOUSE”.
- **Status:** selo pequeno “BETA”.
- **Assinatura:** “Alex Marques | Engenharia de Dados”.
- **Estilo:** editorial tecnológico, alto contraste, poucos elementos e leitura clara em miniatura.
- **Restrições:** sem logotipos, faixas brancas, molduras, textos extras ou elementos próximos das bordas.

## 5. Imagem final

Capa revisada em **1920 × 1080 px**, PNG, com grafia, proporção, margens e coerência técnica verificadas:


A imagem foi criada no modo integrado de geração, com o prompt visual descrito acima.
