import { test, expect } from '@playwright/test';

// Network: mocking, blocking, waiting for responses, listening to events

const API = 'https://jsonplaceholder.typicode.com';

test('mock an API response with route.fulfill', async ({ page }) => {
    await page.route(`${API}/todos/1`, (route) =>
        route.fulfill({
            status: 200,
            headers: { 'access-control-allow-origin': '*' }, // needed: fetch is cross-origin
            json: { id: 1, title: 'mocked title', completed: true },
        })
    );

    await page.goto('https://demo.playwright.dev/todomvc');
    const data = await page.evaluate((url) => fetch(url).then((r) => r.json()), `${API}/todos/1`);

    expect(data.title).toBe('mocked title');
});

test('block images with route.abort', async ({ page }) => {
    let blocked = 0;
    await page.route('**/*.{png,jpg,jpeg,svg,webp}', (route) => {
        blocked++;
        return route.abort();
    });

    await page.goto('https://playwright.dev');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

    console.log('blocked image requests:', blocked);
    expect(blocked).toBeGreaterThan(0);
});

test('wait for a specific response', async ({ page }) => {
    await page.goto('https://demo.playwright.dev/todomvc');

    // start waiting BEFORE the action that triggers the request
    const [response] = await Promise.all([
        page.waitForResponse((r) => r.url().includes('/todos/2')),
        page.evaluate((url) => fetch(url), `${API}/todos/2`),
    ]);

    expect(response.status()).toBe(200);
    expect((await response.json()).id).toBe(2);
});

test('listen to page events (requests, console, errors)', async ({ page }) => {
    const requests: string[] = [];
    const consoleMessages: string[] = [];
    const failed: string[] = [];

    page.on('request', (req) => requests.push(req.url()));
    page.on('console', (msg) => consoleMessages.push(msg.text()));
    page.on('requestfailed', (req) => failed.push(req.url()));

    await page.goto('https://playwright.dev');
    await page.evaluate(() => console.log('hello from the browser'));

    expect(requests.length).toBeGreaterThan(0);
    expect(consoleMessages).toContain('hello from the browser');
    expect(failed).toHaveLength(0);
});

test('modify a real response (route.fetch + fulfill)', async ({ page }) => {
    await page.route(`${API}/todos/3`, async (route) => {
        const real = await route.fetch(); // call the real server
        const body = await real.json();
        body.title = 'changed by test';
        await route.fulfill({
            response: real,
            json: body,
            headers: { ...real.headers(), 'access-control-allow-origin': '*' },
        });
    });

    await page.goto('https://demo.playwright.dev/todomvc');
    const data = await page.evaluate((url) => fetch(url).then((r) => r.json()), `${API}/todos/3`);

    expect(data.id).toBe(3);
    expect(data.title).toBe('changed by test');
});
