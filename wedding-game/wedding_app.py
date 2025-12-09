import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import urllib.parse

# --- 設定區 ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd0SOigmWPwEEP_zQv-LlPyCa99a-SQhqa0PP9kIvyJOaQbLw/formResponse"
FORM_FIELD_NICKNAME = "entry.276737520"
FORM_FIELD_SCORE = "entry.1217367258"
FORM_FIELD_ACCURACY = "entry.1332601410"
FORM_FIELD_ROUND = "entry.58646232"
FORM_FIELD_TIMESTAMP = "entry.329305254"
LEADERBOARD_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRSQIy2l6sp9rnZT7R_sItMthYztPdJyFsQapV09Up05y-kXE2L8kDPGBMkj3cEJGcrjU6b4srIzr_7/pub?output=csv"

st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# 超強化 CSS - 包含動畫和特效
st.markdown("""
    <style>
    /* 隱藏 Streamlit 元素 */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="manage-app"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    .stActionButton {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    div[class*="viewerBadge"] {display: none !important;}
    
    /* 莫蘭迪色系 */
    .stApp {
        background: linear-gradient(135deg, #f5f0f6 0%, #fef4f0 100%);
        animation: gradientShift 10s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, #f5f0f6 0%, #fef4f0 100%); }
        50% { background: linear-gradient(135deg, #fef4f0 0%, #f5f0f6 100%); }
    }
    
    /* 愛心飄落動畫 */
    @keyframes heartFloat {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    .heart {
        position: fixed;
        font-size: 20px;
        animation: heartFloat 8s linear infinite;
        pointer-events: none;
        z-index: 999;
    }
    
    /* 按鈕增強 */
    .stButton>button {
        width: 100%; 
        border-radius: 25px; 
        height: 3.8em;
        font-weight: bold; 
        font-size: 18px;
        border: 3px solid #E8B4B8;
        background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%);
        color: #6B5B6E;
        box-shadow: 0 6px 15px rgba(232, 180, 184, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 12px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(232, 180, 184, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover:before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(232, 180, 184, 0.5);
        border-color: #C4B5CF;
    }
    
    .stButton>button:active { 
        transform: scale(0.95); 
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
        color: white;
        border: none;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 6px 15px rgba(232, 180, 184, 0.3); }
        50% { box-shadow: 0 8px 25px rgba(232, 180, 184, 0.6); }
    }
    
    /* 題目卡片 */
    .big-font { 
        font-size: 24px !important; 
        font-weight: bold; 
        color: #6B5B6E; 
        margin-bottom: 25px; 
        line-height: 1.6;
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #ffffff 0%, #f9f5f9 100%);
        border-radius: 20px;
        border-left: 5px solid #E8B4B8;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Combo 顯示 */
    .combo-display {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 4em;
        font-weight: bold;
        color: #E8B4B8;
        text-shadow: 0 0 20px rgba(232, 180, 184, 0.8);
        animation: comboAnim 1s ease-out;
        pointer-events: none;
        z-index: 9999;
    }
    
    @keyframes comboAnim {
        0% { transform: translate(-50%, -50%) scale(0); opacity: 0; }
        50% { transform: translate(-50%, -50%) scale(1.5); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(1); opacity: 0; }
    }
    
    /* 答對/答錯動畫 */
    .correct-flash {
        animation: correctPulse 0.6s ease-out;
    }
    
    @keyframes correctPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(184, 197, 176, 0); }
        50% { box-shadow: 0 0 30px 10px rgba(184, 197, 176, 0.8); }
    }
    
    .wrong-shake {
        animation: shake 0.5s ease-out;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* 統計卡片 */
    .stat-box {
        display: inline-block; 
        padding: 18px 25px; 
        margin: 8px;
        background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%);
        border-radius: 20px;
        border: 3px solid #E8B4B8;
        color: #6B5B6E;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(232, 180, 184, 0.3);
        transition: transform 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
    }
    
    /* 等級徽章 */
    .badge {
        display: inline-block;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 1.5em;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        animation: badgeAppear 1s ease-out;
    }
    
    @keyframes badgeAppear {
        from { transform: scale(0) rotate(-180deg); opacity: 0; }
        to { transform: scale(1) rotate(0); opacity: 1; }
    }
    
    .badge-gold {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .badge-silver {
        background: linear-gradient(135deg, #C0C0C0 0%, #A8A8A8 100%);
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .badge-bronze {
        background: linear-gradient(135deg, #CD7F32 0%, #B8733C 100%);
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .badge-normal {
        background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
        color: white;
    }
    
    /* 排行榜優化 */
    .leaderboard-item {
        padding: 15px 20px;
        margin: 10px 0;
        background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%);
        border-radius: 15px;
        border-left: 5px solid #E8B4B8;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 3px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .leaderboard-item:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    
    .leaderboard-gold { 
        border-left: 8px solid #FFD700 !important;
        background: linear-gradient(135deg, #FFF9E5 0%, #fef9f9 100%) !important;
    }
    
    .leaderboard-silver { 
        border-left: 8px solid #C0C0C0 !important;
        background: linear-gradient(135deg, #F5F5F5 0%, #fef9f9 100%) !important;
    }
    
    .leaderboard-bronze { 
        border-left: 8px solid #CD7F32 !important;
        background: linear-gradient(135deg, #FFF0E5 0%, #fef9f9 100%) !important;
    }
    
    /* 進度條愛心 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #E8B4B8 0%, #C4B5CF 50%, #A6B8C7 100%);
        height: 15px;
        border-radius: 10px;
    }
    
    /* 載入動畫 */
    .loading-heart {
        text-align: center;
        font-size: 3em;
        animation: heartBeat 1s ease-in-out infinite;
    }
    
    @keyframes heartBeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    
    /* 分享卡片 */
    .share-card {
        padding: 30px;
        background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* 首頁標題特效 */
    .title-glow {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        background: linear-gradient(45deg, #D4838A, #A88BA8, #7A9AB0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleShine 3s ease-in-out infinite;
        text-shadow: 0 2px 10px rgba(212, 131, 138, 0.3);
    }
    
    @keyframes titleShine {
        0%, 100% { filter: brightness(1.2); }
        50% { filter: brightness(1.5); }
    }
    
    /* 副標題顏色加深 */
    h2, h3, .stMarkdown h2, .stMarkdown h3 {
        color: #6B5B6E !important;
    }
    
    /* 確保副標題可見 */
    [data-testid="stHeader"] + div h2 {
        color: #8B6B8E !important;
        font-weight: bold;
    }
    
    /* 訊息提示優化 */
    .stSuccess, .stError, .stInfo {
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* 指標卡片 */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        color: #6B5B6E;
        font-weight: bold;
    }
    
    /* Combo 計數器 */
    .combo-counter {
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 15px 25px;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: white;
        font-size: 1.5em;
        font-weight: bold;
        border-radius: 50px;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.5);
        animation: bounce 0.5s ease-out;
        z-index: 1000;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
    """, unsafe_allow_html=True)

