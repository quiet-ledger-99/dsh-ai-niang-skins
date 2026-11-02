/* Gemini / DSH design preview v0.1. No host connection or model requests. */
(() => {
  const $ = (selector) => document.querySelector(selector);
  const shell = $('#shell'), input = $('#message-input'), composer = $('#composer');
  const settings = $('#settings-dialog'), info = $('#info-dialog');
  const canvas = $('#scene-canvas'), scene = $('.workbench'), face = $('#companion-face');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let focused = false, motion = 'full', toastTimer, tickTimer, view = 'home';
  const artwork = {}, mobileLayer = document.createElement('canvas');
  const frames = {base:'gemini-starfall-wallpaper.png',eyeLeft:'sprites/blink-left.png',eyeRight:'sprites/blink-right.png',tail0:'sprites/tail-low.png',tail1:'sprites/tail-neutral.png',tail2:'sprites/tail-mid.png',tail3:'sprites/tail-high.png'};
  let lastFrame = '', epoch = performance.now();

  function toast(message) {
    clearTimeout(toastTimer); $('#toast').textContent = message; $('#toast').hidden = false;
    toastTimer = setTimeout(() => { $('#toast').hidden = true; }, 2600);
  }
  function expression(kind, label, note) {
    face.src = `assets/ui/q-${kind}.png`;
    $('#companion-state').textContent = label;
    $('#companion-note').textContent = note;
  }
  function showInfo(title, copy) {
    $('#info-title').textContent = title; $('#info-copy').textContent = copy;
    if (!info.open) info.showModal();
  }
  function setDetails(open) {
    $('#details-panel').hidden = !open;
    shell.classList.toggle('details-open', open);
    $('#details-toggle').setAttribute('aria-expanded', String(open));
    $('#details-toggle').setAttribute('aria-label', open ? '关闭会话详情' : '打开会话详情');
  }
  function setFocus() {
    focused = !focused; shell.classList.toggle('focus-mode', focused);
    $('#focus-toggle').setAttribute('aria-pressed', String(focused));
    $('#focus-switch').setAttribute('aria-checked', String(focused));
    paint(true); syncMotion();
  }
  function route() {
    const hash = location.hash.slice(1);
    view = ['chat','trace'].includes(hash) ? hash : 'home';
    shell.classList.toggle('chat-mode', view !== 'home');
    $('#home-view').hidden = view !== 'home';
    $('#chat-view').hidden = view !== 'chat';
    $('#trace-view').hidden = view !== 'trace';
    $('#session-title').textContent = view === 'home' ? '新会话' : '把灵感整理成一份计划';
    $('#session-caption').textContent = view === 'home' ? '留一点空间给新的想法' : view === 'trace' ? '每一步，都可以回看' : '文字有了位置，灵感就有了去处';
    for (const button of document.querySelectorAll('[data-view]')) {
      const selected = (button.dataset.view === 'trace') === (view === 'trace');
      if (button.getAttribute('role') === 'tab') { button.classList.toggle('selected', selected); button.setAttribute('aria-selected', String(selected)); }
    }
    for (const a of document.querySelectorAll('.preview-strip a')) {
      if (a.hash === '#' + view) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
    }
    for (const a of document.querySelectorAll('[data-session]')) a.classList.toggle('active', a.dataset.session === view);
    shell.classList.remove('sidebar-open'); $('#viewport').scrollTop = 0;
    expression('calm', view === 'home' ? '我在，慢慢来。' : '这一页，陪你读完。', view === 'home' ? '随时可以开始' : '示例会话');
    paint(true); syncMotion();
  }
  window.addEventListener('hashchange', route);
  document.addEventListener('click', (event) => {
    const button = event.target.closest('button,a'); if (!button) return;
    if (button.dataset.view) { location.hash = button.dataset.view === 'trace' ? 'trace' : view === 'home' ? 'home' : 'chat'; return; }
    if (button.dataset.prompt) { input.value = button.dataset.prompt; input.focus(); return; }
    if (button.dataset.expression) { expression(button.dataset.expression,'表情预览中','不代表真实任务状态'); return; }
    const action = button.dataset.action;
    if (!action) return;
    event.preventDefault();
    switch (action) {
      case 'new': input.value = ''; $('#local-messages').replaceChildren(); location.hash = 'home'; setDetails(false); if (view === 'home') route(); break;
      case 'sidebar': if (matchMedia('(max-width:700px)').matches) shell.classList.toggle('sidebar-open'); else shell.classList.toggle('sidebar-collapsed'); break;
      case 'details': setDetails($('#details-panel').hidden); break;
      case 'file': setDetails(true); $('#detail-preview').hidden = false; document.querySelector('[data-detail="files"]').click(); break;
      case 'palette': toast('示例配色已在下方预览中展示'); break;
      case 'focus': setFocus(); break;
      case 'settings': settings.showModal(); break;
      case 'close-settings': settings.close(); break;
      case 'close-info': info.close(); break;
      case 'attachment': $('#attachment-chip').hidden = false; input.focus(); break;
      case 'remove-attachment': $('#attachment-chip').hidden = true; break;
      case 'model': showInfo('模型选择','这里保留 DSH 原生模型选择器的位置。设计稿不连接模型服务，当前不显示虚构的额度或费用。'); break;
      case 'permission': showInfo('访问范围','工作区权限入口与模型、附件分别排布；正式接入时由 DSH 原生权限控件负责。'); break;
      case 'usage': showInfo('用量与余额','正式接入后显示 DSH 提供的真实用量和费用。设计预览不填入演示数字。'); break;
      case 'plugins': showInfo('插件','保留 DSH 的插件入口；插件功能仍由各自的原生界面承担。'); break;
      case 'automations': showInfo('自动化任务','保留 DSH 的自动化任务入口。本设计稿没有创建定时任务。'); break;
      case 'board': showInfo('任务看板','看板使用同一组深靛背景、纸页卡片与金色状态点；本轮重点设计会话、输入和详情区域。'); break;
      case 'workspace': showInfo('工作区','工作区与会话沿用 DSH 的层级。窄窗时侧栏收成抽屉，不挤压正文。'); break;
      case 'search': showInfo('搜索会话','搜索入口固定在“工作区”标题旁；长会话名称在列表中截断，完整名称留给会话头部。'); break;
      case 'notice': toast('已演示收藏反馈；未保存到宿主'); break;
    }
  });
  for (const tab of document.querySelectorAll('[data-detail]')) tab.addEventListener('click', () => {
    for (const t of document.querySelectorAll('[data-detail]')) { t.classList.toggle('active', t === tab); t.setAttribute('aria-selected', String(t === tab)); }
    $('#detail-files').hidden = tab.dataset.detail !== 'files'; $('#detail-info').hidden = tab.dataset.detail !== 'info';
  });
  $('#workspace-toggle').addEventListener('click', () => { const collapsed = !$('#sessions').hidden; $('#sessions').hidden = collapsed; $('#workspace-toggle').setAttribute('aria-expanded', String(!collapsed)); });
  $('#motion-select').addEventListener('change', (event) => { motion = event.target.value; paint(true); syncMotion(); });
  input.addEventListener('focus', () => expression('focus','我在听，继续说。','输入中的表情预览'));
  input.addEventListener('blur', () => expression('calm','我在，慢慢来。','随时可以开始'));
  input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = Math.min(input.scrollHeight,140) + 'px'; });
  input.addEventListener('keydown', (event) => { if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); composer.requestSubmit(); } });
  composer.addEventListener('submit', (event) => {
    event.preventDefault(); const text = input.value.trim(); if (!text) { input.focus(); return; }
    if (view !== 'chat') { location.hash = 'chat'; }
    const user = document.createElement('article'); user.className = 'user-message';
    const name = document.createElement('span'); name.textContent = '你'; const content = document.createElement('p'); content.textContent = text; user.append(name,content);
    const reply = document.createElement('article'); reply.className = 'local-reply'; const author = document.createElement('b'); author.textContent = 'Gemini · 预览反馈';
    const body = document.createElement('p'); body.textContent = '收到了。这条内容只留在当前预览页，用来查看输入、消息排版与滚动效果；没有发给模型。'; reply.append(author,body);
    $('#local-messages').append(user,reply); input.value = ''; input.style.height = 'auto'; $('#attachment-chip').hidden = true;
    expression('done','这一步，收到啦。','仅为本地预览反馈');
    requestAnimationFrame(() => { $('#viewport').scrollTop = $('#viewport').scrollHeight; });
  });
  $('.copy-code').addEventListener('click', async () => { await navigator.clipboard.writeText($('.code-block code').innerText); toast('已复制示例代码'); });
  $('.copy-answer').addEventListener('click', async () => { await navigator.clipboard.writeText($('.reading-paper').innerText); toast('已复制示例答复'); });
  for (const dialog of [settings,info]) dialog.addEventListener('click', (event) => { if (event.target === dialog) { const r = dialog.getBoundingClientRect(); if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close(); } });
  document.addEventListener('keydown', (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'n') { event.preventDefault(); location.hash = 'home'; input.focus(); } if (event.key === 'Escape') shell.classList.remove('sidebar-open'); });

  function paint(force = false) {
    if (!artwork.base?.complete || !artwork.base.naturalWidth) return;
    const r = scene.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1,2);
    const w = Math.round(r.width*d), h = Math.round(r.height*d);
    const active = !document.hidden && !reducedMotion.matches && motion !== 'off' && view === 'home' && !focused;
    const elapsed = performance.now() - epoch;
    const sequence = motion === 'subtle' ? [1,2,1] : [0,1,2,3,2,1];
    const pose = active ? sequence[Math.floor(elapsed/(motion === 'subtle' ? 600 : 300)) % sequence.length] : 1;
    const blink = active && elapsed % (motion === 'subtle' ? 6500 : 4200) > (motion === 'subtle' ? 6320 : 4020);
    const key = [w,h,pose,blink].join(':'); if (!force && key === lastFrame) return; lastFrame = key;
    canvas.width = w; canvas.height = h;
    const c = canvas.getContext('2d'); c.imageSmoothingEnabled = false;
    const narrow = r.width < 701;
    const scale = Math.max(w/1672,h/941) * (narrow ? .67 : 1);
    const x = (narrow ? w*.71 : w*.76) - 1190*scale;
    const y = narrow ? h*.64 - 215*scale : h - 941*scale;
    c.clearRect(0,0,w,h);
    let artContext = c;
    if (narrow) {
      c.drawImage(artwork.base,0,0,750,941,0,0,w,h);
      mobileLayer.width = w; mobileLayer.height = h;
      artContext = mobileLayer.getContext('2d'); artContext.imageSmoothingEnabled = false;
    }
    artContext.drawImage(artwork.base,x,y,1672*scale,941*scale);
    const patch = (image,sx,sy,sw,sh) => { if (image?.complete && image.naturalWidth) artContext.drawImage(image,x+sx*scale,y+sy*scale,sw*scale,sh*scale); };
    patch(artwork['tail'+pose],1408,345,264,355);
    if (blink) { patch(artwork.eyeLeft,1134,207,53,35); patch(artwork.eyeRight,1201,177,55,40); }
    if (narrow) {
      const fade = artContext.createLinearGradient(0,y,0,y+110*d);
      fade.addColorStop(0,'transparent'); fade.addColorStop(1,'#000');
      artContext.globalCompositeOperation = 'destination-in'; artContext.fillStyle = fade; artContext.fillRect(0,0,w,h);
      c.drawImage(mobileLayer,0,0);
    }
  }
  function syncMotion() {
    clearInterval(tickTimer); tickTimer = null;
    if (!document.hidden && !reducedMotion.matches && motion !== 'off' && view === 'home' && !focused) tickTimer = setInterval(() => paint(),100);
  }
  for (const [key,path] of Object.entries(frames)) { const image = new Image(); artwork[key] = image; image.onload = () => paint(true); image.src = 'assets/' + path; }
  new ResizeObserver(() => paint(true)).observe(scene);
  document.addEventListener('visibilitychange', () => { paint(true); syncMotion(); });
  reducedMotion.addEventListener('change', () => { paint(true); syncMotion(); });
  route();
})();
