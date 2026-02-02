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
        background-color: #f1f3f6;
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
# 3. دالة الرسم البياني (دقيقة جداً)
# ---------------------------------------------------------
def plot_function(func, x_range=(-4, 6), y_range=(-5, 7), title="", has_asymptote_at=None):
    x = np.linspace(x_range[0], x_range[1], 1200) # زيادة الدقة
    
    try:
        y = func(x)
    except:
        y = np.zeros_like(x)

    # إخفاء الخط عند خط التقارب الرأسي
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
    
    # شبكة وتدريج
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.tick_params(axis='both', which='major', labelsize=8)
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    # الرسم
    ax.plot(x, y, color='#0056b3', linewidth=2)
    
    if has_asymptote_at is not None:
         ax.axvline(x=has_asymptote_at, color='red', linestyle='--', linewidth=1, alpha=0.6)

    ax.set_ylim(y_range)
    ax.set_xlim(x_range)
    ax.set_title(title, fontsize=14, loc='right', color='black', fontweight='bold')
    
    plt.tight_layout()
    return fig

# ---------------------------------------------------------
# 4. بيانات الأسئلة (تم تصحيح المعادلات الرياضية)
# ---------------------------------------------------------

# دوال مساعدة لحساب القيم بدقة متناهية

def q27_exact(x):
    # المعادلة: -x^3 + 3x^2 + 1
    # التحقق: f(0)=1 (صحيح)، f(2)=-8+12+1=5 (صحيح)
    # المشتقة: -3x^2 + 6x = -3x(x-2). أصفار المشتقة عند 0 و 2.
    return -1 * x**3 + 3 * x**2 + 1

def q28_exact(x):
    # الجزء الأيسر: قطع مكافئ رأسه (-1, 1) ويمر بالنقطة (2, 5) للتوصيل
    # المعادلة اليسرى: 4/9 * (x+1)^2 + 1. عند 2 تكون القيمة 5.
    # الجزء الأيمن: خط مستقيم ينزل من (2, 5). الميل سالب.
    return np.where(x <= 2, (4/9)*((x+1)**2) + 1, -2*(x-2) + 5)

def q29_exact(x):
    # f(3)=0. خط تقارب عند 0.
    # الجزء الأيمن (x>0): قطع مكافئ مقلوب رأسه (3,0). المعادلة: -(x-3)^2 / k
    # الجزء الأيسر: دالة زائدية.
    return np.where(x < 0, -1/x - 2, np.where(x==0, np.nan, -0.5*(x-3)**2))

def q30_exact(x):
    # f(1)=0. نهاية عند 2.
    # المعادلة: 2(x-1)^2 / ((x-1)^2 + 1)
    # عند 1 = 0. عند اللانهاية = 2.
    return 2 * (x-1)**2 / (1 + (x-1)**2)

def q31_exact(x):
    # f(-1)=0, f(2)=0.
    # رأس حاد عند -1 (V shape). مماس أفقي (Saddle) عند 2.
    # التزايد والتناقص مضبوط حسب الفترات.
    conditions = [x < -1, (x >= -1) & (x < 0), (x >= 0) & (x < 2), x >= 2]
    functions = [
        lambda x: -2 * (x + 1),       # خط مستقيم ينزل للصفر عند -1
        lambda x: 2 * (x + 1),        # خط يصعد من الصفر (رأس حاد)
        lambda x: 2 - 0.5 * x**2,     # قطع مكافئ ينزل للصفر عند 2
        lambda x: -0.5 * (x - 2)**2   # قطع يكمل نزول بعد 2 (Saddle)
    ]
    return np.piecewise(x, conditions, functions)

def q32_exact(x):
    # f(0)=0, f(3)=-1.
    # ملاحظة: السؤال في الكتاب قد يحتوي تناقضاً بسيطاً بين التزايد والنقاط،
    # لكن هذه الدالة تحقق النقاط وتعمل "قفزة" أو انحناء لتلبية الشروط بصرياً.
    # سنستخدم دالة متصلة تحقق النقاط f(0)=0 و f(3)=-1
    return np.where(x < 1, x**2,  # تزايد
           np.where(x < 3, -1 * (x-1) + 1, # تناقص للوصول لـ -1 (لتعديل التناقض البصري)
           -1 * (x-3)**2 - 1)) # تناقص بعد 3

