import { test, expect } from '@playwright/test';

// Practice site made for automation: https://the-internet.herokuapp.com/login
test.describe('login form', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('https://the-internet.herokuapp.com/login');
    });

    test('wrong password shows an error message', async ({ page }) => {
        await page.getByLabel('Username').fill('tomsmith');
        await page.getByLabel('Password').fill('wrong-password');
        await page.getByRole('button', { name: 'Login' }).click();

        const flash = page.locator('#flash');
        await expect(flash).toBeVisible();
        await expect(flash).toContainText('Your password is invalid!');
        await expect(page).toHaveURL(/\/login$/); // still on the login page
    });

    test('wrong username shows a different error', async ({ page }) => {
        await page.getByLabel('Username').fill('nobody');
        await page.getByLabel('Password').fill('SuperSecretPassword!');
        await page.getByRole('button', { name: 'Login' }).click();

        await expect(page.locator('#flash')).toContainText('Your username is invalid!');
    });

    test('correct credentials log in', async ({ page }) => {
        await page.getByLabel('Username').fill('tomsmith');
        await page.getByLabel('Password').fill('SuperSecretPassword!');
        await page.getByRole('button', { name: 'Login' }).click();

        await expect(page).toHaveURL(/\/secure$/);
        await expect(page.locator('#flash')).toContainText('You logged into a secure area!');
    });
});
