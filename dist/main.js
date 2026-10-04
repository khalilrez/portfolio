document.getElementById('y').textContent=new Date().getFullYear();
if(!matchMedia('(prefers-reduced-motion:reduce)').matches){
  const io=new IntersectionObserver(es=>es.forEach(e=>{
    if(!e.isIntersecting)return;io.unobserve(e.target);
    const el=e.target,to=+el.dataset.to,d=+(el.dataset.dec||0),t0=performance.now();
    (function f(t){const p=Math.min((t-t0)/1100,1);el.textContent=(to*(1-Math.pow(1-p,3))).toFixed(d);if(p<1)requestAnimationFrame(f)})(t0);
  }),{threshold:.6});
  document.querySelectorAll('[data-to]').forEach(el=>io.observe(el));
}
