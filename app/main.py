from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .dependencies import validate_api_key, api_key_header
from json2table import convert
from typing import Union
import logging

app = FastAPI(
    title="pyJsonToTable",
    summary="From JSON to Table :^)",
    version="0.1.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://10.20.10.10:3003","http://10.20.10.10:3002"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.post("/pyJson2table/", tags=["Convertir JSON a HTML"])
def json2table(json_data: Union[dict, list] = Body(...,example={"person":{"name":"John Doe","age":30,"address":{"street":"123 Main Street","city":"Exampleville","zip_code":"12345"},"emails":["john.doe@example.com","j.doe@example.net"]},"items":[{"id":1,"name":"Item 1","price":10.99},{"id":2,"name":"Item 2","price":20.49}]}), authorized: bool = Depends(validate_api_key)):
    try:
        if isinstance(json_data, list):
            json_data = {"data": json_data}
        html_table = convert(json_data, build_direction="LEFT_TO_RIGHT", table_attributes={"style": "width:100%", "class": "table table-striped"})
        return {"html": html_table}
    except Exception as e:
        logging.error(f"Error converting JSON to table: {e}")
        raise HTTPException(status_code=500, detail=str(e))

logging.basicConfig(level=logging.INFO)