# 讀取題目資料
@st.cache_data(ttl=60)
def load_data():
    fallback = []
    if "YOUR_CSV_LINK" in CSV_URL or CSV_URL == "": 
        return fallback
    try:
        df = pd.read_csv(CSV_URL)
        cols = {col.lower().strip(): col for col in df.columns}
        question_col = answer_col = None
        option_cols = []
        for key, col in cols.items():
            if 'question' in key or '題目' in key: question_col = col
            elif 'answer' in key or '答案' in key: answer_col = col
            elif 'option' in key or '選項' in key: option_cols.append(col)
        if not question_col or not answer_col or len(option_cols) < 4: return fallback
        option_cols = sorted(option_cols)[:4]
        data = []
        for _, row in df.iterrows():
            try:
                item = {"q": str(row[question_col]), "options": [str(row[col]) for col in option_cols], "ans": int(row[answer_col])}
                data.append(item)
            except: continue
        return data
    except: return fallback

# 讀取排行榜（快取時間縮短為 10 秒）
@st.cache_data(ttl=10)
def load_leaderboard():
    if not LEADERBOARD_URL or LEADERBOARD_URL == "": return []
    try:
        df = pd.read_csv(LEADERBOARD_URL)
        cols = {col.lower().strip(): col for col in df.columns}
        score_col = nickname_col = accuracy_col = None
        for key, col in cols.items():
            if 'score' in key or '分數' in key: score_col = col
            elif 'nickname' in key or '暱稱' in key or 'name' in key: nickname_col = col
            elif 'accuracy' in key or '答對率' in key or '正確率' in key: accuracy_col = col
        if not score_col or not nickname_col: return []
        leaderboard = []
        for _, row in df.iterrows():
            try:
                record = {'Nickname': str(row[nickname_col]), 'Score': int(row[score_col]), 'Accuracy': int(row[accuracy_col]) if accuracy_col else 0}
                leaderboard.append(record)
            except: continue
        leaderboard.sort(key=lambda x: x['Score'], reverse=True)
        return leaderboard[:50]
    except: return []

