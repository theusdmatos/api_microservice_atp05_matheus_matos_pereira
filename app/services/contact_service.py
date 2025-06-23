from typing import List, Optional, Dict
from ..models.contact import Contact, ContactCreate, ContactUpdate, Phone
from ..models.enums import PhoneType, ContactCategory
import json
from datetime import datetime

class ContactService:
    def __init__(self):
        self._contacts: Dict[int, Contact] = {}
        self._next_id = 1
        self._load_sample_data()
    
    def _load_sample_data(self):
        sample_contacts = [
            ContactCreate(
                name="João Arantes",
                phones=[
                    Phone(number="(19) 99230-7095", type=PhoneType.MOBILE),
                    Phone(number="(19) 3324-8418", type=PhoneType.LANDLINE)
                ],
                category=ContactCategory.FAMILY
            ),
            ContactCreate(
                name="Arantes LTDA",
                phones=[
                    Phone(number="(19) 99330-7093", type=PhoneType.COMMERCIAL),
                    Phone(number="(19) 3424-8414", type=PhoneType.COMMERCIAL)
                ],
                category=ContactCategory.COMMERCIAL
            ),
            ContactCreate(
                name="Vera Bagnara",
                phones=[
                    Phone(number="(19) 99330-7092", type=PhoneType.MOBILE)
                ],
                category=ContactCategory.PERSONAL
            ),
            ContactCreate(
                name="Carlos Silva",
                phones=[
                    Phone(number="(19) 99440-7094", type=PhoneType.MOBILE),
                    Phone(number="(19) 3524-8415", type=PhoneType.LANDLINE)
                ],
                category=ContactCategory.FAMILY
            ),
            ContactCreate(
                name="Bagnara Brasil",
                phones=[
                    Phone(number="(19) 99554-7095", type=PhoneType.COMMERCIAL)
                ],
                category=ContactCategory.COMMERCIAL
            ),
            ContactCreate(
                name="Andreize Cristina",
                phones=[
                    Phone(number="(19) 99556-7096", type=PhoneType.MOBILE)
                ],
                category=ContactCategory.PERSONAL
            )
        ]
        
        for contact_data in sample_contacts:
            self.create_contact(contact_data)
    
    def create_contact(self, contact_data: ContactCreate) -> Contact:
        contact = Contact(
            id=self._next_id,
            name=contact_data.name,
            phones=contact_data.phones,
            category=contact_data.category
        )
        self._contacts[self._next_id] = contact
        self._next_id += 1
        return contact
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        return self._contacts.get(contact_id)
    
    def get_all_contacts(self) -> List[Contact]:
        return list(self._contacts.values())
    
    def search_contacts_by_name(self, name_query: str) -> List[Contact]:
        name_query = name_query.lower().strip()
        return [
            contact for contact in self._contacts.values()
            if name_query in contact.name.lower()
        ]
    
    def update_contact(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        if contact_id not in self._contacts:
            return None
        
        contact = self._contacts[contact_id]
        update_data = contact_data.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(contact, field, value)
        
        return contact
    
    def delete_contact(self, contact_id: int) -> bool:
        if contact_id in self._contacts:
            del self._contacts[contact_id]
            return True
        return False
    
    def get_contacts_by_category(self, category: str) -> List[Contact]:
        return [contact for contact in self._contacts.values() 
                if contact.category.value == category]
    
    def get_statistics(self) -> Dict:
        total_contacts = len(self._contacts)
        
        category_stats = {}
        for category in ContactCategory:
            count = len([c for c in self._contacts.values() if c.category == category])
            category_stats[category.value] = count
        
        phone_type_stats = {}
        for phone_type in PhoneType:
            count = 0
            for contact in self._contacts.values():
                count += len([p for p in contact.phones if p.type == phone_type])
            phone_type_stats[phone_type.value] = count
        
        multi_phone_contacts = len([c for c in self._contacts.values() if len(c.phones) > 1])
        
        return {
            "total_contatos": total_contacts,
            "por_categoria": category_stats,
            "tipos_telefone": phone_type_stats,
            "contatos_multiplos_telefones": multi_phone_contacts,
            "ultima_atualizacao": datetime.now().isoformat()
        }
    
    def export_contacts(self) -> Dict:
        contacts_data = []
        for contact in self._contacts.values():
            contact_dict = {
                "id": contact.id,
                "name": contact.name,
                "phones": [{"number": p.number, "type": p.type.value} for p in contact.phones],
                "category": contact.category.value
            }
            contacts_data.append(contact_dict)
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "total_contacts": len(contacts_data),
            "contacts": contacts_data
        }

contact_service = ContactService() 