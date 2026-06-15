import random
import streamlit as st


# 1. 기존 인증코드 생성 함수
def g_code():
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    num3 = random.randint(0, 9)
    num4 = random.randint(0, 9)
    code = [num1, num2, num3, num4]
    return code


# 2. 스트림릿 세션 상태(Session State) 초기화
if "a_code" not in st.session_state:
    st.session_state.a_code = g_code()

if "lock" not in st.session_state:
    st.session_state.lock = True

# 3. 화면 UI 구성
st.title("🔒 보안 인증 시스템")

code_str = "".join(str(d) for d in st.session_state.a_code)
st.text("=================================")
st.code(f"인증코드: {code_str}", language="")
st.text("=================================")

# 4. 잠금 상태에 따른 로직 처리
if st.session_state.lock:
    # 엔터키나 버튼 클릭 시 한 번에 처리하기 위해 form 사용
    with st.form(key="auth_form", clear_on_submit=True):
        input_str = st.text_input("인증코드를 입력하세요:")
        submit_button = st.form_submit_button(label="인증하기")

        if submit_button:
            # 입력값 변환 로직 (숫자가 아닌 입력 시 에러 방지)
            try:
                input_code = [int(i) for i in input_str]
            except ValueError:
                input_code = []

            # 인증 성공 여부 확인
            if st.session_state.a_code == input_code:
                st.success("인증되었습니다. 잠금을 해제합니다.")
                st.session_state.lock = False
                st.rerun()  # 💡 이 부분의 오타(st.rarun)를 st.rerun()으로 수정했습니다!
            else:
                st.error("인증코드가 일치하지 않습니다. 다시 시도해 주세요.")
                # 실패 시 새로운 인증코드 생성
                st.session_state.a_code = g_code()
                st.rerun()
else:
    st.balloons()  # 축하 효과
    st.success("🔓 잠금이 해제되었습니다! 환영합니다.")

    # 다시 테스트해볼 수 있도록 리셋 버튼 추가
    if st.button("다시 잠그기"):
        st.session_state.lock = True
        st.session_state.a_code = g_code()
        st.rerun()