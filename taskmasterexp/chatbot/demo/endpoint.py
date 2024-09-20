from fastapi import APIRouter, Form, status

from .dependencies import DemoAgent

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/message", status_code=status.HTTP_200_OK)
async def get_message(agent: DemoAgent, message: str = Form(...)):
    response = await agent.ainvoke({"history": [], "text": message})
    return response["output"]
