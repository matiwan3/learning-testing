import { test, expect, beforeEach, afterEach } from '@playwright/test';
import { DevPage } from '../pages/playwright/dev';

// DOC: https://playwright.dev/docs/test-assertions
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

  test.skip('[TEST no. 1] Auto-retrying assertions', async ({ page }) => {
    let locator = 'TO BE DEFINED';

    expect(true).toBeTruthy();
    await expect(locator).toBeAttached(); // Element is attached
    await expect(locator).toBeChecked(); // Element is checked
    await expect(locator).toBeDisabled(); // Element is disabled
    await expect(locator).toBeEditable(); // Element is editable
    await expect(locator).toBeEmpty(); // Element is empty
    await expect(locator).toBeEnabled(); // Element is enabled
    await expect(locator).toBeFocused(); // Element is focused
    await expect(locator).toBeInViewport(); // Element is in the viewport
    await expect(locator).toBeVisible(); // Element is visible
    await expect(locator).toContainText('text'); // Element contains text
    await expect(locator).toHaveAccessibleDescription('description'); // Element has accessible description
    await expect(locator).toHaveAccessibleName('name'); // Element has accessible name
    await expect(locator).toHaveAttribute('name', 'value'); // Element has attribute
    await expect(locator).toHaveClass('class'); // Element has class
    await expect(locator).toHaveCount(1); // List has exact number of children
    await expect(locator).toHaveCSS('style', 'value'); // Element has CSS property
    await expect(locator).toHaveId('id'); // Element has id
    await expect(locator).toHaveScreenshot('screenshot.png'); // Element has screenshot
    await expect(locator).toHaveText('text'); // Element has text
    await expect(locator).toHaveValue('value'); // Element has value
    await expect(page).toHaveScreenshot('screenshot.png'); // Page has screenshot
    await expect(page).toHaveTitle('title'); // Page has title
    await expect(page).toHaveURL('url'); // Page has URL
    await expect(response).toBeOK(); // Response is OK
  });

  test('[TEST no. 2] Non-retrying assertions', async () => {
    expect(1).toBe(1);
    expect(2).toBeCloseTo(2.1, 0.2); // Number is close to another number in a given range
  });

  test('[TEST no. 3] Dynamic assertions', async () => {
    expect(1).toBe(1);
    for (let i = 0; i < 10; i++) {
      console.log('Iteration:', i);
      expect(i).toBeLessThan(10);
    }
  });

  test('[TEST no. 4] DevPage assertions', async ({ page }) => {
    let pageTitle = await page.title();
    let pageUrl = await page.url();

    console.log(`[*] Page title: ${pageTitle} for URL: ${pageUrl}`);
    await expect(page).toHaveTitle(pageTitle);
  });
});
