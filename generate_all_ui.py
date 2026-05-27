#!/usr/bin/env python3
"""Generate all remaining premium UI element showcase pages."""
import html as html_mod
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    """Escape for HTML attribute."""
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#039;')

def attr_esc(s):
    """Escape for putting inside a single-quoted HTML attribute."""
    return s.replace('&','&amp;').replace('"','&quot;').replace("'",'&#39;').replace('<','&lt;').replace('>','&gt;')

def page_head(title, extra_css=''):
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en" class="scroll-smooth">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{title} \u2014 UI Elements</title>\n'
        '<style>::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:3px}::-webkit-scrollbar-thumb:hover{background:#94a3b8}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}</style>\n'
        '<link rel="stylesheet" href="tailwind-production.css">\n'
        '<link rel="stylesheet" href="pro-styles.css">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">\n'
        '<style>\n'
        '.component-item{border:1px solid #e5e7eb;border-radius:.75rem;overflow:hidden;background:#fff;transition:box-shadow .2s,border-color .2s}.component-item:hover{box-shadow:0 4px 12px rgba(0,0,0,.08);border-color:#cbd5e1}\n'
        '.dark .component-item{border-color:#374151;background:#1f2937}.dark .component-item:hover{border-color:#4b5563;box-shadow:0 4px 12px rgba(0,0,0,.3)}\n'
        '.component-item-header{padding:1rem 1.25rem;border-bottom:1px solid #f3f4f6;display:flex;align-items:center;justify-content:space-between}.dark .component-item-header{border-color:#374151}\n'
        '.component-item-preview{padding:1.5rem;display:flex;flex-wrap:wrap;gap:.75rem;align-items:center;min-height:80px}\n'
        '.component-item-actions{padding:.75rem 1.25rem;border-top:1px solid #f3f4f6;display:flex;gap:.5rem}.dark .component-item-actions{border-color:#374151}\n'
        + extra_css + '\n'
        '</style>\n'
        '<script src="https://sites.super.myninja.ai/_assets/ninja-daytona-script.js"></script>\n'
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

def page_foot():
    return '''
</div>
</main>
</div>
</div>
<script src="common-loader.js"></script>
<script src="common-sidebar.js"></script>
<script src="common-header.js"></script>
<script src="app-shell.js"></script>
<script>
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('[data-counter]').forEach(function(el){var target=parseInt(el.dataset.counter);var duration=1200;var start=0;var startTime=null;function step(ts){if(!startTime)startTime=ts;var p=Math.min((ts-startTime)/duration,1);el.textContent=Math.floor(p*target);if(p<1)requestAnimationFrame(step);else el.textContent=target;}requestAnimationFrame(step);});});
</script>
</body>
</html>'''

def breadcrumb(parent, current):
    return f'''<nav class="text-sm text-gray-500 dark:text-gray-400 mb-2" aria-label="Breadcrumb"><ol class="flex items-center gap-1.5"><li><a href="01-main-dashboard.html" class="hover:text-blue-600">Home</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600">{parent}</li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600 font-medium text-gray-800 dark:text-gray-200">{current}</li></ol></nav>'''

def page_header(title, desc, count, cats):
    cats_str = f'{count} component variants across {cats} categories with live preview and source code'
    return f'''<div class="mb-6">
{breadcrumb('UI Elements', title)}
<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">{title}</h1><p class="text-gray-500 dark:text-gray-400 mt-1">{cats_str}</p></div>
<div class="flex gap-2"><div class="relative"><input type="text" id="componentSearch" placeholder="Search {title.lower()}&#8230;" class="pl-9 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-56" oninput="initComponentSearch(this.value)"><svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg></div></div>
</div>
</div>'''

def stat_card(label, value, sub, icon_bg, icon_color, icon_path):
    val_attr = f' data-counter="{value}"' if isinstance(value, int) else ''
    val_text = '0' if isinstance(value, int) else value
    return f'''<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">
<div class="flex items-center justify-between mb-3"><span class="text-sm font-medium text-gray-500 dark:text-gray-400">{label}</span><span class="w-8 h-8 rounded-lg {icon_bg} flex items-center justify-center"><svg class="w-4 h-4 {icon_color}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/></svg></span></div>
<p class="text-2xl font-bold text-gray-900 dark:text-white"{val_attr}>{val_text}</p><p class="text-xs text-green-600 font-medium mt-1">{sub}</p>
</div>'''

def stat_cards(cards):
    inner = ''.join(stat_card(*c) for c in cards)
    return f'<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">{inner}</div>'

def cat_btn(label, cat, active=False):
    cls = 'bg-blue-600 text-white shadow-sm' if active else 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'
    return f'<button class="px-3 py-1.5 text-sm font-medium rounded-lg {cls}" data-category="{cat}" onclick="initCategoryFilter(&#39;{cat}&#39;,this)">{label}</button>'

def category_filters(cats):
    btns = ''.join(cat_btn(label, cat, cat=='all') for label, cat in cats)
    return f'<div class="flex flex-wrap gap-2 mb-6" id="categoryFilter">{btns}</div>'

def component_item(name, desc, cat, badge_cls, preview_html, source_code=None):
    sid = name.lower().replace(' ', '-').replace('/', '-')
    src = attr_esc(source_code if source_code else preview_html)
    badge_label = cat.capitalize()
    return f'''<div class="component-item" data-category="{cat}" data-title="{name}">
<div class="component-item-header"><div><h3 class="font-semibold text-gray-900 dark:text-white">{name}</h3><p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{desc}</p></div><span class="text-[10px] font-medium px-2 py-0.5 rounded-full {badge_cls}">{badge_label}</span></div>
<div class="component-item-preview" data-source-id="{sid}" data-source-code='{src}'>{preview_html}</div>
<div class="component-item-actions"><button class="text-xs font-medium text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 flex items-center gap-1" onclick="openSourceViewer(this)"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>View Source</button><button class="text-xs font-medium text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 flex items-center gap-1" onclick="copySourceCode(this)"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>Copy</button></div>
</div>
'''

def wrap_page(filename, title, desc, count, num_cats, stats, cats, items, extra_css=''):
    p = page_head(title, extra_css)
    p += page_header(title, desc, count, num_cats)
    p += stat_cards(stats)
    p += category_filters(cats)
    p += '<div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="componentGrid">\n'
    for it in items:
        p += component_item(*it)
    p += '</div>\n'
    p += page_foot()
    with open(os.path.join(OUT, filename), 'w', encoding='utf-8') as f:
        f.write(p)
    sz = os.path.getsize(os.path.join(OUT, filename))
    print(f'  {filename}: {sz//1024}KB ({len(items)} items)')

# ============================================================
# PAGES
# ============================================================

