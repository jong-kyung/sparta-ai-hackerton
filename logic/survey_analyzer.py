def survey_summary(scores):
    total_score = sum(scores)

    if total_score >= 20:
        return "고위험군: 즉시 전문가 상담이 필요합니다."
    elif total_score >= 10:
        return "중등도 위험군: 지속적인 관리가 필요합니다."
    else:
        return "낮은 위험 수준: 비교적 안정적입니다."