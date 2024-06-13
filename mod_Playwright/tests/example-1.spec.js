// @ts-check | is a directive that enables TypeScript checking in the file.
import { test, expect, afterEach, beforeEach } from '@playwright/test';

beforeEach(async () => {
  console.log('[+] Executing before each test...');
});

afterEach(async ({ page }) => {
  console.log('[+] Executing after each test...');
  await page.close();
});

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Playwright/);
});

test('get started link', async ({ page }) => {
  await page.goto('https://playwright.dev/');
  await expect(page).toHaveTitle(/Playwright/);

  // Click the get started link.
  await page.getByRole('link', { name: 'Get started' }).click();

  // Expects page to have a heading with the name of Installation.
  await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});
