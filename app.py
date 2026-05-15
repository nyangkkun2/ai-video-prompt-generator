import streamlit as st

st.set_page_config(
    page_title="AI 영상 프롬프트 자동화 시스템",
    layout="wide"
)

# ----------------------------
# 1차 키워드와 2차 키워드 데이터
# ----------------------------
category_data = {
    "먹방": {
        "secondary": ["한식 먹방", "디저트 먹방", "편의점 음식 먹방", "야식 먹방", "매운 음식 먹방"],
        "description": "음식의 맛, 식감, 분위기, 먹는 장면을 중심으로 구성되는 영상",
        "default_scene": "Show a realistic food scene with close-up shots of the food, eating reactions, and a cozy atmosphere."
    },
    "브이로그": {
        "secondary": ["대학생 브이로그", "카페 브이로그", "여행 브이로그", "운동 브이로그", "하루 일상 브이로그"],
        "description": "일상적인 경험과 감정을 자연스럽게 보여주는 영상",
        "default_scene": "Show a natural daily-life vlog with realistic camera movement, casual moments, and emotional details."
    },
    "정보전달": {
        "secondary": ["생활 꿀팁", "건강 정보", "경제 정보", "IT 정보", "학습 정보"],
        "description": "시청자에게 특정 정보를 쉽고 명확하게 전달하는 영상",
        "default_scene": "Create an educational video that explains the topic clearly with visual examples and simple structure."
    },
    "광고": {
        "secondary": ["제품 광고", "서비스 광고", "앱 광고", "브랜드 광고", "공익 광고"],
        "description": "제품, 서비스, 브랜드 또는 메시지를 설득력 있게 전달하는 영상",
        "default_scene": "Create a polished promotional video with strong visual storytelling and a clear call-to-action."
    },
    "여행": {
        "secondary": ["도시 여행", "바다 여행", "캠핑 여행", "해외 여행", "맛집 여행"],
        "description": "장소의 분위기, 경험, 이동 장면, 감성을 중심으로 구성되는 영상",
        "default_scene": "Show a cinematic travel video with beautiful location shots, movement, and emotional atmosphere."
    },
    "제품소개": {
        "secondary": ["전자기기 소개", "화장품 소개", "생활용품 소개", "패션 아이템 소개", "앱 기능 소개"],
        "description": "제품의 기능, 장점, 사용 장면을 보여주는 영상",
        "default_scene": "Show a clean product introduction video with close-up shots, usage examples, and clear feature highlights."
    },
    "위생 캠페인": {
        "secondary": ["화장실 위생", "손 씻기", "칫솔 보관", "수건 관리", "샤워용품 관리"],
        "description": "생활 속 위생 문제와 올바른 습관을 알려주는 교육형 영상",
        "default_scene": "Create an educational hygiene campaign video showing a common mistake and the correct habit."
    }
}

# ----------------------------
# 국가별 언어 및 자동 대사 데이터
# ----------------------------
country_data = {
    "한국": {
        "language": "Korean",
        "dialogue": "작은 습관이 더 좋은 하루를 만듭니다."
    },
    "미국": {
        "language": "English",
        "dialogue": "Small habits can make your day better."
    },
    "일본": {
        "language": "Japanese",
        "dialogue": "小さな習慣が、より良い一日をつくります。"
    },
    "중국": {
        "language": "Chinese",
        "dialogue": "小小的习惯，可以让生活变得更好。"
    },
    "프랑스": {
        "language": "French",
        "dialogue": "De petites habitudes peuvent améliorer votre journée."
    },
    "스페인": {
        "language": "Spanish",
        "dialogue": "Los pequeños hábitos pueden mejorar tu día."
    },
    "독일": {
        "language": "German",
        "dialogue": "Kleine Gewohnheiten können deinen Tag verbessern."
    }
}

# ----------------------------
# 영상 분위기 데이터
# ----------------------------
tone_map = {
    "교육용": "educational, clear, practical, easy to understand",
    "감성적인": "emotional, warm, cinematic, soft and relatable",
    "재미있는": "fun, energetic, casual, entertaining",
    "공익광고 느낌": "public service announcement style, serious but approachable",
    "전문적인": "professional, polished, clean, trustworthy",
    "힙하고 트렌디한": "trendy, modern, social-media-friendly, dynamic"
}

# ----------------------------
# 카메라 연출 데이터
# ----------------------------
camera_map = {
    "기본": "smooth camera movement, medium shots and close-up shots",
    "클로즈업 중심": "close-up shots focusing on details, expressions, objects, and textures",
    "전후 비교 강조": "clear before-and-after comparison shots with smooth transitions",
    "시네마틱": "cinematic camera movement with polished framing and gentle transitions",
    "숏폼 스타일": "fast-paced vertical short-form video style with quick cuts and dynamic framing",
    "브이로그 스타일": "handheld vlog-style camera movement, natural framing, and realistic daily-life perspective"
}

