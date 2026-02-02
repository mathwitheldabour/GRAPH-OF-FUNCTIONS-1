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
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-text-ar { font-size: 20px; font-weight: bold; color: #1f2937; margin-bottom: 8px; }
    .question-text-en { font-size: 16px; color: #4b5563; font-family: sans-serif; direction: ltr; text-align: left; }
    .stButton button { width: 100%; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة حالة الجلسة
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
# 3. دالة الرسم البياني
# ---------------------------------------------------------
def plot_function(func, x_range=(-4, 6), y_range=(-5, 7), title="", has_asymptote_at=None):
    x = np.linspace(x_range[0], x_range[1], 1500)
    
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
# 4. تعريف دوال الرسم (Correct & Distractors)
# ---------------------------------------------------------

# --- Q27 Definitions ---
def q27_correct(x): return -1 * x**3 + 3 * x**2 + 1
def q27_trap_sharp(x): return np.where(x<0, -2*x+1, np.where(x<2, 2*x+1, -2*x+9)) 
def q27_trap_flipped(x): return x**3 - 3*x**2 + 3 
def q27_trap_mono(x): return x**3/4 + 1

# --- Q28 Definitions ---
def q28_correct(x): return np.where(x <= 2, (4/9)*((x+1)**2) + 1, -2*(x-2) + 5)
def q28_trap_smooth(x): return -0.4*(x+1)*(x-4.5) + 0.5 
def q28_trap_sharp_min(x): return np.where(x<-1, -x, np.where(x<2, 1.33*x+2.33, -x+7))

# --- Q29 Definitions ---
def q29_correct(x): return np.where(x < 0, -1/x - 2, np.where(x==0, np.nan, -0.5*(x-3)**2))
def q29_trap_min(x): return np.where(x < 0, -1/x - 2, np.where(x==0, np.nan, 0.5*(x-3)**2))
def q29_trap_hole(x): return np.where(x<3, -(x-3)**2, -(x-3)**2)

# --- Q30 Definitions ---
def q30_correct(x): return 2 * (x-1)**2 / (1 + (x-1)**2)
def q30_trap_max(x): return -2 * (x-1)**2 / (1 + (x-1)**2) + 2
def q30_trap_ha0(x): return (x-1)**2 / (1 + (x-1)**2)

# --- Q31 Definitions ---
def q31_correct(x): 
    conditions = [x < -1, (x >= -1) & (x < 0), (x >= 0) & (x < 2), x >= 2]
    funcs = [lambda x: -2*(x+1), lambda x: 2*(x+1), lambda x: 2-0.5*x**2, lambda x: -0.5*(x-2)**3]
    return np.piecewise(x, conditions, funcs)
def q31_trap_smooth_min(x): return (x+1)**2 * (2-x) * 0.5
def q31_trap_max_at_2(x): return np.where(x<-1, -2*(x+1), np.where(x<2, 2-(x-0.5)**2, -3*(x-2)))

# --- Q32 Definitions ---
def q32_correct(x): 
    return np.where(x < 1, x**3, np.where(x < 3, -0.5*(x-3)**2 - 1 + 2, -1*(x-3)**2 - 1))
def q32_trap_min_0(x): return np.where(x<3, (x)**2, -1*(x-3)**2 + 9)
def q32_trap_smooth_1(x): return np.sin(x) * 2

# ---------------------------------------------------------
# 5. بيانات الأسئلة (النصوص الكاملة)
# ---------------------------------------------------------

questions = [
    {
        "id": 27,
        "latex": r"f(0)=1, \quad f(2)=5, \\ f'(x) < 0 \text{ for } x < 0 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } 0 < x < 2",
        "correct": {"func": q27_correct, "va": None},
        "distractors": [
            {"func": q27_trap_flipped, "va": None},
            {"func": q27_trap_sharp, "va": None},
            {"func": q27_trap_mono, "va": None},
        ]
    },
    {
        "id": 28,
        "latex": r"f(-1)=1, \quad f(2)=5, \\ f'(x) < 0 \text{ for } x < -1 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } -1 < x < 2, \\ f'(-1)=0, \quad f'(2) \text{ does not exist}",
        "correct": {"func": q28_correct, "va": None},
        "distractors": [
            {"func": q28_trap_smooth, "va": None},
            {"func": q28_trap_sharp_min, "va": None},
            {"func": lambda x: -x+3, "va": None},
        ]
    },
    {
        "id": 29,
        "latex": r"f(3)=0, \quad f'(3)=0, \\ f'(x) < 0 \text{ for } x < 0 \text{ and } x > 3, \\ f'(x) > 0 \text{ for } 0 < x < 3, \\ f(0) \text{ and } f'(0) \text{ do not exist}",
        "correct": {"func": q29_correct, "va": 0},
        "distractors": [
            {"func": q29_trap_min, "va": 0},
            {"func": q29_trap_hole, "va": None},
            {"func": lambda x: np.where(x<3, (x-3)**2, -(x-3))+3, "va": 3},
        ]
    },
    {
        "id": 30,
        "latex": r"f(1)=0, \quad \lim_{x \to \infty} f(x) = 2, \\ f'(x) < 0 \text{ for } x < 1, \\ f'(x) > 0 \text{ for } x > 1, \quad f'(1)=0",
        "correct": {"func": q30_correct, "va": None},
        "distractors": [
            {"func": q30_trap_max, "va": None},
            {"func": q30_trap_ha0, "va": None},
            {"func": lambda x: 2*(x+1)**2/(1+(x+1)**2), "va": None},
        ]
    },
    {
        "id": 31,
        "latex": r"f(-1)=f(2)=0, \\ f'(x) < 0 \text{ for } x < -1 \text{ and } 0 < x < 2 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } -1 < x < 0, \\ f'(-1) \text{ does not exist}, \quad f'(2)=0",
        "correct": {"func": q31_correct, "va": None},
        "distractors": [
            {"func": q31_trap_max_at_2, "va": None},
            {"func": q31_trap_smooth_min, "va": None},
            {"func": lambda x: (x+1)*(x-2), "va": None},
        ]
    },
    {
        "id": 32,
        "latex": r"f(0)=0, \quad f(3)=-1, \\ f'(x) < 0 \text{ for } x > 3, \\ f'(x) > 0 \text{ for } x < 0 \text{ and } 0 < x < 1 \text{ and } 1 < x < 3, \\ f'(0)=0, \quad f'(1) \text{ does not exist}, \quad f'(3)=0",
        "correct": {"func": q32_correct, "va": None},
        "distractors": [
            {"func": q32_trap_min_0, "va": None},
            {"func": q32_trap_smooth_1, "va": None},
            {"func": lambda x: -x**2 + 3*x, "va": None},
        ]
    }
]

# ---------------------------------------------------------
# 6. عرض التطبيق
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
        st.success(f"✅ مذهل! الرسم ({correct_letter}) هو الصحيح.")
    else:
        st.error(f"❌ خطأ. الإجابة الصحيحة هي ({correct_letter}).")

st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ السابق"): prev_question(); st.rerun()
with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("التالي ➡️"): next_question(); st.rerun()
