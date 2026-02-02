import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Calculus Quiz: Sketching Functions")

st.markdown("""
<style>
    .stApp { direction: rtl; }
    h1, h2, h3, p, div { text-align: right; }
    .katex-display, .katex { direction: ltr; text-align: center; }
    .stRadio > div { direction: rtl; text-align: right; }
    .question-box {
        background-color: #eef2f3;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #d63384;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-text-ar { font-size: 20px; font-weight: bold; color: #1f2937; margin-bottom: 8px; }
    .question-text-en { font-size: 16px; color: #4b5563; font-family: sans-serif; direction: ltr; text-align: left; }
    .stButton button { width: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. منطق التطبيق
# ---------------------------------------------------------
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

def next_question():
    if st.session_state.q_index < len(questions) - 1:
        st.session_state.q_index += 1

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1

# ---------------------------------------------------------
# 3. دالة الرسم البياني (دقيقة)
# ---------------------------------------------------------
def plot_function(func, x_range=(-4, 6), y_range=(-5, 7), title="", has_asymptote_at=None):
    x = np.linspace(x_range[0], x_range[1], 1500) # دقة عالية جداً
    
    try:
        y = func(x)
    except:
        y = np.zeros_like(x)

    # معالجة خطوط التقارب
    if has_asymptote_at is not None:
        threshold = 10
        y_diff = np.diff(y, prepend=y[0])
        y[np.abs(y_diff) > threshold] = np.nan
        
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # محاور في المنتصف
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    ax.plot(x, y, color='#0056b3', linewidth=2)
    
    if has_asymptote_at is not None:
         ax.axvline(x=has_asymptote_at, color='red', linestyle='--', linewidth=1, alpha=0.6)

    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    ax.set_title(title, fontsize=14, loc='right', color='black', fontweight='bold')
    
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة (الإجابات الصحيحة + المضللة جداً)
# ---------------------------------------------------------

# --- Question 27 ---
# Correct: Smooth Min at 0, Smooth Max at 2.
def q27_correct(x): return -1 * x**3 + 3 * x**2 + 1
# Trap: Sharp corners (Absolute val style) instead of smooth polynomial.
def q27_trap_sharp(x): return np.where(x<0, -2*x+1, np.where(x<2, 2*x+1, -2*x+9)) 
# Trap: Max at 0, Min at 2 (Reversed signs).
def q27_trap_flipped(x): return x**3 - 3*x**2 + 3 
# Trap: Monotonic (Increases then flattens then increases) - ignores the decreasing part.
def q27_trap_mono(x): return x**3/4 + 1

# --- Question 28 ---
# Correct: Smooth Min at -1 (f'=0), Sharp Max at 2 (f' DNE).
def q28_correct(x): return np.where(x <= 2, (4/9)*((x+1)**2) + 1, -2*(x-2) + 5)
# Trap: Smooth Max at 2 (Ignores "DNE" condition, makes it f'=0).
def q28_trap_smooth(x): return -0.4*(x+1)*(x-4.5) + 0.5 # Parabola-like
# Trap: Sharp Min at -1 (Ignores "f'=0" condition).
def q28_trap_sharp_min(x): return np.where(x<-1, -x, np.where(x<2, 1.33*x+2.33, -x+7))
# Trap: Wrong limits (shifts graph).

# --- Question 29 ---
# Correct: VA at 0. Max at 3 (f'=0). 
def q29_correct(x): return np.where(x < 0, -1/x - 2, np.where(x==0, np.nan, -0.5*(x-3)**2))
# Trap: Min at 3 instead of Max (Sign error).
def q29_trap_min(x): return np.where(x < 0, -1/x - 2, np.where(x==0, np.nan, 0.5*(x-3)**2))
# Trap: Hole at 0 instead of Asymptote (Ignores infinite behavior near 0).
def q29_trap_hole(x): return np.where(x<3, -(x-3)**2, -(x-3)**2) # Just a parabola
# Trap: Asymptote at 3 instead of 0.

# --- Question 30 ---
# Correct: Min at 1, HA at y=2.
def q30_correct(x): return 2 * (x-1)**2 / (1 + (x-1)**2)
# Trap: Max at 1 (Looks similar but upside down).
def q30_trap_max(x): return -2 * (x-1)**2 / (1 + (x-1)**2) + 2
# Trap: Min at 1, but HA at y=0 (Missing the vertical shift).
def q30_trap_ha0(x): return (x-1)**2 / (1 + (x-1)**2)
# Trap: Min at -1 (Shifted left).

# --- Question 31 ---
# Correct: Sharp Min at -1 (V), Saddle at 2 (Flat then down).
def q31_correct(x): 
    conditions = [x < -1, (x >= -1) & (x < 0), (x >= 0) & (x < 2), x >= 2]
    funcs = [lambda x: -2*(x+1), lambda x: 2*(x+1), lambda x: 2-0.5*x**2, lambda x: -0.5*(x-2)**3]
    return np.piecewise(x, conditions, funcs)
# Trap: Smooth Min at -1 (Ignores DNE).
def q31_trap_smooth_min(x): return (x+1)**2 * (2-x) # Polynomial approximation
# Trap: Standard Max at 2 (Goes up then down, not saddle). **Strongest Distractor**
def q31_trap_max_at_2(x): return np.where(x<-1, -2*(x+1), np.where(x<2, 2-(x-0.5)**2, -3*(x-2)))
# Trap: Sharp Max at 2 (Two linear lines meeting).

# --- Question 32 ---
# Correct: Saddle at 0 (Up-Flat-Up), Sharp at 1 (Kink), Smooth Max at 3.
def q32_correct(x): 
    return np.where(x < 1, x**3, np.where(x < 3, -0.5*(x-3)**2 - 1 + 2, -1*(x-3)**2 - 1))
# Trap: Min at 0 instead of Saddle.
def q32_trap_min_0(x): return np.where(x<3, (x)**2, -1*(x-3)**2 + 9)
# Trap: Smooth turn at 1 instead of Kink (DNE).
def q32_trap_smooth_1(x): return np.sin(x) * 2 # Random smooth wave
# Trap: Increasing after 3 (Ignores f'<0 for x>3).

questions = [
    {
        "id": 27,
        "latex": r"f(0)=1, f(2)=5, \\ f'(x) < 0 \text{ for } x < 0, x > 2, \\ f'(x) > 0 \text{ for } 0 < x < 2",
        "correct": {"func": q27_correct, "va": None},
        "distractors": [
            {"func": q27_trap_flipped, "va": None}, # Trap: عكس الإشارات (Max at 0)
            {"func": q27_trap_sharp, "va": None},   # Trap: رؤوس حادة بدلاً من ملساء
            {"func": q27_trap_mono, "va": None},    # Trap: دالة متزايدة فقط
        ]
    },
    {
        "id": 28,
        "latex": r"f(-1)=1, f(2)=5, \\ f'(-1)=0, f'(2) \text{ DNE}, \\ f'(x) < 0 \dots f'(x) > 0 \dots",
        "correct": {"func": q28_correct, "va": None},
        "distractors": [
            {"func": q28_trap_smooth, "va": None},    # Trap: قمة ملساء عند 2 (نسي DNE)
            {"func": q28_trap_sharp_min, "va": None}, # Trap: قاع حاد عند -1 (نسي =0)
            {"func": lambda x: -x+3, "va": None},     # Trap: دالة خطية
        ]
    },
    {
        "id": 29,
        "latex": r"f(3)=0, f'(3)=0, f(0) \text{ DNE}, \\ f'(x) < 0 \text{ everywhere except } (0,3)",
        "correct": {"func": q29_correct, "va": 0},
        "distractors": [
            {"func": q29_trap_min, "va": 0},    # Trap: قاع عند 3 بدلاً من قمة
            {"func": q29_trap_hole, "va": None}, # Trap: لا يوجد خط تقارب رأسي
            {"func": lambda x: np.where(x<3, (x-3)**2, -(x-3))+3, "va": 3}, # Trap: خط التقارب في مكان خاطئ
        ]
    },
    {
        "id": 30,
        "latex": r"f(1)=0, f'(1)=0, \lim_{x \to \infty} f(x) = 2",
        "correct": {"func": q30_correct, "va": None},
        "distractors": [
            {"func": q30_trap_max, "va": None}, # Trap: قمة عند 1 بدلاً من قاع
            {"func": q30_trap_ha0, "va": None}, # Trap: خط التقارب الأفقي عند 0
            {"func": lambda x: 2*(x+1)**2/(1+(x+1)**2), "va": None}, # Trap: إزاحة أفقية خطأ
        ]
    },
    {
        "id": 31,
        "latex": r"f(-1)=0, f'(-1) \text{ DNE}, \\ f(2)=0, f'(2)=0, \\ \text{Decreasing after } 2",
        "correct": {"func": q31_correct, "va": None},
        "distractors": [
            {"func": q31_trap_max_at_2, "va": None},   # Trap: قمة عادية عند 2 (ليست نقطة سرج/انقلاب)
            {"func": q31_trap_smooth_min, "va": None}, # Trap: قاع أملس عند -1 (نسي DNE)
            {"func": lambda x: (x+1)*(x-2), "va": None}, # Trap: شكل عام خاطئ
        ]
    },
    {
        "id": 32,
        "latex": r"f(0)=0, f'(0)=0, \\ f(3)=-1, f'(3)=0, \\ f'(1) \text{ DNE}",
        "correct": {"func": q32_correct, "va": None},
        "distractors": [
            {"func": q32_trap_min_0, "va": None},    # Trap: قاع عند 0 بدلاً من نقطة انقلاب
            {"func": q32_trap_smooth_1, "va": None}, # Trap: انحناء أملس عند 1 (نسي DNE)
            {"func": lambda x: -x**2 + 3*x, "va": None}, # Trap: قطع مكافئ بسيط
        ]
    }
]

# ---------------------------------------------------------
# 5. عرض التطبيق
# ---------------------------------------------------------

q_idx = st.session_state.q_index
q = questions[q_idx]

progress = (q_idx + 1) / len(questions)
st.progress(progress)

st.markdown("""
<div class="question-box">
    <div class="question-text-ar">أي من الرسومات البيانية التالية يطابق بدقة جميع الخواص المذكورة؟</div>
    <div class="question-text-en">Which graph accurately represents all the given properties?</div>
    <p style="font-size:14px; color:#666; margin-top:5px;">⚠️ انتبه: الفرق قد يكون في "حدة" الزاوية أو نوع نقطة الرجوع.</p>
</div>
""", unsafe_allow_html=True)

st.latex(q['latex'])

random.seed(q['id'] + 999) 

options_data = []
options_data.append({"type": "correct", "fig": plot_function(q["correct"]["func"], has_asymptote_at=q["correct"]["va"])})
for dist in q["distractors"]:
    options_data.append({"type": "wrong", "fig": plot_function(dist["func"], has_asymptote_at=dist["va"])})

random.shuffle(options_data)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
cols_list = [col1, col2, col3, col4]
letters = ['A', 'B', 'C', 'D']
correct_letter = None

for idx, opt_data in enumerate(options_data):
    letter = letters[idx]
    with cols_list[idx]:
        opt_data["fig"].axes[0].set_title(f"({letter})", loc='left', fontsize=14)
        st.pyplot(opt_data["fig"])
        if opt_data["type"] == "correct":
            correct_letter = letter

st.markdown("---")
col_input, col_action = st.columns([2, 1])

with col_input:
    user_answer = st.radio("الإجابة / Answer:", letters, key=f"radio_{q['id']}", horizontal=True)

with col_action:
    st.write("") 
    st.write("") 
    check_btn = st.button("تحقق / Check", key=f"check_{q['id']}")

if check_btn:
    if user_answer == correct_letter:
        st.success(f"✅ مذهل! ملاحظة دقيقة جداً. الرسم ({correct_letter}) هو الصحيح.")
    else:
        st.error(f"❌ خطأ. ركز في التفاصيل الدقيقة (رأس حاد vs أملس، أو نقطة انقلاب vs عظمى). الإجابة هي ({correct_letter}).")

st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ السابق"): prev_question(); st.rerun()
with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("التالي ➡️"): next_question(); st.rerun()
