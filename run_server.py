import uvicorn

if __name__ == "__main__":
    print("AI 은행원 백엔드 서버를 시작합니다...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 