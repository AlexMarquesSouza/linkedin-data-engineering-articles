## 1. Resumo da pauta

### Tema escolhido

**Capacity Overview Events no Microsoft Fabric: monitoramento e alertas de capacidade agora em disponibilidade geral.**

Em **12 de agosto de 2026**, a Microsoft anunciou que os Capacity Overview Events passaram de **Preview para Generally Available**.

O recurso transforma sinais operacionais de uma capacidade Fabric em eventos consumíveis pelo Real-Time Hub. Esses sinais podem alimentar:

- alertas no Fabric Activator;
- automações operacionais;
- Eventstreams;
- armazenamento histórico em Eventhouse;
- dashboards de capacidade;
- análises de tendência e planejamento.

### Status e escopo

| Capacidade | Status |
|---|---|
| Capacity Overview Events | **Generally Available** |
| `Microsoft.Fabric.Capacity.Summary` | **GA** |
| `Microsoft.Fabric.Capacity.State` | **GA** |
| Capacity Events Accelerator | Projeto comunitário opcional |
| Entrega dos eventos | Best effort |
| Backfill histórico | Não disponível |

Os dois eventos são:

- **Capacity Summary:** emitido a cada 30 segundos enquanto a capacidade está ativa e possui valores relevantes.
- **Capacity State:** emitido somente quando ocorre mudança de estado, como pausa, retomada ou condição relacionada a throttling.

A mudança é relevante para engenharia de dados porque permite tratar observabilidade da plataforma como um fluxo de eventos, aproximando monitoramento, histórico e automação.

Fontes primárias:

