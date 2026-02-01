import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# ---------------------------------------------------------
# 1. Page Config & CSS Styling
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="Rational Functions Quiz")

# CSS to handle RTL for Arabic text and LTR for Math/English
# تنسيقات لضبط اتجاه النص العربي لليمين والمعادلات لليسار
st.markdown("""
<style>
    /* Default direction for the app */
    .stApp {
        direction: rtl; 
    }
    
    /* Headers and Text alignment */
    h1, h2, h3, p, div {
        text-align: right;
    }

    /* Force LaTeX/Math to be LTR */
    .katex-display, .katex {
        direction: ltr;
        text-align: center;
    }
    
    /* Radio buttons alignment */
    .stRadio > div {
        direction: rtl;
        text-align: right;
    }
    
    /* Buttons container center */
    .stButton button {
        width: 100%;
    }
    
    /* Box for the question */
    .question-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-right: 5px solid #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Session State for Pagination (One Question Per Page)
# ---------------------------------------------------------
if 'q_index' not in st.session_state:
    st.session_state.q_index = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

def next_question():
    if st.session_state.q_index < len(questions) - 1:
        st.session_state.q_index += 1

def prev_question():
    if st.session_state.q_index > 0:
        st.session_state.q_index -= 1

# ---------------------------------------------------------
# 3. Plotting Logic
# ---------------------------------------------------------
def plot_function(func, x_range=(-6, 6), vas=[], has=[], title="", correct_flag=True):
    """
    Generates a matplotlib figure for rational functions with asymptotes.
    """
    x = np.linspace(x_range[0], x_range[1], 600)
    
    # Calculate y and handle division by zero or errors
    try:
        y = func(x)
    except:
        y = np.zeros_like(x)

    # Detect discontinuities to avoid vertical connecting lines
    # كشف نقاط الانفصال لمنع توصيل الخطوط رأسياً
    threshold = 15
    y_diff = np.diff(y, prepend=y[0])
    y[np.abs(y_diff) > threshold] = np.nan
    
    # Set Y-axis limits
    y_lim = (-8, 8)
    
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Plot the function
    # رسم الدالة
    ax.plot(x, y, color='blue', linewidth=2, label='f(x)')
    
    # Plot Vertical Asymptotes
    # رسم خطوط التقارب الرأسية
    for va in vas:
        ax.axvline(x=va, color='red', linestyle='--', linewidth=1.5, alpha=0.8)
        
    # Plot Horizontal Asymptotes
    # رسم خطوط التقارب الأفقية
    for ha in has:
        ax.axhline(y=ha, color='green', linestyle='--', linewidth=1.5, alpha=0.8)
        
    # Axis styling
    ax.set_ylim(y_lim)
    ax.set_xlim(x_range)
    ax.grid(True, which='both', linestyle=':', alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    
    # Hide title to force student to look at graph features, using letter instead
    ax.set_title(title, fontsize=14, weight='bold')
    plt.tight_layout()
    
    return fig

# ---------------------------------------------------------
# 4. Question Data (Exercises 33-38)
# ---------------------------------------------------------
questions = [
    {
        "id": 33,
        "latex": r"y = \frac{x}{x^2 - 1}",
        "desc_ar": "أوجد خطوط التقارب والنهايات للدالة التالية:",
        "desc_en": "Find the asymptotes and extrema for:",
        "correct": {"func": lambda x: x / (x**2 - 1), "vas": [-1, 1], "has": [0]},
        "distractors": [
            {"func": lambda x: -x / (x**2 - 1), "vas": [-1, 1], "has": [0]}, # Sign flipped
            {"func": lambda x: x**2 / (x**2 - 1), "vas": [-1, 1], "has": [1]}, # Even function (wrong power)
            {"func": lambda x: x / (x**2 + 1), "vas": [], "has": [0]}, # No VA
        ]
    },
    {
        "id": 34,
        "latex": r"y = \frac{x^2}{x^2 - 1}",
        "desc_ar": "حلل الدالة وأختر الرسم البياني الصحيح:",
        "desc_en": "Analyze the function and choose the correct graph:",
        "correct": {"func": lambda x: x**2 / (x**2 - 1), "vas": [-1, 1], "has": [1]},
        "distractors": [
            {"func": lambda x: x / (x**2 - 1), "vas": [-1, 1], "has": [0]}, # Odd function
            {"func": lambda x: -(x**2) / (x**2 - 1), "vas": [-1, 1], "has": [-1]}, # Flipped
            {"func": lambda x: (x**2 + 1) / (x**2 - 1), "vas": [-1, 1], "has": [1]}, # Similar but different extrema
        ]
    },
    {
        "id": 35,
        "latex": r"y = \frac{x^2}{x^2 - 4x + 3}",
        "desc_ar": "تلميح: حلل المقام لمعرفة خطوط التقارب الرأسية.",
        "desc_en": "Hint: Factor the denominator to find Vertical Asymptotes.",
        "correct": {"func": lambda x: x**2 / (x**2 - 4*x + 3), "vas": [1, 3], "has": [1]},
        "distractors": [
            {"func": lambda x: x**2 / (x**2 + 4*x + 3), "vas": [-1, -3], "has": [1]}, # Wrong signs in denominator
            {"func": lambda x: -x**2 / (x**2 - 4*x + 3), "vas": [1, 3], "has": [-1]}, # Flipped
            {"func": lambda x: (x-1.5)**2 / ((x-1)*(x-3)), "vas": [1, 3], "has": [1]}, # Shifted parabola
        ]
    },
    {
        "id": 36,
        "latex": r"y = \frac{x}{1 - x^4}",
        "desc_ar": "انتبه لإشارة المقام.",
        "desc_en": "Pay attention to the denominator sign.",
        "correct": {"func": lambda x: x / (1 - x**4), "vas": [-1, 1], "has": [0]},
        "distractors": [
            {"func": lambda x: x / (x**4 - 1), "vas": [-1, 1], "has": [0]}, # Sign flipped (x^4 - 1)
            {"func": lambda x: x**2 / (1 - x**4), "vas": [-1, 1], "has": [0]}, # Even function
            {"func": lambda x: x / (1 + x**4), "vas": [], "has": [0]}, # No VA
        ]
    },
    {
        "id": 37,
        "latex": r"y = \frac{x}{\sqrt{x^2 + 1}}",
        "desc_ar": "هذه الدالة لها سلوك مختلف في اللانهاية الموجبة والسالبة.",
        "desc_en": "This function behaves differently at positive/negative infinity.",
        "correct": {"func": lambda x: x / np.sqrt(x**2 + 1), "vas": [], "has": [1, -1]},
        "distractors": [
            {"func": lambda x: 1 / (x**2 + 1), "vas": [], "has": [0]}, # Bell curve
            {"func": lambda x: x**2 / np.sqrt(x**2 + 1), "vas": [], "has": []}, # Parabolic like
            {"func": lambda x: x / (x**2 + 1), "vas": [], "has": [0]}, # Approaches 0 both sides
        ]
    },
    {
        "id": 38,
        "latex": r"y = \frac{x^2 + 2}{(x + 1)^2}",
        "desc_ar": "لاحظ أن المقام مربع كامل.",
        "desc_en": "Note that the denominator is a perfect square.",
        "correct": {"func": lambda x: (x**2 + 2) / (x + 1)**2, "vas": [-1], "has": [1]},
        "distractors": [
            {"func": lambda x: (x**2 + 2) / (x - 1)**2, "vas": [1], "has": [1]}, # Shifted VA to +1
            {"func": lambda x: -(x**2 + 2) / (x + 1)**2, "vas": [-1], "has": [-1]}, # Flipped
            {"func": lambda x: x / (x + 1)**2, "vas": [-1], "has": [0]}, # Degree num < Degree den
        ]
    }
]

# ---------------------------------------------------------
# 5. Rendering the App
# ---------------------------------------------------------

# Title / العنوان
st.title("🔢 Calculus: Graphing Rational Functions")
st.subheader("التفاضل: رسم الدوال النسبية (تمارين 33-38)")
st.markdown("---")

# Get current question
q_idx = st.session_state.q_index
q = questions[q_idx]

# --- Progress Bar / شريط التقدم ---
progress = (q_idx + 1) / len(questions)
st.progress(progress)
st.caption(f"Question {q_idx + 1} of {len(questions)}")

# --- Display Question / عرض السؤال ---
st.markdown(f"""
<div class="question-box">
    <h3>سؤال رقم {q['id']} / Question {q['id']}</h3>
    <p><strong>{q['desc_ar']}</strong><br><span style="color:gray">{q['desc_en']}</span></p>
</div>
""", unsafe_allow_html=True)

# Display Math Equation in Center
st.latex(q['latex'])

# --- Prepare Options (Graphs) / تجهيز الخيارات ---
# We use caching or seed to make sure options don't shuffle on every simple interaction
# unless the question changes.
random.seed(q['id']) 

options_data = []
# Add Correct Option
options_data.append({
    "type": "correct",
    "fig": plot_function(q["correct"]["func"], vas=q["correct"]["vas"], has=q["correct"]["has"])
})
# Add Wrong Options
for dist in q["distractors"]:
    options_data.append({
        "type": "wrong",
        "fig": plot_function(dist["func"], vas=dist["vas"], has=dist["has"])
    })

# Shuffle options
random.shuffle(options_data)

# --- Display Graphs in Grid / عرض الرسوم ---
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
cols_list = [col1, col2, col3, col4]
letters = ['A', 'B', 'C', 'D']
correct_letter = None

for idx, opt_data in enumerate(options_data):
    letter = letters[idx]
    with cols_list[idx]:
        # Add title to the figure before showing
        opt_data["fig"].axes[0].set_title(f"Option ({letter})", color='maroon')
        st.pyplot(opt_data["fig"])
        if opt_data["type"] == "correct":
            correct_letter = letter

# --- User Input Section / منطقة الإجابة ---
st.markdown("---")
col_input, col_action = st.columns([2, 1])

with col_input:
    user_answer = st.radio(
        "اختر الرسم البياني الصحيح / Select the correct graph:",
        letters,
        key=f"radio_{q['id']}",
        horizontal=True
    )

with col_action:
    st.write("") # Spacer
    st.write("") # Spacer
    check_btn = st.button("تحقق من الإجابة / Check Answer", key=f"check_{q['id']}")

# --- Logic for checking answer / منطق التحقق ---
if check_btn:
    if user_answer == correct_letter:
        st.success(f"✅ Correct! Option {correct_letter} is the right graph.")
        st.balloons()
    else:
        st.error(f"❌ Incorrect. The correct graph is {correct_letter}.")
        with st.expander("Show Explanation / عرض الشرح"):
            st.write(f"**Function:** {q['latex']}")
            st.write(f"**Vertical Asymptotes:** {q['correct']['vas']}")
            st.write(f"**Horizontal Asymptotes:** {q['correct']['has']}")
            st.write("تحقق من أصفار المقام لمعرفة خطوط التقارب الرأسية، ودرجة البسط والمقام للأفقية.")

# --- Navigation Buttons / أزرار التنقل ---
st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    if st.session_state.q_index > 0:
        if st.button("⬅️ السابق / Previous"):
            prev_question()
            st.rerun()

with c3:
    if st.session_state.q_index < len(questions) - 1:
        if st.button("التالي / Next ➡️"):
            next_question()
            st.rerun()
