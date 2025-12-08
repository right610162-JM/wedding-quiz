import streamlit as st
import random
import time
import pandas as pd
import requests  # 新增：用來偷偷送出表單

# --- 🛠️ 設定區 (請修改這裡) ---

# 1. 題庫 CSV (原本的題目)
QUESTIONS_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-UEtx8h9lPYrdjWcAxuu7LwadNL0KXDrI-zQJ4XfwHDvKHOaNs35krRervsBPuMhcRs1OXyluKz0K/pub?output=csv"

# 2. 排行榜 CSV (第2步取得的連結)
LEADERBOARD_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTk1vGJOTJjoZHeXWA_JSnNOz9-AzflgHdaJhEgbgrcV4AxpjCa1x1ZP9oGk2H4ex9sDpoiHBRLfiev/pub?output=csv"

# 3. Google 表單提交網址 (第1步取得，記得把 viewform 改成 formResponse)
# 格式通常是: https://docs.google.com/forms/d/e/mVxu..../formResponse
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd0SOigmWPwEEP_zQv-LlPyCa99a-SQhqa0PP9kIvyJOaQbLw/viewform?usp=pp_url&entry.276737520=teamname&entry.1217367258=123"

# 4. Google 表單欄位代號 (第1步解碼取得)
ENTRY_NAME = "entry.xxxxxxx"  # 填入名字的 entry ID
ENTRY_SCORE = "entry.yyyyyyy" # 填入分數的 entry ID

# --------------------------------

st.set_page_config(page_title="敬民 & 紫淇 Wedding Quiz", page_icon="💍", layout="centered")

