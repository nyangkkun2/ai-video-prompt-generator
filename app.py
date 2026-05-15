import streamlit as st

st.set_page_config(page_title="화장실 위생 AI 영상 프롬프트 자동화 시스템", layout="wide")

# ----------------------------
# 기본 데이터
# ----------------------------
hygiene_data = {
    "칫솔": {
        "wrong_example": "toothbrush placed too close to the toilet",
        "risk": "it may be exposed to invisible particles and bathroom moisture",
        "correct_example": "the toothbrush is stored in a clean covered holder away from the toilet",
        "ending_message": "Store your toothbrush in a clean and dry place away from the toilet."
    },
    "수건": {
        "wrong_example": "a damp towel crumpled in a poorly ventilated corner",
        "risk": "moisture can cause unpleasant odors and bacterial growth",
        "correct_example": "the towel is spread out neatly on a towel bar to dry",
        "ending_message": "Dry your towel properly after each use."
    },
    "샤워볼": {
        "wrong_example": "a wet shower puff left on the floor or in a wet soap dish",
        "risk": "remaining moisture can create an unhygienic environment",
        "correct_example": "the shower puff is squeezed dry and hung in a well-ventilated place",
        "ending_message": "Keep your shower puff dry and well ventilated."
    },
    "면도기": {
        "wrong_example": "a razor left in a wet sink area with water droplets remaining on it",
        "risk": "constant moisture may reduce cleanliness and hygiene",
        "correct_example": "the razor is rinsed, dried, and stored in a clean dry holder",
        "ending_message": "Store your razor dry and clean after use."
    },
    "슬리퍼": {
        "wrong_example": "bathroom slippers left wet on the floor without drying",
        "risk": "continued dampness may create an uncomfortable and unhygienic condition",
        "correct_example": "the slippers are placed in a dry ventilated area",
        "ending_message": "Dry bathroom slippers regularly for better hygiene."
    }
}

tone_map = {
    "교육용": "educational, clear, practical, easy to understand",
    "공익광고 느낌": "public service announcement style, serious but approachable",
    "부드러운 정보 전달": "calm, clean, friendly, informative",
    "경고형": "alert, cautionary, impactful but not shocking"
}

camera_map = {
    "기본": "smooth camera movement, medium shots and close-up shots",
    "클로즈업 중심": "close-up shots focusing on the hygiene item and moisture details",
    "전후 비교 강조": "clear before-and-after comparison shots with smooth transitions",
    "시네마틱": "cinematic camera movement with polished framing and gentle transitions"
}

# ----------------------------
# 프롬프트 생성 함수
# ----------------------------
def generate_prompt(
    item,
    duration,
    tone,
    camera_style,
    custom_situation,
    custom_message,
    extra_detail,
    include_text_overlay
):
    data = hygiene_data[item]

    wrong_example = data["wrong_example"]
    risk = data["risk"]
    correct_example = data["correct_example"]
    ending_message = custom_message.strip() if custom_message.strip() else data["ending_message"]

    if custom_situation.strip():
        wrong_scene_detail = f"Incorporate this specific situation: {custom_situation.strip()}."
    else:
        wrong_scene_detail = ""

    if extra_detail.strip():
        extra_scene_detail = f"Additional detail to include: {extra_detail.strip()}."
    else:
        extra_scene_detail = ""

    text_overlay_instruction = ""
    if include_text_overlay:
        text_overlay_instruction = f'At the end, include simple on-screen text: "{ending_message}"'

    prompt = f"""
Create one realistic short video for Veo 3.1 about bathroom hygiene.

Main topic:
{item}

Video duration:
Approximately {duration} seconds.

Overall style:
{tone_map[tone]}
The bathroom should look realistic, clean, modern, and relatable to everyday life.
Do not make the scene disgusting or exaggerated.

Scene structure:

Scene 1:
Show an ordinary bathroom environment.
Focus on {wrong_example}.
{wrong_scene_detail}

Scene 2:
Visually emphasize the hygiene problem in a subtle and educational way.
Show that {risk}.
Use visual storytelling to suggest the problem without using shocking imagery.

Scene 3:
Transition to the correct habit.
Show that {correct_example}.

Scene 4:
Show a clean, well-organized bathroom environment after the correction.
Clearly communicate the positive result of proper storage and hygiene habits.
{extra_scene_detail}

Scene 5:
End with a neat final shot that reinforces the hygiene lesson.
{text_overlay_instruction}

Camera:
{camera_map[camera_style]}

Audio:
No human voice, no narration, no background music.
Use only natural bathroom ambience such as soft room tone, light water sounds, object movement sounds, and gentle environmental sounds.

Important:
Generate only one coherent video prompt.
Keep the video easy to understand and suitable for a university class presentation about generative AI and daily hygiene education.
""".strip()

    return prompt


