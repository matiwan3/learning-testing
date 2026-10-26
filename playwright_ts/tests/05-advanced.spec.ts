import { test, expect } from '@playwright/test';

// Advanced features. Most tests use page.setContent so they are self-contained.

test('test.step groups actions in the report', async ({ page }) => {
    await test.step('open page', async () => {
        await page.goto('https://demo.playwright.dev/todomvc');
    });
    await test.step('add a todo', async () => {
        await page.getByPlaceholder('What needs to be done?').fill('step demo');
        await page.keyboard.press('Enter');
    });
    await test.step('verify', async () => {
        await expect(page.getByTestId('todo-title')).toHaveText('step demo');
    });
});

test('handle a dialog (alert/confirm)', async ({ page }) => {
    await page.setContent(`<button onclick="alert('are you sure?')">go</button>`);

    let message = '';
    page.once('dialog', async (dialog) => {
        message = dialog.message();
        await dialog.accept();
    });
    await page.getByRole('button', { name: 'go' }).click();

    expect(message).toBe('are you sure?');
});

test('handle a popup / new tab', async ({ page }) => {
    await page.setContent(`<button onclick="window.open('about:blank')">open</button>`);

    const [popup] = await Promise.all([
        page.waitForEvent('popup'),
        page.getByRole('button', { name: 'open' }).click(),
    ]);

    expect(popup.url()).toBe('about:blank');
    await popup.close();
});

test('work inside an iframe', async ({ page }) => {
    await page.setContent(`<iframe srcdoc="<button>inside</button>"></iframe>`);

    await expect(page.frameLocator('iframe').getByRole('button', { name: 'inside' })).toBeVisible();
});

test('cookies and storage', async ({ context, page }) => {
    await context.addCookies([{ name: 'token', value: 'abc', url: 'https://demo.playwright.dev' }]);
    await page.goto('https://demo.playwright.dev/todomvc');

    const cookies = await context.cookies();
    expect(cookies.find((c) => c.name === 'token')?.value).toBe('abc');

    await page.evaluate(() => localStorage.setItem('theme', 'dark'));
    expect(await page.evaluate(() => localStorage.getItem('theme'))).toBe('dark');
});

test('expect.poll retries a value, toPass retries a block', async ({ page }) => {
    await page.setContent(`<div id="n">0</div>
        <script>let i = 0; setInterval(() => { document.getElementById('n').textContent = ++i }, 100)</script>`);

    await expect
        .poll(async () => Number(await page.locator('#n').textContent()), { timeout: 5000 })
        .toBeGreaterThan(3);

    await expect(async () => {
        const text = await page.locator('#n').textContent();
        expect(Number(text)).toBeGreaterThan(5);
    }).toPass({ timeout: 5000 });
});

test('run JS in the page and attach a screenshot to the report', async ({ page }, testInfo) => {
    await page.goto('https://playwright.dev');

    const links = await page.evaluate(() => document.querySelectorAll('a').length);
    expect(links).toBeGreaterThan(5);

    await testInfo.attach('home', {
        body: await page.screenshot(),
        contentType: 'image/png',
    });
});

// tags: run only these with `npx playwright test --grep @smoke`
test('tagged test', { tag: '@smoke' }, async ({ page }) => {
    await page.goto('https://playwright.dev');
    await expect(page).toHaveTitle(/Playwright/);
});

// annotations: skip / fixme / slow / conditional
test('conditional skip', async ({ browserName }) => {
    test.skip(browserName === 'webkit', 'not relevant for webkit');
    expect(browserName).not.toBe('webkit');
});

test('slow test gets triple timeout', async ({ page }) => {
    test.slow();
    await page.goto('https://playwright.dev');
});

// emulation: mobile viewport, locale, geolocation, dark mode
test.describe('emulation', () => {
    test.use({
        viewport: { width: 390, height: 844 },
        locale: 'pl-PL',
        colorScheme: 'dark',
    });

    test('mobile + Polish + dark mode', async ({ page }) => {
        await page.goto('https://playwright.dev');

        expect(await page.evaluate(() => navigator.language)).toBe('pl-PL');
        expect(await page.evaluate(() => matchMedia('(prefers-color-scheme: dark)').matches)).toBe(true);
        expect(page.viewportSize()?.width).toBe(390);
    });
});

// serial: tests share state and run in order; if one fails the rest are skipped
test.describe.serial('serial flow', () => {
    let value = 0;

    test('step 1', () => {
        value = 1;
    });
    test('step 2', () => {
        expect(value).toBe(1);
    });
});
