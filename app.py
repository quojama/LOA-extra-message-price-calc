from decimal import Decimal

from flask import Flask, render_template_string, request

app = Flask(__name__)

MAX_CHART_MESSAGES = 30_000_000
CHART_SAMPLE_STEP = 500_000
SHOW_LEGACY_COMPARISON = False  # 2026-10-01の新料金移行により旧プランの表示は停止（計算ロジックは保持）

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
        show_legacy=SHOW_LEGACY_COMPARISON,
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
    <title>ニューLくん V3 - メッセージ費用計算</title>
    <style>
      :root {
        font-family: 'Inter', 'Noto Sans JP', 'SF Pro Display', 'Helvetica Neue', sans-serif;
        --bg: #0b0b0d;
        --surface: #17171a;
        --surface-2: #1e1e22;
        --border: rgba(255, 255, 255, 0.08);
        --border-strong: rgba(255, 255, 255, 0.16);
        --text: #f2f2f3;
        --muted: #96969e;
        --legacy: #f59e0b;
        --new: #06c755;
        --accent: #06c755;
        --accent-contrast: #04210f;
        --accent-soft: rgba(6, 199, 85, 0.12);
        --danger: #f87171;
      }
      *, *::before, *::after {
        box-sizing: border-box;
      }
      body {
        margin: 0;
        min-height: 100vh;
        background: var(--bg);
        color: var(--text);
        line-height: 1.6;
      }
      .page {
        max-width: 1100px;
        margin: 0 auto;
        padding: 56px 20px 80px;
      }
      h1, h2, h3, h4 {
        margin: 0;
        line-height: 1.2;
      }
      .eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.75rem;
        font-weight: 600;
        color: var(--muted);
        margin-bottom: 8px;
      }
      .hero {
        margin-bottom: 32px;
      }
      .hero h1 {
        font-size: clamp(1.8rem, 3.4vw, 2.6rem);
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--text);
      }
      .hero p {
        max-width: 640px;
        margin-top: 14px;
        color: var(--muted);
        font-size: 1rem;
      }
      .panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 32px;
      }
      .calc-form {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .calc-form label {
        font-weight: 600;
        color: var(--text);
      }
      .input-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
      }
      input[type="text"] {
        flex: 1 1 280px;
        padding: 14px 16px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: var(--surface-2);
        color: var(--text);
        font-size: 1.05rem;
        outline: none;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
      }
      input[type="text"]:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 3px var(--accent-soft);
      }
      button {
        padding: 14px 24px;
        border-radius: 10px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        color: var(--accent-contrast);
        background: var(--accent);
        cursor: pointer;
        transition: filter 0.15s ease;
      }
      button:hover {
        filter: brightness(1.08);
      }
      button:active {
        filter: brightness(0.96);
      }
      .form-hint {
        color: var(--muted);
        font-size: 0.9rem;
        margin: 0;
      }
      .alert {
        padding: 12px 16px;
        border-radius: 10px;
        background: rgba(248, 113, 113, 0.1);
        color: var(--danger);
        border: 1px solid rgba(248, 113, 113, 0.25);
      }
      .metrics {
        margin-top: 32px;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
      }
      .metric {
        padding: 24px;
        border-radius: 14px;
        border: 1px solid var(--border);
        border-left: 3px solid var(--border-strong);
        background: var(--surface);
      }
      .metric.legacy {
        border-left-color: var(--legacy);
      }
      .metric.new {
        border-left-color: var(--accent);
      }
      .metric.diff.positive {
        border-left-color: var(--legacy);
      }
      .metric.diff.negative {
        border-left-color: var(--accent);
      }
      .metric h3 {
        margin-bottom: 6px;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--muted);
      }
      .metric .value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 8px 0;
        color: var(--text);
      }
      .metric.legacy .value {
        color: var(--legacy);
      }
      .metric.new .value {
        color: var(--new);
      }
      .metric.diff .value {
        color: var(--text);
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
        border-radius: 16px;
        border: 1px solid var(--border);
        padding: 28px;
        background: var(--surface);
      }
      .details-card h3 {
        margin-bottom: 18px;
        color: var(--text);
      }
      .detail-row {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid var(--border);
        color: var(--muted);
      }
      .detail-row:last-child {
        border-bottom: none;
      }
      .detail-row strong {
        color: var(--text);
        font-size: 1.05rem;
      }
      .pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid var(--border);
        color: var(--muted);
        font-size: 0.8rem;
        gap: 6px;
        background: var(--surface-2);
      }
      .plan-explainer {
        margin-bottom: 32px;
      }
      .plan-explainer h2 {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 20px;
      }
      .plan-steps {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
      }
      .plan-step {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid var(--border);
        background: var(--surface-2);
      }
      .plan-step .pill {
        margin-bottom: 12px;
        color: var(--accent);
        background: var(--accent-soft);
        border-color: transparent;
      }
      .plan-step h3 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 8px;
      }
      .plan-step .value {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--accent);
        margin: 0 0 8px;
      }
      .plan-step p:not(.value) {
        margin: 0;
        color: var(--muted);
        font-size: 0.88rem;
      }
      .plan-formula {
        margin-top: 20px;
        padding: 18px 22px;
        border-radius: 12px;
        border: 1px solid var(--border);
        background: var(--surface);
      }
      .plan-formula h3 {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: var(--muted);
        margin-bottom: 10px;
      }
      .plan-formula p {
        margin: 6px 0;
        color: var(--text);
        font-family: 'SF Mono', 'Menlo', monospace;
        font-size: 0.9rem;
      }
      .plan-example {
        margin-top: 16px;
        color: var(--muted);
        font-size: 0.88rem;
      }
      .chart-card {
        margin-top: 32px;
        padding: 32px;
        border-radius: 16px;
        border: 1px solid var(--border);
        background: var(--surface);
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
        font-size: 1.3rem;
        font-weight: 700;
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
        font-size: 0.9rem;
      }
      .footer {
        margin-top: 48px;
        text-align: center;
        color: var(--muted);
        font-size: 0.85rem;
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
    <div class="page">
      <header class="hero">
        <p class="eyebrow">LINE Official Account helper</p>
        <h1>ニューLくんです V3</h1>
        {% if show_legacy %}
        <p>無料枠30,000通を含む合計配信数を入れるだけで、段階制の旧プランと、新しいシンプルな単価プランの差額が一目でわかります。</p>
        {% else %}
        <p>2026年10月1日から新料金プランに移行しました。無料枠30,000通を含む合計配信数を入れるだけで、料金をシンプルに計算できます。</p>
        {% endif %}
      </header>

      <section class="panel plan-explainer">
        <h2>新料金プランのしくみ</h2>
        <div class="plan-steps">
          <article class="plan-step">
            <span class="pill">無料枠</span>
            <h3>0〜30,000通</h3>
            <p class="value">¥0</p>
            <p>毎月30,000通までは無料でご利用いただけます。</p>
          </article>
          <article class="plan-step">
            <span class="pill">1通あたり3円</span>
            <h3>30,001〜230,000通</h3>
            <p class="value">¥3 / 通</p>
            <p>無料枠を超えた分のうち、最初の200,000通は1通3円です。</p>
          </article>
          <article class="plan-step">
            <span class="pill">1通あたり2.5円</span>
            <h3>230,001通〜</h3>
            <p class="value">¥2.5 / 通</p>
            <p>さらに超えた分は1通あたり2.5円に単価が下がります。</p>
          </article>
        </div>
        <div class="plan-formula">
          <h3>計算式</h3>
          <p>追加メッセージ数 = 合計配信数 − 30,000通</p>
          <p>料金 = min(追加メッセージ数, 200,000) × 3円 + max(追加メッセージ数 − 200,000, 0) × 2.5円</p>
        </div>
        <p class="plan-example">例: 合計500,000通を配信した場合、追加メッセージ数は470,000通。最初の200,000通分は3円（60万円）、残り270,000通分は2.5円（67.5万円）で、合計 ¥1,275,000 です。</p>
      </section>

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
        {% if show_legacy %}
        <article class="metric legacy">
          <h3>旧料金プラン</h3>
          <p class="value">¥{{ currency(comparison.legacy_fee) }}</p>
          <p>追加メッセージ {{ format_number(comparison.additional_messages) }} 通</p>
        </article>
        {% endif %}
        <article class="metric new">
          <h3>料金</h3>
          <p class="value">¥{{ currency(comparison.new_fee) }}</p>
          <p>〜200,000通: 3円 / 以降: 2.5円</p>
        </article>
        {% if show_legacy %}
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
        {% endif %}
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
        {% if show_legacy %}
        <div class="detail-row">
          <span>旧料金プラン</span>
          <span class="pill">段階制の従量課金</span>
        </div>
        {% endif %}
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
            <h2>1通〜{{ format_number(max_chart_messages) }}通の料金推移{% if show_legacy %}比較グラフ{% endif %}</h2>
          </div>
          <div class="pill">約{{ format_number(chart_step) }}通おきのサンプル</div>
        </div>
        <div class="chart-canvas">
          <canvas id="priceChart" aria-label="料金の推移グラフ"></canvas>
        </div>
        {% if show_legacy %}
        <p class="chart-caption">旧料金の複雑な段階制と、新料金のシンプルな単価体系がどこで逆転するかを直感的に把握できます。</p>
        {% else %}
        <p class="chart-caption">配信メッセージ数に応じた料金の増え方をシンプルに把握できます。</p>
        {% endif %}
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
        const showLegacy = {{ show_legacy | tojson }};
        const legacyData = points.map(point => ({ x: point.messages, y: point.legacy }));
        const newData = points.map(point => ({ x: point.messages, y: point.new }));
        const numberFormatter = new Intl.NumberFormat('ja-JP');
        const currencyFormatter = new Intl.NumberFormat('ja-JP', {
          style: 'currency',
          currency: 'JPY',
          maximumFractionDigits: 1,
        });

        const datasets = [];
        if (showLegacy) {
          datasets.push({
            label: '旧料金プラン',
            data: legacyData,
            borderColor: 'rgba(251, 146, 60, 1)',
            backgroundColor: 'rgba(251, 146, 60, 0.08)',
            borderWidth: 3,
            tension: 0.25,
            pointRadius: 0,
            pointHitRadius: 12,
          });
        }
        datasets.push({
          label: showLegacy ? '新料金プラン' : '料金',
          data: newData,
          borderColor: 'rgba(6, 199, 85, 1)',
          backgroundColor: 'rgba(6, 199, 85, 0.1)',
          borderWidth: 2,
          tension: 0.2,
          pointRadius: 0,
          pointHitRadius: 12,
        });

        new Chart(ctx, {
          type: 'line',
          data: {
            datasets: datasets,
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
                  color: '#f2f2f3',
                  usePointStyle: true,
                  pointStyle: 'circle',
                },
              },
              tooltip: {
                backgroundColor: '#1e1e22',
                borderColor: 'rgba(255, 255, 255, 0.12)',
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
                  color: '#96969e',
                  callback(value) {
                    if (value === 0) return '0 通';
                    return `${numberFormatter.format(value)} 通`;
                  },
                },
                grid: {
                  color: 'rgba(255, 255, 255, 0.06)',
                },
                title: {
                  display: true,
                  text: '配信メッセージ数',
                  color: '#f2f2f3',
                },
              },
              y: {
                ticks: {
                  color: '#96969e',
                  callback(value) {
                    return currencyFormatter.format(value);
                  },
                },
                grid: {
                  color: 'rgba(255, 255, 255, 0.06)',
                },
                title: {
                  display: true,
                  text: '費用 (円)',
                  color: '#f2f2f3',
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
