from flask import Flask, render_template
import asyncio
import os

app = Flask(__name__)

# تابع برای دریافت قیمت‌های واقعی از TGJU
async def get_real_prices():
    from tgju import TgjuClient, MarketItem
    
    client = TgjuClient()
    prices = []
    
    items = [
        (MarketItem.PriceDollarRl, "دلار آمریکا"),
        (MarketItem.Geram18, "طلای ۱۸ عیار (گرم)"),
        (MarketItem.Sekee, "سکه امامی"),
        (MarketItem.Sekeb, "سکه بهار آزادی"),
        (MarketItem.Nim, "نیم سکه"),
        (MarketItem.Rob, "ربع سکه"),
        (MarketItem.Gerami, "سکه گرمی"),
    ]
    
    for item, name in items:
        try:
            price = await client.get_price(item)
            prices.append({"name": name, "price": price // 10})
        except Exception:
            prices.append({"name": name, "price": 0})
            
    return prices

@app.route('/')
def home():
    try:
        prices = asyncio.run(get_real_prices())
        if not prices or all(p['price'] == 0 for p in prices):
            raise Exception("No data")
    except Exception as e:
        prices = [{"name": "خطا در دریافت قیمت", "price": 0}]

    return render_template('index.html', prices=prices)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
