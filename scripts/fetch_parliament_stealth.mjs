// ==Playwright Stealth Browser Script==
// Fetches Parliament website pages protected by Radware using stealth techniques.
// Usage: node scripts/fetch_parliament_stealth.mjs
// Use TEST_MODE=1 to only fetch the first URL.

import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const DERIVED = resolve(ROOT, 'derived', 'parliament_stealth');
mkdirSync(DERIVED, { recursive: true });

const TARGETS = [
  {
    label: 'members-current',
    url: 'https://www3.parliament.nz/en/mps-and-electorates/members-of-parliament/',
  },
  {
    label: 'former-members',
    url: 'https://www3.parliament.nz/en/mps-and-electorates/former-members-of-parliament/',
  },
  {
    label: 'daily-progress',
    url: 'https://www3.parliament.nz/en/pb/daily-progress-in-the-house/',
  },
  {
    label: 'order-paper',
    url: 'https://www3.parliament.nz/en/pb/order-paper-questions/order-paper/',
  },
  {
    label: 'hansard-current',
    url: 'https://hansard.parliament.nz/hansard-debates/rhr?lang=en',
  },
];

// Test mode: only fetch first target
const TEST_MODE = process.env.TEST_MODE === '1';
if (TEST_MODE) {
  console.log('TEST_MODE: Only fetching first target');
  TARGETS.splice(1);
}

async function stealthFetch(page, target) {
  console.log(`\n=== ${target.label} ===`);
  console.log(`URL: ${target.url}`);

  try {
    await page.goto(target.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
    await page.waitForTimeout(3000);

    const title = await page.title();
    console.log(`Title: ${title}`);

    if (title.includes('Radware') || title.includes('radware') || title.includes('Just a moment')) {
      console.log('  BLOCKED by Radware - taking screenshot for debugging');
      await page.screenshot({ path: resolve(DERIVED, `${target.label}_blocked.png`), fullPage: true });
      return null;
    }

    const text = await page.evaluate(() => document.body.innerText);
    console.log(`Content length: ${text.length} chars`);

    const html = await page.content();
    writeFileSync(resolve(DERIVED, `${target.label}.html`), html, 'utf-8');
    writeFileSync(resolve(DERIVED, `${target.label}.txt`), text, 'utf-8');
    await page.screenshot({ path: resolve(DERIVED, `${target.label}.png`), fullPage: true });

    console.log(`  Saved: ${target.label}.html/txt/png`);
    return { title, textLength: text.length };
  } catch (err) {
    console.log(`  Error: ${err.message}`);
    return null;
  }
}

(async () => {
  console.log('Launching stealth browser...');

  const browser = await chromium.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-web-security',
      '--disable-features=BlockInsecurePrivateNetworkRequests',
    ],
  });

  const context = await browser.newContext({
    userAgent:
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 },
    locale: 'en-NZ',
    timezoneId: 'Pacific/Auckland',
    bypassCSP: true,
  });

  // Stealth: override navigator.webdriver
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
    window.chrome = { runtime: {} };
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) =>
      parameters.name === 'notifications'
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters);
  });

  const results = [];
  for (const target of TARGETS) {
    const page = await context.newPage();
    const result = await stealthFetch(page, target);
    if (result) results.push(result);
    await page.close();
  }

  await browser.close();

  console.log(`\n=== RESULTS ===`);
  console.log(`Successful: ${results.length}/${TARGETS.length}`);
  for (const r of results) {
    console.log(`  - ${r.title}: ${r.textLength} chars`);
  }

  const log = {
    timestamp: new Date().toISOString(),
    targets: TARGETS.map((t) => t.label),
    successful: results.length,
    total: TARGETS.length,
    results,
  };
  writeFileSync(resolve(DERIVED, 'run_log.json'), JSON.stringify(log, null, 2), 'utf-8');
  console.log(`\nLog saved to ${DERIVED}/run_log.json`);
})();
