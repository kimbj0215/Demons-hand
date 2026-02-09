import os
import time
import random
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Supabase 연결 설정
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def get_next_stage(current_code):
    map_num = int(current_code[0]) 
    stage_num = int(current_code[1])
    stage_num += 1
    
    if stage_num > 9:
        map_num += 1
        stage_num = 0
    return f"{map_num}{stage_num}"


def battle_logic(player, monster):
    """ 실제 치고받고 싸우는 전투 로직 (크리티컬 없음) """
    
    print(f"\n{'='*40}")
    print(f"🔥 전투 시작! [{player['nickname']}] VS [{monster['name']}]")
    print(f"{'='*40}")
    print(f"내 정보: HP {player['hp']} / ATK {player['attack']}")
    print(f"적 정보: HP {monster['hp']} / ATK {monster['attack']}")
    
    if monster.get('special_ability'):
        print(f"⚠️ 특수 능력: {monster['special_ability']}")
    print(f"{'-'*40}\n")
    time.sleep(1)

    while player['hp'] > 0 and monster['hp'] > 0:
        # --- 플레이어 턴 ---
        damage = player['attack'] + random.randint(-2, 2)
        if damage < 0: damage = 0
        monster['hp'] -= damage
        print(f"🗡️ {player['nickname']} 공격! 💥 {damage} 피해 (적 HP: {max(0, monster['hp'])})")

        if monster['hp'] <= 0:
            return "VICTORY"
        
        time.sleep(0.5)

        # --- 몬스터 턴 ---
        monster_damage = monster['attack']
        player['hp'] -= monster_damage
        print(f"   (내 남은 HP: {max(0, player['hp'])})")

        if player['hp'] <= 0:
            return "DEFEAT"
            
        time.sleep(0.5)
        print("")

    return "ERROR"


def start_game_process(screen, user_id, user_nick, user_stage, user_hp):
    if not supabase:
        return
    try:
    
        # 2. 몬스터 정보 가져오기 (monsters 테이블)
        monster_resp = supabase.table("monsters").select("*").eq("stage_code", user_stage).execute()
        
        if not monster_resp.data:
            print("🎉 축하합니다! 준비된 모든 몬스터를 처치했습니다!")
            return

        monster = monster_resp.data[0] # 몬스터 정보 확정

        # 3. 내 캐릭터 생성 (임시 스탯)
        my_player = {"nickname": user_nick, "hp": user_hp}

        # 4. 전투 시작 (위의 battle_logic 함수 호출)
        result = battle_logic(my_player, monster)

        # 5. 결과 처리 및 저장
        if result == "VICTORY":
            print(f"\n🎊 승리했습니다! {monster['name']} 처치 완료!")
            
            # 다음 스테이지 계산
            next_stage = get_next_stage(user_stage)
            
            # DB 업데이트
            supabase.table("users").update({"current_stage": next_stage}).eq("user_id", user_id).execute()
             
        elif result == "DEFEAT":
            print("\n💀 패배했습니다...")

    except Exception as e:
        print(f"❌ 게임 진행 중 오류 발생: {e}")