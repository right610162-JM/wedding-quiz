import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import urllib.parse

# — 設定區 —

# 題目資料庫

CSV_URL = “https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv”

# 👇👇👇 排行榜設定 👇👇👇

# ⚠️ 重要：FORM_FIELD_XXX 的 entry ID 需要從「取得預填連結」中取得真實數值

# 步驟：在 Google Form 點擊「⋮」→「取得預填連結」→ 填入測試資料 → 複製連結 → 分析 entry.XXXXXXX

GOOGLE_FORM_URL = “https://docs.google.com/forms/d/e/1FAIpQLSd0SOigmWPwEEP_zQv-LlPyCa99a-SQhqa0PP9kIvyJOaQbLw/formResponse”

# ✅ 已從預填連結中取得真實 entry ID

FORM_FIELD_NICKNAME = “entry.276737520”   # 暱稱
FORM_FIELD_SCORE = “entry.1217367258”     # 分數
FORM_FIELD_ACCURACY = “entry.1332601410”  # 答對率
FORM_FIELD_ROUND = “entry.58646232”       # 回合數
FORM_FIELD_TIMESTAMP = “entry.329305254”  # 時間戳記

# 排行榜 CSV 連結（從 Google Form 的回應試算表發布）

LEADERBOARD_URL = “https://docs.google.com/spreadsheets/d/e/2PACX-1vRSQIy2l6sp9rnZT7R_sItMthYztPdJyFsQapV09Up05y-kXE2L8kDPGBMkj3cEJGcrjU6b4srIzr_7/pub?output=csv”

st.set_page_config(page_title=“敬民 & 紫淇 Wedding Quiz”, page_icon=“💍”, layout=“centered”)

# 莫蘭迪色系 CSS

st.markdown(”””
<style>
/* 隱藏 Streamlit 預設元素 */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}
[data-testid=“stToolbar”] {display: none;}
[data-testid=“manage-app”] {display: none;}
.css-1dp5vir {display: none;}

```
:root {
    --morandi-pink: #E8B4B8;
    --morandi-blue: #A6B8C7;
    --morandi-green: #B8C5B0;
    --morandi-yellow: #E5D4A6;
    --morandi-purple: #C4B5CF;
    --morandi-coral: #E8C5B5;
}

.stApp {
    background: linear-gradient(135deg, #f5f0f6 0%, #fef4f0 100%);
}

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
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(232, 180, 184, 0.4);
    border-color: #C4B5CF;
}

.stButton>button:active { 
    transform: scale(0.97); 
}

.stButton>button[kind="primary"] {
    background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
    color: white;
    border: none;
}

.stButton>button:disabled {
    background: #e9e9e9;
    border-color: #d0d0d0;
    color: #999;
    opacity: 0.6;
}

.big-font { 
    font-size: 24px !important; 
    font-weight: bold; 
    color: #6B5B6E; 
    margin-bottom: 25px; 
    line-height: 1.6;
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #ffffff 0%, #f9f5f9 100%);
    border-radius: 20px;
    border-left: 5px solid #E8B4B8;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.score-board { 
    padding: 35px; 
    background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 50%, #A6B8C7 100%);
    border-radius: 25px; 
    text-align: center; 
    margin-bottom: 25px; 
    color: white;
    box-shadow: 0 12px 30px rgba(196, 181, 207, 0.4);
    border: 4px solid white;
}

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
}

.accuracy-circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 30px auto;
    border: 6px solid white;
    box-shadow: 0 15px 35px rgba(196, 181, 207, 0.5);
}

[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #6B5B6E;
    font-weight: bold;
}

[data-testid="stMetricLabel"] {
    color: #8B7B8E !important;
    font-weight: 600;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #E8B4B8 0%, #C4B5CF 50%, #A6B8C7 100%);
}

.stSuccess {
    background: linear-gradient(135deg, #B8C5B0 0%, #d4e0cc 100%);
    border-left: 5px solid #8faa7f;
    border-radius: 10px;
}

.stError {
    background: linear-gradient(135deg, #E8B4B8 0%, #f5d4d8 100%);
    border-left: 5px solid #d88a90;
    border-radius: 10px;
}

.stInfo {
    background: linear-gradient(135deg, #A6B8C7 0%, #d0dce5 100%);
    border-left: 5px solid #7a9ab0;
    border-radius: 10px;
}

h1 {
    color: #6B5B6E !important;
    text-align: center;
}

h3 {
    color: #8B7B8E !important;
}

hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #E8B4B8 50%, transparent 100%);
    margin: 30px 0;
}

.pause-banner {
    padding: 25px;
    background: linear-gradient(135deg, #C4B5CF 0%, #A6B8C7 100%);
    border-radius: 20px;
    text-align: center;
    margin: 20px 0;
    color: white;
    box-shadow: 0 8px 20px rgba(196, 181, 207, 0.4);
}

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
}

.leaderboard-rank {
    font-size: 24px;
    font-weight: bold;
    color: #C4B5CF;
    min-width: 50px;
}

.leaderboard-gold { border-left-color: #FFD700 !important; }
.leaderboard-silver { border-left-color: #C0C0C0 !important; }
.leaderboard-bronze { border-left-color: #CD7F32 !important; }

.upload-box {
    padding: 25px;
    background: linear-gradient(135deg, #E5D4A6 0%, #f5ead0 100%);
    border-radius: 20px;
    border: 3px solid #d4b47e;
    margin: 20px 0;
    text-align: center;
}

.setup-guide {
    padding: 20px;
    background: linear-gradient(135deg, #A6B8C7 0%, #d0dce5 100%);
    border-radius: 15px;
    margin: 15px 0;
    border-left: 5px solid #7a9ab0;
}
</style>
""", unsafe_allow_html=True)
```

