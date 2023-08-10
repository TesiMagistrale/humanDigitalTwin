import asyncio
import json
from typing import Optional, Type, Dict, Any
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from domain.ports.HTTPPort import HTTPPort
from domain.model.PersonService import PersonService

from pydantic import BaseModel

class Stereotype(BaseModel):
    name: str
    data: Optional[Dict[str, Any]]

class HttpAdapter(HTTPPort):
    
    def __init__(self, host, port, service: Type[PersonService]):
        self.host = host
        self.port = port
        self.service = service
        
        self.setup()
        
    def setup(self):
        self.app = FastAPI()
        self.app.include_router(self._router())
        
    def run(self):
        uvicorn.run(self.app, host=self.host, port=self.port)



    def _router(self):
       
        router = APIRouter()
        
        @router.post('/stereotype/add', status_code=201)
        async def add_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.add_stereotype(json.loads(stereotype_info.model_dump_json()))
                return jsonable_encoder({})
        
            except Exception as exception:
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
   
        
        @router.post('/stereotype/start', status_code=200)  
        async def start_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.start_stereotype(stereotype_info.name, stereotype_info.data)
                return jsonable_encoder({})
            
            except Exception as exception:
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
                
        @router.post('/stereotype/stop', status_code=200)  
        async def stop_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.stop_stereotype(stereotype_info.name, stereotype_info.data)
                return jsonable_encoder({})
            
            except Exception as exception:
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
                
        return router


