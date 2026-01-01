import os
import random
from dotenv import load_dotenv
from supabase import create_client, Client

# ==========================================
# 1. 환경 변수 로드 및 Supabase 설정
# ==========================================

# .env 파일 내용을 불러옵니다.
load_dotenv()

# os.getenv로 비밀 값을 가져옵니다.
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# 연결 확인 (실수 방지용)
if not url or not key:
    raise ValueError("❌ .env 파일에서 SUPABASE_URL 또는 SUPABASE_KEY를 찾을 수 없습니다.")

supabase: Client = create_client(url, key)

# ==========================================
# 2. 상점 아이템 뽑기 로직
# ==========================================

def fetch_random_items_by_rarity(rarity: str, count: int = 3):
    """
    특정 등급(rarity)의 아이템을 DB에서 가져와서 랜덤하게 count개 반환
    """
    try:
        # 1. DB에서 해당 등급의 모든 아이템 가져오기
        response = supabase.table("items").select("*").eq("rarity", rarity).execute()
        items = response.data

        # 2. 아이템이 없으면 빈 리스트 반환
        if not items:
            print(f"⚠️ '{rarity}' 등급의 아이템이 DB에 없습니다.")
            return []

        # 3. 요청한 개수보다 아이템이 적으면, 있는 거 다 줌
        if len(items) < count:
            print(f"ℹ️ '{rarity}' 아이템이 부족하여 {len(items)}개만 가져옵니다.")
            return items
        
        # 4. 랜덤하게 섞어서 count개 뽑기 (중복 없음)
        return random.sample(items, count)

    except Exception as e:
        print(f"❌ 데이터 가져오기 실패: {e}")
        return []
    
    

# --- 요청하신 3가지 등급별 함수 ---

def get_common_shop_items():
    """상점용: 일반 등급 3개"""
    print("\n[상점] ⬜ 일반 아이템 입고 중...")
    return fetch_random_items_by_rarity("일반", 3)

def get_rare_shop_items():
    """상점용: 희귀 등급 3개"""
    print("\n[상점] 🟦 희귀 아이템 입고 중...")
    return fetch_random_items_by_rarity("희귀", 3)

def get_legendary_shop_items():
    """상점용: 전설 등급 3개"""
    print("\n[상점] 🟨 전설 아이템 입고 중...")
    return fetch_random_items_by_rarity("전설", 3)

def add_to_inventory(user_id: int, item_id: int):
    try:
        data = {
            "user_id_int": user_id,
            "item_id": item_id,
            "is_equipped": False  # 기본값은 장착 해제 상태
        }
        
        # Supabase insert 실행
        supabase.table("inventory").insert(data).execute()
        
        print(f"✅ 유저 {user_id}번의 인벤토리에 아이템 {item_id}번이 추가되었습니다.")
        return True

    except Exception as e:
        print(f"❌ 인벤토리 추가 실패: {e}")
        return False
# ==========================================
# 3. 테스트 실행
# ==========================================
if __name__ == "__main__":
    print("=== 🛒 상점 시스템 테스트 ===")
    add_to_inventory(1, 3)

    # 1. 일반
    common_items = get_common_shop_items()
    for item in common_items:
        print(f" - {item['name']} | {item['rarity']} | {item['price']}G : {item['description']}")

    # 2. 희귀
    rare_items = get_rare_shop_items()
    for item in rare_items:
        print(f" - {item['name']} | {item['rarity']} | {item['price']}G : {item['description']}")

    # 3. 전설
    legend_items = get_legendary_shop_items()
    for item in legend_items:
        print(f" - {item['name']} | {item['rarity']} | {item['price']}G : {item['description']}")