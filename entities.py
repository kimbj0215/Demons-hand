import random
from typing import List, Optional

# ==========================================
# 1. 상수 및 기본 설정 (Constants)
# ==========================================
# 카드 무늬
SUITS = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
# 카드 숫자 (11=J, 12=Q, 13=K, 14=A) -> A를 14로 하면 크기 비교가 쉬워집니다.
RANKS = list(range(2, 15)) 

# ==========================================
# 2. 카드 및 덱 시스템 (Card & Deck)
# ==========================================
class Card:
    """카드 한 장을 나타내는 클래스"""
    def __init__(self, suit: str, rank: int):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        # 출력했을 때 보여질 모습 (예: 'Hearts 10', 'Spades A')
        rank_str = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(self.rank, str(self.rank))
        return f"[{self.suit} {rank_str}]"

class Deck:
    """52장의 카드를 관리하는 덱 클래스"""
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self):
        """덱을 52장으로 초기화하고 섞습니다."""
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        """덱을 무작위로 섞습니다."""
        random.shuffle(self.cards)

    def draw(self, count: int) -> List[Card]:
        """지정한 장수(count)만큼 카드를 뽑아 리스트로 반환합니다."""
        drawn_cards = []
        for _ in range(count):
            if self.cards:
                drawn_cards.append(self.cards.pop())
        return drawn_cards

# ==========================================
# 3. 인장 (아이템) 시스템 (Insignia)
# ==========================================
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

class Enemy:
    """적(몬스터) 정보를 관리하는 클래스"""
    def __init__(self, name: str, max_hp: int):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp

    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def __repr__(self):
        return f"[{self.name} (HP: {self.current_hp}/{self.max_hp})]"

# ==========================================
# 테스트 코드 (이 파일을 직접 실행했을 때만 동작)
# ==========================================
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