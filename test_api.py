#!/usr/bin/env python3

import requests
import json
import sys
import time
from typing import List, Dict

BASE_URL = "http://localhost:8000"

def print_header(title: str):
    print("\n" + "="*60)
    print(f"[{title}]")
    print("="*60)

def print_response(response, operation):
    status_color = "OK" if response.status_code < 400 else "ERROR"
    print(f"\n{status_color} **{operation}**")
    print(f"   Status: {response.status_code}")
    
    if response.content:
        try:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except:
            print(f"   Response: {response.text}")
    else:
        print("   Response: (vazio)")
    print("-" * 50)

def test_api_info():
    print("Obtendo informações da API...")
    try:
        response = requests.get(f"{BASE_URL}/info")
        print_response(response, "Informações da API")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

def test_health_check():
    print("Testando health check avançado...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Check ")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

def test_initial_statistics():
    print("Verificando estatísticas iniciais...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/statistics")
        print_response(response, "Estatísticas Iniciais")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

def test_create_contacts():
    print("Testando criação de contatos com validação...")
    
    test_contacts = [
        {
            "name": "matheus costa silva",
            "phones": [
                {"number": "11999998888", "type": "mobile"},
                {"number": "(11) 3333-4444", "type": "fixo"}
            ],
            "category": "pessoal"
        },
        {
            "name": "EMPRESA DE TECNOLOGIA LTDA",
            "phones": [
                {"number": "1122223333", "type": "comercial"}
            ],
            "category": "comercial"
        },
        {
            "name": "ana de souza",
            "phones": [
                {"number": "85888887777", "type": "mobile"}
            ],
            "category": "familiar"
        }
    ]
    
    created_ids = []
    
    for i, contact in enumerate(test_contacts, 1):
        try:
            response = requests.post(f"{BASE_URL}/contacts/", json=contact)
            print_response(response, f"Criar Contato {i} (com validação)")
            if response.status_code == 201:
                created_ids.append(response.json()["id"])
        except Exception as e:
            print(f"Erro ao criar contato {i}: {e}")
    
    return created_ids

def test_search_functionality():
    print("Testando busca por nome...")
    
    search_terms = ["maria", "Silva", "LTDA", "ana"]
    
    for term in search_terms:
        try:
            response = requests.get(f"{BASE_URL}/contacts/search?name={term}")
            print_response(response, f"Buscar '{term}'")
        except Exception as e:
            print(f"Erro na busca por '{term}': {e}")

