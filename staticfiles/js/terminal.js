/**
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * TRINETRA - TERMINAL & COMMAND PALETTE
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */

document.addEventListener('DOMContentLoaded', () => {
    initCommandPalette();
    initCommandTerminal();
});

function initCommandPalette() {
    const palette = document.getElementById('cmd-palette');
    const input = document.getElementById('cmd-input');
    const results = document.getElementById('cmd-results');
    
    if (!palette || !input) return;
    
    // Toggle on Cmd+K or Ctrl+K
    document.addEventListener('keydown', (e) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
            e.preventDefault();
            togglePalette();
        }
        
        if (e.key === 'Escape' && palette.classList.contains('active')) {
            togglePalette(false);
        }
    });
    
    // Close on click outside
    palette.addEventListener('click', (e) => {
        if (e.target === palette) {
            togglePalette(false);
        }
    });
    
    function togglePalette(forceState = null) {
        const isActive = palette.classList.contains('active');
        const newState = forceState !== null ? forceState : !isActive;
        
        if (newState) {
            palette.classList.add('active');
            input.value = '';
            input.focus();
            renderResults('');
        } else {
            palette.classList.remove('active');
            input.blur();
        }
    }
    
    // Dummy search logic for demo
    const commands = [
        { title: 'New Case', action: '/cases/new/', icon: 'folder-plus' },
        { title: 'Access AI Node', action: '/ai-lab/', icon: 'cpu' },
        { title: 'View Audit Logs', action: '/logs/', icon: 'shield-alert' },
        { title: 'System Settings', action: '/settings/', icon: 'settings' },
        { title: 'Disconnect Session', action: '/logout/', icon: 'power' }
    ];
    
    input.addEventListener('input', (e) => {
        renderResults(e.target.value.toLowerCase());
    });
    
    function renderResults(query) {
        results.innerHTML = '';
        const filtered = commands.filter(cmd => cmd.title.toLowerCase().includes(query));
        
        if (filtered.length === 0) {
            results.innerHTML = `<div class="p-4 text-muted font-mono text-sm">NO DIRECTIVES FOUND</div>`;
            return;
        }
        
        filtered.forEach((cmd, idx) => {
            const el = document.createElement('a');
            el.href = cmd.action;
            el.className = `flex items-center gap-4 p-4 hover:bg-cyan/10 hover:text-cyan border-b border-white/5 transition-colors ${idx === 0 && query ? 'bg-cyan/5 text-cyan' : 'text-text'}`;
            el.innerHTML = `
                <i data-lucide="${cmd.icon}" class="w-5 h-5"></i>
                <span class="font-heading tracking-wider">${cmd.title}</span>
            `;
            results.appendChild(el);
        });
        
        if (window.lucide) {
            lucide.createIcons();
        }
    }
}

function initCommandTerminal() {
    // Hidden Ctrl+Shift+T terminal overlay
    let terminalActive = false;
    
    const termShell = document.createElement('div');
    termShell.id = 'sys-terminal';
    termShell.style.position = 'fixed';
    termShell.style.top = '0';
    termShell.style.left = '0';
    termShell.style.width = '100vw';
    termShell.style.height = '100vh';
    termShell.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
    termShell.style.color = '#00FF9C'; // neon green
    termShell.style.fontFamily = 'var(--font-data)';
    termShell.style.padding = '2rem';
    termShell.style.zIndex = '999999';
    termShell.style.display = 'none';
    termShell.style.overflowY = 'auto';
    
    const outputArea = document.createElement('div');
    outputArea.id = 'term-output';
    outputArea.style.marginBottom = '1rem';
    termShell.appendChild(outputArea);
    
    const inputLine = document.createElement('div');
    inputLine.style.display = 'flex';
    inputLine.innerHTML = `<span style="margin-right: 10px;">TRINETRA:// $</span> <input type="text" id="term-input" style="background: transparent; border: none; color: inherit; font: inherit; outline: none; flex: 1;">`;
    termShell.appendChild(inputLine);
    
    document.body.appendChild(termShell);
    const termInput = document.getElementById('term-input');
    
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 't') {
            e.preventDefault();
            terminalActive = !terminalActive;
            termShell.style.display = terminalActive ? 'block' : 'none';
            if (terminalActive) {
                termInput.focus();
                if (outputArea.innerHTML === '') {
                    printToTerminal('TRINETRA SYSTEM TERMINAL v3.0 [SECURE CONNECTION]');
                    printToTerminal('Type "help" for a list of directives.');
                }
            }
        }
    });
    
    termInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const cmd = termInput.value.trim();
            printToTerminal(`TRINETRA:// $ ${cmd}`);
            termInput.value = '';
            processCommand(cmd.toLowerCase());
        }
    });
    
    function printToTerminal(text) {
        const line = document.createElement('div');
        line.style.marginBottom = '0.5rem';
        outputArea.appendChild(line);
        
        // Typewriter effect
        let i = 0;
        const speed = 10;
        function type() {
            if (i < text.length) {
                line.innerHTML += text.charAt(i);
                i++;
                termShell.scrollTop = termShell.scrollHeight;
                setTimeout(type, speed);
            }
        }
        type();
    }
    
    function processCommand(cmd) {
        if (cmd === '') return;
        
        setTimeout(() => {
            switch(cmd) {
                case 'help':
                    printToTerminal('AVAILABLE DIRECTIVES:');
                    printToTerminal('  whoami      - Display current officer clearance');
                    printToTerminal('  status      - System health check');
                    printToTerminal('  clear       - Clear terminal output');
                    printToTerminal('  lock        - Trigger manual dead-man switch');
                    printToTerminal('  exit        - Close terminal');
                    break;
                case 'whoami':
                    printToTerminal('IDENTITY CONFIRMED: COMMAND OFFICER');
                    printToTerminal('CLEARANCE LEVEL: 4 (TOP SECRET)');
                    printToTerminal('SESSION INTEGRITY: 100%');
                    break;
                case 'status':
                    printToTerminal('[OK] NEURAL CORE ONLINE');
                    printToTerminal('[OK] FIREWALL ACTIVE (IP STRICT)');
                    printToTerminal('[OK] DATABASE ENCRYPTION: AES-256');
                    break;
                case 'clear':
                    outputArea.innerHTML = '';
                    break;
                case 'exit':
                    terminalActive = false;
                    termShell.style.display = 'none';
                    break;
                case 'lock':
                    printToTerminal('CRITICAL: INITIATING SYSTEM LOCKDOWN...');
                    setTimeout(() => { window.location.href = '/logout/'; }, 1500);
                    break;
                default:
                    printToTerminal(`Command not found: ${cmd}`);
            }
        }, 300);
    }
}
