from collections import Counter
from typing import List, Tuple
from entities import Card

# ==========================================
# 1. 족보 별 점수표 (상수)
# ==========================================
# 게임 밸런스에 맞춰 점수를 수정할 수 있습니다.
HAND_SCORES = {
    "Royal Flush": 2000,
    "Straight Flush": 600,
    "Four of a Kind": 300, # 포커 용어: 포카드
    "Full House": 150,
    "Flush": 120,
    "Straight": 100,
    "Three of a Kind": 60, # 포커 용어: 트리플
    "Two Pair": 30,
    "One Pair": 10,
    "High Card": 5
}

# ==========================================
# 2. 보조 함수들 (판별 로직)
# ==========================================
def is_flush(cards: List[Card]) -> bool:
    """5장의 무늬가 모두 같은지 확인"""
    first_suit = cards[0].suit
    for card in cards[1:]:
        if card.suit != first_suit:
            return False
    return True

def is_straight(ranks: List[int]) -> bool:
    """숫자가 연속적인지 확인"""
    # 숫자 오름차순 정렬
    sorted_ranks = sorted(ranks)
    
    # 1. 일반적인 스트레이트 (예: 2,3,4,5,6)
    # 가장 큰 숫자와 작은 숫자의 차이가 4이고, 중복이 없으면 스트레이트
    if len(set(sorted_ranks)) == 5 and (sorted_ranks[-1] - sorted_ranks[0] == 4):
        return True
        
    # 2. 백스트레이트 (A, 2, 3, 4, 5) -> 시스템상 A는 14
    # 정렬하면 [2, 3, 4, 5, 14]가 됨
    if sorted_ranks == [2, 3, 4, 5, 14]:
        return True
        
    return False

# ==========================================
# 3. 핵심 판별 함수
# ==========================================
def evaluate_hand(hand: List[Card]) -> Tuple[str, int]:
    """
    5장의 카드를 받아 (족보이름, 점수)를 반환합니다.
    높은 족보부터 순서대로 검사합니다.
    """
    if len(hand) != 5:
        raise ValueError("카드는 반드시 5장이어야 합니다.")

    # 계산을 편하게 하기 위해 숫자(rank)만 따로 리스트로 만듭니다.
    ranks = [card.rank for card in hand]
    
    # 숫자별 개수를 셉니다. (예: [10, 10, 5, 2, 2] -> {10:2, 2:2, 5:1})
    rank_counts = Counter(ranks)
    # 개수를 기준으로 내림차순 정렬 (예: 풀하우스면 (3, 2) 형태가 됨)
    # values()는 개수만 가져옵니다. sorted(..., reverse=True)로 큰 개수부터 정렬
    counts = sorted(rank_counts.values(), reverse=True)

    # 상태 확인
    flush_check = is_flush(hand)
    straight_check = is_straight(ranks)

    # --- 판별 시작 (높은 순서대로) ---

    # 1. 로열 플러시 & 스트레이트 플러시
    if flush_check and straight_check:
        # 14(Ace)가 포함된 스트레이트 플러시라면 로열 플러시
        if 14 in ranks and 13 in ranks: # A와 K가 포함됨
            hand_name = "Royal Flush"
        else:
            hand_name = "Straight Flush"
    
    # 2. 포카드 (같은 숫자 4장) -> counts가 [4, 1]
    elif counts == [4, 1]:
        hand_name = "Four of a Kind"
        
    # 3. 풀하우스 (같은 숫자 3장 + 2장) -> counts가 [3, 2]
    elif counts == [3, 2]:
        hand_name = "Full House"
        
    # 4. 플러시
    elif flush_check:
        hand_name = "Flush"
        
    # 5. 스트레이트
    elif straight_check:
        hand_name = "Straight"
        
    # 6. 트리플 (같은 숫자 3장) -> counts가 [3, 1, 1]
    elif counts == [3, 1, 1]:
        hand_name = "Three of a Kind"
        
    # 7. 투페어 (같은 숫자 2장, 2장) -> counts가 [2, 2, 1]
    elif counts == [2, 2, 1]:
        hand_name = "Two Pair"
        
    # 8. 원페어 (같은 숫자 2장) -> counts가 [2, 1, 1, 1]
    elif counts == [2, 1, 1, 1]:
        hand_name = "One Pair"
        
    # 9. 하이카드 (꽝)
    else:
        hand_name = "High Card"

    return hand_name, HAND_SCORES[hand_name]

# ==========================================
# 테스트 코드 (이 파일을 실행해서 로직 검증)
# ==========================================
if __name__ == "__main__":
    # 테스트용 카드 덱 생성은 필요 없지만 Card 객체는 필요함
    print("--- 족보 판별기 테스트 ---")

    # 케이스 1: 풀하우스 (10 세 장, 5 두 장)
    test_hand_1 = [
        Card("Spades", 10), Card("Hearts", 10), Card("Diamonds", 10),
        Card("Clubs", 5), Card("Spades", 5)
    ]
    name, score = evaluate_hand(test_hand_1)
    print(f"결과 1: {name} (점수: {score}) -> 예상: Full House")

    # 케이스 2: 스트레이트 (A, 2, 3, 4, 5) - 백스트레이트
    test_hand_2 = [
        Card("Spades", 14), Card("Hearts", 2), Card("Diamonds", 3),
        Card("Clubs", 4), Card("Spades", 5)
    ]
    name, score = evaluate_hand(test_hand_2)
    print(f"결과 2: {name} (점수: {score}) -> 예상: Straight")

    # 케이스 3: 꽝 (하이카드)
    test_hand_3 = [
        Card("Spades", 14), Card("Hearts", 2), Card("Diamonds", 9),
        Card("Clubs", 4), Card("Spades", 7)
    ]
    name, score = evaluate_hand(test_hand_3)
    print(f"결과 3: {name} (점수: {score}) -> 예상: High Card")