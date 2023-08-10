import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from domain.ports.HTTPPort import HTTPPort
from domain.model import NewStereotypeInfo
from domain.ports.PersonServiceUseStereotypePort import PersonServiceNewStereotypePort

class HttpAdapter(HTTPPort):
    
    def __init__(self, host, port, service:PersonServiceNewStereotypePort):
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
        
        @router.post('/add_stereotype')
        async def add_stereotype(stereotype_info: NewStereotypeInfo):
            try:
                await self.service.add_stereotype(stereotype_info)
                return #jsonable_encoder(data)
            
            except Exception as exception:
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception))
            
            
        """ @router.get('/range')    
        async def get_range_by_id(id, data_type, start, end):
            try:
                data = self.service.get_range_by_id(id, data_type, start, end)
            
                return jsonable_encoder(data)
            
            except Exception as exception:
                if isinstance(exception, ValueError):
                    raise HTTPException(status_code=400, detail="wrong or missing parameters")
                else:
                    raise HTTPException(status_code=500, detail=str(exception)) """
                
        return router

from pydantic import BaseModel

class NewStereotype(BaseModel):
    name: str
    github_url: str | None = None
