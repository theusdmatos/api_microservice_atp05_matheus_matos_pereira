from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from .routes import contacts
import datetime

app = FastAPI(
    title="API Agenda de Contatos - FastAPI",
    description="""
## API para gerenciamento de agenda de contatos

Esta API permite gerenciar uma agenda de contatos com as seguintes funcionalidades:

### Funcionalidades principais:
- **Criar contatos** com nome, telefones e categoria
- **Listar todos os contatos** ou filtrar por categoria
- **Buscar contatos** por nome (busca parcial)
- **Atualizar e deletar** contatos existentes
- **Visualizar estatísticas** da agenda
- **Exportar dados** em formato JSON

### Tipos de telefone suportados:
- `mobile` - Celular
- `landline` - Fixo residencial
- `commercial` - Comercial/empresarial

### Categorias de contato:
- `family` - Família
- `personal` - Pessoal
- `commercial` - Comercial/trabalho

### Validação de telefones:
A API valida automaticamente números de telefone brasileiros e aceita formatos como:
- (11) 99999-9999
- 11999999999
- +5511999999999

---
**Desenvolvido por:** Matheus de Matos Pereira - RA: 592176  
**Projeto:** ATP#05 - Implementação de microsserviços REST com FastAPI
    """,
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(contacts.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Agenda de Contatos - Matheus</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
                color: #F8FAFC;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 2rem;
            }}
            
            .container {{
                max-width: 600px;
                text-align: center;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 3rem;
                backdrop-filter: blur(10px);
            }}
            
            .title {{
                font-size: 3rem;
                font-weight: 800;
                background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 50%, #06B6D4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 1rem;
                letter-spacing: -0.02em;
            }}
            
            .subtitle {{
                font-size: 1.25rem;
                color: #94A3B8;
                font-weight: 500;
                margin-bottom: 2rem;
            }}
            
            .status-badge {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(34, 197, 94, 0.1);
                border: 1px solid rgba(34, 197, 94, 0.3);
                color: #22C55E;
                padding: 0.75rem 1.5rem;
                border-radius: 50px;
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 3rem;
            }}
            
            .status-dot {{
                width: 8px;
                height: 8px;
                background: #22C55E;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
            }}
            
            .actions {{
                display: flex;
                justify-content: center;
                gap: 1rem;
                margin-bottom: 3rem;
                flex-wrap: wrap;
            }}
            
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 1rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s ease;
                border: 1px solid transparent;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #3B82F6, #1D4ED8);
                color: white;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
            }}
            
            .btn-secondary {{
                background: rgba(255, 255, 255, 0.05);
                color: #F1F5F9;
                border-color: rgba(255, 255, 255, 0.2);
            }}
            
            .btn-secondary:hover {{
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(-2px);
            }}
            
            .stats-info {{
                color: #94A3B8;
                font-size: 1rem;
                margin-bottom: 2rem;
            }}
            
            .footer {{
                color: #64748B;
                font-size: 0.9rem;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 2rem;
            }}
            
            @media (max-width: 768px) {{
                .title {{ font-size: 2.5rem; }}
                .container {{ padding: 2rem; margin: 1rem; }}
                .actions {{ flex-direction: column; align-items: center; }}
                .btn {{ width: 100%; justify-content: center; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">API Agenda de Contatos - FastAPI</h1>
            <p class="subtitle">Microsserviço REST</p>
            
            <div class="status-badge">
                <div class="status-dot"></div>
                Sistema Online
            </div>
            
            <div class="actions">
                <a href="/docs" class="btn btn-primary">
                    <i class="fas fa-book"></i>
                    Documentação Interativa
                </a>
                <a href="/contacts/statistics" class="btn btn-secondary">
                    <i class="fas fa-chart-line"></i>
                    Ver Estatísticas
                </a>
                <a href="/redoc" class="btn btn-secondary">
                    <i class="fas fa-file-alt"></i>
                    Documentação Técnica
                </a>
            </div>
            
            <div class="stats-info">
                <strong>Online desde:</strong> {datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")} • 
                <strong>Versão:</strong> 0.0.1
            </div>
            
            <div class="footer">
                <p>Desenvolvido por Matheus de Matos Pereira</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/health")
async def health_check():
    """
    Verificar o status de saúde da API.
    
    Retorna informações sobre:
    - Status da API (healthy/unhealthy)
    - Versão atual
    - Timestamp da verificação
    - Número total de contatos
    - Funcionalidades disponíveis
    """
    from .services.contact_service import contact_service
    
    stats = contact_service.get_statistics()
    
    return {
        "status": "healthy",
        "service": "contacts-api",
        "version": "0.0.1",
        "timestamp": datetime.datetime.now().isoformat(),
        "uptime": "API está funcionando perfeitamente!",
        "database_status": "in-memory (mock) - funcionando",
        "contacts_count": stats["total_contatos"],
        "features": [
            "CRUD Completo",
            "Busca por Nome",
            "Estatísticas",
            "Sistema de Backup",
            "Validação Brasileira"
        ]
    }

@app.get("/info")
async def api_info():
    """
    Obter informações técnicas detalhadas da API.
    
    Inclui informações sobre:
    - Nome e versão da API
    - Framework utilizado
    - Funcionalidades implementadas
    - Número total de endpoints
    - Data da última atualização
    """
    return {
        "api_name": "API Agenda de Contatos",
        "version": "0.0.1",
        "framework": "FastAPI",
        "python_version": "3.11+",
        "features": {
            "validation": "Pydantic com validações brasileiras",
            "storage": "In-memory (para demonstração)",
            "documentation": "Swagger UI + ReDoc",
            "containerization": "Docker + Docker Compose"
        },
        "endpoints": {
            "total": 9,
            "categories": ["CRUD", "Search", "Stats", "Backup", "Health"]
        },
        "last_updated": datetime.datetime.now().isoformat()
    } 