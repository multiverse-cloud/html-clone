#!/usr/bin/env python3
"""Generate premium chart and map pages with SVG-based animated charts."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def page_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en" class="scroll-smooth">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<meta name="theme-color" content="#465fff"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n.no-scrollbar::-webkit-scrollbar{display:none}\n.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@media(prefers-reduced-motion:reduce){.fade-up{animation:none}}\n.chart-card{background:#fff;border:1px solid #e2e8f0;border-radius:.75rem;padding:1.5rem;margin-bottom:1.5rem}\n.dark .chart-card{background:#1e293b;border-color:#334155}\n.chart-card h3{font-size:1rem;font-weight:600;color:#0f172a;margin-bottom:.25rem}\n.dark .chart-card h3{color:#e2e8f0}\n.chart-card p{font-size:.8125rem;color:#94a3b8;margin-bottom:1rem}\n.chart-container{position:relative;width:100%}\n.chart-container svg{width:100%;height:auto}\n.chart-tooltip{position:absolute;background:#1e293b;color:#fff;padding:.375rem .75rem;border-radius:.375rem;font-size:.75rem;pointer-events:none;z-index:10;white-space:nowrap}\n.legend{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1rem}\n.legend-item{display:flex;align-items:center;gap:.375rem;font-size:.75rem;color:#64748b}\n.legend-dot{width:8px;height:8px;border-radius:50%}\n.sparkline-card{display:flex;align-items:center;justify-content:space-between;padding:1rem 1.25rem;background:#fff;border:1px solid #e2e8f0;border-radius:.75rem;margin-bottom:1rem}\n.dark .sparkline-card{background:#1e293b;border-color:#334155}\n.map-container{position:relative;width:100%;overflow:hidden;border-radius:.5rem}\n.map-marker{cursor:pointer;transition:transform .15s}\n.map-marker:hover{transform:scale(1.3)}\n.map-legend{display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1rem}\n.map-legend-item{display:flex;align-items:center;gap:.375rem;font-size:.75rem;color:#64748b}\n' + extra_css + '\n</style>\n</head>\n'

def page_foot(extra_js=''):
    return '<script src="common-loader.js"></script>\n<script src="common-sidebar.js"></script>\n<script src="common-header.js"></script>\n<script src="app-shell.js"></script>\n<script>\n' + extra_js + '\n</script>\n</body>\n</html>'

def sidebar_header():
    return '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="sidebar-overlay fixed inset-0 bg-black/40 z-40 hidden lg:hidden"></div>\n<div class="flex h-screen overflow-hidden">\n<div class="sidebar-container w-72 flex-shrink-0"></div>\n<div class="header-container flex-1 flex flex-col overflow-hidden"></div>\n'

def breadcrumb(*parts):
    h = '<nav class="flex items-center gap-2 text-sm text-slate-400 mb-4">\n'
    for i, p in enumerate(parts):
        if i < len(parts) - 1:
            h += '<a href="#" class="hover:text-slate-600 dark:hover:text-slate-300">' + esc(p) + '</a><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>\n'
        else:
            h += '<span class="text-slate-700 dark:text-slate-200 font-medium">' + esc(p) + '</span>\n'
    h += '</nav>\n'
    return h

def page_header(title, desc):
    return breadcrumb('Home', 'Charts', title) + '<div class="mb-6 fade-up">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">' + esc(title) + '</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">' + esc(desc) + '</p>\n</div>\n'

def svg_line_chart(data_str, color, h=200, area=True):
    """Generate SVG line chart from comma-separated values."""
    vals = [float(x) for x in data_str.split(',')]
    n = len(vals)
    mx = max(vals)
    mn = min(vals)
    rng = mx - mn if mx != mn else 1
    w = 500
    pad = 20
    cw = w - 2 * pad
    ch = h - 2 * pad
    points = []
    for i, v in enumerate(vals):
        x = pad + (i / (n - 1)) * cw
        y = pad + ch - ((v - mn) / rng) * ch
        points.append((x, y))
    polyline = ' '.join([str(x) + ',' + str(y) for x, y in points])
    h_html = '<div class="chart-container"><svg viewBox="0 0 ' + str(w) + ' ' + str(h) + '" xmlns="http://www.w3.org/2000/svg">\n'
    # Grid lines
    for i in range(5):
        gy = pad + (i / 4) * ch
        h_html += '<line x1="' + str(pad) + '" y1="' + str(gy) + '" x2="' + str(w - pad) + '" y2="' + str(gy) + '" stroke="#e2e8f0" stroke-width="0.5"/>\n'
    # Area fill
    if area:
        area_path = 'M' + str(points[0][0]) + ',' + str(h - pad) + ' L' + polyline + ' L' + str(points[-1][0]) + ',' + str(h - pad) + ' Z'
        h_html += '<path d="' + area_path + '" fill="' + color + '" fill-opacity="0.1"/>\n'
    # Line
    h_html += '<polyline points="' + polyline + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n'
    h_html += '<animate attributeName="stroke-dashoffset" from="2000" to="0" dur="1.5s" fill="freeze"/>\n'
    h_html += '</polyline>\n'
    # Dots
    for x, y in points:
        h_html += '<circle cx="' + str(x) + '" cy="' + str(y) + '" r="3" fill="#fff" stroke="' + color + '" stroke-width="2" opacity="0.8"/>\n'
    # Y-axis labels
    for i in range(5):
        gy = pad + (i / 4) * ch
        val = mx - (i / 4) * rng
        h_html += '<text x="' + str(pad - 4) + '" y="' + str(gy + 4) + '" text-anchor="end" font-size="9" fill="#94a3b8">' + str(int(val)) + '</text>\n'
    h_html += '</svg></div>\n'
    return h_html

def svg_bar_chart(data_str, labels_str, color, h=200):
    vals = [float(x) for x in data_str.split(',')]
    labels = labels_str.split(',')
    n = len(vals)
    mx = max(vals)
    w = 500
    pad = 30
    cw = w - 2 * pad
    ch = h - 2 * pad - 20
    bar_w = cw / n * 0.6
    gap = cw / n * 0.4
    h_html = '<div class="chart-container"><svg viewBox="0 0 ' + str(w) + ' ' + str(h) + '" xmlns="http://www.w3.org/2000/svg">\n'
    for i in range(5):
        gy = pad + (i / 4) * ch
        h_html += '<line x1="' + str(pad) + '" y1="' + str(gy) + '" x2="' + str(w - pad) + '" y2="' + str(gy) + '" stroke="#e2e8f0" stroke-width="0.5"/>\n'
        val = mx - (i / 4) * mx
        h_html += '<text x="' + str(pad - 4) + '" y="' + str(gy + 4) + '" text-anchor="end" font-size="9" fill="#94a3b8">' + str(int(val)) + '</text>\n'
    for i, v in enumerate(vals):
        bx = pad + i * (cw / n) + gap / 2
        bh = (v / mx) * ch if mx else 0
        by = pad + ch - bh
        h_html += '<rect x="' + str(bx) + '" y="' + str(by) + '" width="' + str(bar_w) + '" height="' + str(bh) + '" rx="3" fill="' + color + '" opacity="0.85">\n'
        h_html += '<animate attributeName="height" from="0" to="' + str(bh) + '" dur="0.8s" fill="freeze"/>\n'
        h_html += '<animate attributeName="y" from="' + str(pad + ch) + '" to="' + str(by) + '" dur="0.8s" fill="freeze"/>\n'
        h_html += '</rect>\n'
        lx = bx + bar_w / 2
        h_html += '<text x="' + str(lx) + '" y="' + str(h - 8) + '" text-anchor="middle" font-size="9" fill="#94a3b8">' + esc(labels[i] if i < len(labels) else '') + '</text>\n'
    h_html += '</svg></div>\n'
    return h_html

def svg_donut_chart(pct, color, size=120, label='', sub=''):
    r = size / 2 - 10
    circ = 2 * 3.14159 * r
    dash = circ * pct / 100
    gap = circ - dash
    cx = size / 2
    cy = size / 2
    h = '<div class="chart-container" style="max-width:' + str(size) + 'px;margin:0 auto">\n'
    h += '<svg viewBox="0 0 ' + str(size) + ' ' + str(size) + '" xmlns="http://www.w3.org/2000/svg">\n'
    h += '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + str(r) + '" fill="none" stroke="#e2e8f0" stroke-width="8"/>\n'
    h += '<circle cx="' + str(cx) + '" cy="' + str(cy) + '" r="' + str(r) + '" fill="none" stroke="' + color + '" stroke-width="8" stroke-dasharray="' + str(dash) + ' ' + str(gap) + '" stroke-dashoffset="' + str(circ * 0.25) + '" stroke-linecap="round" transform="rotate(-90 ' + str(cx) + ' ' + str(cy) + ')">\n'
    h += '<animate attributeName="stroke-dasharray" from="0 ' + str(circ) + '" to="' + str(dash) + ' ' + str(gap) + '" dur="1s" fill="freeze"/>\n'
    h += '</circle>\n'
    h += '<text x="' + str(cx) + '" y="' + str(cy - 4) + '" text-anchor="middle" font-size="18" font-weight="700" fill="#0f172a">' + str(pct) + '%</text>\n'
    if label:
        h += '<text x="' + str(cx) + '" y="' + str(cy + 14) + '" text-anchor="middle" font-size="9" fill="#94a3b8">' + esc(label) + '</text>\n'
    h += '</svg>\n'
    if sub:
        h += '<p class="text-xs text-center text-slate-400 mt-1">' + esc(sub) + '</p>\n'
    h += '</div>\n'
    return h

def svg_pie_chart(segments, size=160):
    """segments: list of (pct, color, label)"""
    cx = size / 2
    cy = size / 2
    r = size / 2 - 10
    h = '<div class="chart-container" style="max-width:' + str(size) + 'px;margin:0 auto">\n'
    h += '<svg viewBox="0 0 ' + str(size) + ' ' + str(size) + '" xmlns="http://www.w3.org/2000/svg">\n'
    start = -90
    for pct, color, label in segments:
        angle = pct * 3.6
        end = start + angle
        rad_start = 3.14159 * start / 180
        rad_end = 3.14159 * end / 180
        x1 = cx + r * __import__('math').cos(rad_start)
        y1 = cy + r * __import__('math').sin(rad_start)
        x2 = cx + r * __import__('math').cos(rad_end)
        y2 = cy + r * __import__('math').sin(rad_end)
        large = 1 if angle > 180 else 0
        h += '<path d="M' + str(cx) + ',' + str(cy) + ' L' + str(x1) + ',' + str(y1) + ' A' + str(r) + ',' + str(r) + ' 0 ' + str(large) + ' 1 ' + str(x2) + ',' + str(y2) + ' Z" fill="' + color + '" opacity="0.85"/>\n'
        start = end
    h += '</svg>\n</div>\n'
    # Legend
    h += '<div class="legend justify-center">\n'
    for pct, color, label in segments:
        h += '<div class="legend-item"><span class="legend-dot" style="background:' + color + '"></span>' + esc(label) + ' (' + str(pct) + '%)</div>\n'
    h += '</div>\n'
    return h

def svg_radial_chart(pct, color, label='', size=120):
    return svg_donut_chart(pct, color, size, label)

def svg_sparkline(data_str, color, w=100, h=32):
    vals = [float(x) for x in data_str.split(',')]
    n = len(vals)
    mx = max(vals)
    mn = min(vals)
    rng = mx - mn if mx != mn else 1
    points = []
    for i, v in enumerate(vals):
        x = (i / (n - 1)) * w
        y = h - ((v - mn) / rng) * h
        points.append(str(x) + ',' + str(y))
    return '<svg viewBox="0 0 ' + str(w) + ' ' + str(h) + '" xmlns="http://www.w3.org/2000/svg"><polyline points="' + ' '.join(points) + '" fill="none" stroke="' + color + '" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ============================================================
# Line Charts Page
# ============================================================
def gen_line_charts():
    title = 'Line Charts'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'SVG line charts with area fills and animations')

    # Sparklines
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    sparks = [
        ('Revenue', '$48.2K', '+12.5%', '20,22,25,24,28,32,35,38,42,48', '#6366f1'),
        ('Users', '2,847', '+8.3%', '100,120,115,140,160,155,180,200,210,230', '#22c55e'),
        ('Orders', '1,284', '+5.1%', '50,55,60,58,65,70,68,75,80,85', '#f59e0b'),
        ('Bounce Rate', '32.4%', '-2.1%', '45,42,40,38,36,35,34,33,32,32', '#ef4444'),
    ]
    for label, val, change, data, color in sparks:
        up = change.startswith('+')
        h += '<div class="sparkline-card"><div><p class="text-xs text-slate-400 mb-1">' + label + '</p><p class="text-lg font-bold text-slate-900 dark:text-white">' + val + '</p><p class="text-xs ' + ('text-green-600' if up else 'text-red-500') + '">' + change + '</p></div><div style="width:100px">' + svg_sparkline(data, color) + '</div></div>\n'
    h += '</div>\n'

    # Basic Line
    h += '<div class="chart-card fade-up"><h3>Revenue Trend</h3><p>Monthly revenue over the past 12 months</p>\n'
    h += svg_line_chart('12,15,18,16,22,28,32,35,38,42,45,48', '#6366f1', 220)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6366f1"></span>Revenue ($K)</div></div></div>\n'

    # Multi-line
    h += '<div class="chart-card fade-up"><h3>Revenue vs Expenses</h3><p>Comparing income and costs</p>\n'
    h += svg_line_chart('12,15,18,16,22,28,32,35,38,42,45,48', '#6366f1', 220)
    h += svg_line_chart('8,10,12,14,15,18,20,22,24,26,28,30', '#f59e0b', 220)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6366f1"></span>Revenue</div><div class="legend-item"><span class="legend-dot" style="background:#f59e0b"></span>Expenses</div></div></div>\n'

    # Smooth Line
    h += '<div class="chart-card fade-up"><h3>User Growth</h3><p>Weekly active users trend</p>\n'
    h += svg_line_chart('200,220,210,250,280,320,310,350,380,420,460,500', '#22c55e', 200)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>Active Users</div></div></div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Bar Charts Page
# ============================================================
def gen_bar_charts():
    title = 'Bar Charts'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'SVG bar charts with animations and labels')

    h += '<div class="chart-card fade-up"><h3>Monthly Sales</h3><p>Sales performance by month</p>\n'
    h += svg_bar_chart('45,52,48,61,55,67,72,68,75,82,78,90', 'Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec', '#6366f1', 220)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Product Categories</h3><p>Revenue by product category</p>\n'
    h += svg_bar_chart('120,95,78,65,42', 'Electronics,Clothing,Home,Sports,Books', '#22c55e', 200)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Team Performance</h3><p>Tasks completed by team</p>\n'
    h += svg_bar_chart('42,38,55,47,33', 'Design,Engineering,Marketing,Sales,Support', '#f59e0b', 200)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Weekly Traffic</h3><p>Page views by day of week</p>\n'
    h += svg_bar_chart('2400,1800,2100,2300,2600,1200,900', 'Mon,Tue,Wed,Thu,Fri,Sat,Sun', '#8b5cf6', 200)
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Pie Charts Page
# ============================================================
def gen_pie_charts():
    title = 'Pie Charts'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'SVG pie and donut charts with legends')

    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">\n'

    h += '<div class="chart-card fade-up"><h3>Traffic Sources</h3><p>Where your visitors come from</p>\n'
    h += svg_pie_chart([(35, '#6366f1', 'Organic'), (25, '#22c55e', 'Direct'), (20, '#f59e0b', 'Social'), (12, '#ef4444', 'Referral'), (8, '#8b5cf6', 'Email')], 180)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Device Breakdown</h3><p>User sessions by device type</p>\n'
    h += svg_pie_chart([(52, '#6366f1', 'Desktop'), (35, '#22c55e', 'Mobile'), (13, '#f59e0b', 'Tablet')], 180)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Revenue Share</h3><p>Revenue by product line</p>\n'
    h += svg_donut_chart(42, '#6366f1', 140, 'SaaS', '$2.1M')
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6366f1"></span>SaaS 42%</div><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>Services 28%</div><div class="legend-item"><span class="legend-dot" style="background:#f59e0b"></span>Licensing 18%</div><div class="legend-item"><span class="legend-dot" style="background:#8b5cf6"></span>Other 12%</div></div></div>\n'

    h += '<div class="chart-card fade-up"><h3>Completion Rate</h3><p>Task completion this quarter</p>\n'
    h += svg_donut_chart(78, '#22c55e', 140, 'Complete', '312 of 400')
    h += '</div>\n'

    h += '</div>\n'
    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Mixed Charts Page
# ============================================================
def gen_mixed_charts():
    title = 'Mixed Charts'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Combined chart types for comprehensive data visualization')

    # Radial gauges
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    gauges = [
        (87, '#22c55e', 'Uptime', 'SLA Target: 99.9%'),
        (64, '#6366f1', 'CPU Usage', '8 cores active'),
        (42, '#f59e0b', 'Memory', '6.7 GB / 16 GB'),
        (23, '#ef4444', 'Error Rate', 'Below threshold'),
    ]
    for pct, color, label, sub in gauges:
        h += '<div class="chart-card text-center" style="padding:1rem">' + svg_radial_chart(pct, color, label, 100) + '<p class="text-xs text-slate-400 mt-2">' + esc(sub) + '</p></div>\n'
    h += '</div>\n'

    # Line + Bar combo
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">\n'

    h += '<div class="chart-card fade-up"><h3>Revenue & Orders</h3><p>Revenue trend with order volume</p>\n'
    h += svg_line_chart('12,15,18,16,22,28,32,35,38,42,45,48', '#6366f1', 200)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6366f1"></span>Revenue ($K)</div><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>Orders</div></div></div>\n'

    h += '<div class="chart-card fade-up"><h3>Conversion Funnel</h3><p>Visitor to customer conversion</p>\n'
    h += svg_bar_chart('10000,4500,2200,1100,550,280', 'Visitors,Leads,Qualified,Proposals,Negotiation,Closed', '#8b5cf6', 200)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Regional Performance</h3><p>Revenue by region</p>\n'
    h += svg_donut_chart(35, '#6366f1', 120, 'Americas', '$1.8M')
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#6366f1"></span>Americas 35%</div><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>Europe 30%</div><div class="legend-item"><span class="legend-dot" style="background:#f59e0b"></span>Asia 25%</div><div class="legend-item"><span class="legend-dot" style="background:#8b5cf6"></span>Other 10%</div></div></div>\n'

    h += '<div class="chart-card fade-up"><h3>Growth Metrics</h3><p>Key growth indicators</p>\n'
    h += svg_line_chart('5,8,12,18,25,35,48', '#22c55e', 180)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>MRR Growth</div></div></div>\n'

    h += '</div>\n'
    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Realtime Charts Page
# ============================================================
def gen_realtime_charts():
    title = 'Realtime Charts'
    h = page_head(title, '\n@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}\n.pulse{animation:pulse 2s ease-in-out infinite}\n.live-dot{width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block;animation:pulse 1.5s ease-in-out infinite}\n')
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Live-updating charts with real-time data simulation')

    # Live Stats
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    for label, val, icon_color in [('Active Users', '1,247', '#22c55e'), ('Requests/sec', '342', '#6366f1'), ('Avg Latency', '45ms', '#f59e0b'), ('Error Rate', '0.12%', '#ef4444')]:
        h += '<div class="chart-card" style="padding:1rem"><div class="flex items-center gap-2 mb-2"><span class="live-dot"></span><p class="text-xs text-slate-400">' + label + '</p></div><p class="text-xl font-bold text-slate-900 dark:text-white" id="live-' + label.replace(' ','-').replace('/','').lower() + '">' + val + '</p></div>\n'
    h += '</div>\n'

    # Realtime line chart (JS-driven)
    h += '<div class="chart-card fade-up"><h3 class="flex items-center gap-2">Live Traffic <span class="live-dot"></span></h3><p>Real-time page views per second</p>\n'
    h += '<div class="chart-container"><canvas id="realtime-chart" height="200" style="width:100%"></canvas></div></div>\n'

    # Realtime bar chart
    h += '<div class="chart-card fade-up"><h3 class="flex items-center gap-2">Server Load <span class="live-dot"></span></h3><p>Current server resource utilization</p>\n'
    h += '<div class="grid grid-cols-4 gap-4" id="server-gauges">\n'
    for label, pct, color in [('CPU', 67, '#6366f1'), ('Memory', 54, '#22c55e'), ('Disk', 38, '#f59e0b'), ('Network', 72, '#8b5cf6')]:
        h += '<div class="text-center">' + svg_donut_chart(pct, color, 90, label) + '</div>\n'
    h += '</div></div>\n'

    # Event Feed
    h += '<div class="chart-card fade-up"><h3 class="flex items-center gap-2">Event Stream <span class="live-dot"></span></h3><p>Recent system events</p>\n'
    h += '<div id="event-feed" class="space-y-2 max-h-64 overflow-y-auto">\n'
    for msg, time_ago in [
        ('User alice@acme.com logged in', '2s ago'),
        ('API request processed in 45ms', '5s ago'),
        ('Cache hit ratio: 94.2%', '8s ago'),
        ('New signup: bob@example.com', '12s ago'),
        ('Payment processed: $245.00', '15s ago'),
    ]:
        h += '<div class="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-800 last:border-0"><p class="text-sm text-slate-600 dark:text-slate-400">' + esc(msg) + '</p><span class="text-xs text-slate-400">' + esc(time_ago) + '</span></div>\n'
    h += '</div></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
// Realtime chart using canvas
var rtCanvas=document.getElementById('realtime-chart');
var rtCtx=rtCanvas.getContext('2d');
var rtData=[];
for(var i=0;i<60;i++)rtData.push(Math.random()*50+20);
function drawRealtime(){
  var w=rtCanvas.width=rtCanvas.offsetWidth;
  var h=rtCanvas.height=200;
  rtCtx.clearRect(0,0,w,h);
  // Grid
  rtCtx.strokeStyle='#e2e8f0';rtCtx.lineWidth=0.5;
  for(var i=0;i<5;i++){var y=i*40+20;rtCtx.beginPath();rtCtx.moveTo(0,y);rtCtx.lineTo(w,y);rtCtx.stroke()}
  // Area
  var max=Math.max.apply(null,rtData)+10;
  rtCtx.beginPath();
  rtCtx.moveTo(0,h);
  for(var i=0;i<rtData.length;i++){var x=i*(w/(rtData.length-1));var y=h-(rtData[i]/max)*(h-20);rtCtx.lineTo(x,y)}
  rtCtx.lineTo(w,h);rtCtx.closePath();
  rtCtx.fillStyle='rgba(99,102,241,0.1)';rtCtx.fill();
  // Line
  rtCtx.beginPath();
  for(var i=0;i<rtData.length;i++){var x=i*(w/(rtData.length-1));var y=h-(rtData[i]/max)*(h-20);if(i===0)rtCtx.moveTo(x,y);else rtCtx.lineTo(x,y)}
  rtCtx.strokeStyle='#6366f1';rtCtx.lineWidth=2;rtCtx.stroke();
  // Dot at end
  var lastX=(rtData.length-1)*(w/(rtData.length-1));
  var lastY=h-(rtData[rtData.length-1]/max)*(h-20);
  rtCtx.beginPath();rtCtx.arc(lastX,lastY,4,0,Math.PI*2);rtCtx.fillStyle='#6366f1';rtCtx.fill();
  rtCtx.beginPath();rtCtx.arc(lastX,lastY,7,0,Math.PI*2);rtCtx.strokeStyle='rgba(99,102,241,0.3)';rtCtx.lineWidth=2;rtCtx.stroke();
}
setInterval(function(){
  rtData.shift();
  rtData.push(Math.random()*50+20);
  drawRealtime();
},1000);
drawRealtime();
// Simulate live stat updates
setInterval(function(){
  var el=document.getElementById('live-active-users');
  if(el)el.textContent=(1200+Math.floor(Math.random()*100)).toLocaleString();
  var el2=document.getElementById('live-requestssec');
  if(el2)el2.textContent=(300+Math.floor(Math.random()*80));
  var el3=document.getElementById('live-avglatency');
  if(el3)el3.textContent=(35+Math.floor(Math.random()*20))+'ms';
},2000);
'''
    h += page_foot(js)
    return h

# ============================================================
# Maps Overview Page
# ============================================================
def gen_maps_overview():
    title = 'Maps Overview'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Interactive SVG maps with markers and metrics')

    # World Map (simplified SVG)
    h += '<div class="chart-card fade-up"><h3>Global User Distribution</h3><p>Active users by region</p>\n'
    h += '<div class="map-container" style="background:#f8fafc;border-radius:.5rem;padding:1rem">\n'
    # Simplified world map using SVG paths
    h += '<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg" style="width:100%">\n'
    h += '<rect width="800" height="400" fill="#f1f5f9" rx="8"/>\n'
    # Simplified continent shapes
    h += '<ellipse cx="200" cy="180" rx="80" ry="60" fill="#dbeafe" stroke="#93c5fd" stroke-width="1"/>\n'  # North America
    h += '<ellipse cx="220" cy="300" rx="40" ry="50" fill="#dbeafe" stroke="#93c5fd" stroke-width="1"/>\n'  # South America
    h += '<ellipse cx="400" cy="170" rx="60" ry="70" fill="#dcfce7" stroke="#86efac" stroke-width="1"/>\n'  # Europe
    h += '<ellipse cx="420" cy="280" rx="50" ry="60" fill="#fef3c7" stroke="#fde68a" stroke-width="1"/>\n'  # Africa
    h += '<ellipse cx="580" cy="200" rx="90" ry="70" fill="#eef2ff" stroke="#a5b4fc" stroke-width="1"/>\n'  # Asia
    h += '<ellipse cx="640" cy="320" rx="40" ry="30" fill="#fce7f3" stroke="#f9a8d4" stroke-width="1"/>\n'  # Australia
    # Markers
    markers = [
        (180, 160, '#6366f1', 'New York', '2,847'),
        (200, 190, '#6366f1', 'Chicago', '1,203'),
        (380, 150, '#22c55e', 'London', '3,421'),
        (420, 160, '#22c55e', 'Berlin', '1,856'),
        (560, 180, '#f59e0b', 'Tokyo', '4,102'),
        (580, 220, '#f59e0b', 'Shanghai', '2,945'),
        (620, 310, '#8b5cf6', 'Sydney', '1,567'),
        (210, 290, '#ef4444', 'Sao Paulo', '2,134'),
    ]
    for mx, my, color, city, users in markers:
        h += '<g class="map-marker"><circle cx="' + str(mx) + '" cy="' + str(my) + '" r="6" fill="' + color + '" opacity="0.8"/><circle cx="' + str(mx) + '" cy="' + str(my) + '" r="12" fill="' + color + '" opacity="0.2"/><title>' + esc(city) + ': ' + esc(users) + ' users</title></g>\n'
    h += '</svg>\n</div>\n'
    # Legend
    h += '<div class="map-legend"><div class="map-legend-item"><span class="legend-dot" style="background:#6366f1"></span>Americas</div><div class="map-legend-item"><span class="legend-dot" style="background:#22c55e"></span>Europe</div><div class="map-legend-item"><span class="legend-dot" style="background:#f59e0b"></span>Asia</div><div class="map-legend-item"><span class="legend-dot" style="background:#8b5cf6"></span>Oceania</div><div class="map-legend-item"><span class="legend-dot" style="background:#ef4444"></span>South America</div></div></div>\n'

    # Regional Stats
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 fade-up">\n'
    regions = [
        ('North America', '8,421', '+12%', '#6366f1'),
        ('Europe', '6,234', '+8%', '#22c55e'),
        ('Asia Pacific', '9,876', '+24%', '#f59e0b'),
        ('Rest of World', '3,567', '+5%', '#8b5cf6'),
    ]
    for region, users, growth, color in regions:
        h += '<div class="chart-card" style="padding:1rem;border-left:3px solid ' + color + '"><p class="text-xs text-slate-400 mb-1">' + esc(region) + '</p><p class="text-lg font-bold text-slate-900 dark:text-white">' + users + '</p><p class="text-xs text-green-600">' + growth + '</p></div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Heatmap Page
# ============================================================
def gen_heatmap():
    title = 'Activity Heatmap'
    h = page_head(title, '\n.heatmap-cell{width:14px;height:14px;border-radius:2px;transition:transform .1s}\n.heatmap-cell:hover{transform:scale(1.5);z-index:1}\n')
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Activity heatmap showing contribution patterns')

    h += '<div class="chart-card fade-up"><h3>Contribution Activity</h3><p>Daily activity over the past 20 weeks</p>\n'
    h += '<div class="overflow-x-auto">\n<div style="display:inline-flex;gap:3px;padding:.5rem">\n'
    # Generate heatmap grid
    import random
    random.seed(42)
    levels = ['bg-slate-100 dark:bg-slate-800', 'bg-green-200 dark:bg-green-900', 'bg-green-400 dark:bg-green-700', 'bg-green-600 dark:bg-green-500', 'bg-green-800 dark:bg-green-300']
    for week in range(20):
        h += '<div style="display:flex;flex-direction:column;gap:3px">\n'
        for day in range(7):
            lvl = random.choices([0, 1, 2, 3, 4], weights=[30, 25, 20, 15, 10])[0]
            h += '<div class="heatmap-cell ' + levels[lvl] + '" title="Week ' + str(week + 1) + ', Day ' + str(day + 1) + ': Level ' + str(lvl) + '"></div>\n'
        h += '</div>\n'
    h += '</div>\n</div>\n'
    # Legend
    h += '<div class="flex items-center gap-2 mt-3"><span class="text-xs text-slate-400">Less</span>'
    for lvl_class in levels:
        h += '<div class="heatmap-cell ' + lvl_class + '"></div>'
    h += '<span class="text-xs text-slate-400">More</span></div></div>\n'

    # Time-of-day heatmap
    h += '<div class="chart-card fade-up"><h3>Hourly Activity</h3><p>Activity by hour of day (Mon-Sun)</p>\n'
    h += '<div class="overflow-x-auto"><table class="w-full" style="border-collapse:separate;border-spacing:2px">\n<thead><tr><th class="text-xs text-slate-400 p-1"></th>'
    for hr in range(24):
        h += '<th class="text-xs text-slate-400 p-1 text-center">' + str(hr).zfill(2) + '</th>'
    h += '</tr></thead><tbody>\n'
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    for d in days:
        h += '<tr><td class="text-xs text-slate-400 p-1">' + d + '</td>'
        for hr in range(24):
            intensity = random.choices([0, 1, 2, 3, 4], weights=[40, 20, 20, 12, 8] if hr < 6 or hr > 22 else [10, 15, 25, 30, 20])[0]
            bg_colors = ['#f1f5f9', '#dcfce7', '#bbf7d0', '#86efac', '#22c55e']
            h += '<td style="background:' + bg_colors[intensity] + ';border-radius:2px;min-width:16px;height:20px" title="' + d + ' ' + str(hr).zfill(2) + ':00 - Level ' + str(intensity) + '"></td>'
        h += '</tr>\n'
    h += '</tbody></table></div></div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Users Geography Page
# ============================================================
def gen_users_geo():
    title = 'Users Geography'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Geographic distribution of users')

    # Top Countries
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">\n'
    h += '<div class="lg:col-span-2">\n'
    h += '<div class="chart-card fade-up"><h3>Top Countries</h3><p>Users by country</p>\n'
    h += '<div class="space-y-3">\n'
    countries = [
        ('United States', 8421, 35, '#6366f1'),
        ('United Kingdom', 3421, 14, '#22c55e'),
        ('Germany', 2856, 12, '#f59e0b'),
        ('Japan', 4102, 17, '#8b5cf6'),
        ('Canada', 2103, 9, '#ef4444'),
        ('Australia', 1567, 6, '#06b6d4'),
        ('France', 1234, 5, '#ec4899'),
        ('Brazil', 2134, 8, '#14b8a6'),
    ]
    for country, users, pct, color in countries:
        h += '<div class="flex items-center gap-3"><span class="text-sm font-medium text-slate-700 dark:text-slate-300 w-32">' + esc(country) + '</span><div class="flex-1 h-6 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div class="h-full rounded-full transition-all" style="width:' + str(pct * 2.5) + '%;background:' + color + '"></div></div><span class="text-sm text-slate-500 w-16 text-right">' + str(users).replace(',', ' ') + '</span><span class="text-xs text-slate-400 w-10 text-right">' + str(pct) + '%</span></div>\n'
    h += '</div></div>\n'
    h += '</div>\n'

    # Side stats
    h += '<div class="space-y-4">\n'
    for label, val, change in [('Total Users', '24,847', '+12.5%'), ('Countries', '42', '+3'), ('Cities', '186', '+12'), ('Avg Session', '4m 32s', '+8%')]:
        h += '<div class="chart-card" style="padding:1rem"><p class="text-xs text-slate-400 mb-1">' + label + '</p><p class="text-lg font-bold text-slate-900 dark:text-white">' + val + '</p><p class="text-xs text-green-600">' + change + '</p></div>\n'
    h += '</div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Regions Page
# ============================================================
def gen_regions():
    title = 'Regional Analytics'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Regional performance metrics and comparisons')

    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">\n'

    h += '<div class="chart-card fade-up"><h3>Revenue by Region</h3><p>Quarterly revenue comparison</p>\n'
    h += svg_bar_chart('1800,1200,2100,800', 'Americas,Europe,Asia,Other', '#6366f1', 200)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Market Share</h3><p>Regional market distribution</p>\n'
    h += svg_pie_chart([(35, '#6366f1', 'Americas'), (28, '#22c55e', 'Europe'), (25, '#f59e0b', 'Asia Pacific'), (12, '#8b5cf6', 'Other')], 160)
    h += '</div>\n'

    h += '<div class="chart-card fade-up"><h3>Growth Trend</h3><p>Year-over-year growth by region</p>\n'
    h += svg_line_chart('100,115,130,142,158,175,190', '#22c55e', 180)
    h += '<div class="legend"><div class="legend-item"><span class="legend-dot" style="background:#22c55e"></span>Growth %</div></div></div>\n'

    h += '<div class="chart-card fade-up"><h3>Customer Satisfaction</h3><p>NPS score by region</p>\n'
    h += svg_donut_chart(72, '#6366f1', 120, 'NPS', 'Score: 72')
    h += '</div>\n'

    h += '</div>\n'

    # Comparison table
    h += '<div class="chart-card fade-up"><h3>Regional Comparison</h3><p>Key metrics by region</p>\n'
    h += '<div class="overflow-x-auto"><table class="data-table"><thead><tr><th>Region</th><th>Users</th><th>Revenue</th><th>Growth</th><th>NPS</th></tr></thead><tbody>\n'
    for region, users, rev, growth, nps in [('Americas', '8,421', '$1.8M', '+12%', '72'), ('Europe', '6,234', '$1.2M', '+8%', '68'), ('Asia Pacific', '9,876', '$2.1M', '+24%', '75'), ('Other', '3,567', '$0.8M', '+5%', '65')]:
        h += '<tr><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(region) + '</td><td>' + users + '</td><td>' + rev + '</td><td class="text-green-600">' + growth + '</td><td>' + nps + '</td></tr>\n'
    h += '</tbody></table></div></div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# Generate all chart/map pages
pages = [
    ('72-charts-line.html', gen_line_charts),
    ('73-charts-bar.html', gen_bar_charts),
    ('74-charts-pie.html', gen_pie_charts),
    ('75-charts-mixed.html', gen_mixed_charts),
    ('76-charts-realtime.html', gen_realtime_charts),
    ('77-maps-overview.html', gen_maps_overview),
    ('78-maps-heatmap.html', gen_heatmap),
    ('79-maps-users-geo.html', gen_users_geo),
    ('80-maps-regions.html', gen_regions),
]

print('Generating premium chart & map pages...')
for fname, gen_fn in pages:
    path = os.path.join(OUT, fname)
    html = gen_fn()
    with open(path, 'w') as f:
        f.write(html)
    sz = os.path.getsize(path)
    print('  ' + fname + ': ' + str(sz // 1024) + 'KB')

print('Done! All chart & map pages generated.')
