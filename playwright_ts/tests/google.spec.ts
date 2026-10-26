import { test, expect } from '../fixtures-playwright';

test('google.com opens', async ({ googlePage }) => {
    await expect(googlePage).toHaveTitle(/Google/);
});
