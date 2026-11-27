const { exec } = require('child_process');
const http = require('http');
const fs = require('fs');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const port = 9336;
const child = exec(`"${chromePath}" --headless=new --remote-debugging-port=${port} --disable-gpu --no-first-run --user-data-dir="${__dirname}\\chrome_profile4" "http://localhost:8080"`);

async function run() {
  await new Promise(r => setTimeout(r, 2000));
  
  const endpoints = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${port}/json`, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
  
  const page = endpoints.find(e => e.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 1;
  const send = (method, params = {}) => new Promise((resolve) => {
    const msgId = id++;
    const handler = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id === msgId) {
        ws.removeEventListener('message', handler);
        resolve(msg.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: msgId, method, params }));
  });

  await new Promise(r => ws.addEventListener('open', r));

  const testSizes = [280, 320, 360, 375];
  for (const width of testSizes) {
    await send('Emulation.setDeviceMetricsOverride', {
      width: width,
      height: 700,
      deviceScaleFactor: 2,
      mobile: true
    });
    
    await send('Page.reload');
    await new Promise(r => setTimeout(r, 3500));

    await send('Runtime.evaluate', {
      expression: `(() => {
        const p = document.getElementById('preloader');
        if (p) p.style.display = 'none';
        document.body.classList.remove('preloader-active');
      })()`
    });

    const result = await send('Runtime.evaluate', {
      expression: `(() => {
        const vw = window.innerWidth;
        const docScrollWidth = document.documentElement.scrollWidth;
        const bodyScrollWidth = document.body.scrollWidth;

        const navLogo = document.querySelector('.nav-logo');
        const navActions = document.querySelector('.nav-actions');
        const newsBtn = document.getElementById('mobile-nav-news-btn');
        const notifBtn = document.getElementById('notif-btn');
        const contactBtn = document.getElementById('mobile-nav-contact-btn');
        const title = document.querySelector('.hero-title');
        const cta = document.getElementById('hero-cta-services');

        return {
          vw,
          docScrollWidth,
          bodyScrollWidth,
          hasHorizontalScroll: docScrollWidth > vw,
          iconsFit: contactBtn ? contactBtn.getBoundingClientRect().right <= vw : false,
          navLogoRight: navLogo ? Math.round(navLogo.getBoundingClientRect().right) : null,
          navActionsLeft: navActions ? Math.round(navActions.getBoundingClientRect().left) : null,
          navActionsRight: navActions ? Math.round(navActions.getBoundingClientRect().right) : null,
          contactBtnRight: contactBtn ? Math.round(contactBtn.getBoundingClientRect().right) : null,
          titleRight: title ? Math.round(title.getBoundingClientRect().right) : null,
          ctaRight: cta ? Math.round(cta.getBoundingClientRect().right) : null,
        };
      })()`,
      returnByValue: true
    });

    console.log(`TEST @ ${width}px:`, JSON.stringify(result.result.value, null, 2));

    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(`${__dirname}/verify_${width}.png`, Buffer.from(screenshot.data, 'base64'));
  }

  ws.close();
  try { child.kill(); } catch (e) {}
  process.exit(0);
}

run().catch(err => {
  console.error(err);
  try { child.kill(); } catch (e) {}
  process.exit(1);
});
