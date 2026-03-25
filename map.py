import pygame
import sys
import combat

# 색상 정의
COLOR_TEXT = (255, 255, 255)

def show_map_screen(screen, user_id, user_nick, user_stage, user_hp):
    font = pygame.font.SysFont("malgungothic", 20)
    
    # 🌟 1. 유저의 현재 맵(월드) 번호 파악하기
    # user_stage가 "10", "21" 같은 문자열이라고 가정합니다.
    current_world = str(user_stage)[0] # 첫 번째 글자만 떼어냄 ('1', '2' 등)
    
    # --- [Step 1: 이미지 로드 영역] ---
    
    bg_image = None
    # 🌟 변경점: 변수 여러 개 대신, 이미지를 모아둘 빈 바구니(딕셔너리)를 하나만 만듭니다!
    monster_images = {} 
    
    try:
        if current_world == "1": 
            bg_image = pygame.image.load("assets/map_bg01.png")
            
            # 💡 [핵심] 노드 코드("11", "12")와 그에 맞는 파일 이름을 짝지어 줍니다.
            files_to_load = {
                "11": "assets/monster_icon1-1.png",
                "12": "assets/monster_icon1-2.png"
                # 나중에 1-3 몬스터가 생기면 여기에 "13": "assets/..." 한 줄만 추가하면 끝납니다!
            }
            
            # for문을 돌면서 이미지를 한 번에 싹 불러와서 바구니에 담습니다.
            for code, file_path in files_to_load.items():
                try:
                    raw_img = pygame.image.load(file_path)
                    # 크기를 60x60으로 줄여서 노드 코드("11", "12")를 열쇠로 바구니에 저장!
                    monster_images[code] = pygame.transform.scale(raw_img, (60, 60))
                except Exception as e:
                    print(f"⚠️ 몬스터 이미지 로드 실패 ({file_path}): {e}")
                    
        elif current_world == "2":
            bg_image = pygame.image.load("assets/map_bg02.png")
            # 2번 맵에 해당하는 몬스터 이미지가 있다면 여기에 추가 로드 로직 작성
            
        # ... (이하 맵 이미지 로드 로직 동일) ...
        
        if bg_image:
            bg_image = pygame.transform.scale(bg_image, (1280, 720))
    except Exception as e:
        print(f"배경 로드 실패: {e}")

    # 🌟 3. 맵 번호에 따라 노드(스테이지) 정보 다르게 세팅하기
    if current_world == "1":
        # 1번 맵 (Monster Forest)의 노드들
        nodes = [
            {"code": "11", "name": "",   "x": 250, "y": 550}, 
            {"code": "12", "name": "",      "x": 550, "y": 550}, # 👈 여기에 몬스터를 띄울 겁니다.
            {"code": "13", "name": "",      "x": 1000, "y": 250}, 
        ]
    # ... (이하 노드 세팅 로직 동일) ...
    elif current_world == "2":
        # 2번 맵 (Demon's Deep Lair)의 노드들 (방금 만든 지도 기준!)
        nodes = [
            {"code": "21", "name": "",     "x": 200, "y": 600}, 
            {"code": "22", "name": "",   "x": 600, "y": 400}, 
            {"code": "23", "name": "","x": 1100, "y": 200}, 
        ]
    else:
        nodes = []

    running = True
    while running:
        # ... (이하 이벤트 처리 로직 동일) ...
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
                        if str(user_stage) >= node["code"]:
                            combat.start_game_process(screen, user_id, user_nick, node["code"], user_hp)
                        else:
                            print(f"🔒 잠겨있습니다! (필요: {node['code']}, 현재: {user_stage})")

        # --- [Step 2: 화면 그리기 영역] ---
        
        # 1. 배경 그리기
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # 2. 노드 위에 상태 및 몬스터 표시
        for node in nodes:
            # 잠금 해제 조건 확인
            is_unlocked = (str(user_stage) >= node["code"])
            
            if is_unlocked:
                # [A] 열린 노드: 기본 노란 테두리 원 그리기
                pygame.draw.circle(screen, (255, 255, 0), (node["x"], node["y"]), 40, 3) 
                
                # 💡 [핵심] 만약 이 노드가 "11"번(Goblin Trail)이고, 몬스터 이미지가 잘 로드되었다면 그립니다.
                if node["code"] in monster_images:
                    img_to_draw = monster_images[node["code"]]
                    screen.blit(img_to_draw, (node["x"] - 30, node["y"] - 30))
                
                # 이름 표시
                name_surf = font.render(node["name"], True, (255, 255, 255), (0, 0, 0))
                screen.blit(name_surf, (node["x"] - name_surf.get_width()//2, node["y"] + 45))
                
            else:
                # [B] 잠긴 노드 처리 (회색 덮개)
                s = pygame.Surface((80, 80), pygame.SRCALPHA)   
                pygame.draw.circle(s, (0, 0, 0, 150), (40, 40), 40) 
                screen.blit(s, (node["x"]-40, node["y"]-40))

                # 잠긴 곳 이름 (선택사항)
                locked_font = pygame.font.SysFont("malgungothic", 15)
                name_surf = locked_font.render(node["name"] + " (Locked)", True, (150, 150, 150))
                screen.blit(name_surf, (node["x"] - name_surf.get_width()//2, node["y"] + 45))

        pygame.display.flip()