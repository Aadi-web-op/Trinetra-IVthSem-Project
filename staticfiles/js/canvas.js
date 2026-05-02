/**
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * TRINETRA - CANVAS PARTICLE NETWORK
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.id = 'particle-network';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '0'; // Behind everything
    canvas.style.pointerEvents = 'none'; // Don't block clicks
    
    // Insert at the beginning of body
    document.body.insertBefore(canvas, document.body.firstChild);
    
    const ctx = canvas.getContext('2d');
    
    let width, height;
    let particles = [];
    
    const mouse = {
        x: null,
        y: null,
        radius: 150 // Repel distance
    };
    
    // Track mouse globally
    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });
    
    window.addEventListener('mouseout', () => {
        mouse.x = null;
        mouse.y = null;
    });
    
    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        initParticles();
    }
    
    window.addEventListener('resize', resize);
    
    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.8; // 0.4 max speed
            this.vy = (Math.random() - 0.5) * 0.8;
            this.baseRadius = Math.random() * 1.5 + 0.5;
            this.radius = this.baseRadius;
            this.color = 'rgba(0, 240, 255, 0.4)';
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
        }
        
        update() {
            // Move
            this.x += this.vx;
            this.y += this.vy;
            
            // Bounce off edges
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
            
            // Mouse repel
            if (mouse.x != null && mouse.y != null) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < mouse.radius) {
                    // Repel logic
                    let forceDirectionX = dx / distance;
                    let forceDirectionY = dy / distance;
                    let force = (mouse.radius - distance) / mouse.radius;
                    
                    this.x -= forceDirectionX * force * 3;
                    this.y -= forceDirectionY * force * 3;
                }
            }
            
            this.draw();
        }
    }
    
    function initParticles() {
        particles = [];
        // ~80 nodes
        const numberOfParticles = Math.min(Math.floor((width * height) / 15000), 100); 
        for (let i = 0; i < numberOfParticles; i++) {
            particles.push(new Particle());
        }
    }
    
    function connectParticles() {
        let opacityValue = 1;
        for (let a = 0; a < particles.length; a++) {
            for (let b = a; b < particles.length; b++) {
                let distance = ((particles[a].x - particles[b].x) * (particles[a].x - particles[b].x)) + 
                               ((particles[a].y - particles[b].y) * (particles[a].y - particles[b].y));
                               
                // Connect if within 120px (120^2 = 14400)
                if (distance < 14400) {
                    opacityValue = 1 - (distance / 14400);
                    ctx.strokeStyle = `rgba(0, 240, 255, ${opacityValue * 0.25})`;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.moveTo(particles[a].x, particles[a].y);
                    ctx.lineTo(particles[b].x, particles[b].y);
                    ctx.stroke();
                }
            }
        }
    }
    
    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, width, height);
        
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
        }
        
        connectParticles();
    }
    
    resize();
    animate();
});
