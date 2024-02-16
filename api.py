import os
from fastapi import FastAPI, UploadFile, HTTPException, Form
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],  
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)
supabase_url ="https://vdwflvvpfqtrtffuecsg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZkd2ZsdnZwZnF0cnRmZnVlY3NnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDc1MzAzMTQsImV4cCI6MjAyMzEwNjMxNH0.BnAsKyXhGIyHxUimXzM7KjfEVaPn9koMDA62iwRUmVY"

supabase_client = create_client(supabase_key=supabase_key, supabase_url=supabase_url)

class CreateTaskQuery(BaseModel):
    query: str



@app.post("/createTask")
async def conversation(query_obj:CreateTaskQuery):
    response = await supabase_client.from_table("tasks").upsert({"task":query_obj.query})
    
    
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Failed to create task")
    return response.json()
    