- [Anúncio oficial do GA](https://community.fabric.microsoft.com/t5/Fabric-Updates-Blog/Capacity-Overview-Events-in-Real-Time-Hub-Generally-Available/ba-p/5356729)
- [Schema dos Capacity Overview Events](https://learn.microsoft.com/en-us/fabric/real-time-hub/explore-fabric-capacity-overview-events)
- [Como criar um Eventstream de capacidade](https://learn.microsoft.com/en-us/fabric/real-time-hub/create-streams-fabric-capacity-overview-events)
- [Tutorial oficial de alertas de throttling](https://learn.microsoft.com/en-us/fabric/real-time-hub/tutorial-monitor-capacity-threshold)

---

## 2. Artigo final para LinkedIn

# Microsoft Fabric transforma capacidade em eventos: observabilidade antes do throttling

Uma capacidade Fabric não deveria começar a ser investigada somente depois que notebooks atrasam, pipelines acumulam filas ou consultas passam a ser rejeitadas.

Com os Capacity Overview Events agora em disponibilidade geral, sinais de utilização e estado podem ser tratados como eventos em tempo quase real.

Isso permite sair de uma observabilidade predominantemente reativa para um fluxo operacional capaz de detectar pressão, gerar alertas e preservar informações para análise histórica.

## O que mudou

Os Capacity Overview Events foram apresentados em Preview em novembro de 2025.

Em 12 de agosto de 2026, a Microsoft anunciou sua disponibilidade geral.

O recurso produz dois tipos de evento.

### Capacity Summary

O evento:

```text
Microsoft.Fabric.Capacity.Summary
```

resume o consumo da capacidade em janelas de 30 segundos.

Entre os campos disponíveis estão:

- `capacityId`;
- `capacityName`;
- `capacitySku`;
- `capacityUnitMs`;
- `baseCapacityUnits`;
- `utilizationInteractive`;
- `utilizationBackground`;
- `interactiveDelayThresholdPercentage`;
- `interactiveRejectionThresholdPercentage`;
- `backgroundRejectionThresholdPercentage`;
- detalhamento de consumo por workload.

Os dados são agregados e suavizados de acordo com a lógica utilizada pelo Fabric para avaliar consumo e throttling. Portanto, não representam uma leitura bruta instantânea de CPU.

### Capacity State

O segundo evento é:

```text
Microsoft.Fabric.Capacity.State
```

Ele registra mudanças relevantes de estado, incluindo:

- capacidade criada;
- capacidade pausada;
- capacidade retomada;
- entrada em estado de sobrecarga;
- condições relacionadas a atraso ou rejeição.

Esse evento não é emitido continuamente. Se a capacidade permanece saudável, podem passar dias sem uma nova linha de estado.

Uma tabela vazia de eventos de estado não significa necessariamente falha de ingestão. Para uma capacidade ativa, ela pode simplesmente indicar que nenhuma mudança ocorreu desde o início da coleta.

## Da observabilidade à ação

Uma arquitetura possível é:

```text
Fabric Capacity
       ↓
Capacity Overview Events
       ↓
Real-Time Hub / Eventstream
       ├── Activator → alerta
       ├── função → automação controlada
       └── Eventhouse → histórico e análise
```

O Activator pode avaliar cada evento e gerar uma ação quando determinado indicador atinge um limite.

A documentação oficial apresenta um exemplo baseado em:

```text
backgroundRejectionThresholdPercentage >= 80
```

Esse valor de 80% é apenas um exemplo. Ele deve ser ajustado conforme a política operacional, o perfil dos workloads e a tolerância da organização a atraso ou rejeição.

## Três sinais importantes

Os eventos expõem indicadores diferentes para cargas interativas e de background.

### Interactive Delay

`interactiveDelayThresholdPercentage` representa a pressão que pode provocar atraso em operações interativas.

Quando o indicador ultrapassa 100%, o Fabric começa a aplicar atrasos.

Esse sinal é relevante para:

- consultas SQL;
- relatórios interativos;
- experiências que dependem de resposta imediata;
- workloads de usuários concorrentes.

### Interactive Rejection

`interactiveRejectionThresholdPercentage` representa o comprometimento de capacidade que pode levar à rejeição de operações interativas.

Ele utiliza um horizonte de suavização diferente do indicador de atraso.

Um alerta não deveria tratar delay e rejection como a mesma condição. São estágios operacionais distintos e podem exigir respostas diferentes.

### Background Rejection

`backgroundRejectionThresholdPercentage` está relacionado à rejeição de workloads executados em background.

Isso pode atingir:

- pipelines;
- notebooks agendados;
- refreshes;
- Spark jobs;
- movimentação de dados;
- tarefas de Dataflow Gen2.

Para um engenheiro de dados, esse indicador pode ser mais útil do que um percentual genérico de utilização, pois está diretamente associado ao risco de trabalho de background ser rejeitado.

## Visibilidade por workload

O evento Summary também disponibiliza um detalhamento de consumo.

Entre os workloads identificáveis estão:

- Spark;
- Warehouse e SQL endpoints;
- Data Integration;
- Dataflow Gen2;
- Eventstream;
- Eventhouse;
- OneLake;
- semantic models;
- Machine Learning;
- User Data Functions;
- Activator;
- recursos de IA.

Isso não substitui uma investigação detalhada no Capacity Metrics, Monitoring Hub ou histórico das execuções.

A utilidade é outra: detectar rapidamente qual grupo de workload estava contribuindo para a pressão naquele intervalo.

## GA não significa entrega exatamente uma vez

Esse é o principal cuidado técnico.

Para priorizar baixa latência e desempenho, os Capacity Overview Events utilizam entrega **best effort**.

Na prática:

- eventos podem chegar duplicados;
- eventos podem, raramente, não ser entregues;
- não existe garantia de exactly-once;
- o sistema não realiza backfill histórico.

Para remover duplicidades do Summary no Eventhouse, a documentação sugere uma estratégia semelhante a:

```kusto
SummaryEvents
| summarize take_any(*)
    by windowStartTime, windowEndTime, capacityId
```

A chave combina:

- capacidade;
- início da janela;
- final da janela.

A automação também deve ser idempotente. Dois eventos equivalentes não podem provocar duas escalas, duas notificações críticas ou duas chamadas de remediação.

## O histórico precisa ser persistido

O Real-Time Hub não recompõe eventos anteriores ao início da coleta.

Se a organização pretende analisar:

- tendências semanais;
- horários de maior pressão;
- crescimento por workload;
- recorrência de throttling;
- impacto de mudanças de SKU;
- comportamento antes de incidentes;

os eventos devem ser enviados desde cedo para Eventhouse ou outro destino persistente.

Sem essa persistência, o recurso atende ao alerta imediato, mas não cria sozinho um histórico operacional.

## Cuidados com capacidade pausada

Quando uma capacidade é pausada, o consumo suavizado pode ser transferido para a próxima janela disponível.

Isso pode criar um pico artificialmente elevado no momento da pausa.

A documentação registra que esses valores podem ser muito superiores ao padrão normal da capacidade.

Para dashboards e detecção de anomalias, eu trataria explicitamente:

- início da pausa;
- retomada;
- mudança do `activationId`;
- janelas com valores extremos;
- ausência de Summary durante a pausa.

Um gráfico que não reconhece esse comportamento pode transformar uma operação administrativa normal em um falso incidente de consumo.

## Rede e permissões

A configuração exige:

- acesso a um workspace Fabric ou Trial com permissão de Contributor ou superior;
- função de Capacity Admin sobre a capacidade monitorada.

Além disso, controles de rede podem interferir na arquitetura.

Quando a proteção de acesso de saída está habilitada no workspace consumidor, o consumo entre workspaces é bloqueado por padrão. É necessário permitir o conector de Real-Time Events nas regras de conexão.

Private Links também podem bloquear consumidores localizados em outros workspaces quando o acesso público está desabilitado.

Portanto, uma arquitetura que funciona em um workspace de teste não deve ser presumida como compatível com o desenho de rede da produção.

## Automação com limites

O Activator pode enviar e-mails ou executar funções quando um indicador ultrapassa o limite configurado.

Uma automação poderia:

- abrir um incidente;
- notificar a equipe de plataforma;
- registrar o evento em uma ferramenta operacional;
- suspender workload não crítico;
- iniciar uma função de mitigação;
- recomendar mudança de janela;
- acionar um runbook.

Eu evitaria começar com uma alteração automática de capacidade.

Antes disso, adicionaria:

- cooldown entre ações;
- deduplicação;
- validação do estado atual;
- limite máximo de execuções;
- trilha de auditoria;
- tratamento de eventos ausentes;
- autorização para ações de custo;
- mecanismo de rollback;
- escalonamento humano.

O recurso automatiza a chegada do sinal. A decisão operacional continua sendo responsabilidade da arquitetura.

## Como eu aplicaria em produção

Eu começaria com três níveis.

### Nível 1 — observação

- Persistir Summary e State no Eventhouse.
- Criar dashboard por capacidade e workload.
- Medir o comportamento durante pelo menos duas semanas.
- Identificar valores normais e períodos de pico.

### Nível 2 — alerta

- Alertar sobre aproximação de delay.
- Criar alerta separado para risco de rejection.
- Aplicar janelas de confirmação para reduzir ruído.
- Diferenciar workloads interativos e de background.

### Nível 3 — ação controlada

- Executar runbooks idempotentes.
- Registrar toda ação e sua causa.
- Impedir ações repetidas durante o mesmo incidente.
- Manter intervenção humana para mudanças de custo ou capacidade.

## Minha avaliação profissional

Como engenheiro de dados, considero o GA dos Capacity Overview Events uma evolução importante na operação do Fabric.

O valor não está apenas em receber uma métrica a cada 30 segundos. Está em transformar a capacidade em uma fonte de eventos que pode participar da própria arquitetura de dados.

Isso permite tratar observabilidade como pipeline:

- capturar;
- validar;
- deduplicar;
- armazenar;
- analisar;
- alertar;
- agir.

Ao mesmo tempo, o modelo best effort, a ausência de backfill e os efeitos da suavização impedem que esses eventos sejam tratados como um ledger exato de cobrança ou como única fonte para investigação.

Eu os utilizaria como camada de detecção e resposta, complementada por Capacity Metrics, histórico de execuções e telemetria dos workloads.

Sua equipe descobre a pressão de capacidade antes do throttling ou somente depois que os pipelines começam a falhar?

#MicrosoftFabric #DataEngineering #Observability #RealTimeAnalytics

### Referências oficiais

- [Capacity Ove
