from dataclasses import dataclass

@dataclass
class db_creds:
    username: str
    password: str
    host: str
    database: str
    
    