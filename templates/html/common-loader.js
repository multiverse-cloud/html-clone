// Common loader utilities for the static HTML bundle.
// Provides shared helper functions used across component showcase pages.
(function () {
  'use strict';

  // ===== Escape HTML for source display =====
  window.escapeHtml = function (str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  };

  // ===== Copy to clipboard with toast =====
  window.copySourceCode = function (sourceId) {
    var el = document.querySelector('[data-source-id="' + sourceId + '"]');
    if (!el) return;
    var code = el.getAttribute('data-source-code') || el.innerHTML;
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(code.trim()).then(function () {
        if (window.showToast) window.showToast('Source code copied to clipboard');
      });
    } else {
      var textarea = document.createElement('textarea');
      textarea.value = code.trim();
      textarea.style.position = 'fixed';
      textarea.style.left = '-9999px';
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        if (window.showToast) window.showToast('Source code copied to clipboard');
      } catch (e) {
        if (window.showToast) window.showToast('Copy failed — please copy manually');
      }
      document.body.removeChild(textarea);
    }
  };

  // ===== Source Code Viewer Panel =====
  window.openSourceViewer = function (sourceId) {
    var item = document.querySelector('[data-source-id="' + sourceId + '"]');
    if (!item) return;

    var existingPanel = document.getElementById('source-viewer-panel');
    if (existingPanel) existingPanel.remove();

    var sourceCode = item.getAttribute('data-source-code') || item.innerHTML;
    var panel = document.createElement('div');
    panel.id = 'source-viewer-panel';
    panel.className = 'source-viewer-overlay';
    panel.innerHTML =
      '<div class="source-viewer-backdrop" onclick="closeSourceViewer()"></div>' +
      '<div class="source-viewer-container">' +
        '<div class="source-viewer-header">' +
          '<div>' +
            '<h3 class="source-viewer-title">Source Code</h3>' +
            '<p class="source-viewer-subtitle">' + escapeHtml(sourceId) + '</p>' +
          '</div>' +
          '<div class="source-viewer-actions">' +
            '<button type="button" class="source-viewer-copy-btn" onclick="copySourceCode(\'' + sourceId + '\')">' +
              '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>' +
              '<span>Copy</span>' +
            '</button>' +
            '<button type="button" class="source-viewer-close-btn" onclick="closeSourceViewer()">' +
              '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>' +
            '</button>' +
          '</div>' +
        '</div>' +
        '<pre class="source-viewer-code"><code>' + escapeHtml(sourceCode.trim()) + '</code></pre>' +
      '</div>';

    document.body.appendChild(panel);
    requestAnimationFrame(function () {
      panel.classList.add('is-open');
    });
  };

  window.closeSourceViewer = function () {
    var panel = document.getElementById('source-viewer-panel');
    if (!panel) return;
    panel.classList.remove('is-open');
    setTimeout(function () { panel.remove(); }, 250);
  };

  // ===== Tab Switching for Component Pages =====
  window.initComponentTabs = function (containerSelector) {
    var container = document.querySelector(containerSelector || '.component-tabs');
    if (!container) return;

    var tabs = container.querySelectorAll('[data-tab-target]');
    var panels = container.querySelectorAll('[data-tab-panel]');

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var target = tab.getAttribute('data-tab-target');
        tabs.forEach(function (t) {
          t.classList.remove('is-active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('is-active');
        tab.setAttribute('aria-selected', 'true');
        panels.forEach(function (panel) {
          if (panel.getAttribute('data-tab-panel') === target) {
            panel.classList.remove('hidden');
            panel.setAttribute('aria-hidden', 'false');
          } else {
            panel.classList.add('hidden');
            panel.setAttribute('aria-hidden', 'true');
          }
        });
      });
    });
  };

  // ===== Filter/Search for Component Lists =====
  window.initComponentSearch = function (inputSelector, itemSelector) {
    var input = document.querySelector(inputSelector || '#component-search');
    if (!input) return;

    input.addEventListener('input', function () {
      var query = input.value.toLowerCase().trim();
      var items = document.querySelectorAll(itemSelector || '[data-component-item]');
      items.forEach(function (item) {
        var text = item.textContent.toLowerCase();
        var keywords = (item.getAttribute('data-keywords') || '').toLowerCase();
        var match = !query || text.includes(query) || keywords.includes(query);
        item.style.display = match ? '' : 'none';
      });
    });
  };

  // ===== Category Filter for Component Pages =====
  window.initCategoryFilter = function (filterSelector, itemSelector) {
    var buttons = document.querySelectorAll(filterSelector || '[data-filter-category]');
    var items = document.querySelectorAll(itemSelector || '[data-component-item]');

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var category = btn.getAttribute('data-filter-category');
        buttons.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        items.forEach(function (item) {
          if (category === 'all' || item.getAttribute('data-category') === category) {
            item.style.display = '';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  };

  // ===== Toggle for live previews =====
  window.togglePreview = function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle('hidden');
  };

  // ===== OTP Input Behavior =====
  window.initOtpInputs = function (containerSelector) {
    var container = document.querySelector(containerSelector || '.otp-input-group');
    if (!container) return;

    var inputs = container.querySelectorAll('input');
    inputs.forEach(function (input, index) {
      input.addEventListener('input', function (e) {
        var value = e.target.value;
        if (value.length === 1 && index < inputs.length - 1) {
          inputs[index + 1].focus();
        }
      });
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Backspace' && !e.target.value && index > 0) {
          inputs[index - 1].focus();
        }
      });
      input.addEventListener('paste', function (e) {
        e.preventDefault();
        var data = e.clipboardData.getData('text').slice(0, inputs.length);
        data.split('').forEach(function (char, i) {
          if (inputs[i]) inputs[i].value = char;
        });
        var lastIndex = Math.min(data.length, inputs.length) - 1;
        if (lastIndex >= 0) inputs[lastIndex].focus();
      });
    });
  };

  // ===== Password Visibility Toggle =====
  window.togglePasswordVisibility = function (inputId, toggleId) {
    var input = document.getElementById(inputId);
    var toggle = document.getElementById(toggleId);
    if (!input || !toggle) return;

    var isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    toggle.innerHTML = isPassword
      ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>'
      : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>';
  };

  // ===== Form Validation Helpers =====
  window.validateEmail = function (email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  window.showFieldError = function (fieldId, message) {
    var field = document.getElementById(fieldId);
    if (!field) return;
    field.classList.add('border-red-500');
    var errorEl = field.parentElement.querySelector('.field-error');
    if (!errorEl) {
      errorEl = document.createElement('p');
      errorEl.className = 'field-error text-red-500 text-xs mt-1';
      field.parentElement.appendChild(errorEl);
    }
    errorEl.textContent = message;
  };

  window.clearFieldError = function (fieldId) {
    var field = document.getElementById(fieldId);
    if (!field) return;
    field.classList.remove('border-red-500');
    var errorEl = field.parentElement.querySelector('.field-error');
    if (errorEl) errorEl.remove();
  };

  // ===== Table Sorting =====
  window.initTableSort = function (tableSelector) {
    var table = document.querySelector(tableSelector || '.sortable-table');
    if (!table) return;

    var headers = table.querySelectorAll('th[data-sort]');
    headers.forEach(function (header) {
      header.style.cursor = 'pointer';
      header.addEventListener('click', function () {
        var col = parseInt(header.getAttribute('data-sort'));
        var tbody = table.querySelector('tbody');
        var rows = Array.from(tbody.querySelectorAll('tr'));
        var asc = header.getAttribute('data-sort-dir') !== 'asc';
        header.setAttribute('data-sort-dir', asc ? 'asc' : 'desc');

        rows.sort(function (a, b) {
          var aVal = a.cells[col] ? a.cells[col].textContent.trim() : '';
          var bVal = b.cells[col] ? b.cells[col].textContent.trim() : '';
          var aNum = parseFloat(aVal.replace(/[^0-9.-]/g, ''));
          var bNum = parseFloat(bVal.replace(/[^0-9.-]/g, ''));
          if (!isNaN(aNum) && !isNaN(bNum)) {
            return asc ? aNum - bNum : bNum - aNum;
          }
          return asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });

        rows.forEach(function (row) { tbody.appendChild(row); });
      });
    });
  };

  // ===== Bulk Selection for Tables =====
  window.initBulkSelect = function (tableSelector) {
    var table = document.querySelector(tableSelector || '.bulk-select-table');
    if (!table) return;

    var selectAll = table.querySelector('th input[type="checkbox"]');
    var rowChecks = table.querySelectorAll('tbody input[type="checkbox"]');
    var countEl = document.querySelector('.bulk-select-count');

    if (selectAll) {
      selectAll.addEventListener('change', function () {
        rowChecks.forEach(function (cb) { cb.checked = selectAll.checked; });
        updateCount();
      });
    }

    rowChecks.forEach(function (cb) {
      cb.addEventListener('change', updateCount);
    });

    function updateCount() {
      var checked = table.querySelectorAll('tbody input[type="checkbox"]:checked').length;
      if (countEl) countEl.textContent = checked > 0 ? checked + ' selected' : '';
    }
  };

  // ===== Accordion Toggle =====
  window.initAccordions = function () {
    document.querySelectorAll('.accordion-trigger').forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        var item = trigger.closest('.accordion-item');
        var content = item.querySelector('.accordion-body');
        var isOpen = item.classList.contains('is-open');

        // Close siblings
        var parent = item.parentElement;
        if (parent && parent.hasAttribute('data-single')) {
          parent.querySelectorAll('.accordion-item.is-open').forEach(function (openItem) {
            if (openItem !== item) {
              openItem.classList.remove('is-open');
              openItem.querySelector('.accordion-body').style.maxHeight = null;
            }
          });
        }

        item.classList.toggle('is-open');
        if (isOpen) {
          content.style.maxHeight = null;
        } else {
          content.style.maxHeight = content.scrollHeight + 'px';
        }
      });
    });
  };

  // ===== Modal Triggers =====
  window.openModal = function (modalId) {
    var modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('hidden');
    requestAnimationFrame(function () {
      modal.querySelector('.modal-backdrop').classList.add('opacity-100');
      modal.querySelector('.modal-content').classList.add('scale-100', 'opacity-100');
    });
  };

  window.closeModal = function (modalId) {
    var modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add('hidden');
  };

  // ===== Simple Chart Drawing (SVG-based, no external libs) =====
  window.drawSparkline = function (containerId, data, options) {
    var container = document.getElementById(containerId);
    if (!container || !data || data.length < 2) return;

    options = options || {};
    var width = options.width || container.offsetWidth || 120;
    var height = options.height || 40;
    var color = options.color || '#3b82f6';
    var fillOpacity = options.fillOpacity || 0.1;

    var max = Math.max.apply(null, data);
    var min = Math.min.apply(null, data);
    var range = max - min || 1;
    var step = width / (data.length - 1);

    var points = data.map(function (val, i) {
      var x = i * step;
      var y = height - ((val - min) / range) * (height - 4) - 2;
      return x + ',' + y;
    }).join(' ');

    var fillPoints = '0,' + height + ' ' + points + ' ' + width + ',' + height;

    container.innerHTML =
      '<svg width="' + width + '" height="' + height + '" viewBox="0 0 ' + width + ' ' + height + '">' +
        '<polygon points="' + fillPoints + '" fill="' + color + '" opacity="' + fillOpacity + '"/>' +
        '<polyline points="' + points + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' +
      '</svg>';
  };

  // ===== Draw bar chart (SVG) =====
  window.drawBarChart = function (containerId, data, options) {
    var container = document.getElementById(containerId);
    if (!container || !data || data.length === 0) return;

    options = options || {};
    var width = options.width || container.offsetWidth || 300;
    var height = options.height || 200;
    var barColor = options.barColor || '#3b82f6';
    var labelColor = options.labelColor || '#6b7280';

    var max = Math.max.apply(null, data.map(function (d) { return d.value; }));
    var barWidth = Math.min(40, (width - 20) / data.length - 8);
    var chartHeight = height - 30;
    var step = (width - 20) / data.length;

    var bars = data.map(function (d, i) {
      var barH = (d.value / max) * (chartHeight - 10);
      var x = 10 + i * step + (step - barWidth) / 2;
      var y = chartHeight - barH;
      return '<rect x="' + x + '" y="' + y + '" width="' + barWidth + '" height="' + barH + '" fill="' + (d.color || barColor) + '" rx="3">' +
        '<animate attributeName="height" from="0" to="' + barH + '" dur="0.6s" fill="freeze"/>' +
        '<animate attributeName="y" from="' + chartHeight + '" to="' + y + '" dur="0.6s" fill="freeze"/>' +
      '</rect>' +
      '<text x="' + (x + barWidth / 2) + '" y="' + (height - 5) + '" text-anchor="middle" fill="' + labelColor + '" font-size="10">' + d.label + '</text>';
    }).join('');

    container.innerHTML =
      '<svg width="' + width + '" height="' + height + '" viewBox="0 0 ' + width + ' ' + height + '">' + bars + '</svg>';
  };

  // ===== Draw donut chart (SVG) =====
  window.drawDonutChart = function (containerId, segments, options) {
    var container = document.getElementById(containerId);
    if (!container || !segments || segments.length === 0) return;

    options = options || {};
    var size = options.size || 160;
    var strokeWidth = options.strokeWidth || 28;
    var radius = (size - strokeWidth) / 2;
    var circumference = 2 * Math.PI * radius;
    var center = size / 2;

    var total = segments.reduce(function (sum, s) { return sum + s.value; }, 0);
    var offset = 0;

    var paths = segments.map(function (segment) {
      var percent = segment.value / total;
      var dashLength = percent * circumference;
      var dashOffset = -offset * circumference;
      offset += percent;

      return '<circle cx="' + center + '" cy="' + center + '" r="' + radius + '" ' +
        'fill="none" stroke="' + segment.color + '" stroke-width="' + strokeWidth + '" ' +
        'stroke-dasharray="' + dashLength + ' ' + (circumference - dashLength) + '" ' +
        'stroke-dashoffset="' + dashOffset + '" ' +
        'transform="rotate(-90 ' + center + ' ' + center + ')">' +
        '<animate attributeName="stroke-dasharray" from="0 ' + circumference + '" to="' + dashLength + ' ' + (circumference - dashLength) + '" dur="0.8s" fill="freeze"/>' +
      '</circle>';
    }).join('');

    var legend = segments.map(function (s) {
      return '<div class="flex items-center gap-2 text-xs"><span class="w-2.5 h-2.5 rounded-full flex-shrink-0" style="background:' + s.color + '"></span><span class="text-gray-600 dark:text-gray-400">' + s.label + '</span><span class="font-medium text-gray-900 dark:text-white">' + Math.round(s.value / total * 100) + '%</span></div>';
    }).join('');

    container.innerHTML =
      '<div class="flex items-center gap-6">' +
        '<div class="relative flex-shrink-0">' +
          '<svg width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '">' + paths + '</svg>' +
          '<div class="absolute inset-0 flex items-center justify-center">' +
            '<div class="text-center">' +
              '<p class="text-2xl font-bold text-gray-900 dark:text-white">' + (options.centerLabel || total.toLocaleString()) + '</p>' +
              (options.centerSublabel ? '<p class="text-xs text-gray-500">' + options.centerSublabel + '</p>' : '') +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="grid gap-2">' + legend + '</div>' +
      '</div>';
  };

  // ===== Animated Number Counter =====
  window.animateCounter = function (element, target, duration) {
    duration = duration || 800;
    var start = 0;
    var startTime = null;

    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var value = Math.floor(progress * target);
      element.textContent = value.toLocaleString();
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        element.textContent = target.toLocaleString();
      }
    }

    requestAnimationFrame(step);
  };

  // ===== Init on DOMContentLoaded =====
  document.addEventListener('DOMContentLoaded', function () {
    // Init accordions
    window.initAccordions();

    // Init component tabs
    window.initComponentTabs();

    // Init counters
    document.querySelectorAll('[data-counter-target]').forEach(function (el) {
      var target = parseInt(el.getAttribute('data-counter-target'));
      if (!isNaN(target) && target > 0) {
        window.animateCounter(el, target);
      }
    });

    // Init OTP inputs
    window.initOtpInputs();

    // Init table sorting
    window.initTableSort();

    // Init bulk select
    window.initBulkSelect();
  });

  // ===== Keyboard shortcut for source viewer =====
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      window.closeSourceViewer();
    }
  });
})();