def generate_scene_summary(item, custom_situation, custom_message):
    data = hygiene_data[item]

    situation_text = custom_situation if custom_situation.strip() else f"{item}의 잘못된 보관 상황"
    message_text = custom_message if custom_message.strip() else data["ending_message"]

    summary = {
        "장면 1": f"일반적인 화장실 환경에서 {situation_text}을 보여줌",
        "장면 2": f"{item} 보관 방식의 위생상 위험성을 시각적으로 강조",
        "장면 3": f"{item}의 올바른 보관 방법 제시",
        "장면 4": "정리되고 위생적인 화장실 상태를 보여줌",
        "장면 5": f"마무리 메시지 전달: {message_text}"
    }
    return summary


# ----------------------------
# UI
# ----------------------------
st.title("화장실 위생 AI 영상 프롬프트 자동화 시스템")
st.markdown("키워드와 세부 내용을 입력하면 **Veo 3.1용 영상 프롬프트**를 자동 생성합니다.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("입력")
    selected_item = st.selectbox("위생 키워드 선택", list(hygiene_data.keys()))
    duration = st.slider("영상 길이(초)", 15, 60, 30)
    tone = st.selectbox("영상 분위기", list(tone_map.keys()))
    camera_style = st.selectbox("카메라 연출", list(camera_map.keys()))
    custom_situation = st.text_area(
        "세부 상황 입력",
        placeholder="예: 변기 바로 옆 컵에 칫솔이 꽂혀 있고 물기가 남아 있는 상황"
    )
    custom_message = st.text_input(
        "마무리 메시지 입력",
        placeholder="예: 작은 습관이 더 건강한 욕실을 만듭니다."
    )
    extra_detail = st.text_area(
        "추가 세부 내용",
        placeholder="예: 전후 비교가 잘 드러나게 보여주기, 학생들도 공감할 수 있는 욕실 분위기"
    )
    include_text_overlay = st.checkbox("마지막 장면에 텍스트 삽입", value=True)

    generate_btn = st.button("프롬프트 생성")

with col2:
    st.subheader("기본 정보")
    base_info = hygiene_data[selected_item]
    st.write(f"**잘못된 예시:** {base_info['wrong_example']}")
    st.write(f"**위험 요소:** {base_info['risk']}")
    st.write(f"**올바른 예시:** {base_info['correct_example']}")
    st.write(f"**기본 마무리 문구:** {base_info['ending_message']}")

if generate_btn:
    prompt = generate_prompt(
        item=selected_item,
        duration=duration,
        tone=tone,
        camera_style=camera_style,
        custom_situation=custom_situation,
        custom_message=custom_message,
        extra_detail=extra_detail,
        include_text_overlay=include_text_overlay
    )

    summary = generate_scene_summary(selected_item, custom_situation, custom_message)

    st.markdown("---")
    st.subheader("1) 자동 생성된 장면 구성 요약")
    for scene, desc in summary.items():
        st.write(f"**{scene}**: {desc}")

    st.subheader("2) 최종 Veo 3.1 프롬프트")
    st.code(prompt, language="text")

    st.download_button(
        label="프롬프트 TXT로 다운로드",
        data=prompt,
        file_name=f"{selected_item}_veo_prompt.txt",
        mime="text/plain"
    )

    st.success("프롬프트 생성 완료!")