# ----------------------------
# 영상 비율
# ----------------------------
ratio_map = {
    "세로형 숏폼 9:16": "vertical 9:16 format for TikTok, YouTube Shorts, and Instagram Reels",
    "가로형 16:9": "horizontal 16:9 format for YouTube and presentation videos",
    "정사각형 1:1": "square 1:1 format for social media posts"
}

# ----------------------------
# 프롬프트 생성 함수
# ----------------------------
def generate_prompt(
    primary_keyword,
    secondary_keyword,
    country,
    duration,
    tone,
    camera_style,
    ratio,
    custom_situation,
    custom_message,
    extra_detail,
    dialogue_mode,
    include_text_overlay
):
    category = category_data[primary_keyword]
    country_info = country_data[country]

    language = country_info["language"]
    auto_dialogue = country_info["dialogue"]

    final_message = custom_message.strip() if custom_message.strip() else auto_dialogue
    situation = custom_situation.strip() if custom_situation.strip() else category["default_scene"]
    extra = extra_detail.strip()

    if dialogue_mode == "자동 대사 사용":
        dialogue_instruction = f"""
Dialogue:
Include one short line of dialogue in {language}.
Use this line naturally:
"{final_message}"
"""
    elif dialogue_mode == "자막으로만 사용":
        dialogue_instruction = f"""
Dialogue:
Do not use spoken narration.
Use the following sentence only as on-screen subtitle text in {language}:
"{final_message}"
"""
    else:
        dialogue_instruction = """
Dialogue:
Do not include spoken dialogue or narration.
"""

    if include_text_overlay:
        text_overlay_instruction = f"""
On-screen text:
Add simple on-screen text in {language}.
Text: "{final_message}"
"""
    else:
        text_overlay_instruction = """
On-screen text:
Do not include additional on-screen text unless necessary.
"""

    if extra:
        extra_instruction = f"""
Additional user detail:
{extra}
"""
    else:
        extra_instruction = ""

    prompt = f"""
Create one high-quality AI-generated video prompt for Veo 3.1.

Main video category:
{primary_keyword}

Specific sub-topic:
{secondary_keyword}

Target country:
{country}

Target language:
{language}

Video duration:
Approximately {duration} seconds.

Video format:
{ratio_map[ratio]}

Overall style:
{tone_map[tone]}

Category purpose:
{category['description']}

User's detailed situation:
{situation}

Scene structure:

Scene 1:
Start with a visually clear opening scene that immediately shows the topic: {secondary_keyword}.
The setting, objects, people, and atmosphere should match the selected category: {primary_keyword}.

Scene 2:
Develop the main situation in a realistic and easy-to-understand way.
Focus on the key details provided by the user.
Make the scene feel natural, not artificial.

Scene 3:
Show the most important visual moment of the video.
Use strong visual storytelling to make the message clear.
The viewer should understand the purpose of the video even without a long explanation.

Scene 4:
Show the result, reaction, benefit, lesson, or conclusion depending on the selected category.
Make the ending suitable for a short AI-generated video.

Scene 5:
End with a clean final shot that reinforces the main message.

{dialogue_instruction}

{text_overlay_instruction}

{extra_instruction}

Camera:
{camera_map[camera_style]}

Audio:
Use audio that matches the selected video style.
If dialogue is included, keep it short and natural.
Avoid unnecessary background noise.
Use realistic environmental sounds that fit the scene.

Important instructions:
Generate only one coherent video prompt.
Keep the video realistic, visually clear, and suitable for a university presentation about an AI video prompt automation system.
Do not include inappropriate, violent, hateful, sexual, or unsafe content.
""".strip()

    return prompt


# ----------------------------
# 한국어 리포트 생성 함수
# ----------------------------
def generate_korean_report(
    primary_keyword,
    secondary_keyword,
    country,
    duration,
    tone,
    camera_style,
    ratio,
    custom_situation,
    custom_message,
    dialogue_mode
):
    country_info = country_data[country]
    category = category_data[primary_keyword]

    final_message = custom_message.strip() if custom_message.strip() else country_info["dialogue"]
    situation = custom_situation.strip() if custom_situation.strip() else "기본 장면 구성을 사용함"

    report = f"""
선택한 1차 키워드: {primary_keyword}
선택한 2차 키워드: {secondary_keyword}
카테고리 설명: {category['description']}

선택한 국가: {country}
사용 언어: {country_info['language']}
자동 생성 대사/문구: {final_message}

영상 길이: 약 {duration}초
영상 분위기: {tone}
카메라 연출: {camera_style}
영상 비율: {ratio}

사용자 세부 상황:
{situation}

대사 적용 방식:
{dialogue_mode}

이 시스템은 사용자가 선택한 영상 장르와 세부 키워드, 국가, 상황 설명을 바탕으로 Veo 3.1에 입력 가능한 영상 프롬프트를 자동 생성합니다.
""".strip()

    return report


