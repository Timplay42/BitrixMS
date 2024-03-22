from Leads.router import bitrix_router
from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()


app.include_router(router=bitrix_router)

if __name__ == '__main__':
    uvicorn.run("app:app")
