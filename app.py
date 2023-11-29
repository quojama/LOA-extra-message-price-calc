import math

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        try:
            x_input = request.form['x'].replace(',', '')  # カンマを取り除く
            x = int(x_input)
            calc_result = calculate(x)
            if isinstance(calc_result, int):
                fee = math.floor(calc_result/10)
                result = f'{x:,}通の金額は {calc_result:,} 円です。\n※プラン費用は含まれていません。'
            else:
                result = "追加メッセージが1,000万通を超えています。この場合はL社へ個別にお問い合わせください。🤚🏻"
        except ValueError:
            result = "入力は整数である必要があります🙏🏻"
    return render_template_string(template, result=result)

def calculate(x):
    y = x - 30000
    if y <= 0:
        return 0
    elif y <= 50000:
        return round(y * 3.0)
    elif y <= 100000:
        return round(150000 + (y - 50000) * 2.8)
    elif y <= 200000:
        return round(290000 + (y - 100000) * 2.6)
    elif y <= 300000:
        return round(550000 + (y - 200000) * 2.4)
    elif y <= 400000:
        return round(790000 + (y - 300000) * 2.2)
    elif y <= 500000:
        return round(1010000 + (y - 400000) * 2.0)
    elif y <= 600000:
        return round(1210000 + (y - 500000) * 1.9)
    elif y <= 700000:
        return round(1400000 + (y - 600000) * 1.8)
    elif y <= 800000:
        return round(1580000 + (y - 700000) * 1.7)
    elif y <= 900000:
        return round(1750000 + (y - 800000) * 1.6)
    elif y <= 1000000:
        return round(1910000 + (y - 900000) * 1.5)
    elif y <= 3000000:
        return round(2060000 + (y - 1000000) * 1.4)
    elif y <= 5000000:
        return round(4860000 + (y - 3000000) * 1.3)
    elif y <= 7000000:
        return round(7460000 + (y - 5000000) * 1.2)
    elif y <= 10000000:
        return round(9860000 + (y - 7000000) * 1.1)
    elif y <= 15000000:
        return round(13160000 + (y - 10000000) * 1.0)
    elif y <= 20000000:
        return round(18160000 + (y - 15000000) * 0.95)
    elif y <= 25000000:
        return round(22910000 + (y - 20000000) * 0.9)
    elif y <= 30000000:
        return round(27410000 + (y - 25000000) * 0.85)
    elif y <= 35000000:
        return round(31660000 + (y - 30000000) * 0.8)
    elif y <= 40000000:
        return round(35660000 + (y - 35000000) * 0.75)
    elif y <= 45000000:
        return round(39410000 + (y - 40000000) * 0.7)
    elif y <= 50000000:
        return round(42910000 + (y - 45000000) * 0.65)
    elif y <= 55000000:
        return round(46160000 + (y - 50000000) * 0.6)
    elif y <= 60000000:
        return round(49160000 + (y - 55000000) * 0.55)
    elif y <= 65000000:
        return round(51910000 + (y - 60000000) * 0.5)
    elif y <= 70000000:
        return round(54410000 + (y - 65000000) * 0.45)
    elif y <= 75000000:
        return round(56660000 + (y - 70000000) * 0.4)
    elif y <= 80000000:
        return round(58660000 + (y - 75000000) * 0.35)
    elif y <= 85000000:
        return round(60410000 + (y - 80000000) * 0.3)
    elif y <= 90000000:
        return round(61910000 + (y - 85000000) * 0.25)
    elif y <= 95000000:
        return round(63160000 + (y - 90000000) * 0.2)
    else:
        return round(64160000 + (y - 95000000) * 0.15)

template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Lくん - メッセージ費用計算</title>
  </head>
  <body>
    <div>
      <h1>Lくんです</h1>
      <form method="post">
        <label for="x">無料分 30,000通を含む合計配信メッセージ数を入力してください。💡: </label>
        <input type="text" id="x" name="x" required autofocus>
        <button type="submit">Calculate</button>
      </form>
      <pre>{{ result }}</pre>
    </div>
  </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
