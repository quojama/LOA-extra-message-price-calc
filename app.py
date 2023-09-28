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
                result = f'金額は {calc_result:,} 円です。\n※プラン費用は含まれていません。'
            else:
                result = "LINE社へ個別にお問い合わせください"
        except ValueError:
            result = "入力は整数である必要があります。"
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
        return round(150000 + 140000 + (y - 100000) * 2.6)
    elif y <= 300000:
        return round(150000 + 140000 + 260000 + (y - 200000) * 2.4)
    elif y <= 400000:
        return round(150000 + 140000 + 260000 + 240000 + (y - 300000) * 2.2)
    elif y <= 500000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + (y - 400000) * 2.0)
    elif y <= 600000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + (y - 500000) * 1.9)
    elif y <= 700000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + (y - 600000) * 1.8)
    elif y <= 800000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + (y - 700000) * 1.7)
    elif y <= 900000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + (y - 800000) * 1.6)
    elif y <= 1000000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + 160000 + (y - 900000) * 1.5)
    elif y <= 3000000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + 160000 + 150000 + (y - 1000000) * 1.4)
    elif y <= 5000000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + 160000 + 150000 + 2800000 + (y - 3000000) * 1.3)
    elif y <= 7000000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + 160000 + 150000 + 2800000 + 2600000 + (y - 5000000) * 1.2)
    elif y <= 10000000:
        return round(150000 + 140000 + 260000 + 240000 + 220000 + 200000 + 190000 + 180000 + 170000 + 160000 + 150000 + 2800000 + 2600000 + 2400000 + (y - 7000000) * 1.1)
    else:
        return "LINE社へ個別にお問い合わせください"

template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>費用計算アプリ</title>
  </head>
  <body>
    <div>
      <h1>Lかつくん</h1>
      <form method="post">
        <label for="x">無料分 30,000通を含む合計配信メッセージ数を入力してください: </label>
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
