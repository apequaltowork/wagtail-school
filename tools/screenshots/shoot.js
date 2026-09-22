// Full-page screenshots of the demo site for one upgrade stage.
//
//   PYTHON=<venv python> DEMO_ADMIN_PASSWORD=... node shoot.js --base http://127.0.0.1:8027 --out ../../notes/screenshots/2.7
//
// Page and site IDs come from ../screenshot_targets.py, so the list works on every stage.
// Note: the thank-you screenshot submits the enrolment form once (one extra submission).
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function arg(name, fallback) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 ? process.argv[i + 1] : fallback;
}

const base = arg('base', 'http://127.0.0.1:8027');
const out = path.resolve(arg('out', '../../notes/screenshots/2.7'));
const only = arg('only', 'all'); // all | frontend | admin
const python = process.env.PYTHON || 'python';
const password = process.env.DEMO_ADMIN_PASSWORD;

const targets = JSON.parse(
  execFileSync(python, [path.join(__dirname, '..', 'screenshot_targets.py')], { encoding: 'utf8' })
);

async function shot(page, name, url) {
  const response = await page.goto(base + url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(300);
  const file = path.join(out, name + '.png');
  await page.screenshot({ path: file, fullPage: true });
  console.log(`${response ? response.status() : '---'} ${url} -> ${path.relative(process.cwd(), file)}`);
}

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await context.newPage();

  // Admin first, so the submissions listing is shot before the test submission below.
  if (only !== 'frontend') {
    if (!password) throw new Error('Set DEMO_ADMIN_PASSWORD to screenshot the admin');
    await page.goto(base + '/admin/login/', { waitUntil: 'networkidle' });
    await page.fill('#id_username', 'admin');
    await page.fill('#id_password', password);
    await Promise.all([page.waitForNavigation({ waitUntil: 'networkidle' }), page.click('button[type=submit]')]);
    for (const [name, url] of targets.admin) await shot(page, name, url);
    await context.clearCookies();
  }

  if (only !== 'admin') {
    for (const [name, url] of targets.frontend) await shot(page, name, url);

    // Enrolment form: fill it in and screenshot the thank-you page.
    await page.goto(base + targets.form.path, { waitUntil: 'networkidle' });
    await page.getByLabel("Parent/Guardian's full name").fill('Screenshot Tester');
    await page.getByLabel('Email address').fill('screenshot.tester@example.com');
    await page.getByLabel("Student's first name").fill('Robin');
    await page.getByLabel('Year level of entry').selectOption('Year 7');
    await page.getByLabel('Term 1').check();
    await Promise.all([page.waitForNavigation({ waitUntil: 'networkidle' }), page.click('button[type=submit]')]);
    await page.screenshot({ path: path.join(out, targets.form.name + '.png'), fullPage: true });
    console.log(`POST ${targets.form.path} -> ${targets.form.name}.png (${page.url()})`);
  }

  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
