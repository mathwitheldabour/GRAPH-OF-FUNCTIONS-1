import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random

# إعداد الصفحة لتكون واسعة وتدعم الكتابة من اليمين لليسار
st.set_page_config(layout="wide", page_title="اختبار الدوال النسبية")

# CSS بسيط لضبط اتجاه النص للعربية
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        text-align: right;
    }
    div[data-testid="stRadio"] > label {
        float: right;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

st.title("اختبار الرسم البياني للدوال (تمارين 33-38)")
st.write("اختر الرسم البياني الصحيح الذي يمثل الدالة المعطاة. انتبه لخطوط التقارب والنهايات.")

# --- دوال مساعدة للرسم ---

def plot_function(func, x_range=(-6, 6), vas=[], has=[], title="", correct=True):
    """
    تقوم هذه الدالة برسم الدالة الرياضية مع معالجة خطوط التقارب
    """
    x = np.linspace(x_range[0], x_range[1], 400)
    y = func(x)
    
    # إزالة الخطوط الواصلة عند خطوط التقارب الرأسية (Discontinuities)
    # أي نقطة يكون فيها الفرق بين قيمتين متتاليتين كبير جداً نعتبرها انقطاع
    threshold = 10
    y_diff = np.diff(y)
    y[:-1][np.abs(y_diff) > threshold] = np.nan
    
    # تحديد نطاق الرسم الصادي ليكون الرسم نظيفاً
    y_lim = (-8, 8)
    
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y, label='الدالة', color='blue' if correct else 'red', linewidth=1.5)
    
    # رسم خطوط التقارب الرأسية (Vertical Asymptotes)
    for va in vas:
        ax.axvline(x=va, color='green', linestyle='--', alpha=0.7, label=f'x={va}')
        
    # رسم خطوط التقارب الأفقية (Horizontal Asymptotes)
    for ha in has:
        ax.axhline(y=ha, color='orange', linestyle='--', alpha=0.7, label=f'y={ha}')
        
    ax.set_ylim(y_lim)
    ax.set_xlim(x_range)
    ax.grid(True, alpha=0.3)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_title(title, fontsize=10)
    
    # إزالة الإطار الزائد
    plt.tight_layout()
    return fig

# --- تعريف الأسئلة والخيارات المضللة ---

# سنقوم بتعريف الدوال كـ Lambda functions
# كل سؤال يحتوي على: المعادلة (latex)، الدالة الصحيحة ومعلوماتها، ودوال خاطئة للتمويه

questions = [
    {
        "id": 33,
        "latex": r"y = \frac{x}{x^2 - 1}",
        "correct": {
            "func": lambda x: x / (x**2 - 1),
            "vas": [-1, 1], "has": [0]
        },
        "distractors": [
            {"func": lambda x: -x / (x**2 - 1), "vas": [-1, 1], "has": [0]}, # معكوسة الإشارة
            {"func": lambda x: x**2 / (x**2 - 1), "vas": [-1, 1], "has": [1]}, # دالة زوجية بدل فردية
            {"func": lambda x: x / (x**2 + 1), "vas": [], "has": [0]}, # لا يوجد تقارب رأسي
        ]
    },
    {
        "id": 34,
        "latex": r"y = \frac{x^2}{x^2 - 1}",
        "correct": {
            "func": lambda x: x**2 / (x**2 - 1),
            "vas": [-1, 1], "has": [1]
        },
        "distractors": [
            {"func": lambda x: x / (x**2 - 1), "vas": [-1, 1], "has": [0]}, # دالة فردية
            {"func": lambda x: -x**2 / (x**2 - 1), "vas": [-1, 1], "has": [-1]}, # مقلوبة
            {"func": lambda x: x**2 / (x**2 + 1), "vas": [], "has": [1]}, # المقام مجموع مربعين (لا أصفار)
        ]
    },
    {
        "id": 35,
        "latex": r"y = \frac{x^2}{x^2 - 4x + 3}",
        "note": r"Hint: $x^2 - 4x + 3 = (x-1)(x-3)$",
        "correct": {
            "func": lambda x: x**2 / (x**2 - 4*x + 3),
            "vas": [1, 3], "has": [1]
        },
        "distractors": [
            {"func": lambda x: x**2 / (x**2 + 4*x + 3), "vas": [-1, -3], "has": [1]}, # خطوط التقارب في السالب
            {"func": lambda x: -x**2 / (x**2 - 4*x + 3), "vas": [1, 3], "has": [-1]}, # مقلوبة
            {"func": lambda x: (x-2) / (x**2 - 4*x + 3), "vas": [1, 3], "has": [0]}, # تقارب أفقي 0
        ]
    },
    {
        "id": 36,
        "latex": r"y = \frac{x}{1 - x^4}",
        "correct": {
            "func": lambda x: x / (1 - x**4),
            "vas": [-1, 1], "has": [0]
        },
        "distractors": [
            {"func": lambda x: x / (x**4 - 1), "vas": [-1, 1], "has": [0]}, # عكس الإشارة (المقام معكوس)
            {"func": lambda x: x**2 / (1 - x**4), "vas": [-1, 1], "has": [0]}, # دالة زوجية
            {"func": lambda x: x / (1 + x**4), "vas": [], "has": [0]}, # لا تقارب رأسي
        ]
    },
    {
        "id": 37,
        "latex": r"y = \frac{x}{\sqrt{x^2 + 1}}",
        "correct": {
            "func": lambda x: x / np.sqrt(x**2 + 1),
            "vas": [], "has": [1, -1] # تقارب أفقي عند 1 و -1
        },
        "distractors": [
            {"func": lambda x: x**2 / np.sqrt(x**2 + 1), "vas": [], "has": []}, # يشبه القطع المكافئ
            {"func": lambda x: 1 / np.sqrt(x**2 + 1), "vas": [], "has": [0]}, # الجرس المقلوب
            {"func": lambda x: -x / np.sqrt(x**2 + 1), "vas": [], "has": [1, -1]}, # معكوسة
        ]
    },
    {
        "id": 38,
        "latex": r"y = \frac{x^2 + 2}{(x + 1)^2}",
        "correct": {
            "func": lambda x: (x**2 + 2) / (x + 1)**2,
            "vas": [-1], "has": [1]
        },
        "distractors": [
            {"func": lambda x: (x**2 + 2) / (x - 1)**2, "vas": [1], "has": [1]}, # تقارب رأسي عند 1
            {"func": lambda x: -(x**2 + 2) / (x + 1)**2, "vas": [-1], "has": [-1]}, # مقلوبة
            {"func": lambda x: (x) / (x + 1)**2, "vas": [-1], "has": [0]}, # درجة البسط أقل من المقام
        ]
    }
]

