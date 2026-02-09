import map
def start_game(screen, user_id, user_nick,user_stage, user_hp):
    print(f"환영합니다 {user_nick}님! 게임을 시작합니다.")
    map.show_map_screen(screen, user_id, user_nick, user_stage, user_hp)