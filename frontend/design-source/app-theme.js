/* React owns the original intro; the hero copies its static content without moving React nodes. */
(() => {
  function enhance() {
    const header = document.querySelector('.topbar');
    const intro = document.querySelector('main > .intro');
    if (!header || !intro) return false;
    if (header.querySelector('.tp-hero')) return true;
    const hero = document.createElement('section');
    hero.className = 'tp-hero';
    hero.setAttribute('aria-label', 'Presentación de Territorio Preparado');
    const copy = intro.firstElementChild.cloneNode(true);
    copy.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
    const actions = document.createElement('div');
    actions.className = 'header-actions';
    const map = document.createElement('a');
    map.href = '#territory-navigation';
    map.textContent = 'Explorar el territorio ↓';
    const tabs = document.querySelector('main > .tabs');
    if (tabs) tabs.id = 'territory-navigation';
    const simulation = document.createElement('a');
    simulation.href = './simulation.html';
    simulation.textContent = 'Abrir simulación 3D ↗';
    actions.append(map, simulation);
    copy.append(actions);
    const seal = document.createElement('aside');
    seal.className = 'tp-seal';
    const title = document.createElement('strong');
    title.textContent = 'Cali ↗';
    const subtitle = document.createElement('span');
    subtitle.textContent = 'Conocer · Preparar · Coordinar';
    seal.append(title, subtitle);
    hero.append(copy, seal);
    header.append(hero);
    document.body.classList.add('tp-themed-home');
    return true;
  }
  if (!enhance()) {
    const root = document.getElementById('root');
    if (!root) return;
    const observer = new MutationObserver(() => {
      if (enhance()) observer.disconnect();
    });
    observer.observe(root, {childList:true, subtree:true});
  }
})();
