import random
from typing import List, Optional
import pygame
import os

# ==========================================
# 1. 상수 및 기본 설정 (Constants)
# ==========================================
SUIT_SORT_ORDER = {
    "dia": 1,   # 다이아몬드 (♦) 가 가장 먼저!
    "moon": 2,  # 그 다음 달 (🌙)
    "fire": 3,  # 그 다음 불꽃 (🔥)
    "sun": 4    # 마지막 태양 (☀)
}
CARD_SUITS = ["dia", "fire", "moon", "sun"] 

# 숫자(1~13)에 따른 동물/인간 영어 이름 매핑
ZODIAC_MAP = {
    1: "mouse", 2: "cow", 3: "tiger", 4: "rabbit",
    5: "dragon", 6: "snake", 7: "horse", 8: "sheep",
    9: "monkey", 10: "chicken", 11: "dog", 12: "pig",
    13: "kbj"
}
 
class Card:
    """카드 한 장을 나타내는 클래스"""
    def __init__(self, value: int, suit: str):
        self.value = value       # 숫자 (1~13)
        self.suit = suit         # 문양 ("dia", "fire" 등)
        self.animal = ZODIAC_MAP[value]  # "mouse", "cow" 등
        
        # 🌟 핵심: 파일 이름 규칙에 맞게 경로 조립! (폴더 이름이 card 라고 하셨으므로)
        # 예: "card/1_mouse_dia.png"
        self.image_path = f"assets/card/{self.value}_{self.animal}_{self.suit}.png"
        
        # 파이게임용 이미지 로드 (실제 게임 화면에 띄우기 위함)
        self.image = None
        try:
            # 카드를 만들 때 이미지를 미리 불러와서 가지고 있게 합니다.
            # 원본 크기가 크다면 pygame.transform.scale 로 크기를 줄여주세요.
            raw_image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(raw_image, (100, 150)) # 예: 카드 크기 조절
        except:
            print(f"⚠️ 이미지 로드 실패: {self.image_path}")

    def __repr__(self):
        return f"[{self.animal}({self.value}) | {self.suit}]"

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = []
        
        # 1부터 13까지, 4개의 문양을 돌면서 카드를 생성합니다.
        for rank in range(1, 14): # 1 ~ 13
            for suit in CARD_SUITS: # "dia", "fire", "moon", "sun"
                # Card 생성자에 숫자(rank)와 문양(suit)만 넘겨주면 알아서 이미지까지 찾아옵니다!
                self.cards.append(Card(rank, suit))
        
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count: int) -> List[Card]:
        self.shuffle()
        drawn_cards = []
        
        for _ in range(count):
            if len(self.cards) > 0:
                card = self.cards.pop()
                drawn_cards.append(card)
            else:
                print("더 이상 뽑을 카드가 없습니다!") 
                break 
                
        return drawn_cards

class Insignia:
    """게임 내 파워업 아이템(인장) 클래스"""
    def __init__(self, name: str, description: str, effect_type: str, value: float):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # 예: 'damage_multiplier', 'heal'
        self.value = value             # 예: 1.5 (1.5배), 10 (10 회복)

    def __repr__(self):
        return f"<Insignia: {self.name}>"

