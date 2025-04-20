import numpy as np
import random
import math
from typing import List, Dict, Any, Optional

class BankTellerAgent:
    def __init__(self):
        self.current_state = "idle"
        self.position = {"x": 0, "y": 0, "z": 0}
        self.rotation = {"y": 0}
        self.animation = "idle"
        self.dialogue = ""
        self.conversation_history = []
        
        # 은행 업무 관련 대화 템플릿
        self.dialogue_templates = {
            "greeting": [
                "안녕하세요, 무엇을 도와드릴까요?",
                "안녕하세요, 은행에 오신 것을 환영합니다. 어떤 업무를 도와드릴까요?",
                "안녕하세요, 오늘 어떤 은행 업무를 도와드릴까요?"
            ],
            "account_opening": [
                "계좌 개설을 원하시는군요. 어떤 종류의 계좌를 개설하고 싶으신가요? 입출금 통장, 적금, 청약 등이 있습니다.",
                "계좌 개설을 도와드리겠습니다. 신분증 확인이 필요합니다. 준비되어 있으신가요?",
                "새 계좌 개설이요? 네, 도와드리겠습니다. 어떤 목적으로 계좌를 개설하시나요?"
            ],
            "deposit": [
                "입금 업무를 도와드리겠습니다. 입금하실 금액이 얼마인가요?",
                "입금이요? 네, 계좌번호와 입금하실 금액을 알려주세요.",
                "입금 처리를 도와드리겠습니다. 현금으로 입금하시나요, 아니면 수표로 입금하시나요?"
            ],
            "withdrawal": [
                "출금 업무를 도와드리겠습니다. 출금하실 금액이 얼마인가요?",
                "출금이요? 네, 계좌번호와 출금하실 금액을 알려주세요. 신분증도 필요합니다.",
                "출금 처리를 도와드리겠습니다. 얼마를 출금하시겠어요?"
            ],
            "loan": [
                "대출 상담을 원하시는군요. 어떤 종류의 대출에 관심이 있으신가요?",
                "대출 상담이요? 네, 주택대출, 개인대출, 사업자대출 등 다양한 상품이 있습니다.",
                "대출 상담을 도와드리겠습니다. 대출 용도와 희망 금액은 어떻게 되시나요?"
            ],
            "transfer": [
                "이체 업무를 도와드리겠습니다. 어떤 계좌로 이체하시겠어요?",
                "이체 처리를 도와드리겠습니다. 받으실 분의 계좌번호를 알려주세요.",
                "이체 서비스입니다. 이체하실 금액과 받으실 분의 정보를 알려주세요."
            ],
            "inquiry": [
                "잔액 조회를 도와드리겠습니다. 어떤 계좌의 잔액을 확인하시겠어요?",
                "계좌 조회 서비스입니다. 조회하실 계좌번호를 알려주세요.",
                "잔액 확인이요? 네, 신분증과 계좌번호를 확인하겠습니다."
            ],
            "farewell": [
                "다른 필요하신 업무가 있으신가요?",
                "더 도와드릴 일이 있으신가요?",
                "다른 문의사항이 있으시면 언제든지 말씀해주세요."
            ],
            "thanks": [
                "감사합니다. 좋은 하루 되세요!",
                "이용해 주셔서 감사합니다. 다음에 또 뵙겠습니다.",
                "도움이 필요하시면 언제든지 찾아주세요. 감사합니다!"
            ],
            "unknown": [
                "죄송합니다. 다시 한번 말씀해주시겠어요?",
                "잘 이해하지 못했습니다. 다른 방식으로 설명해주실 수 있을까요?",
                "죄송합니다만, 다시 한번 설명해주시겠어요?"
            ]
        }
        
        # 행동 패턴 정의
        self.behavior_patterns = [
            {"animation": "idle", "duration": 3, "position_change": None},
            {"animation": "typing", "duration": 5, "position_change": None},
            {"animation": "looking", "duration": 2, "position_change": None},
            {"animation": "paperwork", "duration": 4, "position_change": None},
            {"animation": "walk", "duration": 3, "position_change": {"x": 2, "z": 0}},
            {"animation": "walk", "duration": 3, "position_change": {"x": -2, "z": 0}},
            {"animation": "walk", "duration": 3, "position_change": {"x": 0, "z": 2}},
            {"animation": "walk", "duration": 3, "position_change": {"x": 0, "z": -2}}
        ]
        
        self.current_behavior_index = 0
        self.behavior_timer = 0
        
    def update(self, customer_position=None, customer_query=None):
        # 고객 위치에 따른 상태 업데이트
        if customer_position:
            distance = self.calculate_distance(customer_position)
            
            if distance < 3.0:  # 고객이 가까이 있으면
                self.face_customer(customer_position)
                
                if self.current_state != "interacting":
                    self.current_state = "greeting"
                    self.animation = "talking"
                    self.dialogue = random.choice(self.dialogue_templates["greeting"])
            else:
                # 고객이 멀리 있으면 일상 패턴 수행
                self.update_behavior_pattern()
        
        # 고객 질문에 대한 응답 생성
        if customer_query:
            self.current_state = "interacting"
            self.animation = "talking"
            self.dialogue = self.generate_response(customer_query)
            self.conversation_history.append({"user": customer_query, "agent": self.dialogue})
        
        return {
            "position": self.position,
            "rotation": self.rotation,
            "animation": self.animation,
            "dialogue": self.dialogue,
            "state": self.current_state
        }
    
    def update_behavior_pattern(self):
        # 행동 패턴 업데이트 (일상 움직임)
        self.behavior_timer += 1
        
        current_pattern = self.behavior_patterns[self.current_behavior_index]
        
        # 현재 행동의 지속 시간이 지나면 다음 행동으로 전환
        if self.behavior_timer >= current_pattern["duration"]:
            self.behavior_timer = 0
            self.current_behavior_index = (self.current_behavior_index + 1) % len(self.behavior_patterns)
            current_pattern = self.behavior_patterns[self.current_behavior_index]
            self.animation = current_pattern["animation"]
            
            # 위치 변경이 있는 경우 적용
            if current_pattern["position_change"]:
                self.position["x"] += current_pattern["position_change"]["x"]
                self.position["z"] += current_pattern["position_change"]["z"]
                
                # 은행 영역을 벗어나지 않도록 제한
                self.position["x"] = max(-10, min(10, self.position["x"]))
                self.position["z"] = max(-10, min(10, self.position["z"]))
                
                # 이동 방향으로 회전
                if current_pattern["position_change"]["x"] != 0 or current_pattern["position_change"]["z"] != 0:
                    self.rotation["y"] = math.atan2(
                        current_pattern["position_change"]["z"],
                        current_pattern["position_change"]["x"]
                    )
    
    def calculate_distance(self, customer_position):
        dx = self.position["x"] - customer_position["x"]
        dz = self.position["z"] - customer_position["z"]
        return math.sqrt(dx**2 + dz**2)
    
    def face_customer(self, customer_position):
        dx = customer_position["x"] - self.position["x"]
        dz = customer_position["z"] - self.position["z"]
        self.rotation["y"] = math.atan2(dz, dx)
    
    def classify_intent(self, query: str) -> str:
        """고객 의도 분류 (간단한 키워드 기반 분류)"""
        query = query.lower()
        
        # 의도 분류 로직 (키워드 기반)
        if any(keyword in query for keyword in ["계좌", "통장", "개설", "만들"]):
            return "account_opening"
        elif any(keyword in query for keyword in ["입금", "넣", "저금"]):
            return "deposit"
        elif any(keyword in query for keyword in ["출금", "찾", "인출"]):
            return "withdrawal"
        elif any(keyword in query for keyword in ["대출", "융자", "돈 빌리", "이자"]):
            return "loan"
        elif any(keyword in query for keyword in ["이체", "송금", "보내", "계좌 이동"]):
            return "transfer"
        elif any(keyword in query for keyword in ["잔액", "조회", "확인", "얼마"]):
            return "inquiry"
        elif any(keyword in query for keyword in ["감사", "고마", "땡큐"]):
            return "thanks"
        elif any(keyword in query for keyword in ["안녕", "반가", "처음"]):
            return "greeting"
        else:
            return "unknown"
    
    def generate_response(self, query: str) -> str:
        """고객 질문에 대한 응답 생성"""
        # 의도 분류
        intent = self.classify_intent(query)
        
        # 분류된 의도에 따라 응답 생성
        if intent in self.dialogue_templates:
            return random.choice(self.dialogue_templates[intent])
        else:
            return random.choice(self.dialogue_templates["unknown"]) 