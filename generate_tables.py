#!/usr/bin/env python3
"""Generate premium table pages with search, sorting, filters, pagination, etc."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def page_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en" class="scroll-smooth">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<meta name="theme-color" content="#465fff"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n.no-scrollbar::-webkit-scrollbar{display:none}\n.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@media(prefers-reduced-motion:reduce){.fade-up{animation:none}}\n.data-table{width:100%;border-collapse:separate;border-spacing:0}\n.data-table thead th{padding:.75rem 1rem;font-size:.75rem;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:#64748b;border-bottom:2px solid #e2e8f0;text-align:left;white-space:nowrap;position:sticky;top:0;background:#f8fafc;z-index:1}\n.dark .data-table thead th{background:#1e293b;border-color:#334155;color:#94a3b8}\n.data-table tbody td{padding:.75rem 1rem;font-size:.875rem;border-bottom:1px solid #f1f5f9;color:#334155}\n.dark .data-table tbody td{border-color:#1e293b;color:#cbd5e1}\n.data-table tbody tr:hover{background:#f8fafc}\n.dark .data-table tbody tr:hover{background:#1e293b}\n.data-table tbody tr.selected{background:#eef2ff}\n.dark .data-table tbody tr.selected{background:#1e1b4b}\n.sortable{cursor:pointer;user-select:none}\n.sortable:hover{color:#6366f1}\n.sort-icon{display:inline-block;margin-left:.25rem;opacity:.3}\n.sort-icon.active{opacity:1}\n.status-badge{display:inline-flex;align-items:center;gap:.375rem;padding:.25rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:500}\n.status-badge::before{content:"";width:6px;height:6px;border-radius:50%}\n.status-success{background:#dcfce7;color:#166534}.status-success::before{background:#22c55e}\n.status-warning{background:#fef3c7;color:#92400e}.status-warning::before{background:#f59e0b}\n.status-danger{background:#fef2f2;color:#991b1b}.status-danger::before{background:#ef4444}\n.status-info{background:#dbeafe;color:#1e40af}.status-info::before{background:#3b82f6}\n.status-neutral{background:#f1f5f9;color:#475569}.status-neutral::before{background:#94a3b8}\n.dark .status-success{background:#052e16;color:#86efac}\n.dark .status-warning{background:#422006;color:#fde68a}\n.dark .status-danger{background:#450a0a;color:#fca5a5}\n.dark .status-info{background:#172554;color:#93c5fd}\n.dark .status-neutral{background:#1e293b;color:#94a3b8}\n.pagination{display:flex;align-items:center;gap:.25rem}\n.page-btn{display:flex;align-items:center;justify-content:center;width:2rem;height:2rem;border-radius:.375rem;font-size:.8125rem;border:1px solid #e2e8f0;background:#fff;color:#334155;cursor:pointer;transition:all .15s}\n.page-btn:hover{background:#f1f5f9;border-color:#cbd5e1}\n.page-btn.active{background:#6366f1;border-color:#6366f1;color:#fff}\n.page-btn:disabled{opacity:.4;cursor:not-allowed}\n.dark .page-btn{background:#1e293b;border-color:#334155;color:#e2e8f0}\n.dark .page-btn:hover{background:#334155}\n.dark .page-btn.active{background:#6366f1;border-color:#6366f1}\n.bulk-bar{display:none;padding:.75rem 1rem;background:#eef2ff;border-radius:.5rem;margin-bottom:1rem;font-size:.875rem;color:#4338ca;align-items:center;gap:.75rem}\n.bulk-bar.visible{display:flex}\n.dark .bulk-bar{background:#1e1b4b;color:#a5b4fc}\n.empty-state{text-align:center;padding:3rem 1rem}\n.empty-state svg{margin:0 auto 1rem}\n.skeleton{background:linear-gradient(90deg,#f1f5f9 25%,#e2e8f0 50%,#f1f5f9 75%);background-size:200% 100%;animation:shimmer 1.5s infinite;border-radius:.25rem}\n@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}\n.dark .skeleton{background:linear-gradient(90deg,#1e293b 25%,#334155 50%,#1e293b 75%);background-size:200% 100%}\n.filter-chip{display:inline-flex;align-items:center;gap:.375rem;padding:.375rem .75rem;border-radius:9999px;font-size:.75rem;font-weight:500;border:1px solid #e2e8f0;background:#fff;color:#334155;cursor:pointer;transition:all .15s}\n.filter-chip:hover{border-color:#cbd5e1;background:#f8fafc}\n.filter-chip.active{background:#6366f1;border-color:#6366f1;color:#fff}\n.dark .filter-chip{background:#1e293b;border-color:#334155;color:#e2e8f0}\n.dark .filter-chip.active{background:#6366f1;border-color:#6366f1}\n' + extra_css + '\n</style>\n</head>\n'

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
    return breadcrumb('Home', 'Tables', title) + '<div class="mb-6 fade-up">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">' + esc(title) + '</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">' + esc(desc) + '</p>\n</div>\n'

def status_badge(text, cls):
    return '<span class="status-badge status-' + cls + '">' + esc(text) + '</span>'

def avatar_cell(name, email, img_seed=''):
    seed = img_seed or name.lower().replace(' ','-')
    return '<div class="flex items-center gap-3"><img src="https://images.unsplash.com/photo-' + seed + '?w=32&h=32&fit=crop&crop=face" class="w-8 h-8 rounded-full object-cover" alt="" onerror="this.style.display=\'none\'"/><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</p><p class="text-xs text-slate-400">' + esc(email) + '</p></div></div>'

def action_dropdown():
    return '<div class="relative"><button type="button" class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800" onclick="toggleActionMenu(this)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/></svg></button><div class="action-menu absolute right-0 top-full mt-1 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg shadow-lg py-1 z-10 min-w-[120px]" style="display:none"><a href="#" class="block px-3 py-1.5 text-sm hover:bg-slate-50 dark:hover:bg-slate-700" onclick="showToast(\'View action\',\'info\');return false">View</a><a href="#" class="block px-3 py-1.5 text-sm hover:bg-slate-50 dark:hover:bg-slate-700" onclick="showToast(\'Edit action\',\'info\');return false">Edit</a><a href="#" class="block px-3 py-1.5 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20" onclick="showToast(\'Delete action\',\'error\');return false">Delete</a></div></div>'

# ============================================================
# Data Table Page
# ============================================================
def gen_data_table():
    title = 'Data Table'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Full-featured data table with search, sort, filter, and pagination')

    # Stats
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    stats = [('Total Users', '2,847', '+12.5%', 'up'), ('Active', '2,103', '+8.2%', 'up'), ('Inactive', '744', '-3.1%', 'down'), ('New This Month', '186', '+24.3%', 'up')]
    for label, val, change, dir in stats:
        color = 'text-green-600' if dir == 'up' else 'text-red-500'
        arrow = '&#9650;' if dir == 'up' else '&#9660;'
        h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-4"><p class="text-xs text-slate-400 mb-1">' + label + '</p><p class="text-xl font-bold text-slate-900 dark:text-white">' + val + '</p><p class="text-xs ' + color + '">' + arrow + ' ' + change + '</p></div>\n'
    h += '</div>\n'

    # Toolbar
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up">\n'
    h += '<div class="p-4 border-b border-slate-100 dark:border-slate-800">\n'
    h += '<div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">\n'
    # Search
    h += '<div class="relative flex-1 max-w-xs"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><input type="text" class="form-input pl-9" placeholder="Search users..." oninput="filterTable(this.value)"/></div>\n'
    # Filters
    h += '<div class="flex gap-2 flex-wrap">\n'
    for f in ['All', 'Active', 'Inactive', 'Pending']:
        active = ' active' if f == 'All' else ''
        h += '<button type="button" class="filter-chip' + active + '" onclick="filterByStatus(this,\'' + f.lower() + '\')">' + f + '</button>\n'
    h += '</div>\n'
    # Actions
    h += '<div class="flex gap-2"><button type="button" class="px-3 py-1.5 text-xs font-medium bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Export started\',\'success\')">Export</button></div>\n'
    h += '</div>\n</div>\n'

    # Bulk bar
    h += '<div class="bulk-bar mx-4 mt-4" id="bulk-bar"><span id="bulk-count">0</span> selected <button type="button" class="text-xs font-medium underline" onclick="showToast(\'Bulk delete triggered\',\'error\')">Delete</button><button type="button" class="text-xs font-medium underline" onclick="showToast(\'Bulk export triggered\',\'info\')">Export</button><button type="button" class="text-xs font-medium underline ml-auto" onclick="clearSelection()">Clear</button></div>\n'

    # Table
    h += '<div class="overflow-x-auto">\n<table class="data-table" id="data-table">\n<thead>\n<tr>\n<th class="w-10"><input type="checkbox" id="select-all" onchange="toggleSelectAll(this)"/></th>\n<th class="sortable" onclick="sortTable(1)">Name <span class="sort-icon">&#8597;</span></th>\n<th class="sortable" onclick="sortTable(2)">Email <span class="sort-icon">&#8597;</span></th>\n<th class="sortable" onclick="sortTable(3)">Role <span class="sort-icon">&#8597;</span></th>\n<th>Status</th>\n<th class="sortable" onclick="sortTable(5)">Joined <span class="sort-icon">&#8597;</span></th>\n<th class="w-10"></th>\n</tr>\n</thead>\n<tbody id="table-body">\n'

    users = [
        ('Alice Johnson', 'alice@example.com', 'Admin', 'success', 'Jan 15, 2024'),
        ('Bob Smith', 'bob@example.com', 'Editor', 'success', 'Feb 3, 2024'),
        ('Carol White', 'carol@example.com', 'Viewer', 'neutral', 'Mar 12, 2024'),
        ('David Brown', 'david@example.com', 'Editor', 'warning', 'Apr 7, 2024'),
        ('Eve Davis', 'eve@example.com', 'Admin', 'success', 'May 20, 2024'),
        ('Frank Miller', 'frank@example.com', 'Viewer', 'danger', 'Jun 1, 2024'),
        ('Grace Lee', 'grace@example.com', 'Editor', 'success', 'Jul 14, 2024'),
        ('Henry Wilson', 'henry@example.com', 'Viewer', 'neutral', 'Aug 22, 2024'),
        ('Irene Moore', 'irene@example.com', 'Admin', 'success', 'Sep 5, 2024'),
        ('Jack Taylor', 'jack@example.com', 'Editor', 'warning', 'Oct 18, 2024'),
        ('Karen Anderson', 'karen@example.com', 'Viewer', 'success', 'Nov 2, 2024'),
        ('Leo Thomas', 'leo@example.com', 'Admin', 'success', 'Dec 8, 2024'),
        ('Mia Jackson', 'mia@example.com', 'Editor', 'neutral', 'Jan 25, 2025'),
        ('Nathan Harris', 'nathan@example.com', 'Viewer', 'danger', 'Feb 14, 2025'),
        ('Olivia Martin', 'olivia@example.com', 'Admin', 'success', 'Mar 3, 2025'),
    ]

    for name, email, role, status, joined in users:
        h += '<tr data-status="' + status + '">\n'
        h += '<td><input type="checkbox" class="row-check" onchange="updateBulkBar()"/></td>\n'
        h += '<td><div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center text-xs font-medium text-indigo-600 dark:text-indigo-400">' + name[0] + '</div><span class="font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</span></div></td>\n'
        h += '<td class="text-slate-500 dark:text-slate-400">' + esc(email) + '</td>\n'
        h += '<td>' + esc(role) + '</td>\n'
        h += '<td>' + status_badge(status.capitalize(), status) + '</td>\n'
        h += '<td class="text-slate-500 dark:text-slate-400">' + esc(joined) + '</td>\n'
        h += '<td>' + action_dropdown() + '</td>\n'
        h += '</tr>\n'

    h += '</tbody>\n</table>\n</div>\n'

    # Pagination
    h += '<div class="p-4 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3">\n'
    h += '<p class="text-sm text-slate-400">Showing 1-15 of 2,847</p>\n'
    h += '<div class="pagination">\n'
    h += '<button class="page-btn" disabled>&laquo;</button>\n'
    h += '<button class="page-btn active">1</button>\n'
    for p in range(2, 8):
        h += '<button class="page-btn" onclick="showToast(\'Page ' + str(p) + '\',\'info\')">' + str(p) + '</button>\n'
    h += '<button class="page-btn" disabled>...</button>\n'
    h += '<button class="page-btn" onclick="showToast(\'Last page\',\'info\')">190</button>\n'
    h += '<button class="page-btn">&raquo;</button>\n'
    h += '</div>\n</div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function filterTable(query){
  var rows=document.querySelectorAll('#table-body tr');
  query=query.toLowerCase();
  rows.forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(query)>=0?'':'none'});
}
function filterByStatus(btn,status){
  document.querySelectorAll('.filter-chip').forEach(function(c){c.classList.remove('active')});
  btn.classList.add('active');
  var rows=document.querySelectorAll('#table-body tr');
  rows.forEach(function(r){
    if(status==='all')r.style.display='';
    else r.style.display=r.dataset.status===status?'':'none';
  });
}
function toggleSelectAll(cb){
  document.querySelectorAll('.row-check').forEach(function(c){c.checked=cb.checked});
  updateBulkBar();
}
function updateBulkBar(){
  var checked=document.querySelectorAll('.row-check:checked').length;
  var bar=document.getElementById('bulk-bar');
  document.getElementById('bulk-count').textContent=checked;
  bar.classList.toggle('visible',checked>0);
}
function clearSelection(){
  document.querySelectorAll('.row-check').forEach(function(c){c.checked=false});
  document.getElementById('select-all').checked=false;
  updateBulkBar();
}
function toggleActionMenu(btn){
  var menu=btn.nextElementSibling;
  document.querySelectorAll('.action-menu').forEach(function(m){if(m!==menu)m.style.display='none'});
  menu.style.display=menu.style.display==='none'?'block':'none';
}
document.addEventListener('click',function(e){if(!e.target.closest('.action-menu')&&!e.target.closest('[onclick*="toggleActionMenu"]'))document.querySelectorAll('.action-menu').forEach(function(m){m.style.display='none'})});
var sortDir={};
function sortTable(col){
  var tbody=document.getElementById('table-body'),rows=Array.from(tbody.querySelectorAll('tr'));
  sortDir[col]=!sortDir[col];
  rows.sort(function(a,b){
    var ta=a.cells[col].textContent.trim(),tb=b.cells[col].textContent.trim();
    var na=parseFloat(ta.replace(/[^0-9.-]/g,'')),nb=parseFloat(tb.replace(/[^0-9.-]/g,''));
    if(!isNaN(na)&&!isNaN(nb))return sortDir[col]?na-nb:nb-na;
    return sortDir[col]?ta.localeCompare(tb):tb.localeCompare(ta);
  });
  rows.forEach(function(r){tbody.appendChild(r)});
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Basic Table Page
# ============================================================
def gen_basic_table():
    title = 'Basic Tables'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Standard table styles and variations')

    # Striped Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Striped Table</h3></div>\n<div class="overflow-x-auto">\n<table class="data-table">\n<thead><tr><th>#</th><th>Name</th><th>Email</th><th>Role</th><th>Status</th></tr></thead>\n<tbody>\n'
    for i, (name, email, role, status) in enumerate([
        ('Alice Johnson', 'alice@acme.com', 'Admin', 'success'),
        ('Bob Smith', 'bob@acme.com', 'Editor', 'info'),
        ('Carol White', 'carol@acme.com', 'Viewer', 'neutral'),
        ('David Brown', 'david@acme.com', 'Editor', 'warning'),
        ('Eve Davis', 'eve@acme.com', 'Admin', 'success'),
    ], 1):
        h += '<tr class="' + ('bg-slate-50 dark:bg-slate-800/50' if i % 2 == 0 else '') + '"><td>' + str(i) + '</td><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</td><td class="text-slate-500">' + esc(email) + '</td><td>' + esc(role) + '</td><td>' + status_badge(status.capitalize(), status) + '</td></tr>\n'
    h += '</tbody></table></div></div>\n'

    # Bordered Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Bordered Table</h3></div>\n<div class="overflow-x-auto">\n<table class="w-full border-collapse" style="border:1px solid #e2e8f0">\n<thead><tr style="border:1px solid #e2e8f0"><th style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.75rem;font-weight:600;text-transform:uppercase;color:#64748b;text-align:left;background:#f8fafc">Product</th><th style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.75rem;font-weight:600;text-transform:uppercase;color:#64748b;text-align:left;background:#f8fafc">Category</th><th style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.75rem;font-weight:600;text-transform:uppercase;color:#64748b;text-align:left;background:#f8fafc">Price</th><th style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.75rem;font-weight:600;text-transform:uppercase;color:#64748b;text-align:left;background:#f8fafc">Stock</th></tr></thead>\n<tbody>\n'
    for product, cat, price, stock in [
        ('MacBook Pro 16"', 'Laptops', '$2,499', 'In Stock'),
        ('iPhone 15 Pro', 'Phones', '$999', 'In Stock'),
        ('iPad Air', 'Tablets', '$599', 'Low Stock'),
        ('AirPods Pro', 'Audio', '$249', 'In Stock'),
        ('Apple Watch Ultra', 'Wearables', '$799', 'Out of Stock'),
    ]:
        s_cls = 'success' if stock == 'In Stock' else ('warning' if stock == 'Low Stock' else 'danger')
        h += '<tr style="border:1px solid #e2e8f0"><td style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.875rem;font-weight:500;color:#334155">' + esc(product) + '</td><td style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.875rem;color:#64748b">' + esc(cat) + '</td><td style="border:1px solid #e2e8f0;padding:.75rem 1rem;font-size:.875rem;color:#334155">' + esc(price) + '</td><td style="border:1px solid #e2e8f0;padding:.75rem 1rem">' + status_badge(stock, s_cls) + '</td></tr>\n'
    h += '</tbody></table></div></div>\n'

    # Hover Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Hover Table</h3></div>\n<div class="overflow-x-auto">\n<table class="data-table">\n<thead><tr><th>Project</th><th>Lead</th><th>Budget</th><th>Progress</th><th>Status</th></tr></thead>\n<tbody>\n'
    for proj, lead, budget, pct, status in [
        ('Website Redesign', 'Sarah K.', '$12,400', '75', 'success'),
        ('Mobile App', 'Mike R.', '$28,500', '45', 'info'),
        ('API Integration', 'Tom B.', '$8,200', '90', 'success'),
        ('Dashboard v2', 'Lisa M.', '$15,800', '20', 'warning'),
        ('ML Pipeline', 'Alex P.', '$42,000', '60', 'info'),
    ]:
        bar_color = '#22c55e' if pct >= '70' else ('#f59e0b' if pct >= '40' else '#ef4444')
        h += '<tr><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(proj) + '</td><td class="text-slate-500">' + esc(lead) + '</td><td>' + esc(budget) + '</td><td><div class="flex items-center gap-2"><div class="flex-1 h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden"><div class="h-full rounded-full" style="width:' + pct + '%;background:' + bar_color + '"></div></div><span class="text-xs text-slate-400">' + pct + '%</span></div></td><td>' + status_badge(status.capitalize(), status) + '</td></tr>\n'
    h += '</tbody></table></div></div>\n'

    # Compact Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Compact Table</h3></div>\n<div class="overflow-x-auto">\n<table class="data-table" style="font-size:.8125rem">\n<thead><tr><th style="padding:.5rem .75rem">ID</th><th style="padding:.5rem .75rem">Name</th><th style="padding:.5rem .75rem">Type</th><th style="padding:.5rem .75rem">Date</th></tr></thead>\n<tbody>\n'
    for i, (name, typ, date) in enumerate([
        ('Payment Gateway', 'Integration', '2024-01-15'),
        ('User Auth', 'Service', '2024-02-20'),
        ('Analytics', 'Module', '2024-03-10'),
        ('Email Service', 'Integration', '2024-04-05'),
        ('CDN Config', 'Infrastructure', '2024-05-12'),
        ('Cache Layer', 'Infrastructure', '2024-06-18'),
        ('Search Engine', 'Service', '2024-07-22'),
    ], 1):
        h += '<tr><td style="padding:.375rem .75rem" class="text-slate-400">#' + str(i).zfill(3) + '</td><td style="padding:.375rem .75rem" class="font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</td><td style="padding:.375rem .75rem" class="text-slate-500">' + esc(typ) + '</td><td style="padding:.375rem .75rem" class="text-slate-400">' + esc(date) + '</td></tr>\n'
    h += '</tbody></table></div></div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Advanced Table Page
# ============================================================
def gen_advanced_table():
    title = 'Advanced Tables'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Advanced table features with expandable rows and inline editing')

    # Expandable Rows Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Expandable Rows</h3><p class="text-sm text-slate-400 mt-1">Click a row to see details</p></div>\n<div class="overflow-x-auto">\n<table class="data-table" id="expand-table">\n<thead><tr><th class="w-8"></th><th>Order ID</th><th>Customer</th><th>Amount</th><th>Status</th><th>Date</th></tr></thead>\n<tbody>\n'
    orders = [
        ('ORD-001', 'Acme Corp', '$4,250.00', 'success', 'Jan 15, 2024', '3 items: Widget A x2, Widget B x1'),
        ('ORD-002', 'Globex Inc', '$1,890.00', 'info', 'Feb 3, 2024', '1 item: Premium License x1'),
        ('ORD-003', 'Wayne Ent.', '$12,400.00', 'success', 'Mar 12, 2024', '5 items: Server Unit x3, Cable x2'),
        ('ORD-004', 'Stark Ind.', '$8,750.00', 'warning', 'Apr 7, 2024', '2 items: Reactor Core x1, Shield x1'),
        ('ORD-005', 'Umbrella Co', '$3,200.00', 'danger', 'May 20, 2024', '4 items: Sample Kit x4'),
    ]
    for oid, cust, amt, status, date, details in orders:
        h += '<tr class="cursor-pointer" onclick="toggleExpand(this)">\n<td><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="expand-icon transition-transform"><path d="M9 18l6-6-6-6"/></svg></td>\n<td class="font-mono text-sm font-medium text-slate-700 dark:text-slate-300">' + esc(oid) + '</td>\n<td>' + esc(cust) + '</td>\n<td class="font-medium">' + esc(amt) + '</td>\n<td>' + status_badge(status.capitalize(), status) + '</td>\n<td class="text-slate-400">' + esc(date) + '</td>\n</tr>\n<tr class="expand-row" style="display:none"><td colspan="6" class="bg-slate-50 dark:bg-slate-800/50 px-8 py-4"><p class="text-sm text-slate-600 dark:text-slate-400">' + esc(details) + '</p></td></tr>\n'
    h += '</tbody></table></div></div>\n'

    # Inline Editable Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Inline Editable</h3><p class="text-sm text-slate-400 mt-1">Double-click a cell to edit</p></div>\n<div class="overflow-x-auto">\n<table class="data-table" id="edit-table">\n<thead><tr><th>Product</th><th>SKU</th><th>Price</th><th>Quantity</th><th>Actions</th></tr></thead>\n<tbody>\n'
    products = [
        ('Wireless Headphones', 'WH-001', '$89.99', '234'),
        ('USB-C Hub', 'UCH-015', '$49.99', '567'),
        ('Mechanical Keyboard', 'MK-008', '$129.99', '123'),
        ('4K Monitor', 'MON-022', '$449.99', '45'),
        ('Webcam HD', 'WC-003', '$69.99', '312'),
    ]
    for prod, sku, price, qty in products:
        h += '<tr>\n<td class="editable font-medium text-slate-700 dark:text-slate-300" ondblclick="makeEditable(this)">' + esc(prod) + '</td>\n<td class="editable font-mono text-sm" ondblclick="makeEditable(this)">' + esc(sku) + '</td>\n<td class="editable" ondblclick="makeEditable(this)">' + esc(price) + '</td>\n<td class="editable" ondblclick="makeEditable(this)">' + esc(qty) + '</td>\n<td><button type="button" class="text-xs text-indigo-500 hover:text-indigo-700 font-medium" onclick="showToast(\'Row saved!\',\'success\')">Save</button></td>\n</tr>\n'
    h += '</tbody></table></div></div>\n'

    # Loading State Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Loading State</h3></div>\n<div class="overflow-x-auto p-4">\n'
    for _ in range(5):
        h += '<div class="flex gap-4 mb-4"><div class="skeleton h-4 w-8"></div><div class="skeleton h-4 flex-1"></div><div class="skeleton h-4 w-24"></div><div class="skeleton h-4 w-20"></div><div class="skeleton h-4 w-16"></div></div>\n'
    h += '</div></div>\n'

    # Empty State Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 mb-6 fade-up">\n<div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Empty State</h3></div>\n<div class="empty-state py-12">\n<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>\n<h3 class="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-1">No data found</h3>\n<p class="text-sm text-slate-400 mb-4">There are no records to display yet</p>\n<button type="button" class="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Add record action\',\'info\')">Add Record</button>\n</div></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function toggleExpand(row){
  var next=row.nextElementSibling;
  var icon=row.querySelector('.expand-icon');
  if(next&&next.classList.contains('expand-row')){
    next.style.display=next.style.display==='none'?'table-row':'none';
    icon.style.transform=next.style.display==='table-row'?'rotate(90deg)':'';
  }
}
function makeEditable(cell){
  if(cell.querySelector('input'))return;
  var val=cell.textContent;
  var input=document.createElement('input');
  input.type='text';input.value=val;
  input.className='form-input py-1 px-2 text-sm';
  input.style.minWidth='60px';
  cell.textContent='';cell.appendChild(input);
  input.focus();
  input.addEventListener('blur',function(){cell.textContent=this.value||val});
  input.addEventListener('keydown',function(e){if(e.key==='Enter'){cell.textContent=this.value||val}if(e.key==='Escape'){cell.textContent=val}});
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Orders Table Page
# ============================================================
def gen_orders_table():
    title = 'Orders Table'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'E-commerce orders management with status tracking')

    # Stats
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    for label, val, change, dir in [('Total Orders', '1,284', '+8.4%', 'up'), ('Revenue', '$48,290', '+12.1%', 'up'), ('Pending', '23', '-5.2%', 'down'), ('Avg Order', '$37.61', '+3.8%', 'up')]:
        color = 'text-green-600' if dir == 'up' else 'text-red-500'
        arrow = '&#9650;' if dir == 'up' else '&#9660;'
        h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-4"><p class="text-xs text-slate-400 mb-1">' + label + '</p><p class="text-xl font-bold text-slate-900 dark:text-white">' + val + '</p><p class="text-xs ' + color + '">' + arrow + ' ' + change + '</p></div>\n'
    h += '</div>\n'

    # Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up">\n'
    h += '<div class="p-4 border-b border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">\n<div class="relative flex-1 max-w-xs"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><input type="text" class="form-input pl-9" placeholder="Search orders..." oninput="filterTable(this.value)"/></div>\n<div class="flex gap-2 flex-wrap"><button type="button" class="filter-chip active" onclick="filterByStatus(this,\'all\')">All</button><button type="button" class="filter-chip" onclick="filterByStatus(this,\'success\')">Completed</button><button type="button" class="filter-chip" onclick="filterByStatus(this,\'info\')">Processing</button><button type="button" class="filter-chip" onclick="filterByStatus(this,\'warning\')">Pending</button><button type="button" class="filter-chip" onclick="filterByStatus(this,\'danger\')">Cancelled</button></div>\n</div>\n'

    h += '<div class="overflow-x-auto">\n<table class="data-table" id="orders-table">\n<thead><tr><th class="w-10"><input type="checkbox" id="select-all" onchange="toggleSelectAll(this)"/></th><th class="sortable" onclick="sortTable(1)">Order ID <span class="sort-icon">&#8597;</span></th><th>Customer</th><th class="sortable" onclick="sortTable(3)">Amount <span class="sort-icon">&#8597;</span></th><th>Items</th><th>Status</th><th class="sortable" onclick="sortTable(6)">Date <span class="sort-icon">&#8597;</span></th><th class="w-10"></th></tr></thead>\n<tbody>\n'

    orders = [
        ('#ORD-7821', 'Sarah Johnson', '$245.00', '3 items', 'success', 'Jan 15, 2024'),
        ('#ORD-7822', 'Mike Peters', '$89.50', '1 item', 'info', 'Jan 16, 2024'),
        ('#ORD-7823', 'Emily Davis', '$412.00', '5 items', 'success', 'Jan 17, 2024'),
        ('#ORD-7824', 'Tom Wilson', '$67.90', '2 items', 'warning', 'Jan 18, 2024'),
        ('#ORD-7825', 'Lisa Anderson', '$156.00', '3 items', 'info', 'Jan 19, 2024'),
        ('#ORD-7826', 'James Brown', '$890.00', '8 items', 'success', 'Jan 20, 2024'),
        ('#ORD-7827', 'Anna Lee', '$34.99', '1 item', 'danger', 'Jan 21, 2024'),
        ('#ORD-7828', 'Robert Chen', '$267.50', '4 items', 'success', 'Jan 22, 2024'),
        ('#ORD-7829', 'Maria Garcia', '$178.00', '2 items', 'warning', 'Jan 23, 2024'),
        ('#ORD-7830', 'David Kim', '$523.00', '6 items', 'info', 'Jan 24, 2024'),
    ]

    for oid, cust, amt, items, status, date in orders:
        h += '<tr data-status="' + status + '"><td><input type="checkbox" class="row-check" onchange="updateBulkBar()"/></td><td class="font-mono text-sm font-medium text-slate-700 dark:text-slate-300">' + esc(oid) + '</td><td>' + esc(cust) + '</td><td class="font-medium">' + esc(amt) + '</td><td class="text-slate-400">' + esc(items) + '</td><td>' + status_badge(status.capitalize(), status) + '</td><td class="text-slate-400">' + esc(date) + '</td><td>' + action_dropdown() + '</td></tr>\n'

    h += '</tbody></table></div>\n'
    h += '<div class="p-4 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3"><p class="text-sm text-slate-400">Showing 1-10 of 1,284</p><div class="pagination"><button class="page-btn" disabled>&laquo;</button><button class="page-btn active">1</button><button class="page-btn">2</button><button class="page-btn">3</button><button class="page-btn">4</button><button class="page-btn">&raquo;</button></div></div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function filterTable(q){var rows=document.querySelectorAll('#orders-table tbody tr');q=q.toLowerCase();rows.forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'':'none'})}
function filterByStatus(btn,s){document.querySelectorAll('.filter-chip').forEach(function(c){c.classList.remove('active')});btn.classList.add('active');var rows=document.querySelectorAll('#orders-table tbody tr');rows.forEach(function(r){if(s==='all')r.style.display='';else r.style.display=r.dataset.status===s?'':'none'})}
function toggleSelectAll(cb){document.querySelectorAll('.row-check').forEach(function(c){c.checked=cb.checked});updateBulkBar()}
function updateBulkBar(){var n=document.querySelectorAll('.row-check:checked').length;var bar=document.getElementById('bulk-bar');if(bar){document.getElementById('bulk-count').textContent=n;bar.classList.toggle('visible',n>0)}}
function toggleActionMenu(btn){var m=btn.nextElementSibling;document.querySelectorAll('.action-menu').forEach(function(x){if(x!==m)x.style.display='none'});m.style.display=m.style.display==='none'?'block':'none'}
document.addEventListener('click',function(e){if(!e.target.closest('.action-menu')&&!e.target.closest('[onclick*="toggleActionMenu"]'))document.querySelectorAll('.action-menu').forEach(function(m){m.style.display='none'})});
var sortDir={};
function sortTable(c){var tb=document.querySelector('#orders-table tbody'),rows=Array.from(tb.querySelectorAll('tr'));sortDir[c]=!sortDir[c];rows.sort(function(a,b){var ta=a.cells[c].textContent.trim(),tb2=b.cells[c].textContent.trim();return sortDir[c]?ta.localeCompare(tb2):tb2.localeCompare(ta)});rows.forEach(function(r){tb.appendChild(r)})}
'''
    h += page_foot(js)
    return h

# ============================================================
# Logs Table Page
# ============================================================
def gen_logs_table():
    title = 'Activity Logs'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'System activity logs with severity levels and filtering')

    # Filters
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up">\n'
    h += '<div class="p-4 border-b border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">\n<div class="relative flex-1 max-w-xs"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><input type="text" class="form-input pl-9" placeholder="Search logs..." oninput="filterLogs(this.value)"/></div>\n<div class="flex gap-2 flex-wrap"><button type="button" class="filter-chip active" onclick="filterLevel(this,\'all\')">All</button><button type="button" class="filter-chip" onclick="filterLevel(this,\'info\')">Info</button><button type="button" class="filter-chip" onclick="filterLevel(this,\'warning\')">Warning</button><button type="button" class="filter-chip" onclick="filterLevel(this,\'danger\')">Error</button><button type="button" class="filter-chip" onclick="filterLevel(this,\'success\')">Success</button></div>\n</div>\n'

    h += '<div class="overflow-x-auto">\n<table class="data-table" id="logs-table">\n<thead><tr><th>Timestamp</th><th>Level</th><th>Service</th><th>Message</th><th>User</th></tr></thead>\n<tbody>\n'

    logs = [
        ('2024-01-15 09:23:41', 'info', 'Auth', 'User logged in successfully', 'alice@acme.com'),
        ('2024-01-15 09:24:12', 'success', 'Payment', 'Invoice #4521 paid - $245.00', 'billing@acme.com'),
        ('2024-01-15 09:25:03', 'warning', 'API', 'Rate limit approaching (80%)', 'system'),
        ('2024-01-15 09:26:18', 'info', 'Deploy', 'Build #1842 deployed to production', 'ci@acme.com'),
        ('2024-01-15 09:27:45', 'danger', 'Database', 'Connection pool exhausted - retrying', 'system'),
        ('2024-01-15 09:28:33', 'info', 'CDN', 'Cache purge completed for /assets/*', 'admin@acme.com'),
        ('2024-01-15 09:29:11', 'success', 'Backup', 'Daily backup completed - 2.4GB', 'system'),
        ('2024-01-15 09:30:22', 'warning', 'Storage', 'Disk usage at 85% - consider cleanup', 'system'),
        ('2024-01-15 09:31:05', 'info', 'Auth', 'Password reset requested', 'bob@acme.com'),
        ('2024-01-15 09:32:18', 'danger', 'Security', 'Failed login attempt (5th) from 192.168.1.42', 'system'),
        ('2024-01-15 09:33:44', 'info', 'Email', 'Batch email sent - 1,247 recipients', 'noreply@acme.com'),
        ('2024-01-15 09:34:56', 'success', 'Migration', 'Database migration v2.3 completed', 'dev@acme.com'),
        ('2024-01-15 09:35:23', 'warning', 'SSL', 'Certificate expires in 14 days', 'system'),
        ('2024-01-15 09:36:41', 'info', 'Webhook', 'Delivery to endpoint succeeded', 'api@acme.com'),
        ('2024-01-15 09:37:55', 'danger', 'Queue', 'Dead letter queue has 23 messages', 'system'),
    ]

    for ts, level, service, msg, user in logs:
        level_label = {'info': 'Info', 'success': 'Success', 'warning': 'Warning', 'danger': 'Error'}.get(level, level)
        h += '<tr data-level="' + level + '"><td class="font-mono text-xs text-slate-400 whitespace-nowrap">' + esc(ts) + '</td><td>' + status_badge(level_label, level) + '</td><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(service) + '</td><td class="text-sm text-slate-600 dark:text-slate-400 max-w-md truncate">' + esc(msg) + '</td><td class="text-xs text-slate-400">' + esc(user) + '</td></tr>\n'

    h += '</tbody></table></div>\n'
    h += '<div class="p-4 border-t border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3"><p class="text-sm text-slate-400">Showing 15 of 4,892 log entries</p><div class="pagination"><button class="page-btn" disabled>&laquo;</button><button class="page-btn active">1</button><button class="page-btn">2</button><button class="page-btn">3</button><button class="page-btn">4</button><button class="page-btn">&raquo;</button></div></div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function filterLogs(q){var rows=document.querySelectorAll('#logs-table tbody tr');q=q.toLowerCase();rows.forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'':'none'})}
function filterLevel(btn,level){document.querySelectorAll('.filter-chip').forEach(function(c){c.classList.remove('active')});btn.classList.add('active');var rows=document.querySelectorAll('#logs-table tbody tr');rows.forEach(function(r){if(level==='all')r.style.display='';else r.style.display=r.dataset.level===level?'':'none'})}
'''
    h += page_foot(js)
    return h

# Generate all table pages
pages = [
    ('103-tables-data.html', gen_data_table),
    ('104-tables-basic.html', gen_basic_table),
    ('105-tables-advanced.html', gen_advanced_table),
    ('106-tables-orders.html', gen_orders_table),
    ('109-tables-logs.html', gen_logs_table),
]

print('Generating premium table pages...')
for fname, gen_fn in pages:
    path = os.path.join(OUT, fname)
    html = gen_fn()
    with open(path, 'w') as f:
        f.write(html)
    sz = os.path.getsize(path)
    print('  ' + fname + ': ' + str(sz // 1024) + 'KB')

print('Done! All table pages generated.')
