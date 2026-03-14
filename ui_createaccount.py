import pygame
import sys
# 방금 만든 DB 기능 전용 파일을 불러옵니다.
import createaccount 

# ==========================================
# 색상 및 폰트 설정
# ==========================================
COLOR_BG = (20, 20, 25)
COLOR_BOX = (60, 60, 65)
COLOR_TEXT = (255, 255, 255)
COLOR_SIGNUP_BTN = (40, 60, 100)  # 가입 버튼 (파란색 계열)
COLOR_CANCEL_BTN = (100, 30, 30)  # 취소 버튼 (빨간색 계열)
COLOR_ACTIVE = (180, 180, 200)

def show_signup_window(screen):
    """
    회원가입 UI 화면을 띄우고 입력을 받습니다.
    """
    font = pygame.font.SysFont("malgungothic", 30)
    small_font = pygame.font.SysFont("malgungothic", 20)
    
    WIDTH, HEIGHT = screen.get_size()

    # 1. 배경 이미지 불러오기 (루프 바깥에서 한 번만 로드)
    try:
        bg_image = pygame.image.load("assets/DH_bg.png")
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    except:
        bg_image = None

    # 2. UI 요소 위치 설정 (입력창 3개, 버튼 2개)
    id_box = pygame.Rect(WIDTH//2 - 100, 230, 200, 45)
    pw_box = pygame.Rect(WIDTH//2 - 100, 300, 200, 45)
    nick_box = pygame.Rect(WIDTH//2 - 100, 370, 200, 45)
    
    signup_btn = pygame.Rect(WIDTH//2 - 100, 450, 200, 45)
    cancel_btn = pygame.Rect(WIDTH//2 - 100, 510, 200, 45)

    # 3. 변수 초기화
    user_id = ""
    user_pw = ""
    nickname = ""
    msg = "아이디, 비밀번호, 닉네임을 입력하세요."
    active_field = "id"

    # ==========================================
    # 화면 루프 시작
    # ==========================================
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if id_box.collidepoint(event.pos): active_field = "id"
                elif pw_box.collidepoint(event.pos): active_field = "pw"
                elif nick_box.collidepoint(event.pos): active_field = "nick"
                
                # [취소 버튼] 클릭 시 로그인 화면으로 돌아감
                elif cancel_btn.collidepoint(event.pos):
                    return 

                # [가입 버튼] 클릭 시
                elif signup_btn.collidepoint(event.pos):
                    if not user_id or not user_pw or not nickname:
                        msg = "모든 칸을 채워주세요!"
                    else:
                        msg = "가입 처리 중..."
                        # 처리 중 메시지를 보여주기 위해 화면 한 번 업데이트
                        draw_signup_screen(screen, font, small_font, id_box, pw_box, nick_box, signup_btn, cancel_btn, 
                                           user_id, user_pw, nickname, msg, active_field, bg_image)
                        pygame.display.flip()

                        # ==========================================
                        # ★ 여기서 DB 기능 호출! (createaccount.py 사용)
                        # ==========================================
                        success, result_msg = createaccount.register_user(user_id, user_pw, nickname)
                        msg = result_msg # 성공/실패 메시지 업데이트
                        
                        if success:
                            # 성공 시 화면에 성공 메시지를 1초간 보여주고 메인 화면으로 돌아감
                            draw_signup_screen(screen, font, small_font, id_box, pw_box, nick_box, signup_btn, cancel_btn, 
                                               user_id, user_pw, nickname, msg, active_field, bg_image)
                            pygame.display.flip()
                            pygame.time.delay(1000) 
                            return "success"

            # 키보드 입력 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if active_field == "id": user_id = user_id[:-1]
                    elif active_field == "pw": user_pw = user_pw[:-1]
                    elif active_field == "nick": nickname = nickname[:-1]
                elif event.key == pygame.K_TAB:
                    if active_field == "id": active_field = "pw"
                    elif active_field == "pw": active_field = "nick"
                    else: active_field = "id"
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    if active_field == "id": user_id += event.unicode
                    elif active_field == "pw": user_pw += event.unicode
                    elif active_field == "nick": nickname += event.unicode

        # 화면 그리기
        draw_signup_screen(screen, font, small_font, id_box, pw_box, nick_box, signup_btn, cancel_btn, 
                           user_id, user_pw, nickname, msg, active_field, bg_image)
        pygame.display.flip()

# ==========================================
# 화면을 그리는 함수 (코드 깔끔하게 분리)
# ==========================================
def draw_signup_screen(screen, font, small_font, id_box, pw_box, nick_box, signup_btn, cancel_btn, 
                       user_id, user_pw, nickname, msg, active_field, bg_image):
    WIDTH = screen.get_width()
    
    # 배경 그리기
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(COLOR_BG)

    # 텍스트 라벨 (입력창 위에 조그맣게 표시)
    screen.blit(small_font.render("ID:", True, COLOR_TEXT), (id_box.x, id_box.y - 25))
    screen.blit(small_font.render("PW:", True, COLOR_TEXT), (pw_box.x, pw_box.y - 25))
    screen.blit(small_font.render("Nickname:", True, COLOR_TEXT), (nick_box.x, nick_box.y - 25))

    # 입력창 테두리 그리기 (현재 선택된 칸은 두껍게)
    pygame.draw.rect(screen, COLOR_BOX, id_box)
    pygame.draw.rect(screen, COLOR_ACTIVE if active_field == "id" else COLOR_BOX, id_box, 3 if active_field == "id" else 1)
    
    pygame.draw.rect(screen, COLOR_BOX, pw_box)
    pygame.draw.rect(screen, COLOR_ACTIVE if active_field == "pw" else COLOR_BOX, pw_box, 3 if active_field == "pw" else 1)
    
    pygame.draw.rect(screen, COLOR_BOX, nick_box)
    pygame.draw.rect(screen, COLOR_ACTIVE if active_field == "nick" else COLOR_BOX, nick_box, 3 if active_field == "nick" else 1)

    # 버튼 그리기
    pygame.draw.rect(screen, COLOR_SIGNUP_BTN, signup_btn, border_radius=10)
    pygame.draw.rect(screen, COLOR_CANCEL_BTN, cancel_btn, border_radius=10)
    
    signup_text = font.render("CREATE", True, COLOR_TEXT)
    screen.blit(signup_text, (signup_btn.centerx - signup_text.get_width()//2, signup_btn.centery - signup_text.get_height()//2))
    
    cancel_text = font.render("CANCEL", True, COLOR_TEXT)
    screen.blit(cancel_text, (cancel_btn.centerx - cancel_text.get_width()//2, cancel_btn.centery - cancel_text.get_height()//2))

    # 입력된 텍스트 화면에 표시 (비밀번호는 *로 가림)
    screen.blit(font.render(user_id, True, COLOR_TEXT), (id_box.x + 10, id_box.y + 5))
    screen.blit(font.render("*" * len(user_pw), True, COLOR_TEXT), (pw_box.x + 10, pw_box.y + 5))
    screen.blit(font.render(nickname, True, COLOR_TEXT), (nick_box.x + 10, nick_box.y + 5))

    # 하단 안내 메시지 그리기
    msg_surf = small_font.render(msg, True, (255, 200, 100))
    screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 580))