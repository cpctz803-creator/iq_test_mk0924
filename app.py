import streamlit as st
import random

# --- 数列生成ロジック (変更なし) ---
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

# --- セッション状態の初期化 ---
if 'questions' not in st.session_state:
    patterns = [gen_arithmetic, gen_geometric, gen_fibo, gen_square, gen_cumulative, gen_difference]
    st.session_state.questions = [random.choice(patterns)() for _ in range(10)]
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answered = False # 回答したかどうかのフラグ
    st.session_state.finished = False

# --- UI表示 ---
st.title("🧠 究極のIQパターン認識テスト")

if not st.session_state.finished:
    idx = st.session_state.current_idx
    q = st.session_state.questions[idx]

    st.subheader(f"問題 {idx + 1} / 10")
    st.write(f"### 数列:  **{', '.join(map(str, q['sequence']))}, ?**")

    # 回答入力欄
    user_ans = st.number_input("? に入る数値を入力してください", value=0, step=1, key=f"input_{idx}")

    # 「回答を確定する」ボタン
    if not st.session_state.answered:
        if st.button("回答を確定する"):
            st.session_state.answered = True
            if user_ans == q['correct']:
                st.session_state.last_result = "correct"
                st.session_state.score += 1
            else:
                st.session_state.last_result = "wrong"
            st.rerun() # 画面を更新して解説を表示
    else:
        # 回答後の表示
        if st.session_state.last_result == "correct":
            st.success("★ 正解です！")
        else:
            st.error(f"✗ 残念！ 正解は {q['correct']} でした。")
        
        st.info(f"【解説: {q['type']}】 {q['explanation']}")

        # 「次の問題へ」または「結果を表示」ボタン
        button_label = "次の問題へ" if idx < 9 else "結果を表示する"
        if st.button(button_label):
            if idx < 9:
                st.session_state.current_idx += 1
                st.session_state.answered = False # フラグをリセット
                st.rerun()
            else:
                st.session_state.finished = True
                st.rerun()

else:
    # 最終結果表示
    st.balloons()
    st.header("すべての問題が終了しました！")
    score = st.session_state.score
    st.write(f"## あなたのスコア: {score} / 10")
    
    if score == 10: st.success("判定: 驚異的な洞察力（IQ 140超）")
    elif score >= 7: st.info("判定: 優秀なパターン認識能力")
    elif score >= 4: st.warning("判定: 平均的な知能指数です")
    else: st.error("判定: 焦らずロジックを観察しましょう！")

    if st.button("最初からやり直す"):
        # 全セッションをクリアしてリロード
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
