# grabber-backend
Backend repository for the robotic arm project


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

### Fluxo do Pedido
![diagrama-com](https://github.com/UNB-PI2-Grupo3-BracoRobotico/grabber-backend/assets/40258400/8e3cb9fd-d2ef-4610-ad36-b5eea070269d)
