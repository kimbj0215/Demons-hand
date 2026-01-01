import combat
def start_game(user_id, user_nick,user_stage, user_hp):
    print(f"환영합니다 {user_nick}님! 게임을 시작합니다.")
    combat.start_game_process(user_id, user_nick, user_stage, user_hp)
