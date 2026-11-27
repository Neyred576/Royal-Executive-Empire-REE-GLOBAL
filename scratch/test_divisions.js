const { exec } = require('child_process');
const http = require('http');
const fs = require('fs');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const port = 9337;
const child = exec(`"${chromePath}" --headless=new --remote-debugging-port=${port} --disable-gpu --no-first-run --user-data-dir="${__dirname}\\chrome_profile5" "http://localhost:8080"`);

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

  const testSizes = [320, 360, 375, 412];
  for (const width of testSizes) {
    await send('Emulation.setDeviceMetricsOverride', {
      width: width,
      height: 750,
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

        const navLogo = document.querySelector('.nav-logo');
        const navLinks = document.querySelector('.nav-links');
        const divisionsLink = document.querySelector('.nav-links a[href*="divisions"]');
        const navActions = document.querySelector('.nav-actions');
        const contactBtn = document.getElementById('mobile-nav-contact-btn');

        const logoRect = navLogo ? navLogo.getBoundingClientRect() : null;
        const linksRect = navLinks ? navLinks.getBoundingClientRect() : null;
        const divRect = divisionsLink ? divisionsLink.getBoundingClientRect() : null;
        const actionsRect = navActions ? navActions.getBoundingClientRect() : null;
        const contactRect = contactBtn ? contactBtn.getBoundingClientRect() : null;

        return {
          vw,
          docScrollWidth,
          hasHorizontalScroll: docScrollWidth > vw,
          divisionsVisible: !!(divisionsLink && window.getComputedStyle(divisionsLink).display !== 'none' && divRect && divRect.width > 0),
          divisionsText: divisionsLink ? divisionsLink.innerText : null,
          divisionsLeft: divRect ? Math.round(divRect.left) : null,
          divisionsRight: divRect ? Math.round(divRect.right) : null,
          divisionsWidth: divRect ? Math.round(divRect.width) : null,
          logoRight: logoRect ? Math.round(logoRect.right) : null,
          actionsLeft: actionsRect ? Math.round(actionsRect.left) : null,
          actionsRight: actionsRect ? Math.round(actionsRect.right) : null,
          allFit: contactRect ? contactRect.right <= vw : false
        };
      })()`,
      returnByValue: true
    });

    console.log(`DIVISIONS TEST @ ${width}px:`, JSON.stringify(result.result.value, null, 2));

    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(`${__dirname}/divisions_${width}.png`, Buffer.from(screenshot.data, 'base64'));
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
