import os
import sys
import pygame
from dotenv import load_dotenv
from supabase import create_client, Client

# 아까 완벽하게 만들어둔 카드/플레이어 로직을 가져옵니다!
from entities import Deck, Player 

# 1. Supabase 연결 설정
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def start_game_process(screen, user_id, user_nick, user_stage, user_hp):
    """맵에서 노드를 클릭하면 이 함수가 실행되어 배틀 화면을 띄웁니다."""
    
    # ==========================================
    # 1. 전투 준비 (DB 몬스터 정보 로드 & 카드 덱 세팅)
    # ==========================================
    monster = {"name": "Unknown", "hp": 100, "attack": 10} # 기본값 (DB 실패 대비)
    if supabase:
        try:
            monster_resp = supabase.table("monsters").select("*").eq("stage_code", str(user_stage)).execute()
            if monster_resp.data:
                monster = monster_resp.data[0]
        except Exception as e:
            print(f"DB 오류: {e}")

    # 플레이어와 덱 생성 (방금 만든 entities.py 사용)
    my_deck = Deck()
    p1 = Player(max_hp=user_hp)
    p1.fill_hand(my_deck) # 🌟 시작하자마자 내 손패에 카드 8장을 뽑습니다!
    p1.sort_hand()

    # ==========================================
    # 2. 화면 이미지 로드
    # ==========================================
    font = pygame.font.SysFont("malgungothic", 30)
    
    # 🌟 가지고 계신 배틀맵 이미지 경로를 여기에 적어주세요!
    bg_path = "assets/battlemap_01.png" 
    try:
        bg_image = pygame.image.load(bg_path)
        bg_image = pygame.transform.scale(bg_image, (1280, 720))
    except:
        print("⚠️ 배틀맵 이미지를 찾을 수 없습니다. 임시 배경을 사용합니다.")
        bg_image = None

    # ==========================================
    # 3. 배틀 화면 메인 루프
    # ==========================================
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # 테스트 편의성: ESC 키를 누르면 전투에서 도망쳐서 다시 맵으로 돌아갑니다!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("🏃 전투에서 도망쳤습니다!")
                    running = False 

        # --- 화면 그리기 ---
        
        # 1. 배경 깔기
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((50, 20, 20)) # 어두운 붉은색 (임시 배경)

        # 2. 적 몬스터 정보 표시 (화면 상단)
        enemy_text = font.render(f"적: {monster['name']} (HP: {monster['hp']})", True, (255, 100, 100))
        screen.blit(enemy_text, (50, 50))

        # 3. 내 캐릭터 정보 표시 (화면 중하단)
        player_text = font.render(f"나: {user_nick} (HP: {p1.current_hp})", True, (100, 255, 100))
        screen.blit(player_text, (50, 450))

        mouse_x, mouse_y = pygame.mouse.get_pos() 
        
        card_width = 100
        card_height = 150
        spacing = 20
        total_width = len(p1.hand) * card_width + (len(p1.hand) - 1) * spacing
        start_x = (1280 - total_width) // 2 
        
        # 카드가 놓일 기본 높이 (y좌표)
        base_y = 520 

        for i, card in enumerate(p1.hand):
            card_x = start_x + (i * (card_width + spacing))
            card_y = base_y # 기본 높이로 세팅
            
            # [추가됨] 이 카드가 차지하는 가상의 네모 영역(Rect)을 만듭니다.
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            # [추가됨] 마우스 좌표가 이 카드 영역 안에 들어왔는지 검사합니다!
            if card_rect.collidepoint(mouse_x, mouse_y):
                # 마우스가 닿았다면, y좌표를 30픽셀 빼서 위로 솟구치게 만듭니다!
                card_y -= 30 
                
                # 마우스가 닿은 카드에 예쁜 노란색 테두리 효과를 살짝 줍니다. (선택사항)
                pygame.draw.rect(screen, (255, 255, 0), (card_x-2, card_y-2, card_width+4, card_height+4), 3)

            # 이미지를 그릴 때 base_y가 아니라, 방금 계산한 card_y를 사용합니다!
            if card.image:
                screen.blit(card.image, (card_x, card_y))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (card_x, card_y, card_width, card_height))
                pygame.draw.rect(screen, (0, 0, 0), (card_x, card_y, card_width, card_height), 2) 

        pygame.display.flip()