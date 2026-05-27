#!/usr/bin/env python3
"""Generate premium form pages with 50+ field/control examples."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def attr_esc(s):
    return s.replace('\\','\\\\').replace("'","\\'").replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def page_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en" class="scroll-smooth">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<meta name="theme-color" content="#465fff"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n.no-scrollbar::-webkit-scrollbar{display:none}\n.no-scrollbar{-ms-overflow-style:none;scrollbar-width:none}\n@keyframes slideDown{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}\n.animate-slideDown{animation:slideDown .2s ease-out}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@media(prefers-reduced-motion:reduce){.fade-up,.animate-slideDown{animation:none}}\n.component-item{border:1px solid #e2e8f0;border-radius:.75rem;padding:1.5rem;margin-bottom:1.5rem;background:#fff;transition:box-shadow .2s}\n.component-item:hover{box-shadow:0 4px 12px rgba(0,0,0,.06)}\n.dark .component-item{background:#1e293b;border-color:#334155}\n.component-item h3{font-size:1rem;font-weight:600;margin-bottom:.75rem;color:#0f172a}\n.dark .component-item h3{color:#e2e8f0}\n.form-group{margin-bottom:1.25rem}\n.form-label{display:block;margin-bottom:.375rem;font-size:.875rem;font-weight:500;color:#334155}\n.dark .form-label{color:#cbd5e1}\n.form-input{width:100%;padding:.625rem .875rem;border:1.5px solid #e2e8f0;border-radius:.5rem;font-size:.875rem;transition:border-color .15s,box-shadow .15s;background:#fff;color:#0f172a}\n.form-input:focus{outline:none;border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.12)}\n.dark .form-input{background:#0f172a;border-color:#334155;color:#e2e8f0}\n.dark .form-input:focus{border-color:#818cf8;box-shadow:0 0 0 3px rgba(129,140,248,.15)}\n.form-input.error{border-color:#ef4444}\n.form-input.success{border-color:#22c55e}\n.form-input:disabled{opacity:.5;cursor:not-allowed;background:#f1f5f9}\n.dark .form-input:disabled{background:#1e293b}\n.form-error{font-size:.75rem;color:#ef4444;margin-top:.25rem}\n.form-hint{font-size:.75rem;color:#94a3b8;margin-top:.25rem}\n.form-success{font-size:.75rem;color:#22c55e;margin-top:.25rem}\n.password-wrapper{position:relative}\n.password-toggle{position:absolute;right:.75rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:#94a3b8;padding:.25rem}\n.password-toggle:hover{color:#64748b}\ntextarea.form-input{min-height:100px;resize:vertical}\nselect.form-input{appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'12\' height=\'12\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'%2394a3b8\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpath d=\'M6 9l6 6 6-6\'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right .75rem center;padding-right:2.5rem}\n.checkbox-wrapper{display:flex;align-items:center;gap:.5rem}\n.checkbox-wrapper input[type=checkbox]{width:1rem;height:1rem;accent-color:#6366f1;cursor:pointer}\n.radio-wrapper{display:flex;align-items:center;gap:.5rem}\n.radio-wrapper input[type=radio]{width:1rem;height:1rem;accent-color:#6366f1;cursor:pointer}\n.switch{position:relative;width:2.75rem;height:1.5rem}\n.switch input{opacity:0;width:0;height:0}\n.switch .slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background:#cbd5e1;border-radius:1rem;transition:background .2s}\n.switch .slider::before{content:"";position:absolute;height:1.125rem;width:1.125rem;left:.1875rem;bottom:.1875rem;background:#fff;border-radius:50%;transition:transform .2s}\n.switch input:checked+.slider{background:#6366f1}\n.switch input:checked+.slider::before{transform:translateX(1.25rem)}\n.dark .switch .slider{background:#475569}\n.strength-bar{height:4px;border-radius:2px;background:#e2e8f0;margin-top:.5rem;overflow:hidden}\n.strength-bar .fill{height:100%;border-radius:2px;transition:width .3s,background .3s}\n.dark .strength-bar{background:#334155}\n.input-group{display:flex}\n.input-group .form-input{border-radius:0}\n.input-group .form-input:first-child{border-radius:.5rem 0 0 .5rem}\n.input-group .form-input:last-child{border-radius:0 .5rem .5rem 0}\n.input-group-addon{display:flex;align-items:center;padding:0 .875rem;border:1.5px solid #e2e8f0;background:#f8fafc;font-size:.875rem;color:#64748b;white-space:nowrap}\n.dark .input-group-addon{background:#1e293b;border-color:#334155;color:#94a3b8}\n.input-group-addon:first-child{border-radius:.5rem 0 0 .5rem;border-right:none}\n.input-group-addon:last-child{border-radius:0 .5rem .5rem 0;border-left:none}\n.file-drop{border:2px dashed #e2e8f0;border-radius:.5rem;padding:2rem;text-align:center;cursor:pointer;transition:border-color .2s,background .2s}\n.file-drop:hover{border-color:#6366f1;background:#f8fafc}\n.dark .file-drop{border-color:#334155}\n.dark .file-drop:hover{border-color:#818cf8;background:#1e293b}\n.range-input{-webkit-appearance:none;width:100%;height:6px;border-radius:3px;background:#e2e8f0;outline:none}\n.range-input::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#6366f1;cursor:pointer}\n.dark .range-input{background:#334155}\n.color-swatch{width:2.5rem;height:2.5rem;border-radius:.5rem;border:2px solid #e2e8f0;cursor:pointer}\n.dark .color-swatch{border-color:#334155}\n.wizard-step{display:none}\n.wizard-step.active{display:block}\n.wizard-progress{display:flex;gap:.5rem;margin-bottom:2rem}\n.wizard-progress .step{flex:1;height:4px;border-radius:2px;background:#e2e8f0;transition:background .3s}\n.wizard-progress .step.done{background:#6366f1}\n.wizard-progress .step.current{background:#818cf8}\n.dark .wizard-progress .step{background:#334155}\n' + extra_css + '\n</style>\n</head>\n'

def page_foot(extra_js=''):
    return '<script src="common-loader.js"></script>\n<script src="common-sidebar.js"></script>\n<script src="common-header.js"></script>\n<script src="app-shell.js"></script>\n<script>\n' + extra_js + '\n</script>\n</body>\n</html>'

def sidebar_header():
    return '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n<div class="sidebar-overlay fixed inset-0 bg-black/40 z-40 hidden lg:hidden"></div>\n<div class="flex h-screen overflow-hidden">\n<div class="sidebar-container w-72 flex-shrink-0"></div>\n<div class="header-container flex-1 flex flex-col overflow-hidden"></div>\n'

def breadcrumb(*parts):
    h = '<nav class="flex items-center gap-2 text-sm text-slate-400 mb-4">\n'
    for i, p in enumerate(parts):
        if i < len(parts) - 1:
            h += '<a href="#" class="hover:text-slate-600 dark:hover:text-slate-300">' + esc(p) + '</a>\n<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>\n'
        else:
            h += '<span class="text-slate-700 dark:text-slate-200 font-medium">' + esc(p) + '</span>\n'
    h += '</nav>\n'
    return h

def page_header(title, desc):
    return breadcrumb('Home', 'Forms', title) + '<div class="mb-6 fade-up">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">' + esc(title) + '</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">' + esc(desc) + '</p>\n</div>\n'

def section(title, desc=''):
    h = '<div class="component-item fade-up">\n<h3>' + esc(title) + '</h3>\n'
    if desc:
        h += '<p class="text-sm text-slate-500 dark:text-slate-400 mb-4">' + esc(desc) + '</p>\n'
    return h

def end_section():
    return '</div>\n'

def field_group(label, input_html, hint='', error='', success=''):
    h = '<div class="form-group">\n'
    h += '<label class="form-label">' + esc(label) + '</label>\n'
    h += input_html + '\n'
    if hint:
        h += '<p class="form-hint">' + esc(hint) + '</p>\n'
    if error:
        h += '<p class="form-error">' + esc(error) + '</p>\n'
    if success:
        h += '<p class="form-success">' + esc(success) + '</p>\n'
    h += '</div>\n'
    return h

# ============================================================
# Basic Forms Page
# ============================================================
def gen_basic_forms():
    title = 'Basic Forms'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Complete collection of form inputs, controls, and layouts')

    # Text Inputs
    h += section('Text Inputs', 'Standard text input variations')
    h += field_group('Default Input', '<input type="text" class="form-input" placeholder="Enter text..."/>')
    h += field_group('With Value', '<input type="text" class="form-input" value="John Doe"/>')
    h += field_group('Disabled Input', '<input type="text" class="form-input" placeholder="Disabled input" disabled/>')
    h += field_group('Read Only', '<input type="text" class="form-input" value="Read only value" readonly/>')
    h += field_group('With Placeholder', '<input type="text" class="form-input" placeholder="Search products..."/>')
    h += field_group('With Hint', '<input type="text" class="form-input" placeholder="Enter username"/>', 'Must be 3-20 characters, alphanumeric')
    h += field_group('Error State', '<input type="text" class="form-input error" value="invalid@"/>', '', 'Please enter a valid format')
    h += field_group('Success State', '<input type="text" class="form-input success" value="john@example.com"/>', '', '', 'Email is valid')
    h += field_group('Small Input', '<input type="text" class="form-input py-1.5 text-xs" placeholder="Small size"/>')
    h += field_group('Large Input', '<input type="text" class="form-input py-3 text-base" placeholder="Large size"/>')
    h += end_section()

    # Email & URL
    h += section('Email & URL Inputs')
    h += field_group('Email', '<input type="email" class="form-input" placeholder="you@example.com"/>')
    h += field_group('URL', '<input type="url" class="form-input" placeholder="https://example.com"/>')
    h += field_group('Tel', '<input type="tel" class="form-input" placeholder="+1 (555) 000-0000"/>')
    h += end_section()

    # Number Inputs
    h += section('Number Inputs')
    h += field_group('Number', '<input type="number" class="form-input" placeholder="0" min="0" max="100"/>')
    h += field_group('With Step', '<input type="number" class="form-input" placeholder="0.00" step="0.01" min="0"/>')
    h += field_group('Quantity', '<input type="number" class="form-input" value="1" min="1" max="99"/>')
    h += end_section()

    # Date & Time
    h += section('Date & Time Inputs')
    h += field_group('Date', '<input type="date" class="form-input"/>')
    h += field_group('Time', '<input type="time" class="form-input"/>')
    h += field_group('Datetime Local', '<input type="datetime-local" class="form-input"/>')
    h += field_group('Month', '<input type="month" class="form-input"/>')
    h += field_group('Week', '<input type="week" class="form-input"/>')
    h += end_section()

    # Textarea
    h += section('Textarea Controls')
    h += field_group('Default Textarea', '<textarea class="form-input" placeholder="Write your message..."></textarea>')
    h += field_group('With Rows', '<textarea class="form-input" rows="6" placeholder="Detailed description..."></textarea>')
    h += field_group('Disabled Textarea', '<textarea class="form-input" placeholder="Disabled" disabled></textarea>')
    h += field_group('Character Count', '<textarea class="form-input" rows="3" placeholder="Max 200 characters" maxlength="200" oninput="document.getElementById(\'char-count\').textContent=this.value.length+\'/200\'"></textarea><p class="form-hint" id="char-count">0/200</p>')
    h += end_section()

    # Select
    h += section('Select Dropdowns')
    h += field_group('Default Select', '<select class="form-input"><option value="">Select an option</option><option>Option 1</option><option>Option 2</option><option>Option 3</option></select>')
    h += field_group('With Optgroups', '<select class="form-input"><option value="">Select a country</option><optgroup label="North America"><option>United States</option><option>Canada</option><option>Mexico</option></optgroup><optgroup label="Europe"><option>United Kingdom</option><option>Germany</option><option>France</option></optgroup><optgroup label="Asia"><option>Japan</option><option>China</option><option>India</option></optgroup></select>')
    h += field_group('Disabled Select', '<select class="form-input" disabled><option>Disabled select</option></select>')
    h += field_group('Multiple Select', '<select class="form-input" multiple size="4"><option>React</option><option>Vue</option><option>Angular</option><option>Svelte</option><option>Next.js</option></select>', 'Hold Ctrl/Cmd to select multiple')
    h += end_section()

    # Checkboxes
    h += section('Checkboxes')
    checks = ['Remember me', 'Send notifications', 'Accept terms', 'Subscribe to newsletter', 'Mark as important']
    for c in checks:
        h += '<div class="checkbox-wrapper mb-2"><input type="checkbox" id="chk-' + c.replace(' ','-').lower() + '"/><label for="chk-' + c.replace(' ','-').lower() + '" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">' + c + '</label></div>\n'
    h += '<div class="checkbox-wrapper mb-2"><input type="checkbox" id="chk-disabled" disabled/><label for="chk-disabled" class="text-sm text-slate-400 dark:text-slate-500 cursor-not-allowed">Disabled checkbox</label></div>\n'
    h += '<div class="checkbox-wrapper mb-2"><input type="checkbox" id="chk-checked-disabled" checked disabled/><label for="chk-checked-disabled" class="text-sm text-slate-400 dark:text-slate-500 cursor-not-allowed">Checked & disabled</label></div>\n'
    h += end_section()

    # Radios
    h += section('Radio Buttons')
    radios = [('Small', 'size'), ('Medium', 'size'), ('Large', 'size'), ('Extra Large', 'size')]
    for label, name in radios:
        h += '<div class="radio-wrapper mb-2"><input type="radio" id="rad-' + label.replace(' ','-').lower() + '" name="' + name + '" value="' + label.replace(' ','-').lower() + '"/><label for="rad-' + label.replace(' ','-').lower() + '" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">' + label + '</label></div>\n'
    h += '<div class="radio-wrapper mb-2"><input type="radio" id="rad-disabled" name="size" disabled/><label for="rad-disabled" class="text-sm text-slate-400 dark:text-slate-500 cursor-not-allowed">Disabled radio</label></div>\n'
    h += end_section()

    # Toggle Switches
    h += section('Toggle Switches')
    toggles = [('Email notifications', True), ('SMS alerts', False), ('Auto-save', True), ('Dark mode', False), ('Marketing emails', False)]
    for label, checked in toggles:
        cid = label.replace(' ','-').lower()
        ch = ' checked' if checked else ''
        h += '<div class="flex items-center justify-between mb-3"><span class="text-sm text-slate-600 dark:text-slate-400">' + label + '</span><label class="switch"><input type="checkbox" id="sw-' + cid + '"' + ch + '/><span class="slider"></span></label></div>\n'
    h += '<div class="flex items-center justify-between mb-3"><span class="text-sm text-slate-400 dark:text-slate-500">Disabled toggle</span><label class="switch"><input type="checkbox" disabled/><span class="slider"></span></label></div>\n'
    h += end_section()

    # File Upload
    h += section('File Upload')
    h += field_group('Default File Input', '<input type="file" class="form-input p-2"/>')
    h += '<div class="form-group">\n<label class="form-label">Drag & Drop Zone</label>\n<div class="file-drop" id="file-drop" onclick="document.getElementById(\'file-input\').click()">\n<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>\n<p class="text-sm text-slate-500 dark:text-slate-400">Drag files here or <span class="text-indigo-500 font-medium">browse</span></p>\n<p class="text-xs text-slate-400 mt-1">PNG, JPG, GIF up to 10MB</p>\n<input type="file" id="file-input" class="hidden" multiple onchange="handleFileSelect(this)"/>\n</div>\n<p class="form-hint" id="file-names"></p>\n</div>\n'
    h += end_section()

    # Range & Color
    h += section('Range & Color Inputs')
    h += field_group('Range Slider', '<input type="range" class="range-input" min="0" max="100" value="50" oninput="document.getElementById(\'range-val\').textContent=this.value"/>', '<span id="range-val">50</span>')
    h += field_group('Volume Control', '<input type="range" class="range-input" min="0" max="100" value="75"/>')
    h += field_group('Color Picker', '<div class="flex gap-2 items-center"><input type="color" value="#6366f1" class="color-swatch"/><input type="text" class="form-input w-32" value="#6366f1" id="color-text" oninput="document.getElementById(\'color-pick\').value=this.value"/><input type="color" id="color-pick" value="#6366f1" class="color-swatch" oninput="document.getElementById(\'color-text\').value=this.value"/></div>')
    h += end_section()

    # Input Groups
    h += section('Input Groups')
    h += field_group('Prepend', '<div class="input-group"><span class="input-group-addon">$</span><input type="text" class="form-input" placeholder="0.00"/></div>')
    h += field_group('Append', '<div class="input-group"><input type="text" class="form-input" placeholder="Enter username"/><span class="input-group-addon">@company.com</span></div>')
    h += field_group('Both', '<div class="input-group"><span class="input-group-addon">https://</span><input type="text" class="form-input" placeholder="yoursite"/><span class="input-group-addon">.com</span></div>')
    h += field_group('Search with Button', '<div class="input-group"><input type="text" class="form-input" placeholder="Search..."/><button type="button" class="px-4 bg-indigo-500 text-white text-sm font-medium rounded-r-lg hover:bg-indigo-600 transition-colors">Go</button></div>')
    h += end_section()

    # Hidden & Special
    h += section('Special Inputs')
    h += field_group('Search', '<input type="search" class="form-input" placeholder="Search..." results="5"/>')
    h += field_group('Password', '<div class="password-wrapper"><input type="password" class="form-input" id="pw-basic" placeholder="Enter password"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'pw-basic\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += field_group('Password with Strength', '<div class="password-wrapper"><input type="password" class="form-input" id="pw-strength" placeholder="Create a password" oninput="updateStrength(this)"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'pw-strength\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div><div class="strength-bar"><div class="fill" id="pw-strength-bar" style="width:0%;background:#ef4444"></div></div><p class="form-hint" id="pw-strength-text">Use 8+ characters with a mix of letters, numbers & symbols</p>')
    h += end_section()

    h += '</main>\n</div>\n</div>\n'

    js = '''
function handleFileSelect(input){
  var names=[];
  for(var i=0;i<input.files.length;i++)names.push(input.files[i].name);
  document.getElementById('file-names').textContent=names.join(', ')||'No files selected';
}
function updateStrength(input){
  var v=input.value,s=0,bar=document.getElementById('pw-strength-bar'),txt=document.getElementById('pw-strength-text');
  if(v.length>=8)s+=25;if(/[A-Z]/.test(v))s+=25;if(/[0-9]/.test(v))s+=25;if(/[^A-Za-z0-9]/.test(v))s+=25;
  bar.style.width=s+'%';
  if(s<=25){bar.style.background='#ef4444';txt.textContent='Weak'}
  else if(s<=50){bar.style.background='#f97316';txt.textContent='Fair'}
  else if(s<=75){bar.style.background='#eab308';txt.textContent='Good'}
  else{bar.style.background='#22c55e';txt.textContent='Strong'}
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Validation Forms Page
# ============================================================
def gen_validation_forms():
    title = 'Form Validation'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Real-time form validation with inline error messages')

    # Login Validation
    h += section('Login Form Validation', 'Submit to see validation in action')
    h += '<form id="val-login" novalidate onsubmit="return validateLogin(event)">\n'
    h += field_group('Email', '<input type="email" class="form-input" id="vl-email" placeholder="you@example.com" onblur="validateField(\'vl-email\',\'email\')"/>')
    h += field_group('Password', '<div class="password-wrapper"><input type="password" class="form-input" id="vl-password" placeholder="Enter password" onblur="validateField(\'vl-password\',\'required\')"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'vl-password\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += '<div class="checkbox-wrapper mb-4"><input type="checkbox" id="vl-remember"/><label for="vl-remember" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">Remember me</label></div>\n'
    h += '<button type="submit" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Sign In</button>\n'
    h += '</form>\n'
    h += end_section()

    # Registration Validation
    h += section('Registration Form Validation')
    h += '<form id="val-register" novalidate onsubmit="return validateRegister(event)">\n'
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('First Name', '<input type="text" class="form-input" id="vr-fname" placeholder="John" onblur="validateField(\'vr-fname\',\'required\')"/>')
    h += field_group('Last Name', '<input type="text" class="form-input" id="vr-lname" placeholder="Doe" onblur="validateField(\'vr-lname\',\'required\')"/>')
    h += '</div>\n'
    h += field_group('Email', '<input type="email" class="form-input" id="vr-email" placeholder="you@example.com" onblur="validateField(\'vr-email\',\'email\')"/>')
    h += field_group('Password', '<div class="password-wrapper"><input type="password" class="form-input" id="vr-password" placeholder="Min 8 characters" onblur="validateField(\'vr-password\',\'password\')"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'vr-password\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += field_group('Confirm Password', '<div class="password-wrapper"><input type="password" class="form-input" id="vr-confirm" placeholder="Re-enter password" onblur="validateConfirm()"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'vr-confirm\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += field_group('Phone', '<input type="tel" class="form-input" id="vr-phone" placeholder="+1 (555) 000-0000" onblur="validateField(\'vr-phone\',\'phone\')"/>')
    h += '<div class="checkbox-wrapper mb-4"><input type="checkbox" id="vr-terms"/><label for="vr-terms" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">I agree to the <a href="#" class="text-indigo-500">Terms</a> and <a href="#" class="text-indigo-500">Privacy Policy</a></label></div>\n'
    h += '<button type="submit" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Create Account</button>\n'
    h += '</form>\n'
    h += end_section()

    # Profile Validation
    h += section('Profile Form Validation')
    h += '<form id="val-profile" novalidate onsubmit="return validateProfile(event)">\n'
    h += field_group('Full Name', '<input type="text" class="form-input" id="vp-name" placeholder="John Doe" onblur="validateField(\'vp-name\',\'required\')"/>')
    h += field_group('Username', '<input type="text" class="form-input" id="vp-username" placeholder="johndoe" onblur="validateField(\'vp-username\',\'username\')"/>', '3-20 characters, alphanumeric and underscores')
    h += field_group('Website', '<input type="url" class="form-input" id="vp-website" placeholder="https://yoursite.com" onblur="validateField(\'vp-website\',\'url\')"/>')
    h += field_group('Bio', '<textarea class="form-input" id="vp-bio" rows="3" placeholder="Tell us about yourself..." onblur="validateField(\'vp-bio\',\'optional\')"></textarea>', 'Max 200 characters')
    h += '<button type="submit" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Save Profile</button>\n'
    h += '</form>\n'
    h += end_section()

    # Validation States Showcase
    h += section('Validation States', 'Visual reference for all field states')
    h += field_group('Default State', '<input type="text" class="form-input" placeholder="Default input"/>')
    h += field_group('Focus State', '<input type="text" class="form-input" placeholder="Click to see focus" style="border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.12)"/>')
    h += field_group('Success State', '<input type="text" class="form-input success" value="john@example.com"/>', '', '', 'Looks good!')
    h += field_group('Error State', '<input type="text" class="form-input error" value="invalid"/>', '', 'This field is required')
    h += field_group('Disabled State', '<input type="text" class="form-input" placeholder="Disabled" disabled/>')
    h += field_group('Readonly State', '<input type="text" class="form-input" value="Read-only content" readonly/>')
    h += end_section()

    h += '</main>\n</div>\n</div>\n'

    js = '''
function validateField(id,type){
  var el=document.getElementById(id),val=el.value.trim(),errEl=el.parentElement.querySelector('.form-error')||el.closest('.form-group').querySelector('.form-error');
  if(!errEl){errEl=document.createElement('p');errEl.className='form-error';el.closest('.form-group').appendChild(errEl)}
  var msg='';
  if(type==='required'&&!val)msg='This field is required';
  else if(type==='email'&&val&&!validateEmail(val))msg='Please enter a valid email';
  else if(type==='password'&&val&&val.length<8)msg='Password must be at least 8 characters';
  else if(type==='phone'&&val&&!val.match(/^\\+?[\\d\\s()-]{7,}$/))msg='Please enter a valid phone number';
  else if(type==='username'&&val&&!val.match(/^[a-zA-Z0-9_]{3,20}$/))msg='Username must be 3-20 alphanumeric characters';
  else if(type==='url'&&val&&!val.match(/^https?:\\/\\/.+/))msg='Please enter a valid URL';
  if(msg){el.classList.add('error');el.classList.remove('success');errEl.textContent=msg;errEl.style.display='block'}
  else{el.classList.remove('error');if(val)el.classList.add('success');errEl.style.display='none'}
  return !msg;
}
function validateConfirm(){
  var pw=document.getElementById('vr-password').value,cf=document.getElementById('vr-confirm'),errEl=cf.closest('.form-group').querySelector('.form-error');
  if(!errEl){errEl=document.createElement('p');errEl.className='form-error';cf.closest('.form-group').appendChild(errEl)}
  if(cf.value&&cf.value!==pw){cf.classList.add('error');errEl.textContent='Passwords do not match';errEl.style.display='block'}
  else{cf.classList.remove('error');if(cf.value)cf.classList.add('success');errEl.style.display='none'}
}
function validateLogin(e){
  e.preventDefault();var v1=validateField('vl-email','email'),v2=validateField('vl-password','required');
  if(v1&&v2)showToast('Login successful!','success');return false;
}
function validateRegister(e){
  e.preventDefault();var v=true;
  ['vr-fname','vr-lname'].forEach(function(id){if(!validateField(id,'required'))v=false});
  if(!validateField('vr-email','email'))v=false;
  if(!validateField('vr-password','password'))v=false;
  validateConfirm();
  if(!validateField('vr-phone','phone'))v=false;
  if(!document.getElementById('vr-terms').checked){showToast('Please accept the terms','error');v=false}
  if(v)showToast('Account created successfully!','success');return false;
}
function validateProfile(e){
  e.preventDefault();var v=true;
  if(!validateField('vp-name','required'))v=false;
  if(!validateField('vp-username','username'))v=false;
  if(document.getElementById('vp-website').value&&!validateField('vp-website','url'))v=false;
  if(v)showToast('Profile saved!','success');return false;
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Advanced Forms Page
# ============================================================
def gen_advanced_forms():
    title = 'Advanced Forms'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Advanced form controls, layouts, and interactive elements')

    # Tag Input
    h += section('Tag Input', 'Add and remove tags dynamically')
    h += '<div class="form-group"><label class="form-label">Skills</label><div class="form-input flex flex-wrap gap-2 min-h-[2.75rem] items-center" id="tag-container" onclick="document.getElementById(\'tag-input\').focus()"><span class="inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded-full dark:bg-indigo-900/30 dark:text-indigo-300">JavaScript <button type="button" class="hover:text-indigo-900" onclick="removeTag(this)">&times;</button></span><span class="inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded-full dark:bg-indigo-900/30 dark:text-indigo-300">React <button type="button" class="hover:text-indigo-900" onclick="removeTag(this)">&times;</button></span><input type="text" id="tag-input" class="border-none outline-none flex-1 min-w-[80px] text-sm bg-transparent" placeholder="Add tag..." onkeydown="handleTagInput(event)"/></div></div>\n'
    h += end_section()

    # Rich Text Editor (simplified)
    h += section('Rich Text Editor', 'Basic toolbar with contenteditable')
    h += '<div class="form-group"><label class="form-label">Content</label><div class="border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden"><div class="flex gap-1 p-2 border-b border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 flex-wrap"><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm font-bold" onclick="document.execCommand(\'bold\')" title="Bold">B</button><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm italic" onclick="document.execCommand(\'italic\')" title="Italic">I</button><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm underline" onclick="document.execCommand(\'underline\')" title="Underline">U</button><span class="w-px h-6 bg-slate-300 dark:bg-slate-600 self-center mx-1"></span><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm" onclick="document.execCommand(\'insertUnorderedList\')" title="Bullet List">&#8226; List</button><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm" onclick="document.execCommand(\'insertOrderedList\')" title="Numbered List">1. List</button><span class="w-px h-6 bg-slate-300 dark:bg-slate-600 self-center mx-1"></span><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm" onclick="document.execCommand(\'justifyLeft\')" title="Align Left">Left</button><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm" onclick="document.execCommand(\'justifyCenter\')" title="Center">Center</button><button type="button" class="p-1.5 rounded hover:bg-slate-200 dark:hover:bg-slate-700 text-sm" onclick="document.execCommand(\'justifyRight\')" title="Right">Right</button></div><div contenteditable="true" class="p-3 min-h-[150px] text-sm outline-none bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200" placeholder="Start writing...">Start typing your content here...</div></div></div>\n'
    h += end_section()

    # Date Range Picker
    h += section('Date Range & Time Picker')
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('Start Date', '<input type="date" class="form-input"/>')
    h += field_group('End Date', '<input type="date" class="form-input"/>')
    h += '</div>\n'
    h += field_group('Time Range', '<div class="grid grid-cols-2 gap-4"><div><input type="time" class="form-input" value="09:00"/></div><div><input type="time" class="form-input" value="17:00"/></div></div>')
    h += end_section()

    # Repeatable Sections
    h += section('Repeatable Sections', 'Add/remove groups of fields')
    h += '<div id="repeat-container">\n'
    h += '<div class="repeat-item border border-slate-200 dark:border-slate-700 rounded-lg p-4 mb-3">\n<div class="flex items-center justify-between mb-3"><span class="text-sm font-medium text-slate-700 dark:text-slate-300">Experience #1</span><button type="button" class="text-xs text-red-500 hover:text-red-700" onclick="removeRepeatItem(this)">Remove</button></div>\n'
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('Company', '<input type="text" class="form-input" placeholder="Company name"/>')
    h += field_group('Role', '<input type="text" class="form-input" placeholder="Job title"/>')
    h += '</div>\n'
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('Start Date', '<input type="date" class="form-input"/>')
    h += field_group('End Date', '<input type="date" class="form-input"/>')
    h += '</div>\n'
    h += '</div>\n</div>\n'
    h += '<button type="button" class="text-sm text-indigo-500 hover:text-indigo-700 font-medium" onclick="addRepeatItem()">+ Add Experience</button>\n'
    h += end_section()

    # Multi-step Indicator
    h += section('Form Progress Indicator')
    h += '<div class="flex items-center gap-2 mb-6">\n<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-indigo-500 text-white flex items-center justify-center text-sm font-medium">1</div><span class="text-sm font-medium text-slate-700 dark:text-slate-300">Personal</span></div>\n<div class="flex-1 h-0.5 bg-indigo-500"></div>\n<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-indigo-500 text-white flex items-center justify-center text-sm font-medium">2</div><span class="text-sm font-medium text-slate-700 dark:text-slate-300">Address</span></div>\n<div class="flex-1 h-0.5 bg-slate-200 dark:bg-slate-700"></div>\n<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-400 flex items-center justify-center text-sm font-medium">3</div><span class="text-sm text-slate-400">Payment</span></div>\n<div class="flex-1 h-0.5 bg-slate-200 dark:bg-slate-700"></div>\n<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-400 flex items-center justify-center text-sm font-medium">4</div><span class="text-sm text-slate-400">Review</span></div>\n</div>\n'
    h += end_section()

    # Conditional Fields
    h += section('Conditional Fields', 'Show/hide fields based on selections')
    h += '<div class="form-group"><label class="form-label">Contact Method</label><select class="form-input" onchange="toggleContactFields(this.value)"><option value="">Select method</option><option value="email">Email</option><option value="phone">Phone</option><option value="mail">Mail</option></select></div>\n'
    h += '<div id="contact-email" style="display:none">' + field_group('Email Address', '<input type="email" class="form-input" placeholder="you@example.com"/>') + '</div>\n'
    h += '<div id="contact-phone" style="display:none">' + field_group('Phone Number', '<input type="tel" class="form-input" placeholder="+1 (555) 000-0000"/>') + '</div>\n'
    h += '<div id="contact-mail" style="display:none">' + field_group('Mailing Address', '<textarea class="form-input" rows="2" placeholder="Full mailing address"></textarea>') + '</div>\n'
    h += end_section()

    # Autocomplete
    h += section('Autocomplete Input', 'Type to see suggestions')
    h += '<div class="form-group"><label class="form-label">Country</label><div class="relative"><input type="text" class="form-input" id="ac-input" placeholder="Start typing..." autocomplete="off" oninput="handleAutocomplete(this.value)"/><div id="ac-dropdown" class="absolute top-full left-0 right-0 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-b-lg shadow-lg max-h-48 overflow-y-auto z-10" style="display:none"></div></div></div>\n'
    h += end_section()

    # Rating Input
    h += section('Rating Input')
    h += '<div class="form-group"><label class="form-label">Rate your experience</label><div class="flex gap-1" id="rating-container">'
    for i in range(1, 6):
        h += '<button type="button" class="text-2xl text-slate-300 hover:text-amber-400 transition-colors" onclick="setRating(' + str(i) + ')" data-rating="' + str(i) + '">&#9733;</button>'
    h += '</div><p class="form-hint" id="rating-text">Click a star to rate</p></div>\n'
    h += end_section()

    # Signature Pad
    h += section('Signature Pad', 'Draw your signature below')
    h += '<div class="form-group"><label class="form-label">Signature</label><div class="border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden"><canvas id="sig-canvas" width="400" height="150" class="w-full bg-white dark:bg-slate-900 cursor-crosshair"></canvas><div class="flex justify-end p-2 border-t border-slate-200 dark:border-slate-700"><button type="button" class="text-xs text-slate-500 hover:text-slate-700" onclick="clearSignature()">Clear</button></div></div></div>\n'
    h += end_section()

    h += '</main>\n</div>\n</div>\n'

    js = '''
function handleTagInput(e){
  if(e.key==='Enter'){e.preventDefault();var input=document.getElementById('tag-input'),val=input.value.trim();
  if(!val)return;var container=document.getElementById('tag-container');
  var tag=document.createElement('span');tag.className='inline-flex items-center gap-1 px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded-full dark:bg-indigo-900/30 dark:text-indigo-300';
  tag.innerHTML=val+' <button type="button" class="hover:text-indigo-900" onclick="removeTag(this)">&times;</button>';
  container.insertBefore(tag,input);input.value='';}
}
function removeTag(btn){btn.parentElement.remove()}
function toggleContactFields(val){
  document.getElementById('contact-email').style.display=val==='email'?'block':'none';
  document.getElementById('contact-phone').style.display=val==='phone'?'block':'none';
  document.getElementById('contact-mail').style.display=val==='mail'?'block':'none';
}
var countries=['United States','United Kingdom','Canada','Australia','Germany','France','Japan','China','India','Brazil','Mexico','South Korea','Italy','Spain','Netherlands','Sweden','Norway','Denmark','Finland','Switzerland'];
function handleAutocomplete(val){
  var dd=document.getElementById('ac-dropdown');
  if(!val){dd.style.display='none';return}
  var matches=countries.filter(function(c){return c.toLowerCase().indexOf(val.toLowerCase())>=0});
  if(!matches.length){dd.style.display='none';return}
  dd.innerHTML=matches.map(function(m){return '<div class="px-3 py-2 text-sm hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer" onclick="selectAC(\\''+m.replace(/'/g,"\\\\'")+'\\')">'+m+'</div>'}).join('');
  dd.style.display='block';
}
function selectAC(val){document.getElementById('ac-input').value=val;document.getElementById('ac-dropdown').style.display='none'}
function setRating(n){
  var btns=document.querySelectorAll('#rating-container button');
  btns.forEach(function(b,i){b.style.color=i<n?'#f59e0b':'#cbd5e1'});
  var labels=['','Poor','Fair','Good','Very Good','Excellent'];
  document.getElementById('rating-text').textContent=labels[n]+' ('+n+'/5)';
}
var repeatCount=1;
function addRepeatItem(){
  repeatCount++;var container=document.getElementById('repeat-container');
  var div=document.createElement('div');div.className='repeat-item border border-slate-200 dark:border-slate-700 rounded-lg p-4 mb-3';
  div.innerHTML='<div class="flex items-center justify-between mb-3"><span class="text-sm font-medium text-slate-700 dark:text-slate-300">Experience #'+repeatCount+'</span><button type="button" class="text-xs text-red-500 hover:text-red-700" onclick="removeRepeatItem(this)">Remove</button></div><div class="grid grid-cols-2 gap-4"><div class="form-group"><label class="form-label">Company</label><input type="text" class="form-input" placeholder="Company name"/></div><div class="form-group"><label class="form-label">Role</label><input type="text" class="form-input" placeholder="Job title"/></div></div><div class="grid grid-cols-2 gap-4"><div class="form-group"><label class="form-label">Start Date</label><input type="date" class="form-input"/></div><div class="form-group"><label class="form-label">End Date</label><input type="date" class="form-input"/></div></div>';
  container.appendChild(div);
}
function removeRepeatItem(btn){btn.closest('.repeat-item').remove()}
// Signature pad
var sigCanvas=document.getElementById('sig-canvas'),sigCtx=sigCanvas.getContext('2d'),drawing=false;
sigCanvas.addEventListener('mousedown',function(e){drawing=true;sigCtx.beginPath();var r=sigCanvas.getBoundingClientRect();sigCtx.moveTo(e.clientX-r.left,e.clientY-r.top)});
sigCanvas.addEventListener('mousemove',function(e){if(!drawing)return;var r=sigCanvas.getBoundingClientRect();sigCtx.lineTo(e.clientX-r.left,e.clientY-r.top);sigCtx.strokeStyle='#0f172a';sigCtx.lineWidth=2;sigCtx.stroke()});
sigCanvas.addEventListener('mouseup',function(){drawing=false});
sigCanvas.addEventListener('mouseleave',function(){drawing=false});
function clearSignature(){sigCtx.clearRect(0,0,sigCanvas.width,sigCanvas.height)}
// Touch support
sigCanvas.addEventListener('touchstart',function(e){e.preventDefault();drawing=true;sigCtx.beginPath();var r=sigCanvas.getBoundingClientRect();var t=e.touches[0];sigCtx.moveTo(t.clientX-r.left,t.clientY-r.top)});
sigCanvas.addEventListener('touchmove',function(e){e.preventDefault();if(!drawing)return;var r=sigCanvas.getBoundingClientRect();var t=e.touches[0];sigCtx.lineTo(t.clientX-r.left,t.clientY-r.top);sigCtx.strokeStyle='#0f172a';sigCtx.lineWidth=2;sigCtx.stroke()});
sigCanvas.addEventListener('touchend',function(){drawing=false});
'''
    h += page_foot(js)
    return h

# ============================================================
# Wizard Form Page
# ============================================================
def gen_wizard_form():
    title = 'Multi-Step Wizard'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Multi-step form with progress tracking and validation')

    h += '<div class="component-item fade-up" style="max-width:640px">\n'
    # Progress
    h += '<div class="flex items-center justify-between mb-8">\n'
    steps = ['Account', 'Profile', 'Social', 'Review']
    for i, s in enumerate(steps):
        cls = 'bg-indigo-500 text-white' if i == 0 else 'bg-slate-200 dark:bg-slate-700 text-slate-500'
        h += '<div class="flex items-center gap-2"><div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ' + cls + '" id="wiz-step-' + str(i) + '">' + str(i+1) + '</div><span class="text-sm font-medium ' + ('text-slate-700 dark:text-slate-300' if i==0 else 'text-slate-400') + '" id="wiz-label-' + str(i) + '">' + s + '</span></div>\n'
        if i < len(steps) - 1:
            h += '<div class="flex-1 h-0.5 bg-slate-200 dark:bg-slate-700" id="wiz-line-' + str(i) + '"></div>\n'
    h += '</div>\n'

    # Step 1: Account
    h += '<div class="wizard-step active" id="wiz-p-0">\n'
    h += '<h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Account Information</h3>\n'
    h += field_group('Email', '<input type="email" class="form-input" id="wz-email" placeholder="you@example.com"/>')
    h += field_group('Password', '<div class="password-wrapper"><input type="password" class="form-input" id="wz-password" placeholder="Min 8 characters"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'wz-password\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += field_group('Confirm Password', '<div class="password-wrapper"><input type="password" class="form-input" id="wz-confirm" placeholder="Re-enter password"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'wz-confirm\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += '<div class="flex justify-end"><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="wizardNext()">Next</button></div>\n'
    h += '</div>\n'

    # Step 2: Profile
    h += '<div class="wizard-step" id="wiz-p-1">\n'
    h += '<h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Profile Details</h3>\n'
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('First Name', '<input type="text" class="form-input" id="wz-fname" placeholder="John"/>')
    h += field_group('Last Name', '<input type="text" class="form-input" id="wz-lname" placeholder="Doe"/>')
    h += '</div>\n'
    h += field_group('Phone', '<input type="tel" class="form-input" id="wz-phone" placeholder="+1 (555) 000-0000"/>')
    h += field_group('Country', '<select class="form-input" id="wz-country"><option value="">Select country</option><option>United States</option><option>United Kingdom</option><option>Canada</option><option>Australia</option><option>Germany</option></select>')
    h += '<div class="flex justify-between"><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="wizardPrev()">Back</button><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="wizardNext()">Next</button></div>\n'
    h += '</div>\n'

    # Step 3: Social
    h += '<div class="wizard-step" id="wiz-p-2">\n'
    h += '<h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Social Profiles</h3>\n'
    h += field_group('Twitter', '<div class="input-group"><span class="input-group-addon">@</span><input type="text" class="form-input" id="wz-twitter" placeholder="username"/></div>')
    h += field_group('GitHub', '<div class="input-group"><span class="input-group-addon">github.com/</span><input type="text" class="form-input" id="wz-github" placeholder="username"/></div>')
    h += field_group('LinkedIn', '<div class="input-group"><span class="input-group-addon">linkedin.com/in/</span><input type="text" class="form-input" id="wz-linkedin" placeholder="username"/></div>')
    h += field_group('Website', '<input type="url" class="form-input" id="wz-website" placeholder="https://yoursite.com"/>')
    h += '<div class="flex justify-between"><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="wizardPrev()">Back</button><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="wizardNext()">Next</button></div>\n'
    h += '</div>\n'

    # Step 4: Review
    h += '<div class="wizard-step" id="wiz-p-3">\n'
    h += '<h3 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">Review & Submit</h3>\n'
    h += '<div class="space-y-3 mb-6" id="wiz-review">\n'
    h += '<div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg"><p class="text-xs text-slate-400 mb-1">Email</p><p class="text-sm font-medium text-slate-700 dark:text-slate-300" id="rev-email">-</p></div>\n'
    h += '<div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg"><p class="text-xs text-slate-400 mb-1">Name</p><p class="text-sm font-medium text-slate-700 dark:text-slate-300" id="rev-name">-</p></div>\n'
    h += '<div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg"><p class="text-xs text-slate-400 mb-1">Phone</p><p class="text-sm font-medium text-slate-700 dark:text-slate-300" id="rev-phone">-</p></div>\n'
    h += '<div class="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg"><p class="text-xs text-slate-400 mb-1">Country</p><p class="text-sm font-medium text-slate-700 dark:text-slate-300" id="rev-country">-</p></div>\n'
    h += '</div>\n'
    h += '<div class="checkbox-wrapper mb-4"><input type="checkbox" id="wz-terms"/><label for="wz-terms" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">I confirm all information is correct</label></div>\n'
    h += '<div class="flex justify-between"><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" onclick="wizardPrev()">Back</button><button type="button" class="px-5 py-2.5 bg-green-500 text-white text-sm font-medium rounded-lg hover:bg-green-600 transition-colors" onclick="wizardSubmit()">Submit</button></div>\n'
    h += '</div>\n'

    h += '</div>\n'
    h += '</main>\n</div>\n</div>\n'

    js = '''
var wizCurrent=0,wizTotal=4;
function wizardNext(){
  if(!validateWizardStep(wizCurrent))return;
  if(wizCurrent<wizTotal-1){showWizardStep(wizCurrent+1);wizCurrent++}
}
function wizardPrev(){if(wizCurrent>0){showWizardStep(wizCurrent-1);wizCurrent--}}
function showWizardStep(n){
  for(var i=0;i<wizTotal;i++){
    var p=document.getElementById('wiz-p-'+i);
    p.classList.toggle('active',i===n);
    var step=document.getElementById('wiz-step-'+i);
    var label=document.getElementById('wiz-label-'+i);
    if(i<n){step.className='w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-green-500 text-white';label.className='text-sm font-medium text-green-600'}
    else if(i===n){step.className='w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-indigo-500 text-white';label.className='text-sm font-medium text-slate-700 dark:text-slate-300'}
    else{step.className='w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-slate-200 dark:bg-slate-700 text-slate-500';label.className='text-sm text-slate-400'}
    if(i<wizTotal-1){var line=document.getElementById('wiz-line-'+i);line.className='flex-1 h-0.5 '+(i<n?'bg-green-500':'bg-slate-200 dark:bg-slate-700')}
  }
  if(n===3)populateReview();
}
function validateWizardStep(n){
  if(n===0){
    var em=document.getElementById('wz-email'),pw=document.getElementById('wz-password'),cf=document.getElementById('wz-confirm');
    if(!validateEmail(em.value)){showFieldError('wz-email','Invalid email');return false}clearFieldError('wz-email');
    if(pw.value.length<8){showFieldError('wz-password','Min 8 characters');return false}clearFieldError('wz-password');
    if(pw.value!==cf.value){showFieldError('wz-confirm','Passwords do not match');return false}clearFieldError('wz-confirm');
  }
  if(n===1){
    var fn=document.getElementById('wz-fname'),ln=document.getElementById('wz-lname');
    if(!fn.value.trim()){showFieldError('wz-fname','Required');return false}clearFieldError('wz-fname');
    if(!ln.value.trim()){showFieldError('wz-lname','Required');return false}clearFieldError('wz-lname');
  }
  return true;
}
function populateReview(){
  document.getElementById('rev-email').textContent=document.getElementById('wz-email').value||'-';
  document.getElementById('rev-name').textContent=(document.getElementById('wz-fname').value||'')+' '+(document.getElementById('wz-lname').value||'')||'-';
  document.getElementById('rev-phone').textContent=document.getElementById('wz-phone').value||'-';
  document.getElementById('rev-country').textContent=document.getElementById('wz-country').value||'-';
}
function wizardSubmit(){
  if(!document.getElementById('wz-terms').checked){showToast('Please confirm the information','error');return}
  showToast('Form submitted successfully!','success');
}
'''
    h += page_foot(js)
    return h

# ============================================================
# Settings Form Page
# ============================================================
def gen_settings_form():
    title = 'Settings Form'
    h = page_head(title)
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Application settings with organized sections')

    # General Settings
    h += section('General Settings')
    h += field_group('Site Name', '<input type="text" class="form-input" value="My Application"/>')
    h += field_group('Site URL', '<div class="input-group"><span class="input-group-addon">https://</span><input type="text" class="form-input" value="myapp.com"/></div>')
    h += field_group('Timezone', '<select class="form-input"><option>UTC</option><option>America/New_York</option><option>America/Los_Angeles</option><option>Europe/London</option><option>Europe/Berlin</option><option>Asia/Tokyo</option></select>')
    h += field_group('Language', '<select class="form-input"><option>English</option><option>Spanish</option><option>French</option><option>German</option><option>Japanese</option></select>')
    h += field_group('Date Format', '<select class="form-input"><option>MM/DD/YYYY</option><option>DD/MM/YYYY</option><option>YYYY-MM-DD</option></select>')
    h += '<button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Settings saved!\',\'success\')">Save Changes</button>\n'
    h += end_section()

    # Notification Settings
    h += section('Notification Settings')
    notif_settings = [
        ('Email Notifications', 'Receive email updates about your account', True),
        ('Push Notifications', 'Get push notifications on your device', True),
        ('SMS Alerts', 'Receive SMS for critical alerts', False),
        ('Weekly Digest', 'Get a weekly summary email', True),
        ('Marketing Emails', 'Receive promotional offers', False),
        ('Security Alerts', 'Get notified about security events', True),
        ('Activity Summary', 'Daily activity digest', False),
    ]
    for label, desc, checked in notif_settings:
        cid = label.replace(' ','-').lower()
        ch = ' checked' if checked else ''
        h += '<div class="flex items-center justify-between py-3 border-b border-slate-100 dark:border-slate-700 last:border-0"><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">' + label + '</p><p class="text-xs text-slate-400">' + desc + '</p></div><label class="switch"><input type="checkbox" id="sw-' + cid + '"' + ch + '/><span class="slider"></span></label></div>\n'
    h += end_section()

    # Privacy Settings
    h += section('Privacy Settings')
    h += '<div class="form-group"><label class="form-label">Profile Visibility</label><div class="space-y-2">'
    for val, label in [('public','Public - Anyone can see your profile'), ('members','Members - Only members can see your profile'), ('private','Private - Only you can see your profile')]:
        h += '<div class="radio-wrapper"><input type="radio" id="vis-' + val + '" name="visibility" value="' + val + '"/><label for="vis-' + val + '" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">' + label + '</label></div>\n'
    h += '</div></div>\n'
    h += '<div class="form-group"><label class="form-label">Data Sharing</label>'
    for label in ['Share usage data for analytics', 'Allow third-party integrations', 'Enable personalized recommendations']:
        cid = label[:10].replace(' ','-').lower()
        h += '<div class="checkbox-wrapper mb-2"><input type="checkbox" id="chk-' + cid + '"/><label for="chk-' + cid + '" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">' + label + '</label></div>\n'
    h += '</div>\n'
    h += end_section()

    # API Settings
    h += section('API Settings')
    h += field_group('API Key', '<div class="input-group"><input type="text" class="form-input font-mono text-xs" value="example_key_xxxxxxxxxxxxxxxxxxxx" readonly/><button type="button" class="px-3 bg-slate-100 dark:bg-slate-800 text-xs font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors" onclick="copySourceCode(this.previousElementSibling);showToast(\'API key copied!\',\'success\')">Copy</button></div>')
    h += field_group('Webhook URL', '<input type="url" class="form-input" placeholder="https://yoursite.com/webhook"/>')
    h += field_group('Rate Limit (req/min)', '<input type="number" class="form-input" value="100" min="1" max="10000"/>')
    h += end_section()

    # Danger Zone
    h += section('Danger Zone', 'Irreversible actions')
    h += '<div class="flex items-center justify-between py-3 border-b border-slate-100 dark:border-slate-700"><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">Delete Account</p><p class="text-xs text-slate-400">Permanently delete your account and all data</p></div><button type="button" class="px-4 py-2 bg-red-50 text-red-600 text-sm font-medium rounded-lg hover:bg-red-100 transition-colors dark:bg-red-900/20 dark:text-red-400" onclick="showToast(\'Account deletion requires confirmation via email\',\'error\')">Delete Account</button></div>\n'
    h += '<div class="flex items-center justify-between py-3"><div><p class="text-sm font-medium text-slate-700 dark:text-slate-300">Export Data</p><p class="text-xs text-slate-400">Download all your data as JSON</p></div><button type="button" class="px-4 py-2 bg-slate-100 text-slate-600 text-sm font-medium rounded-lg hover:bg-slate-200 transition-colors dark:bg-slate-800 dark:text-slate-300" onclick="showToast(\'Data export started. You will receive an email.\',\'success\')">Export</button></div>\n'
    h += end_section()

    h += '</main>\n</div>\n</div>\n'
    h += page_foot()
    return h

# ============================================================
# Profile Edit Form Page
# ============================================================
def gen_profile_edit():
    title = 'Profile Edit'
    h = page_head(title, '\n.avatar-upload{position:relative;width:5rem;height:5rem;border-radius:50%;overflow:hidden;cursor:pointer}\n.avatar-upload img{width:100%;height:100%;object-fit:cover}\n.avatar-upload .overlay{position:absolute;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .2s}\n.avatar-upload:hover .overlay{opacity:1}\n')
    h += sidebar_header()
    h += '<main class="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">\n'
    h += page_header(title, 'Edit your personal profile information')

    h += '<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">\n'

    # Left: Avatar & Quick Info
    h += '<div class="component-item fade-up lg:col-span-1">\n'
    h += '<div class="text-center mb-6">\n'
    h += '<div class="avatar-upload mx-auto mb-3" onclick="document.getElementById(\'avatar-input\').click()">\n'
    h += '<img src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop&crop=face" alt="Avatar"/>\n'
    h += '<div class="overlay"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/><circle cx="12" cy="13" r="4"/></svg></div>\n'
    h += '<input type="file" id="avatar-input" class="hidden" accept="image/*" onchange="previewAvatar(this)"/>\n'
    h += '</div>\n'
    h += '<h3 class="text-lg font-semibold text-slate-900 dark:text-white">John Doe</h3>\n'
    h += '<p class="text-sm text-slate-500">Senior Product Designer</p>\n'
    h += '<p class="text-xs text-slate-400 mt-1">San Francisco, CA</p>\n'
    h += '</div>\n'
    h += '<div class="border-t border-slate-100 dark:border-slate-700 pt-4 space-y-3">\n'
    for label, val in [('Email', 'john@example.com'), ('Phone', '+1 (555) 123-4567'), ('Department', 'Design'), ('Joined', 'Jan 2023')]:
        h += '<div class="flex justify-between text-sm"><span class="text-slate-400">' + label + '</span><span class="text-slate-700 dark:text-slate-300">' + val + '</span></div>\n'
    h += '</div>\n'
    h += '</div>\n'

    # Right: Form
    h += '<div class="lg:col-span-2 space-y-6">\n'

    # Personal Info
    h += '<div class="component-item fade-up">\n<h3>Personal Information</h3>\n'
    h += '<form id="profile-form" novalidate onsubmit="return saveProfile(event)">\n'
    h += '<div class="grid grid-cols-2 gap-4">\n'
    h += field_group('First Name', '<input type="text" class="form-input" id="pf-fname" value="John"/>')
    h += field_group('Last Name', '<input type="text" class="form-input" id="pf-lname" value="Doe"/>')
    h += '</div>\n'
    h += field_group('Email', '<input type="email" class="form-input" id="pf-email" value="john@example.com"/>')
    h += field_group('Phone', '<input type="tel" class="form-input" id="pf-phone" value="+1 (555) 123-4567"/>')
    h += field_group('Location', '<input type="text" class="form-input" id="pf-location" value="San Francisco, CA"/>')
    h += field_group('Bio', '<textarea class="form-input" id="pf-bio" rows="3">Passionate product designer with 8+ years of experience creating intuitive digital experiences.</textarea>')
    h += '<div class="flex justify-end gap-3"><button type="button" class="px-5 py-2.5 border border-slate-300 dark:border-slate-600 text-sm font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">Cancel</button><button type="submit" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors">Save Changes</button></div>\n'
    h += '</form>\n</div>\n'

    # Social Links
    h += '<div class="component-item fade-up">\n<h3>Social Links</h3>\n'
    h += field_group('Twitter', '<div class="input-group"><span class="input-group-addon">@</span><input type="text" class="form-input" value="johndoe"/></div>')
    h += field_group('GitHub', '<div class="input-group"><span class="input-group-addon">github.com/</span><input type="text" class="form-input" value="johndoe"/></div>')
    h += field_group('LinkedIn', '<div class="input-group"><span class="input-group-addon">linkedin.com/in/</span><input type="text" class="form-input" value="johndoe"/></div>')
    h += field_group('Portfolio', '<input type="url" class="form-input" value="https://johndoe.design"/>')
    h += '<div class="flex justify-end"><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Social links saved!\',\'success\')">Save</button></div>\n'
    h += '</div>\n'

    # Security
    h += '<div class="component-item fade-up">\n<h3>Security</h3>\n'
    h += field_group('Current Password', '<div class="password-wrapper"><input type="password" class="form-input" id="pf-current-pw" placeholder="Enter current password"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'pf-current-pw\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += field_group('New Password', '<div class="password-wrapper"><input type="password" class="form-input" id="pf-new-pw" placeholder="Enter new password"/><button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'pf-new-pw\')"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></button></div>')
    h += '<div class="flex justify-end"><button type="button" class="px-5 py-2.5 bg-indigo-500 text-white text-sm font-medium rounded-lg hover:bg-indigo-600 transition-colors" onclick="showToast(\'Password updated!\',\'success\')">Update Password</button></div>\n'
    h += '</div>\n'

    h += '</div>\n</div>\n'
    h += '</main>\n</div>\n</div>\n'

    js = '''
function saveProfile(e){
  e.preventDefault();
  var fn=document.getElementById('pf-fname'),ln=document.getElementById('pf-lname'),em=document.getElementById('pf-email');
  var valid=true;
  if(!fn.value.trim()){showFieldError('pf-fname','Required');valid=false}else clearFieldError('pf-fname');
  if(!ln.value.trim()){showFieldError('pf-lname','Required');valid=false}else clearFieldError('pf-lname');
  if(!validateEmail(em.value)){showFieldError('pf-email','Invalid email');valid=false}else clearFieldError('pf-email');
  if(valid)showToast('Profile updated successfully!','success');
  return false;
}
function previewAvatar(input){
  if(input.files&&input.files[0]){
    var reader=new FileReader();
    reader.onload=function(e){input.closest('.avatar-upload').querySelector('img').src=e.target.result};
    reader.readAsDataURL(input.files[0]);
  }
}
'''
    h += page_foot(js)
    return h

# Generate all form pages
pages = [
    ('31-forms-basic.html', gen_basic_forms),
    ('33-forms-validation.html', gen_validation_forms),
    ('108-forms-advanced.html', gen_advanced_forms),
    ('110-forms-wizard.html', gen_wizard_form),
    ('111-forms-settings.html', gen_settings_form),
    ('113-forms-profile-edit.html', gen_profile_edit),
]

print('Generating premium form pages...')
for fname, gen_fn in pages:
    path = os.path.join(OUT, fname)
    html = gen_fn()
    with open(path, 'w') as f:
        f.write(html)
    sz = os.path.getsize(path)
    print('  ' + fname + ': ' + str(sz // 1024) + 'KB')

print('Done! All form pages generated.')