def gen_avatars():
    items = []
    items.append(("Basic Avatars", "Initial-based avatars with color variants", "display", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">JD</div>'
        '<div class="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center text-white text-sm font-semibold">AB</div>'
        '<div class="w-10 h-10 rounded-full bg-violet-600 flex items-center justify-center text-white text-sm font-semibold">CK</div>'
        '<div class="w-10 h-10 rounded-full bg-amber-600 flex items-center justify-center text-white text-sm font-semibold">DM</div>'
        '<div class="w-10 h-10 rounded-full bg-rose-600 flex items-center justify-center text-white text-sm font-semibold">EF</div>'
        '<div class="w-10 h-10 rounded-full bg-cyan-600 flex items-center justify-center text-white text-sm font-semibold">GH</div>',
    ))
    items.append(("Avatar with Image", "Photo-based avatars with fallback", "display", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<img src="https://i.pravatar.cc/80?img=1" class="w-10 h-10 rounded-full object-cover" alt="User">'
        '<img src="https://i.pravatar.cc/80?img=2" class="w-10 h-10 rounded-full object-cover" alt="User">'
        '<img src="https://i.pravatar.cc/80?img=3" class="w-10 h-10 rounded-full object-cover" alt="User">'
        '<img src="https://i.pravatar.cc/80?img=5" class="w-10 h-10 rounded-full object-cover" alt="User">'
        '<div class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center"><svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>',
    ))
    items.append(("Avatar Status Indicator", "Online/offline/busy/dnd status dot", "state", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="relative"><div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">JD</div><span class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white dark:border-gray-900 rounded-full"></span></div>'
        '<div class="relative"><div class="w-10 h-10 rounded-full bg-emerald-600 flex items-center justify-center text-white text-sm font-semibold">AB</div><span class="absolute bottom-0 right-0 w-3 h-3 bg-gray-400 border-2 border-white dark:border-gray-900 rounded-full"></span></div>'
        '<div class="relative"><div class="w-10 h-10 rounded-full bg-violet-600 flex items-center justify-center text-white text-sm font-semibold">CK</div><span class="absolute bottom-0 right-0 w-3 h-3 bg-amber-500 border-2 border-white dark:border-gray-900 rounded-full"></span></div>'
        '<div class="relative"><div class="w-10 h-10 rounded-full bg-rose-600 flex items-center justify-center text-white text-sm font-semibold">DM</div><span class="absolute bottom-0 right-0 w-3 h-3 bg-red-600 border-2 border-white dark:border-gray-900 rounded-full"></span></div>',
    ))
    items.append(("Avatar Group Stack", "Overlapping avatar stacks with count", "display", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex -space-x-3">'
        '<img src="https://i.pravatar.cc/80?img=1" class="w-10 h-10 rounded-full border-2 border-white dark:border-gray-900 object-cover" alt="">'
        '<img src="https://i.pravatar.cc/80?img=2" class="w-10 h-10 rounded-full border-2 border-white dark:border-gray-900 object-cover" alt="">'
        '<img src="https://i.pravatar.cc/80?img=3" class="w-10 h-10 rounded-full border-2 border-white dark:border-gray-900 object-cover" alt="">'
        '<img src="https://i.pravatar.cc/80?img=5" class="w-10 h-10 rounded-full border-2 border-white dark:border-gray-900 object-cover" alt="">'
        '<div class="w-10 h-10 rounded-full border-2 border-white dark:border-gray-900 bg-gray-100 dark:bg-gray-700 flex items-center justify-center text-xs font-medium text-gray-600 dark:text-gray-300">+5</div>'
        '</div>',
    ))
    items.append(("Avatar with Ring", "Ring/border highlight variants", "state", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="ring-2 ring-blue-500 ring-offset-2 rounded-full"><div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">JD</div></div>'
        '<div class="ring-2 ring-emerald-500 ring-offset-2 rounded-full"><img src="https://i.pravatar.cc/80?img=2" class="w-10 h-10 rounded-full object-cover" alt=""></div>'
        '<div class="ring-2 ring-rose-500 ring-offset-2 rounded-full"><div class="w-10 h-10 rounded-full bg-rose-600 flex items-center justify-center text-white text-sm font-semibold">EF</div></div>',
    ))
    items.append(("Square Rounded Avatars", "Square vs rounded variants", "shape", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="w-10 h-10 rounded bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">JD</div>'
        '<div class="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center text-white text-sm font-semibold">AB</div>'
        '<div class="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center text-white text-sm font-semibold">CK</div>'
        '<div class="w-10 h-10 rounded-full bg-amber-600 flex items-center justify-center text-white text-sm font-semibold">DM</div>',
    ))
    items.append(("Avatar Sizes", "XS to XXL size variants", "size", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="flex items-end gap-3">'
        '<div class="text-center"><div class="w-6 h-6 rounded-full bg-blue-600 flex items-center justify-center text-white text-[8px] font-semibold">XS</div><p class="text-[9px] text-gray-400 mt-1">24px</p></div>'
        '<div class="text-center"><div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-[10px] font-semibold">SM</div><p class="text-[9px] text-gray-400 mt-1">32px</p></div>'
        '<div class="text-center"><div class="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-semibold">MD</div><p class="text-[9px] text-gray-400 mt-1">40px</p></div>'
        '<div class="text-center"><div class="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-semibold">LG</div><p class="text-[9px] text-gray-400 mt-1">48px</p></div>'
        '<div class="text-center"><div class="w-14 h-14 rounded-full bg-blue-600 flex items-center justify-center text-white text-base font-semibold">XL</div><p class="text-[9px] text-gray-400 mt-1">56px</p></div>'
        '<div class="text-center"><div class="w-16 h-16 rounded-full bg-blue-600 flex items-center justify-center text-white text-lg font-semibold">2X</div><p class="text-[9px] text-gray-400 mt-1">64px</p></div>'
        '</div>',
    ))
    items.append(("Avatar with Info", "Avatar paired with name and role", "data", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex items-center gap-3"><img src="https://i.pravatar.cc/80?img=1" class="w-10 h-10 rounded-full object-cover" alt=""><div><p class="text-sm font-medium text-gray-900 dark:text-white">Jane Cooper</p><p class="text-xs text-gray-500">Product Manager</p></div></div>'
        '<div class="flex items-center gap-3"><div class="w-10 h-10 rounded-full bg-violet-600 flex items-center justify-center text-white text-sm font-semibold">CK</div><div><p class="text-sm font-medium text-gray-900 dark:text-white">Cody King</p><p class="text-xs text-gray-500">Developer</p></div></div>'
        '<div class="flex items-center gap-3"><img src="https://i.pravatar.cc/80?img=5" class="w-10 h-10 rounded-full object-cover" alt=""><div><p class="text-sm font-medium text-gray-900 dark:text-white">Emily Chen</p><p class="text-xs text-gray-500">Designer</p></div></div>',
    ))
    wrap_page('123-ui-avatars.html', 'Avatars', 'Avatar components', 8, 5,
        [("Components",8,"5 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"),
         ("Sizes",6,"xs to 2xl","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"),
         ("States",4,"online/offline/busy/dnd","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Display","display"),("State","state"),("Size","size"),("Shape","shape"),("Data","data")],
        items)

