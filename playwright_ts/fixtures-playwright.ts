import { test as base, expect, Page, Locator } from '@playwright/test';

// Page Object: wraps selectors + actions for one page
class TodoPage {
    readonly input: Locator;
    readonly items: Locator;

    constructor(readonly page: Page) {
        this.input = page.getByPlaceholder('What needs to be done?');
        this.items = page.getByTestId('todo-title');
    }

    async addTodo(text: string) {
        await this.input.fill(text);
        await this.input.press('Enter');
    }
}

// per-test fixtures
type TestFixtures = {
    googlePage: Page;
    todoPage: TodoPage;
    todoUrl: string;
    autoLog: void;
};

// per-worker fixtures (created once per worker process)
type WorkerFixtures = {
    workerId: number;
};

export const test = base.extend<TestFixtures, WorkerFixtures>({
    // option fixture: can be overridden with test.use({ todoUrl: '...' }) or in playwright.config
    todoUrl: ['https://demo.playwright.dev/todomvc', { option: true }],

    // fixture that checks the HTTP status before the test body
    googlePage: async ({ page }, use) => {
        const response = await page.goto('https://www.google.com');
        expect(response?.status()).toBe(200);

        await use(page);
    },

    // fixture depending on other fixtures (page + todoUrl), returns a Page Object
    todoPage: async ({ page, todoUrl }, use) => {
        await page.goto(todoUrl);
        await use(new TodoPage(page));
    },

    // auto fixture: runs for every test, even when the test does not ask for it
    autoLog: [
        async ({}, use, testInfo) => {
            console.log(`START  ${testInfo.title}`);
            await use();
            console.log(`END    ${testInfo.title} -> ${testInfo.status} (${testInfo.duration}ms)`);
        },
        { auto: true },
    ],

    // worker-scoped fixture: setup once per worker, shared by its tests
    workerId: [
        async ({}, use, workerInfo) => {
            await use(workerInfo.workerIndex);
        },
        { scope: 'worker' },
    ],
});

export { expect };
