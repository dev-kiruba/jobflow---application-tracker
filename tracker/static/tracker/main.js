// Shared UI interactions: navigation, reveal motion, keyboard shortcuts and toasts.
function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? decodeURIComponent(match[2]) : null;
}
window.getCSRFToken = function () { return getCookie('csrftoken'); };

(function () {
    const toggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const backdrop = document.getElementById('sidebarBackdrop');
    if (toggle && sidebar) {
        const close = () => { sidebar.classList.remove('open'); backdrop?.classList.remove('visible'); toggle.setAttribute('aria-expanded', 'false'); };
        toggle.addEventListener('click', () => {
            const open = sidebar.classList.toggle('open');
            backdrop?.classList.toggle('visible', open);
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        backdrop?.addEventListener('click', close);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    }

    document.querySelectorAll('.alert').forEach((alert, index) => {
        setTimeout(() => alert.classList.add('show'), 50 + index * 70);
        setTimeout(() => { alert.classList.add('dismiss'); setTimeout(() => alert.remove(), 350); }, 4200 + index * 100);
    });

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduceMotion && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => entries.forEach(entry => {
            if (entry.isIntersecting) { entry.target.classList.add('revealed'); observer.unobserve(entry.target); }
        }), { threshold: 0.08 });
        document.querySelectorAll('.panel, .stat-card, .board-column, .empty-state, .form-layout').forEach(el => observer.observe(el));
    }

    const searchWrap = document.getElementById('boardSearchWrap');
    const searchToggle = document.getElementById('boardSearchToggle');
    if (searchWrap && searchToggle) searchToggle.addEventListener('click', () => {
        searchWrap.classList.toggle('hidden-search');
        if (!searchWrap.classList.contains('hidden-search')) searchWrap.querySelector('input')?.focus();
    });

    document.addEventListener('keydown', e => {
        if ((e.metaKey || e.ctrlKey) && (e.key.toLowerCase() === 'k' || e.key === '/')) {
            e.preventDefault();
            const input = document.querySelector('#tableSearch, #boardSearchWrap input, #boardSearch');
            if (input) { if (searchWrap) searchWrap.classList.remove('hidden-search'); input.focus(); }
        }
    });
})();
