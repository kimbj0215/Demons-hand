import pygame
import sys
from login import supabase 

# ==========================================
# 색상 및 폰트 설정 (전역 변수로 뺌)
# ==========================================
COLOR_BG = (20, 20, 25)
COLOR_BOX = (60, 60, 65)
COLOR_TEXT = (255, 255, 255)
COLOR_BTN = (100, 30, 30)
COLOR_ACTIVE = (180, 180, 200)

def show_login_window(screen):
    """
    로그인 화면을 실행하고, 성공 시 유저 정보를 반환하는 함수
    """
    # 폰트 설정 (함수 안에서 초기화)
    font = pygame.font.SysFont("malgungothic", 30)
    small_font = pygame.font.SysFont("malgungothic", 20)
    
    # 화면 크기 가져오기
    WIDTH, HEIGHT = screen.get_size()

    # 입력창 위치 설정
    id_box = pygame.Rect(WIDTH//2 - 100, 300, 200, 45)
    pw_box = pygame.Rect(WIDTH//2 - 100, 380, 200, 45)
    login_btn = pygame.Rect(WIDTH//2 - 100, 480, 200, 50)

    # 변수 초기화
    user_id = ""
    user_pw = ""
    login_message = ""
    active_field = "id"

    # ==========================================
    # 로그인 루프 시작
    # ==========================================
    running = True
    while running:
        # [A] 이벤트 체크
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if id_box.collidepoint(event.pos):
                    active_field = "id"
                elif pw_box.collidepoint(event.pos):
                    active_field = "pw"
                elif login_btn.collidepoint(event.pos):
                    # --- 로그인 시도 ---
                    login_message = "서버 연결 확인 중..."
                    # 화면을 한번 그려서 메시지를 보여줌 (반응성 향상)
                    draw_login_screen(screen, font, small_font, id_box, pw_box, login_btn, user_id, user_pw, login_message, active_field)
                    pygame.display.flip()

                    try:
                        response = supabase.table("users") \
                            .select("*") \
                            .eq("user_id", user_id) \
                            .eq("password", user_pw) \
                            .execute()
                        
                        if len(response.data) > 0:
                            print(">> 로그인 성공! 메인 게임으로 이동합니다.")
                            # ★ 핵심: 로그인 성공 시 유저 데이터를 가지고 main.py로 돌아갑니다.
                            return response.data[0] 
                        else:
                            login_message = "실패: 아이디/비번을 확인하세요."
                    except Exception as e:
                        login_message = f"에러 발생: {e}"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "id": user_id = user_id[:-1]
                    else: user_pw = user_pw[:-1]
                elif event.key == pygame.K_TAB:
                    active_field = "pw" if active_field == "id" else "id"
                elif event.key == pygame.K_RETURN: # 엔터키 치면 로그인 버튼 클릭과 동일 효과
                     # (여기서 로그인 로직 중복이라 생략, 버튼 클릭 유도)
                     pass
                else:
                    if active_field == "id": user_id += event.unicode
                    else: user_pw += event.unicode

        # [B] 화면 그리기 (별도 함수 혹은 여기서 처리)
        draw_login_screen(screen, font, small_font, id_box, pw_box, login_btn, user_id, user_pw, login_message, active_field)

        # [C] 화면 업데이트
        pygame.display.flip()

def draw_login_screen(screen, font, small_font, id_box, pw_box, login_btn, user_id, user_pw, login_message, active_field):
    """화면 그리는 코드를 깔끔하게 분리"""
    WIDTH = screen.get_width()
    
    screen.fill(COLOR_BG)

    # 제목
    title_surface = font.render("DEMON'S HAND", True, (200, 50, 50))
    screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 150))

    # 상자 테두리
    id_border = 3 if active_field == "id" else 1
    pw_border = 3 if active_field == "pw" else 1
    
    pygame.draw.rect(screen, COLOR_BOX, id_box)
    pygame.draw.rect(screen, COLOR_ACTIVE, id_box, id_border)
    pygame.draw.rect(screen, COLOR_BOX, pw_box)
    pygame.draw.rect(screen, COLOR_ACTIVE, pw_box, pw_border)

    # 버튼
    pygame.draw.rect(screen, COLOR_BTN, login_btn, border_radius=10)
    btn_text = font.render("LOGIN", True, COLOR_TEXT)
    screen.blit(btn_text, (login_btn.centerx - btn_text.get_width()//2, login_btn.centery - btn_text.get_height()//2))

    # 텍스트 내용
    id_surf = font.render(user_id, True, COLOR_TEXT)
    screen.blit(id_surf, (id_box.x + 10, id_box.y + 5))
    
    pw_display = "*" * len(user_pw)
    pw_surf = font.render(pw_display, True, COLOR_TEXT)
    screen.blit(pw_surf, (pw_box.x + 10, pw_box.y + 5))

    # 메시지
    msg_surf = small_font.render(login_message, True, (255, 200, 100))
    screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 550))