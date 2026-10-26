import { test, expect } from '../fixtures-playwright';

// Uses every kind of fixture defined in fixtures-playwright.ts

test('Page Object fixture (todoPage)', async ({ todoPage }) => {
    await todoPage.addTodo('first');
    await todoPage.addTodo('second');

    await expect(todoPage.items).toHaveText(['first', 'second']);
});

test('worker fixture is the same inside one worker', async ({ workerId }) => {
    console.log('running in worker', workerId);
    expect(workerId).toBeGreaterThanOrEqual(0);
});

test.describe('option fixture overridden for a group', () => {
    // todoUrl is an option fixture, so test.use can change it
    test.use({ todoUrl: 'https://demo.playwright.dev/todomvc/#/active' });

    test('starts on the Active filter', async ({ todoPage, page }) => {
        await expect(page).toHaveURL(/#\/active/);
        await expect(todoPage.items).toHaveCount(0);
    });
});

test('auto fixture runs without being requested', async () => {
    // look at the terminal: START / END lines come from autoLog
    expect(1 + 1).toBe(2);
});
