#!/usr/bin/env python3
"""Generate premium UI element showcase pages."""
import os

BASE_DIR = "/workspace/html-clone/templates/html"

def page_head(title, extra_css=""):
    return f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — UI Elements</title>
<style>::-webkit-scrollbar{{width:6px;height:6px}}::-webkit-scrollbar-track{{background:transparent}}::-webkit-scrollbar-thumb{{background:#cbd5e1;border-radius:3px}}::-webkit-scrollbar-thumb:hover{{background:#94a3b8}}@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important}}}}</style>
<link rel="stylesheet" href="tailwind-production.css">
<link rel="stylesheet" href="pro-styles.css">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
.component-item{{border:1px solid #e5e7eb;border-radius:.75rem;overflow:hidden;background:#fff;transition:box-shadow .2s,border-color .2s}}.component-item:hover{{box-shadow:0 4px 12px rgba(0,0,0,.08);border-color:#cbd5e1}}
.dark .component-item{{border-color:#374151;background:#1f2937}}.dark .component-item:hover{{border-color:#4b5563;box-shadow:0 4px 12px rgba(0,0,0,.3)}}
.component-item-header{{padding:1rem 1.25rem;border-bottom:1px solid #f3f4f6;display:flex;align-items:center;justify-content:space-between}}.dark .component-item-header{{border-color:#374151}}
.component-item-preview{{padding:1.5rem;display:flex;flex-wrap:wrap;gap:.75rem;align-items:flex-start;min-height:80px}}
.component-item-actions{{padding:.75rem 1.25rem;border-top:1px solid #f3f4f6;display:flex;gap:.5rem}}.dark .component-item-actions{{border-color:#374151}}
.modal-backdrop-demo{{position:relative;background:#f9fafb;border-radius:.5rem;padding:2rem;display:flex;align-items:center;justify-content:center;min-height:220px;overflow:hidden}}.dark .modal-backdrop-demo{{background:#111827}}
.modal-demo{{background:#fff;border-radius:.75rem;box-shadow:0 20px 60px rgba(0,0,0,.15);max-width:420px;width:100%;overflow:hidden}}.dark .modal-demo{{background:#1f2937;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
.tab-demo{{border-bottom:2px solid #e5e7eb;display:flex;gap:0}}.tab-demo button{{padding:.625rem 1.25rem;font-size:.875rem;font-weight:500;color:#6b7280;border-bottom:2px solid transparent;margin-bottom:-2px;transition:color .2s,border-color .2s;cursor:pointer;background:none}}.tab-demo button:hover{{color:#374151}}.tab-demo button.active{{color:#2563eb;border-bottom-color:#2563eb}}.dark .tab-demo{{border-color:#374151}}.dark .tab-demo button{{color:#9ca3af}}.dark .tab-demo button:hover{{color:#d1d5db}}.dark .tab-demo button.active{{color:#60a5fa;border-bottom-color:#60a5fa}}
.progress-bar-demo{{height:8px;background:#e5e7eb;border-radius:9999px;overflow:hidden}}.progress-bar-demo .fill{{height:100%;border-radius:9999px;transition:width .6s ease}}.dark .progress-bar-demo{{background:#374151}}
.avatar-ring{{box-shadow:0 0 0 3px #fff,0 0 0 5px #3b82f6}}.dark .avatar-ring{{box-shadow:0 0 0 3px #1f2937,0 0 0 5px #3b82f6}}
.badge-dot{{position:relative}}.badge-dot::after{{content:'';position:absolute;top:-2px;right:-2px;width:8px;height:8px;background:#ef4444;border:2px solid #fff;border-radius:50%}}.dark .badge-dot::after{{border-color:#1f2937}}
{extra_css}
</style>
</head>
<body class="bg-gray-50 text-gray-800 font-sans dark:bg-gray-900 dark:text-gray-100">
<div id="sidebar-overlay" class="fixed inset-0 bg-black/40 z-40 hidden lg:hidden" onclick="window.toggleSidebar&&toggleSidebar()"></div>
<div class="flex h-screen overflow-hidden">
<div id="sidebar-container"></div>
<div class="flex-1 flex flex-col overflow-hidden">
<div id="header-container"></div>
<main class="flex-1 overflow-y-auto overflow-x-hidden px-4 md:px-6 2xl:px-10 py-6" tabindex="-1">
<div class="mx-auto w-full max-w-screen-2xl">'''

def page_foot(extra_js=""):
    return f'''</div>
</main>
</div>
</div>
<script src="common-loader.js"></script>
<script src="common-sidebar.js"></script>
<script src="common-header.js"></script>
<script src="app-shell.js"></script>
<script>
document.addEventListener('DOMContentLoaded',function(){{document.querySelectorAll('[data-counter]').forEach(function(el){{var target=parseInt(el.dataset.counter);var duration=1200;var start=0;var startTime=null;function step(ts){{if(!startTime)startTime=ts;var p=Math.min((ts-startTime)/duration,1);el.textContent=Math.floor(p*target);if(p<1)requestAnimationFrame(step);else el.textContent=target;}}requestAnimationFrame(step);}});}});
{extra_js}
</script>
</body>
</html>'''

def breadcrumb(page_name):
    return f'''<nav class="text-sm text-gray-500 dark:text-gray-400 mb-2" aria-label="Breadcrumb"><ol class="flex items-center gap-1.5"><li><a href="01-main-dashboard.html" class="hover:text-blue-600">Home</a></li><li class="before:content-['/'] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600">UI Elements</li><li class="before:content-['/'] before:mx-1.5 before:text-gray-300 dark:before:text-gray-600 font-medium text-gray-800 dark:text-gray-200">{page_name}</li></ol></nav>'''

def page_header(title, desc, stats, search_placeholder="Search…"):
    stat_cards = ""
    for s in stats:
        stat_cards += f'''<div class="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5">
<div class="flex items-center justify-between mb-3"><span class="text-sm font-medium text-gray-500 dark:text-gray-400">{s['label']}</span><span class="w-8 h-8 rounded-lg {s['icon_bg']} flex items-center justify-center"><svg class="w-4 h-4 {s['icon_color']}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{s['icon_path']}"/></svg></span></div>
<p class="text-2xl font-bold text-gray-900 dark:text-white" {'data-counter="'+str(s['value'])+'"' if isinstance(s['value'],int) else ''}>{s['value'] if not isinstance(s['value'],int) else '0'}</p><p class="text-xs text-green-600 font-medium mt-1">{s['sub']}</p>
</div>'''
    return f'''<div class="mb-6">
{breadcrumb(title)}
<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
<div><h1 class="text-2xl font-bold text-gray-900 dark:text-white">{title}</h1><p class="text-gray-500 dark:text-gray-400 mt-1">{desc}</p></div>
<div class="flex gap-2"><div class="relative"><input type="text" id="componentSearch" placeholder="{search_placeholder}" class="pl-9 pr-4 py-2 text-sm border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 w-56" oninput="initComponentSearch(this.value)"><svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg></div></div>
</div>
</div>
<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">{stat_cards}</div>'''

def category_filter(categories):
    btns = ""
    for i, (cat, label) in enumerate(categories):
        if i == 0:
            btns += f'<button class="px-3 py-1.5 text-sm font-medium rounded-lg bg-blue-600 text-white shadow-sm" data-category="{cat}" onclick="initCategoryFilter(\'{cat}\',this)">{label}</button>'
        else:
            btns += f'<button class="px-3 py-1.5 text-sm font-medium rounded-lg bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700" data-category="{cat}" onclick="initCategoryFilter(\'{cat}\',this)">{label}</button>'
    return f'<div class="flex flex-wrap gap-2 mb-6" id="categoryFilter">{btns}</div>'

def component_item(title, desc, category, category_color, preview_html, source_code):
    src_escaped = source_code.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    return f'''<div class="component-item" data-category="{category}" data-title="{title}">
<div class="component-item-header"><div><h3 class="font-semibold text-gray-900 dark:text-white">{title}</h3><p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{desc}</p></div><span class="text-[10px] font-medium px-2 py-0.5 rounded-full {category_color}">{category.title()}</span></div>
<div class="component-item-preview" data-source-id="{title.lower().replace(' ','-').replace('/','')}" data-source-code="{src_escaped}">{preview_html}</div>
<div class="component-item-actions"><button class="text-xs font-medium text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 flex items-center gap-1" onclick="openSourceViewer(this)"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>View Source</button><button class="text-xs font-medium text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 flex items-center gap-1" onclick="copySourceCode(this)"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>Copy</button></div>
</div>'''

# ============ MODALS PAGE ============
def gen_modals():
    items = []
    
    # 1. Basic Modal
    items.append(component_item(
        "Basic Modal", "Standard modal with header, body, and footer",
        "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Modal Title</h3><p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">A short description here</p></div>
<div class="px-6 py-5"><p class="text-sm text-gray-600 dark:text-gray-300">This is the body content of a basic modal. You can place any content here including forms, text, or other components.</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-2"><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600">Cancel</button><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Confirm</button></div>
</div></div>''',
        '<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-lg w-full mx-4">\n    <div class="px-6 py-4 border-b border-gray-100">\n      <h3 class="text-lg font-semibold">Modal Title</h3>\n    </div>\n    <div class="px-6 py-5">Body content</div>\n    <div class="px-6 py-3 border-t border-gray-100 flex justify-end gap-2">\n      <button class="px-4 py-2 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200">Cancel</button>\n      <button class="px-4 py-2 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">Confirm</button>\n    </div>\n  </div>\n</div>'
    ))
    
    # 2. Confirmation Modal
    items.append(component_item(
        "Confirmation Modal", "Destructive action confirmation with warning",
        "action", "bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700"><div class="flex items-center gap-3"><span class="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center"><svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg></span><div><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Delete Project</h3><p class="text-sm text-gray-500 dark:text-gray-400">This action cannot be undone</p></div></div></div>
<div class="px-6 py-5"><p class="text-sm text-gray-600 dark:text-gray-300">Are you sure you want to delete <strong>Project Alpha</strong>? All data including files, settings, and team members will be permanently removed.</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-2"><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700">Cancel</button><button class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors">Delete Project</button></div>
</div></div>''',
        '<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-md w-full mx-4">\n    <div class="px-6 py-4 border-b">\n      <div class="flex items-center gap-3">\n        <span class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">⚠️</span>\n        <h3 class="font-semibold">Delete Project</h3>\n      </div>\n    </div>\n    <div class="px-6 py-5"><p>Are you sure? This cannot be undone.</p></div>\n    <div class="px-6 py-3 border-t flex justify-end gap-2">\n      <button class="btn-cancel">Cancel</button>\n      <button class="btn-danger">Delete</button>\n    </div>\n  </div>\n</div>'
    ))

    # 3. Success Modal
    items.append(component_item(
        "Success Modal", "Positive feedback after action completion",
        "feedback", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo text-center">
<div class="px-6 py-8"><span class="w-16 h-16 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center mx-auto mb-4"><svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></span><h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Payment Successful!</h3><p class="text-sm text-gray-500 dark:text-gray-400">Your payment of $299.00 has been processed. A receipt has been sent to your email.</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700"><button class="w-full px-4 py-2.5 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors">View Receipt</button></div>
</div></div>''',
        '<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-sm w-full mx-4 text-center">\n    <div class="px-6 py-8">\n      <span class="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mx-auto mb-4">✓</span>\n      <h3 class="text-xl font-semibold mb-2">Payment Successful!</h3>\n      <p class="text-sm text-gray-500">Receipt sent to your email.</p>\n    </div>\n    <div class="px-6 py-3 border-t">\n      <button class="w-full btn-primary">View Receipt</button>\n    </div>\n  </div>\n</div>'
    ))

    # 4. Form Modal
    items.append(component_item(
        "Form Modal", "Modal containing form inputs for data entry",
        "form", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Create New Project</h3><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="px-6 py-5 space-y-4"><div><label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Project Name</label><input type="text" class="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500" placeholder="Enter project name"></div><div><label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label><textarea rows="3" class="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none" placeholder="Describe your project"></textarea></div><div><label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Visibility</label><select class="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700"><option>Private</option><option>Team</option><option>Public</option></select></div></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-2"><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700">Cancel</button><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Create Project</button></div>
</div></div>''',
        '<!-- Form Modal with input fields -->\n<div class="modal-overlay">\n  <div class="modal-content">\n    <div class="modal-header">\n      <h3>Create New Project</h3>\n      <button class="close-btn">&times;</button>\n    </div>\n    <div class="modal-body">\n      <form>\n        <label>Project Name</label>\n        <input type="text" placeholder="Enter name" />\n        <label>Description</label>\n        <textarea rows="3"></textarea>\n        <label>Visibility</label>\n        <select><option>Private</option></select>\n      </form>\n    </div>\n    <div class="modal-footer">\n      <button>Cancel</button>\n      <button>Create Project</button>\n    </div>\n  </div>\n</div>'
    ))

    # 5. Side Drawer / Slide-over
    items.append(component_item(
        "Side Drawer / Slide-over", "Panel sliding in from the right edge",
        "layout", "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300",
        '''<div class="modal-backdrop-demo justify-end"><div class="bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 shadow-xl h-full w-80 flex flex-col">
<div class="px-5 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between"><h3 class="font-semibold text-gray-900 dark:text-white">Notifications</h3><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="flex-1 overflow-y-auto p-5 space-y-4"><div class="flex gap-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20"><span class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/40 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg></span><div><p class="text-sm font-medium text-gray-900 dark:text-white">New deployment</p><p class="text-xs text-gray-500 dark:text-gray-400">v2.4.1 deployed 2m ago</p></div></div><div class="flex gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50"><span class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></span><div><p class="text-sm font-medium text-gray-900 dark:text-white">Tests passed</p><p class="text-xs text-gray-500 dark:text-gray-400">142/142 tests passed</p></div></div><div class="flex gap-3 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50"><span class="w-8 h-8 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01"/></svg></span><div><p class="text-sm font-medium text-gray-900 dark:text-white">SSL warning</p><p class="text-xs text-gray-500 dark:text-gray-400">Certificate expires in 7 days</p></div></div></div>
</div></div>''',
        '<!-- Side Drawer -->\n<div class="fixed inset-0 bg-black/50 z-50 flex justify-end">\n  <div class="bg-white w-96 h-full shadow-xl flex flex-col">\n    <div class="px-5 py-4 border-b flex items-center justify-between">\n      <h3 class="font-semibold">Panel Title</h3>\n      <button class="close-btn">&times;</button>\n    </div>\n    <div class="flex-1 overflow-y-auto p-5">\n      Panel content here\n    </div>\n  </div>\n</div>'
    ))

    # 6. Fullscreen Modal
    items.append(component_item(
        "Fullscreen Modal", "Full viewport modal for immersive experiences",
        "layout", "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300",
        '''<div class="modal-backdrop-demo" style="min-height:280px"><div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full h-full flex flex-col">
<div class="px-6 py-3 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between"><h3 class="font-semibold text-gray-900 dark:text-white">Media Gallery</h3><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="flex-1 overflow-y-auto p-6"><div class="grid grid-cols-3 gap-3"><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div><div class="aspect-square bg-gray-100 dark:bg-gray-700 rounded-lg"></div></div></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-between items-center"><span class="text-sm text-gray-500 dark:text-gray-400">6 of 24 items</span><div class="flex gap-2"><button class="px-3 py-1.5 text-sm text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300">Previous</button><button class="px-3 py-1.5 text-sm text-white bg-blue-600 rounded-lg hover:bg-blue-700">Next</button></div></div>
</div></div>''',
        '<!-- Fullscreen Modal -->\n<div class="fixed inset-0 z-50 bg-white dark:bg-gray-900 flex flex-col">\n  <div class="px-6 py-3 border-b flex items-center justify-between">\n    <h3>Media Gallery</h3>\n    <button class="close-btn">&times;</button>\n  </div>\n  <div class="flex-1 overflow-y-auto p-6">Content</div>\n  <div class="px-6 py-3 border-t flex justify-between">\n    <span>6 of 24 items</span>\n    <div class="flex gap-2"><button>Previous</button><button>Next</button></div>\n  </div>\n</div>'
    ))

    # 7. Info / Announcement Modal
    items.append(component_item(
        "Info / Announcement Modal", "Feature announcements and information dialogs",
        "feedback", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-5 text-center"><span class="w-14 h-14 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mx-auto mb-3"><svg class="w-7 h-7 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></span><h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">What's New in v3.0</h3><p class="text-sm text-gray-500 dark:text-gray-400">We've added dark mode, improved search, and 50+ new components. Check out the changelog for details.</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex flex-col gap-2"><button class="w-full px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Explore New Features</button><button class="w-full px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors">Maybe Later</button></div>
</div></div>''',
        '<!-- Info Modal -->\n<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-sm w-full mx-4 text-center">\n    <div class="px-6 py-5">\n      <h3 class="text-lg font-semibold mb-2">What\'s New in v3.0</h3>\n      <p class="text-sm text-gray-500">Explore new features and improvements.</p>\n    </div>\n    <div class="px-6 py-3 border-t flex flex-col gap-2">\n      <button class="btn-primary w-full">Explore</button>\n      <button class="btn-ghost w-full">Maybe Later</button>\n    </div>\n  </div>\n</div>'
    ))

    # 8. Image Lightbox Modal
    items.append(component_item(
        "Image Lightbox Modal", "Full-size image preview with zoom controls",
        "media", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '''<div class="modal-backdrop-demo !bg-black/80"><div class="text-center">
<div class="w-64 h-40 bg-gray-700 rounded-lg mb-3 flex items-center justify-center"><svg class="w-12 h-12 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg></div>
<div class="flex items-center justify-center gap-3"><button class="p-2 text-white/70 hover:text-white transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg></button><span class="text-white/60 text-sm">1 / 5</span><button class="p-2 text-white/70 hover:text-white transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button><span class="mx-3 text-white/30">|</span><button class="p-2 text-white/70 hover:text-white transition-colors"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7"/></svg></button></div>
</div></div>''',
        '<!-- Image Lightbox -->\n<div class="fixed inset-0 bg-black/90 z-50 flex items-center justify-center">\n  <img src="image.jpg" class="max-w-full max-h-[80vh] object-contain" />\n  <div class="absolute bottom-6 flex items-center gap-3">\n    <button>← Prev</button>\n    <span>1 / 5</span>\n    <button>Next →</button>\n    <button>Zoom +</button>\n  </div>\n  <button class="absolute top-4 right-4 text-white">&times;</button>\n</div>'
    ))

    # 9. Multi-step / Wizard Modal
    items.append(component_item(
        "Multi-step Wizard Modal", "Step-by-step process within a modal",
        "form", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Create Campaign</h3><div class="flex items-center gap-2 mt-3"><div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-medium">1</span><span class="text-xs font-medium text-blue-600">Details</span></div><div class="w-8 h-px bg-gray-300 dark:bg-gray-600"></div><div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-500 dark:text-gray-400 text-xs flex items-center justify-center font-medium">2</span><span class="text-xs font-medium text-gray-400">Audience</span></div><div class="w-8 h-px bg-gray-300 dark:bg-gray-600"></div><div class="flex items-center gap-2"><span class="w-6 h-6 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-500 dark:text-gray-400 text-xs flex items-center justify-center font-medium">3</span><span class="text-xs font-medium text-gray-400">Review</span></div></div></div>
<div class="px-6 py-5"><div><label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Campaign Name</label><input type="text" class="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700" placeholder="e.g., Summer Sale 2024" value="Summer Sale 2024"></div><div class="mt-4"><label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Budget</label><input type="text" class="w-full px-3 py-2 text-sm border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700" placeholder="$0.00" value="$5,000"></div></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-between"><button class="px-4 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition-colors">Skip</button><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors inline-flex items-center gap-1">Next Step<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></button></div>
</div></div>''',
        '<!-- Wizard Modal -->\n<div class="modal-overlay">\n  <div class="modal-content">\n    <div class="modal-header">\n      <h3>Create Campaign</h3>\n      <div class="steps">1 → 2 → 3</div>\n    </div>\n    <div class="modal-body">\n      <!-- Step 1 form fields -->\n    </div>\n    <div class="modal-footer">\n      <button>Skip</button>\n      <button>Next Step →</button>\n    </div>\n  </div>\n</div>'
    ))

    # 10. Toast / Notification Modal
    items.append(component_item(
        "Toast / Notification Modal", "Auto-dismissing notification popups",
        "feedback", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="flex flex-col gap-3">
<div class="flex items-center gap-3 px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm max-w-sm"><span class="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></span><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white">Changes saved</p><p class="text-xs text-gray-500 dark:text-gray-400">Your profile has been updated</p></div><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="flex items-center gap-3 px-4 py-3 bg-white dark:bg-gray-800 border border-red-200 dark:border-red-800 rounded-lg shadow-sm max-w-sm"><span class="w-8 h-8 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></span><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white">Upload failed</p><p class="text-xs text-gray-500 dark:text-gray-400">File size exceeds 10MB limit</p></div><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 flex-shrink-0"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="flex items-center gap-3 px-4 py-3 bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-800 rounded-lg shadow-sm max-w-sm"><span class="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></span><div class="flex-1 min-w-0"><p class="text-sm font-medium text-gray-900 dark:text-white">New update available</p><p class="text-xs text-gray-500 dark:text-gray-400">v3.2.1 is ready to install</p></div><button class="px-3 py-1 text-xs font-medium text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-400 rounded-md hover:bg-blue-100 dark:hover:bg-blue-900/40 transition-colors flex-shrink-0">Update</button></div>
</div>''',
        '<!-- Toast Notifications -->\n<div class="fixed top-4 right-4 z-50 space-y-2">\n  <div class="flex items-center gap-3 px-4 py-3 bg-white border rounded-lg shadow-sm">\n    <span class="icon-success">✓</span>\n    <div><p class="font-medium">Changes saved</p></div>\n    <button class="close">&times;</button>\n  </div>\n</div>'
    ))

    # 11. Cookie Consent Modal
    items.append(component_item(
        "Cookie Consent Modal", "GDPR cookie consent banner and modal",
        "action", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="w-full max-w-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg p-5">
<div class="flex gap-4"><span class="w-10 h-10 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center flex-shrink-0"><svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg></span><div><h4 class="text-sm font-semibold text-gray-900 dark:text-white mb-1">We value your privacy</h4><p class="text-xs text-gray-500 dark:text-gray-400 mb-3">We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies.</p><div class="flex flex-wrap gap-2"><button class="px-3 py-1.5 text-xs font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 transition-colors">Manage Preferences</button><button class="px-3 py-1.5 text-xs font-medium text-gray-600 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 dark:text-gray-300 transition-colors">Reject All</button><button class="px-3 py-1.5 text-xs font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Accept All</button></div></div></div>
</div>''',
        '<!-- Cookie Consent -->\n<div class="fixed bottom-4 left-4 right-4 z-50 md:left-auto md:max-w-lg">\n  <div class="bg-white border rounded-xl shadow-lg p-5">\n    <h4>We value your privacy</h4>\n    <p>We use cookies to enhance your experience.</p>\n    <div class="flex gap-2 mt-3">\n      <button>Manage</button>\n      <button>Reject</button>\n      <button class="btn-primary">Accept All</button>\n    </div>\n  </div>\n</div>'
    ))

    # 12. Error / Warning Modal
    items.append(component_item(
        "Error / Warning Modal", "Error display and warning dialogs",
        "feedback", "bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-5 text-center"><span class="w-14 h-14 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mx-auto mb-3"><svg class="w-7 h-7 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg></span><h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-1">Connection Failed</h3><p class="text-sm text-gray-500 dark:text-gray-400">Unable to reach the server. Please check your internet connection and try again.</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-center gap-2"><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700">Dismiss</button><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Retry</button></div>
</div></div>''',
        '<!-- Error Modal -->\n<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-sm mx-4 text-center">\n    <div class="px-6 py-5">\n      <span class="error-icon">⚠️</span>\n      <h3>Connection Failed</h3>\n      <p>Unable to reach server.</p>\n    </div>\n    <div class="px-6 py-3 border-t flex justify-center gap-2">\n      <button>Dismiss</button>\n      <button class="btn-primary">Retry</button>\n    </div>\n  </div>\n</div>'
    ))

    # 13. Profile / User Card Modal
    items.append(component_item(
        "Profile Card Modal", "User profile information in a modal popup",
        "content", "bg-purple-50 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo text-center">
<div class="h-16 bg-blue-600"></div>
<div class="px-6 pb-5"><div class="w-16 h-16 rounded-full bg-gray-200 dark:bg-gray-600 border-4 border-white dark:border-gray-800 -mt-8 mx-auto flex items-center justify-center text-xl font-bold text-gray-600 dark:text-gray-300">JD</div><h3 class="text-lg font-semibold text-gray-900 dark:text-white mt-2">Jane Doe</h3><p class="text-sm text-gray-500 dark:text-gray-400">Senior Product Designer</p><p class="text-sm text-gray-500 dark:text-gray-400 mt-1">San Francisco, CA</p>
<div class="flex justify-center gap-6 mt-4 pt-4 border-t border-gray-100 dark:border-gray-700"><div><p class="text-lg font-semibold text-gray-900 dark:text-white">142</p><p class="text-xs text-gray-500 dark:text-gray-400">Projects</p></div><div><p class="text-lg font-semibold text-gray-900 dark:text-white">2.4k</p><p class="text-xs text-gray-500 dark:text-gray-400">Followers</p></div><div><p class="text-lg font-semibold text-gray-900 dark:text-white">892</p><p class="text-xs text-gray-500 dark:text-gray-400">Following</p></div></div>
<div class="flex justify-center gap-2 mt-4"><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Follow</button><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700">Message</button></div>
</div></div></div>''',
        '<!-- Profile Card Modal -->\n<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">\n  <div class="bg-white rounded-xl shadow-xl max-w-sm mx-4 text-center">\n    <div class="h-16 bg-blue-600 rounded-t-xl"></div>\n    <div class="px-6 pb-5">\n      <div class="avatar -mt-8 mx-auto">JD</div>\n      <h3>Jane Doe</h3>\n      <p>Senior Product Designer</p>\n      <div class="stats">142 Projects | 2.4k Followers</div>\n      <button class="btn-primary">Follow</button>\n    </div>\n  </div>\n</div>'
    ))

    # 14. Pricing Modal
    items.append(component_item(
        "Pricing Upgrade Modal", "Upgrade and plan selection modal",
        "action", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 text-center"><h3 class="text-lg font-semibold text-gray-900 dark:text-white">Upgrade to Pro</h3><p class="text-sm text-gray-500 dark:text-gray-400">Get unlimited access to all features</p></div>
<div class="px-6 py-5 space-y-3"><div class="flex items-center gap-3 p-3 rounded-lg border-2 border-blue-600 bg-blue-50 dark:bg-blue-900/20"><div class="flex-1"><p class="text-sm font-semibold text-gray-900 dark:text-white">Pro Plan</p><p class="text-xs text-gray-500 dark:text-gray-400">Everything in Free + unlimited projects</p></div><p class="text-sm font-bold text-gray-900 dark:text-white">$12<span class="text-xs font-normal text-gray-500">/mo</span></p></div><div class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700"><div class="flex-1"><p class="text-sm font-semibold text-gray-900 dark:text-white">Team Plan</p><p class="text-xs text-gray-500 dark:text-gray-400">Pro + team collaboration & analytics</p></div><p class="text-sm font-bold text-gray-900 dark:text-white">$29<span class="text-xs font-normal text-gray-500">/mo</span></p></div></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700"><button class="w-full px-4 py-2.5 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Continue with Pro — $12/mo</button></div>
</div></div>''',
        '<!-- Pricing Modal -->\n<div class="modal-overlay">\n  <div class="modal-content">\n    <h3>Upgrade to Pro</h3>\n    <div class="plan selected">Pro - $12/mo</div>\n    <div class="plan">Team - $29/mo</div>\n    <button class="btn-primary w-full">Continue</button>\n  </div>\n</div>'
    ))

    # 15. Search / Command Palette Modal
    items.append(component_item(
        "Search / Command Palette", "Quick search and command execution overlay",
        "navigation", "bg-teal-50 dark:bg-teal-900/30 text-teal-700 dark:text-teal-300",
        '''<div class="modal-backdrop-demo"><div class="bg-white dark:bg-gray-800 rounded-xl shadow-2xl max-w-lg w-full overflow-hidden">
<div class="flex items-center gap-3 px-4 py-3 border-b border-gray-100 dark:border-gray-700"><svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg><input type="text" class="flex-1 text-sm bg-transparent outline-none text-gray-900 dark:text-white placeholder-gray-400" placeholder="Type a command or search…" value="dash"><kbd class="px-2 py-0.5 text-xs text-gray-400 bg-gray-100 dark:bg-gray-700 rounded">ESC</kbd></div>
<div class="py-2"><div class="px-4 py-1"><p class="text-xs font-medium text-gray-400 uppercase">Pages</p></div><button class="w-full px-4 py-2 text-left flex items-center gap-3 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4"/></svg><div><p class="text-sm font-medium">Dashboard</p><p class="text-xs opacity-60">Main analytics overview</p></div></button><button class="w-full px-4 py-2 text-left flex items-center gap-3 hover:bg-gray-50 dark:hover:bg-gray-700/50 text-gray-700 dark:text-gray-300"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg><div><p class="text-sm font-medium">Data Tables</p><p class="text-xs opacity-60">Sort, filter, and manage records</p></div></button></div>
</div></div>''',
        '<!-- Command Palette -->\n<div class="fixed inset-0 bg-black/50 flex items-start justify-center pt-[20vh] z-50">\n  <div class="bg-white rounded-xl shadow-2xl max-w-lg w-full">\n    <div class="flex items-center gap-3 px-4 py-3 border-b">\n      <input type="text" placeholder="Type a command…" />\n      <kbd>ESC</kbd>\n    </div>\n    <div class="py-2">\n      <button class="result-item active">Dashboard</button>\n      <button class="result-item">Data Tables</button>\n    </div>\n  </div>\n</div>'
    ))

    # 16. Image Cropper Modal
    items.append(component_item(
        "Image Cropper / Upload Modal", "Image upload with crop area preview",
        "media", "bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300",
        '''<div class="modal-backdrop-demo"><div class="modal-demo">
<div class="px-6 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between"><h3 class="font-semibold text-gray-900 dark:text-white">Upload Avatar</h3><button class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button></div>
<div class="p-6"><div class="w-48 h-48 mx-auto bg-gray-100 dark:bg-gray-700 rounded-lg relative overflow-hidden"><div class="absolute inset-4 border-2 border-white/80 rounded-full"></div><div class="absolute inset-0 bg-gray-800/30"></div><div class="absolute top-4 left-4 w-10 h-10 bg-gray-400/50 rounded"></div></div><p class="text-xs text-gray-500 dark:text-gray-400 text-center mt-3">Drag to reposition • Scroll to zoom</p></div>
<div class="px-6 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-2"><button class="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors dark:text-gray-300 dark:bg-gray-700">Cancel</button><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors">Apply</button></div>
</div></div>''',
        '<!-- Image Crop Modal -->\n<div class="modal-overlay">\n  <div class="modal-content">\n    <h3>Upload Avatar</h3>\n    <div class="crop-area">\n      <img src="preview.jpg" />\n      <div class="crop-circle"></div>\n    </div>\n    <div class="modal-footer">\n      <button>Cancel</button>\n      <button class="btn-primary">Apply</button>\n    </div>\n  </div>\n</div>'
    ))

    items_html = '\n'.join(items)
    grid = f'<div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="componentGrid">{items_html}</div>'
    
    categories = [("all","All"),("basic","Basic"),("action","Action"),("feedback","Feedback"),("form","Form"),("layout","Layout"),("media","Media"),("navigation","Navigation"),("content","Content")]
    
    html = page_head("Modals")
    html += page_header("Modals", "16 modal variants with live preview, source code, and copy functionality",
        [{"label":"Variants","value":16,"sub":"8 categories","icon_bg":"bg-blue-50 dark:bg-blue-900/30","icon_color":"text-blue-600","icon_path":"M4 6h16M4 12h16M4 18h7"},
         {"label":"States","value":48,"sub":"open/close/scroll","icon_bg":"bg-emerald-50 dark:bg-emerald-900/30","icon_color":"text-emerald-600","icon_path":"M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"},
         {"label":"Categories","value":8,"sub":"unique styles","icon_bg":"bg-violet-50 dark:bg-violet-900/30","icon_color":"text-violet-600","icon_path":"M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"},
         {"label":"Responsive","value":"100%","sub":"Mobile ready","icon_bg":"bg-amber-50 dark:bg-amber-900/30","icon_color":"text-amber-600","icon_path":"M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"}],
        "Search modals…")
    html += category_filter(categories)
    html += grid
    html += page_foot()
    
    with open(os.path.join(BASE_DIR, "133-ui-modals.html"), 'w') as f:
        f.write(html)
    print(f"Written 133-ui-modals.html ({len(html)} bytes)")

# ============ TABS PAGE ============
def gen_tabs():
    items = []
    
    # 1. Basic Tabs
    items.append(component_item(
        "Basic Tabs", "Standard horizontal tab navigation",
        "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="w-full"><div class="tab-demo"><button class="active">Overview</button><button>Analytics</button><button>Settings</button></div><div class="p-4 bg-white dark:bg-gray-800 border border-t-0 border-gray-200 dark:border-gray-700 rounded-b-lg"><p class="text-sm text-gray-600 dark:text-gray-300">This is the <strong>Overview</strong> tab content. Click any tab to switch between different content sections.</p></div></div>''',
        '<div class="tabs">\n  <div class="tab-nav border-b">\n    <button class="active">Overview</button>\n    <button>Analytics</button>\n    <button>Settings</button>\n  </div>\n  <div class="tab-content p-4">\n    <p>Tab content goes here</p>\n  </div>\n</div>'
    ))
    
    # 2. Pill Tabs
    items.append(component_item(
        "Pill Tabs", "Rounded pill-style tab indicators",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="inline-flex p-1 bg-gray-100 dark:bg-gray-800 rounded-lg"><button class="px-4 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md shadow-sm">All</button><button class="px-4 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 rounded-md">Active</button><button class="px-4 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 rounded-md">Completed</button><button class="px-4 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 rounded-md">Archived</button></div></div>''',
        '<div class="inline-flex p-1 bg-gray-100 rounded-lg">\n  <button class="px-4 py-1.5 text-sm font-medium bg-blue-600 text-white rounded-md">All</button>\n  <button class="px-4 py-1.5 text-sm text-gray-600 rounded-md">Active</button>\n  <button class="px-4 py-1.5 text-sm text-gray-600 rounded-md">Completed</button>\n</div>'
    ))
    
    # 3. Vertical Tabs
    items.append(component_item(
        "Vertical Tabs", "Side navigation tab layout",
        "layout", "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300",
        '''<div class="w-full flex gap-4"><div class="w-44 flex-shrink-0 space-y-1"><button class="w-full px-3 py-2 text-sm font-medium text-blue-600 bg-blue-50 dark:bg-blue-900/20 dark:text-blue-400 rounded-lg text-left">General</button><button class="w-full px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg text-left">Security</button><button class="w-full px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg text-left">Notifications</button><button class="w-full px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg text-left">Billing</button><button class="w-full px-3 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded-lg text-left">API</button></div><div class="flex-1 p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg"><h4 class="font-semibold text-gray-900 dark:text-white mb-2">General Settings</h4><p class="text-sm text-gray-500 dark:text-gray-400">Manage your account general settings and preferences here.</p></div></div>''',
        '<div class="flex gap-4">\n  <div class="w-44 space-y-1">\n    <button class="w-full px-3 py-2 text-sm active">General</button>\n    <button class="w-full px-3 py-2 text-sm">Security</button>\n    <button class="w-full px-3 py-2 text-sm">Notifications</button>\n  </div>\n  <div class="flex-1 p-4 border rounded-lg">\n    Content area\n  </div>\n</div>'
    ))
    
    # 4. Icon Tabs
    items.append(component_item(
        "Icon Tabs", "Tabs with icons alongside labels",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="tab-demo"><button class="active flex items-center gap-1.5"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4"/></svg>Home</button><button class="flex items-center gap-1.5"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>Profile</button><button class="flex items-center gap-1.5"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>Settings</button></div></div>''',
        '<div class="tab-nav border-b">\n  <button class="flex items-center gap-1.5"><svg>🏠</svg>Home</button>\n  <button class="flex items-center gap-1.5"><svg>👤</svg>Profile</button>\n  <button class="flex items-center gap-1.5"><svg>⚙️</svg>Settings</button>\n</div>'
    ))
    
    # 5. Underline Tabs
    items.append(component_item(
        "Underline Tabs", "Minimal underline indicator style",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="flex gap-6 border-b border-gray-200 dark:border-gray-700"><button class="pb-3 text-sm font-medium text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400 -mb-px">Recent</button><button class="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 -mb-px">Popular</button><button class="pb-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 -mb-px">Trending</button></div></div>''',
        '<div class="flex gap-6 border-b">\n  <button class="pb-3 text-sm font-medium text-blue-600 border-b-2 border-blue-600 -mb-px">Recent</button>\n  <button class="pb-3 text-sm text-gray-500 -mb-px">Popular</button>\n  <button class="pb-3 text-sm text-gray-500 -mb-px">Trending</button>\n</div>'
    ))
    
    # 6. Tab with Badge Count
    items.append(component_item(
        "Tab with Badge Count", "Tabs showing item counts in badges",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full"><div class="tab-demo"><button class="active flex items-center gap-1.5">All <span class="px-1.5 py-0.5 text-[10px] font-bold bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-full">24</span></button><button class="flex items-center gap-1.5">Active <span class="px-1.5 py-0.5 text-[10px] font-bold bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full">12</span></button><button class="flex items-center gap-1.5">Pending <span class="px-1.5 py-0.5 text-[10px] font-bold bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 rounded-full">5</span></button><button class="flex items-center gap-1.5">Closed <span class="px-1.5 py-0.5 text-[10px] font-bold bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded-full">7</span></button></div></div>''',
        '<div class="tab-nav border-b">\n  <button class="active">All <span class="badge">24</span></button>\n  <button>Active <span class="badge green">12</span></button>\n  <button>Pending <span class="badge amber">5</span></button>\n  <button>Closed <span class="badge gray">7</span></button>\n</div>'
    ))
    
    # 7. Centered Tabs
    items.append(component_item(
        "Centered Tabs", "Center-aligned tab navigation",
        "layout", "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300",
        '''<div class="w-full"><div class="tab-demo justify-center"><button>Photos</button><button class="active">Videos</button><button>Documents</button></div></div>''',
        '<div class="tab-nav border-b flex justify-center">\n  <button>Photos</button>\n  <button class="active">Videos</button>\n  <button>Documents</button>\n</div>'
    ))
    
    # 8. Card Tabs
    items.append(component_item(
        "Card Tabs", "Tab navigation within card containers",
        "layout", "bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300",
        '''<div class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl overflow-hidden"><div class="px-5 py-4 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between"><h3 class="font-semibold text-gray-900 dark:text-white">Performance</h3><div class="tab-demo border-0"><button class="active">Weekly</button><button>Monthly</button><button>Yearly</button></div></div><div class="p-5"><div class="grid grid-cols-3 gap-4 text-center"><div><p class="text-2xl font-bold text-gray-900 dark:text-white">2,847</p><p class="text-xs text-gray-500 dark:text-gray-400">Visitors</p></div><div><p class="text-2xl font-bold text-gray-900 dark:text-white">$12.4k</p><p class="text-xs text-gray-500 dark:text-gray-400">Revenue</p></div><div><p class="text-2xl font-bold text-gray-900 dark:text-white">3.2%</p><p class="text-xs text-gray-500 dark:text-gray-400">Conv. Rate</p></div></div></div></div>''',
        '<div class="card border rounded-xl">\n  <div class="px-5 py-4 border-b flex justify-between">\n    <h3>Performance</h3>\n    <div class="tabs">\n      <button class="active">Weekly</button>\n      <button>Monthly</button>\n    </div>\n  </div>\n  <div class="p-5">Content</div>\n</div>'
    ))
    
    # 9. Segmented Control Tabs
    items.append(component_item(
        "Segmented Control Tabs", "iOS-style segmented tab control",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="inline-flex p-1 bg-gray-100 dark:bg-gray-800 rounded-full"><button class="px-5 py-1.5 text-sm font-medium text-gray-500 dark:text-gray-400 rounded-full">Day</button><button class="px-5 py-1.5 text-sm font-medium text-white bg-gray-800 dark:bg-gray-600 rounded-full shadow-sm">Week</button><button class="px-5 py-1.5 text-sm font-medium text-gray-500 dark:text-gray-400 rounded-full">Month</button><button class="px-5 py-1.5 text-sm font-medium text-gray-500 dark:text-gray-400 rounded-full">Year</button></div></div>''',
        '<div class="inline-flex p-1 bg-gray-100 rounded-full">\n  <button class="px-5 py-1.5 text-sm rounded-full">Day</button>\n  <button class="px-5 py-1.5 text-sm bg-gray-800 text-white rounded-full shadow-sm">Week</button>\n  <button class="px-5 py-1.5 text-sm rounded-full">Month</button>\n</div>'
    ))
    
    # 10. Tab with Icons Only
    items.append(component_item(
        "Icon-Only Tabs", "Compact tabs using only icons",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="inline-flex p-1 bg-gray-100 dark:bg-gray-800 rounded-lg gap-1"><button class="p-2 rounded-md text-blue-600 dark:text-blue-400 bg-white dark:bg-gray-700 shadow-sm" title="Grid"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg></button><button class="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700" title="List"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/></svg></button><button class="p-2 rounded-md text-gray-500 dark:text-gray-400 hover:bg-white dark:hover:bg-gray-700" title="Map"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/></svg></button></div></div>''',
        '<div class="inline-flex p-1 bg-gray-100 rounded-lg gap-1">\n  <button class="p-2 rounded-md bg-white shadow-sm" title="Grid">▦</button>\n  <button class="p-2 rounded-md" title="List">☰</button>\n  <button class="p-2 rounded-md" title="Map">🗺</button>\n</div>'
    ))

    # 11. Step Tabs / Wizard
    items.append(component_item(
        "Step Tabs / Wizard", "Progress step indicators as tab navigation",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full"><div class="flex items-center gap-2"><div class="flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-medium">1</span><span class="text-sm font-medium text-blue-600 dark:text-blue-400">Account</span></div><div class="flex-1 h-px bg-blue-600"></div><div class="flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-medium">2</span><span class="text-sm font-medium text-blue-600 dark:text-blue-400">Profile</span></div><div class="flex-1 h-px bg-gray-300 dark:bg-gray-600"></div><div class="flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-500 dark:text-gray-400 text-xs flex items-center justify-center font-medium">3</span><span class="text-sm font-medium text-gray-400">Review</span></div><div class="flex-1 h-px bg-gray-300 dark:bg-gray-600"></div><div class="flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-500 dark:text-gray-400 text-xs flex items-center justify-center font-medium">4</span><span class="text-sm font-medium text-gray-400">Complete</span></div></div></div>''',
        '<div class="flex items-center gap-2">\n  <div class="step completed"><span>1</span>Account</div>\n  <div class="step-line active"></div>\n  <div class="step current"><span>2</span>Profile</div>\n  <div class="step-line"></div>\n  <div class="step"><span>3</span>Review</div>\n  <div class="step-line"></div>\n  <div class="step"><span>4</span>Complete</div>\n</div>'
    ))

    # 12. Bordered / Boxed Tabs
    items.append(component_item(
        "Bordered / Boxed Tabs", "Tab buttons with border styling",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full"><div class="flex gap-2"><button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-blue-600 rounded-lg">Dashboard</button><button class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">Reports</button><button class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">Analytics</button><button class="px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">Export</button></div></div>''',
        '<div class="flex gap-2">\n  <button class="px-4 py-2 text-sm border border-blue-600 bg-blue-600 text-white rounded-lg">Dashboard</button>\n  <button class="px-4 py-2 text-sm border border-gray-200 rounded-lg">Reports</button>\n  <button class="px-4 py-2 text-sm border border-gray-200 rounded-lg">Analytics</button>\n</div>'
    ))

    items_html = '\n'.join(items)
    grid = f'<div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="componentGrid">{items_html}</div>'
    
    categories = [("all","All"),("basic","Basic"),("style","Style"),("layout","Layout"),("data","Data")]
    
    html = page_head("Tabs")
    html += page_header("Tabs", "12 tab variants with live preview and source code",
        [{"label":"Variants","value":12,"sub":"5 categories","icon_bg":"bg-blue-50 dark:bg-blue-900/30","icon_color":"text-blue-600","icon_path":"M4 6h16M4 12h16M4 18h7"},
         {"label":"States","value":36,"sub":"active/hover/disabled","icon_bg":"bg-emerald-50 dark:bg-emerald-900/30","icon_color":"text-emerald-600","icon_path":"M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"},
         {"label":"Layouts","value":4,"sub":"horizontal/vertical","icon_bg":"bg-violet-50 dark:bg-violet-900/30","icon_color":"text-violet-600","icon_path":"M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"},
         {"label":"Responsive","value":"100%","sub":"Mobile ready","icon_bg":"bg-amber-50 dark:bg-amber-900/30","icon_color":"text-amber-600","icon_path":"M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"}],
        "Search tabs…")
    html += category_filter(categories)
    html += grid
    html += page_foot()
    
    with open(os.path.join(BASE_DIR, "140-ui-tabs.html"), 'w') as f:
        f.write(html)
    print(f"Written 140-ui-tabs.html ({len(html)} bytes)")

# ============ PROGRESS BAR PAGE ============
def gen_progress():
    items = []
    
    # 1. Basic Progress
    items.append(component_item(
        "Basic Progress Bars", "Standard horizontal progress indicators",
        "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="w-full space-y-4">
<div><div class="flex justify-between text-sm mb-1"><span class="text-gray-600 dark:text-gray-400">Storage Used</span><span class="font-medium text-gray-900 dark:text-white">73%</span></div><div class="progress-bar-demo"><div class="fill bg-blue-600" style="width:73%"></div></div></div>
<div><div class="flex justify-between text-sm mb-1"><span class="text-gray-600 dark:text-gray-400">Upload Progress</span><span class="font-medium text-gray-900 dark:text-white">45%</span></div><div class="progress-bar-demo"><div class="fill bg-green-600" style="width:45%"></div></div></div>
<div><div class="flex justify-between text-sm mb-1"><span class="text-gray-600 dark:text-gray-400">Memory Usage</span><span class="font-medium text-gray-900 dark:text-white">91%</span></div><div class="progress-bar-demo"><div class="fill bg-red-600" style="width:91%"></div></div></div>
</div>''',
        '<div class="progress-bar">\n  <div class="flex justify-between text-sm mb-1">\n    <span>Storage Used</span>\n    <span>73%</span>\n  </div>\n  <div class="h-2 bg-gray-200 rounded-full overflow-hidden">\n    <div class="h-full bg-blue-600 rounded-full" style="width:73%"></div>\n  </div>\n</div>'
    ))
    
    # 2. Striped Progress
    items.append(component_item(
        "Striped / Animated Progress", "Progress bars with stripe and animation effects",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full space-y-4">
<div><div class="progress-bar-demo h-3"><div class="fill bg-blue-600" style="width:65%;background:repeating-linear-gradient(45deg,transparent,transparent 10px,rgba(255,255,255,.15) 10px,rgba(255,255,255,.15) 20px)"></div></div><p class="text-xs text-gray-500 mt-1">Striped — 65%</p></div>
<div><div class="progress-bar-demo h-3"><div class="fill bg-green-600" style="width:80%;background:repeating-linear-gradient(45deg,transparent,transparent 10px,rgba(255,255,255,.15) 10px,rgba(255,255,255,.15) 20px);background-size:28px 28px;animation:progressStripe 1s linear infinite"></div></div><p class="text-xs text-gray-500 mt-1">Animated Stripe — 80%</p></div>
</div>''',
        '<div class="progress-bar h-3">\n  <div class="fill bg-blue-600" style="width:65%;\n    background: repeating-linear-gradient(45deg,transparent,transparent 10px,rgba(255,255,255,.15) 10px,rgba(255,255,255,.15) 20px)">\n  </div>\n</div>\n<style>\n@keyframes progressStripe {\n  0% { background-position: 0 0; }\n  100% { background-position: 28px 0; }\n}\n</style>'
    ))
    
    # 3. Circular / Radial Progress
    items.append(component_item(
        "Circular / Radial Progress", "SVG-based circular progress indicators",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="flex flex-wrap gap-6 items-center">
<div class="text-center"><svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="#e5e7eb" stroke-width="3"/><circle cx="18" cy="18" r="15.9" fill="none" stroke="#3b82f6" stroke-width="3" stroke-dasharray="75 25" stroke-linecap="round" class="dark:stroke-blue-400"/></svg><p class="text-sm font-semibold text-gray-900 dark:text-white mt-1">75%</p><p class="text-xs text-gray-500">Storage</p></div>
<div class="text-center"><svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="#e5e7eb" stroke-width="3"/><circle cx="18" cy="18" r="15.9" fill="none" stroke="#10b981" stroke-width="3" stroke-dasharray="45 55" stroke-linecap="round"/></svg><p class="text-sm font-semibold text-gray-900 dark:text-white mt-1">45%</p><p class="text-xs text-gray-500">CPU</p></div>
<div class="text-center"><svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="#e5e7eb" stroke-width="3"/><circle cx="18" cy="18" r="15.9" fill="none" stroke="#f59e0b" stroke-width="3" stroke-dasharray="60 40" stroke-linecap="round"/></svg><p class="text-sm font-semibold text-gray-900 dark:text-white mt-1">60%</p><p class="text-xs text-gray-500">Memory</p></div>
<div class="text-center"><svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36"><circle cx="18" cy="18" r="15.9" fill="none" stroke="#e5e7eb" stroke-width="3"/><circle cx="18" cy="18" r="15.9" fill="none" stroke="#ef4444" stroke-width="3" stroke-dasharray="92 8" stroke-linecap="round"/></svg><p class="text-sm font-semibold text-gray-900 dark:text-white mt-1">92%</p><p class="text-xs text-gray-500">Disk</p></div>
</div>''',
        '<svg class="w-20 h-20 -rotate-90" viewBox="0 0 36 36">\n  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#e5e7eb" stroke-width="3"/>\n  <circle cx="18" cy="18" r="15.9" fill="none" stroke="#3b82f6" stroke-width="3"\n    stroke-dasharray="75 25" stroke-linecap="round"/>\n</svg>\n<p>75%</p>'
    ))
    
    # 4. Multi-segment Progress
    items.append(component_item(
        "Multi-segment Progress", "Stacked progress with multiple segments",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full space-y-4">
<div><div class="flex justify-between text-sm mb-1"><span class="text-gray-600 dark:text-gray-400">Sprint Progress</span></div><div class="progress-bar-demo h-4 !rounded-lg"><div class="flex h-full rounded-lg overflow-hidden"><div class="bg-green-500" style="width:40%"></div><div class="bg-blue-500" style="width:25%"></div><div class="bg-amber-500" style="width:15%"></div><div class="bg-gray-300 dark:bg-gray-600" style="width:20%"></div></div></div><div class="flex gap-4 mt-2 text-xs"><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-green-500"></span>Done 40%</span><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-blue-500"></span>In Progress 25%</span><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-amber-500"></span>Review 15%</span><span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-gray-300 dark:bg-gray-600"></span>Todo 20%</span></div></div>
</div>''',
        '<div class="h-4 bg-gray-200 rounded-lg overflow-hidden">\n  <div class="flex h-full">\n    <div class="bg-green-500" style="width:40%"></div>\n    <div class="bg-blue-500" style="width:25%"></div>\n    <div class="bg-amber-500" style="width:15%"></div>\n    <div class="bg-gray-300" style="width:20%"></div>\n  </div>\n</div>'
    ))
    
    # 5. Step Progress / Stepper
    items.append(component_item(
        "Step Progress / Stepper", "Multi-step process progress indicator",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full"><div class="flex items-center"><div class="flex flex-col items-center"><span class="w-8 h-8 rounded-full bg-green-600 text-white text-sm flex items-center justify-center font-medium"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></span><span class="text-xs font-medium text-green-600 mt-1">Cart</span></div><div class="flex-1 h-0.5 bg-green-600"></div><div class="flex flex-col items-center"><span class="w-8 h-8 rounded-full bg-green-600 text-white text-sm flex items-center justify-center font-medium"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg></span><span class="text-xs font-medium text-green-600 mt-1">Shipping</span></div><div class="flex-1 h-0.5 bg-blue-600"></div><div class="flex flex-col items-center"><span class="w-8 h-8 rounded-full bg-blue-600 text-white text-sm flex items-center justify-center font-medium">3</span><span class="text-xs font-medium text-blue-600 mt-1">Payment</span></div><div class="flex-1 h-0.5 bg-gray-200 dark:bg-gray-700"></div><div class="flex flex-col items-center"><span class="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400 text-sm flex items-center justify-center font-medium">4</span><span class="text-xs font-medium text-gray-400 mt-1">Confirm</span></div></div></div>''',
        '<div class="flex items-center">\n  <div class="step completed"><span>✓</span>Cart</div>\n  <div class="flex-1 h-0.5 bg-green-600"></div>\n  <div class="step completed"><span>✓</span>Shipping</div>\n  <div class="flex-1 h-0.5 bg-blue-600"></div>\n  <div class="step current"><span>3</span>Payment</div>\n  <div class="flex-1 h-0.5 bg-gray-200"></div>\n  <div class="step"><span>4</span>Confirm</div>\n</div>'
    ))
    
    # 6. Thin / Slim Progress
    items.append(component_item(
        "Thin / Slim Progress", "Minimal thin progress bars for inline use",
        "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="w-full space-y-3">
<div class="flex items-center gap-3"><span class="text-xs text-gray-600 dark:text-gray-400 w-20">React</span><div class="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full"><div class="h-full bg-blue-600 rounded-full" style="width:90%"></div></div><span class="text-xs font-medium text-gray-900 dark:text-white w-8 text-right">90%</span></div>
<div class="flex items-center gap-3"><span class="text-xs text-gray-600 dark:text-gray-400 w-20">TypeScript</span><div class="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full"><div class="h-full bg-blue-600 rounded-full" style="width:78%"></div></div><span class="text-xs font-medium text-gray-900 dark:text-white w-8 text-right">78%</span></div>
<div class="flex items-center gap-3"><span class="text-xs text-gray-600 dark:text-gray-400 w-20">Python</span><div class="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full"><div class="h-full bg-green-600 rounded-full" style="width:65%"></div></div><span class="text-xs font-medium text-gray-900 dark:text-white w-8 text-right">65%</span></div>
<div class="flex items-center gap-3"><span class="text-xs text-gray-600 dark:text-gray-400 w-20">Rust</span><div class="flex-1 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full"><div class="h-full bg-amber-500 rounded-full" style="width:35%"></div></div><span class="text-xs font-medium text-gray-900 dark:text-white w-8 text-right">35%</span></div>
</div>''',
        '<div class="flex items-center gap-3">\n  <span class="text-xs w-20">React</span>\n  <div class="flex-1 h-1.5 bg-gray-200 rounded-full">\n    <div class="h-full bg-blue-600 rounded-full" style="width:90%"></div>\n  </div>\n  <span class="text-xs w-8 text-right">90%</span>\n</div>'
    ))
    
    # 7. Progress with Label Inside
    items.append(component_item(
        "Progress with Label Inside", "Progress bars with text inside the bar",
        "style", "bg-violet-50 dark:bg-violet-900/30 text-violet-700 dark:text-violet-300",
        '''<div class="w-full space-y-3">
<div class="progress-bar-demo h-6 !rounded-lg"><div class="fill bg-blue-600 rounded-lg flex items-center justify-end pr-2" style="width:68%"><span class="text-xs font-medium text-white">68%</span></div></div>
<div class="progress-bar-demo h-6 !rounded-lg"><div class="fill bg-green-600 rounded-lg flex items-center justify-end pr-2" style="width:45%"><span class="text-xs font-medium text-white">45%</span></div></div>
<div class="progress-bar-demo h-6 !rounded-lg"><div class="fill bg-red-600 rounded-lg flex items-center justify-end pr-2" style="width:88%"><span class="text-xs font-medium text-white">88%</span></div></div>
</div>''',
        '<div class="h-6 bg-gray-200 rounded-lg overflow-hidden">\n  <div class="h-full bg-blue-600 rounded-lg flex items-center justify-end pr-2" style="width:68%">\n    <span class="text-xs font-medium text-white">68%</span>\n  </div>\n</div>'
    ))
    
    # 8. Color Variants
    items.append(component_item(
        "Color Variants", "Progress bars in different semantic colors",
        "basic", "bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300",
        '''<div class="w-full space-y-3">
<div class="progress-bar-demo"><div class="fill bg-blue-600" style="width:70%"></div></div><p class="text-xs text-gray-500">Blue — Default (70%)</p>
<div class="progress-bar-demo"><div class="fill bg-green-600" style="width:55%"></div></div><p class="text-xs text-gray-500">Green — Success (55%)</p>
<div class="progress-bar-demo"><div class="fill bg-amber-500" style="width:80%"></div></div><p class="text-xs text-gray-500">Amber — Warning (80%)</p>
<div class="progress-bar-demo"><div class="fill bg-red-600" style="width:95%"></div></div><p class="text-xs text-gray-500">Red — Danger (95%)</p>
<div class="progress-bar-demo"><div class="fill bg-purple-600" style="width:40%"></div></div><p class="text-xs text-gray-500">Purple — Info (40%)</p>
</div>''',
        '<div class="h-2 bg-gray-200 rounded-full overflow-hidden">\n  <div class="h-full bg-blue-600 rounded-full" style="width:70%"></div>\n</div>\n<!-- Use bg-green-600, bg-amber-500, bg-red-600, bg-purple-600 -->'
    ))

    # 9. Skeleton Loading
    items.append(component_item(
        "Skeleton Loading Bars", "Placeholder progress indicators for loading states",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full space-y-3">
<div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full w-full animate-pulse"></div>
<div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full w-4/5 animate-pulse"></div>
<div class="h-3 bg-gray-200 dark:bg-gray-700 rounded-full w-3/5 animate-pulse"></div>
<div class="h-8 bg-gray-200 dark:bg-gray-700 rounded-lg w-2/5 animate-pulse mt-2"></div>
</div>''',
        '<div class="space-y-3">\n  <div class="h-3 bg-gray-200 rounded-full w-full animate-pulse"></div>\n  <div class="h-3 bg-gray-200 rounded-full w-4/5 animate-pulse"></div>\n  <div class="h-3 bg-gray-200 rounded-full w-3/5 animate-pulse"></div>\n  <div class="h-8 bg-gray-200 rounded-lg w-2/5 animate-pulse"></div>\n</div>'
    ))

    # 10. Dashboard Metric Cards with Progress
    items.append(component_item(
        "Dashboard Metric Cards", "Cards combining metrics with progress indicators",
        "data", "bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-300",
        '''<div class="w-full grid grid-cols-2 gap-3">
<div class="p-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl"><div class="flex items-center justify-between mb-2"><span class="text-xs text-gray-500 dark:text-gray-400">Revenue</span><span class="text-xs font-medium text-green-600">+12%</span></div><p class="text-xl font-bold text-gray-900 dark:text-white">$48,250</p><div class="mt-2 progress-bar-demo h-1.5"><div class="fill bg-green-500" style="width:72%"></div></div></div>
<div class="p-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl"><div class="flex items-center justify-between mb-2"><span class="text-xs text-gray-500 dark:text-gray-400">Users</span><span class="text-xs font-medium text-blue-600">+8%</span></div><p class="text-xl font-bold text-gray-900 dark:text-white">12,480</p><div class="mt-2 progress-bar-demo h-1.5"><div class="fill bg-blue-500" style="width:58%"></div></div></div>
<div class="p-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl"><div class="flex items-center justify-between mb-2"><span class="text-xs text-gray-500 dark:text-gray-400">Orders</span><span class="text-xs font-medium text-amber-600">-3%</span></div><p class="text-xl font-bold text-gray-900 dark:text-white">1,284</p><div class="mt-2 progress-bar-demo h-1.5"><div class="fill bg-amber-500" style="width:45%"></div></div></div>
<div class="p-4 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl"><div class="flex items-center justify-between mb-2"><span class="text-xs text-gray-500 dark:text-gray-400">Conversion</span><span class="text-xs font-medium text-purple-600">+5%</span></div><p class="text-xl font-bold text-gray-900 dark:text-white">3.24%</p><div class="mt-2 progress-bar-demo h-1.5"><div class="fill bg-purple-500" style="width:32%"></div></div></div>
</div>''',
        '<div class="p-4 bg-white border rounded-xl">\n  <span class="text-xs text-gray-500">Revenue</span>\n  <p class="text-xl font-bold">$48,250</p>\n  <div class="mt-2 h-1.5 bg-gray-200 rounded-full">\n    <div class="h-full bg-green-500 rounded-full" style="width:72%"></div>\n  </div>\n</div>'
    ))

    items_html = '\n'.join(items)
    grid = f'<div class="grid grid-cols-1 lg:grid-cols-2 gap-6" id="componentGrid">{items_html}</div>'
    
    categories = [("all","All"),("basic","Basic"),("style","Style"),("data","Data")]
    
    html = page_head("Progress Bars")
    html += page_header("Progress Bars", "10 progress bar variants with live preview and source code",
        [{"label":"Variants","value":10,"sub":"4 categories","icon_bg":"bg-blue-50 dark:bg-blue-900/30","icon_color":"text-blue-600","icon_path":"M4 6h16M4 12h16M4 18h7"},
         {"label":"States","value":30,"sub":"static/animated/loading","icon_bg":"bg-emerald-50 dark:bg-emerald-900/30","icon_color":"text-emerald-600","icon_path":"M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"},
         {"label":"Styles","value":4,"sub":"linear/circular/stepper","icon_bg":"bg-violet-50 dark:bg-violet-900/30","icon_color":"text-violet-600","icon_path":"M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"},
         {"label":"Responsive","value":"100%","sub":"Mobile ready","icon_bg":"bg-amber-50 dark:bg-amber-900/30","icon_color":"text-amber-600","icon_path":"M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"}],
        "Search progress…")
    html += category_filter(categories)
    html += grid
    html += page_foot("/* Stripe animation */\n@keyframes progressStripe{0%{background-position:0 0}100%{background-position:28px 0}}")
    
    with open(os.path.join(BASE_DIR, "137-ui-progressbar.html"), 'w') as f:
        f.write(html)
    print(f"Written 137-ui-progressbar.html ({len(html)} bytes)")

# Run all generators
if __name__ == "__main__":
    gen_modals()
    gen_tabs()
    gen_progress()
    print("All UI pages generated!")
