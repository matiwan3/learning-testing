/**
 * @description Sleep using the waitForTimeout function in Playwright
 * @param {import('@playwright/test').Page} page
 * @param {number} milliseconds
 */
export async function sleep(page, milliseconds) {
  await page.waitForTimeout(milliseconds);
}
