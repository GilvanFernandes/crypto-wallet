# Crypto Wallet API

Uma API REST completa para gerenciamento de carteiras de criptomoedas, desenvolvida com FastAPI e MySQL. O sistema permite gerenciar endereços de Bitcoin e Ethereum, acompanhar transações, calcular saldos em tempo real com atualização automática de preços em USD e BRL, e sistema de notificações inteligente baseado em gatilhos de preço.

## 🚀 Funcionalidades

- **Autenticação JWT** - Sistema seguro de login e autenticação
- **Gerenciamento de Usuários** - Criação e atualização de perfis
- **Gerenciamento de Endereços** - Suporte para BTC e ETH
- **Acompanhamento de Transações** - Histórico completo de transações
- **Cálculo de Saldos** - Saldos em USD, BRL e criptomoedas atualizados automaticamente
- **Atualização Automática de Preços** - Integração com CoinGecko API (USD e BRL)
- **Sistema de Notificações** - Alertas baseados em gatilhos de preço
- **Logs de Notificações** - Histórico completo de alertas disparados
- **Documentação Interativa** - Swagger UI automático

## 📋 Pré-requisitos

- Python 3.9+
- MySQL 8.0+ (ou Docker)
- pipenv

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd crypto-wallet
```

### 2. Instale as dependências com pipenv
```bash
pipenv install
```

### 3. Ative o ambiente virtual
```bash
pipenv shell
```

### 4. Configure o banco de dados

#### Opção A: MySQL Local
```sql
CREATE DATABASE crypto_wallet;
```

#### Opção B: Docker MySQL
```bash
docker run --name mysql-crypto -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=crypto_wallet -p 3306:3306 -d mysql:8.0
```

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no `env.example`:
```bash
cp env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
DATABASE_URL=mysql+mysqlconnector://root:root@127.0.0.1:3306/crypto_wallet
SECRET_KEY=sua-chave-secreta-jwt
```

### 6. Execute as migrações (opcional)
```bash
alembic revision --autogenerate -m "create initial tables"
alembic upgrade head
```

### 7. Inicie a aplicação
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

A aplicação estará disponível em: http://127.0.0.1:8000

## 📚 Documentação da API

### Autenticação

A API usa autenticação JWT. Para acessar endpoints protegidos, você precisa:

1. Criar uma conta via `/users`
2. Fazer login via `/users/login`
3. Usar o token retornado no header `Authorization: Bearer <token>`

### Endpoints Disponíveis

#### 1. Criar Usuário
**POST** `/users`

Cria uma nova conta de usuário.

**Request:**
```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com",
  "is_active": true
}
```

#### 2. Login
**POST** `/users/login`

Faz login e retorna um token JWT.

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/users/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao@example.com&password=senha123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 3. Atualizar Dados do Usuário
**PUT** `/users/me`

Atualiza os dados do usuário logado.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Request:**
```json
{
  "name": "João Silva Atualizado",
  "email": "joao.novo@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "João Silva Atualizado",
  "email": "joao.novo@example.com",
  "is_active": true
}
```

#### 4. Criar Endereço
**POST** `/addresses`

Cria um novo endereço de criptomoeda para o usuário autenticado.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Request:**
```json
{
  "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "type": "BTC"
}
```

**Response:**
```json
{
  "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "type": "BTC"
}
```

#### 5. Listar Endereços
**GET** `/addresses`

Lista todos os endereços do usuário autenticado.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    "type": "BTC"
  },
  {
    "id": 2,
    "user_id": 1,
    "address": "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    "type": "ETH"
  }
]
```

#### 6. Ver Transações de um Endereço
**GET** `/addresses/{address_id}/transactions`

Lista todas as transações de um endereço específico.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
[
  {
    "id": 1,
    "address_id": 1,
    "tx_hash": "0x1234567890abcdef...",
    "amount": 0.5,
    "timestamp": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "address_id": 1,
    "tx_hash": "0xabcdef1234567890...",
    "amount": -0.1,
    "timestamp": "2024-01-15T11:45:00"
  }
]
```

#### 7. Ver Saldo de um Endereço
**GET** `/addresses/{address_id}/balance`

Calcula o saldo atual de um endereço em USD, BRL e criptomoeda.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
{
  "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
  "balance_usd": 25000.50,
  "balance_brl": 125000.25,
  "balance_crypto": 0.5,
  "crypto_type": "BTC"
}
```

#### 8. Criar Notificação
**POST** `/notifications`

Cria uma nova notificação de preço.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Request:**
```json
{
  "crypto_type": "BTC",
  "notification_type": ">=",
  "threshold_value": 100000.0
}
```

**Response:**
```json
{
  "id": 1,
  "crypto_type": "BTC",
  "notification_type": ">=",
  "threshold_value": 100000.0,
  "is_active": true,
  "created_at": "2024-01-15T12:00:00"
}
```

#### 9. Listar Notificações
**GET** `/notifications`

Lista todas as notificações do usuário.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
[
  {
    "id": 1,
    "crypto_type": "BTC",
    "notification_type": ">=",
    "threshold_value": 100000.0,
    "is_active": true,
    "created_at": "2024-01-15T12:00:00"
  },
  {
    "id": 2,
    "crypto_type": "ETH",
    "notification_type": "<=",
    "threshold_value": 2000.0,
    "is_active": false,
    "created_at": "2024-01-15T12:30:00"
  }
]
```

#### 10. Ativar/Desativar Notificação
**PUT** `/notifications/{notification_id}/toggle`

Ativa ou desativa uma notificação.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
{
  "message": "Notificação ativada com sucesso"
}
```

