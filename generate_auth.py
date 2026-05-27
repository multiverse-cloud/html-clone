#!/usr/bin/env python3
"""Generate premium auth pages with real form validation, OTP, password toggle, etc."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'templates', 'html')

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')

def attr_esc(s):
    return s.replace('\\','\\\\').replace("'","\\'").replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def page_head(title, extra_css=''):
    return '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8"/>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>\n<meta http-equiv="X-UA-Compatible" content="ie=edge"/>\n<title>' + esc(title) + ' | TailAdmin</title>\n<link rel="stylesheet" href="tailwind-production.css"/>\n<link rel="stylesheet" href="pro-styles.css"/>\n<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet"/>\n<style>\nbody{font-family:Outfit,system-ui,sans-serif}\n.auth-wrapper{min-height:100vh;display:flex;align-items:center;justify-content:center}\n.auth-card{width:100%;max-width:480px;padding:2.5rem;border-radius:1rem;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.04)}\n.dark .auth-card{background:#1e293b;box-shadow:0 1px 3px rgba(0,0,0,.3),0 8px 24px rgba(0,0,0,.2)}\n.auth-illustration{display:flex;align-items:center;justify-content:center;min-height:200px}\n.form-group{margin-bottom:1.25rem}\n.form-label{display:block;margin-bottom:.375rem;font-size:.875rem;font-weight:500;color:#334155}\n.dark .form-label{color:#cbd5e1}\n.form-input{width:100%;padding:.625rem .875rem;border:1.5px solid #e2e8f0;border-radius:.5rem;font-size:.875rem;transition:border-color .15s,box-shadow .15s;background:#fff;color:#0f172a}\n.form-input:focus{outline:none;border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.12)}\n.dark .form-input{background:#0f172a;border-color:#334155;color:#e2e8f0}\n.dark .form-input:focus{border-color:#818cf8;box-shadow:0 0 0 3px rgba(129,140,248,.15)}\n.form-input.error{border-color:#ef4444;box-shadow:0 0 0 3px rgba(239,68,68,.1)}\n.form-input.success{border-color:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.1)}\n.form-error{font-size:.75rem;color:#ef4444;margin-top:.25rem;display:none}\n.form-error.visible{display:block}\n.form-hint{font-size:.75rem;color:#94a3b8;margin-top:.25rem}\n.password-wrapper{position:relative}\n.password-toggle{position:absolute;right:.75rem;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;color:#94a3b8;padding:.25rem}\n.password-toggle:hover{color:#64748b}\n.btn-primary{width:100%;padding:.75rem;border:none;border-radius:.5rem;font-size:.875rem;font-weight:600;color:#fff;background:#6366f1;cursor:pointer;transition:background .15s,transform .1s}\n.btn-primary:hover{background:#4f46e5}\n.btn-primary:active{transform:scale(.98)}\n.btn-primary:disabled{opacity:.6;cursor:not-allowed}\n.btn-outline{width:100%;padding:.75rem;border:1.5px solid #e2e8f0;border-radius:.5rem;font-size:.875rem;font-weight:500;color:#334155;background:#fff;cursor:pointer;transition:background .15s,border-color .15s}\n.btn-outline:hover{background:#f8fafc;border-color:#cbd5e1}\n.dark .btn-outline{background:#1e293b;border-color:#334155;color:#e2e8f0}\n.dark .btn-outline:hover{background:#334155;border-color:#475569}\n.divider{display:flex;align-items:center;gap:.75rem;margin:1.5rem 0;color:#94a3b8;font-size:.8125rem}\n.divider::before,.divider::after{content:"";flex:1;height:1px;background:#e2e8f0}\n.dark .divider::before,.dark .divider::after{background:#334155}\n.otp-input{width:3rem;height:3.5rem;text-align:center;font-size:1.25rem;font-weight:600;border:1.5px solid #e2e8f0;border-radius:.5rem;background:#fff;color:#0f172a;transition:border-color .15s,box-shadow .15s}\n.otp-input:focus{outline:none;border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.12)}\n.dark .otp-input{background:#0f172a;border-color:#334155;color:#e2e8f0}\n.dark .otp-input:focus{border-color:#818cf8}\n.checkbox-wrapper{display:flex;align-items:center;gap:.5rem}\n.checkbox-wrapper input[type=checkbox]{width:1rem;height:1rem;accent-color:#6366f1;cursor:pointer}\n.strength-bar{height:4px;border-radius:2px;background:#e2e8f0;margin-top:.5rem;overflow:hidden}\n.strength-bar .fill{height:100%;border-radius:2px;transition:width .3s,background .3s}\n.dark .strength-bar{background:#334155}\n.social-btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;padding:.625rem 1rem;border:1.5px solid #e2e8f0;border-radius:.5rem;font-size:.8125rem;font-weight:500;color:#334155;background:#fff;cursor:pointer;transition:background .15s}\n.social-btn:hover{background:#f8fafc}\n.dark .social-btn{background:#1e293b;border-color:#334155;color:#e2e8f0}\n.dark .social-btn:hover{background:#334155}\n.link{color:#6366f1;font-weight:500;text-decoration:none;font-size:.875rem;transition:color .15s}\n.link:hover{color:#4f46e5;text-decoration:underline}\n.dark .link{color:#818cf8}\n.dark .link:hover{color:#a5b4fc}\n@keyframes fadeUp{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}\n.fade-up{animation:fadeUp .4s ease-out}\n@keyframes countUp{from{opacity:0}to{opacity:1}}\n@media(prefers-reduced-motion:reduce){.fade-up{animation:none}}\n@media(max-width:640px){.auth-card{margin:1rem;padding:1.5rem;border-radius:.75rem}.auth-split{flex-direction:column}.auth-split .auth-illustration{min-height:160px}}\n' + extra_css + '\n</style>\n</head>\n'

def page_foot(extra_js=''):
    return '<script src="common-loader.js"></script>\n<script>\n' + extra_js + '\n</script>\n</body>\n</html>'

def social_buttons():
    return '''<div class="grid grid-cols-2 gap-3">
<button type="button" class="social-btn" onclick="showToast('Google OAuth would launch here','info')">
<svg width="18" height="18" viewBox="0 0 18 18" fill="none"><path d="M17.64 9.2c0-.74-.07-1.45-.2-2.13H9v4.03h4.87a4.16 4.16 0 01-1.8 2.73v2.27h2.91c1.7-1.57 2.66-3.88 2.66-6.9z" fill="#4285F4"/><path d="M9 18c2.43 0 4.47-.8 5.96-2.17l-2.91-2.27c-.8.54-1.83.86-3.05.86-2.35 0-4.34-1.58-5.05-3.71H.96v2.34A8.99 8.99 0 009 18z" fill="#34A853"/><path d="M3.95 10.71A5.4 5.4 0 013.67 9c0-.6.1-1.17.28-1.71V4.95H.96A8.99 8.99 0 000 9c0 1.45.35 2.82.96 4.05l2.99-2.34z" fill="#FBBC05"/><path d="M9 3.58c1.32 0 2.51.45 3.44 1.35l2.58-2.59C13.46.89 11.43 0 9 0 5.48 0 2.47 2.02.96 4.95l2.99 2.34C4.66 5.16 6.65 3.58 9 3.58z" fill="#EB4335"/></svg>
Google
</button>
<button type="button" class="social-btn" onclick="showToast('GitHub OAuth would launch here','info')">
<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
GitHub
</button>
</div>'''

def password_field(id, label, placeholder='Enter password', with_toggle=True, with_strength=False):
    h = '<div class="form-group">\n<label class="form-label" for="' + id + '">' + label + '</label>\n'
    if with_toggle:
        h += '<div class="password-wrapper">\n<input type="password" id="' + id + '" name="' + id + '" class="form-input" placeholder="' + placeholder + '" autocomplete="' + id + '"/>\n<button type="button" class="password-toggle" onclick="togglePasswordVisibility(\'' + id + '\')" aria-label="Toggle password visibility">\n<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>\n</button>\n</div>\n'
    else:
        h += '<input type="password" id="' + id + '" name="' + id + '" class="form-input" placeholder="' + placeholder + '"/>\n'
    if with_strength:
        h += '<div class="strength-bar"><div class="fill" id="' + id + '-strength" style="width:0%;background:#ef4444"></div></div>\n<p class="form-hint" id="' + id + '-strength-text">Use 8+ characters with a mix of letters, numbers & symbols</p>\n'
    h += '<p class="form-error" id="' + id + '-error"></p>\n</div>\n'
    return h

def email_field(id='email', label='Email', placeholder='you@example.com'):
    return '<div class="form-group">\n<label class="form-label" for="' + id + '">' + label + '</label>\n<input type="email" id="' + id + '" name="' + id + '" class="form-input" placeholder="' + placeholder + '" autocomplete="email"/>\n<p class="form-error" id="' + id + '-error"></p>\n</div>\n'

def text_field(id, label, placeholder='', autocomplete=''):
    ac = ' autocomplete="' + autocomplete + '"' if autocomplete else ''
    return '<div class="form-group">\n<label class="form-label" for="' + id + '">' + label + '</label>\n<input type="text" id="' + id + '" name="' + id + '" class="form-input" placeholder="' + placeholder + '"' + ac + '/>\n<p class="form-error" id="' + id + '-error"></p>\n</div>\n'

def otp_section(digits=6):
    h = '<div class="form-group">\n<label class="form-label">Verification Code</label>\n<div class="flex gap-2 justify-center" id="otp-container">\n'
    for i in range(digits):
        h += '<input type="text" maxlength="1" class="otp-input" data-otp-index="' + str(i) + '" inputmode="numeric" pattern="[0-9]" autocomplete="one-time-code"/>\n'
    h += '</div>\n<p class="form-error text-center" id="otp-error"></p>\n</div>\n'
    return h

def gen_login():
    title = 'Sign In'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up">\n'
    # Back link
    h += '<a href="01-main-dashboard.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to dashboard\n</a>\n'
    # Header
    h += '<div class="mb-6">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Welcome back</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">Sign in to your account to continue</p>\n</div>\n'
    # Social
    h += social_buttons()
    h += '<div class="divider">or</div>\n'
    # Form
    h += '<form id="login-form" novalidate onsubmit="return handleLogin(event)">\n'
    h += email_field()
    h += password_field('password', 'Password', 'Enter your password')
    h += '<div class="flex items-center justify-between mb-5">\n<div class="checkbox-wrapper">\n<input type="checkbox" id="remember" name="remember"/>\n<label for="remember" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">Remember me</label>\n</div>\n<a href="83-auth-forgot-password.html" class="link text-sm">Forgot password?</a>\n</div>\n'
    h += '<button type="submit" class="btn-primary" id="login-btn">Sign In</button>\n'
    h += '</form>\n'
    h += '<p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">Don\'t have an account? <a href="82-auth-register.html" class="link">Sign up</a></p>\n'
    h += '</div>\n</div>\n'
    # JS
    js = '''
function handleLogin(e){
  e.preventDefault();
  var email=document.getElementById('email');
  var pass=document.getElementById('password');
  var valid=true;
  if(!validateEmail(email.value)){showFieldError('email','Please enter a valid email address');valid=false}else{clearFieldError('email')}
  if(!pass.value||pass.value.length<6){showFieldError('password','Password must be at least 6 characters');valid=false}else{clearFieldError('password')}
  if(valid){
    var btn=document.getElementById('login-btn');
    btn.disabled=true;btn.textContent='Signing in...';
    setTimeout(function(){btn.disabled=false;btn.textContent='Sign In';showToast('Login successful! Redirecting...','success');setTimeout(function(){window.location.href='01-main-dashboard.html'},1500)},1200);
  }
  return false;
}
document.getElementById('email').addEventListener('blur',function(){if(this.value&&!validateEmail(this.value))showFieldError('email','Please enter a valid email');else clearFieldError('email')});
document.getElementById('password').addEventListener('blur',function(){if(this.value&&this.value.length<6)showFieldError('password','Password must be at least 6 characters');else clearFieldError('password')});
'''
    h += page_foot(js)
    return h

def gen_register():
    title = 'Sign Up'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up">\n'
    h += '<a href="01-main-dashboard.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to dashboard\n</a>\n'
    h += '<div class="mb-6">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Create an account</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">Start your journey with a free account</p>\n</div>\n'
    h += social_buttons()
    h += '<div class="divider">or</div>\n'
    h += '<form id="register-form" novalidate onsubmit="return handleRegister(event)">\n'
    h += '<div class="grid grid-cols-2 gap-3">\n'
    h += text_field('first_name', 'First Name', 'John', 'given-name')
    h += text_field('last_name', 'Last Name', 'Doe', 'family-name')
    h += '</div>\n'
    h += email_field()
    h += password_field('password', 'Password', 'Create a password', True, True)
    h += password_field('confirm_password', 'Confirm Password', 'Confirm your password', True, False)
    h += '<div class="checkbox-wrapper mb-5">\n<input type="checkbox" id="terms" name="terms"/>\n<label for="terms" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">I agree to the <a href="#" class="link">Terms of Service</a> and <a href="#" class="link">Privacy Policy</a></label>\n</div>\n'
    h += '<button type="submit" class="btn-primary" id="register-btn">Create Account</button>\n'
    h += '</form>\n'
    h += '<p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5">Already have an account? <a href="81-auth-login.html" class="link">Sign in</a></p>\n'
    h += '</div>\n</div>\n'
    js = '''
function handleRegister(e){
  e.preventDefault();
  var fn=document.getElementById('first_name'),ln=document.getElementById('last_name'),em=document.getElementById('email'),pw=document.getElementById('password'),cpw=document.getElementById('confirm_password'),terms=document.getElementById('terms');
  var valid=true;
  if(!fn.value.trim()){showFieldError('first_name','First name is required');valid=false}else{clearFieldError('first_name')}
  if(!ln.value.trim()){showFieldError('last_name','Last name is required');valid=false}else{clearFieldError('last_name')}
  if(!validateEmail(em.value)){showFieldError('email','Please enter a valid email');valid=false}else{clearFieldError('email')}
  if(!pw.value||pw.value.length<8){showFieldError('password','Password must be at least 8 characters');valid=false}else{clearFieldError('password')}
  if(pw.value!==cpw.value){showFieldError('confirm_password','Passwords do not match');valid=false}else{clearFieldError('confirm_password')}
  if(!terms.checked){showToast('Please accept the terms and conditions','error');valid=false}
  if(valid){
    var btn=document.getElementById('register-btn');
    btn.disabled=true;btn.textContent='Creating account...';
    setTimeout(function(){btn.disabled=false;btn.textContent='Create Account';showToast('Account created! Please verify your email.','success');setTimeout(function(){window.location.href='85-auth-verify-email.html'},1500)},1200);
  }
  return false;
}
var pwInput=document.getElementById('password');
pwInput.addEventListener('input',function(){
  var v=this.value,s=0,bar=document.getElementById('password-strength'),txt=document.getElementById('password-strength-text');
  if(v.length>=8)s+=25;if(/[A-Z]/.test(v))s+=25;if(/[0-9]/.test(v))s+=25;if(/[^A-Za-z0-9]/.test(v))s+=25;
  bar.style.width=s+'%';
  if(s<=25){bar.style.background='#ef4444';txt.textContent='Weak password'}
  else if(s<=50){bar.style.background='#f97316';txt.textContent='Fair password'}
  else if(s<=75){bar.style.background='#eab308';txt.textContent='Good password'}
  else{bar.style.background='#22c55e';txt.textContent='Strong password'}
});
'''
    h += page_foot(js)
    return h

def gen_forgot_password():
    title = 'Forgot Password'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up" style="max-width:440px">\n'
    h += '<a href="81-auth-login.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to sign in\n</a>\n'
    # Illustration
    h += '<div class="auth-illustration mb-6">\n<svg width="120" height="120" viewBox="0 0 120 120" fill="none">\n<circle cx="60" cy="60" r="50" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/>\n<rect x="42" y="45" width="36" height="28" rx="4" fill="#6366f1"/>\n<path d="M50 58h20M50 64h12" stroke="#fff" stroke-width="2" stroke-linecap="round"/>\n<circle cx="60" cy="50" r="5" fill="#fff"/>\n<path d="M55 50l5-4 5 4" stroke="#6366f1" stroke-width="1.5" fill="none"/>\n</svg>\n</div>\n'
    h += '<div class="mb-6 text-center">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Forgot password?</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">No worries, we\'ll send you reset instructions</p>\n</div>\n'
    h += '<form id="forgot-form" novalidate onsubmit="return handleForgot(event)">\n'
    h += email_field()
    h += '<button type="submit" class="btn-primary" id="forgot-btn">Send Reset Link</button>\n'
    h += '</form>\n'
    # Success state (hidden)
    h += '<div id="forgot-success" class="text-center" style="display:none">\n<div class="auth-illustration mb-4">\n<svg width="64" height="64" viewBox="0 0 64 64" fill="none">\n<circle cx="32" cy="32" r="30" fill="#dcfce7"/>\n<path d="M20 32l8 8 16-16" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n</div>\n<h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-1">Check your email</h2>\n<p class="text-sm text-slate-500 dark:text-slate-400 mb-4">We sent a password reset link to <span id="sent-email" class="font-medium text-slate-700 dark:text-slate-300"></span></p>\n<button type="button" class="btn-outline" onclick="showToast(\'Another reset link sent!\',\'success\')">Resend email</button>\n</div>\n'
    h += '<p class="text-center text-sm text-slate-500 dark:text-slate-400 mt-5"><a href="81-auth-login.html" class="link">Back to sign in</a></p>\n'
    h += '</div>\n</div>\n'
    js = '''
function handleForgot(e){
  e.preventDefault();
  var em=document.getElementById('email');
  if(!validateEmail(em.value)){showFieldError('email','Please enter a valid email');return false}
  clearFieldError('email');
  var btn=document.getElementById('forgot-btn');
  btn.disabled=true;btn.textContent='Sending...';
  setTimeout(function(){
    document.getElementById('forgot-form').style.display='none';
    document.getElementById('forgot-success').style.display='block';
    document.getElementById('sent-email').textContent=em.value;
    showToast('Reset link sent to your email','success');
  },1200);
  return false;
}
'''
    h += page_foot(js)
    return h

def gen_reset_password():
    title = 'Reset Password'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up" style="max-width:440px">\n'
    h += '<a href="81-auth-login.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to sign in\n</a>\n'
    h += '<div class="auth-illustration mb-6">\n<svg width="100" height="100" viewBox="0 0 100 100" fill="none">\n<circle cx="50" cy="50" r="40" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>\n<path d="M50 30v25" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>\n<circle cx="50" cy="65" r="3" fill="#f59e0b"/>\n<rect x="35" y="55" width="30" height="20" rx="4" fill="#f59e0b"/>\n<path d="M42 62h16M42 67h10" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/>\n</svg>\n</div>\n'
    h += '<div class="mb-6 text-center">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Set new password</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">Your new password must be different from previous passwords</p>\n</div>\n'
    h += '<form id="reset-form" novalidate onsubmit="return handleReset(event)">\n'
    h += password_field('new_password', 'New Password', 'Enter new password', True, True)
    h += password_field('confirm_new_password', 'Confirm New Password', 'Confirm new password', True, False)
    h += '<div class="checkbox-wrapper mb-5">\n<input type="checkbox" id="sign_out_all" name="sign_out_all" checked/>\n<label for="sign_out_all" class="text-sm text-slate-600 dark:text-slate-400 cursor-pointer">Sign out of all other sessions</label>\n</div>\n'
    h += '<button type="submit" class="btn-primary" id="reset-btn">Reset Password</button>\n'
    h += '</form>\n'
    h += '</div>\n</div>\n'
    js = '''
function handleReset(e){
  e.preventDefault();
  var pw=document.getElementById('new_password'),cpw=document.getElementById('confirm_new_password');
  var valid=true;
  if(!pw.value||pw.value.length<8){showFieldError('new_password','Password must be at least 8 characters');valid=false}else{clearFieldError('new_password')}
  if(pw.value!==cpw.value){showFieldError('confirm_new_password','Passwords do not match');valid=false}else{clearFieldError('confirm_new_password')}
  if(valid){
    var btn=document.getElementById('reset-btn');
    btn.disabled=true;btn.textContent='Resetting...';
    setTimeout(function(){showToast('Password reset successfully!','success');setTimeout(function(){window.location.href='81-auth-login.html'},1500)},1200);
  }
  return false;
}
var pwInput=document.getElementById('new_password');
pwInput.addEventListener('input',function(){
  var v=this.value,s=0,bar=document.getElementById('new_password-strength'),txt=document.getElementById('new_password-strength-text');
  if(v.length>=8)s+=25;if(/[A-Z]/.test(v))s+=25;if(/[0-9]/.test(v))s+=25;if(/[^A-Za-z0-9]/.test(v))s+=25;
  bar.style.width=s+'%';
  if(s<=25){bar.style.background='#ef4444';txt.textContent='Weak password'}
  else if(s<=50){bar.style.background='#f97316';txt.textContent='Fair password'}
  else if(s<=75){bar.style.background='#eab308';txt.textContent='Good password'}
  else{bar.style.background='#22c55e';txt.textContent='Strong password'}
});
'''
    h += page_foot(js)
    return h

def gen_verify_email():
    title = 'Verify Email'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up" style="max-width:440px">\n'
    h += '<div class="auth-illustration mb-6">\n<svg width="100" height="100" viewBox="0 0 100 100" fill="none">\n<circle cx="50" cy="50" r="40" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/>\n<rect x="25" y="35" width="50" height="35" rx="4" fill="#6366f1"/>\n<path d="M25 39l25 17 25-17" stroke="#818cf8" stroke-width="2" fill="none"/>\n<circle cx="72" cy="35" r="12" fill="#22c55e"/>\n<path d="M67 35l3 3 6-6" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n</div>\n'
    h += '<div class="mb-6 text-center">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Verify your email</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">We\'ve sent a 6-digit code to <span class="font-medium text-slate-700 dark:text-slate-300">john@example.com</span></p>\n</div>\n'
    h += '<form id="verify-form" novalidate onsubmit="return handleVerify(event)">\n'
    h += otp_section(6)
    h += '<button type="submit" class="btn-primary mt-4" id="verify-btn">Verify Email</button>\n'
    h += '</form>\n'
    h += '<div class="text-center mt-5">\n<p class="text-sm text-slate-500 dark:text-slate-400">Didn\'t receive the code? <button type="button" class="link" id="resend-btn" onclick="handleResend()">Resend</button></p>\n<p class="text-xs text-slate-400 dark:text-slate-500 mt-1" id="resend-timer"></p>\n</div>\n'
    h += '</div>\n</div>\n'
    js = '''
initOtpInputs();
var resendCooldown=0;
function handleVerify(e){
  e.preventDefault();
  var inputs=document.querySelectorAll('.otp-input');
  var code='';inputs.forEach(function(i){code+=i.value});
  if(code.length<6){document.getElementById('otp-error').textContent='Please enter all 6 digits';document.getElementById('otp-error').classList.add('visible');return false}
  document.getElementById('otp-error').classList.remove('visible');
  var btn=document.getElementById('verify-btn');
  btn.disabled=true;btn.textContent='Verifying...';
  setTimeout(function(){btn.disabled=false;btn.textContent='Verify Email';showToast('Email verified successfully!','success');setTimeout(function(){window.location.href='01-main-dashboard.html'},1500)},1200);
  return false;
}
function handleResend(){
  if(resendCooldown>0)return;
  showToast('New verification code sent!','success');
  resendCooldown=60;
  var btn=document.getElementById('resend-btn');
  btn.style.opacity='0.5';btn.style.pointerEvents='none';
  var timer=document.getElementById('resend-timer');
  var iv=setInterval(function(){
    resendCooldown--;
    timer.textContent='Resend available in '+resendCooldown+'s';
    if(resendCooldown<=0){clearInterval(iv);btn.style.opacity='1';btn.style.pointerEvents='auto';timer.textContent=''}
  },1000);
}
'''
    h += page_foot(js)
    return h

def gen_2fa():
    title = 'Two-Step Verification'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up" style="max-width:440px">\n'
    h += '<a href="81-auth-login.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to sign in\n</a>\n'
    h += '<div class="auth-illustration mb-6">\n<svg width="100" height="100" viewBox="0 0 100 100" fill="none">\n<circle cx="50" cy="50" r="40" fill="#f0fdf4" stroke="#22c55e" stroke-width="2"/>\n<rect x="38" y="30" width="24" height="30" rx="4" fill="#22c55e"/>\n<circle cx="50" cy="42" r="4" fill="#fff"/>\n<path d="M46 50h8" stroke="#fff" stroke-width="2" stroke-linecap="round"/>\n<path d="M42 60l8 8 16-16" stroke="#16a34a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>\n</svg>\n</div>\n'
    h += '<div class="mb-6 text-center">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Two-factor authentication</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">Enter the 6-digit code from your authenticator app</p>\n</div>\n'
    h += '<form id="twofa-form" novalidate onsubmit="return handle2FA(event)">\n'
    h += otp_section(6)
    h += '<button type="submit" class="btn-primary mt-4" id="twofa-btn">Verify</button>\n'
    h += '</form>\n'
    h += '<div class="divider">or</div>\n'
    h += '<div class="text-center space-y-3">\n<button type="button" class="btn-outline" onclick="showToast(\'Recovery code mode activated\',\'info\')">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inline mr-1"><path d="M9 12h6M12 9v6M3 12a9 9 0 1018 0 9 9 0 00-18 0z"/></svg>\nUse recovery code\n</button>\n<p class="text-sm text-slate-500 dark:text-slate-400">Having trouble? <a href="#" class="link">Contact support</a></p>\n</div>\n'
    h += '</div>\n</div>\n'
    js = '''
initOtpInputs();
function handle2FA(e){
  e.preventDefault();
  var inputs=document.querySelectorAll('.otp-input');
  var code='';inputs.forEach(function(i){code+=i.value});
  if(code.length<6){document.getElementById('otp-error').textContent='Please enter all 6 digits';document.getElementById('otp-error').classList.add('visible');return false}
  document.getElementById('otp-error').classList.remove('visible');
  var btn=document.getElementById('twofa-btn');
  btn.disabled=true;btn.textContent='Verifying...';
  setTimeout(function(){btn.disabled=false;btn.textContent='Verify';showToast('2FA verified! Redirecting...','success');setTimeout(function(){window.location.href='01-main-dashboard.html'},1500)},1200);
  return false;
}
'''
    h += page_foot(js)
    return h

def gen_sso():
    title = 'SSO Login'
    h = page_head(title)
    h += '<body class="bg-slate-50 dark:bg-slate-950 dark:text-white">\n'
    h += '<div class="auth-wrapper p-4 sm:p-6">\n'
    h += '<div class="auth-card fade-up" style="max-width:520px">\n'
    h += '<a href="01-main-dashboard.html" class="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-600 dark:hover:text-slate-300 mb-6 transition-colors">\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>\nBack to dashboard\n</a>\n'
    h += '<div class="mb-6 text-center">\n<h1 class="text-2xl font-bold text-slate-900 dark:text-white mb-1">Sign in with SSO</h1>\n<p class="text-sm text-slate-500 dark:text-slate-400">Use your organization\'s identity provider to sign in</p>\n</div>\n'
    # SSO providers
    h += '<div class="space-y-3 mb-6">\n'
    # Okta
    h += '<button type="button" class="btn-outline flex items-center gap-3" onclick="handleSSO(\'Okta\')">\n<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="4" stroke="#0076CE" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="#0076CE"/></svg>\n<span class="flex-1 text-left">Continue with Okta</span>\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>\n</button>\n'
    # Azure AD
    h += '<button type="button" class="btn-outline flex items-center gap-3" onclick="handleSSO(\'Azure AD\')">\n<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="4" stroke="#00a4ef" stroke-width="2"/><path d="M11 7l-5 5 5 5M13 7l5 5-5 5" stroke="#00a4ef" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>\n<span class="flex-1 text-left">Continue with Azure AD</span>\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>\n</button>\n'
    # Google Workspace
    h += '<button type="button" class="btn-outline flex items-center gap-3" onclick="handleSSO(\'Google Workspace\')">\n<svg width="20" height="20" viewBox="0 0 18 18" fill="none"><path d="M17.64 9.2c0-.74-.07-1.45-.2-2.13H9v4.03h4.87a4.16 4.16 0 01-1.8 2.73v2.27h2.91c1.7-1.57 2.66-3.88 2.66-6.9z" fill="#4285F4"/><path d="M9 18c2.43 0 4.47-.8 5.96-2.17l-2.91-2.27c-.8.54-1.83.86-3.05.86-2.35 0-4.34-1.58-5.05-3.71H.96v2.34A8.99 8.99 0 009 18z" fill="#34A853"/><path d="M3.95 10.71A5.4 5.4 0 013.67 9c0-.6.1-1.17.28-1.71V4.95H.96A8.99 8.99 0 000 9c0 1.45.35 2.82.96 4.05l2.99-2.34z" fill="#FBBC05"/><path d="M9 3.58c1.32 0 2.51.45 3.44 1.35l2.58-2.59C13.46.89 11.43 0 9 0 5.48 0 2.47 2.02.96 4.95l2.99 2.34C4.66 5.16 6.65 3.58 9 3.58z" fill="#EB4335"/></svg>\n<span class="flex-1 text-left">Continue with Google Workspace</span>\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>\n</button>\n'
    # SAML
    h += '<button type="button" class="btn-outline flex items-center gap-3" onclick="handleSSO(\'SAML\')">\n<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="4" stroke="#6366f1" stroke-width="2"/><path d="M8 12h8M12 8v8" stroke="#6366f1" stroke-width="2" stroke-linecap="round"/></svg>\n<span class="flex-1 text-left">Continue with SAML</span>\n<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>\n</button>\n'
    h += '</div>\n'
    # Domain-based SSO
    h += '<div class="divider">or enter your company domain</div>\n'
    h += '<form id="sso-form" novalidate onsubmit="return handleDomainSSO(event)">\n'
    h += text_field('company_domain', 'Company Domain', 'acme-corp', 'organization')
    h += '<button type="submit" class="btn-primary" id="sso-btn">Continue with SSO</button>\n'
    h += '</form>\n'
    h += '<div class="divider">or</div>\n'
    h += '<div class="text-center">\n<a href="81-auth-login.html" class="link">Sign in with email and password</a>\n</div>\n'
    h += '<p class="text-center text-xs text-slate-400 dark:text-slate-500 mt-5">By continuing, you agree to our <a href="#" class="link text-xs">Terms</a> and <a href="#" class="link text-xs">Privacy Policy</a></p>\n'
    h += '</div>\n</div>\n'
    js = '''
function handleSSO(provider){
  showToast('Redirecting to '+provider+'...','info');
  setTimeout(function(){showToast(provider+' authentication successful!','success');setTimeout(function(){window.location.href='01-main-dashboard.html'},1000)},1500);
}
function handleDomainSSO(e){
  e.preventDefault();
  var domain=document.getElementById('company_domain');
  if(!domain.value.trim()||!domain.value.trim().match(/^[a-z0-9-]+$/i)){showFieldError('company_domain','Please enter a valid company domain');return false}
  clearFieldError('company_domain');
  var btn=document.getElementById('sso-btn');
  btn.disabled=true;btn.textContent='Connecting...';
  setTimeout(function(){showToast('Redirecting to SSO portal for '+domain.value.trim()+'...','info');setTimeout(function(){window.location.href='01-main-dashboard.html'},1500)},1200);
  return false;
}
'''
    h += page_foot(js)
    return h

# Generate all auth pages
pages = [
    ('81-auth-login.html', gen_login),
    ('82-auth-register.html', gen_register),
    ('83-auth-forgot-password.html', gen_forgot_password),
    ('84-auth-reset-password.html', gen_reset_password),
    ('85-auth-verify-email.html', gen_verify_email),
    ('86-auth-2fa.html', gen_2fa),
    ('87-auth-sso.html', gen_sso),
]

print('Generating premium auth pages...')
for fname, gen_fn in pages:
    path = os.path.join(OUT, fname)
    html = gen_fn()
    with open(path, 'w') as f:
        f.write(html)
    sz = os.path.getsize(path)
    print('  ' + fname + ': ' + str(sz // 1024) + 'KB')

print('Done! All auth pages generated.')
