/**
 * AI Meal Planner Pro - Modern UI Utilities
 * Shared functions and components for the new modern UI
 */

// ===== NOTIFICATIONS SYSTEM =====
const Toast = {
    show(message, type = 'info', duration = 3000) {
        const toastContainer = document.getElementById('toastContainer') || this.createContainer();
        const toast = document.createElement('div');
        const icons = {
            'success': '✓',
            'error': '✕',
            'info': 'ℹ',
            'warning': '⚠'
        };

        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${icons[type]}</span>
            <span class="toast-message">${message}</span>
            <button class="toast-close">&times;</button>
        `;

        toastContainer.appendChild(toast);
        toast.style.animation = 'slideInRight 0.3s ease-out';

        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            toast.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        });

        if (duration > 0) {
            setTimeout(() => {
                toast.style.animation = 'slideOutRight 0.3s ease-in';
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }
    },

    createContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 400px;
        `;
        document.body.appendChild(container);
        return container;
    },

    success(message, duration = 3000) {
        this.show(message, 'success', duration);
    },

    error(message, duration = 5000) {
        this.show(message, 'error', duration);
    },

    info(message, duration = 3000) {
        this.show(message, 'info', duration);
    },

    warning(message, duration = 4000) {
        this.show(message, 'warning', duration);
    }
};

// ===== LOADING STATES =====
const Loader = {
    show() {
        let loader = document.getElementById('globalLoader');
        if (!loader) {
            loader = document.createElement('div');
            loader.id = 'globalLoader';
            loader.innerHTML = `
                <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
                    <div class="spinner" style="
                        width: 50px;
                        height: 50px;
                        border: 4px solid rgba(102, 126, 234, 0.2);
                        border-top-color: #667eea;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    "></div>
                    <p style="color: rgba(241, 245, 249, 0.7);">Loading...</p>
                </div>
            `;
            loader.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(15, 23, 42, 0.8);
                backdrop-filter: blur(5px);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
            `;
            document.body.appendChild(loader);
        }
        loader.style.display = 'flex';
    },

    hide() {
        const loader = document.getElementById('globalLoader');
        if (loader) {
            loader.style.display = 'none';
        }
    }
};

// ===== API UTILITIES =====
const API = {
    baseURL: '',

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaults = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const config = { ...defaults, ...options };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: error.message };
        }
    },

    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    },

    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
};

// ===== FORM VALIDATION =====
const Validator = {
    validate(form) {
        const errors = [];
        const inputs = form.querySelectorAll('[data-validate]');

        inputs.forEach(input => {
            const rules = input.getAttribute('data-validate').split('|');
            rules.forEach(rule => {
                if (!this.checkRule(input, rule)) {
                    errors.push(`${input.name}: ${rule} validation failed`);
                }
            });
        });

        return errors;
    },

    checkRule(input, rule) {
        const value = input.value.trim();

        if (rule === 'required') {
            return value.length > 0;
        }
        if (rule === 'email') {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        }
        if (rule === 'minlength:8') {
            return value.length >= 8;
        }
        if (rule === 'number') {
            return !isNaN(value);
        }
        if (rule === 'url') {
            try {
                new URL(value);
                return true;
            } catch {
                return false;
            }
        }
        return true;
    }
};

// ===== ANIMATION UTILITIES =====
const Animations = {
    fadeIn(element, duration = 600) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease-out`;
        element.offsetHeight; // Trigger reflow
        element.style.opacity = '1';
    },

    slideUp(element, duration = 600) {
        element.style.transform = 'translateY(20px)';
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ease-out`;
        element.offsetHeight; // Trigger reflow
        element.style.transform = 'translateY(0)';
        element.style.opacity = '1';
    },

    slideDown(element, duration = 600) {
        element.style.transform = 'translateY(-20px)';
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ease-out`;
        element.offsetHeight; // Trigger reflow
        element.style.transform = 'translateY(0)';
        element.style.opacity = '1';
    },

    scale(element, duration = 600) {
        element.style.transform = 'scale(0.9)';
        element.style.opacity = '0';
        element.style.transition = `all ${duration}ms ease-out`;
        element.offsetHeight; // Trigger reflow
        element.style.transform = 'scale(1)';
        element.style.opacity = '1';
    }
};

// ===== DOM UTILITIES =====
const DOM = {
    query(selector) {
        return document.querySelector(selector);
    },

    queryAll(selector) {
        return document.querySelectorAll(selector);
    },

    create(tag, className = '', innerHTML = '') {
        const element = document.createElement(tag);
        if (className) element.className = className;
        if (innerHTML) element.innerHTML = innerHTML;
        return element;
    },

    addClass(element, className) {
        element.classList.add(className);
    },

    removeClass(element, className) {
        element.classList.remove(className);
    },

    toggleClass(element, className) {
        element.classList.toggle(className);
    },

    hide(element) {
        element.style.display = 'none';
    },

    show(element) {
        element.style.display = 'block';
    },

    remove(element) {
        element.remove();
    }
};

// ===== STORAGE UTILITIES =====
const Storage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },

    get(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Storage error:', error);
            return null;
        }
    },

    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    },

    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Storage error:', error);
            return false;
        }
    }
};