# 讀取題目資料

@st.cache_data(ttl=60)
def load_data():
fallback = []
if “YOUR_CSV_LINK” in CSV_URL or CSV_URL == “”:
return fallback

```
try:
    df = pd.read_csv(CSV_URL)
    cols = {col.lower().strip(): col for col in df.columns}
    
    question_col = None
    answer_col = None
    option_cols = []
    
    for key, col in cols.items():
        if 'question' in key or '題目' in key:
            question_col = col
        elif 'answer' in key or '答案' in key:
            answer_col = col
        elif 'option' in key or '選項' in key:
            option_cols.append(col)
    
    if not question_col or not answer_col or len(option_cols) < 4:
        st.error(f"欄位偵測失敗！請確認 CSV 包含：題目、選項1-4、答案欄位")
        return fallback
    
    option_cols = sorted(option_cols)[:4]
    
    data = []
    for _, row in df.iterrows():
        try:
            item = {
                "q": str(row[question_col]),
                "options": [str(row[col]) for col in option_cols],
                "ans": int(row[answer_col])
            }
            data.append(item)
        except:
            continue
    
    return data
    
except Exception as e:
    st.error(f"讀取資料時發生錯誤: {e}")
    return fallback
```

# 讀取排行榜

@st.cache_data(ttl=30)
def load_leaderboard():
if not LEADERBOARD_URL or LEADERBOARD_URL == “”:
return []

```
try:
    df = pd.read_csv(LEADERBOARD_URL)
    # 自動偵測欄位名稱
    cols = {col.lower().strip(): col for col in df.columns}
    
    score_col = None
    nickname_col = None
    accuracy_col = None
    
    for key, col in cols.items():
        if 'score' in key or '分數' in key:
            score_col = col
        elif 'nickname' in key or '暱稱' in key or 'name' in key:
            nickname_col = col
        elif 'accuracy' in key or '答對率' in key or '正確率' in key:
            accuracy_col = col
    
    if not score_col or not nickname_col:
        return []
    
    # 轉換資料
    leaderboard = []
    for _, row in df.iterrows():
        try:
            record = {
                'Nickname': str(row[nickname_col]),
                'Score': int(row[score_col]),
                'Accuracy': int(row[accuracy_col]) if accuracy_col else 0
            }
            leaderboard.append(record)
        except:
            continue
    
    # 排序
    leaderboard.sort(key=lambda x: x['Score'], reverse=True)
    return leaderboard[:50]
    
except Exception as e:
    st.error(f"讀取排行榜失敗: {e}")
    return []
```

# 產生 Google Form 預填網址

def generate_form_url(nickname, score, accuracy, round_num):
if not GOOGLE_FORM_URL or not all([FORM_FIELD_NICKNAME, FORM_FIELD_SCORE, FORM_FIELD_ACCURACY]):
return None

```
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

params = {
    FORM_FIELD_NICKNAME: nickname,
    FORM_FIELD_SCORE: str(score),
    FORM_FIELD_ACCURACY: str(int(accuracy)),
    FORM_FIELD_ROUND: str(round_num),
    FORM_FIELD_TIMESTAMP: timestamp
}

# 移除空的欄位
params = {k: v for k, v in params.items() if k}

query_string = urllib.parse.urlencode(params)
return f"{GOOGLE_FORM_URL}?{query_string}"
```

# 初始化