# 產生 Google Form 預填網址
def generate_form_url(nickname, score, accuracy, round_num):
    if not GOOGLE_FORM_URL or not all([FORM_FIELD_NICKNAME, FORM_FIELD_SCORE, FORM_FIELD_ACCURACY]): return None
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    params = {FORM_FIELD_NICKNAME: nickname, FORM_FIELD_SCORE: str(score), FORM_FIELD_ACCURACY: str(int(accuracy)), FORM_FIELD_ROUND: str(round_num), FORM_FIELD_TIMESTAMP: timestamp}
    params = {k: v for k, v in params.items() if k}
    query_string = urllib.parse.urlencode(params)
    return f"{GOOGLE_FORM_URL}?{query_string}"

# 取得等級徽章
def get_badge(accuracy):
    if accuracy == 100: return ("🏆 完美達人", "badge-gold")
    elif accuracy >= 90: return ("🥇 金牌高手", "badge-gold")
    elif accuracy >= 80: return ("🥈 銀牌好友", "badge-silver")
    elif accuracy >= 70: return ("🥉 銅牌賓客", "badge-bronze")
    else: return ("🎯 熱情參與", "badge-normal")

# 初始化
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'correct_count' not in st.session_state: st.session_state.correct_count = 0
if 'questions' not in st.session_state: st.session_state.questions = []
if 'lifelines' not in st.session_state: st.session_state.lifelines = 3
if 'disabled_opts' not in st.session_state: st.session_state.disabled_opts = []
if 'answer_start_time' not in st.session_state: st.session_state.answer_start_time = None
if 'used_questions' not in st.session_state: st.session_state.used_questions = []
if 'round_num' not in st.session_state: st.session_state.round_num = 1
if 'paused' not in st.session_state: st.session_state.paused = False
if 'auto_next' not in st.session_state: st.session_state.auto_next = False
if 'score_uploaded' not in st.session_state: st.session_state.score_uploaded = False
if 'combo' not in st.session_state: st.session_state.combo = 0
if 'max_combo' not in st.session_state: st.session_state.max_combo = 0
if 'show_combo' not in st.session_state: st.session_state.show_combo = False

def shuffle_options(question):
    correct_idx = question['ans'] - 1
    options = question['options'][:]
    correct_answer = options[correct_idx]
    random.shuffle(options)
    new_correct_idx = options.index(correct_answer)
    return {'q': question['q'], 'options': options, 'ans': new_correct_idx + 1}

def start_game(round_num=1):
    all_q = load_data()
    if not all_q: 
        st.error("讀取不到題目，請檢查 Google Sheet 連結")
        return
    available_q = [q for q in all_q if q['q'] not in st.session_state.used_questions]
    if len(available_q) < 20:
        st.error("剩餘題目不足20題！")
        return
    random.shuffle(available_q)
    selected_q = available_q[:20]
    shuffled_q = [shuffle_options(q) for q in selected_q]
    st.session_state.used_questions.extend([q['q'] for q in selected_q])
    st.session_state.questions = shuffled_q
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.lifelines = 3
    st.session_state.disabled_opts = []
    st.session_state.answer_start_time = time.time()
    st.session_state.round_num = round_num
    st.session_state.paused = False
    st.session_state.auto_next = False
    st.session_state.score_uploaded = False
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.show_combo = False
    st.session_state.page = 'game'

