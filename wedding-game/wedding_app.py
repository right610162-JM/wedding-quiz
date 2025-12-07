import streamlit as st
import random
import time
import pandas as pd

# --- 設定區 ---
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"

st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# CSS 美化 (手機版優化)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        font-weight: bold; font-size: 18px;
        border: 2px solid #f0f2f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .stButton>button:active { transform: scale(0.98); }
    .big-font { font-size: 22px !important; font-weight: bold; color: #2D3436; margin-bottom: 20px; line-height: 1.5; }
    .score-board { 
        padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; text-align: center; margin-bottom: 20px; color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .answer-reveal {
        padding: 15px; background-color: #ffeaa7; border-radius: 10px;
        border-left: 4px solid #fdcb6e; margin: 15px 0;
    }
    .stat-box {
        display: inline-block; padding: 10px 20px; margin: 5px;
        background-color: #f0f2f5; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# 讀取資料
@st.cache_data(ttl=60)
def load_data():
    fallback = {"easy": [], "hard": []}
    if "YOUR_CSV_LINK" in CSV_URL or CSV_URL == "": return fallback
    try:
        df = pd.read_csv(CSV_URL)
        data = {"easy": [], "hard": []}
        for _, row in df.iterrows():
            item = {
                "q": str(row['Question']),
                "options": [str(row['Option1']), str(row['Option2']), str(row['Option3']), str(row['Option4'])],
                "ans": int(row['Answer'])
            }
            if str(row['Mode']).lower().strip() == 'hard':
                data['hard'].append(item)
            else:
                data['easy'].append(item)
        return data
    except Exception as e:
        st.error(f"讀取資料時發生錯誤: {e}")
        return fallback


# 初始化
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'advanced_unlocked' not in st.session_state: st.session_state.advanced_unlocked = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'correct_count' not in st.session_state: st.session_state.correct_count = 0
if 'questions' not in st.session_state: st.session_state.questions = []
if 'lifelines' not in st.session_state: st.session_state.lifelines = 2
if 'disabled_opts' not in st.session_state: st.session_state.disabled_opts = []
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
if 'last_answer_correct' not in st.session_state: st.session_state.last_answer_correct = None
if 'answer_start_time' not in st.session_state: st.session_state.answer_start_time = None


# 邏輯函數
def start_game(mode):
    all_q = load_data()
    if not all_q[mode]:
        st.error("讀取不到題目，請檢查 Google Sheet 連結")
        return

    q_list = all_q[mode][:]
    random.shuffle(q_list)

    st.session_state.questions = q_list
    st.session_state.mode = mode
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

    # 計算答題時間
    time_taken = time.time() - st.session_state.answer_start_time

    # 基礎分數
    base_score = 100

    # 速度加分 (10秒內答對有額外分數)
    speed_bonus = 0
    if time_taken < 10:
        speed_bonus = int((10 - time_taken) * 5)

    # 使用過求救功能減分
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
    st.subheader("Wedding Quiz")

    st.markdown("""
    ### 🎮 遊戲規則
    - 每題答對得 **100分** (速度越快加分越多)
    - 使用求救功能會扣分哦
    - 初階模式正確率達 **70%** 解鎖進階模式
    """)

    load_data()
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💖 初階：甜蜜回憶", type="primary", use_container_width=True):
            start_game("easy")
            st.rerun()

    with col2:
        if st.session_state.advanced_unlocked:
            if st.button("🔥 進階：鐵粉魔王", use_container_width=True):
                start_game("hard")
                st.rerun()
        else:
            st.button("🔒 進階：鐵粉魔王", disabled=True, use_container_width=True)
            st.caption("🔒 正確率達 70% 解鎖")

elif st.session_state.page == 'game':
    q = st.session_state.questions[st.session_state.current_q]
    total = len(st.session_state.questions)

    # 進度條和統計
    st.progress((st.session_state.current_q + 1) / total)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("分數", st.session_state.score)
    with col2:
        st.metric("題數", f"{st.session_state.current_q + 1}/{total}")
    with col3:
        st.metric("正確", f"{st.session_state.correct_count}")

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
        # 顯示答案解析
        correct_idx = q['ans'] - 1

        if st.session_state.last_answer_correct:
            st.success("✅ 恭喜答對！")
        else:
            st.error("❌ 很可惜答錯了")
            st.markdown(f"<div class='answer-reveal'>💡 正確答案是：<strong>{q['options'][correct_idx]}</strong></div>",
                        unsafe_allow_html=True)

        # 顯示所有選項（高亮正確答案）
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

    if st.session_state.mode == 'easy' and acc >= 70 and not st.session_state.advanced_unlocked:
        st.session_state.advanced_unlocked = True
        st.balloons()
        st.success("🎊 恭喜解鎖進階模式！")

    st.title("🎉 挑戰結束")

    st.markdown(f"""
    <div class='score-board'>
        <h1 style='font-size: 3em; margin: 0;'>{st.session_state.score}</h1>
        <p style='font-size: 1.2em; margin: 10px 0;'>總分</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='stat-box'><strong>{st.session_state.correct_count}/{total_q}</strong><br>答對</div>",
                    unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box'><strong>{int(acc)}%</strong><br>正確率</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-box'><strong>{2 - st.session_state.lifelines}</strong><br>使用求救</div>",
                    unsafe_allow_html=True)

    # 評價
    st.write("---")
    if acc == 100:
        st.markdown("### 🏆 完美！你們倆真的是天生一對！")
    elif acc >= 80:
        st.markdown("### 🌟 太棒了！對新人非常了解呢！")
    elif acc >= 60:
        st.markdown("### 👍 不錯喔！繼續加油！")
    else:
        st.markdown("### 💪 再接再厲！多多關注新人動態～")

    st.write("")
    if st.button("🏠 回首頁", type="primary", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
