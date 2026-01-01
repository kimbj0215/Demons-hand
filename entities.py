import random
from typing import List, Optional

# ==========================================
# 1. 상수 및 기본 설정 (Constants)
# ==========================================

CARD_TYPES = {
    "DIAMOND": "♦",  # 다이아몬드 모양
    "FIRE": "🔥",    # 불꽃 모양
    "MOON": "🌙",     # 달 모양
    "SUN": "☀"     # 해/폭발 모양
}
 
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
        self.cards = []
        types = list(CARD_TYPES.values())
        
        # 숫자별 이름 (없으면 그냥 '병사'로 통일)
        name_map = {
            1: "test1",
            2: "test2",
            3: "test3",
            4: "test4",
            5: "test5",
            6: "test6",
            7: "test7",
            8: "test8",
            9: "test9",
            10: "test10",
            11: "test11",
            12: "test12",
            0: "test0"
        }

        for rank in range(0,13): # 1~13
            for c_type in types:

                # 2. 카드 추가
                self.cards.append(Card(name_map[rank], rank, c_type))
        
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, count: int) -> List[Card]:
        self.shuffle
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