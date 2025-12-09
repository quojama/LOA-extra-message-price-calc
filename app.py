from decimal import Decimal

from flask import Flask, render_template_string, request

app = Flask(__name__)

MAX_CHART_MESSAGES = 10_000_000
CHART_SAMPLE_STEP = 500_000

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
        request=request,
        chart_points=CHART_POINTS,
        max_chart_messages=MAX_CHART_MESSAGES,
        chart_step=CHART_SAMPLE_STEP,
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

def generate_chart_points(max_messages=MAX_CHART_MESSAGES, step=CHART_SAMPLE_STEP):
    """Precompute sampled pricing data for the chart."""
    anchor_points = {
        1,
        30000,
        50000,
        100000,
        200000,
        300000,
        400000,
        500000,
        600000,
        700000,
        800000,
        900000,
        1_000_000,
        3_000_000,
        5_000_000,
        7_000_000,
        10_000_000,
        15_000_000,
        20_000_000,
        25_000_000,
        30_000_000,
        35_000_000,
        40_000_000,
        45_000_000,
        50_000_000,
        max_messages,
    }
    anchor_points.update(range(step, max_messages + 1, step))
    totals = sorted({value for value in anchor_points if 0 < value <= max_messages})
    chart_points = []
    for total in totals:
        legacy_fee = calculate_legacy_fee(total)
        new_fee = calculate_new_fee(total)
        chart_points.append(
            {
                "messages": total,
                "legacy": legacy_fee,
                "new": float(new_fee),
            }
        )
    return chart_points

CHART_POINTS = generate_chart_points()

