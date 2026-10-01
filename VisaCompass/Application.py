from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from Agent import stream_query
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def serving_ui(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/stream")
async def stream_agent_response(request: QueryRequest):
    # FIX: Changed media_type to text/event-stream for SSE
    return StreamingResponse(
        stream_query(request.question),
        media_type="text/event-stream"
    )



