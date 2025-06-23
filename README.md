### API Agenda de Contatos - FastAPI

**ATP #05 - Implementação de microsserviços**

### Operações Básicas
- **Criar Contato** - Adicionar novo contato à agenda
- **Buscar Contato** - Consultar contato por ID
- **Listar Contatos** - Visualizar todos os contatos cadastrados
- **Atualizar Contato** - Modificar dados de contato existente
- **Deletar Contato** - Remover contato da agenda

### Dados Pré-carregados
A API já vem com **6 contatos de exemplo** para demonstração imediata

## Modelo de Dados

### Contato
- **nome**: Nome completo (formatação inteligente automática)
- **telefones**: Lista de números com tipos (máximo 5, formato brasileiro)
- **categoria**: Categoria do contato

### Tipos de Telefone (Enum)
- **mobile** - Celular
- **fixo** - Telefone fixo residencial  
- **comercial** - Telefone comercial/empresarial

### Categorias de Contato (Enum)
- **familiar** - Contatos da família
- **pessoal** - Contatos pessoais
- **comercial** - Contatos comerciais/profissionais

## Como Executar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+ 

### 1. Executar com Docker (Recomendado)
```bash
# Construir e executar
docker-compose up --build

# Em background
docker-compose up --build -d
```

### 2. Executar Localmente
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar API
uvicorn app.main:app --reload
```

### 3. Verificar Funcionamento
**Acesse:** http://localhost:8000

## Documentação e Recursos
| Recurso | URL | Descrição |
|---------|-----|-----------|
| **Página Inicial** | http://localhost:8000/ | Interface web  |
| **Swagger UI** | http://localhost:8000/docs | Documentação interativa |
| **ReDoc** | http://localhost:8000/redoc | Documentação técnica |
| **Estatísticas** | http://localhost:8000/contacts/statistics | Dashboard de dados |
| **Backup** | http://localhost:8000/contacts/backup | Export completo |
| **Health Check** | http://localhost:8000/health | Status avançado |
| **Info** | http://localhost:8000/info | Informações técnicas |

## Executar Testes 

### Script Automatizado Completo
```bash
# Instalar requests (se necessário)
pip install requests

# Executar bateria completa de testes
python test_api.py
```

**O script testa:**
- Health check avançado
- Informações da API
- Dados pré-carregados
- Validação brasileira de telefones
- Formatação inteligente de nomes
- Sistema de busca
- Dashboard de estatísticas
- Sistema de backup
- Tratamento de erros
- Validações de dados

## Endpoints da API 

### Operações CRUD Básicas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/contacts/` | Criar novo contato |
| GET | `/contacts/{id}` | Buscar contato por ID |
| GET | `/contacts/` | Listar todos os contatos |
| PUT | `/contacts/{id}` | Atualizar contato |
| DELETE | `/contacts/{id}` | Deletar contato |

### Funcionalidades 
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/contacts/search?name={nome}` | Busca por nome |
| GET | `/contacts/statistics` | Dashboard completo |
| GET | `/contacts/backup` | Export de dados |
| GET | `/contacts/?category={categoria}` | Filtrar categoria |

### Sistema e Informações
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Página inicial  |
| GET | `/health` | Health check avançado |
| GET | `/info` | Informações técnicas |

## Exemplos de Uso

### Criar Contato com Validação Brasileira
```bash
curl -X POST "http://localhost:8000/contacts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wesley Krebs",
    "phones": [
      {"number": "19999998888", "type": "mobile"},
      {"number": "1933334444", "type": "fixo"}
    ],
    "category": "pessoal"
  }'
```

**Resultado:** Nome formatado para "João da Silva" e telefones para "(00) 00000-0000" e "(00) 0000-0000"

### Buscar por Nome
```bash
curl "http://localhost:8000/contacts/search?name=Silva"
```

### Ver Dashboard de Estatísticas
```bash
curl "http://localhost:8000/contacts/statistics"
```

### Exportar Backup Completo
```bash
curl "http://localhost:8000/contacts/backup"
```

## Arquitetura 

```
api_microservice/
├── app/
│   ├── models/
│   │   ├── contact.py
│   │   └── enums.py
│   ├── services/
│   │   └── contact_service.py
│   ├── routes/
│   │   └── contacts.py
│   └── main.py
├── test_api.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Tecnologias e Bibliotecas

- **FastAPI 0.104.1** - Framework web moderno
- **Pydantic 2.5.0** - Validação de dados
- **Uvicorn 0.24.0** - Servidor ASGI
- **Docker** - Containerização
- **Python 3.11** - Linguagem base

### Funcionalidades de Monitoramento
- Health check com status detalhado
- Endpoint de informações técnicas
- Métricas em tempo real
- Timestamps de operações
---