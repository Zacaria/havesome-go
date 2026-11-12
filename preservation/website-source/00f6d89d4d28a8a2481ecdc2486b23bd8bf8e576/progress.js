(() => {
  const nav = document.querySelector('aside nav');
  const links = [...nav.querySelectorAll('a[href^="#"]')];
  const entries = links
    .map(link => ({ link, section: document.getElementById(link.hash.slice(1)) }))
    .filter(x => x.section);
  let active = null;
  let scheduled = false;
  function update() {
    scheduled = false;
    const aside = nav.closest('aside');
    const readingLine = matchMedia('(max-width: 800px)').matches
      ? Math.max(80, aside.getBoundingClientRect().bottom + 32)
      : Math.max(80, innerHeight * 0.2);
    const atEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 2;
    let next = null;
    for (const entry of entries) {
      if (entry.section.getBoundingClientRect().top <= readingLine) next = entry;
    }
    if (atEnd) next = entries.at(-1);
    if (next === active) return;
    if (active) active.link.removeAttribute('aria-current');
    active = next;
    if (active) {
      active.link.setAttribute('aria-current', 'location');
      if (matchMedia('(max-width: 800px)').matches) {
        const list = nav.querySelector('ol');
        list.scrollLeft = active.link.offsetLeft - list.offsetLeft - list.clientWidth / 2 + active.link.offsetWidth / 2;
      }
    }
  }
  function schedule() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(update);
    }
  }
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule);
  addEventListener('hashchange', schedule);
  update();
})();
