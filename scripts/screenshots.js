/**
 * s-MeteoRisk Automated Screenshot Generator
 * Captures portfolio-quality screenshots of the Streamlit dashboard and Apache Airflow UI.
 *
 * Usage with Docker (zero host installation):
 * docker run --rm --add-host host.docker.internal:host-gateway \
 *   -e NODE_PATH=/tmp/node_modules -v "${PWD}:/work" -w /tmp \
 *   mcr.microsoft.com/playwright:v1.48.0-focal \
 *   bash -c "npm install playwright@1.48.0 && node /work/scripts/screenshots.js"
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DASHBOARD_URL = process.env.DASHBOARD_URL || 'http://host.docker.internal:8502';
const AIRFLOW_URL = process.env.AIRFLOW_URL || 'http://host.docker.internal:8080';
const OUT_DIR = path.resolve(__dirname, '../docs/screenshots');

(async () => {
  if (!fs.existsSync(OUT_DIR)) {
    fs.mkdirSync(OUT_DIR, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });

  const page = await context.newPage();

  console.log(`Connecting to Streamlit Dashboard at ${DASHBOARD_URL}...`);
  try {
    await page.goto(DASHBOARD_URL, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(4000);

    console.log('Capturing 01-dashboard-overview.png...');
    await page.screenshot({
      path: path.join(OUT_DIR, '01-dashboard-overview.png'),
      fullPage: false
    });

    console.log('Scrolling down to Risk Dispersion chart...');
    await page.evaluate(() => {
      const container = document.querySelector('section.main') || document.querySelector('[data-testid="stMain"]') || window;
      if (container.scrollTo) {
        container.scrollTo(0, 950);
      } else {
        window.scrollBy(0, 950);
      }
    });
    await page.waitForTimeout(2500);

    console.log('Capturing 02-dashboard-risk-analysis.png...');
    await page.screenshot({
      path: path.join(OUT_DIR, '02-dashboard-risk-analysis.png'),
      fullPage: false
    });
  } catch (err) {
    console.error('Error capturing dashboard:', err.message);
  }

  console.log(`Connecting to Airflow at ${AIRFLOW_URL}...`);
  try {
    await page.goto(`${AIRFLOW_URL}/login/`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.fill('input[name="username"]', 'airflow');
    await page.fill('input[name="password"]', 'airflow');
    await page.click('input[type="submit"]');
    await page.waitForTimeout(3000);

    console.log('Capturing 03-airflow-dags.png...');
    await page.screenshot({
      path: path.join(OUT_DIR, '03-airflow-dags.png'),
      fullPage: false
    });

    console.log('Navigating to s_meteorisk_daily_update DAG Graph...');
    await page.goto(`${AIRFLOW_URL}/dags/s_meteorisk_daily_update/graph`, {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    await page.waitForTimeout(3000);

    console.log('Capturing 04-airflow-dag-graph.png...');
    await page.screenshot({
      path: path.join(OUT_DIR, '04-airflow-dag-graph.png'),
      fullPage: false
    });
  } catch (err) {
    console.error('Error capturing Airflow:', err.message);
  }

  await browser.close();
  console.log('All screenshots completed successfully!');
})();
