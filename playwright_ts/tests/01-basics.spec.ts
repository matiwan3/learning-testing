import { test, expect } from '@playwright/test';

// Basics: locators, actions, assertions, hooks. Site: TodoMVC demo.
test.describe('basics', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
    });

    test('add todos and assert list', async ({ page }) => {
        const input = page.getByPlaceholder('What needs to be done?'); // locator by placeholder

        await input.fill('buy milk');
        await input.press('Enter');
        await input.fill('learn playwright');
        await input.press('Enter');

        const titles = page.getByTestId('todo-title'); // locator by data-testid
        await expect(titles).toHaveCount(2);
        await expect(titles).toHaveText(['buy milk', 'learn playwright']);
    });

    test('complete a todo and use filters', async ({ page }) => {
        const input = page.getByPlaceholder('What needs to be done?');
        for (const text of ['one', 'two', 'three']) {
            await input.fill(text);
            await input.press('Enter');
        }

        // filter(): narrow down a list of locators, then chain into the item
        await page
            .getByTestId('todo-item')
            .filter({ hasText: 'two' })
            .getByRole('checkbox')
            .check();

        await page.getByRole('link', { name: 'Completed' }).click(); // locator by role + name
        await expect(page.getByTestId('todo-title')).toHaveText(['two']);

        await page.getByRole('link', { name: 'Active' }).click();
        await expect(page.getByTestId('todo-title')).toHaveText(['one', 'three']);
    });

    test('edit a todo with double click', async ({ page }) => {
        await page.getByPlaceholder('What needs to be done?').fill('old name');
        await page.keyboard.press('Enter');

        await page.getByTestId('todo-title').dblclick();
        await page.getByRole('textbox', { name: 'Edit' }).fill('new name');
        await page.keyboard.press('Enter');

        await expect(page.getByTestId('todo-title')).toHaveText('new name');
    });

    test('soft assertions do not stop the test', async ({ page }) => {
        // all soft failures are reported at the end, the test keeps running
        await expect.soft(page).toHaveTitle(/TodoMVC/);
        await expect.soft(page.getByRole('heading', { name: 'todos' })).toBeVisible();
        await expect.soft(page.getByTestId('todo-title')).toHaveCount(0);
    });

    test('counter text updates', async ({ page }) => {
        const input = page.getByPlaceholder('What needs to be done?');
        await input.fill('a');
        await input.press('Enter');

        // auto-retrying assertion: waits until it passes or times out
        await expect(page.getByTestId('todo-count')).toHaveText('1 item left');
    });
});
