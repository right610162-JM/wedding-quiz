# --- 🛠️ 設定區 (已幫你填好 Google 表單資訊) ---

# 1. 題庫 CSV (這是你原本的題目，請確認是否正確)
QUESTIONS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"

# 2. ⚠️ 排行榜 CSV (請注意！這裡還缺一個連結)
# 請去 Google 表單 -> 回覆 -> 建立試算表 -> 檔案 -> 發布到網路 -> 選擇 CSV
LEADERBOARD_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTk1vGJOTJjoZHeXWA_JSnNOz9-AzflgHdaJhEgbgrcV4AxpjCa1x1ZP9oGk2H4ex9sDpoiHBRLfiev/pub?output=csv" 

# 3. Google 表單提交網址 (已幫你修改好，可以直接用)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd0SOigmWPwEEP_zQv-LlPyCa99a-SQhqa0PP9kIvyJOaQbLw/formResponse"

# 4. Google 表單欄位代號 (已幫你解析出來)
ENTRY_NAME = "entry.276737520"   # 對應 testname
ENTRY_SCORE = "entry.1217367258" # 對應 123
st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# 莫蘭迪色系 CSS
st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)


# 讀取資料
@st.cache_data(ttl=60)
def load_data():
    fallback = []
    if "YOUR_CSV_LINK" in CSV_URL or CSV_URL == "": 
        return fallback
    
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


# 初始化
if 'page' not in st.session_state: 
    st.session_state.page = 'home'
if 'score' not in st.session_state: 
    st.session_state.score = 0
if 'current_q' not in st.session_state: 
    st.session_state.current_q = 0
if 'correct_count' not in st.session_state: 
    st.session_state.correct_count = 0
if 'questions' not in st.session_state: 
    st.session_state.questions = []
if 'lifelines' not in st.session_state: 
    st.session_state.lifelines = 3
if 'disabled_opts' not in st.session_state: 
    st.session_state.disabled_opts = []
if 'answer_start_time' not in st.session_state: 
    st.session_state.answer_start_time = None
if 'used_questions' not in st.session_state:
    st.session_state.used_questions = []
if 'round_num' not in st.session_state:
    st.session_state.round_num = 1
if 'paused' not in st.session_state:
    st.session_state.paused = False
if 'auto_next' not in st.session_state:
    st.session_state.auto_next = False


# 打亂選項順序
def shuffle_options(question):
    """打亂選項順序，並記錄正確答案的新位置"""
    correct_idx = question['ans'] - 1
    options = question['options'][:]
    correct_answer = options[correct_idx]
    
    # 打亂選項
    random.shuffle(options)
    
    # 找出正確答案的新位置
    new_correct_idx = options.index(correct_answer)
    
    return {
        'q': question['q'],
        'options': options,
        'ans': new_correct_idx + 1
    }


# 開始遊戲
def start_game(round_num=1):
    all_q = load_data()
    if not all_q: 
        st.error("讀取不到題目，請檢查 Google Sheet 連結")
        return
    
    # 過濾掉已使用過的題目
    available_q = [q for q in all_q if q['q'] not in st.session_state.used_questions]
    
    if len(available_q) < 20:
        st.error("剩餘題目不足20題！")
        return
    
    # 隨機選20題
    random.shuffle(available_q)
    selected_q = available_q[:20]
    
    # 打亂每題的選項順序
    shuffled_q = [shuffle_options(q) for q in selected_q]
    
    # 記錄已使用的題目
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
    st.session_state.page = 'game'


