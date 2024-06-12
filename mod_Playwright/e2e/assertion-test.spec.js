const {test, expect, beforeEach, afterEach} = require('@playwright/test');
const { DevPage } = require('../pages/playwright/dev');

test.describe('Test assertion methods', () => {
    beforeEach(async ({ page }) => {
        console.log('[+] Executing before each test');
        const devPage = new DevPage(page);
        await devPage.goto();
    });

    afterEach(async ({ page }) => {
        console.log('[+] Executing after each test');
        await page.close();
    });

    test('[TEST no. 1] Auto-retrying assertions', async () => {
        expect(true).toBeTruthy();
    });

    test('[TEST no. 2] Non-retrying assertions', async () => {
        expect(1).toBe(1);
    });
});
