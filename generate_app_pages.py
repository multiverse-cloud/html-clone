#!/usr/bin/env python3
"""Generate premium app pages: pricing, file manager, billing, API keys, integrations, settings, error pages, FAQ, blank."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def page_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en" class="scroll-smooth">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<meta name="theme-color" content="#465fff"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n.no-scrollbar::-webkit-scrollbar{display:none}\n.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@media(prefers-reduced-motion:reduce){.fade-up{animation:none}}\n' + extra_css + '\n</style>\n</head>\n'

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
    return breadcrumb('Home', title) + '<div class="mb-6 fade-up">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">' + esc(title) + '</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">' + esc(desc) + '</p>\n</div>\n'

def fullpage_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@media(prefers-reduced-motion:reduce){.fade-up{animation:none}}\n' + extra_css + '\n</style>\n</head>\n'

def fullpage_foot(extra_js=''):
    return '<script src="common-loader.js"></script>\n<script>\n' + extra_js + '\n</script>\n</body>\n</html>'

# ============================================================
# Pricing Page
# ============================================================
def gen_pricing():
    title = 'Pricing Plans'
    h = page_head(title, '\n.pricing-card{border:1px solid #e2e8f0;border-radius:1rem;padding:2rem;background:#fff;transition:transform .2s,box-shadow .2s}\n.pricing-card:hover{transform:translateY(-4px);box-shadow:0 12px 24px rgba(0,0,0,.08)}\n.dark .pricing-card{background:#1e293b;border-color:#334155}\n.pricing-card.featured{border-color:#6366f1;box-shadow:0 0 0 1px #6366f1}\n.pricing-card.featured:hover{box-shadow:0 12px 24px rgba(99,102,241,.15)}\n.pricing-badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:#6366f1;color:#fff;font-size:.75rem;font-weight:600;padding:.25rem 1rem;border-radius:9999px}\n.check-icon{color:#22c55e}\n.cross-icon{color:#e2e8f0}\n.dark .cross-icon{color:#334155}\n')
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Choose the perfect plan for your needs')

    # Toggle
    h += '<div class="flex items-center justify-center gap-3 mb-8 fade-up"><span class="text-sm font-medium text-slate-600 dark:text-slate-400" id="monthly-label">Monthly</span><label class="switch" style="width:3rem;height:1.625rem"><input type="checkbox" id="pricing-toggle" onchange="togglePricing(this)"/><span class="slider"></span></label><span class="text-sm font-medium text-slate-600 dark:text-slate-400" id="yearly-label">Yearly <span class="text-xs text-green-600 font-semibold">Save 20%</span></span></div>\n'

    # Cards
    h += '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto fade-up">\n'

    plans = [
        ('Starter', 0, 'Free forever', False, ['1 User', '5 Projects', '1GB Storage', 'Community Support', 'Basic Analytics']),
        ('Professional', 29, 'Best for growing teams', True, ['10 Users', '50 Projects', '25GB Storage', 'Priority Support', 'Advanced Analytics', 'API Access', 'Custom Integrations']),
        ('Enterprise', 99, 'For large organizations', False, ['Unlimited Users', 'Unlimited Projects', '500GB Storage', '24/7 Support', 'Custom Analytics', 'Full API Access', 'SSO & SAML', 'Dedicated Manager', 'SLA Guarantee']),
    ]

    for name, price_m, desc, featured, features in plans:
        price_y = int(price_m * 0.8) if price_m else 0
        featured_cls = ' featured' if featured else ''
        h += '<div class="pricing-card relative' + featured_cls + '">\n'
        if featured:
            h += '<div class="pricing-badge">Most Popular</div>\n'
        h += '<h3 class="text-lg font-bold text-slate-900 dark:text-white mb-1">' + esc(name) + '</h3>\n'
        h += '<p class="text-sm text-slate-400 mb-4">' + esc(desc) + '</p>\n'
        h += '<div class="mb-6"><span class="text-4xl font-bold text-slate-900 dark:text-white" data-monthly="$' + str(price_m) + '" data-yearly="$' + str(price_y) + '">$' + str(price_m) + '</span><span class="text-sm text-slate-400">/month</span></div>\n'
        h += '<ul class="space-y-3 mb-6">\n'
        for feat in features:
            h += '<li class="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></svg>' + esc(feat) + '</li>\n'
        h += '</ul>\n'
        btn_cls = 'bg-indigo-500 text-white hover:bg-indigo-600' if featured else 'bg-slate-100 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700'
        h += '<button type="button" class="w-full py-2.5 rounded-lg text-sm font-medium transition-colors ' + btn_cls + '" onclick="showToast(\'Selected ' + esc(name) + ' plan\',\'success\')">' + ('Get Started' if price_m == 0 else 'Subscribe') + '</button>\n'
        h += '</div>\n'

    h += '</div>\n'

    # FAQ
    h += '<div class="max-w-2xl mx-auto mt-12 fade-up"><h2 class="text-xl font-bold text-slate-900 dark:text-white mb-6 text-center">Frequently Asked Questions</h2>\n'
    faqs = [
        ('Can I change my plan later?', 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the start of your next billing cycle.'),
        ('What happens when my trial ends?', 'Your account will switch to the Free plan. No data is lost, but some features may become unavailable.'),
        ('Do you offer refunds?', 'Yes, we offer a 30-day money-back guarantee for all paid plans.'),
        ('Is there a discount for nonprofits?', 'Yes! We offer 50% off for verified nonprofit organizations. Contact our sales team for details.'),
    ]
    for q, a in faqs:
        h += '<div class="border border-slate-200 dark:border-slate-700 rounded-lg mb-3"><button type="button" class="w-full flex items-center justify-between p-4 text-sm font-medium text-slate-700 dark:text-slate-300 text-left" onclick="toggleFaq(this)">' + esc(q) + '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transition-transform"><path d="M6 9l6 6 6-6"/></svg></button><div class="px-4 pb-4 text-sm text-slate-500 dark:text-slate-400" style="display:none">' + esc(a) + '</div></div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function togglePricing(cb){
  var yearly=cb.checked;
  document.querySelectorAll('[data-monthly]').forEach(function(el){
    el.textContent=yearly?el.dataset.yearly:el.dataset.monthly;
  });
  document.getElementById('monthly-label').style.opacity=yearly?'0.5':'1';
  document.getElementById('yearly-label').style.opacity=yearly?'1':'0.5';
}
function toggleFaq(btn){
  var content=btn.nextElementSibling;
  var icon=btn.querySelector('svg');
  content.style.display=content.style.display==='none'?'block':'none';
  icon.style.transform=content.style.display==='block'?'rotate(180deg)':'';
}
'''
    h += page_foot(js)
    return h

# ============================================================
# File Manager Page
# ============================================================
def gen_file_manager():
    title = 'File Manager'
    h = page_head(title, '\n.file-item{display:flex;align-items:center;gap:.75rem;padding:.75rem 1rem;border:1px solid #e2e8f0;border-radius:.5rem;background:#fff;cursor:pointer;transition:background .15s,border-color .15s}\n.file-item:hover{background:#f8fafc;border-color:#cbd5e1}\n.dark .file-item{background:#1e293b;border-color:#334155}\n.dark .file-item:hover{background:#334155;border-color:#475569}\n.file-icon{width:40px;height:40px;border-radius:.5rem;display:flex;align-items:center;justify-content:center;font-size:1.25rem}\n.folder-icon{background:#fef3c7;color:#f59e0b}\n.file-pdf{background:#fef2f2;color:#ef4444}\n.file-doc{background:#dbeafe;color:#3b82f6}\n.file-img{background:#dcfce7;color:#22c55e}\n.file-xls{background:#dcfce7;color:#16a34a}\n.file-zip{background:#f3e8ff;color:#8b5cf6}\n.file-code{background:#eef2ff;color:#6366f1}\n')
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Manage your files and folders')

    # Stats
    h += '<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6 fade-up">\n'
    for label, val, sub in [('Total Files', '1,247', '12.4 GB used'), ('Folders', '86', '3 levels deep'), ('Shared', '234', 'With 12 users'), ('Recent', '18', 'Modified today')]:
        h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-4"><p class="text-xs text-slate-400 mb-1">' + label + '</p><p class="text-xl font-bold text-slate-900 dark:text-white">' + val + '</p><p class="text-xs text-slate-400">' + sub + '</p></div>\n'
    h += '</div>\n'

    # Toolbar
    h += '<div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between mb-6 fade-up">\n<div class="relative flex-1 max-w-xs"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="absolute left-3 top-1/2 -translate-y-1/2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><input type="text" class="form-input pl-9" placeholder="Search files..." oninput="searchFiles(this.value)"/></div>\n<div class="flex gap-2"><button type="button" class="px-3 py-1.5 text-xs font-medium bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Upload dialog would open\',\'info\')">Upload</button><button type="button" class="px-3 py-1.5 text-xs font-medium border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="showToast(\'New folder created\',\'success\')">New Folder</button></div>\n</div>\n'

    # Folders
    h += '<h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 fade-up">Folders</h3>\n<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-6 fade-up" id="folders-grid">\n'
    folders = [('Documents', 24), ('Images', 156), ('Videos', 12), ('Downloads', 89), ('Projects', 34), ('Archives', 18)]
    for name, count in folders:
        h += '<div class="file-item" onclick="showToast(\'Opening ' + esc(name) + '\',\'info\')"><div class="file-icon folder-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/></svg></div><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</p><p class="text-xs text-slate-400">' + str(count) + ' files</p></div></div>\n'
    h += '</div>\n'

    # Files
    h += '<h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3 fade-up">Recent Files</h3>\n<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up">\n<div class="overflow-x-auto"><table class="data-table"><thead><tr><th>Name</th><th>Size</th><th>Modified</th><th>Type</th><th></th></tr></thead><tbody id="files-table">\n'
    files = [
        ('Q4 Report.pdf', '2.4 MB', 'Jan 15, 2024', 'pdf'),
        ('Design System.fig', '18.2 MB', 'Jan 14, 2024', 'doc'),
        ('Screenshot.png', '856 KB', 'Jan 13, 2024', 'img'),
        ('Budget 2024.xlsx', '1.1 MB', 'Jan 12, 2024', 'xls'),
        ('Source Code.zip', '45.6 MB', 'Jan 11, 2024', 'zip'),
        ('index.html', '12 KB', 'Jan 10, 2024', 'code'),
        ('Presentation.pdf', '5.8 MB', 'Jan 9, 2024', 'pdf'),
        ('Logo.svg', '4 KB', 'Jan 8, 2024', 'img'),
    ]
    for name, size, modified, ftype in files:
        icon_cls = {'pdf': 'file-pdf', 'doc': 'file-doc', 'img': 'file-img', 'xls': 'file-xls', 'zip': 'file-zip', 'code': 'file-code'}.get(ftype, 'file-doc')
        ext = name.split('.')[-1].upper()
        h += '<tr><td><div class="flex items-center gap-3"><div class="file-icon ' + icon_cls + '" style="width:32px;height:32px;font-size:.625rem;font-weight:700">' + ext + '</div><span class="font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</span></div></td><td class="text-slate-400">' + esc(size) + '</td><td class="text-slate-400">' + esc(modified) + '</td><td><span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500">' + ext + '</span></td><td><button type="button" class="p-1 rounded hover:bg-slate-100 dark:hover:bg-slate-800" onclick="showToast(\'Download started\',\'success\')"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/></svg></button></td></tr>\n'
    h += '</tbody></table></div></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function searchFiles(q){q=q.toLowerCase();document.querySelectorAll('#files-table tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)>=0?'':'none'})}
'''
    h += page_foot(js)
    return h

# ============================================================
# Billing Page
# ============================================================
def gen_billing():
    title = 'Billing'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Manage your billing and subscription')

    # Current Plan
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 mb-6 fade-up">\n<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"><div><h3 class="text-lg font-semibold text-slate-900 dark:text-white">Professional Plan</h3><p class="text-sm text-slate-400">$29/month per user &middot; Billed monthly &middot; 10 users</p></div><div class="flex gap-2"><button type="button" class="px-4 py-2 text-sm font-medium border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="showToast(\'Plan change dialog\',\'info\')">Change Plan</button><button type="button" class="px-4 py-2 text-sm font-medium bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Upgrade dialog\',\'info\')">Upgrade</button></div></div>\n</div>\n'

    # Payment Method
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 mb-6 fade-up"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">Payment Method</h3><div class="flex items-center gap-4 p-4 border border-slate-200 dark:border-slate-700 rounded-lg"><div class="w-12 h-8 bg-indigo-100 dark:bg-indigo-900/30 rounded flex items-center justify-center text-xs font-bold text-indigo-600 dark:text-indigo-400">VISA</div><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">Visa ending in 4242</p><p class="text-xs text-slate-400">Expires 12/2026</p></div><button type="button" class="ml-auto text-sm text-indigo-500 hover:text-indigo-700 font-medium" onclick="showToast(\'Edit payment method\',\'info\')">Edit</button></div></div>\n'

    # Billing History
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up"><div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Billing History</h3></div><div class="overflow-x-auto"><table class="data-table"><thead><tr><th>Date</th><th>Description</th><th>Amount</th><th>Status</th><th>Invoice</th></tr></thead><tbody>\n'
    invoices = [
        ('Jan 1, 2024', 'Professional Plan - 10 users', '$290.00', 'success', 'INV-2024-001'),
        ('Dec 1, 2023', 'Professional Plan - 10 users', '$290.00', 'success', 'INV-2023-012'),
        ('Nov 1, 2023', 'Professional Plan - 8 users', '$232.00', 'success', 'INV-2023-011'),
        ('Oct 1, 2023', 'Professional Plan - 8 users', '$232.00', 'success', 'INV-2023-010'),
        ('Sep 1, 2023', 'Starter Plan - 3 users', '$0.00', 'neutral', 'INV-2023-009'),
    ]
    for date, desc, amt, status, inv in invoices:
        h += '<tr><td class="text-slate-400">' + esc(date) + '</td><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(desc) + '</td><td>' + esc(amt) + '</td><td><span class="status-badge status-' + status + '">' + ('Paid' if status == 'success' else 'Free') + '</span></td><td><a href="#" class="text-sm text-indigo-500 hover:text-indigo-700 font-medium" onclick="showToast(\'Download ' + esc(inv) + '\',\'success\');return false">' + esc(inv) + '</a></td></tr>\n'
    h += '</tbody></table></div></div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# API Keys Page
# ============================================================
def gen_api_keys():
    title = 'API Keys'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Manage your API keys and webhooks')

    # Create Key
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 mb-6 fade-up"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">Create New Key</h3><div class="grid grid-cols-1 sm:grid-cols-3 gap-4"><div class="form-group"><label class="form-label">Key Name</label><input type="text" class="form-input" placeholder="e.g. Production API" id="key-name"/></div><div class="form-group"><label class="form-label">Permissions</label><select class="form-input" id="key-perm"><option>Read Only</option><option>Read & Write</option><option>Full Access</option></select></div><div class="form-group flex items-end"><button type="button" class="w-full px-4 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="createApiKey()">Generate Key</button></div></div></div>\n'

    # Keys Table
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 fade-up"><div class="p-4 border-b border-slate-100 dark:border-slate-800"><h3 class="font-semibold text-slate-900 dark:text-white">Active Keys</h3></div><div class="overflow-x-auto"><table class="data-table"><thead><tr><th>Name</th><th>Key</th><th>Permissions</th><th>Created</th><th>Last Used</th><th>Status</th><th></th></tr></thead><tbody>\n'
    keys = [
        ('Production API', 'prod_key_xxx...xxx', 'Full Access', 'Jan 10, 2024', '2 hours ago', 'success'),
        ('Staging API', 'staging_key_xxx...xxx', 'Read & Write', 'Dec 5, 2023', '1 day ago', 'success'),
        ('Analytics Read', 'analytics_key_xxx...xxx', 'Read Only', 'Nov 20, 2023', '5 days ago', 'warning'),
        ('Legacy Key', 'sk_old_1234...5678', 'Full Access', 'Jun 1, 2023', '30 days ago', 'danger'),
    ]
    for name, key, perm, created, last_used, status in keys:
        status_text = {'success': 'Active', 'warning': 'Expiring', 'danger': 'Expired'}.get(status, status)
        h += '<tr><td class="font-medium text-slate-700 dark:text-slate-300">' + esc(name) + '</td><td class="font-mono text-xs text-slate-400">' + esc(key) + ' <button type="button" class="text-indigo-500 hover:text-indigo-700" onclick="copySourceCode(this.parentElement);showToast(\'Key copied!\',\'success\')">Copy</button></td><td class="text-slate-500">' + esc(perm) + '</td><td class="text-slate-400">' + esc(created) + '</td><td class="text-slate-400">' + esc(last_used) + '</td><td><span class="status-badge status-' + status + '">' + status_text + '</span></td><td><button type="button" class="text-xs text-red-500 hover:text-red-700 font-medium" onclick="showToast(\'Key revoked\',\'error\')">Revoke</button></td></tr>\n'
    h += '</tbody></table></div></div>\n'

    # Webhooks
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 mt-6 fade-up"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">Webhooks</h3><div class="space-y-3">\n'
    webhooks = [
        ('https://api.example.com/webhooks/payments', 'Payment Events', 'success'),
        ('https://api.example.com/webhooks/users', 'User Events', 'success'),
        ('https://api.example.com/webhooks/errors', 'Error Events', 'danger'),
    ]
    for url, events, status in webhooks:
        h += '<div class="flex items-center justify-between p-3 border border-slate-200 dark:border-slate-700 rounded-lg"><div><p class="text-sm font-mono text-slate-700 dark:text-slate-300">' + esc(url) + '</p><p class="text-xs text-slate-400">' + esc(events) + '</p></div><span class="status-badge status-' + status + '">' + ('Active' if status == 'success' else 'Failing') + '</span></div>\n'
    h += '</div><button type="button" class="mt-4 px-4 py-2 text-sm font-medium border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="showToast(\'Add webhook dialog\',\'info\')">Add Webhook</button></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function createApiKey(){
  var name=document.getElementById('key-name').value.trim();
  if(!name){showToast('Please enter a key name','error');return}
  var perm=document.getElementById('key-perm').value;
  showToast('API key "'+name+'" created with '+perm+' permissions','success');
  document.getElementById('key-name').value='';
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Integrations Page
# ============================================================
def gen_integrations():
    title = 'Integrations'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Connect your favorite tools and services')

    h += '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 fade-up">\n'
    integrations = [
        ('Slack', 'Get notifications in your Slack channels', True, '#4A154B'),
        ('GitHub', 'Sync issues and pull requests', True, '#333'),
        ('Jira', 'Link tickets and track progress', False, '#0052CC'),
        ('Figma', 'Import designs and prototypes', True, '#F24E1E'),
        ('Notion', 'Sync docs and databases', False, '#000'),
        ('Zapier', 'Automate workflows with 5000+ apps', False, '#FF4A00'),
        ('Google Drive', 'Access and share files', True, '#4285F4'),
        ('Salesforce', 'Sync CRM data', False, '#00A1E0'),
        ('Stripe', 'Process payments automatically', True, '#635BFF'),
    ]
    for name, desc, connected, color in integrations:
        h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-5 transition-shadow hover:shadow-md">\n'
        h += '<div class="flex items-center gap-3 mb-3"><div class="w-10 h-10 rounded-lg flex items-center justify-center text-white text-sm font-bold" style="background:' + color + '">' + name[0] + '</div><div><h4 class="text-sm font-semibold text-slate-900 dark:text-white">' + esc(name) + '</h4><p class="text-xs text-slate-400">' + esc(desc) + '</p></div></div>\n'
        if connected:
            h += '<div class="flex items-center justify-between"><span class="status-badge status-success">Connected</span><button type="button" class="text-xs text-red-500 hover:text-red-700 font-medium" onclick="showToast(\'' + esc(name) + ' disconnected\',\'error\')">Disconnect</button></div>\n'
        else:
            h += '<button type="button" class="w-full py-2 text-sm font-medium border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="showToast(\'' + esc(name) + ' connected!\',\'success\')">Connect</button>\n'
        h += '</div>\n'
    h += '</div>\n'

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Settings General Page
# ============================================================
def gen_settings():
    title = 'General Settings'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Configure your application preferences')

    # Tabs
    h += '<div class="flex gap-1 mb-6 border-b border-slate-200 dark:border-slate-700 fade-up"><button class="px-4 py-2.5 text-sm font-medium text-indigo-600 border-b-2 border-indigo-600" onclick="switchSettingsTab(this,0)">General</button><button class="px-4 py-2.5 text-sm font-medium text-slate-400 hover:text-slate-600" onclick="switchSettingsTab(this,1)">Notifications</button><button class="px-4 py-2.5 text-sm font-medium text-slate-400 hover:text-slate-600" onclick="switchSettingsTab(this,2)">Security</button><button class="px-4 py-2.5 text-sm font-medium text-slate-400 hover:text-slate-600" onclick="switchSettingsTab(this,3)">Advanced</button></div>\n'

    # General Tab
    h += '<div class="settings-tab fade-up" id="settings-tab-0">\n'
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6 mb-6"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">Application</h3>\n'
    h += '<div class="form-group"><label class="form-label">Application Name</label><input type="text" class="form-input" value="My Dashboard"/></div>\n'
    h += '<div class="form-group"><label class="form-label">Logo</label><div class="flex items-center gap-4"><div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg flex items-center justify-center text-indigo-600 font-bold">M</div><button type="button" class="text-sm text-indigo-500 hover:text-indigo-700 font-medium" onclick="showToast(\'Upload dialog\',\'info\')">Change Logo</button></div></div>\n'
    h += '<div class="grid grid-cols-2 gap-4"><div class="form-group"><label class="form-label">Timezone</label><select class="form-input"><option>UTC</option><option>America/New_York</option><option>Europe/London</option><option>Asia/Tokyo</option></select></div><div class="form-group"><label class="form-label">Language</label><select class="form-input"><option>English</option><option>Spanish</option><option>French</option></select></div></div>\n'
    h += '<div class="form-group"><label class="form-label">Date Format</label><select class="form-input"><option>MM/DD/YYYY</option><option>DD/MM/YYYY</option><option>YYYY-MM-DD</option></select></div>\n'
    h += '</div>\n'

    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">Appearance</h3>\n'
    h += '<div class="form-group"><label class="form-label">Theme</label><div class="flex gap-3"><button type="button" class="px-4 py-2 text-sm border-2 border-indigo-500 rounded-lg bg-white dark:bg-slate-900 font-medium" onclick="showToast(\'Light theme\',\'info\')">Light</button><button type="button" class="px-4 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800" onclick="showToast(\'Dark theme\',\'info\')">Dark</button><button type="button" class="px-4 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800" onclick="showToast(\'System theme\',\'info\')">System</button></div></div>\n'
    h += '<div class="form-group"><label class="form-label">Sidebar Position</label><div class="flex gap-3"><button type="button" class="px-4 py-2 text-sm border-2 border-indigo-500 rounded-lg font-medium">Left</button><button type="button" class="px-4 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800">Right</button></div></div>\n'
    h += '<div class="flex items-center justify-between py-3"><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">Compact Mode</p><p class="text-xs text-slate-400">Reduce spacing and padding</p></div><label class="switch"><input type="checkbox"/><span class="slider"></span></label></div>\n'
    h += '</div>\n'
    h += '<div class="flex justify-end mt-6"><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Settings saved!\',\'success\')">Save Changes</button></div>\n'
    h += '</div>\n'

    # Other tabs (hidden)
    for i in range(1, 4):
        tab_names = {1: 'Notifications', 2: 'Security', 3: 'Advanced'}
        h += '<div class="settings-tab" id="settings-tab-' + str(i) + '" style="display:none"><div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-6"><h3 class="font-semibold text-slate-900 dark:text-white mb-4">' + tab_names[i] + '</h3><p class="text-sm text-slate-400">Settings for ' + tab_names[i].lower() + ' will appear here.</p></div></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function switchSettingsTab(btn,n){
  document.querySelectorAll('.settings-tab').forEach(function(t){t.style.display='none'});
  document.getElementById('settings-tab-'+n).style.display='block';
  btn.parentElement.querySelectorAll('button').forEach(function(b){b.className='px-4 py-2.5 text-sm font-medium text-slate-400 hover:text-slate-600'});
  btn.className='px-4 py-2.5 text-sm font-medium text-indigo-600 border-b-2 border-indigo-600';
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Error Pages (full-page, no sidebar)
# ============================================================
def gen_error_404():
    h = fullpage_head('404 - Page Not Found')
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="min-h-screen flex items-center justify-center p-6">\n<div class="text-center fade-up">\n'
    h += '<div class="mb-6"><svg width="120" height="120" viewBox="0 0 120 120" fill="none" class="mx-auto"><circle cx="60" cy="60" r="50" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/><text x="60" y="68" text-anchor="middle" font-size="32" font-weight="700" fill="#6366f1">404</text></svg></div>\n'
    h += '<h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Page Not Found</h1>\n<p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">The page you are looking for might have been removed, had its name changed, or is temporarily unavailable.</p>\n'
    h += '<div class="flex gap-3 justify-center"><a href="01-main-dashboard.html" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Back to Dashboard</a><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="showToast(\'Report sent\',\'success\')">Report Issue</button></div>\n'
    h += '</div>\n</div>\n'
    h += fullpage_foot()
    return h

def gen_error_500():
    h = fullpage_head('500 - Server Error')
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="min-h-screen flex items-center justify-center p-6">\n<div class="text-center fade-up">\n'
    h += '<div class="mb-6"><svg width="120" height="120" viewBox="0 0 120 120" fill="none" class="mx-auto"><circle cx="60" cy="60" r="50" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/><path d="M40 80L80 40M40 40L80 80" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/></svg></div>\n'
    h += '<h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Internal Server Error</h1>\n<p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">Something went wrong on our end. Our team has been notified and is working on a fix.</p>\n'
    h += '<div class="flex gap-3 justify-center"><a href="01-main-dashboard.html" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Back to Dashboard</a><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="location.reload()">Try Again</button></div>\n'
    h += '</div>\n</div>\n'
    h += fullpage_foot()
    return h

def gen_maintenance():
    h = fullpage_head('Under Maintenance')
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="min-h-screen flex items-center justify-center p-6">\n<div class="text-center fade-up">\n'
    h += '<div class="mb-6"><svg width="120" height="120" viewBox="0 0 120 120" fill="none" class="mx-auto"><circle cx="60" cy="60" r="50" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/><path d="M50 45v20M70 45v20M45 80h30" stroke="#f59e0b" stroke-width="4" stroke-linecap="round"/></svg></div>\n'
    h += '<h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Under Maintenance</h1>\n<p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">We are performing scheduled maintenance to improve your experience. We will be back shortly.</p>\n'
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-4 max-w-sm mx-auto mb-6"><p class="text-sm text-slate-600 dark:text-slate-400">Estimated downtime</p><p class="text-lg font-bold text-slate-900 dark:text-white">~2 hours</p><p class="text-xs text-slate-400">Started at 10:00 AM UTC</p></div>\n'
    h += '<a href="01-main-dashboard.html" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors inline-block">Check Status</a>\n'
    h += '</div>\n</div>\n'
    h += fullpage_foot()
    return h

def gen_coming_soon():
    h = fullpage_head('Coming Soon')
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="min-h-screen flex items-center justify-center p-6">\n<div class="text-center fade-up">\n'
    h += '<div class="mb-6"><svg width="120" height="120" viewBox="0 0 120 120" fill="none" class="mx-auto"><circle cx="60" cy="60" r="50" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/><path d="M60 35v25l15 10" stroke="#6366f1" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n'
    h += '<h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Coming Soon</h1>\n<p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">We are working on something exciting. Stay tuned for our launch!</p>\n'
    # Countdown
    h += '<div class="flex gap-4 justify-center mb-8" id="countdown"><div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-3 w-16"><p class="text-2xl font-bold text-slate-900 dark:text-white" id="cd-days">14</p><p class="text-xs text-slate-400">Days</p></div><div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-3 w-16"><p class="text-2xl font-bold text-slate-900 dark:text-white" id="cd-hours">08</p><p class="text-xs text-slate-400">Hours</p></div><div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-3 w-16"><p class="text-2xl font-bold text-slate-900 dark:text-white" id="cd-mins">42</p><p class="text-xs text-slate-400">Mins</p></div><div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-3 w-16"><p class="text-2xl font-bold text-slate-900 dark:text-white" id="cd-secs">15</p><p class="text-xs text-slate-400">Secs</p></div></div>\n'
    # Email signup
    h += '<form class="flex gap-2 max-w-sm mx-auto" onsubmit="event.preventDefault();showToast(\'You will be notified!\',\'success\')"><input type="email" class="form-input flex-1" placeholder="Enter your email"/><button type="submit" class="px-4 py-2 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors whitespace-nowrap">Notify Me</button></form>\n'
    h += '</div>\n</div>\n'
    js = '''
var target=new Date();target.setDate(target.getDate()+14);
function updateCountdown(){
  var now=new Date(),diff=target-now;
  if(diff<=0)return;
  var d=Math.floor(diff/86400000),h=Math.floor((diff%86400000)/3600000),m=Math.floor((diff%3600000)/60000),s=Math.floor((diff%60000)/1000);
  document.getElementById('cd-days').textContent=d;
  document.getElementById('cd-hours').textContent=String(h).padStart(2,'0');
  document.getElementById('cd-mins').textContent=String(m).padStart(2,'0');
  document.getElementById('cd-secs').textContent=String(s).padStart(2,'0');
}
setInterval(updateCountdown,1000);updateCountdown();
'''
    h += fullpage_foot(js)
    return h

def gen_success_page():
    h = fullpage_head('Success')
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="min-h-screen flex items-center justify-center p-6">\n<div class="text-center fade-up">\n'
    h += '<div class="mb-6"><svg width="120" height="120" viewBox="0 0 120 120" fill="none" class="mx-auto"><circle cx="60" cy="60" r="50" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/><path d="M40 60l12 12 28-28" stroke="#22c55e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n'
    h += '<h1 class="text-3xl font-bold text-slate-900 dark:text-white mb-2">Success!</h1>\n<p class="text-slate-500 dark:text-slate-400 mb-6 max-w-md mx-auto">Your action has been completed successfully. You can now proceed to your dashboard.</p>\n'
    h += '<div class="flex gap-3 justify-center"><a href="01-main-dashboard.html" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Go to Dashboard</a></div>\n'
    h += '</div>\n</div>\n'
    h += fullpage_foot()
    return h

# ============================================================
# FAQ Page
# ============================================================
def gen_faq():
    title = 'FAQ'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Frequently asked questions and answers')

    # Search
    h += '<div class="max-w-2xl mx-auto mb-8 fade-up"><div class="relative"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" class="absolute left-4 top-1/2 -translate-y-1/2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><input type="text" class="form-input pl-12 py-3 text-base" placeholder="Search questions..." oninput="searchFaq(this.value)"/></div></div>\n'

    # Categories
    categories = [
        ('Getting Started', [
            ('How do I create an account?', 'Visit our sign-up page and fill in your details. You will receive a verification email to confirm your account.'),
            ('What are the system requirements?', 'Our platform works in all modern browsers (Chrome, Firefox, Safari, Edge). No installation required.'),
            ('How do I set up my profile?', 'After signing in, go to Settings > Profile to update your personal information, avatar, and preferences.'),
        ]),
        ('Billing & Plans', [
            ('What payment methods do you accept?', 'We accept all major credit cards (Visa, Mastercard, Amex), PayPal, and bank transfers for annual plans.'),
            ('Can I change my plan anytime?', 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect at the next billing cycle.'),
            ('Do you offer refunds?', 'We offer a 30-day money-back guarantee on all paid plans. Contact support for assistance.'),
        ]),
        ('Features & Usage', [
            ('How many users can I add?', 'The number of users depends on your plan: Starter (1), Professional (10), Enterprise (unlimited).'),
            ('Can I export my data?', 'Yes, you can export all your data in CSV, JSON, or PDF format from Settings > Data Export.'),
            ('Is there an API available?', 'Yes, our REST API is available on Professional and Enterprise plans with comprehensive documentation.'),
        ]),
        ('Security & Privacy', [
            ('Is my data encrypted?', 'Yes, all data is encrypted at rest (AES-256) and in transit (TLS 1.3). We follow industry best practices.'),
            ('Do you support 2FA?', 'Yes, we support TOTP-based two-factor authentication via apps like Google Authenticator or Authy.'),
            ('Where is my data stored?', 'Data is stored in SOC 2 Type II certified data centers in the US and EU. You can choose your region.'),
        ]),
    ]

    for cat_name, questions in categories:
        h += '<div class="max-w-2xl mx-auto mb-6 fade-up"><h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-3">' + esc(cat_name) + '</h2>\n'
        for q, a in questions:
            h += '<div class="faq-item border border-slate-200 dark:border-slate-700 rounded-lg mb-2"><button type="button" class="w-full flex items-center justify-between p-4 text-sm font-medium text-slate-700 dark:text-slate-300 text-left" onclick="toggleFaq(this)">' + esc(q) + '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transition-transform flex-shrink-0"><path d="M6 9l6 6 6-6"/></svg></button><div class="px-4 pb-4 text-sm text-slate-500 dark:text-slate-400" style="display:none">' + esc(a) + '</div></div>\n'
        h += '</div>\n'

    # Contact
    h += '<div class="max-w-2xl mx-auto mt-8 text-center fade-up"><p class="text-sm text-slate-400 mb-3">Still have questions?</p><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Contact support dialog\',\'info\')">Contact Support</button></div>\n'

    h += '</main>\n</div>\n</div>\n'

    js = '''
function toggleFaq(btn){
  var content=btn.nextElementSibling;
  var icon=btn.querySelector('svg');
  content.style.display=content.style.display==='none'?'block':'none';
  icon.style.transform=content.style.display==='block'?'rotate(180deg)':'';
}
function searchFaq(q){
  q=q.toLowerCase();
  document.querySelectorAll('.faq-item').forEach(function(item){
    item.style.display=item.textContent.toLowerCase().indexOf(q)>=0?'':'none';
  });
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Blank Page
# ============================================================
def gen_blank():
    title = 'Blank Page'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Start building your page from here')
    h += '<div class="bg-white dark:bg-slate-900 rounded-lg border border-slate-200 dark:border-slate-800 p-12 text-center fade-up">\n<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" class="mx-auto mb-4"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 8v8M8 12h8"/></svg>\n<h3 class="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-2">This is a blank page</h3>\n<p class="text-sm text-slate-400 max-w-md mx-auto">Use this as a starting point for your custom pages. Add components, forms, tables, or any content you need.</p>\n</div>\n'
    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# Generate all app pages
pages = [
    ('27-cards-pricing.html', gen_pricing),
    ('36-file-manager.html', gen_file_manager),
    ('51-settings-billing.html', gen_billing),
    ('21-api-keys.html', gen_api_keys),
    ('52-settings-integrations.html', gen_integrations),
    ('49-settings-general.html', gen_settings),
    ('88-error-404.html', gen_error_404),
    ('89-error-500.html', gen_error_500),
    ('90-error-maintenance.html', gen_maintenance),
    ('91-error-coming-soon.html', gen_coming_soon),
    ('92-success-page.html', gen_success_page),
    ('118-faq.html', gen_faq),
    ('119-blank-page.html', gen_blank),
]

print('Generating premium app pages...')
for fname, gen_fn in pages:
    path = os.path.join(OUT, fname)
    html = gen_fn()
    with open(path, 'w') as f:
        f.write(html)
    sz = os.path.getsize(path)
    print('  ' + fname + ': ' + str(sz // 1024) + 'KB')

print('Done! All app pages generated.')
