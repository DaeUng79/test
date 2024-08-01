import streamlit as st
import json
from openai import OpenAI

st.set_page_config(layout="wide")
client = OpenAI()

# JSON 파일 읽기
with open('gabgil_define.json', 'r', encoding='utf-8') as file:
    gabgil_define = json.load(file)

with open('gabgil_cases.json', 'r', encoding='utf-8') as file:
    gabgil_cases = json.load(file)


def 갑질상담(내용): 
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            # {"role": "system", "content": f"당신은 갑질의 개념 {gabgil_define['갑질의 개념']}과 갑질 유형분류 {gabgil_define['갑질의 유형']}를 숙지하는 상담원입니다. 상담 순서는 입력된 내용{내용} 화면에 출력한 후 상세히 분석하여 상답해야 합니다. 갑질 유형을 분류 안내를 시작으로 유형별 갑질 사례 {gabgil_cases['유형별_갑질_사례']} 3개 이상 안내하고, 해당 갑질 사례의 통계{gabgil_cases['유형통계']}를 화면에 표시후 친절하게 안내되어야 합니다."},

            {"role": "system", "content": f"""
             당신은 공공분야 갑질 방지 및 예방을 위한 분석가입니다.
             {gabgil_define['갑질의 개념']}, {gabgil_define['갑질의 유형']}, {gabgil_cases['유형별_갑질_사례']}, {gabgil_cases['유형통계']}을 기준으로 이해하고있으며, 상담내용{내용}을 기준으로 유사 사례와 징계사항을 포함하여 자세한 분석결과와 예방대책을 알려주세요
             """}, 

            {"role": "user", "content": f"상담내용{내용}"}  
        ],
        stream=True
    )
    return completion

def 상담출력(completion):
    output_placeholder = st.empty()
    full_text = ""
    for chunk in completion:
        if hasattr(chunk.choices[0].delta, 'content'):
            content = chunk.choices[0].delta.content
            if content:
                full_text += content
                output_placeholder.write(full_text)
    return full_text
 

st.title("국무조정실 갑질 예방 및 진단 챗봇")

st.success("**✔️ 공공기관 갑질 사례집'의 내용을 바탕으로 8가지 갑질 유형과 주요 사례를 확인할 수 있으며, 본인의 상황이나 갑질 사례를 입력하면 공공기관 갑질 사례 기준으로 인공지능이 분석한 결과를 확인할 수 있습니다.**\n\n"
           "**:orange[✔️ 입력된 정보는 저장되지 않으며, 브라우저를 새로고침하면 자료가 삭제됩니다. 참고용으로 활용하시기 바랍니다.]**\n\n"
           )

내용 = st.text_area("**🔹 내용을 입력하세요**", 
                    placeholder='(공공분야 갑질 알아보기) 갑질 징계 기준에 대해서 알려줘, 갑질 유형에 대해서 알려줘, 갑질 사례에 대해서 알려줘\n\n'
                                '(팀장 관점) 내가 커피를 사는데 팀원에게 카드를 주며 "너 커피도 같이 사와"라고 말했는데, 이것이 갑질인가요?\n\n'
                                '(직원 관점) 팀장이 내 커피도 사오라며 자신의 카드를 주는데, 업무도 많고 가기 싫어서 짜증나고 힘들어요.', height=150)

if st.button("분석 및 진단하기"):
    if 내용:
        completion = 갑질상담(내용)
        full_text = 상담출력(completion)
    else:
        st.error("사례를 알려주세요.")