def check(u_idx, ans_idx):
    time_taken = time.time() - st.session_state.answer_start_time
    base_score = 100
    speed_bonus = 0
    if time_taken < 10:
        speed_bonus = int((10 - time_taken) * 5)
    
    lifeline_penalty = (3 - st.session_state.lifelines) * 15
    
    if u_idx == (ans_idx - 1):
        final_score = max(base_score + speed_bonus - lifeline_penalty, 50)
        st.session_state.score += final_score
        st.session_state.correct_count += 1
        st.toast(f"🎉 答對了！+{final_score}分", icon="✅")
    else:
        st.toast("❌ 答錯了！", icon="❌")
    
    # 設定自動進入下一題
    st.session_state.auto_next = True
    time.sleep(1.2)
    
    # 檢查是否每5題暫停
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
    st.title("💖 敬民 & 紫淇")
    st.subheader("🎊 Wedding Quiz 婚禮問答")
    
    st.markdown("""
    <div style='text-align: center; padding: 25px; background: linear-gradient(135deg, #ffffff 0%, #fef9f9 100%); 
         border-radius: 20px; margin: 20px 0; border: 3px solid #E8B4B8;'>
        <h3 style='color: #6B5B6E; margin-bottom: 15px;'>🎮 遊戲規則</h3>
        <p style='color: #8B7B8E; font-size: 16px; line-height: 1.8;'>
            📝 每回合隨機抽取 <strong>20題</strong><br>
            ✨ 答對得分，速度越快加分越多<br>
            🆘 提供 <strong>3次</strong> 求救機會<br>
            ⏸️ 每 <strong>5題</strong> 可選擇暫停休息<br>
            🎯 答完可挑戰下一回合（題目不重複）
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

elif st.session_state.page == 'game':
    # 檢查是否暫停
    if st.session_state.paused:
        st.markdown(f"""
        <div class='pause-banner'>
            <h2 style='color: white; margin: 0;'>⏸️ 休息時間</h2>
            <p style='font-size: 18px; margin-top: 10px;'>已完成 {st.session_state.current_q + 1} 題，還剩 {20 - st.session_state.current_q - 1} 題</p>
            <p style='font-size: 16px; opacity: 0.9;'>目前分數：{st.session_state.score} 分</p>
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

        # 進度條
        st.progress((st.session_state.current_q + 1) / total)
        
        # 統計資訊
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 分數", st.session_state.score)
        with col2:
            st.metric("📝 題數", f"{st.session_state.current_q + 1}/{total}")
        with col3:
            st.metric("🆘 求救", st.session_state.lifelines)
        
        st.write("---")
        
        # 題目
        st.markdown(f"<div class='big-font'>Q{st.session_state.current_q + 1}. {q['q']}</div>", unsafe_allow_html=True)

        # 求救按鈕
        if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
            if st.button(f"🆘 求救 (剩餘 {st.session_state.lifelines} 次)", use_container_width=True): 
                lifeline(q['ans'])

        # 選項
        for i, opt in enumerate(q['options']):
            disabled = i in st.session_state.disabled_opts
            if st.button(opt, key=f"opt_{st.session_state.current_q}_{i}", disabled=disabled, use_container_width=True): 
                check(i, q['ans'])

elif st.session_state.page == 'result':
    total_q = 20
    acc = (st.session_state.correct_count / total_q) * 100
    wrong_count = total_q - st.session_state.correct_count

    st.title(f"🎉 第 {st.session_state.round_num} 回合結束")
    
    # 答對率大圓圈
    st.markdown(f"""
    <div class='accuracy-circle'>
        <div style='font-size: 3.5em; font-weight: bold; color: white;'>{int(acc)}%</div>
        <div style='font-size: 1.1em; color: white; opacity: 0.95;'>答對率</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 詳細統計
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{st.session_state.correct_count}</div><div style='font-size: 14px; margin-top: 5px;'>✅ 答對</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{wrong_count}</div><div style='font-size: 14px; margin-top: 5px;'>❌ 答錯</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-box'><div style='font-size: 24px;'>{st.session_state.score}</div><div style='font-size: 14px; margin-top: 5px;'>💰 總分</div></div>", unsafe_allow_html=True)
    
    # 評價（根據答對率）
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
    
    # 檢查是否還有足夠題目
    all_q = load_data()
    available = len(all_q) - len(st.session_state.used_questions)
    
    if available >= 20:
        st.success(f"🎊 還有 {available} 題可以挑戰！")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 挑戰下一回合 (20題)", type="primary", use_container_width=True):
                start_game(st.session_state.round_num + 1)
                st.rerun()
        with col2:
            if st.button("🏠 回首頁", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
    else:
        st.info(f"剩餘題目不足20題（剩餘 {available} 題）")
        if st.button("🏠 回首頁", type="primary", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
