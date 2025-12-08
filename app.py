from decimal import Decimal

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    comparison = None
    error_message = ""
    if request.method == 'POST':
        try:
            x_input = request.form['x'].replace(',', '')  # カンマを取り除く
            total_messages = int(x_input)
            if total_messages < 0:
                raise ValueError
            legacy_fee = Decimal(calculate_legacy_fee(total_messages))
            new_fee = calculate_new_fee(total_messages)
            additional_messages = max(total_messages - 30000, 0)
            difference = new_fee - legacy_fee
            comparison = {
                'total_messages': total_messages,
                'additional_messages': additional_messages,
                'legacy_fee': legacy_fee,
                'new_fee': new_fee,
                'difference': difference,
                'difference_abs': abs(difference),
            }
        except ValueError:
            error_message = "入力は整数である必要があります🙏🏻"
    return render_template_string(
        template,
        comparison=comparison,
        error_message=error_message,
        currency=format_currency,
        format_number=format_number,
    )

def calculate_legacy_fee(x):
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

def calculate_new_fee(total_messages):
    additional = max(total_messages - 30000, 0)
    if additional <= 0:
        return Decimal('0')
    tier_one = min(additional, 200000)
    tier_two = max(additional - 200000, 0)
    total = (Decimal(tier_one) * Decimal('3.0')) + (Decimal(tier_two) * Decimal('2.5'))
    return total

def format_currency(value):
    if isinstance(value, Decimal):
        if value == value.to_integral():
            return f"{int(value):,}"
        return f"{value:,.1f}"
    return f"{value:,}"

def format_number(value):
    return f"{value:,}"

template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ニューLくん - メッセージ費用計算</title>
    <style>
      :root {
        color-scheme: light dark;
        font-family: 'SF Pro Display', 'Helvetica Neue', Arial, sans-serif;
        --bg: #f4f6fb;
        --card-bg: #fff;
        --accent: #2563eb;
        --accent-soft: rgba(37, 99, 235, 0.15);
        --legacy: #f97316;
        --new: #22c55e;
        --diff: #0f172a;
      }
      body {
        margin: 0;
        background: var(--bg);
        color: #0f172a;
      }
      .page {
        max-width: 960px;
        margin: 0 auto;
        padding: 32px 16px 64px;
      }
      h1 {
        margin-bottom: 8px;
      }
      p.subtitle {
        margin-top: 0;
        color: #475569;
      }
      form {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin: 24px 0 16px;
      }
      label {
        flex-basis: 100%;
        font-weight: 600;
      }
      input {
        flex: 1 1 240px;
        padding: 12px;
        border-radius: 12px;
        border: 1px solid #cbd5f5;
        font-size: 1rem;
      }
      button {
        padding: 12px 24px;
        border: none;
        border-radius: 12px;
        background: var(--accent);
        color: #fff;
        font-size: 1rem;
        cursor: pointer;
      }
      button:hover {
        opacity: 0.95;
      }
      .alert {
        background: #fee2e2;
        color: #b91c1c;
        padding: 12px 16px;
        border-radius: 12px;
        margin-top: 8px;
      }
      .cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-top: 24px;
      }
      .card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
      }
      .card h2 {
        margin-top: 0;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .price {
        font-size: 2rem;
        margin: 8px 0 0;
      }
      .card.legacy h2 { color: var(--legacy); }
      .card.new h2 { color: var(--new); }
      .card.diff h2 { color: var(--diff); }
      .details {
        margin-top: 32px;
        background: var(--card-bg);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08);
      }
      .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #e2e8f0;
      }
      .detail-row:last-child {
        border-bottom: none;
      }
      .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--accent-soft);
        color: var(--accent);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.85rem;
      }
      .diff.positive .price {
        color: var(--new);
      }
      .diff.negative .price {
        color: #ef4444;
      }
      .diff.neutral .price {
        color: var(--diff);
      }
    </style>
  </head>
  <body>
    <div class="page">
      <h1>ニューLくんです！</h1>
      <p class="subtitle">旧料金と新料金（20万通までは3円/通、以降2.5円/通）を同時にチェックできます。</p>
      <form method="post">
        <label for="x">無料分30,000通を含む合計配信メッセージ数を入力してください。</label>
        <input type="text" id="x" name="x" placeholder="例: 500,000" required autofocus>
        <button type="submit">計算する</button>
      </form>
      {% if error_message %}
        <div class="alert">{{ error_message }}</div>
      {% endif %}

      {% if comparison %}
      <div class="cards">
        <div class="card legacy">
          <h2>旧料金プラン</h2>
          <p class="price">¥{{ currency(comparison.legacy_fee) }}</p>
          <p>追加メッセージ {{ format_number(comparison.additional_messages) }}通で計算</p>
        </div>
        <div class="card new">
          <h2>新料金プラン</h2>
          <p class="price">¥{{ currency(comparison.new_fee) }}</p>
          <p>〜200,000通: 3円 ／ それ以降: 2.5円</p>
        </div>
        <div class="card diff {% if comparison.difference < 0 %}negative{% elif comparison.difference > 0 %}positive{% else %}neutral{% endif %}">
          <h2>差額</h2>
          <p class="price">
            {% if comparison.difference > 0 %}
              +¥{{ currency(comparison.difference) }}
            {% elif comparison.difference < 0 %}
              -¥{{ currency(comparison.difference_abs) }}
            {% else %}
              ¥0
            {% endif %}
          </p>
          <p>{% if comparison.difference > 0 %}新料金の方が高いです{% elif comparison.difference < 0 %}新料金の方がお得です{% else %}同じ金額です{% endif %}</p>
        </div>
      </div>

      <div class="details">
        <div class="detail-row">
          <span>合計配信メッセージ数</span>
          <strong>{{ format_number(comparison.total_messages) }} 通</strong>
        </div>
        <div class="detail-row">
          <span>無料分を除いた追加メッセージ</span>
          <strong>{{ format_number(comparison.additional_messages) }} 通</strong>
        </div>
        <div class="detail-row">
          <span>旧料金プラン 単価</span>
          <span class="badge">段階制</span>
        </div>
        <div class="detail-row">
          <span>新料金プラン 単価</span>
          <span class="badge">20万通まで3円 / 以降2.5円</span>
        </div>
      </div>
      {% endif %}
    </div>
  </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