def test_advanced_statistics():
    print("Verificando estatísticas atualizadas...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/statistics")
        print_response(response, "Estatísticas Completas")
        
        if response.status_code == 200:
            stats = response.json()
            print("\n**Resumo das Estatísticas:**")
            print(f"   Total de contatos: {stats.get('total_contatos', 0)}")
            print(f"   Familiares: {stats.get('por_categoria', {}).get('familiar', 0)}")
            print(f"   Pessoais: {stats.get('por_categoria', {}).get('pessoal', 0)}")
            print(f"   Comerciais: {stats.get('por_categoria', {}).get('comercial', 0)}")
            print(f"   Telefones móveis: {stats.get('tipos_telefone', {}).get('mobile', 0)}")
            print(f"   Telefones fixos: {stats.get('tipos_telefone', {}).get('fixo', 0)}")
            print(f"   Telefones comerciais: {stats.get('tipos_telefone', {}).get('comercial', 0)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

def test_backup_functionality():
    print("Testando sistema de backup...")
    try:
        response = requests.get(f"{BASE_URL}/contacts/backup")
        print_response(response, "Backup Completo")
        
        if response.status_code == 200:
            backup_data = response.json()
            print(f"\n**Backup gerado com sucesso:**")
            print(f"   Data: {backup_data.get('export_timestamp', 'N/A')}")
            print(f"   Contatos exportados: {backup_data.get('total_contacts', 0)}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Erro: {e}")
        return False

def test_error_handling():
    print("Testando tratamento de erros...")
    
    try:
        response = requests.get(f"{BASE_URL}/contacts/999")
        print_response(response, "Buscar Contato Inexistente")
    except Exception as e:
        print(f"Erro: {e}")
    
    try:
        response = requests.get(f"{BASE_URL}/contacts/search?name=INEXISTENTE")
        print_response(response, "Busca Sem Resultados")
    except Exception as e:
        print(f"Erro: {e}")
    
    try:
        response = requests.get(f"{BASE_URL}/contacts/?category=pessoal")
        print_response(response, "Filtrar Categoria Específica")
    except Exception as e:
        print(f"Erro: {e}")

def test_validation_errors():
    print("Testando validações de dados...")
    
    invalid_contact1 = {
        "name": "A",
        "phones": [{"number": "11999998888", "type": "mobile"}],
        "category": "pessoal"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contacts/", json=invalid_contact1)
        print_response(response, "Teste Nome Muito Curto")
    except Exception as e:
        print(f"Erro: {e}")
    
    invalid_contact2 = {
        "name": "Teste Silva",
        "phones": [{"number": "123", "type": "mobile"}],
        "category": "pessoal"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/contacts/", json=invalid_contact2)
        print_response(response, "Teste Telefone Inválido")
    except Exception as e:
        print(f"Erro: {e}")

def show_final_summary():
    print_header("RESUMO FINAL DOS TESTES")
    print("Funcionalidades testadas:")
    print("   Health Check ")
    print("   Informações da API")
    print("   Sistema de Estatísticas")
    print("   Busca por Nome")
    print("   Criação com Validação Brasileira")
    print("   Sistema de Backup")
    print("   Tratamento de Erros")
    print("   Validações de Dados")
def main():
    print_header("API AGENDA DE CONTATOS  - TESTE COMPLETO")
    print("Iniciando bateria completa de testes...")
    
    test_results = []
    
    try:
        test_results.append(("API Info", test_api_info()))
        time.sleep(0.5)
        
        test_results.append(("Health Check", test_health_check()))
        time.sleep(0.5)
        
        test_results.append(("Estatísticas Iniciais", test_initial_statistics()))
        time.sleep(0.5)
        
        print_header("TESTE DE CRIAÇÃO COM VALIDAÇÕES")
        created_ids = test_create_contacts()
        test_results.append(("Criação de Contatos", len(created_ids) > 0))
        time.sleep(0.5)
        
        print_header("TESTE DE BUSCA POR NOME")
        test_search_functionality()
        time.sleep(0.5)
        
        print_header("ESTATÍSTICAS ATUALIZADAS")
        test_results.append(("Estatísticas", test_advanced_statistics()))
        time.sleep(0.5)
        
        print_header("TESTE DE BACKUP")
        test_results.append(("Backup", test_backup_functionality()))
        time.sleep(0.5)
        
        print_header("TESTE DE TRATAMENTO DE ERROS")
        test_error_handling()
        time.sleep(0.5)
        
        print_header("TESTE DE VALIDAÇÕES")
        test_validation_errors()
        time.sleep(0.5)
        
        show_final_summary()
        
        print("\n**RESULTADOS DOS TESTES:**")
        passed = sum(1 for _, result in test_results if result)
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "PASS" if result else "FAIL"
            print(f"   {status} {test_name}")
        
        print(f"\n**SCORE: {passed}/{total} testes passaram**")
        
        if passed == total:
            print("TODOS OS TESTES PASSARAM! API funcionando perfeitamente!")
        else:
            print("Alguns testes falharam. Verifique os logs acima.")
        
        return passed == total
        
    except requests.exceptions.ConnectionError:
        print("ERRO DE CONEXÃO!")
        print("Certifique-se de que a API está rodando:")
        print("   Execute: docker-compose up --build")
        print("   Ou: uvicorn app.main:app --reload")
        print(f"   URL esperada: {BASE_URL}")
        return False
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 