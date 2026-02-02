# ---------------------------------------------------------
# 4. بيانات الأسئلة (تم تحديث النصوص لتطابق صور الكتاب تماماً)
# ---------------------------------------------------------

questions = [
    {
        "id": 27,
        # النص الكامل كما في الصورة
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
        # تمت إضافة الشروط الكاملة والنقاط الحرجة
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
        # تمت إضافة شرط عدم الوجود عند الصفر
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
        # النص الكامل للنهاية والمشتقة
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
        # كتابة الفترات كاملة كما في السؤال
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
        # النص الطويل للفترات المتعددة
        "latex": r"f(0)=0, \quad f(3)=-1, \\ f'(x) < 0 \text{ for } x > 3, \\ f'(x) > 0 \text{ for } x < 0 \text{ and } 0 < x < 1 \text{ and } 1 < x < 3, \\ f'(0)=0, \quad f'(1) \text{ does not exist}, \quad f'(3)=0",
        "correct": {"func": q32_correct, "va": None},
        "distractors": [
            {"func": q32_trap_min_0, "va": None},
            {"func": q32_trap_smooth_1, "va": None},
            {"func": lambda x: -x**2 + 3*x, "va": None},
        ]
    }
]
