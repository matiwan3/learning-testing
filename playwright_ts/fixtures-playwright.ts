import { test as base, expect, Page } from '@playwright/test';

type MyFixtures = {
    googlePage: Page;
};

export const test = base.extend<MyFixtures>({
    googlePage: async ({ page }, use) => {
        // setup: runs before each test that uses this fixture
        const response = await page.goto('https://www.google.com');
        expect(response?.status()).toBe(200);

        await use(page);
    },
});

export { expect };
