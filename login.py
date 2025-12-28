import os
from supabase import create_client, Client

SUPABASE_URL = "https://najcspwedgqmopnjkhht.supabase.co"
SUPABASE_KEY = "sb_publishable_Hf0T9DUTjp7WkRdp2GIF-A_WW59gJEc"
print(f"내 URL 확인: [{SUPABASE_URL}]")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def show_login_screen():
    print("\n=== 악마의 패(Demon's Hand) 로그인 ===")
    input_id = input("아이디: ")
    input_pw = input("비밀번호: ")

    print("로그인 확인 중...")

    try:
        response = supabase.table("users") \
            .select("*") \
            .eq("user_id", input_id) \
            .eq("password", input_pw) \
            .execute()
        
        user_data = response.data

        if len(user_data) > 0:
            print(">> 로그인 성공!")
            return True, user_data[0]['user_id'], user_data[0]['nickname']
        else:
            print(">> 로그인 실패: 아이디나 비밀번호를 확인하세요.")
            return False, None

    except Exception as e:
        print(f">> 서버 에러 발생: {e}")
        return False, None
