import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=openai_api_key)

def analyze_diary_and_comfort(diary_text):
    if not diary_text.strip():
        return "일기 내용이 비어 있어 분석할 수 없습니다.", "따뜻한 위로를 전할 수 없습니다."

    try:
        
        analysis_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 사용자의 감정 상태를 부드럽게 분석하는 심리 상담가야."},
                {"role": "user", "content": f"다음은 사용자가 쓴 일기야:\n{diary_text}\n이 사용자의 감정 상태를 간결하고 따뜻하게 분석해줘."}
            ]
        )
        analysis_result = analysis_response.choices[0].message.content

    
        comfort_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 사용자의 마음을 따뜻하게 위로하는 심리 상담가야."},
                {"role": "user", "content": f"다음은 사용자가 쓴 일기야:\n{diary_text}\n이 사용자에게 따뜻하고 진심 어린 위로의 말을 건네줘."}
            ]
        )
        comfort_message = comfort_response.choices[0].message.content

        return analysis_result, comfort_message

    except Exception as e:
        return f"⚠️ 감정 분석 실패: {e}", f"⚠️ 위로 생성 실패: {e}"