#### 11. Deletar Notificação
**DELETE** `/notifications/{notification_id}`

Remove uma notificação.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
{
  "message": "Notificação deletada com sucesso"
}
```

#### 12. Ver Logs de Notificações
**GET** `/notifications/logs`

Lista o histórico de notificações disparadas.

**Headers:**
```
Authorization: Bearer <seu_token_jwt>
```

**Response:**
```json
[
  {
    "id": 1,
    "crypto_type": "BTC",
    "current_price_usd": 104353.0,
    "current_price_brl": 521765.0,
    "threshold_value": 100000.0,
    "triggered_at": "2024-01-15T12:05:00"
  }
]
```

#### 13. Status do Sistema
**GET** `/prices/status`

Verifica o status do sistema e últimos preços atualizados.

**Response:**
```json
{
  "status": "online",
  "database": "connected",
  "price_updates": {
    "btc": {
      "price_usd": 104353.0,
      "price_brl": 521765.0,
      "last_updated": "2024-01-15T12:00:00"
    },
    "eth": {
      "price_usd": 2500.36,
      "price_brl": 12501.8,
      "last_updated": "2024-01-15T12:00:00"
    }
  },
  "timestamp": "2024-01-15T12:00:00"
}
```

#### 14. Health Check
**GET** `/health`

Verifica se a aplicação está funcionando.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T12:00:00"
}
```

## 🔧 Configuração

### Variáveis de Ambiente

Configure as seguintes variáveis no arquivo `.env`:

```env
DATABASE_URL=mysql+mysqlconnector://user:password@host:port/database
SECRET_KEY=sua-chave-secreta-jwt
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Atualização de Preços

O sistema atualiza automaticamente os preços de BTC e ETH a cada 5 minutos via CoinGecko API. Os preços são salvos em USD e BRL no banco de dados e usados para calcular saldos e verificar notificações.

### Sistema de Notificações

O sistema suporta os seguintes tipos de notificação:
- `>=` - Maior ou igual
- `<=` - Menor ou igual  
- `>` - Maior que
- `<` - Menor que
- `==` - Igual a

As notificações são verificadas automaticamente a cada atualização de preço e os logs são salvos quando as condições são atingidas.

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

- **users**: Usuários do sistema
- **addresses**: Endereços de criptomoedas
- **transactions**: Transações dos endereços
- **prices**: Histórico de preços das criptomoedas (USD e BRL)
- **notifications**: Notificações configuradas pelos usuários
- **notification_logs**: Histórico de notificações disparadas

### Relacionamentos

- Um usuário pode ter múltiplos endereços
- Um usuário pode ter múltiplas notificações
- Um endereço pode ter múltiplas transações
- Uma notificação pode ter múltiplos logs
- Preços são armazenados com timestamp para histórico

## 📁 Estrutura do Projeto

```
crypto-wallet/
├── alembic/                 # Migrações do banco de dados
├── api/
│   └── routers/            # Endpoints da API
│       ├── users.py        # Gerenciamento de usuários
│       ├── addresses.py    # Gerenciamento de endereços
│       ├── notifications.py # Sistema de notificações
│       └── prices.py       # Preços e status
├── services/               # Serviços da aplicação
│   ├── notification_service.py # Lógica de notificações
│   └── price_service.py    # Atualização de preços
├── config.py              # Configurações da aplicação
├── dependencies.py        # Dependências e autenticação
├── models.py              # Modelos do banco de dados
├── schemas.py             # Schemas Pydantic
├── main.py               # Aplicação principal
├── Pipfile               # Dependências Python
├── docker-compose.yml    # Configuração Docker
└── README.md             # Documentação
```

## 🚀 Executando em Produção

### Com Docker

```bash
# Build da imagem
docker build -t crypto-wallet .

# Executar container
docker run -p 8000:8000 crypto-wallet
```

### Com Docker Compose

```bash
# Executar com docker-compose
docker-compose up -d
```

### Com Gunicorn

```bash
pipenv install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Logs

A aplicação gera logs detalhados incluindo:
- Inicialização do sistema
- Atualizações de preços (USD e BRL)
- Verificação de notificações
- Logs de notificações disparadas
- Erros de conexão
- Operações de banco de dados

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Tokens JWT com expiração configurável
- Validação de entrada com Pydantic
- Proteção contra SQL injection via SQLAlchemy
- Autenticação obrigatória para endpoints sensíveis
- Verificação de propriedade de recursos (usuário só acessa seus próprios dados)

## 🎯 Funcionalidades Avançadas

### Sistema de Notificações Inteligente

- **Gatilhos Personalizados**: Configure alertas baseados em preços específicos
- **Múltiplas Condições**: Suporte para >=, <=, >, <, ==
- **Verificação Automática**: Sistema roda em background sem interferir na API
- **Histórico Completo**: Logs de todas as notificações disparadas
- **Ativação/Desativação**: Controle total sobre suas notificações

### Preços em Tempo Real

- **Dual Currency**: Preços em USD e BRL simultaneamente
- **Atualização Automática**: A cada 5 minutos via CoinGecko API
- **Cálculo de Saldos**: Saldos em USD, BRL e criptomoedas
- **Histórico de Preços**: Armazenamento completo para análise

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

**Desenvolvido com ❤️ usando FastAPI, SQLAlchemy e MySQL** 