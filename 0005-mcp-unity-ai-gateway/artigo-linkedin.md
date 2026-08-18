## Pauta de hoje: conectores MCP gerenciados passam pelo Unity AI Gateway

Em **6 de agosto de 2026**, o Azure Databricks migrou seus conectores MCP gerenciados para o Unity AI Gateway.

A mudança abrange os conectores utilizados pelo Genie One e pelo Genie Code para acessar serviços como Google Drive, Microsoft 365, Slack, Atlassian e GitHub.

O objetivo é colocar esses conectores sob uma camada centralizada de governança, controle de acesso e visibilidade, junto aos demais servidores MCP e ferramentas de IA.

**Status:** a integração dos conectores externos permanece em **Beta**. O Unity AI Gateway tornou-se GA em 4 de agosto, mas algumas capacidades associadas, incluindo os conectores gerenciados e determinadas políticas de serviço, continuam em Beta.

**Ação necessária:** usuários que já utilizavam esses conectores precisam realizar uma nova autenticação. O Genie apresenta uma notificação solicitando a reconexão. [Notas oficiais de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)

## Artigo final para o LinkedIn

# Conectores MCP agora passam pelo Unity AI Gateway no Azure Databricks

Conectar agentes a documentos, mensagens, repositórios e aplicações corporativas amplia muito o que eles conseguem fazer.

Mas também aumenta uma questão importante: como controlar quais ferramentas o agente pode acessar, em nome de quem e com quais permissões?

Em 6 de agosto de 2026, o Azure Databricks migrou seus conectores MCP gerenciados para o Unity AI Gateway.

## O que mudou?

Os conectores gerenciados utilizados pelo Genie One e pelo Genie Code passaram a operar sob a governança do Unity AI Gateway.

Entre as fontes suportadas estão:

- Google Drive;
- Gmail;
- Microsoft 365, incluindo SharePoint, Teams, Outlook e Calendar;
- Atlassian, incluindo Jira e Confluence;
- Slack;
- Glean;
- GitHub.

Essas integrações permitem que o Genie consulte conteúdos externos para responder perguntas e executar tarefas com mais contexto.

A principal mudança não está apenas na conectividade. Está na inclusão dessas ferramentas em um ponto de controle centralizado.

## Por que o MCP precisa de governança?

O Model Context Protocol permite que agentes descubram e utilizem ferramentas externas por meio de uma interface padronizada.

Uma ferramenta MCP pode buscar um documento, consultar um repositório, recuperar uma mensagem ou acessar uma API corporativa.

Isso significa que o controle não deve considerar somente o modelo de IA. Também precisa abranger:

- o servidor MCP utilizado;
- as ferramentas expostas pelo servidor;
- o usuário que iniciou a solicitação;
- as permissões disponíveis na fonte;
- as credenciais e conexões externas;
- o histórico de utilização.

O Unity AI Gateway foi criado para estender a governança do Unity Catalog às interações entre modelos, agentes, servidores MCP e ferramentas.

## A identidade do usuário continua importante

Cada usuário autentica individualmente seu conector. Os tokens OAuth não são compartilhados entre usuários.

Além disso, o conteúdo acessível continua limitado por dois fatores:

1. os escopos OAuth aprovados na conexão;
2. as permissões que o próprio usuário possui na aplicação de origem.

Portanto, conectar o Microsoft 365 ao Genie não concede automaticamente acesso a todos os documentos da empresa. O resultado também depende das permissões existentes no SharePoint, Teams, Outlook e demais serviços.

Na minha visão, esse modelo é importante porque mantém a identidade da pessoa no centro da autorização, em vez de criar uma credencial ampla utilizada indistintamente por todos.

## Reautenticação obrigatória

A migração traz uma ação operacional imediata.

Quem já utilizava conectores gerenciados precisa reautenticá-los para continuar usando-os no Genie One ou no Genie Code.

O Azure Databricks informa os usuários afetados por meio de uma notificação no Genie.

