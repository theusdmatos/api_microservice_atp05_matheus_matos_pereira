from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models.contact import Contact, ContactCreate, ContactUpdate, ContactStats
from ..models.enums import ContactCategory
from ..services.contact_service import contact_service

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=Contact, status_code=201)
async def create_contact(contact: ContactCreate):
    return contact_service.create_contact(contact)

@router.get("/statistics", response_model=ContactStats)
async def get_statistics():
    return contact_service.get_statistics()

@router.get("/search", response_model=List[Contact])
async def search_contacts(
    name: str = Query(..., min_length=2, description="Nome ou parte do nome para buscar")
):
    contacts = contact_service.search_contacts_by_name(name)
    if not contacts:
        raise HTTPException(status_code=404, detail=f"Nenhum contato encontrado com o nome '{name}'")
    return contacts

@router.get("/backup", response_model=dict)
async def backup_contacts():
    return contact_service.export_contacts()

@router.get("/{contact_id}", response_model=Contact)
async def get_contact(contact_id: int):
    contact = contact_service.get_contact(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contato com ID {contact_id} não encontrado")
    return contact

@router.get("/", response_model=List[Contact])
async def get_contacts(
    category: Optional[ContactCategory] = Query(None, description="Filtrar por categoria específica")
):
    if category:
        contacts = contact_service.get_contacts_by_category(category.value)
        if not contacts:
            raise HTTPException(
                status_code=404, 
                detail=f"Nenhum contato encontrado na categoria '{category.value}'"
            )
        return contacts
    return contact_service.get_all_contacts()

@router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, contact_update: ContactUpdate):
    contact = contact_service.update_contact(contact_id, contact_update)
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contato com ID {contact_id} não encontrado")
    return contact

@router.delete("/{contact_id}", status_code=204)
async def delete_contact(contact_id: int):
    success = contact_service.delete_contact(contact_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Contato com ID {contact_id} não encontrado") 