def gen_badges():
    items = []
    items.append(("Status Badges", "Live status indicators", "state", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"><span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>Active</span>'
        '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300"><span class="w-1.5 h-1.5 rounded-full bg-gray-400"></span>Inactive</span>'
        '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300"><span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>Pending</span>'
        '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300"><span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>Failed</span>'
        '<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"><span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>In Progress</span>',
    ))
    items.append(("Dot Badges", "Small colored dot indicators", "indicator", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<span class="inline-flex items-center gap-1.5 text-sm text-gray-700 dark:text-gray-300"><span class="w-2 h-2 rounded-full bg-green-500"></span>Online</span>'
        '<span class="inline-flex items-center gap-1.5 text-sm text-gray-700 dark:text-gray-300"><span class="w-2 h-2 rounded-full bg-red-500"></span>Offline</span>'
        '<span class="inline-flex items-center gap-1.5 text-sm text-gray-700 dark:text-gray-300"><span class="w-2 h-2 rounded-full bg-amber-500"></span>Away</span>'
        '<span class="inline-flex items-center gap-1.5 text-sm text-gray-700 dark:text-gray-300"><span class="w-2 h-2 rounded-full bg-blue-500"></span>Busy</span>',
    ))
    items.append(("Count Badges", "Numeric count indicators", "data", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-red-500 text-white text-[10px] font-bold">3</span>'
        '<span class="inline-flex items-center justify-center w-5 h-5 rounded-full bg-blue-500 text-white text-[10px] font-bold">12</span>'
        '<span class="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded-full bg-red-500 text-white text-[10px] font-bold">99+</span>'
        '<span class="relative inline-flex"><span class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg></span><span class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-red-500 text-white text-[8px] font-bold flex items-center justify-center">5</span></span>',
    ))
    items.append(("Solid Badges", "Filled background badges", "style", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-blue-600 text-white">New</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-green-600 text-white">Verified</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-red-600 text-white">Urgent</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-amber-500 text-white">Warning</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-purple-600 text-white">Premium</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium bg-gray-600 text-white">Draft</span>',
    ))
    items.append(("Outlined Badges", "Border-only badge styles", "style", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium border border-blue-600 text-blue-600 dark:border-blue-400 dark:text-blue-400">Info</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium border border-green-600 text-green-600 dark:border-green-400 dark:text-green-400">Success</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium border border-red-600 text-red-600 dark:border-red-400 dark:text-red-400">Error</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium border border-amber-600 text-amber-600 dark:border-amber-400 dark:text-amber-400">Warning</span>'
        '<span class="px-2.5 py-0.5 rounded text-xs font-medium border border-purple-600 text-purple-600 dark:border-purple-400 dark:text-purple-400">Pro</span>',
    ))
    items.append(("Tag Label Badges", "Removable tag/label badges", "interactive", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">React <button class="ml-0.5 hover:text-blue-900"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></span>'
        '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">Production <button class="ml-0.5 hover:text-green-900"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></span>'
        '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">Design <button class="ml-0.5 hover:text-violet-900"><svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></span>',
    ))
    items.append(("Pill vs Rounded", "Shape comparison variants", "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<span class="px-3 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">Pill Badge</span>'
        '<span class="px-3 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">Rounded Badge</span>'
        '<span class="px-3 py-0.5 rounded-l-full text-xs font-medium bg-blue-600 text-white">Left Pill</span>'
        '<span class="px-3 py-0.5 rounded-r-full text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300 border border-l-0 border-blue-200 dark:border-blue-800">Right Pill</span>',
    ))
    items.append(("Size Variants", "XS through XL badge sizes", "size", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<span class="px-1.5 py-0.5 rounded text-[10px] font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">XS Badge</span>'
        '<span class="px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">SM Badge</span>'
        '<span class="px-2.5 py-1 rounded text-sm font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">MD Badge</span>'
        '<span class="px-3 py-1.5 rounded text-base font-medium bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">LG Badge</span>',
    ))
    wrap_page('124-ui-badge.html', 'Badges', 'Badge components', 8, 5,
        [("Variants",8,"5 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"),
         ("Colors",10,"semantic palette","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Interactive",3,"removable tags","bg-violet-50 dark:violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("State","state"),("Indicator","indicator"),("Data","data"),("Style","style"),("Size","size"),("Interactive","interactive")],
        items)

def gen_breadcrumbs():
    items = []
    items.append(("Basic Breadcrumb", "Standard chevron-separated breadcrumb", "navigation", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<nav class="text-sm"><ol class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400"><li><a href="#" class="hover:text-blue-600">Home</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600">Products</li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600 font-medium text-gray-800 dark:text-gray-200">Details</li></ol></nav>',
    ))
    items.append(("Chevron Breadcrumb", "Chevron icon separator style", "navigation", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<nav class="text-sm"><ol class="flex items-center gap-1 text-gray-500 dark:text-gray-400"><li><a href="#" class="hover:text-blue-600">Home</a></li><li><svg class="w-4 h-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></li><li><a href="#" class="hover:text-blue-600">Settings</a></li><li><svg class="w-4 h-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></li><li class="font-medium text-gray-800 dark:text-gray-200">Profile</li></ol></nav>',
    ))
    items.append(("Breadcrumb with Icons", "Breadcrumb with icon elements", "navigation", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<nav class="text-sm"><ol class="flex items-center gap-1.5 text-gray-500 dark:text-gray-400"><li><a href="#" class="inline-flex items-center gap-1 hover:text-blue-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>Home</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600"><a href="#" class="inline-flex items-center gap-1 hover:text-blue-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>Projects</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600 font-medium text-gray-800 dark:text-gray-200">Design System</li></ol></nav>',
    ))
    items.append(("Pill Breadcrumb", "Pill-shaped breadcrumb segments", "style", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<nav class="text-sm"><ol class="flex items-center gap-1"><li><a href="#" class="px-3 py-1 rounded-l-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700">Home</a></li><li><a href="#" class="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700">Products</a></li><li><span class="px-3 py-1 rounded-r-full bg-blue-600 text-white font-medium">Details</span></li></ol></nav>',
    ))
    items.append(("Dark Background Breadcrumb", "Breadcrumb on dark surface", "style", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="bg-gray-900 rounded-lg p-4"><nav class="text-sm"><ol class="flex items-center gap-1.5 text-gray-400"><li><a href="#" class="hover:text-white transition-colors">Home</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-600">Dashboard</a></li><li class="before:content-[&#39;/&#39;] before:mx-1.5 before:text-gray-600 font-medium text-white">Analytics</li></ol></nav></div>',
    ))
    wrap_page('125-ui-breadcrumb.html', 'Breadcrumbs', 'Breadcrumb components', 5, 2,
        [("Variants",5,"2 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M9 5l7 7-7 7"),
         ("Responsive","100%","Mobile ready","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Navigation","navigation"),("Style","style")],
        items)

def gen_notifications():
    items = []
    items.append(("Info Alert", "Informational alert variant", "info", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="w-full max-w-lg border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"><div class="flex gap-3"><svg class="w-5 h-5 text-blue-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg><div><h4 class="text-sm font-medium text-blue-800 dark:text-blue-300">Information</h4><p class="text-sm text-blue-700 dark:text-blue-400 mt-1">Your account settings have been updated successfully.</p></div></div></div>',
    ))
    items.append(("Success Alert", "Positive confirmation alert", "success", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="w-full max-w-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 rounded-lg p-4"><div class="flex gap-3"><svg class="w-5 h-5 text-green-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg><div><h4 class="text-sm font-medium text-green-800 dark:text-green-300">Success</h4><p class="text-sm text-green-700 dark:text-green-400 mt-1">Your payment has been processed and your order is confirmed.</p></div></div></div>',
    ))
    items.append(("Warning Alert", "Caution/warning alert variant", "warning", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="w-full max-w-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4"><div class="flex gap-3"><svg class="w-5 h-5 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg><div><h4 class="text-sm font-medium text-amber-800 dark:text-amber-300">Warning</h4><p class="text-sm text-amber-700 dark:text-amber-400 mt-1">Your storage is at 90% capacity. Consider upgrading your plan.</p></div></div></div>',
    ))
    items.append(("Error Alert", "Critical error alert variant", "error", "bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300",
        '<div class="w-full max-w-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 rounded-lg p-4"><div class="flex gap-3"><svg class="w-5 h-5 text-red-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg><div><h4 class="text-sm font-medium text-red-800 dark:text-red-300">Error</h4><p class="text-sm text-red-700 dark:text-red-400 mt-1">Failed to save changes. Please check your connection and try again.</p></div></div></div>',
    ))
    items.append(("Dismissible Alert", "Alert with close button", "interactive", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="w-full max-w-lg border border-blue-200 dark:border-blue-800 bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4" id="dismiss-alert-demo"><div class="flex gap-3 items-start"><svg class="w-5 h-5 text-blue-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg><div class="flex-1"><h4 class="text-sm font-medium text-blue-800 dark:text-blue-300">Heads up!</h4><p class="text-sm text-blue-700 dark:text-blue-400 mt-1">A new version is available. Refresh to update.</p></div><button onclick="this.closest(&#39;[id^=dismiss]&#39;).style.display=&#39;none&#39;" class="text-blue-600 hover:text-blue-800 dark:hover:text-blue-200"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div></div>',
    ))
    items.append(("Toast Notifications", "Stacked toast messages", "toast", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex flex-col gap-3 max-w-sm">'
        '<div class="flex items-center gap-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3 shadow-sm"><div class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center"><svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></div><div class="flex-1"><p class="text-sm font-medium text-gray-900 dark:text-white">Saved successfully</p><p class="text-xs text-gray-500">2 seconds ago</p></div><button class="text-gray-400 hover:text-gray-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>'
        '<div class="flex items-center gap-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3 shadow-sm"><div class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center"><svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></div><div class="flex-1"><p class="text-sm font-medium text-gray-900 dark:text-white">Upload failed</p><p class="text-xs text-gray-500">5 seconds ago</p></div><button class="text-gray-400 hover:text-gray-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>'
        '<div class="flex items-center gap-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3 shadow-sm"><div class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></div><div class="flex-1"><p class="text-sm font-medium text-gray-900 dark:text-white">New update available</p><p class="text-xs text-gray-500">1 minute ago</p></div><button class="text-gray-400 hover:text-gray-600"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>'
        '</div>',
    ))
    items.append(("Alert with Action", "Alert containing action buttons", "interactive", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="w-full max-w-lg border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 rounded-lg p-4"><div class="flex gap-3"><svg class="w-5 h-5 text-amber-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg><div class="flex-1"><h4 class="text-sm font-medium text-amber-800 dark:text-amber-300">Storage Almost Full</h4><p class="text-sm text-amber-700 dark:text-amber-400 mt-1">You have used 90% of your storage. Upgrade to Pro for unlimited storage.</p><div class="flex gap-2 mt-3"><button class="px-3 py-1.5 text-xs font-medium bg-amber-600 text-white rounded-md hover:bg-amber-700">Upgrade Now</button><button class="px-3 py-1.5 text-xs font-medium border border-amber-300 dark:border-amber-700 text-amber-700 dark:text-amber-300 rounded-md hover:bg-amber-100 dark:hover:bg-amber-900/30">Dismiss</button></div></div></div></div>',
    ))
    wrap_page('134-ui-notifications.html', 'Notifications', 'Notification components', 7, 5,
        [("Variants",7,"5 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"),
         ("Types",4,"info/success/warning/error","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Interactive",2,"dismissible + action","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Info","info"),("Success","success"),("Warning","warning"),("Error","error"),("Interactive","interactive"),("Toast","toast")],
        items)

def gen_tooltips():
    items = []
    items.append(("Top Tooltip", "Tooltip appearing above element", "position", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-6">'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 rounded-md">Hover me</button><div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Tooltip on top</div></div>'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md">Info</button><div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Click for details</div></div>'
        '</div>',
    ))
    items.append(("Bottom Tooltip", "Tooltip appearing below element", "position", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="flex gap-6 pt-8">'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 rounded-md">Hover me</button><div class="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Tooltip on bottom</div></div>'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-emerald-600 text-white rounded-md">Save</button><div class="absolute top-full left-1/2 -translate-x-1/2 mt-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Save changes (Ctrl+S)</div></div>'
        '</div>',
    ))
    items.append(("Left Right Tooltips", "Side-positioned tooltips", "position", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="flex gap-12 justify-center">'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 rounded-md">Left</button><div class="absolute right-full top-1/2 -translate-y-1/2 mr-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Left tooltip</div></div>'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 rounded-md">Right</button><div class="absolute left-full top-1/2 -translate-y-1/2 ml-2 px-2 py-1 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Right tooltip</div></div>'
        '</div>',
    ))
    items.append(("Light Tooltip", "Light/white background tooltip", "style", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex gap-6">'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-800 rounded-md">Light tip</button><div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 text-xs bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded shadow-lg border border-gray-100 dark:border-gray-700 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap">Light tooltip</div></div>'
        '</div>',
    ))
    items.append(("Multi-line Tooltip", "Tooltip with longer content", "data", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-6">'
        '<div class="relative group"><button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md">Details</button><div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 text-xs bg-gray-900 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none max-w-[200px] text-center leading-relaxed">This is a multi-line tooltip with more detailed information about the element.</div></div>'
        '</div>',
    ))
    wrap_page('141-ui-tooltips.html', 'Tooltips', 'Tooltip components', 5, 2,
        [("Variants",5,"2 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Positions",4,"top/bottom/left/right","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4")],
        [("All","all"),("Position","position"),("Style","style"),("Data","data")],
        items)

def gen_spinners():
    items = []
    items.append(("Border Spinner", "Classic CSS border spinner", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-6 items-center">'
        '<div class="w-6 h-6 border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>'
        '<div class="w-10 h-10 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>'
        '<div class="w-12 h-12 border-4 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>'
        '</div>',
    ))
    items.append(("SVG Circle Spinner", "SVG-based animated spinner", "basic", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="flex gap-6 items-center">'
        '<svg class="w-6 h-6 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>'
        '<svg class="w-8 h-8 animate-spin text-emerald-600" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>'
        '<svg class="w-10 h-10 animate-spin text-violet-600" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>'
        '</div>',
    ))
    items.append(("Dots Spinner", "Animated bouncing dots", "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="flex gap-6 items-center">'
        '<div class="flex gap-1"><div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay:0ms"></div><div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay:150ms"></div><div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay:300ms"></div></div>'
        '<div class="flex gap-1.5"><div class="w-2.5 h-2.5 bg-emerald-600 rounded-full animate-bounce" style="animation-delay:0ms"></div><div class="w-2.5 h-2.5 bg-emerald-600 rounded-full animate-bounce" style="animation-delay:150ms"></div><div class="w-2.5 h-2.5 bg-emerald-600 rounded-full animate-bounce" style="animation-delay:300ms"></div></div>'
        '</div>',
    ))
    items.append(("Pulse Spinner", "Pulsing circle indicator", "style", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex gap-6 items-center">'
        '<div class="w-4 h-4 bg-blue-600 rounded-full animate-pulse"></div>'
        '<div class="w-6 h-6 bg-emerald-600 rounded-full animate-pulse"></div>'
        '<div class="w-8 h-8 bg-violet-600 rounded-full animate-pulse"></div>'
        '</div>',
    ))
    items.append(("Color Variants", "Spinner in multiple semantic colors", "style", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-5 items-center flex-wrap">'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-blue-600 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-green-600 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-red-600 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-amber-500 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-purple-600 rounded-full animate-spin"></div>'
        '<div class="w-8 h-8 border-[3px] border-gray-200 border-t-cyan-600 rounded-full animate-spin"></div>'
        '</div>',
    ))
    items.append(("Loading with Text", "Spinner paired with message", "data", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="flex flex-col gap-4">'
        '<div class="flex items-center gap-3"><div class="w-5 h-5 border-2 border-gray-200 border-t-blue-600 rounded-full animate-spin"></div><span class="text-sm text-gray-600 dark:text-gray-400">Loading data&#8230;</span></div>'
        '<div class="flex items-center gap-3"><svg class="w-5 h-5 animate-spin text-blue-600" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg><span class="text-sm text-gray-600 dark:text-gray-400">Saving changes&#8230;</span></div>'
        '</div>',
    ))
    items.append(("Full Page Loader", "Centered full-page overlay", "overlay", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="w-full h-40 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center"><div class="text-center"><svg class="w-10 h-10 animate-spin text-blue-600 mx-auto mb-3" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg><p class="text-sm font-medium text-gray-600 dark:text-gray-400">Loading application&#8230;</p><p class="text-xs text-gray-400 dark:text-gray-500 mt-1">This will not take long</p></div></div>',
    ))
    wrap_page('139-ui-spinners.html', 'Spinners', 'Spinner components', 7, 4,
        [("Variants",7,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"),
         ("Colors",6,"semantic palette","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Animated","7","CSS animations","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Style","style"),("Data","data"),("Overlay","overlay")],
        items)

def gen_pagination():
    items = []
    items.append(("Basic Pagination", "Standard page navigation", "navigation", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<nav class="flex items-center gap-1"><button class="px-3 py-1.5 text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">Prev</button><button class="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md">1</button><button class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">2</button><button class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">3</button><span class="px-2 text-gray-400">&#8230;</span><button class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">12</button><button class="px-3 py-1.5 text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">Next</button></nav>',
    ))
    items.append(("Icon Pagination", "Arrow icon navigation", "navigation", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<nav class="flex items-center gap-1"><button class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button><button class="w-8 h-8 flex items-center justify-center text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">1</button><button class="w-8 h-8 flex items-center justify-center text-sm bg-blue-600 text-white rounded-md">2</button><button class="w-8 h-8 flex items-center justify-center text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">3</button><button class="w-8 h-8 flex items-center justify-center text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md">4</button><button class="p-1.5 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button></nav>',
    ))
    items.append(("Compact Pagination", "Minimal page indicator", "compact", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="flex items-center gap-3"><button class="p-1 text-gray-400 hover:text-gray-600"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button><span class="text-sm text-gray-600 dark:text-gray-400">Page <strong class="text-gray-900 dark:text-white">3</strong> of <strong class="text-gray-900 dark:text-white">12</strong></span><button class="p-1 text-gray-400 hover:text-gray-600"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button></div>',
    ))
    items.append(("Table Pagination", "Pagination with page size selector", "data", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="flex items-center justify-between"><p class="text-sm text-gray-500 dark:text-gray-400">Showing <span class="font-medium text-gray-700 dark:text-gray-300">1</span> to <span class="font-medium text-gray-700 dark:text-gray-300">10</span> of <span class="font-medium text-gray-700 dark:text-gray-300">96</span> results</p><div class="flex items-center gap-3"><select class="text-sm border border-gray-200 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800 px-2 py-1"><option>10</option><option>25</option><option>50</option></select><nav class="flex items-center gap-1"><button class="px-2.5 py-1 text-sm text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">Prev</button><button class="px-2.5 py-1 text-sm bg-blue-600 text-white rounded">1</button><button class="px-2.5 py-1 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">2</button><button class="px-2.5 py-1 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">3</button><button class="px-2.5 py-1 text-sm text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded">Next</button></nav></div></div>',
    ))
    items.append(("Load More Button", "Progressive loading pattern", "interactive", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="text-center"><button class="px-6 py-2.5 text-sm font-medium text-blue-600 border border-blue-600 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors">Load More</button><p class="text-xs text-gray-400 mt-2">Showing 20 of 156 items</p></div>',
    ))
    wrap_page('135-ui-pagination.html', 'Pagination', 'Pagination components', 5, 3,
        [("Variants",5,"3 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"),
         ("Patterns",3,"standard/compact/table","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.582a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Navigation","navigation"),("Compact","compact"),("Data","data"),("Interactive","interactive")],
        items)

def gen_button_groups():
    items = []
    items.append(("Basic Button Group", "Connected horizontal button set", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">'
        '<button class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700">Left</button>'
        '<button class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700">Center</button>'
        '<button class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700">Right</button>'
        '</div>',
    ))
    items.append(("Primary Button Group", "Filled/active button group", "action", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="inline-flex rounded-lg overflow-hidden">'
        '<button class="px-4 py-2 text-sm text-white bg-blue-600 hover:bg-blue-700 border-r border-blue-700">Day</button>'
        '<button class="px-4 py-2 text-sm text-blue-600 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/40 border-r border-blue-200 dark:border-blue-800">Week</button>'
        '<button class="px-4 py-2 text-sm text-blue-600 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-900/40">Month</button>'
        '</div>',
    ))
    items.append(("Icon Button Group", "Icon-only connected buttons", "icon", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">'
        '<button class="p-2 text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700" aria-label="Bold"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M6 4h8a4 4 0 014 4 4 4 0 01-4 4H6z"/></svg></button>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700" aria-label="Italic"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M10 4h4m-2 0v16m0 0h-2m4 0h-2"/></svg></button>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700" aria-label="Underline"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M7 4v7a5 5 0 0010 0V4m-2 0v7a3 3 0 01-6 0V4M4 18h16"/></svg></button>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700" aria-label="Strikethrough"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5c2.76 0 5 1.12 5 2.5S14.76 10 12 10s-5-1.12-5-2.5S9.24 5 12 5zm0 14c-2.76 0-5-1.12-5-2.5h0c0-1.38 2.24-2.5 5-2.5s5 1.12 5 2.5h0c0 1.38-2.24 2.5-5 2.5z"/></svg></button>'
        '</div>',
    ))
    items.append(("Vertical Button Group", "Stacked vertical buttons", "layout", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="inline-flex flex-col rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden w-40">'
        '<button class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-b border-gray-200 dark:border-gray-700 text-left">Option 1</button>'
        '<button class="px-4 py-2 text-sm text-white bg-blue-600 text-left">Option 2</button>'
        '<button class="px-4 py-2 text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 border-t border-gray-200 dark:border-gray-700 text-left">Option 3</button>'
        '</div>',
    ))
    items.append(("Toolbar Button Group", "App toolbar action strip", "action", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex items-center gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">'
        '<button class="p-2 text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 rounded-md" aria-label="Undo"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a5 5 0 015 5v2M3 10l4-4m-4 4l4 4"/></svg></button>'
        '<button class="p-2 text-gray-400 dark:text-gray-600 cursor-not-allowed rounded-md" aria-label="Redo" disabled><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10H11a5 5 0 00-5 5v2m15-7l-4-4m4 4l-4 4"/></svg></button>'
        '<div class="w-px h-6 bg-gray-300 dark:bg-gray-600 mx-1"></div>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 rounded-md" aria-label="Copy"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg></button>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 rounded-md" aria-label="Paste"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg></button>'
        '<div class="w-px h-6 bg-gray-300 dark:bg-gray-600 mx-1"></div>'
        '<button class="p-2 text-gray-600 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700 rounded-md" aria-label="Delete"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg></button>'
        '</div>',
    ))
    items.append(("Segmented Control", "iOS-style segmented picker", "selection", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="inline-flex p-0.5 bg-gray-100 dark:bg-gray-800 rounded-lg">'
        '<button class="px-4 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md shadow-sm">All</button>'
        '<button class="px-4 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white rounded-md">Active</button>'
        '<button class="px-4 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white rounded-md">Archived</button>'
        '</div>',
    ))
    items.append(("Size Toggle Group", "XS/S/M/L/XL size selector", "selection", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="inline-flex rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">'
        '<button class="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700">XS</button>'
        '<button class="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700">S</button>'
        '<button class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 border-r border-blue-700">M</button>'
        '<button class="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700 border-r border-gray-200 dark:border-gray-700">L</button>'
        '<button class="px-3 py-1.5 text-xs text-gray-500 dark:text-gray-500 hover:bg-gray-50 dark:hover:bg-gray-700">XL</button>'
        '</div>',
    ))
    wrap_page('127-ui-button-groups.html', 'Button Groups', 'Button group components', 7, 4,
        [("Variants",7,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M4 6h16M4 12h16M4 18h7"),
         ("Layouts",2,"horizontal/vertical","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z"),
         ("Interactive","100%","clickable items","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Action","action"),("Icon","icon"),("Layout","layout"),("Selection","selection")],
        items)

def gen_carousel():
    items = []
    items.append(("Basic Carousel", "Image carousel with nav arrows", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative w-full max-w-md overflow-hidden rounded-lg bg-gray-200 dark:bg-gray-700" style="height:200px" id="carousel-basic">'
        '<div class="flex transition-transform duration-300" id="carousel-basic-track">'
        '<div class="w-full shrink-0 h-[200px] bg-blue-500 flex items-center justify-center text-white text-xl font-bold">Slide 1</div>'
        '<div class="w-full shrink-0 h-[200px] bg-emerald-500 flex items-center justify-center text-white text-xl font-bold">Slide 2</div>'
        '<div class="w-full shrink-0 h-[200px] bg-violet-500 flex items-center justify-center text-white text-xl font-bold">Slide 3</div>'
        '</div>'
        '<button onclick="var t=document.getElementById(&#39;carousel-basic-track&#39;);var c=parseInt(t.dataset.c||0);c=c>0?c-1:2;t.dataset.c=c;t.style.transform=&#39;translateX(-&#39;+c*100+&#39;%)&#39;" class="absolute left-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-white/80 dark:bg-gray-800/80 rounded-full flex items-center justify-center shadow"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button>'
        '<button onclick="var t=document.getElementById(&#39;carousel-basic-track&#39;);var c=parseInt(t.dataset.c||0);c=c<2?c+1:0;t.dataset.c=c;t.style.transform=&#39;translateX(-&#39;+c*100+&#39;%)&#39;" class="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 bg-white/80 dark:bg-gray-800/80 rounded-full flex items-center justify-center shadow"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button>'
        '</div>',
    ))
    items.append(("Dot Indicator Carousel", "Carousel with dot indicators", "navigation", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative w-full max-w-md overflow-hidden rounded-lg bg-gray-200 dark:bg-gray-700" style="height:200px" id="carousel-dots">'
        '<div class="flex transition-transform duration-300" id="carousel-dots-track">'
        '<div class="w-full shrink-0 h-[200px] bg-amber-500 flex items-center justify-center text-white text-xl font-bold">Photo 1</div>'
        '<div class="w-full shrink-0 h-[200px] bg-rose-500 flex items-center justify-center text-white text-xl font-bold">Photo 2</div>'
        '<div class="w-full shrink-0 h-[200px] bg-cyan-500 flex items-center justify-center text-white text-xl font-bold">Photo 3</div>'
        '</div>'
        '<div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2"><button class="w-2.5 h-2.5 rounded-full bg-white" onclick="document.getElementById(&#39;carousel-dots-track&#39;).style.transform=&#39;translateX(0)&#39;"></button><button class="w-2.5 h-2.5 rounded-full bg-white/50" onclick="document.getElementById(&#39;carousel-dots-track&#39;).style.transform=&#39;translateX(-100%)&#39;"></button><button class="w-2.5 h-2.5 rounded-full bg-white/50" onclick="document.getElementById(&#39;carousel-dots-track&#39;).style.transform=&#39;translateX(-200%)&#39;"></button></div>'
        '</div>',
    ))
    items.append(("Card Carousel", "Content card slider", "content", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="flex gap-4 overflow-x-auto pb-2 snap-x snap-mandatory" style="scrollbar-width:none">'
        '<div class="min-w-[260px] snap-start bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"><div class="w-full h-32 bg-blue-100 dark:bg-blue-900/30 rounded mb-3 flex items-center justify-center text-blue-600 text-sm">Image</div><h4 class="font-medium text-gray-900 dark:text-white text-sm">Card Title 1</h4><p class="text-xs text-gray-500 mt-1">Description for card content</p></div>'
        '<div class="min-w-[260px] snap-start bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"><div class="w-full h-32 bg-emerald-100 dark:bg-emerald-900/30 rounded mb-3 flex items-center justify-center text-emerald-600 text-sm">Image</div><h4 class="font-medium text-gray-900 dark:text-white text-sm">Card Title 2</h4><p class="text-xs text-gray-500 mt-1">Description for card content</p></div>'
        '<div class="min-w-[260px] snap-start bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4"><div class="w-full h-32 bg-violet-100 dark:bg-violet-900/30 rounded mb-3 flex items-center justify-center text-violet-600 text-sm">Image</div><h4 class="font-medium text-gray-900 dark:text-white text-sm">Card Title 3</h4><p class="text-xs text-gray-500 mt-1">Description for card content</p></div>'
        '</div>',
    ))
    items.append(("Testimonial Carousel", "Customer testimonial slider", "content", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="w-full max-w-md bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">'
        '<svg class="w-8 h-8 text-gray-300 dark:text-gray-600 mb-3" fill="currentColor" viewBox="0 0 24 24"><path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/></svg>'
        '<p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed mb-4">This product has completely transformed our workflow. The team productivity increased by 40% in the first month.</p>'
        '<div class="flex items-center gap-3"><img src="https://i.pravatar.cc/48?img=11" class="w-10 h-10 rounded-full" alt=""><div><p class="text-sm font-medium text-gray-900 dark:text-white">Sarah Johnson</p><p class="text-xs text-gray-500">CEO at TechCorp</p></div></div>'
        '</div>',
    ))
    items.append(("Thumbnail Carousel", "Main image with thumbnail strip", "navigation", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="w-full max-w-md">'
        '<div class="w-full h-48 bg-gray-200 dark:bg-gray-700 rounded-lg mb-2 flex items-center justify-center text-gray-400 text-sm">Main Preview</div>'
        '<div class="flex gap-2">'
        '<button class="w-16 h-12 bg-blue-200 dark:bg-blue-900/30 rounded border-2 border-blue-600"></button>'
        '<button class="w-16 h-12 bg-gray-200 dark:bg-gray-700 rounded border-2 border-transparent hover:border-gray-400"></button>'
        '<button class="w-16 h-12 bg-gray-200 dark:bg-gray-700 rounded border-2 border-transparent hover:border-gray-400"></button>'
        '<button class="w-16 h-12 bg-gray-200 dark:bg-gray-700 rounded border-2 border-transparent hover:border-gray-400"></button>'
        '</div></div>',
    ))
    wrap_page('128-ui-carousel.html', 'Carousel', 'Carousel components', 5, 3,
        [("Variants",5,"3 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"),
         ("Interactive",5,"swipe/click navigable","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Navigation","navigation"),("Content","content")],
        items)

def gen_dropdowns():
    items = []
    items.append(("Basic Dropdown", "Click-triggered dropdown menu", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 inline-flex items-center gap-2">Options <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute left-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 py-1">'
        '<a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Edit</a>'
        '<a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Duplicate</a>'
        '<a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Archive</a>'
        '<div class="border-t border-gray-100 dark:border-gray-700 my-1"></div>'
        '<a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">Delete</a>'
        '</div></div>',
    ))
    items.append(("Dropdown with Icons", "Menu items with leading icons", "icon", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 inline-flex items-center gap-2">Actions <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute right-0 mt-2 w-52 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 py-1">'
        '<a href="#" class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>Edit</a>'
        '<a href="#" class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>Copy</a>'
        '<a href="#" class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>Share</a>'
        '</div></div>',
    ))
    items.append(("Dropdown with Checkbox", "Multi-select dropdown items", "selection", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">Filter Columns <svg class="w-4 h-4 ml-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute left-0 mt-2 w-48 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 py-1">'
        '<label class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"><input type="checkbox" checked class="rounded border-gray-300 text-blue-600">Name</label>'
        '<label class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"><input type="checkbox" checked class="rounded border-gray-300 text-blue-600">Email</label>'
        '<label class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"><input type="checkbox" class="rounded border-gray-300 text-blue-600">Role</label>'
        '<label class="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer"><input type="checkbox" class="rounded border-gray-300 text-blue-600">Status</label>'
        '</div></div>',
    ))
    items.append(("User Profile Dropdown", "Profile/account menu dropdown", "profile", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="flex items-center gap-2"><img src="https://i.pravatar.cc/32?img=1" class="w-8 h-8 rounded-full"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10">'
        '<div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700"><p class="text-sm font-medium text-gray-900 dark:text-white">Jane Cooper</p><p class="text-xs text-gray-500">jane@company.com</p></div>'
        '<div class="py-1"><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Your Profile</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Settings</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Billing</a></div>'
        '<div class="border-t border-gray-100 dark:border-gray-700 py-1"><a href="#" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">Sign out</a></div>'
        '</div></div>',
    ))
    items.append(("Dropdown with Search", "Searchable dropdown with filter", "search", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">Select Country <svg class="w-4 h-4 ml-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute left-0 mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10">'
        '<div class="p-2 border-b border-gray-100 dark:border-gray-700"><input type="text" placeholder="Search..." class="w-full px-3 py-1.5 text-sm border border-gray-200 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800"></div>'
        '<div class="max-h-40 overflow-y-auto py-1"><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">United States</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">United Kingdom</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Canada</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Australia</a><a href="#" class="block px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Germany</a></div>'
        '</div></div>',
    ))
    items.append(("Dropdown with Shortcut", "Items with keyboard shortcuts", "data", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative inline-block">'
        '<button onclick="var m=this.nextElementSibling;m.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">File <svg class="w-4 h-4 ml-1 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg></button>'
        '<div class="hidden absolute left-0 mt-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 py-1">'
        '<a href="#" class="flex items-center justify-between px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">New <kbd class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded">Ctrl+N</kbd></a>'
        '<a href="#" class="flex items-center justify-between px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Open <kbd class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded">Ctrl+O</kbd></a>'
        '<a href="#" class="flex items-center justify-between px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Save <kbd class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded">Ctrl+S</kbd></a>'
        '<div class="border-t border-gray-100 dark:border-gray-700 my-1"></div>'
        '<a href="#" class="flex items-center justify-between px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">Print <kbd class="text-[10px] px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-500 rounded">Ctrl+P</kbd></a>'
        '</div></div>',
    ))
    wrap_page('129-ui-dropdowns.html', 'Dropdowns', 'Dropdown components', 6, 5,
        [("Variants",6,"5 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"),
         ("Interactive",6,"click-triggered","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Keyboard",4,"shortcut support","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M12 19l9 2-9-18-9 18 9-2zm0 0v7"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Icon","icon"),("Selection","selection"),("Profile","profile"),("Search","search"),("Data","data")],
        items)

def gen_images():
    items = []
    items.append(("Basic Image", "Responsive image with aspect ratio", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<img src="https://images.unsplash.com/photo-1506905925345-21bbac3d2b3e?w=400&h=250&fit=crop" class="w-full max-w-sm rounded-lg object-cover" alt="Landscape" style="height:200px">',
    ))
    items.append(("Rounded Image", "Image with rounded corners", "shape", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<img src="https://images.unsplash.com/photo-1519125323398-675c0e7b1903?w=200&h=200&fit=crop" class="w-32 h-32 rounded-2xl object-cover" alt="">'
        '<img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop" class="w-32 h-32 rounded-full object-cover" alt="">',
    ))
    items.append(("Image with Overlay", "Image with text overlay", "overlay", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="relative w-full max-w-sm rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1493246507139-91e8fad9971e?w=400&h=250&fit=crop" class="w-full object-cover" style="height:200px" alt=""><div class="absolute inset-0 bg-black/40 flex items-end p-4"><p class="text-white text-sm font-medium">Mountain Sunset</p></div></div>',
    ))
    items.append(("Image Grid", "Multi-image gallery grid", "layout", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="grid grid-cols-3 gap-2 w-full max-w-sm">'
        '<img src="https://images.unsplash.com/photo-1506905925345-21bbac3d2b3e?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt="">'
        '<img src="https://images.unsplash.com/photo-1519125323398-675c0e7b1903?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt="">'
        '<img src="https://images.unsplash.com/photo-1493246507139-91e8fad9971e?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt="">'
        '<img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt="">'
        '<img src="https://images.unsplash.com/photo-1504198453319-5ce911b9de45?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt="">'
        '<div class="relative"><img src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=200&h=200&fit=crop" class="w-full aspect-square object-cover rounded-lg" alt=""><div class="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center"><span class="text-white text-sm font-semibold">+12</span></div></div>'
        '</div>',
    ))
    items.append(("Avatar Image", "Circular avatar images", "avatar", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-4 items-center">'
        '<img src="https://i.pravatar.cc/64?img=1" class="w-16 h-16 rounded-full object-cover ring-2 ring-white dark:ring-gray-800 shadow" alt="">'
        '<img src="https://i.pravatar.cc/64?img=5" class="w-16 h-16 rounded-full object-cover ring-2 ring-white dark:ring-gray-800 shadow" alt="">'
        '<img src="https://i.pravatar.cc/64?img=8" class="w-16 h-16 rounded-full object-cover ring-2 ring-white dark:ring-gray-800 shadow" alt="">'
        '</div>',
    ))
    items.append(("Image Placeholder", "SVG/placeholder when no image", "state", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="w-full max-w-sm h-48 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center"><svg class="w-12 h-12 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg></div>',
    ))
    wrap_page('130-ui-images.html', 'Images', 'Image components', 6, 5,
        [("Variants",6,"5 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"),
         ("Responsive","100%","Mobile ready","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"),
         ("Overlay",1,"text overlay","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M15 12a3 3 0 11-6 0 3 3 0 016 0z"),
         ("Grid",1,"gallery layout","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5z")],
        [("All","all"),("Basic","basic"),("Shape","shape"),("Overlay","overlay"),("Layout","layout"),("Avatar","avatar"),("State","state")],
        items)

def gen_links():
    items = []
    items.append(("Basic Links", "Standard text links", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<a href="#" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 hover:underline">Default Link</a>'
        '<a href="#" class="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline">Underlined Link</a>'
        '<a href="#" class="text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400">Muted Link</a>',
    ))
    items.append(("Icon Links", "Links with icon elements", "icon", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<a href="#" class="inline-flex items-center gap-1.5 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>External Link</a>'
        '<a href="#" class="inline-flex items-center gap-1.5 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300">Learn More <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></a>',
    ))
    items.append(("Breadcrumb Links", "Navigation breadcrumb links", "navigation", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<nav class="flex items-center gap-1.5 text-sm"><a href="#" class="text-blue-600 hover:text-blue-800 dark:text-blue-400">Home</a><span class="text-gray-300 dark:text-gray-600">/</span><a href="#" class="text-blue-600 hover:text-blue-800 dark:text-blue-400">Products</a><span class="text-gray-300 dark:text-gray-600">/</span><span class="text-gray-800 dark:text-gray-200 font-medium">Details</span></nav>',
    ))
    items.append(("Footer Links", "Multi-column footer link groups", "layout", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="grid grid-cols-3 gap-6 text-sm">'
        '<div><h5 class="font-medium text-gray-900 dark:text-white mb-2">Product</h5><div class="flex flex-col gap-1.5"><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Features</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Pricing</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Integrations</a></div></div>'
        '<div><h5 class="font-medium text-gray-900 dark:text-white mb-2">Company</h5><div class="flex flex-col gap-1.5"><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">About</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Blog</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Careers</a></div></div>'
        '<div><h5 class="font-medium text-gray-900 dark:text-white mb-2">Support</h5><div class="flex flex-col gap-1.5"><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Help Center</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Contact</a><a href="#" class="text-gray-500 dark:text-gray-400 hover:text-blue-600">Status</a></div></div>'
        '</div>',
    ))
    items.append(("Social Links", "Social media icon links", "social", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-3">'
        '<a href="#" class="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-500 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/></svg></a>'
        '<a href="#" class="w-9 h-9 rounded-lg bg-gray-100 dark:bg-gray-800 flex items-center justify-center text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg></a>'
        '</div>',
    ))
    wrap_page('131-ui-links.html', 'Links', 'Link components', 5, 4,
        [("Variants",5,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"),
         ("Styles",3,"underline/muted/icon","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Icon","icon"),("Navigation","navigation"),("Layout","layout"),("Social","social")],
        items)

def gen_lists():
    items = []
    items.append(("Basic List", "Unordered and ordered lists", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="flex gap-8">'
        '<ul class="list-disc list-inside space-y-2 text-sm text-gray-700 dark:text-gray-300"><li>First item</li><li>Second item</li><li>Third item</li><li>Fourth item</li></ul>'
        '<ol class="list-decimal list-inside space-y-2 text-sm text-gray-700 dark:text-gray-300"><li>Step one</li><li>Step two</li><li>Step three</li></ol>'
        '</div>',
    ))
    items.append(("Icon List", "List items with custom icons", "icon", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<ul class="space-y-3">'
        '<li class="flex items-center gap-3"><svg class="w-5 h-5 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">Free shipping on orders over $50</span></li>'
        '<li class="flex items-center gap-3"><svg class="w-5 h-5 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">24/7 customer support</span></li>'
        '<li class="flex items-center gap-3"><svg class="w-5 h-5 text-green-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">30-day money-back guarantee</span></li>'
        '<li class="flex items-center gap-3"><svg class="w-5 h-5 text-gray-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg><span class="text-sm text-gray-400 line-through">Priority access (Pro only)</span></li>'
        '</ul>',
    ))
    items.append(("Description List", "Key-value pair listing", "data", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<dl class="divide-y divide-gray-200 dark:divide-gray-700">'
        '<div class="py-2 flex justify-between"><dt class="text-sm text-gray-500 dark:text-gray-400">Full Name</dt><dd class="text-sm font-medium text-gray-900 dark:text-white">Jane Cooper</dd></div>'
        '<div class="py-2 flex justify-between"><dt class="text-sm text-gray-500 dark:text-gray-400">Email</dt><dd class="text-sm font-medium text-gray-900 dark:text-white">jane@company.com</dd></div>'
        '<div class="py-2 flex justify-between"><dt class="text-sm text-gray-500 dark:text-gray-400">Role</dt><dd class="text-sm font-medium text-gray-900 dark:text-white">Product Manager</dd></div>'
        '<div class="py-2 flex justify-between"><dt class="text-sm text-gray-500 dark:text-gray-400">Status</dt><dd><span class="px-2 py-0.5 text-xs rounded-full bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">Active</span></dd></div>'
        '</dl>',
    ))
    items.append(("Navigation List", "Clickable list items for navigation", "navigation", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="w-full max-w-xs border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">'
        '<a href="#" class="flex items-center gap-3 px-4 py-3 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 border-b border-gray-100 dark:border-gray-700"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>Dashboard</a>'
        '<a href="#" class="flex items-center gap-3 px-4 py-3 text-sm bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-b border-gray-100 dark:border-gray-700"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>Profile</a>'
        '<a href="#" class="flex items-center gap-3 px-4 py-3 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"><svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>Settings</a>'
        '</div>',
    ))
    items.append(("Feature List", "Plan comparison feature list", "data", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="space-y-2">'
        '<div class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">Unlimited projects</span></div>'
        '<div class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">Advanced analytics</span></div>'
        '<div class="flex items-center gap-2"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg><span class="text-sm text-gray-700 dark:text-gray-300">Priority support</span></div>'
        '<div class="flex items-center gap-2"><svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/></svg><span class="text-sm text-gray-400">Custom domain</span></div>'
        '<div class="flex items-center gap-2"><svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/></svg><span class="text-sm text-gray-400">SSO integration</span></div>'
        '</div>',
    ))
    wrap_page('132-ui-list.html', 'Lists', 'List components', 5, 4,
        [("Variants",5,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M4 6h16M4 10h16M4 14h16M4 18h16"),
         ("Styles",3,"disc/decimal/icon","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"),
         ("Interactive","2","clickable items","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Icon","icon"),("Data","data"),("Navigation","navigation")],
        items)

def gen_popovers():
    items = []
    items.append(("Basic Popover", "Click-triggered popover card", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative inline-block">'
        '<button onclick="var p=this.nextElementSibling;p.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm bg-gray-100 dark:bg-gray-800 rounded-lg">Click for Popover</button>'
        '<div class="hidden absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 p-4">'
        '<h4 class="text-sm font-medium text-gray-900 dark:text-white mb-1">Popover Title</h4>'
        '<p class="text-xs text-gray-500 dark:text-gray-400">This is a popover with richer content than a tooltip.</p>'
        '</div></div>',
    ))
    items.append(("Popover with Actions", "Interactive popover with buttons", "action", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative inline-block">'
        '<button onclick="var p=this.nextElementSibling;p.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg">Delete Item</button>'
        '<div class="hidden absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 p-4">'
        '<h4 class="text-sm font-medium text-gray-900 dark:text-white mb-1">Confirm Delete</h4>'
        '<p class="text-xs text-gray-500 dark:text-gray-400 mb-3">Are you sure you want to delete this item? This action cannot be undone.</p>'
        '<div class="flex gap-2"><button class="px-3 py-1 text-xs bg-red-600 text-white rounded-md hover:bg-red-700">Delete</button><button class="px-3 py-1 text-xs border border-gray-200 dark:border-gray-700 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700">Cancel</button></div>'
        '</div></div>',
    ))
    items.append(("Profile Popover", "User profile info popover", "profile", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="relative inline-block">'
        '<button onclick="var p=this.nextElementSibling;p.classList.toggle(&#39;hidden&#39;)" class="flex items-center gap-2"><img src="https://i.pravatar.cc/32?img=3" class="w-8 h-8 rounded-full">John</button>'
        '<div class="hidden absolute bottom-full left-0 mb-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 p-4">'
        '<div class="flex items-center gap-3 mb-3"><img src="https://i.pravatar.cc/48?img=3" class="w-10 h-10 rounded-full"><div><p class="text-sm font-medium text-gray-900 dark:text-white">John Doe</p><p class="text-xs text-gray-500">john@company.com</p></div></div>'
        '<p class="text-xs text-gray-500 dark:text-gray-400">Product Designer at TechCorp. San Francisco, CA.</p>'
        '</div></div>',
    ))
    items.append(("Notification Popover", "Notification list popover", "data", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="relative inline-block">'
        '<button onclick="var p=this.nextElementSibling;p.classList.toggle(&#39;hidden&#39;)" class="relative p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg><span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span></button>'
        '<div class="hidden absolute right-0 mt-2 w-72 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10">'
        '<div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700"><h4 class="text-sm font-medium text-gray-900 dark:text-white">Notifications</h4></div>'
        '<div class="max-h-48 overflow-y-auto"><div class="px-4 py-3 border-b border-gray-50 dark:border-gray-700"><p class="text-sm text-gray-700 dark:text-gray-300">New comment on your post</p><p class="text-xs text-gray-400 mt-0.5">2 min ago</p></div><div class="px-4 py-3"><p class="text-sm text-gray-700 dark:text-gray-300">Project deployment successful</p><p class="text-xs text-gray-400 mt-0.5">1 hour ago</p></div></div>'
        '<div class="px-4 py-2 border-t border-gray-100 dark:border-gray-700"><a href="#" class="text-xs text-blue-600 hover:text-blue-800">View all notifications</a></div>'
        '</div></div>',
    ))
    items.append(("Form Popover", "Popover with form inputs", "action", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative inline-block">'
        '<button onclick="var p=this.nextElementSibling;p.classList.toggle(&#39;hidden&#39;)" class="px-4 py-2 text-sm bg-gray-100 dark:bg-gray-800 rounded-lg">Add Label</button>'
        '<div class="hidden absolute bottom-full left-0 mb-2 w-56 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg z-10 p-4">'
        '<h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">New Label</h4>'
        '<input type="text" placeholder="Label name" class="w-full px-3 py-1.5 text-sm border border-gray-200 dark:border-gray-700 rounded-md bg-white dark:bg-gray-800 mb-2">'
        '<div class="flex gap-1.5 mb-3"><span class="w-5 h-5 rounded-full bg-blue-500 cursor-pointer ring-2 ring-blue-200"></span><span class="w-5 h-5 rounded-full bg-green-500 cursor-pointer"></span><span class="w-5 h-5 rounded-full bg-amber-500 cursor-pointer"></span><span class="w-5 h-5 rounded-full bg-red-500 cursor-pointer"></span><span class="w-5 h-5 rounded-full bg-purple-500 cursor-pointer"></span></div>'
        '<button class="w-full px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700">Add Label</button>'
        '</div></div>',
    ))
    wrap_page('136-ui-popovers.html', 'Popovers', 'Popover components', 5, 4,
        [("Variants",5,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"),
         ("Interactive",5,"click-triggered","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Content",3,"text/form/actions","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.582a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Action","action"),("Profile","profile"),("Data","data")],
        items)

def gen_ribbons():
    items = []
    items.append(("Corner Ribbon", "Top-right corner ribbon badge", "corner", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative w-full max-w-xs h-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="absolute top-3 -right-6 bg-blue-600 text-white text-[10px] font-semibold px-8 py-1 rotate-45 shadow-sm">NEW</div><div class="p-4"><p class="text-sm font-medium text-gray-900 dark:text-white">Card Title</p><p class="text-xs text-gray-500 mt-1">With corner ribbon</p></div></div>',
    ))
    items.append(("Sale Ribbon", "Discount/sale ribbon badge", "sale", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative w-full max-w-xs h-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="absolute top-0 -right-0 bg-red-500 text-white text-[10px] font-bold px-3 py-1 rounded-bl-lg">-30%</div><div class="p-4"><p class="text-sm font-medium text-gray-900 dark:text-white">Premium Plan</p><p class="text-xs text-gray-500 mt-1">With sale ribbon</p></div></div>',
    ))
    items.append(("Featured Ribbon", "Featured/popular ribbon", "featured", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="relative w-full max-w-xs h-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="absolute top-3 -left-6 bg-amber-500 text-white text-[10px] font-semibold px-8 py-1 -rotate-45 shadow-sm">POPULAR</div><div class="p-4 ml-4"><p class="text-sm font-medium text-gray-900 dark:text-white">Standard Plan</p><p class="text-xs text-gray-500 mt-1">With featured ribbon</p></div></div>',
    ))
    items.append(("Status Ribbon", "Status indicator ribbon", "status", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="relative w-full max-w-xs h-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="absolute top-0 left-0 bg-green-500 text-white text-[10px] font-bold px-3 py-1 rounded-br-lg">VERIFIED</div><div class="p-4 mt-2"><p class="text-sm font-medium text-gray-900 dark:text-white">Verified Account</p><p class="text-xs text-gray-500 mt-1">With status ribbon</p></div></div>',
    ))
    items.append(("Banner Ribbon", "Full-width banner ribbon", "banner", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative w-full max-w-xs bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="bg-blue-600 text-white text-xs font-semibold px-4 py-1.5 text-center">Limited Time Offer</div><div class="p-4"><p class="text-sm font-medium text-gray-900 dark:text-white">Special Product</p><p class="text-xs text-gray-500 mt-1">With banner ribbon</p></div></div>',
    ))
    wrap_page('138-ui-ribbons.html', 'Ribbons', 'Ribbon components', 5, 4,
        [("Variants",5,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A2 2 0 013 12V7a4 4 0 014-4z"),
         ("Positions",3,"corner/top/bottom","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z"),
         ("Interactive","5","clickable items","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M13 10V3L4 14h7v7l9-11h-7z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Corner","corner"),("Sale","sale"),("Featured","featured"),("Status","status"),("Banner","banner")],
        items)

def gen_videos():
    items = []
    items.append(("Embedded Video Player", "Standard video embed with controls", "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="w-full max-w-md bg-gray-900 rounded-lg overflow-hidden"><div class="relative aspect-video flex items-center justify-center"><svg class="w-16 h-16 text-white/80" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg><div class="absolute bottom-0 left-0 right-0 bg-black/50 p-3"><div class="flex items-center gap-3"><button class="text-white"><svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button><div class="flex-1 h-1 bg-white/30 rounded-full"><div class="w-1/3 h-full bg-blue-500 rounded-full"></div></div><span class="text-xs text-white/80">3:24 / 10:15</span><button class="text-white"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg></button></div></div></div></div>',
    ))
    items.append(("Video Thumbnail", "Thumbnail with play overlay", "thumbnail", "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300",
        '<div class="relative w-full max-w-sm rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1493246507139-91e8fad9971e?w=400&h=225&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute inset-0 bg-black/30 flex items-center justify-center"><div class="w-14 h-14 bg-white/90 rounded-full flex items-center justify-center shadow-lg"><svg class="w-6 h-6 text-blue-600 ml-1" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div></div><div class="absolute bottom-2 right-2 px-1.5 py-0.5 bg-black/80 text-white text-xs rounded">10:15</div></div>',
    ))
    items.append(("Video Card", "Video info card with thumbnail", "layout", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '<div class="w-full max-w-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"><div class="relative"><img src="https://images.unsplash.com/photo-1506905925345-21bbac3d2b3e?w=400&h=225&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute bottom-2 right-2 px-1.5 py-0.5 bg-black/80 text-white text-xs rounded">8:42</div></div><div class="p-4"><h4 class="text-sm font-medium text-gray-900 dark:text-white">Getting Started with Design Systems</h4><p class="text-xs text-gray-500 mt-1">1.2K views &#183; 3 days ago</p></div></div>',
    ))
    items.append(("Video Grid", "Multi-video gallery layout", "layout", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '<div class="grid grid-cols-2 gap-3 w-full max-w-lg">'
        '<div class="relative rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1506905925345-21bbac3d2b3e?w=200&h=112&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute bottom-1 right-1 px-1 py-0.5 bg-black/80 text-white text-[9px] rounded">5:30</div></div>'
        '<div class="relative rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1493246507139-91e8fad9971e?w=200&h=112&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute bottom-1 right-1 px-1 py-0.5 bg-black/80 text-white text-[9px] rounded">12:45</div></div>'
        '<div class="relative rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1519125323398-675c0e7b1903?w=200&h=112&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute bottom-1 right-1 px-1 py-0.5 bg-black/80 text-white text-[9px] rounded">7:18</div></div>'
        '<div class="relative rounded-lg overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center aspect-video"><div class="text-center"><svg class="w-6 h-6 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg><p class="text-[9px] text-gray-400 mt-1">More</p></div></div>'
        '</div>',
    ))
    items.append(("Live Stream Badge", "Live/broadcast indicator overlay", "state", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '<div class="relative w-full max-w-sm rounded-lg overflow-hidden"><img src="https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400&h=225&fit=crop" class="w-full aspect-video object-cover" alt=""><div class="absolute top-2 left-2 flex items-center gap-1.5 px-2 py-1 bg-red-600 rounded text-white text-[10px] font-bold"><span class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></span>LIVE</div><div class="absolute bottom-2 left-2 flex items-center gap-1.5 px-2 py-1 bg-black/60 rounded text-white text-xs"><svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>2.4K watching</div></div>',
    ))
    wrap_page('142-ui-videos.html', 'Videos', 'Video components', 5, 4,
        [("Variants",5,"4 categories","bg-blue-50 dark:bg-blue-900/30","text-blue-600","M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"),
         ("Layouts",2,"card/grid","bg-emerald-50 dark:bg-emerald-900/30","text-emerald-600","M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6z"),
         ("Overlay",2,"play/live indicators","bg-violet-50 dark:bg-violet-900/30","text-violet-600","M15 12a3 3 0 11-6 0 3 3 0 016 0z"),
         ("Responsive","100%","Mobile ready","bg-amber-50 dark:bg-amber-900/30","text-amber-600","M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z")],
        [("All","all"),("Basic","basic"),("Thumbnail","thumbnail"),("Layout","layout"),("State","state")],
        items)

# ============================================================
# RUN ALL GENERATORS
# ============================================================
if __name__ == '__main__':
    print('Generating premium UI element pages...')
    gen_avatars()
    gen_badges()
    gen_breadcrumbs()
    gen_notifications()
    gen_tooltips()
    gen_spinners()
    gen_pagination()
    gen_button_groups()
    gen_carousel()
    gen_dropdowns()
    gen_images()
    gen_links()
    gen_lists()
    gen_popovers()
    gen_ribbons()
    gen_videos()
    print('Done! All UI element pages generated.')
