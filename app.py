import streamlit as st
import random

# --- 数列生成ロジック (前回のものをそのまま利用) ---
def gen_arithmetic():
    start, diff = random.randint(1, 20), random.randint(2, 10)
    return {"type": "等差数列", "sequence": [start + i * diff for i in range(4)], "correct": start + 4 * diff, "explanation": f"「{diff}」ずつ足す規則です。"}

def gen_geometric():
    start, ratio = random.randint(1, 5), random.choice([2, 3])
    return {"type": "等比数列", "sequence": [start * (ratio ** i) for i in range(4)], "correct": start * (ratio ** 4), "explanation": f"「{ratio}」倍ずつ掛ける規則です。"}

def gen_fibo():
    a, b = random.randint(1, 5), random.randint(1, 5)
    seq = [a, b]
    for _ in range(2): seq.append(seq[-1] + seq[-2])
    return {"type": "フィボナッチ数列", "sequence": seq, "correct": seq[-1] + seq[-2], "explanation": "前の2つを足す規則です。"}

def gen_square():
    p = random.choice([2, 3]); s = random.randint(1, 5)
    return {"type": "累乗数列", "sequence": [i**p for i in range(s, s+4)], "correct": (s+4)**p, "explanation": f"{p}乗の数値が並ぶ規則です。"}

def gen_cumulative():
    s = random.randint(1, 3); seq = [s, s*2]
    for _ in range(2): seq.append(sum(seq))
    return {"type": "累計数列", "sequence": seq, "correct": sum(seq), "explanation": "それまでの全合計が次になる規則です。"}

def gen_difference():
    curr, d, step = random.randint(1, 10), random.randint(1, 5), random.randint(1, 3)
    seq = []
    for _ in range(4): seq.append(curr); curr += d; d += step
    return {"type": "階差数列", "sequence": seq, "correct": curr, "explanation": f"増える量が{step}ずつ増える規則です。"}

# --- Streamlit アプリ本体 ---
st.title("🧠 究極のIQパターン認識テスト")

# セッション状態の初期化（状態を保持する）
if 'questions' not in st.session_state:
    patterns = [gen_arithmetic, gen_geometric, gen_fibo, gen_square, gen_cumulative, gen_difference]
    st.session_state.questions = [random.choice(patterns)() for _ in range(10)]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.finished = False

if not st.session_state.finished:
    idx = st.session_state.current_idx
    q = st.session_state.questions[idx]

    st.subheader(f"問題 {idx + 1} / 10")
    st.write(f"### 数列:  **{', '.join(map(str, q['sequence']))}, ?**")

    # 回答入力
    user_ans = st.number_input("? に入る数値を入力してください", value=0, step=1, key=f"q_{idx}")
    
    if st.button("回答を確定する"):
        if user_ans == q['correct']:
            st.success("★ 正解です！")
            st.session_state.score += 1
        else:
            st.error(f"✗ 残念！ 正解は {q['correct']} でした。")
        
        st.info(f"【解説: {q['type']}】 {q['explanation']}")
        
        # 次の問題へ進むボタン
        if idx < 9:
            if st.button("次の問題へ"):
                st.session_state.current_idx += 1
                st.rerun()
        else:
            st.session_state.finished = True
            if st.button("結果を表示する"):
                st.rerun()

else:
    # 結果発表
    st.balloons()
    st.header("テスト終了！")
    score = st.session_state.score
    st.write(f"## あなたのスコア: {score} / 10")
    
    if score == 10: st.success("判定: 驚異的な洞察力（IQ 140超）")
    elif score >= 7: st.info("判定: 優秀なパターン認識能力")
    else: st.warning("判定: 伸びしろがあります！")

    if st.button("もう一度挑戦する"):
        del st.session_state.questions
        st.rerun()