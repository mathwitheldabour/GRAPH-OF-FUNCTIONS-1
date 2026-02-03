# ... (بعد كود الرسم البياني مباشرة) ...

st.write("---")

# خلط الخيارات
seed_val = q_idx + int(q_data['func'](0)*100)
random.seed(seed_val)
options_list = []
options_list.append({**q_data['correct'], "is_correct": True})
for dist in q_data['distractors']:
    options_list.append({**dist, "is_correct": False})
random.shuffle(options_list)

# عرض الخيارات في 4 أعمدة
cols = st.columns(4)
letters = ['A', 'B', 'C', 'D']
option_map = {}

for idx, col in enumerate(cols):
    opt = options_list[idx]
    letter = letters[idx]
    option_map[letter] = opt
    
    with col:
        # استخدام الحاوية لعمل الإطار
        with st.container(border=True):
            # الحرف A, B, C
            st.markdown(f"<span class='opt-letter'>{letter}</span>", unsafe_allow_html=True)
            
            # النص الإنجليزي
            st.markdown(f"<div class='opt-en'>{opt['en']}</div>", unsafe_allow_html=True)
            
            # خط فاصل خفيف
            st.markdown("---")
            
            # النص العربي (تم ضبطه بالـ CSS ليكون RTL)
            st.markdown(f"<div class='opt-ar'>{opt['ar']}</div>", unsafe_allow_html=True)
            
            # الزر
            if st.button(f"Choose {letter}", key=f"btn_{q_idx}_{letter}"):
                check_answer(letter)

# ... (بقية كود التحقق والأزرار كما هو) ...
