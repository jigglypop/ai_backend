# AI 은행원 백엔드 서버

이 백엔드 서버는 AI 은행원 시스템의 핵심 기능을 제공합니다. FastAPI를 기반으로 하며 웹소켓을 통해 실시간 통신도 지원합니다.

## 기능

- 은행원 에이전트 기본 행동 제어
- 고객 대화 처리 및 응답 생성
- 고객과의 상호작용 관리
- 실시간 위치 및 상태 업데이트

## 설치 방법

1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

1. 서버 실행

```bash
python run_server.py
```

또는

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 엔드포인트

- `GET /`: 서버 상태 확인
- `POST /api/dialogue`: 대화 처리
- `WebSocket /ws`: 실시간 통신

## 웹소켓 메시지 형식

### 클라이언트 -> 서버

```json
// 위치 업데이트
{
  "type": "position_update",
  "position": {"x": 0, "y": 0, "z": 0}
}

// 대화 메시지
{
  "type": "dialogue",
  "text": "안녕하세요, 계좌를 개설하고 싶습니다."
}
```

### 서버 -> 클라이언트

```json
{
  "position": {"x": 0, "y": 0, "z": 0},
  "rotation": {"y": 0},
  "animation": "talking",
  "dialogue": "안녕하세요, 계좌 개설을 도와드리겠습니다.",
  "state": "greeting"
}
```

## 확장 방법

더 복잡한 자연어 처리나 강화학습 모델을 적용하려면:

1. `bank_teller_agent.py`의 `classify_intent()` 및 `generate_response()` 메서드를 커스터마이징하세요.
2. 고급 NLP 모델 (예: Transformers, KoGPT)을 통합할 수 있습니다.
3. 강화학습 모델을 사용하여 대화 정책을 최적화할 수 있습니다. 