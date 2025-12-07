import streamlit as st
import random
import time
import pandas as pd

# --- 設定區 ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"

st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# 莫蘭迪色系 CSS (活潑風格)
st.markdown("""
    <style>
    /* 主要配色：莫蘭迪色系 */
    :root {
        --morandi-pink: #E8B4B8;
        --morandi-blue: #A6B8C7;
        --morandi-green: #B8C5B0;
        --morandi-yellow: #E5D4A6;
        --morandi-purple: #C4B5CF;
        --morandi-coral: #E8C5B5;
    }
    
    /* 整體背景 */
    .stApp {
        background: linear-gradient(135deg, #f5f0f6 0%, #fef4f0 100%);
    }
    
    /* 按鈕樣式 */
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
    
    /* 主要按鈕 */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #E8B4B8 0%, #C4B5CF 100%);
        color: white;
        border: none;
    }
    
    /* 禁用按鈕 */
    .stButton>button:disabled {
        background: #e9e9e9;
        border-color: #d0d0d0;
        color: #999;
        opacity: 0.6;
    }
    
    /* 題目文字 */
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
    
    /* 分數板 */
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
    
    /* 答案提示框 */
    .answer-reveal {
        padding: 20px; 
        background: linear-gradient(135deg, #E5D4A6 0%, #f5ead0 100%);
        border-radius: 15px;
        border-left: 6px solid #d4b47e;
        margin: 15px 0;
        color: #6B5B6E;
        font-weight: bold;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    
    /* 統計框 */
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
    
    /* 答對率大圓圈 */
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
    
    /* 指標卡片 */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #6B5B6E;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8B7B8E !important;
        font-weight: 600;
    }
    
    /* 進度條 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #E8B4B8 0%, #C4B5CF 50%, #A6B8C7 100%);
    }
    
    /* 成功/錯誤訊息 */
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
    
    /* 標題樣式 */
    h1 {
        color: #6B5B6E !important;
        text-align: center;
    }
    
    h3 {
        color: #8B7B8E !important;
    }
    
    /* 分隔線 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #E8B4B8 50%, transparent 100%);
        margin: 30px 0;
    }
    </style>
    """, unsafe_allow_html=True)


# 讀取資料 (簡化版 - 不區分難度)
@st.cache_data(ttl=60)
def load_data():
    fallback = []
    if "YOUR_CSV_LINK" in CSV_URL or CSV_URL == "": 
        return fallback
    
    try:
        df = pd.read_csv(CSV_URL)
        
        # 自動偵測欄位名稱 (不區分大小寫，去除空格)
        cols = {col.lower().strip(): col for col in df.columns}
        
        # 找出對應的欄位
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
            st.write("目前偵測到的欄位：", df.columns.tolist())
            return fallback
        
        option_cols = sorted(option_cols)[:4]  # 取前4個選項
        
        data = []
        for _, row in df.iterrows():
            try:
                item = {
                    "q": str(row[question_col]),
                    "options": [str(row[col]) for col in option_cols],
                    "ans": int(row[answer_col])
                }
                data.append(item)
            except Exception as e:
                st.warning(f"跳過一筆資料: {e}")
                continue
        
        return data
        
    except Exception as e:
        st.error(f"讀取資料時發生錯誤: {e}")
        st.write("請檢查 CSV 連結是否正確，並確認已設定為「任何知道連結的使用者」可檢視")
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
    st.session_state.lifelines = 2
if 'disabled_opts' not in st.session_state: 
    st.session_state.disabled_opts = []
if 'show_answer' not in st.session_state: 
    st.session_state.show_answer = False
if 'last_answer_correct' not in st.session_state: 
    st.session_state.last_answer_correct = None
if 'answer_start_time' not in st.session_state: 
    st.session_state.answer_start_time = None


# 邏輯函數
def start_game():
    all_q = load_data()
    if not all_q: 
        st.error("讀取不到題目，請檢查 Google Sheet 連結與欄位設定")
        return

    # 打散所有題目
    q_list = all_q[:]
    random.shuffle(q_list)

    st.session_state.questions = q_list
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.lifelines = 2
    st.session_state.disabled_opts = []
    st.session_state.show_answer = False
    st.session_state.last_answer_correct = None
    st.session_state.answer_start_time = time.time()
    st.session_state.page = 'game'


