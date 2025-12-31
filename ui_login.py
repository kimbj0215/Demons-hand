import pygame
import sys
# [설명] login.py 파일에 있는 'supabase' 접속 도구를 가져옵니다. 
# 이렇게 하면 ui_login에서도 서버에 접속할 수 있습니다.
from login import supabase 

# 1. 초기 설정 (환경 구축)
pygame.init()

# [설명] 게임 창의 가로와 세로 크기를 설정합니다.
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("악마의 패 - 로그인 화면")

# [설명] 글꼴을 설정합니다. 한글이 깨지지 않게 'malgungothic'을 사용합니다.
font = pygame.font.SysFont("malgungothic", 30)
small_font = pygame.font.SysFont("malgungothic", 20)

# [설명] 사용할 색상들을 이름표로 미리 정해둡니다 (RGB 값).
COLOR_BG = (20, 20, 25)      # 어두운 배경색
COLOR_BOX = (60, 60, 65)     # 입력창 배경색
COLOR_TEXT = (255, 255, 255) # 흰색 글자
COLOR_BTN = (100, 30, 30)    # 로그인 버튼색 (진한 빨강)
COLOR_ACTIVE = (180, 180, 200) # 클릭했을 때 강조색

# 2. 사용자 입력 및 상태 관리 변수
user_id = ""       # 사용자가 입력한 아이디 저장용
user_pw = ""       # 사용자가 입력한 비밀번호 저장용
login_message = "" # "로그인 중...", "성공!" 등의 메시지 표시용
active_field = "id" # 현재 어느 칸에 글을 쓰고 있는지 기록

# [설명] pygame.Rect는 사각형의 위치와 크기를 정의합니다. (x좌표, y좌표, 가로, 세로)
id_box = pygame.Rect(WIDTH//2 - 100, 300, 200, 45)
pw_box = pygame.Rect(WIDTH//2 - 100, 380, 200, 45)
login_btn = pygame.Rect(WIDTH//2 - 100, 480, 200, 50)

# 3. 메인 루프 (1초에 60번씩 반복 실행)
while True:
    # [A] 이벤트 체크 (마우스/키보드 감시)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # 창 닫기 버튼 눌렀을 때
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 클릭 시
            # [설명] 클릭한 위치(event.pos)가 각 상자 안에 있는지 확인합니다.
            if id_box.collidepoint(event.pos):
                active_field = "id"
            elif pw_box.collidepoint(event.pos):
                active_field = "pw"
            elif login_btn.collidepoint(event.pos):
                # [설명] 로그인 버튼을 클릭하면 서버에 물어보는 로직을 실행합니다.
                login_message = "서버 연결 확인 중..."
                try:
                    # [설명] login.py에서 가져온 supabase 도구로 DB를 조회합니다.
                    response = supabase.table("users") \
                        .select("*") \
                        .eq("user_id", user_id) \
                        .eq("password", user_pw) \
                        .execute()
                    
                    if len(response.data) > 0:
                        login_message = f"성공! {response.data[0]['nickname']}님 환영합니다."
                        # 여기에 나중에 다음 화면으로 넘어가는 코드를 넣을 거예요.
                    else:
                        login_message = "실패: 아이디/비번을 확인하세요."
                except Exception as e:
                    login_message = f"에러 발생: {e}"

        if event.type == pygame.KEYDOWN: # 키보드를 눌렀을 때
            if event.key == pygame.K_BACKSPACE: # 지우기 키
                if active_field == "id": user_id = user_id[:-1]
                else: user_pw = user_pw[:-1]
            elif event.key == pygame.K_TAB: # 탭 키를 누르면 입력칸 이동
                active_field = "pw" if active_field == "id" else "id"
            else:
                # [설명] 누른 글자를 각 변수에 추가합니다.
                if active_field == "id": user_id += event.unicode
                else: user_pw += event.unicode

    # [B] 화면 그리기 (도화지에 작업하기)
    screen.fill(COLOR_BG) # 배경을 어둡게 칠합니다.

    # 제목 그리기
    title_surface = font.render("DEMON'S HAND", True, (200, 50, 50))
    screen.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 150))

    # 입력창 상자 그리기 (선택된 창은 테두리를 두껍게 표시)
    id_border = 3 if active_field == "id" else 1
    pw_border = 3 if active_field == "pw" else 1
    pygame.draw.rect(screen, COLOR_BOX, id_box) # 아이디 칸 배경
    pygame.draw.rect(screen, COLOR_ACTIVE, id_box, id_border) # 아이디 칸 테두리
    
    pygame.draw.rect(screen, COLOR_BOX, pw_box) # 비번 칸 배경
    pygame.draw.rect(screen, COLOR_ACTIVE, pw_box, pw_border) # 비번 칸 테두리

    # 로그인 버튼 그리기
    pygame.draw.rect(screen, COLOR_BTN, login_btn, border_radius=10)
    btn_text = font.render("LOGIN", True, COLOR_TEXT)
    screen.blit(btn_text, (login_btn.centerx - btn_text.get_width()//2, login_btn.centery - btn_text.get_height()//2))

    # [설명] 입력 중인 텍스트를 화면에 그립니다.
    id_surf = font.render(user_id, True, COLOR_TEXT)
    screen.blit(id_surf, (id_box.x + 10, id_box.y + 5))
    
    # [설명] 비밀번호는 보안상 '*'로 표시되게 만듭니다.
    pw_display = "*" * len(user_pw)
    pw_surf = font.render(pw_display, True, COLOR_TEXT)
    screen.blit(pw_surf, (pw_box.x + 10, pw_box.y + 5))

    # 결과 메시지 그리기
    msg_surf = small_font.render(login_message, True, (255, 200, 100))
    screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, 550))

    # [C] 화면 업데이트 (그린 도화지를 모니터에 출력)
    pygame.display.flip()