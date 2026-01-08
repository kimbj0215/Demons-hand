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
        return f"[{self.name} | {self.value} | {self.card_type}]"

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

    def fill_hand(self, deck):
        """현재 손패 규칙(기본 8장 + 아이템)에 맞춰 부족한 만큼 덱에서 뽑아 채웁니다."""
        draw_amount = self.get_draw_count() # 님이 만든 로직 (8 - 현재장수)
        
        if draw_amount > 0:
            new_cards = deck.draw(draw_amount)
            self.hand.extend(new_cards)
            # print(f"🎴 {draw_amount}장을 드로우하여 손패를 채웠습니다.")
        else:
            print("✋ 손패가 이미 가득 찼습니다.")    

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