template = '''
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ニューLくん - メッセージ費用計算</title>
    <style>
      :root {
        font-family: 'Inter', 'Noto Sans JP', 'SF Pro Display', 'Helvetica Neue', sans-serif;
        --bg: #030712;
        --bg-secondary: #0f172a;
        --panel: rgba(15, 23, 42, 0.75);
        --border: rgba(148, 163, 184, 0.2);
        --text: #e2e8f0;
        --muted: #94a3b8;
        --legacy: #fb923c;
        --new: #22c55e;
        --accent: #2563eb;
        --danger: #f87171;
      }
      *, *::before, *::after {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        min-height: 100vh;
        background: radial-gradient(circle at top, rgba(59, 130, 246, 0.12), transparent 50%), var(--bg);
        color: var(--text);
        line-height: 1.6;
      }
      .page {
        max-width: 1100px;
        margin: 0 auto;
        padding: 56px 20px 80px;
        position: relative;
        z-index: 1;
      }
      .glow {
        position: fixed;
        inset: 0;
        background: radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.25), transparent 45%),
                    radial-gradient(circle at 80% 10%, rgba(14, 165, 233, 0.2), transparent 40%);
        pointer-events: none;
        z-index: 0;
      }
      h1, h2, h3, h4 {
        margin: 0;
        line-height: 1.2;
      }
      .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-size: 0.75rem;
        color: var(--muted);
        margin-bottom: 8px;
      }
      .hero {
        margin-bottom: 32px;
      }
      .hero h1 {
        font-size: clamp(2rem, 4vw, 3.2rem);
        color: #f8fafc;
      }
      .hero p {
        max-width: 640px;
        margin-top: 16px;
        color: var(--muted);
        font-size: 1.05rem;
      }
      .panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 28px;
        padding: 32px;
        backdrop-filter: blur(12px);
        box-shadow: 0 40px 120px rgba(2, 6, 23, 0.55);
      }
      .calc-form {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .calc-form label {
        font-weight: 600;
        color: #f1f5f9;
      }
      .input-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }
      input[type="text"] {
        flex: 1 1 280px;
        padding: 16px 20px;
        border-radius: 18px;
        border: 1px solid var(--border);
        background: rgba(15, 23, 42, 0.65);
        color: var(--text);
        font-size: 1.1rem;
        outline: none;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }
      input[type="text"]:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.35);
      }
      button {
        padding: 16px 28px;
        border-radius: 18px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        color: #fff;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }
      button:hover {
        transform: translateY(-1px);
        box-shadow: 0 20px 30px rgba(79, 70, 229, 0.35);
      }
      .form-hint {
        color: var(--muted);
        font-size: 0.95rem;
        margin: 0;
      }
      .alert {
        padding: 12px 16px;
        border-radius: 14px;
        background: rgba(248, 113, 113, 0.15);
        color: var(--danger);
        border: 1px solid rgba(248, 113, 113, 0.25);
      }
      .metrics {
        margin-top: 32px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
      }
      .metric {
        padding: 24px;
        border-radius: 24px;
        border: 1px solid var(--border);
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        position: relative;
        overflow: hidden;
      }
      .metric::after {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: inherit;
        border: 1px solid transparent;
        pointer-events: none;
      }
      .metric.legacy::after {
        border-color: rgba(251, 146, 60, 0.3);
      }
      .metric.new::after {
        border-color: rgba(34, 197, 94, 0.3);
      }
      .metric.diff::after {
        border-color: rgba(94, 234, 212, 0.25);
      }
      .metric h3 {
        margin-bottom: 6px;
        font-size: 1rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--muted);
      }
      .metric .value {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 8px 0;
      }
      .metric.legacy .value {
        color: var(--legacy);
      }
      .metric.new .value {
        color: var(--new);
      }
      .metric.diff .value {
        color: #38bdf8;
      }
      .metric.diff.positive .value {
        color: var(--legacy);
      }
      .metric.diff.negative .value {
        color: var(--new);
      }
      .metric p {
        margin: 0;
        color: var(--muted);
      }
      .details-card {
        margin-top: 24px;
        border-radius: 28px;
        border: 1px solid var(--border);
        padding: 28px;
        background: rgba(15, 23, 42, 0.85);
      }
      .details-card h3 {
        margin-bottom: 18px;
        color: #f8fafc;
      }
      .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.2);
        color: var(--muted);
      }
      .detail-row:last-child {
        border-bottom: none;
      }
      .detail-row strong {
        color: #f4f4f5;
        font-size: 1.05rem;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1px solid var(--border);
        color: var(--muted);
        font-size: 0.85rem;
        gap: 6px;
        background: rgba(15, 23, 42, 0.7);
      }
      .chart-card {
        margin-top: 40px;
        padding: 32px;
        border-radius: 28px;
        border: 1px solid var(--border);
        background: rgba(2, 6, 23, 0.85);
      }
      .chart-head {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 24px;
      }
      .chart-head h2 {
        font-size: 1.4rem;
      }
      .chart-canvas {
        position: relative;
        height: 420px;
      }
      #priceChart {
        width: 100%;
        height: 100%;
      }
      .chart-caption {
        margin-top: 18px;
        color: var(--muted);
        font-size: 0.95rem;
      }
      .footer {
        margin-top: 56px;
        text-align: center;
        color: var(--muted);
        font-size: 0.9rem;
      }
      @media (max-width: 640px) {
        .panel, .details-card, .chart-card {
          padding: 24px;
        }
        .input-row {
          flex-direction: column;
        }
        button {
          width: 100%;
        }
        .chart-canvas {
          height: 320px;
        }
      }
    </style>
  </head>
  <body>
    <div class="glow" aria-hidden="true"></div>
    <div class="page">
      <header class="hero">
        <p class="eyebrow">LINE Official Account helper</p>
        <h1>ニューLくんです</h1>
        <p>無料枠30,000通を含む合計配信数を入れるだけで、段階制の旧プランと、新しいシンプルな単価プランの差額が一目でわかります。</p>
      </header>

      <section class="panel input-card">
        <form method="post" class="calc-form">
          <label for="x">合計配信メッセージ数</label>
          <div class="input-row">
            <input type="text" id="x" name="x" placeholder="例: 5,000,000" value="{{ request.form.get('x', '') }}" inputmode="numeric" autocomplete="off" required>
            <button type="submit">計算する</button>
          </div>
          <p class="form-hint">半角数字（カンマ区切りOK）で、無料分30,000通を含む配信数を入力してください。</p>
          {% if error_message %}
            <div class="alert">{{ error_message }}</div>
          {% endif %}
        </form>
      </section>

      {% if comparison %}
      <section class="metrics">
        <article class="metric legacy">
          <h3>旧料金プラン</h3>
          <p class="value">¥{{ currency(comparison.legacy_fee) }}</p>
          <p>追加メッセージ {{ format_number(comparison.additional_messages) }} 通</p>
        </article>
        <article class="metric new">
          <h3>新料金プラン</h3>
          <p class="value">¥{{ currency(comparison.new_fee) }}</p>
          <p>〜200,000通: 3円 / 以降: 2.5円</p>
        </article>
        <article class="metric diff {% if comparison.difference < 0 %}negative{% elif comparison.difference > 0 %}positive{% endif %}">
          <h3>差額</h3>
          <p class="value">
            {% if comparison.difference > 0 %}
              +¥{{ currency(comparison.difference) }}
            {% elif comparison.difference < 0 %}
              -¥{{ currency(comparison.difference_abs) }}
            {% else %}
              ¥0
            {% endif %}
          </p>
          <p>{% if comparison.difference > 0 %}新料金の方が高いです{% elif comparison.difference < 0 %}新料金の方がお得です{% else %}同じ金額です{% endif %}</p>
        </article>
      </section>

      <section class="details-card">
        <h3>内訳</h3>
        <div class="detail-row">
          <span>合計配信メッセージ数</span>
          <strong>{{ format_number(comparison.total_messages) }} 通</strong>
        </div>
        <div class="detail-row">
          <span>無料分を除いた追加メッセージ</span>
          <strong>{{ format_number(comparison.additional_messages) }} 通</strong>
        </div>
        <div class="detail-row">
          <span>旧料金プラン</span>
          <span class="pill">段階制の従量課金</span>
        </div>
        <div class="detail-row">
          <span>新料金プラン</span>
          <span class="pill">20万通まで3円 / 以降2.5円</span>
        </div>
      </section>
      {% endif %}

      <section class="chart-card">
        <div class="chart-head">
          <div>
            <p class="eyebrow">Fee trend</p>
            <h2>1通〜{{ format_number(max_chart_messages) }}通の比較グラフ</h2>
          </div>
          <div class="pill">約{{ format_number(chart_step) }}通おきのサンプル</div>
        </div>
        <div class="chart-canvas">
          <canvas id="priceChart" aria-label="料金の比較グラフ"></canvas>
        </div>
        <p class="chart-caption">旧料金の複雑な段階制と、新料金のシンプルな単価体系がどこで逆転するかを直感的に把握できます。</p>
      </section>

      <footer class="footer">
        <p>LINE公式アカウントの料金比較サポーター「ニューLくん」</p>
      </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
      document.addEventListener('DOMContentLoaded', () => {
        const canvas = document.getElementById('priceChart');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const points = {{ chart_points|tojson }};
        const legacyData = points.map(point => ({ x: point.messages, y: point.legacy }));
        const newData = points.map(point => ({ x: point.messages, y: point.new }));
        const numberFormatter = new Intl.NumberFormat('ja-JP');
        const currencyFormatter = new Intl.NumberFormat('ja-JP', {
          style: 'currency',
          currency: 'JPY',
          maximumFractionDigits: 1,
        });

        new Chart(ctx, {
          type: 'line',
          data: {
            datasets: [
              {
                label: '旧料金プラン',
                data: legacyData,
                borderColor: 'rgba(251, 146, 60, 1)',
                backgroundColor: 'rgba(251, 146, 60, 0.08)',
                borderWidth: 3,
                tension: 0.25,
                pointRadius: 0,
                pointHitRadius: 12,
              },
              {
                label: '新料金プラン',
                data: newData,
                borderColor: 'rgba(34, 197, 94, 1)',
                backgroundColor: 'rgba(34, 197, 94, 0.12)',
                borderWidth: 3,
                tension: 0.25,
                pointRadius: 0,
                pointHitRadius: 12,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
              mode: 'index',
              intersect: false,
            },
            plugins: {
              legend: {
                labels: {
                  color: '#e2e8f0',
                  usePointStyle: true,
                  pointStyle: 'circle',
                },
              },
              tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                borderColor: 'rgba(148, 163, 184, 0.35)',
                borderWidth: 1,
                callbacks: {
                  title(items) {
                    const value = items[0].parsed.x;
                    return `${numberFormatter.format(value)} 通`;
                  },
                  label(item) {
                    const label = item.dataset.label || '';
                    const value = item.parsed.y;
                    return `${label}: ${currencyFormatter.format(value)}`;
                  },
                },
              },
            },
            scales: {
              x: {
                type: 'linear',
                min: 0,
                max: {{ max_chart_messages }},
                ticks: {
                  color: '#94a3b8',
                  callback(value) {
                    if (value === 0) return '0 通';
                    return `${numberFormatter.format(value)} 通`;
                  },
                },
                grid: {
                  color: 'rgba(148, 163, 184, 0.15)',
                },
                title: {
                  display: true,
                  text: '配信メッセージ数',
                  color: '#e2e8f0',
                },
              },
              y: {
                ticks: {
                  color: '#94a3b8',
                  callback(value) {
                    return currencyFormatter.format(value);
                  },
                },
                grid: {
                  color: 'rgba(148, 163, 184, 0.1)',
                },
                title: {
                  display: true,
                  text: '費用 (円)',
                  color: '#e2e8f0',
                },
              },
            },
          },
        });
      });
    </script>
  </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