// ===== DATE UTILITIES =====
const DateUtils = {
    format(date, format = 'MMM DD, YYYY') {
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const d = new Date(date);
        
        return format
            .replace('YYYY', d.getFullYear())
            .replace('MM', String(d.getMonth() + 1).padStart(2, '0'))
            .replace('MMM', months[d.getMonth()])
            .replace('DD', String(d.getDate()).padStart(2, '0'))
            .replace('HH', String(d.getHours()).padStart(2, '0'))
            .replace('mm', String(d.getMinutes()).padStart(2, '0'));
    },

    today() {
        return new Date().toISOString().split('T')[0];
    },

    addDays(date, days) {
        const d = new Date(date);
        d.setDate(d.getDate() + days);
        return d;
    },

    isToday(date) {
        return this.format(date, 'YYYY-MM-DD') === this.today();
    }
};

// ===== DEBOUNCE & THROTTLE =====
function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

function throttle(func, delay) {
    let lastCall = 0;
    return function (...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            func(...args);
        }
    };
}

// ===== INJECT TOAST STYLES =====
const toastStyles = `
<style>
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    .toast {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 20px;
        background: rgba(26, 40, 71, 0.9);
        border: 1px solid rgba(100, 116, 139, 0.3);
        border-radius: 8px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        color: #f1f5f9;
        font-size: 14px;
        font-weight: 500;
    }

    .toast-icon {
        font-weight: 700;
        font-size: 16px;
    }

    .toast-success {
        border-left: 3px solid #10b981;
    }

    .toast-success .toast-icon {
        color: #10b981;
    }

    .toast-error {
        border-left: 3px solid #ef4444;
    }

    .toast-error .toast-icon {
        color: #ef4444;
    }

    .toast-info {
        border-left: 3px solid #667eea;
    }

    .toast-info .toast-icon {
        color: #667eea;
    }

    .toast-warning {
        border-left: 3px solid #f59e0b;
    }

    .toast-warning .toast-icon {
        color: #f59e0b;
    }

    .toast-close {
        margin-left: auto;
        background: none;
        border: none;
        color: inherit;
        cursor: pointer;
        font-size: 20px;
        padding: 0;
        opacity: 0.7;
        transition: opacity 0.2s;
    }

    .toast-close:hover {
        opacity: 1;
    }

    @media (max-width: 480px) {
        #toastContainer {
            right: 10px !important;
            left: 10px !important;
            max-width: none !important;
        }

        .toast {
            font-size: 13px;
            padding: 10px 16px;
        }
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
`;

if (document.readyState !== 'loading') {
    document.head.insertAdjacentHTML('beforeend', toastStyles);
} else {
    document.addEventListener('DOMContentLoaded', () => {
        document.head.insertAdjacentHTML('beforeend', toastStyles);
    });
}

// ===== EXPORT FOR MODULAR USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Toast, Loader, API, Validator, Animations, DOM, Storage, DateUtils, debounce, throttle };
}
