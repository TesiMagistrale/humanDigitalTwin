import asyncio
import json
from typing import Optional, Type, Dict, Any
import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from domain.ports.HTTPPort import HTTPPort
from domain.ports.PersonServiceGeneralPort import PersonServiceGeneralPort
import traceback


from pydantic import BaseModel

class Stereotype(BaseModel):
    name: str
    data: Optional[Dict[str, Any]]
    
class UserData(BaseModel):
    data_name: str
    data_value: Any

class HttpAdapter(HTTPPort):
    
    def __init__(self, host, port, service: PersonServiceGeneralPort):
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
        
        self._user_routes(router=router)
        self._stereotypes_routes(router=router)

        return router

    def _user_routes(self, router: APIRouter):
        @router.get('/user/general_data', status_code=200)  
        async def general_data():
            try: 
                return jsonable_encoder(self.service.get_general_data())
            
            except Exception as exception:
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(exception))
            
        @router.post('/user/general_data', status_code=201)  
        async def add_general_data(data: UserData):
            try: 
                self.service.add_general_data(data.data_name, data.data_value)
                return jsonable_encoder({})
            
            except Exception as exception:
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
        
        @router.put('/user/general_data', status_code=204)  
        async def update_general_data(data: UserData):
            try: 
                self.service.update_general_data(data.data_name, data.data_value)
                return 
            
            except Exception as exception:
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
                
        @router.get('/user/characteristics', status_code=200)  
        async def characteristics():
            try: 
                return jsonable_encoder(self.service.get_characteristics())
            
            except Exception as exception:
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(exception))
            
        @router.post('/user/characteristics', status_code=201)  
        async def add_characteristics(data: UserData):
            try: 
                self.service.add_characteristics(data.data_name, data.data_value)
                return jsonable_encoder({})
            
            except Exception as exception:
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
        
        @router.put('/user/characteristics', status_code=204)  
        async def update_characteristics(data: UserData):
            try: 
                self.service.update_characteristics(data.data_name, data.data_value)
                return 
            
            except Exception as exception:
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
        
            
        @router.get('/user/sensors', status_code=200)  
        async def sensors():
            try: 
                return jsonable_encoder(self.service.get_sensors())
            
            except Exception as exception:
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(exception))
            
        @router.get('/user/state', status_code=200)  
        async def state():
            try: 
                return jsonable_encoder(self.service.get_actual_state())
            
            except Exception as exception:
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(exception))
            
    def _stereotypes_routes(self, router: APIRouter):
        @router.post('/stereotype/add', status_code=201)
        async def add_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.add_stereotype(json.loads(stereotype_info.model_dump_json()))
                return jsonable_encoder({})
        
            except Exception as exception:
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
   
        
        @router.post('/stereotype/start', status_code=204)  
        async def start_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.start_stereotype(stereotype_info.name, stereotype_info.data)
                return 
            
            except Exception as exception:
                import traceback
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
                
        @router.post('/stereotype/stop', status_code=204)  
        async def stop_stereotype(stereotype_info: Stereotype):
            try:
                await self.service.stop_stereotype(stereotype_info.name, stereotype_info.data)
                return 
            
            except Exception as exception:
                
                traceback.print_exc()
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
