from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    prices = []
    try:
        # دریافت قیمت دلار
        usd_response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        usd_data = usd_response.json()
        usd_to_toman = int(usd_data['rates']['IRR'] / 10) 
        
        # محاسبه قیمت طلا و سکه
        gold_ounce_usd = 2350 
        gold_gram_18 = int((gold_ounce_usd * usd_to_toman) / 31.1035 * 0.75)
        
        coin_emami = int(gold_gram_18 * 8.13) 
        coin_bahar = int(gold_gram_18 * 8.13) 
        half_coin = int(gold_gram_18 * 4.06)
        quarter_coin = int(gold_gram_18 * 2.03)
        
        prices = [
            {"name": "دلار آمریکا", "price": usd_to_toman, "link": "https://www.tgju.org/profile/price_dollar_rl"},
            {"name": "طلای ۱۸ عیار (گرم)", "price": gold_gram_18, "link": "https://www.tgju.org/profile/geram18"},
            {"name": "سکه امامی", "price": coin_emami, "link": "https://www.tgju.org/profile/sekee"},
            {"name": "سکه بهار آزادی", "price": coin_bahar, "link": "https://www.tgju.org/profile/sekeb"},
            {"name": "نیم سکه", "price": half_coin, "link": "https://www.tgju.org/profile/nim"},
            {"name": "ربع سکه", "price": quarter_coin, "link": "https://www.tgju.org/profile/rob"},
        ]
    except Exception as e:
        prices = [{"name": "خطا در اتصال به اینترنت", "price": 0, "link": "#"}]

    return render_template('index.html', prices=prices)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