Eu trataria essa mudança como uma pequena migração de identidade:

- identificar os conectores existentes;
- comunicar os usuários afetados;
- revisar os escopos solicitados;
- realizar a nova autenticação;
- testar as pesquisas nas fontes externas;
- confirmar se as permissões continuam adequadas.

## O que eu avaliaria antes da adoção?

Antes de liberar os conectores de maneira ampla, eu revisaria:

- quais fontes externas são realmente necessárias;
- quais grupos podem utilizar cada conexão;
- os escopos OAuth solicitados;
- o princípio do menor privilégio;
- as permissões mantidas nas aplicações de origem;
- os procedimentos para revogação de acesso;
- as regiões suportadas;
- as limitações de formato e tamanho de arquivos.

Por exemplo, os conectores externos estão disponíveis apenas em regiões que possuem suporte ao Model Serving.

No Google Drive, o tamanho máximo de arquivo é 10 MB e somente arquivos nativos do Google são suportados. PDFs, imagens e outros formatos binários não são aceitos.

No Microsoft 365, arquivos do SharePoint também possuem limite de 10 MB. Documentos, planilhas, apresentações e formatos textuais comuns são suportados, mas PDFs, imagens e outros binários não são.

## Beta não significa produção irrestrita

A integração permanece em Beta e precisa ser habilitada pelo administrador do workspace na página de previews.

Segundo a classificação do Azure Databricks, recursos Beta:

- não são recomendados para produção;
- não possuem SLA;
- podem sofrer alterações;
- são gerenciados principalmente pela equipe de engenharia;
- podem exigir habilitação explícita no workspace.

Por isso, eu começaria com um grupo controlado de usuários e fontes de menor risco.

Também evitaria conceder conectores apenas porque estão disponíveis. Cada integração deve ter um caso de uso, um responsável e uma política clara de acesso.

## A governança precisa acompanhar a conectividade

Agentes corporativos estão deixando de apenas responder perguntas para utilizar ferramentas e acessar sistemas externos.

Nesse cenário, governar somente os dados e os modelos não é suficiente. Precisamos governar também as conexões, as ferramentas e as ações disponíveis durante a execução.

A migração dos conectores MCP para o Unity AI Gateway é um passo nessa direção.

Sua organização já possui uma estratégia de governança para as ferramentas utilizadas por agentes de IA?

#AzureDatabricks #UnityAIGateway #DataGovernance #MCP

## Referências oficiais

- [Azure Databricks — novidades de agosto de 2026](https://learn.microsoft.com/en-us/azure/databricks/release-notes/product/2026/august)
- [Conexão com ferramentas e fontes externas](https://learn.microsoft.com/en-us/azure/databricks/genie-one/external-sources)
- [Governança de IA com Unity AI Gateway](https://learn.microsoft.com/en-us/azure/databricks/ai-gateway/)
- [Classificações de versões do Azure Databricks](https://learn.microsoft.com/en-us/azure/databricks/release-notes/release-types)

## Texto para “Conte para sua rede”

> Dar acesso a ferramentas externas torna os agentes mais úteis — e também aumenta a necessidade de governança.
>
> Os conectores MCP gerenciados do Azure Databricks agora passam pelo Unity AI Gateway, centralizando controle de acesso e visibilidade. A migração, ainda em Beta, também exige que usuários existentes reautentiquem suas conexões.
>
> No artigo, explico o impacto técnico e os cuidados que eu avaliaria antes da adoção.
>
> Sua empresa já governa as ferramentas utilizadas pelos agentes de IA?
>
> #AzureDatabricks #DataGovernance #MCP

## Orientação visual

A capa foi criada no formato horizontal **1,91:1**, apresentando:

- conectores externos à esquerda;
- MCP como camada intermediária;
- governança pelo Unity Catalog à direita;
- acesso, visibilidade e auditoria;
- alerta de reautenticação;
- selo `Beta — 6 ago. 2026`;
- margens seguras e assinatura discreta.
