from pydantic import BaseModel, Field
from typing import List

class Options(BaseModel):
    title:str
    description:str
    tangible_steps:List[str]

class References(BaseModel):
    title:str
    url:str

class ImmigrationResponse(BaseModel):
    verdict:str
    options:List[Options]
    mistakes_to_avoid:List[str]
    lawyer_questions:List[str]
    references:List[References]