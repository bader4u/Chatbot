
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import sqlite3

app = Flask(__name__)

# حفظ المحادثات والحالات
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

# تخزين حالة المستخدمين
user_states = {}

@app.route("/sms", methods=["POST"])
def sms_reply():
    msg = request.form.get("Body").strip()
    sender = request.form.get("From")
    msg_clean = msg.lower()
    reply = ""


from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

user_states = {}

sheet_url = "https://script.google.com/macros/s/AKfycbz848N4dWzNPuGHFb6_eq0QKk2F1y8ukLYCX19XQUK60-a6Kxxy_J7u3F_d90Mbs/exec"

@app.route("/sms", methods=["POST"])
def sms_reply():
    msg = request.form.get("Body")
    phone = request.form.get("From")
    msg_clean = msg.strip()

    response = MessagingResponse()

    # الحالة الافتراضية
    if phone not in user_states:
        user_states[phone] = "main_menu"
        response.message("""
مرحباً بك في مكتب فهد للاستقدام،
كيف يمكنني مساعدتك؟
يرجى اختيار من القائمة التالية:
- تقديم طلب جديد
- متابعة طلب سابق
- نقل كفالة
- الملاحظات والشكاوى
        """)
        return str(response)

    state = user_states[phone]

    if state == "main_menu":
        if "طلب جديد" in msg_clean:
            response.message("يرجى تحديد الجنسية التي ترغب بالتقديم لها.")
            user_states[phone] = "awaiting_country"
        elif "طلب سابق" in msg_clean:
            response.message("📨 تم تحويلك إلى الموظف المختص، يرجى الانتظار...")
            user_states.pop(phone)
        elif "نقل كفالة" in msg_clean:
    response.message(
    "الجنسيات المتوفرة لنقل الكفالة:\n"
    "- أوغندا\n"
    "- كينيا\n"
    "- الفلبين"
)
 
    response.message("هل تود تنفيذ إجراء آخر؟\n"
           "اختر من القائمة"
    "- تقديم طلب جديد\n"
    "- متابعة طلب سابق\n"
    "- نقل كفالة\n"
    "- الشكاوى")
            user_states[phone] = "main_menu"
        elif "شكاوى" in msg_clean or "ملاحظات" in msg_clean:
            response.message("🔄 تم تحويلك إلى الإدارة، يرجى الانتظار...")
            user_states.pop(phone)
        else:
            response.message("يرجى اختيار خيار صحيح من القائمة\n"
"- تقديم طلب جديد\n"
"- متابعة طلب سابق\"
"- نقل كفالة\n"
"- الشكاوى")

    elif state == "awaiting_country":
        result = requests.get(sheet_url, params={"country": msg_clean})
        if result.status_code == 200:
            response.message(result.text + "\n\nهل تود تنفيذ إجراء آخر؟\nاختر من القائمة
- تقديم طلب جديد
- متابعة طلب سابق
- نقل كفالة
- الشكاوى")
            user_states[phone] = "main_menu"
        else:
            response.message("⚠️ لم يتم العثور على الدولة: " + msg_clean + "\nيرجى المحاولة مجددًا.")
            user_states[phone] = "main_menu"

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)


if __name__ == "__main__":
    app.run(debug=Tr
