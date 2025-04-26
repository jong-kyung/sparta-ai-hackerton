import os
from openai import OpenAI
import streamlit as st



os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
openai_api_key = os.environ.get("OPENAI_API_KEY")


client = OpenAI(api_key=openai_api_key)

import re

def analyze_diary(diary_text):
    if not diary_text.strip():
        return "감정 일기가 비어 있습니다.", "https://www.youtube.com/watch?v=9Sc-ir2UwGU"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "너는 따뜻한 심리 상담가야. 사용자의 감정 일기를 읽고:\n"
                    "1. 감정 상태에 대한 언급 없이, 부드럽고 진심 어린 위로의 말을 건네줘.\n"
                    "2. 위로의 말 마지막에 꼭 어울리는 무료 YouTube 음악 링크를 하나 추천해줘. (YouTube만 가능)\n"
                    "3. 답변은 자연스럽고 사람다운 따뜻한 문장으로 작성해줘.\n"
                    "4. 링크는 반드시 텍스트 안에 자연스럽게 포함시켜줘."
                )},
                {"role": "user", "content": f"내가 쓴 감정 일기야:\n\n{diary_text}\n\n부드럽게 위로해줘."}
            ]
        )
        comfort_message = response.choices[0].message.content
        music_link = extract_music_link(comfort_message)
        return comfort_message, music_link
    except Exception as e:
        return f"⚠️ 위로 생성 실패: {e}", "https://www.youtube.com/watch?v=9Sc-ir2UwGU"

def extract_music_link(text):
    """
    텍스트 중 첫 번째 YouTube URL 추출
    """
    urls = re.findall(r'(https?://[^\s]+)', text)
    for url in urls:
        if "youtube.com" in url or "youtu.be" in url:
            return url
    return "https://www.youtube.com/watch?v=9Sc-ir2UwGU"


def analyze_diary_and_comfort(diary_text):
    if not diary_text.strip():
        return "일기 내용이 비어 있어 분석할 수 없습니다.", "따뜻한 위로를 전할 수 없습니다."

    try:
        
        analysis_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 나의 감정 상태를 부드럽게 분석하는 심리 상담가야."},
                {"role": "user", "content": f"내가 쓴 일기야:\n{diary_text}\n이 사용자의 감정 상태를 간결하고 따뜻하게 분석해줘."}
            ]
        )
        analysis_result = analysis_response.choices[0].message.content


        return analysis_result

    except Exception as e:
        return f"⚠️ 감정 분석 실패: {e}", f"⚠️ 위로 생성 실패: {e}"

def analyze_with_dsm5(diary_text, phq9_scores=None):
    """
    DSM-5 우울장애 진단 기준에 따라 일기를 전문적으로 분석합니다.
    
    Args:
        diary_text (str): 사용자의 일기 내용
        phq9_scores (list, optional): PHQ-9 설문 결과 점수 리스트
        
    Returns:
        dict: DSM-5 기준에 따른 분석 결과를 포함한 딕셔너리
    """
    if not diary_text.strip():
        return {
            "error": "일기 내용이 비어 있어 DSM-5 분석을 수행할 수 없습니다.",
            "symptom_analysis": {},
            "professional_opinion": "",
            "severity": "",
            "recommendation": ""
        }
    
    # DSM-5 우울장애 핵심 증상 목록과 설명 
    dsm5_symptoms = [
        "우울한 기분: 하루 중 대부분, 거의 매일",
        "흥미나 즐거움의 현저한 감소: 이전에 즐겨했던 활동에 흥미 상실",
        "체중 변화(의도하지 않은 체중 감소 또는 증가) 또는 식욕 변화",
        "불면증 또는 과다 수면",
        "정신운동성 초조 또는 지체(관찰 가능한 수준)",
        "피로감 또는 에너지 상실",
        "무가치감 또는 과도하거나 부적절한 죄책감",
        "사고력이나 집중력 감소, 우유부단함",
        "죽음에 대한 반복적인 생각, 자살 사고, 자살 시도 또는 계획"
    ]

    try:
        # PHQ-9 점수가 제공된 경우 함께 전달
        phq9_info = ""
        if phq9_scores and len(phq9_scores) == 9:
            total_score = sum(phq9_scores)
            phq9_info = f"PHQ-9 점수는 다음과 같습니다 (총점: {total_score}):\n"
            for i, score in enumerate(phq9_scores):
                phq9_info += f"- 문항 {i+1}: {score}점\n"
        
        # DSM-5 기준으로 분석 요청
        dsm5_prompt = f"""
다음은 사용자가 작성한 일기입니다:

{diary_text}

{phq9_info}

DSM-5 주요 우울장애 진단 기준에 따라 다음 증상들이 일기 내용에 나타나는지 전문적으로 분석해주세요:

{", ".join(dsm5_symptoms)}

다음 형식의 JSON으로 응답해주세요:
```json
{{
  "symptom_analysis": {{
    "우울한 기분": {{
      "present": true/false,
      "evidence": "일기에서 이 증상을 시사하는 구체적인 문구나 표현",
      "severity": "없음/경미함/중간/심각함 중 하나로 평가"
    }},
    "흥미나 즐거움의 감소": {{
      "present": true/false,
      "evidence": "일기에서 이 증상을 시사하는 구체적인 문구나 표현",
      "severity": "없음/경미함/중간/심각함 중 하나로 평가"
    }},
    // 나머지 7개 증상에 대해서도 동일한 형식으로 분석
  }},
  "positive_symptoms_count": 0-9 사이의 숫자 (present가 true인 증상의 수),
  "severity": "최소한의 우울증 징후/가벼운 우울증/중등도 우울증/중등도-심한 우울증/심한 우울증 중 하나",
  "professional_opinion": "일기 내용과 DSM-5 기준을 종합한 전문가 관점의 분석",
  "recommendation": "분석 결과에 따른 전문적 권고사항"
}}
```

전문가 관점에서 객관적이고 정확하게 분석해주세요. 다만, 이 분석은 공식적인 진단이 아니며 참고용일 뿐임을 기억하세요.
"""

        # API 호출하여 DSM-5 분석 결과 얻기
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 DSM-5 진단 기준에 정통한 정신건강 전문가입니다. 객관적이고 정확한 분석을 제공하되, 공식 진단이 아님을 항상 유의합니다."},
                {"role": "user", "content": dsm5_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # JSON 형식으로 결과 파싱
        result_text = response.choices[0].message.content
        import json
        
        try:
            result = json.loads(result_text)
            # 추가 정보 포함
            result["is_clinical_diagnosis"] = False
            result["disclaimer"] = "이 분석은 참고용일 뿐이며, 정확한 진단은 전문가와의 직접 상담을 통해 이루어져야 합니다."
            return result
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트 그대로 반환
            return {
                "error": "응답 형식 분석 실패",
                "raw_response": result_text,
                "is_clinical_diagnosis": False,
                "disclaimer": "이 분석은 참고용일 뿐이며, 정확한 진단은 전문가와의 직접 상담을 통해 이루어져야 합니다."
            }
            
    except Exception as e:
        return {
            "error": f"DSM-5 분석 중 오류가 발생했습니다: {str(e)}",
            "is_clinical_diagnosis": False,
            "disclaimer": "이 분석은 참고용일 뿐이며, 정확한 진단은 전문가와의 직접 상담을 통해 이루어져야 합니다."
        }