if ‘page’ not in st.session_state:
st.session_state.page = ‘home’
if ‘score’ not in st.session_state:
st.session_state.score = 0
if ‘current_q’ not in st.session_state:
st.session_state.current_q = 0
if ‘correct_count’ not in st.session_state:
st.session_state.correct_count = 0
if ‘questions’ not in st.session_state:
st.session_state.questions = []
if ‘lifelines’ not in st.session_state:
st.session_state.lifelines = 3
if ‘disabled_opts’ not in st.session_state:
st.session_state.disabled_opts = []
if ‘answer_start_time’ not in st.session_state:
st.session_state.answer_start_time = None
if ‘used_questions’ not in st.session_state:
st.session_state.used_questions = []
if ‘round_num’ not in st.session_state:
st.session_state.round_num = 1
if ‘paused’ not in st.session_state:
st.session_state.paused = False
if ‘auto_next’ not in st.session_state:
st.session_state.auto_next = False
if ‘score_uploaded’ not in st.session_state:
st.session_state.score_uploaded = False
if ‘show_setup_guide’ not in st.session_state:
st.session_state.show_setup_guide = False

# 打亂選項順序

def shuffle_options(question):
correct_idx = question[‘ans’] - 1
options = question[‘options’][:]
correct_answer = options[correct_idx]
random.shuffle(options)
new_correct_idx = options.index(correct_answer)

```
return {
    'q': question['q'],
    'options': options,
    'ans': new_correct_idx + 1
}
```

# 開始遊戲

def start_game(round_num=1):
all_q = load_data()
if not all_q:
st.error(“讀取不到題目，請檢查 Google Sheet 連結”)
return

```
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
st.session_state.page = 'game'
```

def check(u_idx, ans_idx):
time_taken = time.time() - st.session_state.answer_start_time
base_score = 100
speed_bonus = 0
if time_taken < 10:
speed_bonus = int((10 - time_taken) * 5)

```
lifeline_penalty = (3 - st.session_state.lifelines) * 15

if u_idx == (ans_idx - 1):
    final_score = max(base_score + speed_bonus - lifeline_penalty, 50)
    st.session_state.score += final_score
    st.session_state.correct_count += 1
    st.toast(f"🎉 答對了！+{final_score}分", icon="✅")
else:
    st.toast("❌ 答錯了！", icon="❌")

st.session_state.auto_next = True
time.sleep(1.2)

if (st.session_state.current_q + 1) % 5 == 0 and st.session_state.current_q + 1 < 20:
    st.session_state.paused = True
    st.rerun()
else:
    next_question()
```

def next_question():
if st.session_state.current_q < len(st.session_state.questions) - 1:
st.session_state.current_q += 1
st.session_state.disabled_opts = []
st.session_state.answer_start_time = time.time()
st.session_state.auto_next = False
st.rerun()
else:
st.session_state.page = ‘result’
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
st.toast(“💡 已刪除兩個錯誤選項！”, icon=“🆘”)
st.rerun()

# 介面

if st.session_state.page == ‘home’:
st.title(“💖 敬民 & 紫淇”)
st.subheader(“🎊 Wedding Quiz 婚禮問答”)

```
# 顯示排行榜按鈕
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🏆 排行榜", use_container_width=True):
        st.session_state.page = 'leaderboard'
        st.rerun()

st.markdown("""
<div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%); 
     border-radius: 20px; margin: 20px 0; border: 3px solid #E8B4B8;'>
    <h3 style='color: #6B5B6E; margin-bottom: 15px;'>🎮 遊戲規則</h3>
    <p style='color: #8B7B8E; font-size: 16px; line-height: 1.8;'>
        📝 每回合隨機抽取 <strong>20題</strong><br>
        ✨ 答對得分，速度越快加分越多<br>
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

st.write("---")

if st.button("🎯 開始挑戰", type="primary", use_container_width=True): 
    start_game(1)
    st.rerun()
```

elif st.session_state.page == ‘leaderboard’:
st.title(“🏆 排行榜”)
st.subheader(“TOP 50 最強婚禮達人”)

```
if not LEADERBOARD_URL or LEADERBOARD_URL == "":
    st.warning("⚠️ 尚未設定排行榜！")
    st.info("請點擊首頁的「⚙️ 設定」按鈕查看設定指南")
else:
    leaderboard = load_leaderboard()
    
    if leaderboard:
        for idx, record in enumerate(leaderboard, 1):
            rank_emoji = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
            rank_class = "leaderboard-gold" if idx == 1 else "leaderboard-silver" if idx == 2 else "leaderboard-bronze" if idx == 3 else ""
            
            nickname = record.get('Nickname', '匿名')
            score = record.get('Score', 0)
            accuracy = record.get('Accuracy', 0)
            
            st.markdown(f"""
            <div class='leaderboard-item {rank_class}'>
                <div>
                    <span class='leaderboard-rank'>{rank_emoji}</span>
                    <strong style='font-size: 18px;'>{nickname}</strong>
                </div>
                <div style='text-align: right;'>
                    <div style='font-size: 20px; font-weight: bold; color: #E8B4B8;'>{score} 分</div>
                    <div style='font-size: 14px; color: #999;'>{accuracy}% 正確率</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🎯 目前還沒有人上傳成績，快來當第一名吧！")

st.write("---")
if st.button("🏠 回首頁", type="primary", use_container_width=True):
    st.session_state.page = 'home'
    st.rerun()
```

