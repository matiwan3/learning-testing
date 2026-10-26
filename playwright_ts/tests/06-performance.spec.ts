import { test, expect } from '@playwright/test';

// Performance tests. Thresholds are generous on purpose (real network = noisy).
// Tune them to your own site/baseline.
const URL = 'https://playwright.dev';

test('navigation timing (TTFB, DOMContentLoaded, load)', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'load' });

    const timing = await page.evaluate(() => {
        const [nav] = performance.getEntriesByType('navigation') as PerformanceNavigationTiming[];
        return {
            ttfb: nav.responseStart - nav.requestStart,
            domContentLoaded: nav.domContentLoadedEventEnd - nav.startTime,
            load: nav.loadEventStart - nav.startTime,
        };
    });
    console.table(timing);

    expect(timing.ttfb).toBeLessThan(2000);
    expect(timing.domContentLoaded).toBeLessThan(5000);
    expect(timing.load).toBeLessThan(8000);
});

test('Core Web Vitals: LCP and CLS', async ({ page }) => {
    // observers must exist BEFORE the page scripts run -> addInitScript
    await page.addInitScript(() => {
        const w = window as any;
        w.__vitals = { lcp: 0, cls: 0 };

        new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) w.__vitals.lcp = entry.startTime;
        }).observe({ type: 'largest-contentful-paint', buffered: true });

        new PerformanceObserver((list) => {
            for (const entry of list.getEntries() as any[]) {
                if (!entry.hadRecentInput) w.__vitals.cls += entry.value;
            }
        }).observe({ type: 'layout-shift', buffered: true });
    });

    await page.goto(URL, { waitUntil: 'networkidle' });
    const vitals = await page.evaluate(() => (window as any).__vitals);
    console.table(vitals);

    expect(vitals.lcp).toBeGreaterThan(0);
    expect(vitals.lcp).toBeLessThan(5000); // "good" is < 2500 ms
    expect(vitals.cls).toBeLessThan(0.25); // "good" is < 0.1
});

test('resource budget: request count and transferred bytes', async ({ page }) => {
    await page.goto(URL, { waitUntil: 'networkidle' });

    const stats = await page.evaluate(() => {
        const res = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
        const byType: Record<string, number> = {};
        for (const r of res) byType[r.initiatorType] = (byType[r.initiatorType] ?? 0) + 1;
        return {
            requests: res.length,
            kbTransferred: Math.round(res.reduce((sum, r) => sum + r.transferSize, 0) / 1024),
            slowest: res
                .map((r) => ({ name: r.name.slice(-60), ms: Math.round(r.duration) }))
                .sort((a, b) => b.ms - a.ms)
                .slice(0, 3),
            byType,
        };
    });
    console.log(JSON.stringify(stats, null, 2));

    expect(stats.requests).toBeLessThan(150);
    expect(stats.kbTransferred).toBeLessThan(5000);
});

test('slow 3G via Chrome DevTools Protocol (chromium only)', async ({ page, context, browserName }) => {
    test.skip(browserName !== 'chromium', 'CDP is chromium only');
    test.setTimeout(90_000);

    const t0 = Date.now();
    await page.goto(URL, { waitUntil: 'load' });
    const normalMs = Date.now() - t0;

    const cdp = await context.newCDPSession(page);
    await cdp.send('Network.enable');
    await cdp.send('Network.emulateNetworkConditions', {
        offline: false,
        latency: 400, // ms added to every request
        downloadThroughput: (500 * 1024) / 8, // ~500 kbit/s
        uploadThroughput: (500 * 1024) / 8,
    });
    await cdp.send('Network.clearBrowserCache');

    const t1 = Date.now();
    await page.goto(URL, { waitUntil: 'load' });
    const slowMs = Date.now() - t1;

    console.log({ normalMs, slowMs });
    expect(slowMs).toBeGreaterThan(normalMs);
    expect(slowMs).toBeLessThan(60_000);
});

test('3 concurrent users: p95 load time', async ({ browser }) => {
    test.setTimeout(90_000);
    const users = 3;

    // each "user" = own isolated context (own cookies/cache)
    const times = await Promise.all(
        Array.from({ length: users }, async () => {
            const context = await browser.newContext();
            const page = await context.newPage();
            const start = Date.now();
            await page.goto(URL, { waitUntil: 'load' });
            const ms = Date.now() - start;
            await context.close();
            return ms;
        })
    );

    const sorted = [...times].sort((a, b) => a - b);
    const p95 = sorted[Math.min(sorted.length - 1, Math.ceil(0.95 * sorted.length) - 1)];
    console.log({ times, p95 });

    expect(p95).toBeLessThan(15_000);
});

test('interaction speed: measure an action with performance.now()', async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc');
    const input = page.getByPlaceholder('What needs to be done?');

    const start = Date.now();
    for (let i = 0; i < 20; i++) {
        await input.fill(`todo ${i}`);
        await input.press('Enter');
    }
    await expect(page.getByTestId('todo-title')).toHaveCount(20);
    const ms = Date.now() - start;

    console.log(`added 20 todos in ${ms} ms`);
    expect(ms).toBeLessThan(10_000);
});
