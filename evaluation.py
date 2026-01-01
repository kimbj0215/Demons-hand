from typing import List, Tuple
from collections import Counter
from entities import Card  # entities.py에서 Card 클래스 가져오기

# ==========================================
# 1. 족보 점수 및 설정
# ==========================================
HAND_SCORES = {
    "Serious Punch": 2000,    # 로열 스티플 (0 포함)
    "TSET3": 600,             # 스티플
    "Triple and Couple": 300, # 풀하우스
    "Type Set": 150,             # 플러시
    "TEST2": 120,             # 스트레이트
    "Family": 100,            # 포카드
    "Triple": 60,             # 트리플
    "Couple Set": 40,         # 투페어
    "Couple": 20,             # 원페어
    "Solo": 10,               # 하이카드
}

# ==========================================
# 2. 판별 핵심 로직 (변수명 수정됨)
# ==========================================
def get_power(value: int) -> int:
    """0을 가장 높은 숫자(13)로 변환"""
    return 13 if value == 0 else value

def is_Type_Set(cards: List[Card]) -> bool:
    """[Type Set] 무늬(card_type)가 모두 같은지 확인"""
    if not cards: return False
    
    # [수정] card.suit -> card.card_type
    first_type = cards[0].card_type
    for card in cards[1:]:
        if card.card_type != first_type:
            return False
    return True

def is_TEST2(values: List[int]) -> bool:
    """[TEST2] 숫자가 연속적인지 확인 (Straight)"""
    powers = [get_power(v) for v in values]
    sorted_powers = sorted(powers)
    
    # 중복이 없고, (최대값 - 최소값)이 4이면 연속된 숫자임
    if len(set(sorted_powers)) == 5 and (sorted_powers[-1] - sorted_powers[0] == 4):
        return True
    return False

def evaluate_hand(hand: List[Card]) -> Tuple[str, int]:
    """카드 5장을 받아 족보 이름과 점수를 반환"""
    
    if len(hand) != 5:
        return "Solo", 10

    # 1. 숫자(Value)만 추출 및 파워 변환
    # [수정] card.rank -> card.value 사용
    raw_values = [card.value for card in hand]
    powers = [get_power(v) for v in raw_values]
    
    # 2. 같은 숫자 개수 세기
    counts = sorted(Counter(powers).values(), reverse=True)

    # 3. 플러시(Type Set), 스트레이트(TEST2) 여부 미리 계산
    check_type_set = is_Type_Set(hand)
    check_test2 = is_TEST2(raw_values)

    # 4. 족보 판별 (점수가 높은 순서대로)
    hand_name = "Solo"

    # [2000] Serious Punch (0 포함 + 무늬같음 + 연속)
    if check_type_set and check_test2 and (13 in powers):
        hand_name = "Serious Punch"
    elif check_type_set and check_test2:
        hand_name = "TSET3"
    elif counts == [3, 2]:
        hand_name = "Triple and Couple"
    elif check_type_set:
        hand_name = "Type Set"
    elif check_test2:
        hand_name = "TEST2"
    elif counts == [4, 1]:
        hand_name = "Family"
    elif counts == [3, 1, 1]:
        hand_name = "Triple"
    elif counts == [2, 2, 1]:
        hand_name = "Couple Set"
    elif counts == [2, 1, 1, 1]:
        hand_name = "Couple"
    else:
        hand_name = "Solo"

    return hand_name, HAND_SCORES[hand_name]

# ==========================================
# 3. 실행 테스트 코드
# ==========================================
if __name__ == "__main__":
    print("=== 🃏 entities.Card 연동 족보 테스트 시작 ===")

    # [중요] Card 생성 시 (name, value, card_type) 순서를 지켜야 함
    test_cases = [
        ("Serious Punch", [
            Card("T", 0, "♦"), Card("T", 12, "♦"), Card("T", 11, "♦"), Card("T", 10, "♦"), Card("T", 9, "♦")
        ]),
        ("TSET3", [
            Card("T", 1, "🔥"), Card("T", 2, "🔥"), Card("T", 3, "🔥"), Card("T", 4, "🔥"), Card("T", 5, "🔥")
        ]),
        ("Triple and Couple", [
            Card("T", 7, "🌙"), Card("T", 7, "☀"), Card("T", 7, "♦"), Card("T", 2, "🌙"), Card("T", 2, "🔥")
        ]),
        ("Type Set", [
            Card("T", 1, "☀"), Card("T", 5, "☀"), Card("T", 8, "☀"), Card("T", 10, "☀"), Card("T", 12, "☀")
        ]),
        ("TEST2", [
            Card("T", 0, "♦"), Card("T", 12, "🔥"), Card("T", 11, "🌙"), Card("T", 10, "☀"), Card("T", 9, "♦")
        ]),
        ("Family", [
            Card("T", 5, "♦"), Card("T", 5, "🔥"), Card("T", 5, "🌙"), Card("T", 5, "☀"), Card("T", 9, "♦")
        ]),
        ("Triple", [
            Card("T", 3, "♦"), Card("T", 3, "🔥"), Card("T", 3, "🌙"), Card("T", 8, "☀"), Card("T", 1, "♦")
        ]),
        ("Couple Set", [
            Card("T", 8, "♦"), Card("T", 8, "🔥"), Card("T", 4, "🌙"), Card("T", 4, "☀"), Card("T", 1, "♦")
        ]),
        ("Couple", [
            Card("T", 11, "♦"), Card("T", 11, "🔥"), Card("T", 1, "🌙"), Card("T", 1, "☀"), Card("T", 9, "♦")
        ]),
        ("Solo", [
            Card("T", 1, "♦"), Card("T", 3, "🔥"), Card("T", 5, "🌙"), Card("T", 8, "☀"), Card("T", 11, "♦")
        ]),
    ]

    success_cnt = 0
    for expected, hand in test_cases:
        result_name, score = evaluate_hand(hand)
        
        if result_name == expected:
            print(f"✅ [성공] {expected:<17} | 점수: {score}")
            success_cnt += 1
        else:
            print(f"❌ [실패] 기대값: {expected} != 결과: {result_name}")
            print(f"   패: {hand}")

    print("-" * 40)
    print(f"총 {len(test_cases)}개 케이스 중 {success_cnt}개 통과")