// Main JavaScript file for SmartCareer

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize form validations
    initFormValidations();
    
    // Initialize animations
    initAnimations();
}

// Smooth Scroll Behavior with throttling for performance
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Throttle scroll events for better performance
    let ticking = false;
    
    function updateScrollPosition() {
        // Any scroll-related updates can go here
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateScrollPosition);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
}

// Form Validations
function initFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else if (input.type === 'email' && !isValidEmail(input.value)) {
            showError(input, 'Please enter a valid email');
            isValid = false;
        }
    });
    
    return isValid;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showError(element, message) {
    element.classList.add('border-red-500');
    element.parentElement.classList.add('text-red-500');
    
    let errorDiv = element.parentElement.querySelector('.error-message');
    if (!errorDiv) {
        errorDiv = document.createElement('p');
        errorDiv.className = 'error-message text-red-500 text-sm mt-1';
        element.parentElement.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

function clearError(element) {
    element.classList.remove('border-red-500');
    element.parentElement.classList.remove('text-red-500');
    
    const errorDiv = element.parentElement.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Tooltip Initialization
function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'fixed bg-gray-900 text-white px-3 py-2 rounded text-sm z-50';
            tooltip.textContent = this.getAttribute('data-tooltip');
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - 40) + 'px';
            
            document.body.appendChild(tooltip);
            
            this.addEventListener('mouseleave', function() {
                tooltip.remove();
            });
        });
    });
}

// Animation Utilities
// Performance-optimized animation initialization
function initAnimations() {
    // Use a more efficient Intersection Observer with better performance settings
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                // Stop observing this element to improve performance
                observer.unobserve(entry.target);
            }
        });
    }, {
        // Performance optimization options
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    });
    
    // Only observe elements that are close to the viewport
    document.querySelectorAll('[data-animate]').forEach(el => {
        observer.observe(el);
    });
    
    // Initialize service card animations if on career services page
    initServiceCardAnimations();
}

// Service card animations for career services page
function initServiceCardAnimations() {
    // Check if we're on the career services page
    if (!document.querySelector('.service-card')) return;
    
    // Use Intersection Observer for scroll-triggered animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -100px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add staggered delays
                const delay = index * 150;
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.classList.add(`card-${entry.target.id.slice(-1)}`);
                    
                    // Add floating animation after entrance
                    setTimeout(() => {
                        entry.target.classList.add('animate-float');
                    }, 600);
                }, delay);
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all service cards
    document.querySelectorAll('.service-card').forEach(card => {
        observer.observe(card);
    });

    // 3D Tilt Effect
    document.querySelectorAll('.service-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const cardRect = card.getBoundingClientRect();
            const cardCenterX = cardRect.left + cardRect.width / 2;
            const cardCenterY = cardRect.top + cardRect.height / 2;
            
            const mouseX = e.clientX - cardCenterX;
            const mouseY = e.clientY - cardCenterY;
            
            const rotateY = (mouseX / cardRect.width) * 10;
            const rotateX = -(mouseY / cardRect.height) * 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
}

// Utility Functions
function formatCurrency(value) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(value);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function getInitials(name) {
    return name
        .split(' ')
        .map(word => word[0])
        .join('')
        .toUpperCase();
}

function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Session Management
function setSessionItem(key, value) {
    sessionStorage.setItem(key, JSON.stringify(value));
}

function getSessionItem(key) {
    const item = sessionStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}

function removeSessionItem(key) {
    sessionStorage.removeItem(key);
}

// Local Storage Management
function setLocalItem(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

function getLocalItem(key) {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}

function removeLocalItem(key) {
    localStorage.removeItem(key);
}

// Toast Notifications
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    const bgColor = {
        'success': 'bg-green-500',
        'error': 'bg-red-500',
        'warning': 'bg-yellow-500',
        'info': 'bg-blue-500'
    }[type] || 'bg-blue-500';
    
    toast.className = `fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, duration);
}

// API Request Helper
async function apiRequest(endpoint, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    try {
        const response = await fetch(endpoint, {
            ...defaultOptions,
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showToast('An error occurred. Please try again.', 'error');
        throw error;
    }
}

// Responsive Utilities
function isMobile() {
    return window.innerWidth < 768;
}

function isTablet() {
    return window.innerWidth >= 768 && window.innerWidth < 1024;
}

function isDesktop() {
    return window.innerWidth >= 1024;
}

// Event Listeners for Global Features
document.addEventListener('input', function(e) {
    if (e.target.hasAttribute('required')) {
        clearError(e.target);
    }
});

// Handle visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'visible') {
        console.log('User is back to the page');
    } else {
        console.log('User left the page');
    }
});

// Version
console.log('SmartCareer v1.0.0 loaded');
