import os
import bcrypt
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_user(input_id, input_pw, input_nickname):
    """
    유저 정보를 DB에 저장합니다.
    성공 시 (True, 메시지), 실패 시 (False, 에러메시지)를 반환합니다.
    """
    print(f"\n=== 악마의 패(Demon's Hand) 회원가입 시도: {input_id} ===")
    print("DB 저장 중...")

    try:
        hashed_pw = bcrypt.hashpw(input_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # 새로 가입할 유저의 데이터 세팅
        # (게임 시작 시 기본 체력을 100, 스테이지를 "00"으로 설정합니다)
        new_user_data = {
            "user_id": input_id,
            "password": hashed_pw,
            "nickname": input_nickname,
            "current_stage": "00",  # 초기 스테이지
            "user_hp": 100          # 초기 체력
        }

        # Supabase users 테이블에 데이터 삽입
        response = supabase.table("users").insert(new_user_data).execute()

        # 데이터가 정상적으로 들어갔다면 반환
        if len(response.data) > 0:
            print(">> 회원가입 성공!")
            return True, "회원가입이 완료되었습니다."
        else:
            return False, "알 수 없는 이유로 가입에 실패했습니다."

    except Exception as e:
        error_msg = str(e)
        print(f">> 서버 에러 발생: {error_msg}")
        
        # 중복 아이디 에러 잡기 (Supabase/PostgreSQL의 Unique 제약 조건 위반 시)
        if "duplicate key value" in error_msg or "Unique violation" in error_msg:
            return False, "이미 사용 중인 아이디입니다."
        else:
            return False, "서버 연결에 실패했습니다."