import { test, expect } from '@playwright/test';
import fs from 'fs';

test.describe('Testing database files', () => {
  test.beforeEach(async() => {
    console.log('Executing before each');
    const dbFilePath = 'test_files/test.db';

    fs.writeFileSync(dbFilePath, '');
  });

  test.afterEach(async() => {
    console.log('Executing after each');
    const dbFilePath = 'test_files/test.db';

    fs.unlinkSync(dbFilePath);
  });

  test('[TEST no. 1] Test database connection', async({ page }) => {
    console.log('Executing test 1');
    await page.goto('https://youtube.com');
    expect(await page.textContent('title')).toMatchSnapshot({ path: "__snapshots__/test-database.spec.js.snap" });

  });
});