# CSS 優化
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; font-weight: bold; font-size: 18px; border: 2px solid #f0f2f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .stButton>button:active { transform: scale(0.98); }
    .big-font { font-size: 22px !important; font-weight: bold; color: #2D3436; margin-bottom: 20px; }
    .score-board { padding: 20px; background-color: #f0f2f5; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .rank-item { padding: 10px; margin: 5px 0; background: white; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #eee;}
    .rank-num { font-weight: bold; font-size: 20px; color: #81D8D0; width: 40px;}
    .rank-name { flex-grow: 1; text-align: left; font-weight: bold; color: #2D3436;}
    .rank-score { font-weight: bold; color: #E1B12C;}
    </style>
    """, unsafe_allow_html=True)

# 讀取題庫
@st.cache_data(ttl=60)
def load_questions():
    fallback = {"easy": [], "hard": []}
    if "http" not in QUESTIONS_CSV_URL: return fallback
    try:
        df = pd.read_csv(QUESTIONS_CSV_URL)
        data = {"easy": [], "hard": []}
        for _, row in df.iterrows():
            item = {
                "q": str(row['Question']),
                "options": [str(row['Option1']), str(row['Option2']), str(row['Option3']), str(row['Option4'])],
                "ans": int(row['Answer'])
            }
            if str(row['Mode']).lower().strip() == 'hard': data['hard'].append(item)
            else: data['easy'].append(item)
        return data
    except: return fallback

# 讀取排行榜 (快取時間設短一點，例如 10 秒，這樣才看得到最新排名)
@st.cache_data(ttl=10)
def load_leaderboard():
    if "http" not in LEADERBOARD_CSV_URL: return []
    try:
        df = pd.read_csv(LEADERBOARD_CSV_URL)
        # 假設表單欄位是 "Name" 和 "Score" (依據你的 Google 表單欄位名稱)
        # 通常 CSV 欄位名稱會是題目名稱
        # 這裡做一個簡單的欄位對應，請確保你表單題目是 Name 和 Score
        cols = df.columns.tolist()
        # 簡單判定：含有 Name 的欄位當名字，含有 Score 的當分數
        name_col = next((c for c in cols if 'Name' in c or '名稱' in c or '暱稱' in c), cols[1]) 
        score_col = next((c for c in cols if 'Score' in c or '分數' in c), cols[2])
        
        ranking = []
        for _, row in df.iterrows():
            ranking.append({"name": str(row[name_col]), "score": int(row[score_col])})
        
        # 排序：分數高到低
        ranking.sort(key=lambda x: x['score'], reverse=True)
        return ranking[:10] # 只回傳前 10 名
    except Exception as e:
        return []

# 送出分數到 Google Form
def submit_to_google(name, score):
    url = FORM_URL
    data = {
        ENTRY_NAME: name,
        ENTRY_SCORE: str(score)
    }
    try:
        requests.post(url, data=data)
        return True
    except:
        return False

# 初始化
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'advanced_unlocked' not in st.session_state: st.session_state.advanced_unlocked = False
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'correct_count' not in st.session_state: st.session_state.correct_count = 0
if 'questions' not in st.session_state: st.session_state.questions = []
if 'lifelines' not in st.session_state: st.session_state.lifelines = 2
if 'disabled_opts' not in st.session_state: st.session_state.disabled_opts = []
if 'submitted' not in st.session_state: st.session_state.submitted = False

# 頁面邏輯
def start_game(mode):
    all_q = load_questions()
    if not all_q[mode]: st.error("題庫讀取錯誤"); return
    q_list = all_q[mode][:]
    random.shuffle(q_list)
    st.session_state.questions = q_list
    st.session_state.mode = mode
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct_count = 0
    st.session_state.lifelines = 2
    st.session_state.disabled_opts = []
    st.session_state.submitted = False
    st.session_state.page = 'game'

def check(u_idx, ans_idx):
    if u_idx == (ans_idx - 1):
        st.session_state.score += 100
        st.session_state.correct_count += 1
        st.toast("🎉 答對了！ +100分", icon="✅")
    else:
        st.toast("❌ 答錯囉！", icon="❌")
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
        wrong = [i for i in range(4) if i != (ans_val - 1)]
        st.session_state.disabled_opts = random.sample(wrong, 2)
        st.rerun()

# --- 介面呈現 ---

if st.session_state.page == 'home':
    st.title("💖 敬民 & 紫淇")
    st.subheader("Wedding Quiz")
    st.write("---")
    if st.button("💖 初階：甜蜜回憶", type="primary"): start_game("easy"); st.rerun()
    st.write("")
    if st.session_state.advanced_unlocked:
        if st.button("🔥 進階：鐵粉魔王"): start_game("hard"); st.rerun()
    else:
        st.button("🔒 進階：鐵粉魔王", disabled=True)
    
    # 首頁顯示排行榜按鈕
    st.write("---")
    if st.button("🏆 查看目前排行榜"):
        st.session_state.page = 'leaderboard'
        st.rerun()

elif st.session_state.page == 'game':
    q = st.session_state.questions[st.session_state.current_q]
    st.progress((st.session_state.current_q + 1) / len(st.session_state.questions))
    st.markdown(f"**💎 {st.session_state.score}**")
    st.markdown(f"<div class='big-font'>Q{st.session_state.current_q+1}. {q['q']}</div>", unsafe_allow_html=True)
    
    if st.session_state.lifelines > 0 and not st.session_state.disabled_opts:
        if st.button(f"🆘 求救 ({st.session_state.lifelines})"): lifeline(q['ans'])

    for i, opt in enumerate(q['options']):
        disabled = i in st.session_state.disabled_opts
        if st.button(opt, key=f"{st.session_state.current_q}_{i}", disabled=disabled): check(i, q['ans'])

elif st.session_state.page == 'result':
    acc = (st.session_state.correct_count / len(st.session_state.questions)) * 100
    if st.session_state.mode == 'easy' and acc >= 70 and not st.session_state.advanced_unlocked:
        st.session_state.advanced_unlocked = True; st.balloons()

    st.title("挑戰結束")
    st.markdown(f"<div class='score-board'><h1>{st.session_state.score}</h1><p>正確率: {int(acc)}%</p></div>", unsafe_allow_html=True)
    
    st.write("### 📝 上傳成績")
    if not st.session_state.submitted:
        name_input = st.text_input("請輸入你的暱稱", max_chars=10)
        if st.button("上傳並查看排名", type="primary"):
            if name_input:
                with st.spinner("上傳中..."):
                    success = submit_to_google(name_input, st.session_state.score)
                    if success:
                        st.session_state.submitted = True
                        st.success("上傳成功！")
                        time.sleep(1)
                        st.session_state.page = 'leaderboard'
                        st.rerun()
                    else:
                        st.error("上傳失敗，請檢查網路或設定")
            else:
                st.warning("記得輸入名字喔！")
    else:
        st.info("✅ 成績已上傳")
        if st.button("查看排行榜"): st.session_state.page = 'leaderboard'; st.rerun()
    
    st.write("---")
    if st.button("🏠 回首頁重玩"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'leaderboard':
    st.title("🏆 英雄榜")
    if st.button("🔄 重新整理"): st.cache_data.clear(); st.rerun()
    
    ranking = load_leaderboard()
    
    if not ranking:
        st.info("目前還沒有人上傳成績，快來當第一名！")
    else:
        st.write("Top 10 高手")
        for i, rank in enumerate(ranking):
            medal = "🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else f"{i+1}."
            st.markdown(f"""
            <div class='rank-item'>
                <div class='rank-num'>{medal}</div>
                <div class='rank-name'>{rank['name']}</div>
                <div class='rank-score'>{rank['score']} 分</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.write("---")
    if st.button("🏠 回首頁"): st.session_state.page = 'home'; st.rerun()
