import { test, expect } from '@playwright/test';

// codegen recorded Polish labels, so the browser must run in Polish too
test.use({ locale: 'pl-PL' });

test('test', async ({ page }) => {
  await page.goto('https://www.facebook.com/');
  await page.getByRole('button', { name: 'Zezwól na wszystkie pliki' }).click();
  await page.getByRole('textbox', { name: 'Adres e-mail lub numer' }).click();
  await page.getByRole('textbox', { name: 'Adres e-mail lub numer' }).fill('test@gmail.com');
  await page.getByRole('textbox', { name: 'Adres e-mail lub numer' }).press('Tab');
  await page.getByRole('textbox', { name: 'Hasło' }).fill('tstplaywright');
  await page.getByRole('button', { name: 'Zaloguj się' }).click();
  await expect(page.getByText('Podane hasło jest nieprawidłowe')).toBeVisible();
});