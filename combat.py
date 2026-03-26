import os
import sys
import pygame
from dotenv import load_dotenv
from supabase import create_client, Client

from entities import Deck, Player 

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def start_game_process(screen, user_id, user_nick, user_stage, user_hp):
    """맵에서 노드를 클릭하면 이 함수가 실행되어 배틀 화면을 띄웁니다."""
    
    # ==========================================
    # 1. 전투 준비 (DB 몬스터 정보 로드 & 카드 덱 세팅)
    # ==========================================
    monster = {"name": "Unknown", "hp": 100, "attack": 10} 
    if supabase:
        try:
            monster_resp = supabase.table("monsters").select("*").eq("stage_code", str(user_stage)).execute()
            if monster_resp.data:
                monster = monster_resp.data[0]
        except Exception as e:
            print(f"DB 오류: {e}")

    my_deck = Deck()
    p1 = Player(max_hp=user_hp)
    p1.fill_hand(my_deck) 
    p1.sort_hand()

    # ==========================================
    # 2. 화면 이미지 로드 (배경 & 🌟몬스터🌟)
    # ==========================================
    font = pygame.font.SysFont("malgungothic", 30)
    
    # [배경 로드]
    bg_path = "assets/battlemap_01.png" 
    try:
        bg_image = pygame.image.load(bg_path)
        bg_image = pygame.transform.scale(bg_image, (1280, 720))
    except:
        bg_image = None

    # 🌟 [몬스터 이미지 로드] 🌟
    # user_stage(예: "11")를 이용해서 파일 이름("assets/monster1-1.png")을 만듭니다.
    # 맵에서는 monster_icon 이었는데 배틀에서는 monster 라고 하셨으니 그에 맞춥니다!
    world_num = str(user_stage)[0]
    stage_num = str(user_stage)[1]
    monster_img_path = f"assets/monster{world_num}-{stage_num}.png"
    
    monster_image = None
    try:
        raw_monster = pygame.image.load(monster_img_path)
        # 배틀 화면이니 몬스터를 300x300 크기로 큼직하게 키웁니다!
        monster_image = pygame.transform.scale(raw_monster, (300, 300))
    except Exception as e:
        print(f"⚠️ 몬스터 이미지({monster_img_path}) 로드 실패: {e}")

    # ==========================================
    # 3. 배틀 화면 메인 루프
    # ==========================================
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("🏃 전투에서 도망쳤습니다!")
                    running = False 

        # --- 화면 그리기 ---
        
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 20, 20)) 

        # ==========================================
        # 🌟 2. 몬스터 이미지 & 스탯(공격력, 체력) 띄우기 🌟
        # ==========================================
        if monster_image:
            # 💡 몬스터의 기준 좌표를 변수로 만듭니다. (유저님이 원하시는 중앙 위치로 숫자 조절 가능!)
            monster_x = 490  # 가로 중앙쯤 (1280 - 300) / 2
            monster_y = 120  # 위에서 살짝 떨어진 위치
            
            # 1) 몬스터 이미지 그리기
            screen.blit(monster_image, (monster_x, monster_y)) 

            # 2) 스탯 글씨용 폰트 (좀 더 두껍고 눈에 띄게)
            stat_font = pygame.font.SysFont("malgungothic", 35, bold=True)
            
            atk_text = stat_font.render(f" {monster['attack']}", True, (255, 80, 80))
            atk_x = monster_x
            atk_y = monster_y + 250  # 몬스터 이미지 높이(300)보다 살짝 위쪽
            screen.blit(atk_text, (atk_x, atk_y))

            hp_text = stat_font.render(f"{monster['hp']}", True, (80, 255, 80))
            hp_x = monster_x + 300 - hp_text.get_width() # 오른쪽 끝에 딱 맞추기 위해 글씨 폭만큼 빼줍니다.
            hp_y = monster_y + 250
            screen.blit(hp_text, (hp_x, hp_y))

        # 🚨 (기존에 있던 enemy_text, player_text 등 글씨 띄우던 4줄은 싹 다 지워주세요!) 🚨
        
        # 3. 내 손패(카드) 그리기 & 호버 효과 (기존 코드 그대로 둠)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        card_width = 100
        card_height = 150
        spacing = 20
        total_width = len(p1.hand) * card_width + (len(p1.hand) - 1) * spacing
        start_x = (1280 - total_width) // 2 
        
        base_y = 520 

        for i, card in enumerate(p1.hand):
            card_x = start_x + (i * (card_width + spacing))
            card_y = base_y 
            
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            if card_rect.collidepoint(mouse_x, mouse_y):
                card_y -= 30 
                pygame.draw.rect(screen, (255, 255, 0), (card_x-2, card_y-2, card_width+4, card_height+4), 3)

            if card.image:
                screen.blit(card.image, (card_x, card_y))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (card_x, card_y, card_width, card_height))
                pygame.draw.rect(screen, (0, 0, 0), (card_x, card_y, card_width, card_height), 2) 

        pygame.display.flip()