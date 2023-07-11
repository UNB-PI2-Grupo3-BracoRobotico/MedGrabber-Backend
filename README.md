# grabber-backend
Backend repository for the robotic arm project

## Possui dúvidas?

> Dúvidas sobre como rodar testes? Dúvidas sobre como usar o docker?

Se você tem dúvidas sobre como realizar algumas ações no projeto, temos a seção de dúvidas na wiki do projeto: [FAQ - Perguntas Frequentes](https://github.com/UNB-PI2-Grupo3-BracoRobotico/grabber-backend/wiki)

# Instalação

## Subindo os microsserviços

```sh
docker compose up -d
```

Este comando irá realizar a build e deixará disponível todos os containers da aplicação.

# Execução

### 🚨 Tutorial KAFKA
[Video: como usar o kafka nesse projeto](https://youtu.be/7xh3CTJqkVM)

Execute a aplicação com o comando:

```sh
docker compose up -d
```

### Interface para o Kafka

Para visualizar os tópicos e as mensagens que estão sendo enviadas, acesse a interface do Kafka em http://localhost:8080

Nessa interface é possível visualizar e criar mensagens para os tópicos do kafka.

---

## Diagrama representando comunicação entre os tópicos e os microserviços

Diagrama representando o fluxo de um pedido que foi realizado corretamente e houve sucesso em todas as etapas do pedido

```mermaid
sequenceDiagram
    Frontend->>topic order-creation: Dados iniciais do pedido
    topic order-creation->>order_service: Dados iniciais do pedido
    order_service-->>database: Cria pedido
    order_service->>topic order-status: Status: Pedido recebido
    order_service->>topic payment: Dados para gerar pagamento do pedido
    topic payment->>payment_service: Dados para gerar pagamento do pedido
    payment_service->>topic order-status: Status: aguardando pagamento
    topic order-status->>order_service: Recebe status do pedido
    order_service-->>database: Salva status do pedido
    payment_service->>topic order-status: Status: pagamento recebido
    topic order-status->>order_service: Recebe status do pedido
    order_service-->>database: Salva status do pedido
    topic order-status->>robotic_arm_service: Status: pagamento recebido
    robotic_arm_service->>topic order-status: Status: separando pedido
    topic order-status->>order_service: Recebe status do pedido
    order_service-->>database: Salva status do pedido
    robotic_arm_service->>topic order-products: Dados com coordenadas e quantidade dos pedidos
    topic order-products->>firmware do braço robótico: Dados com coordenadas e quantidade dos pedidos
    firmware do braço robótico->>topic order-status: Status: Pedido Separado
    topic order-status->>order_service: Status: Pedido Separado
    order_service-->>database: Salva status do pedido finalizado
```

## Milestones

Cada parte destacada representa um pedaço do software que deverão ser construidos e testados.
Essa divisão torna possível o desenvolvimento em paralelo de cada parte.

Esse diagrama omite algumas operações que deverão ser feitas no banco de dados. Lembrem-se de implementar as operações com o banco de dados.

### Fluxo do Pedido
![diagrama-com](https://github.com/UNB-PI2-Grupo3-BracoRobotico/grabber-backend/assets/40258400/8e3cb9fd-d2ef-4610-ad36-b5eea070269d)
