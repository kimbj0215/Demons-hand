import random
from typing import List, Optional

# ==========================================
# 1. 상수 및 기본 설정 (Constants)
# ==========================================
# 카드 무늬
CARD_TYPES = {
    "DIAMOND": "♦",  # 다이아몬드 모양
    "FIRE": "🔥",    # 불꽃 모양
    "MOON": "🌙",     # 달 모양
    "SUN": "☀"     # 해/폭발 모양
}
 
# ==========================================
# 2. 카드 및 덱 시스템 (Card & Deck)
# ==========================================
class Card:
    """카드 한 장을 나타내는 클래스"""
    def __init__(self, name: str, value: int, card_type: str):
        self.name = name        # 카드 이름
        self.value = value      # 좌측 하단 숫자 (위력)
        self.card_type = card_type # 우측 하단 아이콘 (속성)

    def __repr__(self):
        # 출력 예: [부족민 | 2 | 자원(♦)]
        return f"[{self.name} | ⚔️{self.value} | {self.card_type}]"

class Deck:
    """52장의 카드를 관리하는 덱 클래스"""
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        """사진에 있는 느낌대로 카드 목록을 생성합니다."""
        self.cards = []
        
        card_data = [
            ("", 2, CARD_TYPES["RESOURCE"]),
            ("", 3, CARD_TYPES["RESOURCE"]),
            ("", 6, CARD_TYPES["ATTACK"]),
            ("", 7, CARD_TYPES["SPECIAL"]),
            ("", 9, CARD_TYPES["MAGIC"]),
            ("", 4, CARD_TYPES["ATTACK"]),
            ("", 5, CARD_TYPES["MAGIC"]),
            ("", 1, CARD_TYPES["RESOURCE"]),
        ]

        # 덱에 카드를 채워넣음 (테스트를 위해 각 카드를 3장씩 넣음)
        for name, val, c_type in card_data:
            for _ in range(3): 
                self.cards.append(Card(name, val, c_type))
        
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count: int) -> List[Card]:
        drawn_cards = []
        for _ in range(count):
            if self.cards:
                drawn_cards.append(self.cards.pop())
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

# ==========================================
# 4. 캐릭터 (Player & Enemy)
# ==========================================
class Player:
    """플레이어 정보를 관리하는 클래스"""
    def __init__(self, max_hp: int = 100):
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hand: List[Card] = []          # 현재 손에 쥐고 있는 카드들
        self.insignia_list: List[Insignia] = [] # 보유한 인장 목록

    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def heal(self, amount: int):
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def is_alive(self) -> bool:
        return self.current_hp > 0


if __name__ == "__main__":
    # 1. 덱 테스트
    print("--- 덱 생성 및 드로우 테스트 ---")
    my_deck = Deck()
    print(f"전체 카드 수: {len(my_deck.cards)}")
    
    my_hand = my_deck.draw(5)
    print(f"뽑은 카드 5장: {my_hand}")
    print(f"남은 카드 수: {len(my_deck.cards)}")

    # 2. 플레이어 및 적 테스트
    print("\n--- 플레이어 vs 적 테스트 ---")
    hero = Player(max_hp=100)
    monster = Enemy(name="사악한 미니언", max_hp=50)

    print(f"플레이어 HP: {hero.current_hp}")
    print(f"적 정보: {monster}")

    print("...적이 공격받음 (20 데미지)...")
    monster.take_damage(20)
    print(f"적 정보: {monster}")