# --- عرض التطبيق ---

for i, q in enumerate(questions):
    st.markdown("---")
    st.subheader(f"سؤال {q['id']}")
    
    # عرض الدالة
    st.latex(q['latex'])
    if "note" in q:
        st.caption(q["note"])
    
    # تجهيز الخيارات (1 صحيح + 3 خطأ)
    options = []
    
    # الخيار الصحيح
    options.append({
        "type": "correct", 
        "fig": plot_function(q["correct"]["func"], vas=q["correct"]["vas"], has=q["correct"]["has"], title="الخيار A")
    })
    
    # الخيارات الخاطئة (نعطيها أحرف B, C, D مبدئياً ثم نخلط)
    labels = ["B", "C", "D"]
    for idx, dist in enumerate(q["distractors"]):
        title = f"الخيار {labels[idx]}"
        options.append({
            "type": "wrong",
            "fig": plot_function(dist["func"], vas=dist["vas"], has=dist["has"], title=title)
        })
    
    # خلط الخيارات عشوائياً حتى لا تكون الإجابة دائماً A
    # نستخدم مفتاح ثابت (Seed) لثبات الخيارات عند إعادة التحميل إلا إذا أردنا تغييرها
    random.seed(i) 
    random.shuffle(options)
    
    # إعادة تسمية العناوين بعد الخلط (أ، ب، ج، د)
    chars = ['أ', 'ب', 'ج', 'د']
    correct_char = ""
    
    cols = st.columns(4)
    for idx, opt in enumerate(options):
        # تحديث عنوان الرسم ليتوافق مع العمود
        opt["fig"].axes[0].set_title(f"الخيار ({chars[idx]})", fontsize=14)
        
        # عرض الرسم في العمود
        with cols[idx]:
            st.pyplot(opt["fig"])
        
        # حفظ الحرف الصحيح للمقارنة
        if opt["type"] == "correct":
            correct_char = chars[idx]

    # قائمة الاختيار
    user_choice = st.radio(
        f"اختر الرسم البياني الصحيح للدالة رقم {q['id']}:",
        chars,
        key=f"q_{q['id']}",
        horizontal=True
    )
    
    # زر التحقق
    if st.button(f"تحقق من إجابة السؤال {q['id']}", key=f"btn_{q['id']}"):
        if user_choice == correct_char:
            st.success(f"أحسنت! الإجابة ({correct_char}) صحيحة.")
        else:
            st.error(f"إجابة خاطئة. الإجابة الصحيحة هي ({correct_char}).")
            
    # شرح بسيط (اختياري)
    with st.expander("عرض تلميح للحل"):
        st.write("تذكر القواعد التالية:")
        st.write("1. **خط التقارب الرأسي (Vertical Asymptote):** يحدث عندما يساوي المقام صفرًا.")
        st.write("2. **خط التقارب الأفقي (Horizontal Asymptote):** يعتمد على درجة البسط والمقام.")
        st.write("- إذا كانت درجة البسط = درجة المقام، نقسم المعاملات الرئيسية.")
        st.write("- إذا كانت درجة البسط < درجة المقام، الخط هو y=0.")
        st.write("- إذا كانت درجة البسط > درجة المقام، لا يوجد خط أفقي (قد يكون مائلاً).")