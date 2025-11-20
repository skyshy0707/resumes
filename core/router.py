from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Depends, Query, Path, Request, status
from fastapi.security import HTTPBasic

from core import crud, dependencies
from core.schemes import params, schemes



class CustomHTTPBasic(HTTPBasic):

    async def __call__(self, request: Request):
        model: schemes.BaseModel = await super().__call__(request)
        return schemes.BasicAuth(**model.model_dump())
    
security = CustomHTTPBasic()

class Router:

    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()



    def setup_routes(self):
        pass

class ServerAPI(Router):

    def setup_routes(self):

        @self.router.post(
            "/registration", 
            response_model=schemes.OrdinaryIdResponse, 
            status_code=status.HTTP_201_CREATED
        )
        async def registration(credentials: Annotated[schemes.HTTPBasicCredentials, Depends(security)]):
            return await crud.registration(credentials)
        
        @self.router.put(
            "/signup", 
            response_model=schemes.UserJWTTokenResponse,
            status_code=status.HTTP_201_CREATED
        )
        async def signup(request: Request, credentials: Annotated[schemes.HTTPBasicCredentials, Depends(security)]):
            return await crud.signup(request, credentials)
        
        @self.router.put(
            "/refresh-token"
        )
        async def refresh_token(
            request: Request, 
            user_id: Annotated[int, Depends(dependencies.authorize)]
        ):
            return await crud.get_refresh_token(request, user_id)


        
        @self.router.get(
            "/resumes", 
            response_model=schemes.create_pagination_response_model(schemes.ResumeViewResponse),
        )
        async def get_resumes(
            request: Request, 
            user_id: Annotated[int, Depends(dependencies.authorize)],
            params: params.SearchResume = Depends()
        ):
            return await crud.get_user_resumes(user_id, params)
        

        @self.router.get(
            "/resume{id}/view",
            response_model=schemes.ResumeViewResponse
        )
        async def get_resume(
            request: Request,
            access: dependencies.grant_access_resume,
            id: int
        ):
            return await crud.get_resume(id)
        
        @self.router.patch(
            "/resume{id}/edit", 
            response_model=schemes.ResumeViewResponse
        )
        async def edit_resume(
            request: Request,
            access: dependencies.grant_access_resume,
            resume: schemes.ResumeEditRequest,
            id: int,
        ):
            return await crud.edit_resume(id, resume)
        
        @self.router.post(
            "/resume/create",
            response_model=schemes.OrdinaryIdResponse
        )
        async def create_resume(
            request: Request,
            user_id: Annotated[int, Depends(dependencies.authorize)],
            resume: schemes.ResumeCreateRequest
        ):
            return await crud.create_resume(resume)
        
        @self.router.delete(
            "/resume{id}/delete",
            response_model=schemes.OrdinaryIdResponse
        )
        async def delete_resume(
            request: Request,
            access: dependencies.grant_access_resume,
            id: int
        ):
            return await crud.delete_resume(id)



service = ServerAPI()