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
        "default_scene": "Create an educational video that explains the topic clearly with visual examples and a simple structure."
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
# 국가별 언어 데이터
# ----------------------------
country_data = {
    "한국": "Korean",
    "미국": "English",
    "일본": "Japanese",
    "중국": "Chinese",
    "프랑스": "French",
    "스페인": "Spanish",
    "독일": "German"
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
# 영상 비율 데이터
# ----------------------------
ratio_map = {
    "세로형 숏폼 9:16": "vertical 9:16 format for TikTok, YouTube Shorts, and Instagram Reels",
    "가로형 16:9": "horizontal 16:9 format for YouTube and presentation videos",
    "정사각형 1:1": "square 1:1 format for social media posts"
}

# ----------------------------
# 대사 지시문 생성 함수
# ----------------------------
def generate_dialogue_instruction(dialogue_type, country, user_dialogue):
    language = country_data[country]

    if dialogue_type == "자동대사":
        return f"""
Dialogue:
Include natural spoken dialogue in {language}.
The dialogue should fit the selected topic, country, mood, and scene naturally.
Do not use a fixed scripted sentence.
Make the dialogue sound realistic, short, and appropriate for the video style.
""".strip()

    if dialogue_type == "입력대사":
        if user_dialogue.strip():
            return f"""
Dialogue:
Include the following exact spoken dialogue in {language}.
The dialogue must be naturally integrated into the scene.

Dialogue line:
"{user_dialogue.strip()}"
""".strip()
        else:
            return f"""
Dialogue:
No dialogue line was entered by the user.
If dialogue is needed, include short and natural spoken dialogue in {language} that fits the scene.
""".strip()


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
    extra_detail,
    dialogue_type,
    user_dialogue
):
    category = category_data[primary_keyword]
    language = country_data[country]

    situation = custom_situation.strip() if custom_situation.strip() else category["default_scene"]
    extra = extra_detail.strip()
    dialogue_instruction = generate_dialogue_instruction(dialogue_type, country, user_dialogue)

    if extra:
        extra_instruction = f"""
Additional user detail:
{extra}
""".strip()
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

{extra_instruction}

Camera:
{camera_map[camera_style]}

Audio:
Use realistic audio that matches the selected video style.
If dialogue is included, keep it short, natural, and suitable for the selected country and language.
Use realistic environmental sounds that fit the scene.
Avoid unnecessary background noise.

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
    extra_detail,
    dialogue_type,
    user_dialogue
):
    language = country_data[country]
    category = category_data[primary_keyword]

    situation = custom_situation.strip() if custom_situation.strip() else "기본 장면 구성을 사용함"
    extra = extra_detail.strip() if extra_detail.strip() else "추가 세부 내용 없음"

    if dialogue_type == "자동대사":
        dialogue_summary = f"선택한 국가의 언어인 {language}로 장면에 어울리는 자연스러운 대사가 생성되도록 설정함"
    else:
        if user_dialogue.strip():
            dialogue_summary = f"사용자가 입력한 대사 사용: {user_dialogue.strip()}"
        else:
            dialogue_summary = "입력대사를 선택했지만 입력된 대사가 없어, 필요한 경우 자연스러운 대사를 생성하도록 설정함"

    report = f"""
선택한 1차 키워드: {primary_keyword}
선택한 2차 키워드: {secondary_keyword}
카테고리 설명: {category['description']}

선택한 국가: {country}
사용 언어: {language}

영상 길이: 약 {duration}초
영상 분위기: {tone}
카메라 연출: {camera_style}
영상 비율: {ratio}

사용자 세부 상황:
{situation}

추가 세부 내용:
{extra}

대사 방식:
{dialogue_type}

대사 설정:
{dialogue_summary}

이 시스템은 사용자가 선택한 영상 장르, 세부 키워드, 국가, 상황 설명, 대사 방식을 바탕으로 Veo 3.1에 입력 가능한 영상 프롬프트를 자동 생성합니다.
""".strip()

    return report


# ----------------------------
# UI 화면 구성
# ----------------------------
st.title("AI 영상 프롬프트 자동화 시스템")

st.markdown(
    """
    사용자가 **1차 키워드, 2차 키워드, 국가, 세부 상황, 대사 방식**을 선택하면  
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

    dialogue_type = st.radio(
        "대사 방식 선택",
        ["자동대사", "입력대사"]
    )

    user_dialogue = ""

    if dialogue_type == "입력대사":
        user_dialogue = st.text_area(
            "사용할 대사 입력",
            placeholder="예: 오늘 하루를 더 특별하게 만들어 줄 작은 습관을 소개합니다."
        )

    custom_situation = st.text_area(
        "세부 상황 입력",
        placeholder="예: 대학생이 편의점 음식을 먹으며 솔직하게 맛을 설명하는 장면"
    )

    extra_detail = st.text_area(
        "추가 세부 내용",
        placeholder="예: 숏폼 느낌으로 빠르게 전개, 음식 클로즈업 강조, 밝고 재미있는 분위기"
    )

    generate_btn = st.button("프롬프트 생성")

with col2:
    st.subheader("선택 정보 미리보기")

    st.write(f"**1차 키워드:** {primary_keyword}")
    st.write(f"**2차 키워드:** {secondary_keyword}")
    st.write(f"**카테고리 설명:** {category_data[primary_keyword]['description']}")

    st.markdown("---")

    st.write(f"**선택 국가:** {country}")
    st.write(f"**사용 언어:** {country_data[country]}")

    st.markdown("---")

    st.write(f"**영상 분위기:** {tone}")
    st.write(f"**카메라 연출:** {camera_style}")
    st.write(f"**영상 비율:** {ratio}")
    st.write(f"**대사 방식:** {dialogue_type}")

    if dialogue_type == "자동대사":
        st.info("자동대사 선택 시, 특정 문장을 넣는 것이 아니라 선택한 국가 언어로 자연스러운 대사가 나오도록 프롬프트에 지시합니다.")
    else:
        st.info("입력대사 선택 시, 사용자가 입력한 문장이 프롬프트의 대사로 들어갑니다.")

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
        extra_detail=extra_detail,
        dialogue_type=dialogue_type,
        user_dialogue=user_dialogue
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
        extra_detail=extra_detail,
        dialogue_type=dialogue_type,
        user_dialogue=user_dialogue
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
