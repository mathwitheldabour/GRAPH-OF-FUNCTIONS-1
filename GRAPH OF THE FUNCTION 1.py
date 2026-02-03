import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات (CSS)
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Generator")

st.markdown("""
<style>
    /* تنسيق عام */
    .stApp { text-align: center; font-family: sans-serif; }
    
    /* تنسيق صندوق السؤال */
    .question-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-top: 5px solid #0d6efd;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .q-en {
        text-align: left;
        direction: ltr;
        font-size: 18px;
        color: #0d6efd;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .q-ar {
        text-align: right;
        direction: rtl;
        font-size: 20px;
        color: #0d6efd;
        font-weight: bold;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* تنسيق البطاقة (الخيار) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 15px !important;
        background: white;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #0d6efd;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(13, 110, 253, 0.15);
    }

    /* الحرف A, B, C */
    .opt-letter {
        color: #d63384;
        font-size: 24px;
        font-weight: 900;
        display: block;
        margin-bottom: 10px;
    }

    /* النص الإنجليزي */
    .opt-en {
        text-align: left;
        direction: ltr;
        font-size: 16px;
        color: #212529;
        margin-bottom: 5px;
        font-weight: 500;
    }

    /* النص العربي - تم ضبطه ليكون يمين ليسار */
    .opt-ar {
        text-align: right; 
        direction: rtl;
        font-size: 18px;
        color: #495057;
        font-family: 'Segoe UI', sans-serif;
        margin-top: 5px;
        padding-top: 5px;
        border-top: 1px dashed #e9ecef;
    }

    /* الأزرار */
    div[data-testid="column"] .stButton button {
        width: 100%;
        border-radius: 6px;
        margin-top: 10px;
        background-color: #f8f9fa;
        color: #212529;
        border: 1px solid #ced4da;
        font-weight: bold;
    }
    div[data-testid="column"] .stButton button:hover {
        background-color: #0d6efd;
        color: white;
        border-color: #0d6efd;
    }
    
    /* زر محاولة جديدة */
    .new-quiz-btn button {
        background-color: #198754 !important;
        color: white !important;
        font-size: 18px !important;
        padding: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. مولد الأسئلة الذكي
# ---------------------------------------------------------

def generate_linear_question():
    """توليد سؤال لدالة خطية (مشتقة)"""
    r = random.randint(-3, 3)
    slope = random.choice([-1, 1])
    
    def func_prime(x): return slope * (x - r)
    
    # تم إضافة مسافات حول المعادلات لحل مشكلة التنسيق
    if slope > 0:
        correct_en = rf"Dec on $(-\infty, {r})$, Inc on $({r}, \infty)$; Min at $x={r}$"
        correct_ar = rf"تناقص $(-\infty, {r})$، تزايد $({r}, \infty)$؛ صغرى عند $ x={r} $"
        d1_en = rf"Inc on $(-\infty, {r})$, Dec on $({r}, \infty)$; Max at $x={r}$"
        d1_ar = rf"تزايد $(-\infty, {r})$، تناقص $({r}, \infty)$؛ عظمى عند $ x={r} $"
    else:
        correct_en = rf"Inc on $(-\infty, {r})$, Dec on $({r}, \infty)$; Max at $x={r}$"
        correct_ar = rf"تزايد $(-\infty, {r})$، تناقص $({r}, \infty)$؛ عظمى عند $ x={r} $"
        d1_en = rf"Dec on $(-\infty, {r})$, Inc on $({r}, \infty)$; Min at $x={r}$"
        d1_ar = rf"تناقص $(-\infty, {r})$، تزايد $({r}, \infty)$؛ صغرى عند $ x={r} $"
        
    return {
        "func": func_prime,
        "q_en": r"Determine the local extrema from the graph of $f'(x)$.",
        "q_ar": r"حدد القيم القصوى المحلية من رسم المشتقة $f'(x)$.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": d1_en, "ar": d1_ar},
            {"en": rf"No local extrema", "ar": rf"لا توجد قيم قصوى محلية"},
            {"en": rf"Local Max at $x=0$", "ar": rf"قيمة عظمى محلية عند $ x=0 $"}
        ]
    }

def generate_quadratic_question():
    """توليد سؤال لدالة تربيعية (مشتقة)"""
    roots = sorted(random.sample(range(-3, 4), 2))
    r1, r2 = roots[0], roots[1]
    a = random.choice([-0.5, 0.5])
    
    def func_prime(x): return a * (x - r1) * (x - r2)
    
    if a > 0:
        correct_en = rf"Max at $x={r1}$, Min at $x={r2}$"
        correct_ar = rf"عظمى عند $ x={r1} $، صغرى عند $ x={r2} $"
        d1_en = rf"Min at $x={r1}$, Max at $x={r2}$"
        d1_ar = rf"صغرى عند $ x={r1} $، عظمى عند $ x={r2} $"
    else:
        correct_en = rf"Min at $x={r1}$, Max at $x={r2}$"
        correct_ar = rf"صغرى عند $ x={r1} $، عظمى عند $ x={r2} $"
        d1_en = rf"Max at $x={r1}$, Min at $x={r2}$"
        d1_ar = rf"عظمى عند $ x={r1} $، صغرى عند $ x={r2} $"

    vertex = round((r1+r2)/2, 1)
    return {
        "func": func_prime,
        "q_en": r"Identify the local extrema for $f(x)$.",
        "q_ar": r"حدد القيم القصوى المحلية للدالة $f(x)$.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": d1_en, "ar": d1_ar},
            {"en": rf"Max at $x={vertex}$ (Vertex)", "ar": rf"عظمى عند رأس القطع $ x={vertex} $"},
            {"en": rf"Decreasing everywhere", "ar": rf"متناقصة على مجالها"}
        ]
    }

def generate_touching_question():
    """توليد سؤال لجذر مكرر (يمس المحور)"""
    r = random.randint(-2, 2)
    a = random.choice([-0.3, 0.3])
    def func_prime(x): return a * (x - r)**2
    
    correct_en = rf"No extrema (Inflection at $x={r}$)"
    correct_ar = rf"لا توجد قيم قصوى (انقلاب عند $ x={r} $)"
    
    return {
        "func": func_prime,
        "q_en": r"Analyze the critical point at the root.",
        "q_ar": r"حلل النقطة الحرجة عند الجذر.",
        "correct": {"en": correct_en, "ar": correct_ar},
        "distractors": [
            {"en": rf"Local Max at $x={r}$", "ar": rf"قيمة عظمى محلية عند $ x={r} $"},
            {"en": rf"Local Min at $x={r}$", "ar": rf"قيمة صغرى محلية عند $ x={r} $"},
            {"en": rf"Vertical Asymptote", "ar": rf"خط تقارب رأسي"}
        ]
    }

def generate_quiz():
    """تكوين اختبار جديد"""
    q1 = generate_linear_question()
    q2 = generate_quadratic_question()
    q3 = generate_touching_question()
    q4 = generate_linear_question() # سؤال إضافي
    
    quiz = [q1, q2, q3, q4]
    random.shuffle(quiz)
    return quiz

# ---------------------------------------------------------
# 3. إدارة الحالة (Session State)
# ---------------------------------------------------------
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = generate_quiz()
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'selected_opt' not in st.session_state:
    st.session_state.selected_opt = None

def reset_quiz():
    st.session_state.quiz_data = generate_quiz()
    st.session_state.q_index = 0
    st.session_state.answered = False
    st.session_state.selected_opt = None

def check_answer(code):
    st.session_state.selected_opt = code
    st.session_state.answered = True

def next_question():
    if st.session_state.q_index < len(st.session_state.quiz_data) - 1:
        st.session_state.q_index += 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1
        st.session_state.answered = False
        st.session_state.selected_opt = None

# ---------------------------------------------------------
# 4. دالة الرسم
# ---------------------------------------------------------
def plot_derivative(func_prime, x_range=(-5, 5), y_range=(-5, 5)):
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = func_prime(x)
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # إعداد المحاور
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    
    # الرسم
    ax.plot(x, y, color='#0d6efd', linewidth=2.5)
    ax.text(x_range[1]*0.8, y_range[1]*0.8, "y = f'(x)", fontsize=12, color='#0d6efd', fontweight='bold')
    
    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 5. العرض (UI)
# ---------------------------------------------------------

current_quiz = st.session_state.quiz_data
q_idx = st.session_state.q_index
q_data = current_quiz[q_idx]

# شريط التقدم
st.progress((q_idx + 1) / len(current_quiz))

# 1. صندوق السؤال
st.markdown(f"""
<div class="question-box">
    <div class="q-en">Q{q_idx+1}: {q_data['q_en']}</div>
    <div class="q-ar">س{q_idx+1}: {q_data['q_ar']}</div>
</div>
""", unsafe_allow_html=True)

# 2. الرسم البياني
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.pyplot(plot_derivative(q_data['func']))

st.write("---")

# 3. الخيارات
# استخدام seed لضمان ثبات الخيارات أثناء الضغط
seed_val = q_idx + int(q_data['func'](0)*100)
random.seed(seed_val)

options_list = []
options_list.append({**q_data['correct'], "is_correct": True})
for dist in q_data['distractors']:
    options_list.append({**dist, "is_correct": False})
random.shuffle(options_list)

cols = st.columns(4)
letters = ['A', 'B', 'C', 'D']
option_map = {}

for idx, col in enumerate(cols):
    opt = options_list[idx]
    letter = letters[idx]
    option_map[letter] = opt
    
    with col:
        # إطار البطاقة
        with st.container(border=True):
            # الحرف
            st.markdown(f"<div class='opt-letter'>{letter}</div>", unsafe_allow_html=True)
            
            # النص الإنجليزي (LTR)
            st.markdown(f"<div class='opt-en'>{opt['en']}</div>", unsafe_allow_html=True)
            
            # النص العربي (RTL) مع class CSS مخصص
            st.markdown(f"<div class='opt-ar'>{opt['ar']}</div>", unsafe_allow_html=True)
            
            # الزر
            if st.button(f"Choose {letter}", key=f"btn_{q_idx}_{letter}"):
                check_answer(letter)

# 4. النتيجة
if st.session_state.answered:
    selected = st.session_state.selected_opt
    chosen_data = option_map[selected]
    
    st.write("")
    if chosen_data['is_correct']:
        st.success(f"✅ Correct! الإجابة ({selected}) صحيحة.", icon="✅")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. لقد اخترت ({selected}).", icon="❌")
        # عرض الإجابة الصحيحة
        correct_letter = [k for k, v in option_map.items() if v['is_correct']][0]
        correct_text = option_map[correct_letter]
        
        st.markdown(f"""
        <div style="background-color:#d1e7dd; color:#0f5132; padding:15px; border-radius:10px; text-align:center; border:1px solid #badbcc;">
            <div style="font-weight:bold; font-size:18px; margin-bottom:10px;">الإجابة الصحيحة هي: {correct_letter}</div>
            <div style="direction:ltr;">{correct_text['en']}</div>
            <div style="direction:rtl; margin-top:5px;">{correct_text['ar']}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("---")

# 5. التحكم
c_prev, c_new, c_next = st.columns([1, 2, 1])

with c_prev:
    if q_idx > 0:
        if st.button("⬅️ Previous / السابق"):
            prev_question()
            st.rerun()

with c_next:
    if q_idx < len(current_quiz) - 1:
        if st.button("Next / التالي ➡️"):
            next_question()
            st.rerun()

with c_new:
    st.markdown('<div class="new-quiz-btn">', unsafe_allow_html=True)
    if st.button("🔄 New Quiz / محاولة جديدة"):
        reset_quiz()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
