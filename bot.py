{# =========================================================
# 💙 مشروع دروب آمنة - الإصدار الذكي المبهر 💙
# 👩‍💻 Developed by: أريام الشافعي
# =========================================================

import gradio as gr
import webbrowser
import string
import re
from difflib import get_close_matches
from datetime import datetime
import google.generativeai as genai

# ============================
# 1️⃣ إعداد Gemini API
# ============================

GEMINI_API_KEY_DIRECT = "AIzaSyBd8j6f-SoI5EtC33zJUesGufU9fk9E7O8"

try:
    if GEMINI_API_KEY_DIRECT and GEMINI_API_KEY_DIRECT != "YOUR_GEMINI_API_KEY_HERE":
        genai.configure(api_key=GEMINI_API_KEY_DIRECT)
        GEMINI_MODEL = "gemini-2.5-flash"
        GEMINI_ENABLED = True
        print("✅ Gemini client initialized successfully.")
    else:
        GEMINI_ENABLED = False
except Exception as e:
    print(f"⚠️ Failed to initialize Gemini client: {e}")
    GEMINI_ENABLED = False

def call_gemini_api(prompt):
    if not GEMINI_ENABLED:
        return "Gemini API غير مفعّل."
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"حدث خطأ أثناء استدعاء Gemini: {e}"

# ============================
# 2️⃣ روابط الصور وواتساب
# ============================

IMAGE_URLS = {
    "library": "images/library.jpg",
    "cafeteria": "images/cafeteria.jpg",
    "gate_clinic": "images/gate_clinic.jpg",
    "trainer_offices": "images/trainer_offices.jpg",
    "gate_main": "images/gate_main.jpg",
    "gate_classrooms": "images/gate_classrooms.jpg",
    "parking_front": "images/parking_front.jpg",
    "parking_back": "images/parking_back.jpg"
}

whatsapp_link = "https://wa.me/qr/YQ5U5MAW36FAP1"

def launch_whatsapp_button():
    webbrowser.open_new_tab(whatsapp_link)
    return None

# ============================
# 🚪 المواقف والبوابات التفاعلية بالصور
# ============================

PLACES_EXTENDED = {
    "المواقف": {
        "desc": "🚗 توجد مواقف أمامية وخلفية في الكلية.\nاختاري أحدها:\n1️⃣ المواقف الأمامية\n2️⃣ المواقف الخلفية",
        "options": ["المواقف الأمامية", "المواقف الخلفية"]
    },
    "بوابات": {
        "desc": "🚪 توجد 3 بوابات في الكلية:\n1️⃣ البوابة الرئيسية 👑\n2️⃣ بوابة القاعات 📚\n3️⃣ بوابة العيادة 🏥\nاختاري رقم البوابة لمعرفة التفاصيل.",
        "options": ["بوابة 1", "بوابة 2", "بوابة 3"]
    }
}

GATE_DETAILS = {
    "بوابة 1": "👑 **البوابة الرئيسية**: المدخل الأساسي للكلية، فيها حارسة الأمن.\n[صورة: gate_main]",
    "بوابة 2": "📚 **بوابة القاعات**: قريبة من الفصول النظرية.\n[صورة: gate_classrooms]",
    "بوابة 3": "🏥 **بوابة العيادة**: تؤدي مباشرة للعيادة الطبية.\n[صورة: gate_clinic]"
}

PARKING_DETAILS = {
    "المواقف الأمامية": "🚘 **المواقف الأمامية**: أمام المبنى الرئيسي، مهيأة لذوي الاحتياجات الخاصة.\n[صورة: parking_front]",
    "المواقف الخلفية": "🚗 **المواقف الخلفية**: خلف مبنى القاعات، مناسبة للموظفات والزائرات.\n[صورة: parking_back]"
}

def get_extended_place(message):
    message = message.strip()
    if message in PLACES_EXTENDED:
        return PLACES_EXTENDED[message]["desc"]
    elif message in GATE_DETAILS:
        return GATE_DETAILS[message]
    elif message in PARKING_DETAILS:
        return PARKING_DETAILS[message]
    return None

# ============================
# 3️⃣ رسالة الترحيب
# ============================

def get_welcome_message():
    hour = datetime.now().hour
    greeting = "صباح الخير 🌸" if hour < 12 else "مساء الخير 🌙"

    return [
        {"role": "assistant", "content": f"""
{greeting}! أهلاً بكِ في **دروب آمنة 💙**  
أنا مرشدتك الآلية، أساعدك في التنقل داخل الكلية بسهولة ويسر 🌟  
اسألي أي سؤال أو اختاري من الأزرار بالأسفل 👇  
"""}
    ]

# ============================
# 4️⃣ دوال مساعدة
# ============================

def format_answer_with_images(answer_text):
    def replace_tag(match):
        image_key = match.group(1).strip()
        image_url = IMAGE_URLS.get(image_key)
        if image_url:
            return f"\n\n<div style='text-align:center;'>" \
                   f"<img src='{image_url}' alt='صورة' style='width:80%; border-radius:16px; box-shadow:0 0 10px #b3d1ff;'/>" \
                   f"</div>\n"
        else:
            return match.group(0)
    return re.sub(r'\[صورة: ([\w_]+)\]', replace_tag, answer_text)

# ============================
# 🧭 الأماكن العامة والمسارات الذكية
# ============================

PLACES = {
    "المسرح": {"floor": "الأرضي", "desc": "🎭 المسرح في الدور الأرضي قرب البوابة الرئيسية.", "accessible": True},
    "الكافتيريا": {"floor": "الأرضي", "desc": "☕️ الكافتيريا بالدور الأرضي بجانب السلالم.", "accessible": True},
    "مكاتب الإدارة": {"floor": "الأرضي", "desc": "🏢 مكاتب الإدارة عند مدخل الكلية.", "accessible": True},
    "المكتبة": {"floor": "الأول", "desc": "📚 المكتبة في الدور الأول مقابل المصعد.", "accessible": True},
    "العيادة": {"floor": "الأرضي", "desc": "🏥 العيادة الطبية قرب المسرح.", "accessible": True},
    "الإرشاد الأكاديمي": {"floor": "الأول", "desc": "🧭 مكتب الإرشاد الأكاديمي في الدور الأول بجانب المكتبة.", "accessible": True},
    "ساحة المدربات": {"floor": "الثاني", "desc": "👩‍🏫 ساحة المدربات في الدور الثاني، تجمع معظم مكاتب المدربات.", "accessible": True}
}

ROUTES = {
    ("المسرح", "الكافتيريا"): "🚶‍♀️ من المسرح اتجهي يمينًا عبر الممر حتى تصلي إلى الكافتيريا.",
    ("الكافتيريا", "المكتبة"): "📚 اصعدي بالمصعد إلى الدور الأول، المكتبة أمامك مباشرة.",
    ("المكتبة", "الإرشاد الأكاديمي"): "🧭 مكتب الإرشاد بجانب المكتبة في نفس الدور.",
    ("العيادة", "مكاتب الإدارة"): "🏢 من العيادة اتجهي يسارًا إلى نهاية الممر لتصلي إلى مكاتب الإدارة.",
    ("الكافتيريا", "ساحة المدربات"): "☕️ من الكافتيريا اصعدي بالمصعد إلى الدور الثاني لتجدي ساحة المدربات.",
    ("المكتبة", "ساحة المدربات"): "📚 من المكتبة اتجهي يمينًا إلى المصعد ثم إلى الدور الثاني، ستجدين ساحة المدربات أمامك.",
    ("ساحة المدربات", "المكتبة"): "⬇️ من ساحة المدربات استخدمي المصعد للنزول إلى الدور الأول، المكتبة أمامك."
}

FLOOR_MAP = {"1": "الأرضي", "2": "الأول", "3": "الثاني"}
SECTION_MAP = {"A": "القسم الأول", "B": "القسم الثاني", "C": "القسم الثالث"}

def detect_classroom(text):
    text = text.upper()
    match = re.search(r"([1-3])([ABC])([0-9]{2,3})", text)
    if match:
        floor, sec, num = match.groups()
        return f"📘 الكلاس في {FLOOR_MAP[floor]} – {SECTION_MAP[sec]} – رقم {num}."
    return None

# ============================
# 6️⃣ قاعدة المعرفة
# ============================

faq = {
    "مواقف": ("🌸 نعم، المواقف متوفرة. 1. الأمامية 🚪 2. الخلفية 📚", "AWAITING_PARKING_CHOICE"),
    "بوابات": ("🚪 تتوفر 3 بوابات. 1. الرئيسية 👑 2. القاعات 📚 3. العيادة 🏥", "AWAITING_GATE_CHOICE"),
    "مطعم_وكوفي": ("☕️ المطاعم: 1. الكافتيريا (أرضي) 🖼️ [صورة: cafeteria] 2. المقهى (أول)", "AWAITING_FOOD_CHOICE"),
    "تنقل": ("💙 يمكنك التنقل بسهولة عن طريق المصاعد والمنحدرات.", None),
    "حمامات": ("🚻 دورات المياه متوفرة في المبنى.", None),
    "قاعات": ("📚 القاعات تشمل الأرضي وبعض القاعات مهيأة.", None),
    "مصاعد": ("⬆️ المصاعد متوفرة في كل المباني.", None),
    "تواصل": ("🤝 تواصل مع الإدارة عبر مكتب شؤون الطلاب أو المرشد الأكاديمي.", None),
    "العيادة_الطبية": ("🏥 العيادة بالدور الأرضي 🖼️ [صورة: gate_clinic]", None),
    "مكاتب_الإدارة_الرئيسية": ("🏢 مكاتب الإدارة بالدور الأرضي.", None),
    "المسرح": ("🎬 المسرح بالدور الأرضي 🖼️ [صورة: gate_main]", None),
    "المكتبة_الرئيسية": ("📚 المكتبة بالدور الأول 🖼️ [صورة: library]", None),
    "قاعة_متعددة": ("🎭 القاعة المتعددة بالدور الأرضي.", None),
    "قاعة_الفهيد": ("👑 قاعة الفهيد بالدور الأول.", None),
    "المكتبة_المالية": ("💰 المكتبة المالية بالدور الأرضي 🖼️ [صورة: financial_library]", None),
    "الإرشاد": ("🧭 مكتب الإرشاد بالدور الأول 🖼️ [صورة: guidance_office]", None),
    "حارسة_الأمن": ("🛡️ حارسة الأمن عند البوابة الرئيسية 🖼️ [صورة: security_guard]", None),
    "مكاتب_المدربات": ("👩‍🏫 مكاتب المدربات بالدور الثاني 🖼️ [صورة: trainer_offices]", None),
    "مساعدة": (f"💡 اضغطي الزر للتواصل عبر واتساب: [📲 واتساب]({whatsapp_link})", None)
}

synonym_map = {
    "مواقف": ["موقف", "سيارات"],
    "بوابات": ["بوابة", "مدخل"],
    "مصاعد": ["مصعد", "اسنسير"],
    "مطعم_وكوفي": ["كافتيريا", "مطعم", "كوفي"],
    "مكاتب_المدربات": ["مدربات", "مكتب المدربة", "ساحة المدربات"],
    "مساعدة": ["مساعدة", "دعم", "مشكلة"]
}

# ============================
# 7️⃣ دالة المحادثة الوحيدة
# ============================

def clean_text(text):
    return text.lower().translate(str.maketrans('', '', string.punctuation))

def get_keyword(user_input):
    user_text = clean_text(user_input)
    for main_keyword, synonyms in synonym_map.items():
        if any(term in user_text for term in [main_keyword] + synonyms):
            return main_keyword, None
    match = get_close_matches(user_text, list(faq.keys()), n=1, cutoff=0.7)
    return (match[0], None) if match else (None, None)

def chat(message, history, user_session):
    try:
        history = history or get_welcome_message()
        user_session = user_session or {"state": "NORMAL"}
        user_message_log = message or ""

        if not message or str(message).strip() == "":
            return history, history, user_session, "", None

        message = str(message)
        keyword, _ = get_keyword(message)
        answer = ""

        # 🎯 التحقق من المواقف أو البوابات
        extended_response = get_extended_place(message)
        if extended_response:
            answer = extended_response

        # 🧭 التحقق من الأماكن العامة
        src, dest = detect_place_route(message)
        if dest:
            if src and (src, dest) in ROUTES:
                answer = ROUTES[(src, dest)]
            else:
                place_info = get_place_info(dest)
                if place_info:
                    answer = place_info

        # 💬 لو ما طلع رد من الأعلى
        if not answer:
            if keyword in faq:
                answer = faq[keyword][0]
            else:
                answer = call_gemini_api(message)

        if not isinstance(answer, str):
            answer = str(answer)

        final_bot_answer = format_answer_with_images(answer)

        gradio_history_format = history + [
            {"role": "user", "content": user_message_log},
            {"role": "assistant", "content": final_bot_answer}
        ]

        return gradio_history_format, gradio_history_format, user_session, "", None

    except Exception as e:
        error_msg = f"⚠️ حدث خطأ أثناء المعالجة: {str(e)}"
        gradio_history_format = history + [
            {"role": "assistant", "content": error_msg}
        ]
        return gradio_history_format, gradio_history_format, user_session, "", None

def clear_all():
    return get_welcome_message(), get_welcome_message(), {"state": "NORMAL"}, "", None


# ============================
# 🌟 واجهة من صفحتين (صفحة تعريفية + البوت)
# ============================

# ============================
# 🌟 واجهة من صفحتين (صفحة تعريفية + البوت)
# ============================

with gr.Blocks(title="💙 دروب آمنة - الكلية التقنية الرقمية بجدة", theme=gr.themes.Soft()) as app:
    
    # ---------- الصفحة الأولى ----------
    intro_box = gr.Column(visible=True)
    with intro_box:
        gr.Markdown("""
        <style>
        .gradio-container {
            background: linear-gradient(135deg, #ffffff, #e6f0ff);
            text-align: center;
            font-family: 'Cairo', sans-serif;
        }
        .intro-title {
            color: #004aad;
            font-size: 28px;
            font-weight: bold;
            margin-top: 40px;
        }
        .intro-desc {
            color: #333;
            font-size: 18px;
            margin-top: 20px;
            line-height: 1.8;
        }
        .start-btn {
            background-color: #004aad !important;
            color: white !important;
            border-radius: 20px !important;
            font-size: 18px !important;
            padding: 10px 40px !important;
            margin-top: 40px;
        }
        </style>

        <h1 class="intro-title">💙 دروب آمنة - الكلية التقنية الرقمية بجدة 💙</h1>
        <p class="intro-desc">
        أهلاً وسهلاً بكِ في الكلية التقنية الرقمية بجدة 🌸<br>
        نسعى لتمكين طالباتنا من المهارات التقنية والمهنية بأجواء تعليمية آمنة وميسّرة.<br>
        من خلال "دروب آمنة"، يمكنكِ التعرف على مرافق الكلية بسهولة مثل المكتبة، العيادة، المسرح والمكاتب الإدارية....<br><br>
        اضغطي الزر أدناه للبدء 👇
        </p>
        """)
        start_btn = gr.Button("🚀 ابدئي الآن", elem_classes="start-btn")

    # ---------- صفحة البوت ----------
    bot_box = gr.Column(visible=False)
    with bot_box:
        gr.Markdown("""
        <style>
        .gradio-container {background: linear-gradient(135deg, #ffffff, #e6f0ff);}
        .gr-button {border-radius: 16px !important;}
        </style>
        <h2 style='text-align:center;color:#004aad;'>💙 دروب آمنة - المساعدة الذكية 💙</h2>
        """)

        chatbot_history = gr.State(get_welcome_message())
        user_session = gr.State({"state": "NORMAL"})
        chatbot = gr.Chatbot(value=get_welcome_message(), type='messages')
        message = gr.Textbox(label="اكتبي رسالتك هنا...", placeholder="اسألي أي شيء...", lines=1)

        # أزرار جاهزة
        with gr.Row():
            btns = [
                gr.Button("مواقف"), gr.Button("بوابات"), gr.Button("مصاعد"),
                gr.Button("مطعم وكوفي"), gr.Button("العيادة"), gr.Button("المكتبة"),
                gr.Button("الإرشاد الأكاديمي"), gr.Button("ساحة المدربات"), gr.Button("مساعدة")
            ]

        # أزرار إرسال ومسح وواتساب
        with gr.Row():
            send_button = gr.Button("إرسال", variant="primary")
            clear_btn = gr.Button("🗑️ مسح", variant="secondary")
            whatsapp_button = gr.Button("📲 واتساب", variant="share")

        # قائمة المخرجات بدون audio_input
        outputs_list = [chatbot, chatbot_history, user_session, message]

        # ربط الأحداث
        send_button.click(chat, [message, chatbot_history, user_session], outputs_list)
        message.submit(chat, [message, chatbot_history, user_session], outputs_list)
        clear_btn.click(clear_all, None, outputs_list)
        whatsapp_button.click(launch_whatsapp_button, [], [])

        for btn in btns:
            btn.click(lambda b=btn: b.value, None, [message]).then(
                chat, [message, chatbot_history, user_session], outputs_list
            )

        gr.Markdown("<br><p style='text-align:center;color:#007BFF;'>Developed by: أريام الشافعي 💙</p>")

    # 🚀 عند الضغط على الزر — يخفي صفحة التعريف ويُظهر صفحة البوت
    start_btn.click(lambda: (gr.update(visible=False), gr.update(visible=True)), outputs=[intro_box, bot_box])

# ----------------------------
# تشغيل التطبيق
# ----------------------------
if __name__ == "__main__":
    app.launch(share=True)
}
