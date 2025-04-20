from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from pydantic import BaseModel
import asyncio
from bank_teller_agent import BankTellerAgent

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 은행원 에이전트 인스턴스 생성
bank_teller = BankTellerAgent()

# WebSocket 연결 관리
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "position_update":
                # 고객 위치 업데이트 처리
                response = bank_teller.update(customer_position=message["position"])
                await websocket.send_json(response)
            
            elif message["type"] == "dialogue":
                # 고객 대화 처리
                response = bank_teller.update(customer_query=message["text"])
                await websocket.send_json(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()

# API 엔드포인트
class DialogueRequest(BaseModel):
    text: str

@app.post("/api/dialogue")
async def dialogue(request: DialogueRequest):
    response = bank_teller.update(customer_query=request.text)
    return response

@app.get("/")
async def root():
    return {"message": "AI 은행원 백엔드 서버가 실행 중입니다."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 