class Player:
    """플레이어 정보를 관리하는 클래스"""
    def __init__(self, max_hp: int = 100):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hand: List[Card] = [] 
        self.insignia_list: List[Insignia] = [] # 아이템 목록
        self.used_reroll_count = 0     
        self.default_reroll_limit = 3  

    @property
    def max_reroll_count(self):
        bonus = 0
        # 인벤토리에 '인장' 아이템이 있는지 확인
        for item in self.insignia_list:
            # 아이템의 효과 타입이 '리롤 횟수 증가(reroll_plus)'인지 확인
            if item.effect_type == "reroll_plus":
                # 아이템에 설정된 수치(value)만큼 더하기 (1.0 -> 1, 2.0 -> 2)
                bonus += int(item.value)
        
        return self.default_reroll_limit + bonus
    
    def discard_cards(self, indices: list, deck):
        if self.used_reroll_count >= self.max_reroll_count:
            print(f"🚫 리롤 횟수 소진! ({self.used_reroll_count}/{self.max_reroll_count})")
            return
        indices.sort(reverse=True)
        
        for idx in indices:
            if 0 <= idx < len(self.hand):
                self.hand.pop(idx) 

        draw_amount = self.get_draw_count()

        if draw_amount > 0:
            new_cards = deck.draw(draw_amount)
            self.hand.extend(new_cards)
        self.used_reroll_count += 1

    def fill_hand(self, deck):
        """현재 손패 규칙(기본 8장 + 아이템)에 맞춰 부족한 만큼 덱에서 뽑아 채웁니다."""
        draw_amount = self.get_draw_count() # 님이 만든 로직 (8 - 현재장수)
        
        if draw_amount > 0:
            new_cards = deck.draw(draw_amount)
            self.hand.extend(new_cards)
            # print(f"🎴 {draw_amount}장을 드로우하여 손패를 채웠습니다.")
        else:
            print("✋ 손패가 이미 가득 찼습니다.")  

    def sort_hand(self):
        """🌟 유저 요청대로 숫자 우선 정렬 + 같은 숫자면 문양 순서 정렬 🌟"""
        
        # 1. 파이썬 sort()의 key에 tuple을 넘겨줘서 정렬 기준 순서를 정합니다!
        # key=lambda card: (1순위_정렬_기준, 2순위_정렬_기준)
        
        self.hand.sort(key=lambda card: (
            # 기준 1 (최우선): 카드의 숫자(value) - 1부터 13까지 순서대로 모읍니다. (다이아 1, 불꽃 1, 달 1...)
            card.value, 
            
            # 기준 2 (같은 숫자일 때): SUIT_SORT_ORDER에 정의된 문양 순서 (♦ -> 🌙 -> 🔥 -> ☀)
            SUIT_SORT_ORDER.get(card.suit, 5) 
        ))
        
        # 유저님 헷갈리지 않게 메시지 업데이트!
        print("🗂️ 손패가 유저 요청대로 (숫자 -> 문양 순) 완벽하게 정렬되었습니다!")        

    def get_draw_count(self) -> int:
        # 1. 기본 장수 설정 (무조건 8장)
        target_hand_size = 8 
        current_hand_size = len(self.hand)
        draw_amount = target_hand_size - current_hand_size

        if draw_amount < 0:
            draw_amount = 0
        
        # 2. 인장 아이템 효과 확인
        for item in self.insignia_list:
            
            # 아이템 효과가 'draw_plus'(손 크기 증가)인지 확인
            if item.effect_type == "draw_plus":
                # value가 float(1.0)일 수 있으므로 int로 변환해서 더함
                draw_amount += int(item.value)

        return draw_amount

    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def is_alive(self) -> bool:
        return self.current_hp > 0


if __name__ == "__main__":
    print("\n=== 🎮 게임 시작 프로세스 테스트 ===")

    # 1. 덱과 플레이어 생성 (아직 빈 손패)
    my_deck = Deck()
    p1 = Player()

    # ========================================================
    # [핵심] 2. 드로우 전에 아이템(DB 정보)을 먼저 로드합니다!
    # ========================================================
    print(">> 🎒 인벤토리/아이템 정보 로딩 중...")
    
    # 예: DB에서 '수집가(draw_plus)' 아이템을 가져왔다고 가정
    start_item = Insignia(name="수집가", description="시작 손패 +1", effect_type="draw_plus", value=1)
    p1.insignia_list.append(start_item) 
    
    print(f"   ㄴ 아이템 적용됨: {start_item.name} (효과: {start_item.effect_type})")


    # ========================================================
    # 3. 이제 드로우를 합니다. (아이템 효과가 반영됨)
    # ========================================================
    print("\n>> 🎴 게임 시작 드로우 (fill_hand) 실행")
    p1.fill_hand(my_deck)


    # ========================================================
    # 4. 결과 검증 (8장이 아니라 9장이어야 함)
    # ========================================================
    print(f"\n[검증 결과]")
    print(f"현재 손패 갯수: {len(p1.hand)}장")
    print(f"손패 내용: {p1.hand}")

    if len(p1.hand) == 9:
        print("✅ 성공! 시작부터 아이템 효과가 적용되어 9장을 뽑았습니다.")
    else:
        print(f"❌ 실패... 기대값: 9, 실제값: {len(p1.hand)}")