st.markdown("""
<style>
    /* تنسيق عام */
    .stApp { text-align: center; }
    
    /* تنسيق البطاقة (الإطار) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
        padding: 15px;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #007bff;
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,123,255,0.1);
    }
    
    /* الحرف (A, B, C...) */
    .opt-letter {
        color: #0d6efd;
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        display: block;
        margin-bottom: 8px;
    }

    /* النص الإنجليزي */
    .opt-en {
        text-align: left;
        direction: ltr;
        font-size: 16px;
        color: #333;
        font-weight: 500;
        margin-bottom: 8px;
    }

    /* النص العربي - الحل لمشكلة التداخل */
    .opt-ar {
        text-align: right; 
        direction: rtl;
        font-size: 18px;
        color: #444;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        margin-top: 8px;
        line-height: 1.8;
    }

    /* الأزرار */
    div[data-testid="column"] .stButton button {
        width: 100%;
        border-radius: 8px;
        margin-top: 12px;
        background-color: #f8f9fa;
        border: 1px solid #ced4da;
        color: #495057;
        font-weight: bold;
    }
    div[data-testid="column"] .stButton button:hover {
        background-color: #007bff;
        color: white;
        border-color: #007bff;
    }
</style>
""", unsafe_allow_html=True)