def check(u_idx, ans_idx):
    time_taken = time.time() - st.session_state.answer_start_time
    base_score = 100
    speed_bonus = 0
    if time_taken < 10:
        speed_bonus = int((10 - time_taken) * 5)
    lifeline_penalty = (3 - st.session_state.lifelines) * 15
    
    if u_idx == (ans_idx - 1):
        # 答對：增加 Combo
        st.session_state.combo += 1
        if st.session_state.combo > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo
        
        # Combo 獎勵
        combo_bonus = 0
        if st.session_state.combo >= 5:
            combo_bonus = 100
            st.session_state.show_combo = True
        elif st.session_state.combo >= 3:
            combo_bonus = 50
            st.session_state.show_combo = True
        
        final_score = max(base_score + speed_bonus + combo_bonus - lifeline_penalty, 50)
        st.session_state.score += final_score
        st.session_state.correct_count += 1
        
        if combo_bonus > 0:
            st.toast(f"🔥 {st.session_state.combo} COMBO! +{final_score}分", icon="🎉")
        else:
            st.toast(f"🎉 答對了！+{final_score}分", icon="✅")
    else:
        # 答錯：重置 Combo
        st.session_state.combo = 0
        st.session_state.show_combo = False
        st.toast("❌ 答錯了！Combo 中斷", icon="❌")
    
    st.session_state.auto_next = True
    time.sleep(1.2)
    
    if (st.session_state.current_q + 1) % 5 == 0 and st.session_state.current_q + 1 < 20:
        st.session_state.paused = True
        st.rerun()
    else:
        next_question()

def next_question():
    if st.session_state.current_q < len(st.session_state.questions) - 1:
        st.session_state.current_q += 1
        st.session_state.disabled_opts = []
        st.session_state.answer_start_time = time.time()
        st.session_state.auto_next = False
        st.session_state.show_combo = False
        st.rerun()
    else:
        st.session_state.page = 'result'
        st.rerun()

def resume_game():
    st.session_state.paused = False
    st.session_state.auto_next = False
    next_question()

def lifeline(ans_val):
    if st.session_state.lifelines > 0:
        st.session_state.lifelines -= 1
        ans_idx = ans_val - 1
        wrong = [i for i in range(4) if i != ans_idx]
        st.session_state.disabled_opts = random.sample(wrong, 2)
        st.toast("💡 已刪除兩個錯誤選項！", icon="🆘")
        st.rerun()

