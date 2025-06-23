from enum import Enum

class PhoneType(str, Enum):
    MOBILE = "celular"
    LANDLINE = "fixo"
    COMMERCIAL = "comercial"

class ContactCategory(str, Enum):
    FAMILY = "familiar"
    PERSONAL = "pessoal"
    COMMERCIAL = "comercial" 