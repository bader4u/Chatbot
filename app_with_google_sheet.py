
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import sqlite3

app = Flask(__name__)

# حفظ المحادثات والردود
def save_to_db(msg, reply):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            msg TEXT,
            response TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("INSERT INTO messages (msg, response) VALUES (?, ?)", (msg, reply))
    conn.commit()
    conn.close()

user_states = {}
sheet_url = "https://script.google.com/macros/s/AKfycbzB48NdWlzNPUGHfb6_eg0Qk2F1y8uKLYCQ19XQUK60-a6Kxoy_7JJuF_d90Ms/exec"

@app.route("/sms", methods=["POST"])
def sms_reply():
    msg = request.form.get("Body").strip()
    phone = request.form.get("From")
    msg_clean = msg.lower()
    response = MessagingResponse()

    if phone not in user_states:
        user_states[phone] = "main_menu"
        response.message("مرحباً بك في مكتب فهد للاستقدام، كيف يمكنني مساعدتك؟\nيرجى اختيار من القائمة التالية:\n• تقديم طلب جديد\n• متابعة طلب سابق\n• نقل كفالة\n• الملاحظات والشكاوى")
        return str(response)

    state = user_states[phone]

    if state == "main_menu":
        if "طلب جديد" in msg_clean:
            response.message("يرجى تحديد الجنسية التي ترغب بالتقديم لها.")
            user_states[phone] = "awaiting_country"
        elif "طلب سابق" in msg_clean:
            response.message("✅ تم تحويلك إلى الموظف المختص، يرجى الانتظار...")
            user_states.pop(phone)
        elif "نقل كفالة" in msg_clean:
            response.message("الجنسيات المتوفرة لنقل الكفالة:\n• أوغندا\n• الفلبين")
            user_states[phone] = "main_menu"
        elif "ملاحظات" in msg_clean or "شكوى" in msg_clean:
            response.message("📩 تم تحويلك إلى الإدارة، يرجى الانتظار...")
            user_states.pop(phone)
        else:
            response.message("❌ يرجى اختيار خيار صحيح من القائمة:\n• تقديم طلب جديد\n• متابعة طلب سابق\n• نقل كفالة\n• الشكوى")
            user_states[phone] = "main_menu"

    elif state == "awaiting_country":
        result = requests.get(sheet_url, params={"country": msg_clean})
        if result.status_code == 200:
            response.message(result.text + "\n\nاختر من القائمة:\nهل تود تنفيذ إجراء آخر؟")
            user_states[phone] = "main_menu"
        else:
            response.message(f"❌ لم يتم العثور على الدولة: {msg_clean}\nتمت إعادتك للقائمة الرئيسية.")
            user_states[phone] = "main_menu"

    save_to_db(msg, response.message.body)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
