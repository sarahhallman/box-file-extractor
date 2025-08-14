from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from boxsdk import Client, OAuth2
from datetime import datetime
import csv, io

app = FastAPI()

class BoxRequest(BaseModel):
    access_token: str
    folder_id: str

class FileRequest(BaseModel):
    access_token: str
    file_id: str

class ColumnRequest(BaseModel):
    content: str
    columns: List[int]

@app.post("/get-file-id")
def get_file_id(req: BoxRequest):
    oauth = OAuth2(client_id=None, client_secret=None, access_token=req.access_token)
    client = Client(oauth)

    items = client.folder(folder_id=req.folder_id).get_items(fields=['id', 'type', 'created_at'])
    files = [item for item in items if item.type == 'file']
    files.sort(key=lambda x: datetime.fromisoformat(x.created_at.replace('Z', '+00:00')), reverse=True)

    if not files:
        raise HTTPException(status_code=404, detail="No files found.")

    return {"file_id": files[0].id}

@app.post("/get-file-content")
def get_file_content(req: FileRequest):
    oauth = OAuth2(client_id=None, client_secret=None, access_token=req.access_token)
    client = Client(oauth)

    content = client.file(req.file_id).content().decode('utf-8')
    return {"content": content}

@app.post("/extract-columns")
def extract_columns(req: ColumnRequest):
    reader = csv.reader(io.StringIO(req.content))
    headers = next(reader)
    selected = []

    for row in reader:
        if len(row) >= max(req.columns) + 1:
            selected.append({headers[i]: row[i] for i in req.columns})

    return selected
