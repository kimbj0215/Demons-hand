import pygame
import sys
import combat

# 색상 정의
COLOR_TEXT = (255, 255, 255)

def show_map_screen(screen, user_id, user_nick, user_stage, user_hp):
    font = pygame.font.SysFont("malgungothic", 20)
    
    # 1. 배경 이미지 로드 (아까 만든 지도)
    # 파일명이 map_bg.png 라고 가정하고 assets 폴더에 넣어주세요
    try:
        bg_image = pygame.image.load("assets/map_bg01.png")
        bg_image = pygame.transform.scale(bg_image, (1280, 720))
    except:
        bg_image = None # 이미지가 없으면 검은색 배경 쓰기 위함

    # 2. 상태 아이콘 로드 (잠김/열림 표시용)
    # 간단하게 동그라미로 그려도 되고, 자물쇠 이미지를 구해도 됩니다.
    # 여기서는 코드로 그리는 걸로 예시를 듭니다.

    # 맵 데이터 (좌표는 배경 그림의 건물 위치에 맞춰서 수정해줘야 함)
    nodes = [
        {"code": "00", "name": "Forest Entrance",   "x": 250, "y": 550}, 
        {"code": "01", "name": "Goblin Trail",      "x": 450, "y": 420}, 
        {"code": "02", "name": "Shadow Cave",       "x": 750, "y": 500}, 
        {"code": "03", "name": "Demon's Lair",      "x": 1000, "y": 250}, 
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for node in nodes:
                    # 클릭 판정 (반지름 40)
                    dist = ((mouse_pos[0] - node["x"])**2 + (mouse_pos[1] - node["y"])**2)**0.5
                    if dist <= 40:
                        if user_stage >= node["code"]:
                            combat.start_game_process(screen, user_id, user_nick, node["code"], user_hp)
                        else:
                            print("🔒 잠겨있습니다!")

        # --- 화면 그리기 ---
        
        # 1. 배경 그리기
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # 2. 노드 위에 상태 표시 (배경 그림 위에 덧칠하기)
        for node in nodes:
            # 갈 수 있는 곳인지 확인
            is_unlocked = (user_stage >= node["code"])
            
            if is_unlocked:
                # 갈 수 있는 곳: 반짝이는 효과 or 화살표 (여기선 노란 테두리)
                # 중심점에 투명한 원을 그리거나, 텍스트를 띄워줌
                pygame.draw.circle(screen, (255, 255, 0), (node["x"], node["y"]), 40, 3) # 노란 테두리
                
                # 이름 표시 (잘 보이게 배경색 추가)
                name_surf = font.render(node["name"], True, (255, 255, 255), (0, 0, 0))
                screen.blit(name_surf, (node["x"] - name_surf.get_width()//2, node["y"] + 45))
                
            else:
                # 못 가는 곳: 자물쇠 아이콘이나 X 표시 (여기선 회색 덮개)
                # 약간 투명한 검은 원을 씌워서 '비활성' 느낌 주기
                s = pygame.Surface((80, 80), pygame.SRCALPHA)   # 투명 판 생성
                pygame.draw.circle(s, (0, 0, 0, 150), (40, 40), 40) # 반투명 검은원
                screen.blit(s, (node["x"]-40, node["y"]-40))

        pygame.display.flip()