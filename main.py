import sys
import pygame
import game 
# 'login' 대신 방금 만든 'ui_login'에서 함수를 가져옵니다.
from ui_login import show_login_window 

def main():
    # 1. Pygame 초기화 (창 만들기)
    pygame.init()
    
    # 해상도 설정 (ui_login.py와 똑같이 맞춥니다)
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("악마의 패 (Demon's Hand)")

    # 2. GUI 로그인 화면 실행
    # show_login_window 함수에 'screen(창)'을 넘겨줘야 그림을 그릴 수 있습니다.
    # 로그인이 성공하면 유저 정보(딕셔너리)가 돌아옵니다.
    user_data = show_login_window(screen)
    
    # 3. 로그인 결과 처리
    if user_data:
        print(f"✅ 메인: {user_data['nickname']}님 로그인 성공!")
        
        # 4. 게임 시작
        # 유저 정보를 쪼개서 game.start_game으로 넘깁니다.
        # (주의: game.py도 pygame 화면(screen)을 받아야 이어집니다!)
        game.start_game(
            screen,  # ★ 게임 화면도 이 창에 그려야 하니 screen을 넘겨줍니다.
            user_data['user_id'], 
            user_data['nickname'], 
            user_data['current_stage'], 
            user_data['user_hp']
        )
    else:
        print("❌ 로그인을 취소했거나 실패하여 종료합니다.")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()