elif st.session_state.page == ‘game’:
if st.session_state.paused:
st.markdown(f”””
<div class='pause-banner'>
<h2 style='color: white; margin: 0;'>⏸️ 休息時間</h2>
<p style='font-size: 18px; margin-top: 10px;'>已完成 {st.session_state.current_q + 1} 題，還剩 {20 - st.session_state.current_q - 1} 題</p>
<p style='font-size: 16px; opacity: 0.9;'>目前分數：{st.session_state.score} 分</p>
</div>
“””, unsafe_allow_html=True)

```
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

    st.progress((st.session_state.current_q + 1) / total)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 分數", st.session_state.score)
    with col2:
        st.metric("📝 題數", f"{st.session_state.current_q + 1}/{total}")
    with col3:
        st.metric("🆘 求救", st.session_state.lifelines)
    
    st.write("---")
    
    st.markdown(f"<div class='big-font'>Q{st.session_state.current_q + 1}. {q['q']}</div>", unsafe_allow_html=True)

    if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
        if st.button(f"🆘 求救 (剩餘 {st.session_state.lifelines} 次)", use_container_width=True): 
            lifeline(q['ans'])

    for i, opt in enumerate(q['options']):
        disabled = i in st.session_state.disabled_opts
        if st.button(opt, key=f"opt_{st.session_state.current_q}_{i}", disabled=disabled, use_container_width=True): 
            check(i, q['ans'])
```

elif st.session_state.page == ‘result’:
total_q = 20
acc = (st.session_state.correct_count / total_q) * 100
wrong_count = total_q - st.session_state.correct_count

```
st.title(f"🎉 第 {st.session_state.round_num} 回合結束")

st.markdown(f"""
<div class='accuracy-circle'>
    <div style='font-size: 3.5em; font-weight: bold; color: white;'>{int(acc)}%</div>
    <div style='font-size: 1.1em; color: white; opacity: 0.95;'>答對率</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{st.session_state.correct_count}</div><div style='font-size: 14px; margin-top: 5px;'>✅ 答對</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{wrong_count}</div><div style='font-size: 14px; margin-top: 5px;'>❌ 答錯</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{st.session_state.score}</div><div style='font-size: 14px; margin-top: 5px;'>💰 總分</div></div>", unsafe_allow_html=True)

st.write("---")

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

st.write("---")

# 上傳成績區塊
if not st.session_state.score_uploaded:
    form_configured = all([GOOGLE_FORM_URL, FORM_FIELD_NICKNAME, FORM_FIELD_SCORE, FORM_FIELD_ACCURACY])
    
    if form_configured:
        st.markdown("""
        <div class='upload-box'>
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
                        <div style='text-align: center; padding: 20px; background: #B8C5B0; border-radius: 15px; margin: 15px 0;'>
                            <p style='color: white; font-size: 16px; margin-bottom: 15px;'>
                                請點擊下方按鈕開啟 Google Form 並提交成績
                            </p>
                            <a href="{form_url}" target="_blank" style='
                                display: inline-block;
                                padding: 15px 30px;
                                background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
                                color: white;
                                text-decoration: none;
                                border-radius: 25px;
                                font-weight: bold;
                                font-size: 18px;
                                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                            '>
                                📝 開啟 Google Form 提交
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("💡 提示：開啟 Form 後，確認資料無誤後點擊「提交」即可")
                        st.balloons()
        with col2:
            if st.button("❌ 不上傳", use_container_width=True):
                st.session_state.score_uploaded = True
                st.info("好的，已跳過上傳")
                time.sleep(0.8)
                st.rerun()
        
        st.caption("💡 點擊「上傳成績」後會開啟預填好的 Google Form")
    else:
        st.warning("⚠️ 排行榜功能尚未設定")
        st.info("請點擊首頁的「⚙️ 設定」按鈕查看設定指南")
        if st.button("⏭️ 跳過上傳", use_container_width=True):
            st.session_state.score_uploaded = True
            st.rerun()

else:
    if all([GOOGLE_FORM_URL, FORM_FIELD_NICKNAME, FORM_FIELD_SCORE]):
        st.success("✅ 成績已準備完成！別忘了提交 Google Form 哦～")
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
```