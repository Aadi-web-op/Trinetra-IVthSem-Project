/**
 * TRINETRA SECURITY PROTOCOL
 * Enforces Auto-Logout on Tab Switch/Minimize
 */
console.log("Trinetra Security Protocol: ACTIVE");

document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.warn("Security Breach: User left the secure window. Terminating Session.");
        // Use sendBeacon for more reliable transmission during unload/hide
        // But for redirect, we just force window location
        window.location.href = '/admin/logout/';
    }
});

// Optional: Prevent Context Menu (Right Click) to secure content
document.addEventListener('contextmenu', event => event.preventDefault());
