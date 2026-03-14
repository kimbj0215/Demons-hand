import pygame
import sys
import bcrypt
from login import supabase 
import ui_createaccount

# ==========================================
# 색상 및 폰트 설정 (전역 변수로 뺌)
# ==========================================
COLOR_BG = (20, 20, 25)
COLOR_BOX = (60, 60, 65)
COLOR_TEXT = (255, 255, 255)
COLOR_BTN = (100, 30, 30)
COLOR_SIGNUP = (40, 60, 100)
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

    try:
        bg_image = pygame.image.load("assets/DH_bg.png")
        # 화면 크기에 딱 맞게 이미지 사이즈 조절
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"배경 로드 실패: {e}")
        bg_image = None

    # 입력창 위치 설정
    id_box = pygame.Rect(WIDTH//2 - 100, 300, 200, 45)
    pw_box = pygame.Rect(WIDTH//2 - 100, 380, 200, 45)
    login_btn = pygame.Rect(WIDTH//2 - 100, 450, 200, 50)
    signup_btn = pygame.Rect(WIDTH//2 - 100, 530, 200, 50)

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
                        response = supabase.table("users").select("*").eq("user_id", input_id).execute()
        
                        if len(response.data) > 0:
                            user_data = response.data[0]
                            stored_hashed_pw = user_data['password'] # DB에 저장된 암호화된 비밀번호
            
            # 🌟 2. bcrypt.checkpw 로 입력한 비번과 DB의 암호화된 비번이 맞는지 확인합니다.
                            if bcrypt.checkpw(input_pw.encode('utf-8'), stored_hashed_pw.encode('utf-8')):
                                print(">> 로그인 성공!")
                                return True, user_data['user_id'], user_data['nickname'] # 등등..
                            else:
                                print(">> 로그인 실패: 비밀번호가 틀렸습니다.")
                                return False, None
                        else:
                            print(">> 로그인 실패: 존재하지 않는 아이디입니다.")
                            return False, None
                    except Exception as e:
                        login_message = f"에러 발생: {e}"

                elif signup_btn.collidepoint(event.pos):
                    print(">> 회원가입 화면으로 이동합니다.")
                    # createaccount.py 안에 있는 회원가입 화면 함수를 실행합니다.
                    try:
                        result =ui_createaccount.show_signup_window(screen)
                        # 회원가입이 끝나고 돌아오면 안내 메시지 출력
                        if result == "success":
                            login_message = "✨ 회원가입 성공! 이제 로그인해 주세요."
                        elif result == "cancel":
                            login_message = "회원가입을 취소했습니다."
                        else:
                            login_message = ""
                    except Exception as e:
                        login_message = "회원가입 화면을 불러올 수 없습니다."
                        print(f"회원가입 에러: {e}")    

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
        draw_login_screen(screen, font, small_font, id_box, pw_box, login_btn, signup_btn, user_id, user_pw, login_message, active_field, bg_image)

        # [C] 화면 업데이트
        pygame.display.flip()

def draw_login_screen(screen, font, small_font, id_box, pw_box, login_btn, signup_btn, user_id, user_pw, login_message, active_field, bg_image):
    """화면 그리는 코드를 깔끔하게 분리"""
    WIDTH = screen.get_width()
    
    if bg_image:
        screen.blit(bg_image, (0, 0)) # (0, 0) 좌표부터 화면 전체에 덮어씌움
    else:
        screen.fill(COLOR_BG)

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

    pygame.draw.rect(screen, COLOR_SIGNUP, signup_btn, border_radius=10)
    signup_text = font.render("SIGN UP", True, COLOR_TEXT)
    screen.blit(signup_text, (signup_btn.centerx - signup_text.get_width()//2, signup_btn.centery - signup_text.get_height()//2))

    # 텍스트 내용
    id_surf = font.render(user_id, True, COLOR_TEXT)
    screen.blit(id_surf, (id_box.x + 10, id_box.y + 5))
    
    pw_display = "*" * len(user_pw)
    pw_surf = font.render(pw_display, True, COLOR_TEXT)
    screen.blit(pw_surf, (pw_box.x + 10, pw_box.y + 5))

    # 메시지
    msg_surf = small_font.render(login_message, True, (255, 200, 100))
    screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 550))