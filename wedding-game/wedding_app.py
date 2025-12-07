import streamlit as st
import random
import time
import pandas as pd

# --- 設定區 ---
# 👇👇👇 請把你的 Google Sheet CSV 連結貼在引號裡面 👇👇👇
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"
# ☝️☝️☝️ 例如 "https://docs.google.com/spreadsheets/.....output=csv"

st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# CSS 美化 (手機版優化)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; border-radius: 20px; height: 3.5em;
        font-weight: bold; font-size: 18px;
        border: 2px solid #f0f2f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:active { transform: scale(0.98); }
    .big-font { font-size: 22px !important; font-weight: bold; color: #2D3436; margin-bottom: 20px; }
    .score-board { padding: 20px; background-color: #f0f2f5; border-radius: 15px; text-align: center; margin-bottom: 20px; }
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
    except:
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


# 邏輯函數
def start_game(mode):
    all_q = load_data()
    if not all_q[mode]: st.error("讀取不到題目，請檢查 Google Sheet 連結"); return

    # ★ 隨機打亂題目
    q_list = all_q[mode][:]
    random.shuffle(q_list)

    st.session_state.questions = q_list
    st.session_state.mode = mode
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.lifelines = 2
    st.session_state.disabled_opts = []
    st.session_state.page = 'game'


def check(u_idx, ans_idx):
    # ★ 不顯示答案，只顯示對錯
    if u_idx == (ans_idx - 1):
        st.session_state.score += 100
        st.session_state.correct_count += 1
        st.toast("🎉 答對了！ +100分", icon="✅")
    else:
        st.toast("❌ 答錯囉！繼續加油～", icon="❌")

    time.sleep(0.6)
    if st.session_state.current_q < len(st.session_state.questions) - 1:
        st.session_state.current_q += 1
        st.session_state.disabled_opts = []
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
        st.rerun()


# 介面
if st.session_state.page == 'home':
    st.title("💖 敬民 & 紫淇")
    st.subheader("Wedding Quiz")
    load_data()  # 預載
    st.write("---")
    if st.button("💖 初階：甜蜜回憶", type="primary"): start_game("easy"); st.rerun()
    st.write("")
    if st.session_state.advanced_unlocked:
        if st.button("🔥 進階：鐵粉魔王"): start_game("hard"); st.rerun()
    else:
        st.button("🔒 進階：鐵粉魔王", disabled=True)
        st.caption("🔒 正確率達 70% 解鎖")

elif st.session_state.page == 'game':
    q = st.session_state.questions[st.session_state.current_q]
    total = len(st.session_state.questions)

    st.progress((st.session_state.current_q + 1) / total)
    st.markdown(f"**分數: {st.session_state.score}**")
    st.markdown(f"<div class='big-font'>Q{st.session_state.current_q + 1}. {q['q']}</div>", unsafe_allow_html=True)

    if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
        if st.button(f"🆘 求救 ({st.session_state.lifelines})"): lifeline(q['ans'])

    for i, opt in enumerate(q['options']):
        disabled = i in st.session_state.disabled_opts
        if st.button(opt, key=f"{st.session_state.current_q}_{i}", disabled=disabled): check(i, q['ans'])

elif st.session_state.page == 'result':
    acc = (st.session_state.correct_count / len(st.session_state.questions)) * 100
    if st.session_state.mode == 'easy' and acc >= 70 and not st.session_state.advanced_unlocked:
        st.session_state.advanced_unlocked = True;
        st.balloons()

    st.title("挑戰結束")
    st.markdown(f"<div class='score-board'><h1>{st.session_state.score}</h1><p>正確率: {int(acc)}%</p></div>",
                unsafe_allow_html=True)
    if st.button("🏠 回首頁"): st.session_state.page = 'home'; st.rerun()