/**
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * TRINETRA - GLOBAL JS UTILITIES
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */

document.addEventListener('DOMContentLoaded', () => {
    init3DTiltEffect();
    initSplitFlapAnimations();
    initRippleEffect();
    initPageTransitions();
    initSessionTimer();
    
    // Fix for glitch-hover data-text
    document.querySelectorAll('.glitch-hover').forEach(el => {
        if (!el.getAttribute('data-text')) el.setAttribute('data-text', el.innerText);
    });
});

/**
 * 3D PERSPECTIVE TILT ON CARDS
 * Applies a slight 3D rotation based on mouse position.
 */
function init3DTiltEffect() {
    // 3D Tilt effect disabled as per user request to fix misbehavior on hover
    // const cards = document.querySelectorAll('.card-glass, .card-tilt');
    // cards.forEach(card => { ... });
}

/**
 * SPLIT-FLAP ANIMATION
 * Cycles characters like an airport departure board for elements with .split-flap class
 */
function initSplitFlapAnimations() {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    const elements = document.querySelectorAll('.split-flap');
    
    elements.forEach(el => {
        const finalValue = el.getAttribute('data-value') || el.innerText;
        el.innerText = '';
        
        let spans = [];
        for (let i = 0; i < finalValue.length; i++) {
            const span = document.createElement('span');
            span.innerText = chars[Math.floor(Math.random() * chars.length)];
            el.appendChild(span);
            spans.push({
                el: span,
                target: finalValue[i],
                cycles: Math.floor(Math.random() * 6) + 4 // 4 to 10 cycles
            });
        }
        
        let currentCycle = 0;
        const interval = setInterval(() => {
            let done = true;
            
            spans.forEach(item => {
                if (currentCycle < item.cycles) {
                    item.el.innerText = chars[Math.floor(Math.random() * chars.length)];
                    done = false;
                } else {
                    item.el.innerText = item.target;
                }
            });
            
            currentCycle++;
            if (done) clearInterval(interval);
        }, 60);
    });
}

/**
 * BUTTON RIPPLE EFFECT
 */
function initRippleEffect() {
    const buttons = document.querySelectorAll('.btn-cyber, .btn-primary');
    
    buttons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const circle = document.createElement('span');
            circle.style.position = 'absolute';
            circle.style.top = `${y}px`;
            circle.style.left = `${x}px`;
            circle.style.width = '2px';
            circle.style.height = '2px';
            circle.style.background = 'rgba(255, 255, 255, 0.4)';
            circle.style.borderRadius = '50%';
            circle.style.transform = 'translate(-50%, -50%)';
            circle.style.pointerEvents = 'none';
            circle.style.transition = 'width 0.6s ease-out, height 0.6s ease-out, opacity 0.6s ease-out';
            circle.style.zIndex = '0';
            
            this.appendChild(circle);
            
            // Trigger animation
            setTimeout(() => {
                circle.style.width = '300px';
                circle.style.height = '300px';
                circle.style.opacity = '0';
            }, 10);
            
            setTimeout(() => {
                circle.remove();
            }, 600);
        });
    });
}

/**
 * MORSE CODE PAGE TRANSITION
 * Intercepts links and shows a brief overlay before navigating.
 */
function initPageTransitions() {
    // Create the overlay container
    const overlay = document.createElement('div');
    overlay.id = 'morse-overlay';
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100vw';
    overlay.style.height = '100vh';
    overlay.style.backgroundColor = 'var(--clr-bg)';
    overlay.style.zIndex = '999999';
    overlay.style.display = 'flex';
    overlay.style.flexDirection = 'column';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.style.opacity = '0';
    overlay.style.pointerEvents = 'none';
    overlay.style.transition = 'opacity 0.15s ease';
    
    overlay.innerHTML = `
        <div style="font-family: var(--font-data); color: var(--clr-cyan); font-size: 24px; letter-spacing: 4px;" id="morse-text"></div>
        <div style="width: 200px; height: 1px; background: rgba(0,240,255,0.2); margin-top: 20px; position: relative; overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; height: 100%; width: 50%; background: var(--clr-cyan); animation: scanLine 0.5s linear infinite;"></div>
        </div>
        <style>@keyframes scanLine { 0% { left: -50%; } 100% { left: 100%; } }</style>
    `;
    
    document.body.appendChild(overlay);
    
    // Intercept links
    document.querySelectorAll('a').forEach(link => {
        if (link.hostname === window.location.hostname && !link.target && !link.href.includes('#')) {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const url = link.href;
                
                // Show overlay
                overlay.style.opacity = '1';
                overlay.style.pointerEvents = 'all';
                
                // Random morse pattern
                const morse = '-. . ..- .-. .- .-.. / .-.. .. -. -.- / . ... - .- -... .-.. .. ... .... . -..';
                let idx = 0;
                const textEl = document.getElementById('morse-text');
                
                const interval = setInterval(() => {
                    textEl.innerText += morse[idx] || '';
                    idx++;
                }, 10);
                
                setTimeout(() => {
                    clearInterval(interval);
                    window.location.href = url;
                }, 300);
            });
        }
    });
}

/**
 * SESSION TIMER
 * Counts down from the server-provided session expiry time
 */
function initSessionTimer() {
    const timerEl = document.getElementById('nav-session-timer');
    if (!timerEl) return;
    
    let seconds = parseInt(timerEl.getAttribute('data-seconds'), 10) || 1800;
    
    const interval = setInterval(() => {
        seconds--;
        if (seconds <= 0) {
            clearInterval(interval);
            timerEl.innerText = "EXPIRED";
            timerEl.style.color = "var(--clr-red)";
            // Trigger auto-logout or visual warning
            setTimeout(() => { window.location.href = '/logout/'; }, 2000);
            return;
        }
        
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        timerEl.innerText = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        
        if (seconds < 300) { // Under 5 minutes
            timerEl.style.color = "var(--clr-amber)";
        }
        if (seconds < 60) { // Under 1 minute
            timerEl.style.color = "var(--clr-red)";
            timerEl.classList.add('animate-pulse');
        }
    }, 1000);
}
