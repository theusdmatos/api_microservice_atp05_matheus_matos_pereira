from pydantic import BaseModel, Field, validator
from typing import List, Optional
from .enums import PhoneType, ContactCategory
import re

class Phone(BaseModel):
    number: str = Field(..., description="Número de telefone brasileiro")
    type: PhoneType = Field(..., description="Tipo do telefone")
    
    @validator('number')
    def validate_phone_number(cls, v):
        numbers_only = re.sub(r'[^\d]', '', v)
        
        if len(numbers_only) < 8 or len(numbers_only) > 11:
            raise ValueError('Número de telefone deve ter entre 8 e 11 dígitos')
        
        if len(numbers_only) == 11:
            formatted = f"({numbers_only[:2]}) {numbers_only[2:7]}-{numbers_only[7:]}"
        elif len(numbers_only) == 10:
            formatted = f"({numbers_only[:2]}) {numbers_only[2:6]}-{numbers_only[6:]}"
        elif len(numbers_only) == 9:
            formatted = f"{numbers_only[:5]}-{numbers_only[5:]}"
        elif len(numbers_only) == 8:
            formatted = f"{numbers_only[:4]}-{numbers_only[4:]}"
        else:
            formatted = v
        
        return formatted

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome do contato")
    phones: List[Phone] = Field(..., min_items=1, max_items=5, description="Lista de telefones (máximo 5)")
    category: ContactCategory = Field(..., description="Categoria do contato")
    
    @validator('name')
    def validate_name(cls, v):
        name = ' '.join(v.strip().split())
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\.]+$', name):
            raise ValueError('Nome deve conter apenas letras, espaços, hífens e pontos')
        
        prepositions = ['de', 'da', 'do', 'das', 'dos', 'e']
        words = name.lower().split()
        capitalized_words = []
        
        for i, word in enumerate(words):
            if i == 0 or word not in prepositions:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)
        
        return ' '.join(capitalized_words)

class ContactUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do contato")
    phones: Optional[List[Phone]] = Field(None, min_items=1, max_items=5, description="Lista de telefones")
    category: Optional[ContactCategory] = Field(None, description="Categoria do contato")
    
    @validator('name')
    def validate_name(cls, v):
        if v is None:
            return v
        
        name = ' '.join(v.strip().split())
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s\-\.]+$', name):
            raise ValueError('Nome deve conter apenas letras, espaços, hífens e pontos')
        
        prepositions = ['de', 'da', 'do', 'das', 'dos', 'e']
        words = name.lower().split()
        capitalized_words = []
        
        for i, word in enumerate(words):
            if i == 0 or word not in prepositions:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word)
        
        return ' '.join(capitalized_words)

class Contact(BaseModel):
    id: int = Field(..., description="ID único do contato")
    name: str = Field(..., description="Nome do contato")
    phones: List[Phone] = Field(..., description="Lista de telefones")
    category: ContactCategory = Field(..., description="Categoria do contato")

    class Config:
        json_encoders = {
            PhoneType: lambda v: v.value,
            ContactCategory: lambda v: v.value,
        }

class ContactStats(BaseModel):
    total_contatos: int = Field(..., description="Total de contatos cadastrados")
    por_categoria: dict = Field(..., description="Quantidade por categoria")
    tipos_telefone: dict = Field(..., description="Quantidade por tipo de telefone")
    contatos_multiplos_telefones: int = Field(..., description="Contatos com múltiplos telefones")
    ultima_atualizacao: str = Field(..., description="Timestamp da última atualização") 