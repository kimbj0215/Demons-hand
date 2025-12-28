# main.py
import login
import game
import sys

def main():
    is_success, user_id, user_nick = login.show_login_screen()
    
    if is_success:
        game.start_game(user_id, user_nick)
    else:
        print("로그인 실패 또는 종료")
        sys.exit()

if __name__ == "__main__":
    main()