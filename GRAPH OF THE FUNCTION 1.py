import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

# ---------------------------------------------------------
# 1. إعداد الصفحة والتنسيقات
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Math Quiz")

st.markdown("""
<style>
    /* الاتجاه العام للتطبيق من اليمين لليسار */
    .stApp {
        direction: rtl; 
    }
    
    /* محاذاة النصوص */
    h1, h2, h3, p, div {
        text-align: right;
    }

    /* إجبار المعادلات الرياضية واللاتكس على الاتجاه من اليسار لليمين */
    .katex-display, .katex {
        direction: ltr;
        text-align: center;
    }
    
    /* محاذاة أزرار الاختيار */
    .stRadio > div {
        direction: rtl;
        text-align: right;
    }
    
    /* تنسيق صندوق السؤال */
    .question-box {
        background-color: #f1f3f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #007bff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-text-ar {
        font-size: 20px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 8px;
    }
    .question-text-en {
        font-size: 16px;
        color: #4b5563;
        font-family: sans-serif;
        direction: ltr;
        text-align: left;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. إدارة حالة الجلسة (للتنقل)
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
# 3. دالة الرسم البياني (محاور في المنتصف)
# ---------------------------------------------------------
def plot_function(func, x_range=(-5, 5), vas=[], has=[], title=""):
    """
    رسم الدالة مع محاور إحداثية مركزية (Centered Spines)
    """
    x = np.linspace(x_range[0], x_range[1], 800)
    
    # حساب قيم y ومعالجة الأخطاء
    try:
        y = func(x)
    except:
        y = np.zeros_like(x)

    # معالجة نقاط الانفصال (Asymptotes) لمنع الخطوط الرأسية الخاطئة
    threshold = 10
    y_diff = np.diff(y, prepend=y[0])
    y[np.abs(y_diff) > threshold] = np.nan
    
    # حدود المحور الصادي
    y_lim = (-6, 6)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # --- تعديل المحاور لتكون في المنتصف (0,0) ---
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # تدريج المحاور
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    
    # تحسين مظهر الأرقام
    ax.tick_params(axis='both', which='major', labelsize=8, direction='inout')
    
    # رسم شبكة خفيفة
    ax.grid(True, which='both', linestyle=':', alpha=0.4)

    # رسم الدالة
    ax.plot(x, y, color='#0056b3', linewidth=2, label='f(x)')
    
    # رسم خطوط التقارب الرأسية (VA)
    for va in vas:
        ax.axvline(x=va, color='red', linestyle='--', linewidth=1, alpha=0.6)
        
    # رسم خطوط التقارب الأفقية (HA)
    for ha in has:
        ax.axhline(y=ha, color='green', linestyle='--', linewidth=1, alpha=0.6)
        
    ax.set_ylim(y_lim)
    ax.set_xlim(x_range)
    
    # وضع عنوان صغير للحرف (A, B, C, D)
    ax.set_title(title, fontsize=12, loc='right', color='black', fontweight='bold')
    
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة
# ---------------------------------------------------------
questions = [
    {
        "id": 33, # ID is used for logic only, not displayed
        "latex": r"y = \frac{x}{x^2 - 1}",
        "correct": {"func": lambda x: x / (x**2 - 1), "vas": [-1, 1], "has": [0]},
        "distractors": [
            {"func": lambda x: -x / (x**2 - 1), "vas": [-1, 1], "has": [0]},
            {"func": lambda x: x**2 / (x**2 - 1), "vas": [-1, 1], "has": [1]},
            {"func": lambda x: x / (x**2 + 1), "vas": [], "has": [0]},
        ]
    },
    {
        "id": 34,
        "latex": r"y = \frac{x^2}{x^2 - 1}",
        "correct": {"func": lambda x: x**2 / (x**2 - 1), "vas": [-1, 1], "has": [1]},
        "distractors": [
            {"func": lambda x: x / (x**2 - 1), "vas": [-1, 1], "has": [0]},
            {"func": lambda x: -(x**2) / (x**2 - 1), "vas": [-1, 1], "has": [-1]},
            {"func": lambda x: (x**2 + 2) / (x**2 - 1), "vas": [-1, 1], "has": [1]},
        ]
    },
    {
        "id": 35,
        "latex": r"y = \frac{x^2}{x^2 - 4x + 3}",
        "correct": {"func": lambda x: x**2 / (x**2 - 4*x + 3), "vas": [1, 3], "has": [1]},
        "distractors": [
            {"func": lambda x: x**2 / (x**2 + 4*x + 3), "vas": [-1, -3], "has": [1]},
            {"func": lambda x: -x**2 / (x**2 - 4*x + 3), "vas": [1, 3], "has": [-1]},
            {"func": lambda x: (x-2) / ((x-1)*(x-3)), "vas": [1, 3], "has": [0]},
        ]
    },
    {
        "id": 36,
        "latex": r"y = \frac{x}{1 - x^4}",
        "correct": {"func": lambda x: x / (1 - x**4), "vas": [-1, 1], "has": [0]},
        "distractors": [
            {"func": lambda x: x / (x**4 - 1), "vas": [-1, 1], "has": [0]},
            {"func": lambda x: x**2 / (1 - x**4), "vas": [-1, 1], "has": [0]},
            {"func": lambda x: x / (1 + x**4), "vas": [], "has": [0]},
        ]
    },
    {
        "id": 37,
        "latex": r"y = \frac{x}{\sqrt{x^2 + 1}}",
        "correct": {"func": lambda x: x / np.sqrt(x**2 + 1), "vas": [], "has": [1, -1]},
        "distractors": [
            {"func": lambda x: 1 / (x**2 + 1), "vas": [], "has": [0]},
            {"func": lambda x: x**2 / np.sqrt(x**2 + 1), "vas": [], "has": []},
            {"func": lambda x: -x / np.sqrt(x**2 + 1), "vas": [], "has": [1, -1]},
        ]
    },
    {
        "id": 38,
        "latex": r"y = \frac{x^2 + 2}{(x + 1)^2}",
        "correct": {"func": lambda x: (x**2 + 2) / (x + 1)**2, "vas": [-1], "has": [1]},
        "distractors": [
            {"func": lambda x: (x**2 + 2) / (x - 1)**2, "vas": [1], "has": [1]},
            {"func": lambda x: -(x**2 + 2) / (x + 1)**2, "vas": [-1], "has": [-1]},
            {"func": lambda x: x / (x + 1)**2, "vas": [-1], "has": [0]},
        ]
    }
]

# ---------------------------------------------------------
# 5. عرض التطبيق
# ---------------------------------------------------------

# الحصول على السؤال الحالي
q_idx = st.session_state.q_index
q = questions[q_idx]

# --- شريط التقدم ---
progress = (q_idx + 1) / len(questions)
st.progress(progress)

# --- نص السؤال (عربي / انجليزي) ---
st.markdown("""
<div class="question-box">
    <div class="question-text-ar">أي مما يلي يوضح جميع خواص الدالة التالية؟</div>
    <div class="question-text-en">Which of the following illustrates all properties of the function below?</div>
</div>
""", unsafe_allow_html=True)

# عرض معادلة الدالة
st.latex(q['latex'])

# --- تجهيز الخيارات (الرسوم) ---
# نستخدم معرف السؤال كـ Seed لضمان ثبات الخيارات لنفس السؤال
random.seed(q['id']) 

options_data = []
# إضافة الخيار الصحيح
options_data.append({
    "type": "correct",
    "fig": plot_function(q["correct"]["func"], vas=q["correct"]["vas"], has=q["correct"]["has"])
})
# إضافة الخيارات الخاطئة
for dist in q["distractors"]:
    options_data.append({
        "type": "wrong",
        "fig": plot_function(dist["func"], vas=dist["vas"], has=dist["has"])
    })

# خلط الخيارات
random.shuffle(options_data)

# --- عرض الرسوم في شبكة ---
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
cols_list = [col1, col2, col3, col4]
letters = ['A', 'B', 'C', 'D']
correct_letter = None

for idx, opt_data in enumerate(options_data):
    letter = letters[idx]
    with cols_list[idx]:
        # نضع الحرف داخل الرسم كعنوان
        opt_data["fig"].axes[0].set_title(f"({letter})", loc='left', fontsize=14)
        st.pyplot(opt_data["fig"])
        if opt_data["type"] == "correct":
            correct_letter = letter

# --- منطقة الإجابة ---
st.markdown("---")
col_input, col_action = st.columns([2, 1])

with col_input:
    user_answer = st.radio(
        "الإجابة / Answer:",
        letters,
        key=f"radio_{q['id']}",
        horizontal=True
    )

with col_action:
    st.write("") # مسافة جمالية
    st.write("") 
    check_btn = st.button("تحقق / Check", key=f"check_{q['id']}")

# --- التحقق من الإجابة ---
if check_btn:
    if user_answer == correct_letter:
        st.success(f"✅ إجابة صحيحة! الرسم ({correct_letter}) هو الصحيح.")
    else:
        st.error(f"❌ خطأ. الإجابة الصحيحة هي ({correct_letter}).")

# --- أزرار التنقل ---
st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ السابق"):
            prev_question()
            st.rerun()

with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("التالي ➡️"):
            next_question()
            st.rerun()
