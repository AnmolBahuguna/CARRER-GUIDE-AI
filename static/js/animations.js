// Advanced 3D Effects and Scroll Animations
// GPU-accelerated animations using transform and opacity

(function() {
    'use strict';

    // ========== INTERSECTION OBSERVER FOR SCROLL ANIMATIONS ==========
    class ScrollAnimations {
        constructor() {
            this.observers = [];
            this.init();
        }

        init() {
            this.initScrollReveal();
            this.initParallax();
            this.init3DCards();
            this.initMagneticHover();
            this.initStaggeredAnimations();
            this.initScrollProgress();
        }

        // Scroll-triggered reveal animations
        initScrollReveal() {
            const observerOptions = {
                root: null,
                rootMargin: '0px 0px -100px 0px',
                threshold: 0.1
            };

            const revealObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        const animationType = element.dataset.animate || 'fade-up';
                        const delay = parseInt(element.dataset.delay) || 0;

                        setTimeout(() => {
                            element.classList.add('animate-in');
                            element.classList.add(`animate-${animationType}`);
                            revealObserver.unobserve(element);
                        }, delay);
                    }
                });
            }, observerOptions);

            // Observe all elements with data-animate attribute
            document.querySelectorAll('[data-animate]').forEach(el => {
                el.classList.add('animate-hidden');
                revealObserver.observe(el);
            });

            this.observers.push(revealObserver);
        }

        // Parallax scrolling effects
        initParallax() {
            const parallaxElements = document.querySelectorAll('[data-parallax]');
            
            if (parallaxElements.length === 0) return;

            const handleParallax = () => {
                const scrollTop = window.pageYOffset;
                
                parallaxElements.forEach(element => {
                    const speed = parseFloat(element.dataset.parallax) || 0.5;
                    const yPos = -(scrollTop * speed);
                    
                    // Use transform for GPU acceleration
                    element.style.transform = `translate3d(0, ${yPos}px, 0)`;
                });
            };

            // Throttled scroll handler
            let ticking = false;
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        handleParallax();
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        }

        // 3D card effects with tilt
        init3DCards() {
            const cards = document.querySelectorAll('[data-3d-card]');
            
            cards.forEach(card => {
                // Enable 3D perspective
                card.style.transformStyle = 'preserve-3d';
                card.style.perspective = '1000px';
                
                // Mouse move tilt effect
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    
                    const rotateX = (y - centerY) / 10;
                    const rotateY = (centerX - x) / 10;
                    
                    // GPU-accelerated transform
                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(20px)`;
                });
                
                card.addEventListener('mouseleave', () => {
                    card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
                });
            });
        }

        // Magnetic hover effect
        initMagneticHover() {
            const magneticElements = document.querySelectorAll('[data-magnetic]');
            
            magneticElements.forEach(element => {
                element.addEventListener('mousemove', (e) => {
                    const rect = element.getBoundingClientRect();
                    const x = e.clientX - rect.left - rect.width / 2;
                    const y = e.clientY - rect.top - rect.height / 2;
                    
                    const moveX = x * 0.3;
                    const moveY = y * 0.3;
                    
                    element.style.transform = `translate3d(${moveX}px, ${moveY}px, 0) scale(1.05)`;
                });
                
                element.addEventListener('mouseleave', () => {
                    element.style.transform = 'translate3d(0, 0, 0) scale(1)';
                });
            });
        }

        // Staggered animations for multiple items
        initStaggeredAnimations() {
            const containers = document.querySelectorAll('[data-stagger]');
            
            containers.forEach(container => {
                const items = container.querySelectorAll('[data-stagger-item]');
                const staggerDelay = parseInt(container.dataset.stagger) || 100;
                
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            items.forEach((item, index) => {
                                setTimeout(() => {
                                    item.classList.add('animate-in');
                                    item.style.opacity = '1';
                                    item.style.transform = 'translateY(0)';
                                }, index * staggerDelay);
                            });
                            observer.unobserve(container);
                        }
                    });
                }, { threshold: 0.1 });
                
                observer.observe(container);
            });
        }

        // Scroll progress indicator
        initScrollProgress() {
            const progressBar = document.querySelector('[data-scroll-progress]');
            if (!progressBar) return;
            
            const updateProgress = () => {
                const windowHeight = document.documentElement.scrollHeight - window.innerHeight;
                const scrolled = window.pageYOffset;
                const progress = (scrolled / windowHeight) * 100;
                
                progressBar.style.width = `${progress}%`;
            };
            
            window.addEventListener('scroll', () => {
                window.requestAnimationFrame(updateProgress);
            }, { passive: true });
        }
    }

    // ========== 3D CARD FLIP EFFECT ==========
    class CardFlip {
        constructor() {
            this.init();
        }

        init() {
            const flipCards = document.querySelectorAll('[data-flip-card]');
            
            flipCards.forEach(card => {
                card.addEventListener('click', () => {
                    card.classList.toggle('flipped');
                });
            });
        }
    }

    // ========== FLOATING ANIMATIONS ==========
    class FloatingElements {
        constructor() {
            this.init();
        }

        init() {
            const floatingElements = document.querySelectorAll('[data-float]');
            
            floatingElements.forEach((element, index) => {
                const duration = parseFloat(element.dataset.float) || 3;
                const delay = index * 0.2;
                
                element.style.animation = `float-3d ${duration}s ease-in-out infinite`;
                element.style.animationDelay = `${delay}s`;
            });
        }
    }

    // ========== SMOOTH PAGE ENTRANCE ==========
    class PageEntrance {
        constructor() {
            this.init();
        }

        init() {
            // Add entrance animation to body
            document.body.classList.add('page-loading');
            
            window.addEventListener('load', () => {
                setTimeout(() => {
                    document.body.classList.remove('page-loading');
                    document.body.classList.add('page-loaded');
                }, 100);
            });
        }
    }

    // ========== INITIALIZE ALL ANIMATIONS ==========
    document.addEventListener('DOMContentLoaded', () => {
        new ScrollAnimations();
        new CardFlip();
        new FloatingElements();
        new PageEntrance();
    });

    // ========== PERFORMANCE OPTIMIZATION ==========
    // Reduce motion for users who prefer it
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.style.setProperty('--animation-duration', '0.01ms');
    }

})();