# ----------------------------
# UI 화면 구성
# ----------------------------
st.title("AI 영상 프롬프트 자동화 시스템")
st.markdown(
    """
    사용자가 **1차 키워드, 2차 키워드, 국가, 세부 상황**을 선택하거나 입력하면  
    **Veo 3.1용 AI 영상 프롬프트**를 자동 생성하는 시스템입니다.
    """
)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("입력 설정")

    primary_keyword = st.selectbox(
        "1차 키워드 선택",
        list(category_data.keys())
    )

    secondary_keyword = st.selectbox(
        "2차 키워드 선택",
        category_data[primary_keyword]["secondary"]
    )

    country = st.selectbox(
        "원하는 국가 선택",
        list(country_data.keys())
    )

    duration = st.slider(
        "영상 길이(초)",
        10,
        90,
        30
    )

    tone = st.selectbox(
        "영상 분위기",
        list(tone_map.keys())
    )

    camera_style = st.selectbox(
        "카메라 연출",
        list(camera_map.keys())
    )

    ratio = st.selectbox(
        "영상 비율",
        list(ratio_map.keys())
    )

    dialogue_mode = st.radio(
        "대사 적용 방식",
        ["자동 대사 사용", "자막으로만 사용", "대사 없음"]
    )

    custom_situation = st.text_area(
        "세부 상황 입력",
        placeholder="예: 대학생이 편의점 음식을 먹으며 솔직하게 맛을 설명하는 장면"
    )

    custom_message = st.text_input(
        "직접 넣고 싶은 대사 또는 메시지",
        placeholder="비워두면 선택한 국가 언어에 맞는 기본 대사가 자동 사용됩니다."
    )

    extra_detail = st.text_area(
        "추가 세부 내용",
        placeholder="예: 숏폼 느낌으로 빠르게 전개, 음식 클로즈업 강조, 밝고 재미있는 분위기"
    )

    include_text_overlay = st.checkbox(
        "마지막 장면에 텍스트 삽입",
        value=True
    )

    generate_btn = st.button("프롬프트 생성")

with col2:
    st.subheader("선택 정보 미리보기")

    st.write(f"**1차 키워드:** {primary_keyword}")
    st.write(f"**2차 키워드:** {secondary_keyword}")
    st.write(f"**카테고리 설명:** {category_data[primary_keyword]['description']}")

    st.markdown("---")

    st.write(f"**선택 국가:** {country}")
    st.write(f"**사용 언어:** {country_data[country]['language']}")
    st.write(f"**기본 자동 대사:** {country_data[country]['dialogue']}")

    st.markdown("---")

    st.write(f"**영상 분위기:** {tone}")
    st.write(f"**카메라 연출:** {camera_style}")
    st.write(f"**영상 비율:** {ratio}")

# ----------------------------
# 결과 출력
# ----------------------------
if generate_btn:
    prompt = generate_prompt(
        primary_keyword=primary_keyword,
        secondary_keyword=secondary_keyword,
        country=country,
        duration=duration,
        tone=tone,
        camera_style=camera_style,
        ratio=ratio,
        custom_situation=custom_situation,
        custom_message=custom_message,
        extra_detail=extra_detail,
        dialogue_mode=dialogue_mode,
        include_text_overlay=include_text_overlay
    )

    report = generate_korean_report(
        primary_keyword=primary_keyword,
        secondary_keyword=secondary_keyword,
        country=country,
        duration=duration,
        tone=tone,
        camera_style=camera_style,
        ratio=ratio,
        custom_situation=custom_situation,
        custom_message=custom_message,
        dialogue_mode=dialogue_mode
    )

    st.markdown("---")

    st.subheader("1) 한국어 결과 리포트")
    st.text(report)

    st.subheader("2) 최종 Veo 3.1 프롬프트")
    st.code(prompt, language="text")

    st.download_button(
        label="프롬프트 TXT로 다운로드",
        data=prompt,
        file_name=f"{primary_keyword}_{secondary_keyword}_veo_prompt.txt",
        mime="text/plain"
    )

    st.success("프롬프트 생성 완료!")
