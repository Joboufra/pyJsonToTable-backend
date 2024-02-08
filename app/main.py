from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import validate_api_key, api_key_header
from json2table import convert
from typing import Union
import logging
import logging.handlers
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM


# Configuración de logging
logger = logging.getLogger("uvicorn.access")
logger.setLevel(logging.INFO)
handler = logging.handlers.RotatingFileHandler("/home/joboufra/actions-jsontotable-backend/deploy/access.log", maxBytes=100000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configuración de Elastic APM
apm_config = {
    'SERVICE_NAME': 'json2table',
    'SERVER_URL': 'http://10.20.10.10:8200',
}
apm_client = make_apm_client(apm_config)

# App
app = FastAPI(
    title="pyJsonToTable",
    summary="From JSON to Table :^)",
    version="0.1.1",
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
app.add_middleware(ElasticAPM, client=apm_client)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://10.20.10.10:3003",
        "http://10.20.10.10:8000", 
        "https://jsontotable.joboufra.es"
    ], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.post("/api/pyJson2table/", tags=["Convertir JSON a HTML"])
def json2table(json_data: Union[dict, list] = Body(...,example={"person":{"name":"John Doe","age":30,"address":{"street":"123 Main Street","city":"Exampleville","zip_code":"12345"},"emails":["john.doe@example.com","j.doe@example.net"]},"items":[{"id":1,"name":"Item 1","price":10.99},{"id":2,"name":"Item 2","price":20.49}]}), authorized: bool = Depends(validate_api_key)):
    logger.info("Recibida petición en /api/pyJson2table/")
    try:
        if isinstance(json_data, list):
            json_data = {"data": json_data}
        html_table = convert(json_data, build_direction="LEFT_TO_RIGHT", table_attributes={"style": "width:100%", "class": "table table-striped"})
        logger.info("Petición procesada con éxito")
        return {"html": html_table}
    except Exception as e:
        logger.error(f"Error convirtiendo JSON a tabla: {e}")
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.INFO)