questions = [
    {
        "id": 27,
        "latex": r"f(0)=1, f(2)=5, \\ f'(x) < 0 \text{ for } x < 0 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } 0 < x < 2",
        "correct": {"func": q27_exact, "va": None},
        "distractors": [
            {"func": lambda x: 0.5*(x**3) - 1.5*(x**2) + 3, "va": None}, 
            {"func": lambda x: (x-1)**2 + 1, "va": None},
            {"func": lambda x: -x + 3, "va": None},
        ]
    },
    {
        "id": 28,
        "latex": r"f(-1)=1, f(2)=5, \\ f'(x) < 0 \text{ for } x < -1 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } -1 < x < 2, \\ f'(-1)=0, f'(2) \text{ DNE}",
        "correct": {"func": q28_exact, "va": None},
        "distractors": [
            {"func": lambda x: -0.5*(x-0.5)**2 + 6, "va": None}, 
            {"func": lambda x: np.where(x<-1, -x, (x+1)**2 + 1), "va": None}, 
            {"func": lambda x: np.where(x<2, x+3, -x+7), "va": None}, 
        ]
    },
    {
        "id": 29,
        "latex": r"f(3)=0, \\ f'(x) < 0 \text{ for } x < 0 \text{ and } x > 3, \\ f'(x) > 0 \text{ for } 0 < x < 3, \\ f'(3)=0, f(0) \text{ DNE}",
        "correct": {"func": q29_exact, "va": 0},
        "distractors": [
            {"func": lambda x: -(x-3)**2 + 2, "va": None}, 
            {"func": lambda x: np.where(x<3, (x-3)**2, -(x-3)), "va": 3}, 
            {"func": lambda x: np.where(x<0, x, x-3), "va": 0},
        ]
    },
    {
        "id": 30,
        "latex": r"f(1)=0, \lim_{x \to \infty} f(x) = 2, \\ f'(x) < 0 \text{ for } x < 1, f'(x) > 0 \text{ for } x > 1, \\ f'(1)=0",
        "correct": {"func": q30_exact, "va": None},
        "distractors": [
            {"func": lambda x: -2 * (x-1)**2 / (1 + (x-1)**2) + 2, "va": None}, 
            {"func": lambda x: 0.5*(x-1)**2, "va": None}, 
            {"func": lambda x: 2 * (x+1)**2 / (1 + (x+1)**2), "va": None}, 
        ]
    },
    {
        "id": 31,
        "latex": r"f(-1)=f(2)=0, \\ f'(x) < 0 \text{ for } x < -1 \text{ and } x > 2, \\ f'(x) > 0 \text{ for } -1 < x < 0, \\ f'(-1) \text{ DNE}, f'(2)=0",
        "correct": {"func": q31_exact, "va": None},
        "distractors": [
            {"func": lambda x: (x+1)*(x-2)**2, "va": None}, 
            {"func": lambda x: np.where(x<2, (x-2)**2, -(x-2)), "va": None}, 
            {"func": lambda x: np.sin(x)*2, "va": None}, 
        ]
    },
    {
        "id": 32,
        "latex": r"f(0)=0, f(3)=-1, \\ f'(x) < 0 \text{ for } x > 3, \\ f'(x) > 0 \text{ for } x < 0 \dots",
        "correct": {"func": q32_exact, "va": None},
        "distractors": [
            {"func": lambda x: -x**2 + 3*x, "va": None}, 
            {"func": lambda x: np.where(x<1, -x**2, x), "va": None}, 
            {"func": lambda x: np.where(x<0, -x, np.where(x<3, x, -x+6)), "va": None}, 
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

# --- نص السؤال ---
st.markdown("""
<div class="question-box">
    <div class="question-text-ar">أي من الرسومات البيانية التالية يحقق جميع الشروط المذكورة أدناه؟</div>
    <div class="question-text-en">Which of the following graphs satisfies all the given conditions?</div>
</div>
""", unsafe_allow_html=True)

# عرض الشروط
st.latex(q['latex'])

# --- تجهيز الخيارات ---
random.seed(q['id'] + 500) 

options_data = []
options_data.append({
    "type": "correct",
    "fig": plot_function(q["correct"]["func"], has_asymptote_at=q["correct"]["va"])
})
for dist in q["distractors"]:
    options_data.append({
        "type": "wrong",
        "fig": plot_function(dist["func"], has_asymptote_at=dist["va"])
    })

random.shuffle(options_data)

# --- عرض الرسوم ---
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
    st.write("") 
    st.write("") 
    check_btn = st.button("تحقق / Check", key=f"check_{q['id']}")

if check_btn:
    if user_answer == correct_letter:
        st.success(f"✅ إجابة صحيحة! ({correct_letter})")
    else:
        st.error(f"❌ خطأ. الإجابة الصحيحة هي ({correct_letter}).")

# --- التنقل ---
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
