from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    prices = []
    try:
        # دریافت قیمت‌ها از وب‌سرویس ۲۴طلا
        url = "https://24tala.ir/api/v1/prices"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("ok"):
            # استخراج قیمت‌ها از ساختار JSON این سرویس
            # (ساختار ممکنه کمی متفاوت باشه، این کد بر اساس مستنداتش تنظیم شده)
            items = data.get("data", {}).get("items", [])
            
            # اگر ساختار فرق داشت، از دیکشنری مستقیم استفاده می‌کنیم
            gold_data = data.get("data", {})
            
            prices = [
                {"name": "طلای ۱۸ عیار (گرم)", "price": gold_data.get("gold", {}).get("current", 0), "link": "https://24tala.ir/"},
                {"name": "دلار آمریکا", "price": next((i.get("sell") for i in items if i.get("code") == "USD"), 0), "link": "https://24tala.ir/"},
                {"name": "سکه امامی", "price": next((i.get("price") for i in items if i.get("code") == "seke_emami"), 0), "link": "https://24tala.ir/"},
                {"name": "نیم سکه", "price": next((i.get("price") for i in items if i.get("code") == "seke_nim"), 0), "link": "https://24tala.ir/"},
                {"name": "ربع سکه", "price": next((i.get("price") for i in items if i.get("code") == "seke_rob"), 0), "link": "https://24tala.ir/"},
            ]
            
            # فیلتر کردن مواردی که قیمت صفر دارن
            prices = [p for p in prices if p["price"] and p["price"] > 0]
            
            if not prices:
                raise Exception("No valid prices found")
        else:
            raise Exception("API returned not ok")

    except Exception as e:
        # در صورت خطا، پیام نمایش داده می‌شود
        prices = [{"name": "خطا در دریافت قیمت (لطفاً بعداً تلاش کنید)", "price": 0, "link": "#"}]

    return render_template('index.html', prices=prices)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
