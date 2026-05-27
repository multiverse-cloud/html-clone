#!/usr/bin/env python3
"""Generate premium dashboard pages."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def attr_esc(s):
    return s.replace('&','&amp;').replace('"','&quot;').replace("'",'&#39;').replace('<','&lt;').replace('>','&gt;')

def write_file(filename, content):
    path = os.path.join(OUT, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    sz = os.path.getsize(path)
    print(f'  {filename}: {sz//1024}KB')

def page_head(title, desc, extra_css=''):
    return (
        '<!DOCTYPE html>\n<html lang="en" class="scroll-smooth">\n<head>\n'
        '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<meta name="description" content="{desc}">\n'
        f'<title>{title}</title>\n'
        '<style>\n'
        '.no-scrollbar::-webkit-scrollbar{display:none}.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}\n'
        '@keyframes slideDown{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}.animate-slideDown{animation:slideDown .2s ease-out}\n'
        '@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}.animate-fadeUp{animation:fadeUp .4s ease-out both}\n'
        '@keyframes countUp{from{opacity:0}to{opacity:1}}\n'
        '@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}\n'
        + extra_css + '\n'
        '</style>\n'
        '<link rel="stylesheet" href="tailwind-production.css">\n'
        '<link rel="stylesheet" href="pro-styles.css">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap" rel="stylesheet">\n'
        '</head>\n'
        '<body class="bg-gray-50 text-gray-800 font-sans dark:bg-gray-900 dark:text-gray-100">\n'
        '<div id="sidebar-overlay" class="fixed inset-0 bg-black/40 z-40 hidden lg:hidden" onclick="window.toggleSidebar&&toggleSidebar()"></div>\n'
        '<div class="flex h-screen overflow-hidden">\n'
        '<div id="sidebar-container"></div>\n'
        '<div class="flex-1 flex flex-col overflow-hidden">\n'
        '<div id="header-container"></div>\n'
        '<main class="flex-1 overflow-y-auto overflow-x-hidden px-4 md:px-6 2xl:px-10 py-6" tabindex="-1">\n'
        '<div class="mx-auto w-full max-w-screen-2xl">\n'
    )

def page_foot(extra_js=''):
    return (
        '</div>\n</main>\n</div>\n</div>\n'
        '<script src="common-loader.js"></script>\n'
        '<script src="common-sidebar.js"></script>\n'
        '<script src="common-header.js"></script>\n'
        '<script src="app-shell.js"></script>\n'
        '<script>\n'
        'document.addEventListener("DOMContentLoaded",function(){'
        'document.querySelectorAll("[data-counter]").forEach(function(el){'
        'var t=el.dataset.counter;if(!t)return;var n=parseFloat(t.replace(/[^0-9.-]/g,""));'
        'var pre=t.replace(/[0-9.,-]/g,"");var dur=1200;var s=null;var st=null;'
        'function step(ts){if(!st)st=ts;var p=Math.min((ts-st)/dur,1);'
        'var v=Math.floor(p*n);if(n>=1000)el.textContent=pre+v.toLocaleString();'
        'else if(String(n).includes("."))el.textContent=pre+(p*n).toFixed(2);'
        'else el.textContent=pre+v;if(p<1)requestAnimationFrame(step);else el.textContent=t;'
        '}requestAnimationFrame(step);});'
        'document.querySelectorAll("[data-sparkline]").forEach(function(el){'
        'var d=el.dataset.sparkline;if(!d)return;var vals=d.split(",").map(Number);'
        'var w=el.offsetWidth||80;var h=el.offsetHeight||32;var max=Math.max.apply(null,vals);'
        'var min=Math.min.apply(null,vals);var range=max-min||1;var step=w/(vals.length-1);'
        'var pts=vals.map(function(v,i){return i*step+","+((1-(v-min)/range)*h);}).join(" ");'
        'el.innerHTML=\'<svg viewBox="0 0 \'+w+\' \'+h+\'" class="w-full h-full"><polyline fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" points="\'+pts+\'"/></svg>\';'
        '});});\n'
        + extra_js + '\n'
        '</script>\n</body>\n</html>'
    )

def breadcrumb(*parts):
    nav = '<nav class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-4">'
    nav += '<a href="01-main-dashboard.html" class="hover:text-blue-600">Home</a>'
    for i, p in enumerate(parts):
        nav += '<svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'
        if i == len(parts) - 1:
            nav += f'<span class="text-gray-800 dark:text-gray-200 font-medium">{p}</span>'
        else:
            nav += f'<a href="#" class="hover:text-blue-600">{p}</a>'
    nav += '</nav>'
    return nav

def kpi_card(label, value, change, change_dir, icon_bg, icon_color, icon_path, spark_data=''):
    change_cls = 'text-green-600' if change_dir == 'up' else 'text-red-500'
    arrow = '\u2191' if change_dir == 'up' else '\u2193'
    spark_attr = f' data-sparkline="{spark_data}"' if spark_data else ''
    spark_html = f'<div class="w-20 h-8 text-{icon_color.split("-")[1]}-500"{spark_attr}></div>' if spark_data else ''
    return (
        f'<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5 animate-fadeUp">'
        f'<div class="flex items-center justify-between mb-3">'
        f'<span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wide">{label}</span>'
        f'<div class="flex items-center gap-2">'
        f'{spark_html}'
        f'<div class="w-8 h-8 {icon_bg} rounded-lg flex items-center justify-center">'
        f'<svg class="w-4 h-4 {icon_color}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/></svg></div></div></div>'
        f'<p class="text-2xl font-bold text-gray-900 dark:text-white" data-counter="{value}">{value}</p>'
        f'<p class="text-xs {change_cls} mt-1 font-medium">{arrow} {change} vs last month</p>'
        f'</div>'
    )

def svg_line_chart(data_str, color='#3b82f6', height=160, id_suffix=''):
    """Generate an SVG line chart from comma-separated values."""
    vals = [float(x) for x in data_str.split(',')]
    n = len(vals)
    if n < 2: return ''
    w = 500
    h = height
    mx = max(vals)
    mn = min(vals)
    rng = mx - mn or 1
    pad = 20
    cw = w - 2*pad
    ch = h - 2*pad
    step = cw / (n-1)
    pts = []
    area_pts = [f'{pad},{h-pad}']
    for i, v in enumerate(vals):
        x = pad + i*step
        y = pad + (1-(v-mn)/rng)*ch
        pts.append(f'{x:.1f},{y:.1f}')
        area_pts.append(f'{x:.1f},{y:.1f}')
    area_pts.append(f'{pad+cw},{h-pad}')
    points_str = ' '.join(pts)
    area_str = ' '.join(area_pts)
    # X-axis labels
    labels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    label_html = ''
    for i in range(0, n, max(1, n//6)):
        x = pad + i*step
        lbl = labels[i] if i < len(labels) else str(i+1)
        label_html += f'<text x="{x:.0f}" y="{h-2}" text-anchor="middle" class="text-[10px] fill-gray-400">{lbl}</text>'
    return (
        f'<svg viewBox="0 0 {w} {h}" class="w-full" style="height:{h}px" id="line-chart{id_suffix}">'
        f'<defs><linearGradient id="areaGrad{id_suffix}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{color}" stop-opacity="0.15"/>'
        f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/></linearGradient></defs>'
        f'<polygon fill="url(#areaGrad{id_suffix})" points="{area_str}"/>'
        f'<polyline fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" points="{points_str}"/>'
        f'{label_html}'
        f'</svg>'
    )

def svg_bar_chart(data_str, color='#3b82f6', height=160, id_suffix=''):
    vals = [float(x) for x in data_str.split(',')]
    n = len(vals)
    if n < 1: return ''
    w = 500
    h = height
    mx = max(vals)
    pad = 20
    cw = w - 2*pad
    ch = h - 2*pad - 15
    bar_w = cw / n * 0.6
    gap = cw / n * 0.4
    bars_html = ''
    labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun','W2','W3','W4','W5','W6']
    for i, v in enumerate(vals):
        x = pad + i*(cw/n) + gap/2
        bh = (v/mx)*ch if mx > 0 else 0
        y = pad + ch - bh
        lbl = labels[i] if i < len(labels) else str(i+1)
        bars_html += (
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bh:.1f}" rx="3" fill="{color}" opacity="0.85"/>'
            f'<text x="{x+bar_w/2:.0f}" y="{h-2}" text-anchor="middle" class="text-[10px] fill-gray-400">{lbl}</text>'
        )
    return f'<svg viewBox="0 0 {w} {h}" class="w-full" style="height:{h}px">{bars_html}</svg>'

def svg_donut_chart(pct, color='#3b82f6', size=120, label='', sub=''):
    r = 40
    circ = 2 * 3.14159 * r
    offset = circ * (1 - pct/100)
    return (
        f'<div class="flex flex-col items-center">'
        f'<svg viewBox="0 0 100 100" width="{size}" height="{size}">'
        f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="#e5e7eb" stroke-width="8" class="dark:stroke-gray-700"/>'
        f'<circle cx="50" cy="50" r="{r}" fill="none" stroke="{color}" stroke-width="8" '
        f'stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}" '
        f'stroke-linecap="round" transform="rotate(-90 50 50)" style="transition:stroke-dashoffset .6s ease"/>'
        f'<text x="50" y="46" text-anchor="middle" class="text-lg font-bold fill-gray-900 dark:fill-white" style="font-size:16px">{pct}%</text>'
        f'<text x="50" y="60" text-anchor="middle" class="text-[8px] fill-gray-400">{sub}</text>'
        f'</svg>'
        f'<p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{label}</p>'
        f'</div>'
    )

def status_badge(text, cls):
    return f'<span class="px-2 py-0.5 rounded-full text-xs font-medium {cls}">{text}</span>'

# ============================================================
# DASHBOARD 1: SaaS Analytics
# ============================================================
def gen_saas_dashboard():
    h = page_head('SaaS Dashboard \u2014 mtverse', 'Production-ready SaaS Analytics Dashboard with KPIs, charts, tables, and dark mode')
    h += breadcrumb('Dashboards', 'SaaS Analytics')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">SaaS Analytics</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Real-time metrics and performance insights</p></div>'
    h += '<div class="flex gap-2"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300"><option>Last 30 days</option><option>Last 7 days</option><option>Last 90 days</option><option>This year</option></select>'
    h += '<button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 inline-flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>Export</button></div></div>'

    # KPI Cards
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Monthly Revenue', '$48,295', '12.4%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', '30,42,38,55,48,62,58,72,65,78,82,95')
    h += kpi_card('Active Users', '3,842', '8.1%', 'up', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', '2800,3100,3200,3400,3500,3600,3700,3842')
    h += kpi_card('API Requests', '1.2M', '2.3%', 'down', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600', 'M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z', '1.4,1.3,1.35,1.25,1.3,1.2,1.18,1.2')
    h += kpi_card('Conversion Rate', '4.67%', '0.5%', 'up', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600', 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6', '3.2,3.5,3.8,4.0,4.2,4.3,4.5,4.67')
    h += '</div>'

    # Charts Row
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    # Revenue Line Chart
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Revenue Overview</h2>'
    h += '<div class="flex gap-1"><button class="px-2.5 py-1 text-xs bg-blue-600 text-white rounded-md">Monthly</button><button class="px-2.5 py-1 text-xs text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Weekly</button></div></div>'
    h += svg_line_chart('28,35,32,45,42,55,52,68,62,75,72,85', '#3b82f6', 180, '-revenue')
    h += '</div>'
    # Donut + Top Channels
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Traffic Sources</h2>'
    h += '<div class="flex justify-center gap-6 mb-4">'
    h += svg_donut_chart(42, '#3b82f6', 90, 'Direct', '1,610')
    h += svg_donut_chart(28, '#10b981', 90, 'Organic', '1,075')
    h += svg_donut_chart(18, '#8b5cf6', 90, 'Referral', '691')
    h += '</div>'
    h += '<div class="space-y-2.5 mt-4">'
    for name, pct, color in [('Direct','42%','bg-blue-500'),('Organic Search','28%','bg-emerald-500'),('Referral','18%','bg-violet-500'),('Social','12%','bg-amber-500')]:
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{pct}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"><div class="{color} h-1.5 rounded-full" style="width:{pct}"></div></div></div>'
    h += '</div></div>'
    h += '</div>'

    # Second row: Bar chart + Activity
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    # Bar chart
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">User Signups</h2><span class="text-xs text-gray-400">Last 7 days</span></div>'
    h += svg_bar_chart('120,185,145,210,175,95,160', '#10b981', 160, '-signups')
    h += '</div>'
    # Activity feed
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Recent Activity</h2>'
    h += '<div class="space-y-4">'
    activities = [
        ('https://i.pravatar.cc/32?img=1', 'Sarah Mitchell', 'upgraded to Pro plan', '2 min ago', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600'),
        ('https://i.pravatar.cc/32?img=3', 'James Patel', 'created a new project', '15 min ago', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600'),
        ('https://i.pravatar.cc/32?img=5', 'Emily Chen', 'deployed to production', '1 hour ago', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600'),
        ('https://i.pravatar.cc/32?img=8', 'Marco Rivera', 'added 3 team members', '2 hours ago', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600'),
        ('https://i.pravatar.cc/32?img=11', 'Lisa Wang', 'generated API key', '3 hours ago', 'bg-rose-50 dark:bg-rose-900/30', 'text-rose-600'),
    ]
    for img, name, action, time, ibg, ic in activities:
        h += f'<div class="flex items-start gap-3"><img src="{img}" class="w-8 h-8 rounded-full"><div class="flex-1 min-w-0"><p class="text-sm text-gray-700 dark:text-gray-300"><span class="font-medium text-gray-900 dark:text-white">{name}</span> {action}</p><p class="text-xs text-gray-400 mt-0.5">{time}</p></div></div>'
    h += '</div></div>'
    h += '</div>'

    # Transactions table
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Recent Transactions</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View all</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Customer</th><th class="pb-2 text-left font-medium">Plan</th><th class="pb-2 text-left font-medium">Amount</th><th class="pb-2 text-left font-medium">Status</th><th class="pb-2 text-left font-medium">Date</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    txns = [
        ('Sarah Mitchell','Pro','$49.00','Paid','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300','May 24, 2026'),
        ('James Patel','Enterprise','$299.00','Paid','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300','May 23, 2026'),
        ('Laura Chen','Starter','$12.00','Pending','bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300','May 23, 2026'),
        ('Marco Rivera','Pro','$49.00','Failed','bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-300','May 22, 2026'),
        ('Aisha Khan','Business','$99.00','Paid','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300','May 22, 2026'),
        ('Tom Bradley','Pro','$49.00','Refunded','bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300','May 21, 2026'),
    ]
    for name, plan, amt, status, scls, date in txns:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-3 font-medium text-gray-800 dark:text-gray-200">{name}</td><td class="py-3 text-gray-600 dark:text-gray-400">{plan}</td><td class="py-3 font-medium text-gray-800 dark:text-gray-200">{amt}</td><td class="py-3"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{status}</span></td><td class="py-3 text-gray-500 dark:text-gray-400">{date}</td></tr>'
    h += '</tbody></table></div></div>'

    h += page_foot()
    write_file('01-main-dashboard.html', h)

# ============================================================
# DASHBOARD 2: Ecommerce
# ============================================================
def gen_ecommerce_dashboard():
    h = page_head('Ecommerce Dashboard \u2014 mtverse', 'Production-ready Ecommerce Dashboard with sales, orders, products, and revenue analytics')
    h += breadcrumb('Dashboards', 'Ecommerce')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">Ecommerce Overview</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Sales performance and order management</p></div>'
    h += '<div class="flex gap-2"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300"><option>This Month</option><option>Last Month</option><option>This Quarter</option></select></div></div>'

    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Total Sales', '$124,563', '18.2%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z', '85,92,78,105,112,98,124,135,128,142,156,168')
    h += kpi_card('Orders', '1,847', '5.4%', 'up', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z', '120,145,132,168,155,178,165,190,175,185,195,210')
    h += kpi_card('Avg Order Value', '$67.42', '3.1%', 'up', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600', 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z', '58,60,62,63,64,65,66,67,67,68,67,67')
    h += kpi_card('Refund Rate', '2.3%', '0.8%', 'down', 'bg-rose-50 dark:bg-rose-900/30', 'text-rose-600', 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z', '3.1,2.9,2.8,2.7,2.6,2.5,2.4,2.3,2.3,2.3,2.3,2.3')
    h += '</div>'

    # Charts
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Sales Trend</h2>'
    h += '<div class="flex gap-1"><button class="px-2.5 py-1 text-xs bg-blue-600 text-white rounded-md">Revenue</button><button class="px-2.5 py-1 text-xs text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Orders</button></div></div>'
    h += svg_line_chart('45,52,48,65,58,72,68,85,78,92,88,105', '#3b82f6', 180, '-ecom')
    h += '</div>'
    # Category breakdown
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Category Breakdown</h2>'
    h += '<div class="flex justify-center gap-4 mb-4">'
    h += svg_donut_chart(35, '#3b82f6', 80, 'Electronics', '')
    h += svg_donut_chart(25, '#10b981', 80, 'Clothing', '')
    h += svg_donut_chart(20, '#f59e0b', 80, 'Home', '')
    h += '</div>'
    h += '<div class="space-y-2">'
    for name, pct, color in [('Electronics','35%','bg-blue-500'),('Clothing','25%','bg-emerald-500'),('Home & Garden','20%','bg-amber-500'),('Sports','12%','bg-violet-500'),('Other','8%','bg-gray-400')]:
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{pct}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"><div class="{color} h-1.5 rounded-full" style="width:{pct}"></div></div></div>'
    h += '</div></div></div>'

    # Top Products + Recent Orders
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    # Top Products
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Top Products</h2>'
    h += '<div class="space-y-3">'
    products = [
        ('Wireless Headphones Pro', '2,341 sold', '$89.99', 'bg-blue-100 dark:bg-blue-900/30 text-blue-600'),
        ('Smart Watch Ultra', '1,892 sold', '$249.99', 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600'),
        ('Laptop Stand Adjustable', '1,567 sold', '$45.99', 'bg-violet-100 dark:bg-violet-900/30 text-violet-600'),
        ('USB-C Hub 7-in-1', '1,234 sold', '$34.99', 'bg-amber-100 dark:bg-amber-900/30 text-amber-600'),
        ('Mechanical Keyboard', '987 sold', '$129.99', 'bg-rose-100 dark:bg-rose-900/30 text-rose-600'),
    ]
    for name, sold, price, icls in products:
        h += f'<div class="flex items-center gap-3"><div class="w-10 h-10 rounded-lg {icls} flex items-center justify-center text-xs font-bold">#</div><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white truncate">{name}</p><p class="text-xs text-gray-500">{sold}</p></div><p class="text-sm font-semibold text-gray-900 dark:text-white">{price}</p></div>'
    h += '</div></div>'
    # Recent Orders
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Recent Orders</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View all</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Order ID</th><th class="pb-2 text-left font-medium">Customer</th><th class="pb-2 text-left font-medium">Total</th><th class="pb-2 text-left font-medium">Status</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    orders = [
        ('#ORD-7291','Sarah M.','$189.97','Shipped','bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'),
        ('#ORD-7290','James P.','$249.99','Delivered','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('#ORD-7289','Emily C.','$67.98','Processing','bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'),
        ('#ORD-7288','Marco R.','$124.95','Cancelled','bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-300'),
        ('#ORD-7287','Aisha K.','$349.97','Delivered','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
    ]
    for oid, cust, total, status, scls in orders:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{oid}</td><td class="py-2.5 text-gray-600 dark:text-gray-400">{cust}</td><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{total}</td><td class="py-2.5"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{status}</span></td></tr>'
    h += '</tbody></table></div></div>'
    h += '</div>'

    h += page_foot()
    write_file('03-ecommerce-dashboard.html', h)

# ============================================================
# DASHBOARD 3: CRM
# ============================================================
def gen_crm_dashboard():
    h = page_head('CRM Dashboard \u2014 mtverse', 'Production-ready CRM Dashboard with leads, deals, pipeline, and customer analytics')
    h += breadcrumb('Dashboards', 'CRM')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">CRM Overview</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Pipeline, deals, and customer insights</p></div>'
    h += '<div class="flex gap-2"><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 inline-flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>Add Deal</button></div></div>'

    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Total Leads', '2,456', '15.3%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', '1800,1950,2100,2200,2300,2350,2400,2456')
    h += kpi_card('Deals Won', '384', '22.1%', 'up', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', '280,295,310,320,335,350,365,384')
    h += kpi_card('Pipeline Value', '$2.4M', '8.7%', 'up', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600', 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', '1.8,1.9,2.0,2.1,2.15,2.2,2.3,2.4')
    h += kpi_card('Avg Deal Size', '$6,240', '4.2%', 'up', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600', 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6', '5200,5400,5600,5800,5900,6000,6100,6240')
    h += '</div>'

    # Pipeline + Chart
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    # Pipeline stages
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Deal Pipeline</h2>'
    h += '<div class="space-y-3">'
    stages = [
        ('Qualification', 45, '$540K', 'bg-blue-500'),
        ('Proposal', 32, '$384K', 'bg-indigo-500'),
        ('Negotiation', 28, '$336K', 'bg-violet-500'),
        ('Closed Won', 18, '$216K', 'bg-emerald-500'),
        ('Closed Lost', 8, '$96K', 'bg-red-400'),
    ]
    total = sum(s[1] for s in stages)
    for name, count, value, color in stages:
        pct = int(count/total*100)
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{count} deals \u00b7 {value}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2"><div class="{color} h-2 rounded-full" style="width:{pct}%"></div></div></div>'
    h += '</div></div>'
    # Win rate chart
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Monthly Deal Closings</h2></div>'
    h += svg_bar_chart('28,35,42,38,45,52,48,55,62,58,65,72', '#8b5cf6', 180, '-crm')
    h += '</div></div>'

    # Recent deals + Top accounts
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Recent Deals</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View all</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Deal</th><th class="pb-2 text-left font-medium">Company</th><th class="pb-2 text-left font-medium">Value</th><th class="pb-2 text-left font-medium">Stage</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    deals = [
        ('Enterprise License','Acme Corp','$48,000','Negotiation','bg-violet-50 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300'),
        ('Platform Upgrade','TechStart Inc','$12,500','Proposal','bg-indigo-50 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300'),
        ('Annual Contract','GlobalNet','$96,000','Closed Won','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('Pilot Program','DataFlow','$8,400','Qualification','bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'),
        ('SMB Package','CloudBase','$3,600','Closed Lost','bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-300'),
    ]
    for deal, comp, val, stage, scls in deals:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{deal}</td><td class="py-2.5 text-gray-600 dark:text-gray-400">{comp}</td><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{val}</td><td class="py-2.5"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{stage}</span></td></tr>'
    h += '</tbody></table></div></div>'
    # Top accounts
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Top Accounts</h2>'
    h += '<div class="space-y-3">'
    accounts = [
        ('Acme Corp', '$156K', '12 deals', 'https://i.pravatar.cc/32?img=12'),
        ('TechStart Inc', '$89K', '8 deals', 'https://i.pravatar.cc/32?img=14'),
        ('GlobalNet', '$234K', '15 deals', 'https://i.pravatar.cc/32?img=16'),
        ('DataFlow', '$45K', '5 deals', 'https://i.pravatar.cc/32?img=18'),
        ('CloudBase', '$67K', '7 deals', 'https://i.pravatar.cc/32?img=20'),
    ]
    for name, revenue, deals, img in accounts:
        h += f'<div class="flex items-center gap-3"><img src="{img}" class="w-9 h-9 rounded-lg"><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white">{name}</p><p class="text-xs text-gray-500">{deals}</p></div><p class="text-sm font-semibold text-gray-900 dark:text-white">{revenue}</p></div>'
    h += '</div></div></div>'

    h += page_foot()
    write_file('05-prompt-cms-dashboard.html', h)

# ============================================================
# DASHBOARD 4: Finance
# ============================================================
def gen_finance_dashboard():
    h = page_head('Finance Dashboard \u2014 mtverse', 'Production-ready Finance Dashboard with P&L, cash flow, expenses, and financial analytics')
    h += breadcrumb('Dashboards', 'Finance')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">Finance Overview</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Revenue, expenses, and financial health</p></div>'
    h += '<div class="flex gap-2"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300"><option>FY 2026</option><option>FY 2025</option><option>FY 2024</option></select>'
    h += '<button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">Download Report</button></div></div>'

    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Gross Revenue', '$1.24M', '14.2%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', '850,920,980,1020,1050,1080,1120,1160,1200,1240')
    h += kpi_card('Net Profit', '$342K', '8.5%', 'up', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6', '220,240,260,280,290,300,310,320,330,342')
    h += kpi_card('Total Expenses', '$898K', '12.1%', 'down', 'bg-rose-50 dark:bg-rose-900/30', 'text-rose-600', 'M19 14l-7 7m0 0l-7-7m7 7V3', '630,680,720,750,780,800,820,840,860,898')
    h += kpi_card('Profit Margin', '27.6%', '1.2%', 'up', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600', 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z', '24,24.5,25,25.5,26,26.2,26.5,27,27.3,27.6')
    h += '</div>'

    # Revenue vs Expenses chart + Expense breakdown
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Revenue vs Expenses</h2></div>'
    h += svg_line_chart('85,92,98,105,112,108,116,120,125,130', '#3b82f6', 180, '-fin-rev')
    h += '</div>'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Expense Breakdown</h2>'
    h += '<div class="flex justify-center gap-4 mb-4">'
    h += svg_donut_chart(40, '#ef4444', 80, 'Salaries', '')
    h += svg_donut_chart(25, '#3b82f6', 80, 'Operations', '')
    h += svg_donut_chart(20, '#f59e0b', 80, 'Marketing', '')
    h += '</div>'
    h += '<div class="space-y-2">'
    for name, pct, color in [('Salaries & Benefits','40%','bg-red-500'),('Operations','25%','bg-blue-500'),('Marketing','20%','bg-amber-500'),('R&D','10%','bg-emerald-500'),('Other','5%','bg-gray-400')]:
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{pct}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"><div class="{color} h-1.5 rounded-full" style="width:{pct}"></div></div></div>'
    h += '</div></div></div>'

    # Cash flow + Recent invoices
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Monthly Cash Flow</h2>'
    h += svg_bar_chart('45,52,-12,38,65,-8,72,55,-15,82', '#10b981', 160, '-cashflow')
    h += '</div>'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Recent Invoices</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View all</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Invoice</th><th class="pb-2 text-left font-medium">Client</th><th class="pb-2 text-left font-medium">Amount</th><th class="pb-2 text-left font-medium">Status</th><th class="pb-2 text-left font-medium">Due</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    invoices = [
        ('INV-2024-001','Acme Corp','$48,000','Paid','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300','Jun 1'),
        ('INV-2024-002','TechStart','$12,500','Pending','bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300','Jun 15'),
        ('INV-2024-003','GlobalNet','$96,000','Overdue','bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-300','May 28'),
        ('INV-2024-004','DataFlow','$8,400','Paid','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300','Jun 5'),
        ('INV-2024-005','CloudBase','$3,600','Draft','bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300','Jun 20'),
    ]
    for inv, client, amt, status, scls, due in invoices:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{inv}</td><td class="py-2.5 text-gray-600 dark:text-gray-400">{client}</td><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{amt}</td><td class="py-2.5"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{status}</span></td><td class="py-2.5 text-gray-500 dark:text-gray-400">{due}</td></tr>'
    h += '</tbody></table></div></div></div>'

    h += page_foot()
    write_file('13-ai-usage-analytics.html', h)

# ============================================================
# DASHBOARD 5: AI Operations
# ============================================================
def gen_ai_dashboard():
    h = page_head('AI Operations Dashboard \u2014 mtverse', 'Production-ready AI Operations Dashboard with model metrics, usage, costs, and performance')
    h += breadcrumb('Dashboards', 'AI Operations')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">AI Operations</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Model performance, usage, and cost analytics</p></div>'
    h += '<div class="flex gap-2"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300"><option>All Models</option><option>GPT-4</option><option>Claude</option><option>Custom</option></select></div></div>'

    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Total Requests', '4.2M', '28.5%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M13 10V3L4 14h7v7l9-11h-7z', '2.8,3.0,3.2,3.4,3.5,3.6,3.8,4.0,4.1,4.2')
    h += kpi_card('Avg Latency', '142ms', '8.3%', 'down', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z', '180,175,168,162,155,150,148,145,143,142')
    h += kpi_card('Token Cost', '$12,480', '15.2%', 'up', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600', 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z', '8200,8800,9200,9600,10000,10500,11000,11500,12000,12480')
    h += kpi_card('Success Rate', '99.7%', '0.2%', 'up', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600', 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z', '99.1,99.2,99.3,99.4,99.5,99.5,99.6,99.6,99.7,99.7')
    h += '</div>'

    # Request volume + Model comparison
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Request Volume</h2>'
    h += '<div class="flex gap-1"><button class="px-2.5 py-1 text-xs bg-blue-600 text-white rounded-md">Daily</button><button class="px-2.5 py-1 text-xs text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md">Hourly</button></div></div>'
    h += svg_line_chart('320,380,350,420,480,450,520,580,550,620,680,720', '#8b5cf6', 180, '-ai-req')
    h += '</div>'
    # Model comparison donuts
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Model Usage</h2>'
    h += '<div class="flex justify-center gap-4 mb-4">'
    h += svg_donut_chart(45, '#3b82f6', 80, 'GPT-4', '')
    h += svg_donut_chart(30, '#10b981', 80, 'Claude', '')
    h += svg_donut_chart(25, '#f59e0b', 80, 'Custom', '')
    h += '</div>'
    h += '<div class="space-y-2">'
    for name, pct, color in [('GPT-4','45%','bg-blue-500'),('Claude 3','30%','bg-emerald-500'),('Custom Models','25%','bg-amber-500')]:
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{pct}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"><div class="{color} h-1.5 rounded-full" style="width:{pct}"></div></div></div>'
    h += '</div></div></div>'

    # Latency by model + Recent runs
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Latency Distribution</h2>'
    h += svg_bar_chart('85,120,95,180,142,110,75', '#10b981', 160, '-ai-lat')
    h += '</div>'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Recent Model Runs</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View logs</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Run ID</th><th class="pb-2 text-left font-medium">Model</th><th class="pb-2 text-left font-medium">Tokens</th><th class="pb-2 text-left font-medium">Status</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    runs = [
        ('run-a7f3','GPT-4','2,450','Completed','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('run-b8e2','Claude 3','1,820','Completed','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('run-c9d1','Custom-v2','3,100','Running','bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'),
        ('run-d4a5','GPT-4','980','Failed','bg-red-50 text-red-600 dark:bg-red-900/30 dark:text-red-300'),
        ('run-e6f7','Claude 3','2,200','Completed','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
    ]
    for rid, model, tokens, status, scls in runs:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-2.5 font-mono text-xs text-gray-800 dark:text-gray-200">{rid}</td><td class="py-2.5 text-gray-600 dark:text-gray-400">{model}</td><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{tokens}</td><td class="py-2.5"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{status}</span></td></tr>'
    h += '</tbody></table></div></div></div>'

    h += page_foot()
    write_file('04-ai-tools-dashboard.html', h)

# ============================================================
# DASHBOARD 6: Marketing Analytics
# ============================================================
def gen_marketing_dashboard():
    h = page_head('Marketing Analytics Dashboard \u2014 mtverse', 'Production-ready Marketing Analytics Dashboard with campaigns, channels, and engagement metrics')
    h += breadcrumb('Dashboards', 'Marketing')
    h += '<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">'
    h += '<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">Marketing Analytics</h1><p class="text-gray-500 dark:text-gray-400 mt-1">Campaign performance and audience insights</p></div>'
    h += '<div class="flex gap-2"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300"><option>Last 30 days</option><option>Last 7 days</option><option>This quarter</option></select></div></div>'

    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">'
    h += kpi_card('Website Visitors', '84.2K', '12.8%', 'up', 'bg-blue-50 dark:bg-blue-900/30', 'text-blue-600', 'M15 12a3 3 0 11-6 0 3 3 0 016 0z', '62,65,68,72,75,78,80,82,83,84')
    h += kpi_card('Email Open Rate', '34.2%', '2.1%', 'up', 'bg-emerald-50 dark:bg-emerald-900/30', 'text-emerald-600', 'M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z', '28,29,30,31,32,32,33,33,34,34')
    h += kpi_card('Social Engagement', '12.4K', '18.5%', 'up', 'bg-violet-50 dark:bg-violet-900/30', 'text-violet-600', 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z', '8.2,8.8,9.2,9.8,10.2,10.8,11.2,11.6,12.0,12.4')
    h += kpi_card('Cost per Lead', '$18.40', '5.2%', 'down', 'bg-amber-50 dark:bg-amber-900/30', 'text-amber-600', 'M13 17h8m0 0V9m0 8l-8-8-4 4-6-6', '22,21.5,21,20.5,20,19.5,19,18.8,18.6,18.4')
    h += '</div>'

    # Traffic chart + Channel breakdown
    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">'
    h += '<div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Website Traffic</h2></div>'
    h += svg_line_chart('42,48,52,58,55,62,68,72,78,82,85,92', '#3b82f6', 180, '-mkt-traffic')
    h += '</div>'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Channel Performance</h2>'
    h += '<div class="space-y-3">'
    channels = [
        ('Organic Search', '38%', '32.4K sessions', 'bg-blue-500'),
        ('Paid Search', '22%', '18.5K sessions', 'bg-emerald-500'),
        ('Social Media', '18%', '15.2K sessions', 'bg-violet-500'),
        ('Email', '14%', '11.8K sessions', 'bg-amber-500'),
        ('Direct', '8%', '6.7K sessions', 'bg-gray-400'),
    ]
    for name, pct, detail, color in channels:
        h += f'<div><div class="flex justify-between text-xs mb-1"><span class="text-gray-600 dark:text-gray-400">{name}</span><span class="font-medium text-gray-800 dark:text-gray-200">{pct}</span></div><div class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"><div class="{color} h-1.5 rounded-full" style="width:{pct}"></div></div><p class="text-[10px] text-gray-400 mt-0.5">{detail}</p></div>'
    h += '</div></div></div>'

    # Campaign performance + Top pages
    h += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">'
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<div class="flex items-center justify-between mb-4"><h2 class="text-sm font-semibold text-gray-800 dark:text-white">Active Campaigns</h2><a href="#" class="text-xs text-blue-600 hover:underline font-medium">View all</a></div>'
    h += '<div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="text-xs text-gray-400 uppercase border-b border-gray-100 dark:border-gray-700"><th class="pb-2 text-left font-medium">Campaign</th><th class="pb-2 text-left font-medium">Channel</th><th class="pb-2 text-left font-medium">Leads</th><th class="pb-2 text-left font-medium">ROI</th><th class="pb-2 text-left font-medium">Status</th></tr></thead><tbody class="divide-y divide-gray-50 dark:divide-gray-700">'
    campaigns = [
        ('Summer Sale 2026','Email','1,242','340%','Active','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('Product Launch','Paid','856','280%','Active','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('Brand Awareness','Social','2,100','180%','Paused','bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'),
        ('Retargeting Q2','Paid','432','420%','Active','bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-300'),
        ('Newsletter June','Email','678','260%','Ended','bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'),
    ]
    for name, ch, leads, roi, status, scls in campaigns:
        h += f'<tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50"><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{name}</td><td class="py-2.5 text-gray-600 dark:text-gray-400">{ch}</td><td class="py-2.5 font-medium text-gray-800 dark:text-gray-200">{leads}</td><td class="py-2.5 text-emerald-600 font-medium">{roi}</td><td class="py-2.5"><span class="px-2 py-0.5 rounded-full text-xs font-medium {scls}">{status}</span></td></tr>'
    h += '</tbody></table></div></div>'
    # Top pages
    h += '<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">'
    h += '<h2 class="text-sm font-semibold text-gray-800 dark:text-white mb-4">Top Landing Pages</h2>'
    h += '<div class="space-y-3">'
    pages = [
        ('/pricing', '12.4K views', '3.2% bounce', 'bg-blue-100 dark:bg-blue-900/30 text-blue-600'),
        ('/features', '8.7K views', '5.1% bounce', 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600'),
        ('/blog/ai-tools', '6.2K views', '2.8% bounce', 'bg-violet-100 dark:bg-violet-900/30 text-violet-600'),
        ('/demo', '4.8K views', '4.5% bounce', 'bg-amber-100 dark:bg-amber-900/30 text-amber-600'),
        ('/docs/api', '3.1K views', '1.2% bounce', 'bg-rose-100 dark:bg-rose-900/30 text-rose-600'),
    ]
    for path, views, bounce, icls in pages:
        h += f'<div class="flex items-center gap-3"><div class="w-8 h-8 rounded-lg {icls} flex items-center justify-center"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.582a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg></div><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white font-mono">{path}</p><p class="text-xs text-gray-500">{views}</p></div><p class="text-xs text-gray-400">{bounce}</p></div>'
    h += '</div></div></div>'

    h += page_foot()
    write_file('02-analytics-dashboard.html', h)

# ============================================================
# RUN ALL
# ============================================================
if __name__ == '__main__':
    print('Generating premium dashboard pages...')
    gen_saas_dashboard()
    gen_ecommerce_dashboard()
    gen_crm_dashboard()
    gen_finance_dashboard()
    gen_ai_dashboard()
    gen_marketing_dashboard()
    print('Done! All dashboard pages generated.')
