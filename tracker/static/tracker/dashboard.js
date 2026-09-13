(function () {
    const counters = document.querySelectorAll('[data-count-to]');
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    counters.forEach((el, index) => {
        const target = Number(el.dataset.countTo || 0);
        if (reduced) { el.textContent = target; return; }
        const start = performance.now() + index * 70;
        const duration = 650;
        const tick = now => {
            const p = Math.min(1, Math.max(0, (now - start) / duration));
            const eased = 1 - Math.pow(1 - p, 3);
            el.textContent = Math.round(target * eased);
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    });

    const canvas = document.getElementById('statusChart');
    const dataNode = document.getElementById('chart-data');
    if (!canvas || !dataNode) return;
    let data = [];
    try { data = JSON.parse(dataNode.textContent || '[]'); } catch (_) { return; }
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const colors = ['#69a9ff', '#8b7cff', '#55d69a', '#ff6f88', '#737b8a'];
    const draw = () => {
        const rect = canvas.getBoundingClientRect();
        const w = Math.max(320, rect.width), h = Math.max(220, rect.height);
        canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr,0,0,dpr,0,0);
        ctx.clearRect(0,0,w,h);
        const pad = {l:28,r:18,t:18,b:42}; const chartW = w-pad.l-pad.r, chartH = h-pad.t-pad.b;
        const max = Math.max(1, ...data.map(d => Number(d.count)||0));
        ctx.strokeStyle='rgba(255,255,255,.055)'; ctx.lineWidth=1; ctx.font='9px DM Sans'; ctx.fillStyle='#596172';
        for(let i=0;i<=4;i++){ const y=pad.t+(chartH/4)*i; ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(w-pad.r,y);ctx.stroke();ctx.fillText(String(Math.round(max-(max/4)*i)),3,y+3); }
        const gap = Math.min(28, chartW/(data.length*3)); const bw = Math.max(20,(chartW-gap*(data.length-1))/data.length);
        data.forEach((d,i)=>{const count=Number(d.count)||0;const bh=(count/max)*chartH;const x=pad.l+i*(bw+gap);const y=pad.t+chartH-bh;const g=ctx.createLinearGradient(0,y,0,pad.t+chartH);g.addColorStop(0,colors[i%colors.length]);g.addColorStop(1,'rgba(139,124,255,.18)');ctx.fillStyle=g;ctx.beginPath();ctx.roundRect(x,y,bw,bh,7);ctx.fill();ctx.fillStyle='#a9afbc';ctx.textAlign='center';ctx.fillText(d.label,x+bw/2,h-18);if(count){ctx.fillStyle='#e5e8ef';ctx.font='600 10px DM Sans';ctx.fillText(String(count),x+bw/2,y-7);ctx.font='9px DM Sans';}});
    };
    draw(); window.addEventListener('resize', draw);
})();
