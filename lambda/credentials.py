from dataclasses import dataclass
import string

@dataclass
class db_creds:
    username: str
    password: str
    host: str
    database: str
    
    