# 介面
if st.session_state.page == 'home':
    # 愛心飄落效果
    st.markdown("""
    <div class='heart' style='left: 10%; animation-delay: 0s;'>💖</div>
    <div class='heart' style='left: 30%; animation-delay: 2s;'>💕</div>
    <div class='heart' style='left: 50%; animation-delay: 4s;'>💗</div>
    <div class='heart' style='left: 70%; animation-delay: 1s;'>💖</div>
    <div class='heart' style='left: 90%; animation-delay: 3s;'>💕</div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='title-glow'>💖 敬民 & 紫淇</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #6B5B6E; font-weight: bold; margin-top: -10px;'>🎊 Wedding Quiz 婚禮問答</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🏆 排行榜", use_container_width=True):
            st.session_state.page = 'leaderboard'
            st.rerun()
    
    st.markdown("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%); 
         border-radius: 25px; margin: 20px 0; border: 3px solid #E8B4B8; box-shadow: 0 8px 20px rgba(0,0,0,0.1);'>
        <h3 style='color: #6B5B6E; margin-bottom: 20px;'>🎮 遊戲規則</h3>
        <p style='color: #8B7B8E; font-size: 17px; line-height: 2;'>
            📝 每回合隨機抽取 <strong>20題</strong><br>
            ✨ 答對得分，速度越快加分越多<br>
            🔥 <strong>連續答對有 Combo 獎勵</strong><br>
            🆘 提供 <strong>3次</strong> 求救機會<br>
            ⏸️ 每 <strong>5題</strong> 可選擇暫停休息<br>
            🏆 遊戲結束可上傳成績到排行榜
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    data = load_data()
    if data:
        available = len(data) - len(st.session_state.used_questions)
        st.info(f"📊 題庫共有 {len(data)} 題 | 剩餘可用 {available} 題")
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    if st.button("🎯 開始挑戰", type="primary", use_container_width=True): 
        start_game(1)
        st.rerun()

elif st.session_state.page == 'leaderboard':
    st.title("🏆 排行榜")
    st.subheader("TOP 50 最強婚禮達人")
    
    # 重新整理按鈕
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 重新整理", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    if not LEADERBOARD_URL or LEADERBOARD_URL == "":
        st.warning("⚠️ 尚未設定排行榜！")
    else:
        leaderboard = load_leaderboard()
        if leaderboard:
            st.markdown(f"<p style='text-align: center; color: #8B7B8E;'>🎊 目前共有 {len(leaderboard)} 位挑戰者 | ⏰ 資料每 10 秒自動更新</p>", unsafe_allow_html=True)
            for idx, record in enumerate(leaderboard, 1):
                rank_emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
                rank_class = "leaderboard-gold" if idx == 1 else "leaderboard-silver" if idx == 2 else "leaderboard-bronze" if idx == 3 else ""
                nickname = record.get('Nickname', '匿名')
                score = record.get('Score', 0)
                accuracy = record.get('Accuracy', 0)
                st.markdown(f"""
                <div class='leaderboard-item {rank_class}'>
                    <div>
                        <span style='font-size: 28px; margin-right: 15px;'>{rank_emoji}</span>
                        <strong style='font-size: 20px;'>{nickname}</strong>
                    </div>
                    <div style='text-align: right;'>
                        <div style='font-size: 24px; font-weight: bold; color: #E8B4B8;'>{score} 分</div>
                        <div style='font-size: 15px; color: #999;'>{accuracy}% 正確率</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("🎯 目前還沒有人上傳成績，快來當第一名吧！")
    
    st.write("---")
    if st.button("🏠 回首頁", type="primary", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'game':
    if st.session_state.paused:
        st.markdown(f"""
        <div style='padding: 30px; background: linear-gradient(135deg, #C4B5CF 0%, #A6B8C7 100%);
             border-radius: 25px; text-align: center; margin: 20px 0; color: white;
             box-shadow: 0 10px 25px rgba(196, 181, 207, 0.5);'>
            <h2 style='color: white; margin: 0; font-size: 2em;'>⏸️ 休息時間</h2>
            <p style='font-size: 20px; margin-top: 15px;'>已完成 {st.session_state.current_q + 1} 題，還剩 {20 - st.session_state.current_q - 1} 題</p>
            <p style='font-size: 18px; opacity: 0.95;'>目前分數：{st.session_state.score} 分</p>
            <p style='font-size: 16px; opacity: 0.9;'>🔥 最高 Combo：{st.session_state.max_combo}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ 繼續答題", type="primary", use_container_width=True):
                resume_game()
        with col2:
            if st.button("🏠 結束挑戰", use_container_width=True):
                st.session_state.page = 'result'
                st.rerun()
    else:
        q = st.session_state.questions[st.session_state.current_q]
        total = len(st.session_state.questions)
        
        # Combo 顯示
        if st.session_state.combo >= 3:
            st.markdown(f"""
            <div class='combo-counter'>
                🔥 {st.session_state.combo} COMBO!
            </div>
            """, unsafe_allow_html=True)
        
        st.progress((st.session_state.current_q + 1) / total)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 分數", st.session_state.score)
        with col2:
            st.metric("📝 題數", f"{st.session_state.current_q + 1}/{total}")
        with col3:
            st.metric("🆘 求救", st.session_state.lifelines)
        with col4:
            st.metric("🔥 Combo", st.session_state.combo)
        
        st.write("---")
        st.markdown(f"<div class='big-font'>Q{st.session_state.current_q + 1}. {q['q']}</div>", unsafe_allow_html=True)
        
        if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
            if st.button(f"🆘 求救 (剩餘 {st.session_state.lifelines} 次)", use_container_width=True): 
                lifeline(q['ans'])
        
        for i, opt in enumerate(q['options']):
            disabled = i in st.session_state.disabled_opts
            if st.button(opt, key=f"opt_{st.session_state.current_q}_{i}", disabled=disabled, use_container_width=True): 
                check(i, q['ans'])

elif st.session_state.page == 'result':
    total_q = 20
    acc = (st.session_state.correct_count / total_q) * 100
    wrong_count = total_q - st.session_state.correct_count
    badge_text, badge_class = get_badge(acc)
    
    st.title(f"🎉 第 {st.session_state.round_num} 回合結束")
    
    # 等級徽章
    st.markdown(f"""
    <div style='text-align: center;'>
        <div class='badge {badge_class}'>{badge_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 答對率圓圈
    st.markdown(f"""
    <div style='width: 220px; height: 220px; border-radius: 50%;
         background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
         display: flex; flex-direction: column; justify-content: center; align-items: center;
         margin: 30px auto; border: 8px solid white;
         box-shadow: 0 15px 40px rgba(196, 181, 207, 0.6);'>
        <div style='font-size: 4em; font-weight: bold; color: white;'>{int(acc)}%</div>
        <div style='font-size: 1.2em; color: white; opacity: 0.95;'>答對率</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stat-box'><div style='font-size: 28px;'>{st.session_state.correct_count}</div><div style='font-size: 14px; margin-top: 5px;'>✅ 答對</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box'><div style='font-size: 28px;'>{wrong_count}</div><div style='font-size: 14px; margin-top: 5px;'>❌ 答錯</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-box'><div style='font-size: 28px;'>{st.session_state.score}</div><div style='font-size: 14px; margin-top: 5px;'>💰 總分</div></div>", unsafe_allow_html=True)
    
    # Combo 統計
    if st.session_state.max_combo > 0:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
             border-radius: 20px; margin: 20px 0; color: white; box-shadow: 0 5px 15px rgba(255, 215, 0, 0.4);'>
            <p style='font-size: 1.5em; margin: 0; font-weight: bold;'>🔥 最高 Combo: {st.session_state.max_combo} 連擊！</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # 評價
    if acc == 100:
        st.markdown("### 🏆 完美滿分！你們倆真的是天生一對！")
        st.balloons()
    elif acc >= 90:
        st.markdown("### 🌟 超級鐵粉！對新人瞭若指掌！")
    elif acc >= 80:
        st.markdown("### 💖 太棒了！對新人非常了解呢！")
    elif acc >= 70:
        st.markdown("### 👍 不錯喔！是新人的好朋友！")
    elif acc >= 60:
        st.markdown("### 😊 還不錯！繼續加油！")
    elif acc >= 50:
        st.markdown("### 💪 再接再厲！多多關注新人動態～")
    else:
        st.markdown("### 🎯 加油！下次一定更好！")
    
    # 排名統計
    leaderboard = load_leaderboard()
    if leaderboard:
        better_than = sum(1 for r in leaderboard if st.session_state.score > r['Score'])
        total_players = len(leaderboard)
        if total_players > 0:
            percentage = int((better_than / total_players) * 100)
            st.info(f"📊 你打敗了 {percentage}% 的賓客！（{better_than}/{total_players}）")
    
    st.write("---")
    
    # 分享卡片
    st.markdown(f"""
    <div class='share-card'>
        <h3 style='margin: 0 0 15px 0;'>📸 分享我的成績</h3>
        <p style='font-size: 1.2em; margin: 10px 0;'>我在「敬民 & 紫淇婚禮問答」獲得了</p>
        <p style='font-size: 2em; font-weight: bold; margin: 10px 0;'>{st.session_state.score} 分</p>
        <p style='font-size: 1.1em; margin: 10px 0;'>答對率 {int(acc)}% | {badge_text}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 上傳成績
    if not st.session_state.score_uploaded:
        form_configured = all([GOOGLE_FORM_URL, FORM_FIELD_NICKNAME, FORM_FIELD_SCORE, FORM_FIELD_ACCURACY])
        
        if form_configured:
            st.markdown("""
            <div style='padding: 25px; background: linear-gradient(135deg, #E5D4A6 0%, #f5ead0 100%);
                 border-radius: 20px; border: 3px solid #d4b47e; margin: 20px 0; text-align: center;'>
                <h3 style='color: #6B5B6E; margin: 0 0 10px 0;'>🏆 上傳成績到排行榜</h3>
                <p style='color: #8B7B8E; margin: 0;'>輸入暱稱，自動開啟 Google Form 提交成績！</p>
            </div>
            """, unsafe_allow_html=True)
            
            nickname = st.text_input("請輸入暱稱（2-10個字）", max_chars=10, placeholder="例如：婚禮達人", key="nickname_input")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚀 上傳成績", type="primary", use_container_width=True, disabled=len(nickname.strip()) < 2):
                    if len(nickname.strip()) >= 2:
                        form_url = generate_form_url(nickname, st.session_state.score, acc, st.session_state.round_num)
                        if form_url:
                            st.session_state.score_uploaded = True
                            st.success(f"✅ 已為 {nickname} 準備好成績！")
                            st.markdown(f"""
                            <div style='text-align: center; padding: 25px; background: #B8C5B0; border-radius: 20px; margin: 20px 0;'>
                                <p style='color: white; font-size: 18px; margin-bottom: 20px; font-weight: bold;'>
                                    ⚠️ 重要：請點擊下方按鈕開啟 Google Form
                                </p>
                                <a href="{form_url}" target="_blank" style='
                                    display: inline-block; padding: 18px 40px;
                                    background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
                                    color: white; text-decoration: none; border-radius: 30px;
                                    font-weight: bold; font-size: 20px;
                                    box-shadow: 0 6px 15px rgba(0,0,0,0.3);'>
                                    📝 開啟 Google Form 提交
                                </a>
                                <p style='color: white; font-size: 16px; margin-top: 20px;'>
                                    👆 開啟後請確認資料並點擊「<strong>提交</strong>」按鈕
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.warning("💡 提醒：必須在 Google Form 中點擊「提交」按鈕，成績才會進入排行榜！")
                            st.info("⏰ 提交後約 10 秒，排行榜就會更新顯示你的成績")
                            st.balloons()
            with col2:
                if st.button("❌ 不上傳", use_container_width=True):
                    st.session_state.score_uploaded = True
                    st.info("好的，已跳過上傳")
                    time.sleep(0.8)
                    st.rerun()
        else:
            if st.button("⏭️ 跳過上傳", use_container_width=True):
                st.session_state.score_uploaded = True
                st.rerun()
    else:
        if all([GOOGLE_FORM_URL, FORM_FIELD_NICKNAME, FORM_FIELD_SCORE]):
            st.success("✅ 成績已準備完成！")
            st.info("💡 記得要在 Google Form 中點擊「提交」按鈕，成績才會進入排行榜哦～")
        else:
            st.success("✅ 已跳過上傳")
    
    st.write("---")
    
    # 繼續挑戰
    all_q = load_data()
    available = len(all_q) - len(st.session_state.used_questions)
    
    if available >= 20:
        st.success(f"🎊 還有 {available} 題可以挑戰！")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🎯 挑戰下一回合", type="primary", use_container_width=True):
                start_game(st.session_state.round_num + 1)
                st.rerun()
        with col2:
            if st.button("🏆 查看排行榜", use_container_width=True):
                st.session_state.page = 'leaderboard'
                st.rerun()
        with col3:
            if st.button("🏠 回首頁", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
    else:
        st.info(f"剩餘題目不足20題（剩餘 {available} 題）")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 查看排行榜", type="primary", use_container_width=True):
                st.session_state.page = 'leaderboard'
                st.rerun()
        with col2:
            if st.button("🏠 回首頁", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