def check(u_idx, ans_idx):
    if st.session_state.show_answer:
        return
    
    time_taken = time.time() - st.session_state.answer_start_time
    base_score = 100
    speed_bonus = 0
    if time_taken < 10:
        speed_bonus = int((10 - time_taken) * 5)
    
    lifeline_penalty = (2 - st.session_state.lifelines) * 20
    
    if u_idx == (ans_idx - 1):
        final_score = max(base_score + speed_bonus - lifeline_penalty, 50)
        st.session_state.score += final_score
        st.session_state.correct_count += 1
        st.session_state.last_answer_correct = True
        st.balloons()
        st.toast(f"🎉 答對了！+{final_score}分", icon="✅")
    else:
        st.session_state.last_answer_correct = False
        st.toast("❌ 答錯了！", icon="❌")
    
    st.session_state.show_answer = True
    st.rerun()


def next_question():
    if st.session_state.current_q < len(st.session_state.questions) - 1:
        st.session_state.current_q += 1
        st.session_state.disabled_opts = []
        st.session_state.show_answer = False
        st.session_state.last_answer_correct = None
        st.session_state.answer_start_time = time.time()
        st.rerun()
    else:
        st.session_state.page = 'result'
        st.rerun()


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
            ✨ 每題答對得 <strong>100分</strong><br>
            ⚡ 速度越快，加分越多<br>
            🆘 使用求救會扣分哦<br>
            📊 最後以<strong>答對率</strong>評估你對新人的了解程度
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 預載資料
    data = load_data()
    
    if data:
        st.info(f"📝 共有 {len(data)} 題，準備好了嗎？")
    
    st.write("---")
    
    if st.button("🎯 開始挑戰", type="primary", use_container_width=True): 
        start_game()
        st.rerun()

elif st.session_state.page == 'game':
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
        current_acc = int((st.session_state.correct_count / (st.session_state.current_q + 1 if st.session_state.show_answer else st.session_state.current_q or 1)) * 100) if st.session_state.current_q > 0 or st.session_state.show_answer else 0
        st.metric("📊 答對率", f"{current_acc}%")
    
    st.write("---")
    
    # 題目
    st.markdown(f"<div class='big-font'>Q{st.session_state.current_q + 1}. {q['q']}</div>", unsafe_allow_html=True)

    # 求救按鈕
    if not st.session_state.show_answer:
        if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
            if st.button(f"🆘 求救 ({st.session_state.lifelines})", use_container_width=True): 
                lifeline(q['ans'])

    # 選項
    if not st.session_state.show_answer:
        for i, opt in enumerate(q['options']):
            disabled = i in st.session_state.disabled_opts
            if st.button(opt, key=f"opt_{st.session_state.current_q}_{i}", disabled=disabled, use_container_width=True): 
                check(i, q['ans'])
    else:
        # 顯示答案
        correct_idx = q['ans'] - 1
        
        if st.session_state.last_answer_correct:
            st.success("🎉 恭喜答對！")
        else:
            st.error("😢 很可惜答錯了")
            st.markdown(f"<div class='answer-reveal'>💡 正確答案是：<strong>{q['options'][correct_idx]}</strong></div>", unsafe_allow_html=True)
        
        # 顯示所有選項
        for i, opt in enumerate(q['options']):
            if i == correct_idx:
                st.success(f"✓ {opt}")
            else:
                st.info(f"  {opt}")
        
        st.write("---")
        if st.button("➡️ 下一題", type="primary", use_container_width=True):
            next_question()

elif st.session_state.page == 'result':
    total_q = len(st.session_state.questions)
    acc = (st.session_state.correct_count / total_q) * 100 if total_q > 0 else 0
    wrong_count = total_q - st.session_state.correct_count

    st.title("🎉 挑戰結束")
    
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
    
    # 額外統計
    st.write("")
    st.info(f"🎮 本次共答題 {total_q} 題 | 🆘 使用求救 {2 - st.session_state.lifelines} 次")
    
    st.write("")
    if st.button("🏠 回首頁", type="primary", use_container_width=True): 
        st.session_state.page = 'home'
        st.rerun()
