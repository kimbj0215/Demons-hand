import pygame
import sys
import combat

# 색상 정의
COLOR_TEXT = (255, 255, 255)

def show_map_screen(screen, user_id, user_nick, user_stage, user_hp):
    font = pygame.font.SysFont("malgungothic", 20)
    
    # 🌟 1. 유저의 현재 맵(월드) 번호 파악하기
    # user_stage가 "10", "21" 같은 문자열이라고 가정합니다.
    # 만약 숫자(int)라면 str(user_stage) 로 바꿔서 쓰세요.
    current_world = str(user_stage)[0] # 첫 번째 글자만 떼어냄 ('1', '2' 등)
    
    # 🌟 2. 맵 번호에 따라 배경 이미지 다르게 불러오기
    bg_image = None
    try:
        if current_world == "1": 
            bg_image = pygame.image.load("assets/map_bg01.png")
        elif current_world == "2":
            bg_image = pygame.image.load("assets/map_bg02.png")
        elif current_world == "3":
            bg_image = pygame.image.load("assets/map_bg03.png")
        else :
            print(f"⚠️ 알 수 없는 맵 번호: {current_world}")   
        
        if bg_image:
            bg_image = pygame.transform.scale(bg_image, (1280, 720))
    except Exception as e:
        print(f"배경 로드 실패: {e}")

    # 🌟 3. 맵 번호에 따라 노드(스테이지) 정보 다르게 세팅하기
    if current_world == "1":
        # 1번 맵 (Monster Forest)의 노드들
        nodes = [
            {"code": "10", "name": "Forest Entrance",   "x": 250, "y": 550}, 
            {"code": "11", "name": "Goblin Trail",      "x": 450, "y": 420}, 
            {"code": "12", "name": "Demon's Lair",      "x": 1000, "y": 250}, 
        ]
    elif current_world == "2":
        # 2번 맵 (Demon's Deep Lair)의 노드들 (방금 만든 지도 기준!)
        nodes = [
            {"code": "20", "name": "Lair Entrance",     "x": 200, "y": 600}, 
            {"code": "21", "name": "Demon's Outpost",   "x": 600, "y": 400}, 
            {"code": "22", "name": "The Core of the Lair","x": 1100, "y": 200}, 
        ]
    else:
        nodes = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for node in nodes:
                    dist = ((mouse_pos[0] - node["x"])**2 + (mouse_pos[1] - node["y"])**2)**0.5
                    if dist <= 40:
                        # 🌟 4. 잠금 해제 조건 수정 (문자열 비교)
                        # 예: user_stage가 "11"이면, "10"과 "11"은 갈 수 있지만 "12"는 못 감.
                        if str(user_stage) >= node["code"]:
                            # 게임 진입 시 user_stage는 그대로 유지 (클리어 시 업데이트)
                            combat.start_game_process(screen, user_id, user_nick, node["code"], user_hp)
                        else:
                            print(f"🔒 잠겨있습니다! (필요: {node['code']}, 현재: {user_stage})")

        # --- 화면 그리기 ---
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # 2. 노드 위에 상태 표시
        for node in nodes:
            # 🌟 잠금 해제 조건 수정 (여기도 문자열 비교)
            is_unlocked = (str(user_stage) >= node["code"])
            
            if is_unlocked:
                pygame.draw.circle(screen, (255, 255, 0), (node["x"], node["y"]), 40, 3) 
                name_surf = font.render(node["name"], True, (255, 255, 255), (0, 0, 0))
                screen.blit(name_surf, (node["x"] - name_surf.get_width()//2, node["y"] + 45))
            else:
                s = pygame.Surface((80, 80), pygame.SRCALPHA)   
                pygame.draw.circle(s, (0, 0, 0, 150), (40, 40), 40) 
                screen.blit(s, (node["x"]-40, node["y"]-40))

                # 잠긴 곳도 이름은 흐릿하게 보여주기 (선택사항)
                locked_font = pygame.font.SysFont("malgungothic", 15)
                name_surf = locked_font.render(node["name"] + " (Locked)", True, (150, 150, 150))
                screen.blit(name_surf, (node["x"] - name_surf.get_width()//2, node["y"] + 45))

        pygame.display.flip()