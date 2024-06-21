import { sleep } from '../helpers/sleep';
import { chromium } from '@playwright/test';
import { PageLogin } from './pages/login';

const fs = require('fs');
const fsExtra = require('fs-extra');

const testResultsPath = './test-results';

fsExtra.ensureDir(testResultsPath);
let browser;

export default async function globalSetup(config) {
  const { baseURL, storageState } = config.projects[0].use;

  fs.unlink(storageState, (err) => {
    if (err) {
      console.error(`No old storage_state file: ${err}`);
    } else {
      console.log('Storage_state file removed successfully');
    }
  });

  fs.unlink(loginLogFilePath, (err) => {
    if (err) {
      // Do nothing
    } else {
      // Do nothing
    }
  });

  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto(baseURL, { timeout: 60000 });
  await page.setViewportSize({ width: 1920, height: 1080 });

  try {
    await context.tracing.start({ screenshots: true, snapshots: true });

    for (let i = 0; i < 5; i++) {
      const loginPage = new PageLogin(page);

      await loginPage.login();

      await sleep(page, 2500);

      const navigationPage = new PageNavigation(page);
      const isWorklistEnabled =
        await navigationPage.navigationWorklist.isEnabled({ waitFor: 15000 });

      await page.context().storageState({
        path: storageState,
      });

      if (isWorklistEnabled) {
        console.log('Worklist button is enabled. Login was successful!');
        writeToLoginLogFile(
          'Login was successful!\n  - Worklist button is enabled!',
        );
        break;
      }

      console.log('Login failed!');
      writeToLoginLogFile('Login failed!');
    }

    await context.tracing.stop({
      path: `${testResultsPath}/setup-trace.zip`,
    });
    await browser.close();
  } catch (error) {
    await context.tracing.stop({
      path: `${testResultsPath}/failed-setup-trace.zip`,
    });
    await browser.close();
    throw error;
  }
}

const loginLogFilePath = `${testResultsPath}/login.txt`;

function writeToLoginLogFile(logLine) {
  const finalLogLine = `${new Date().toLocaleString()} - ${logLine}`;

  // Write to the log file
  fs.appendFile(loginLogFilePath, `${finalLogLine }\n`, (err) => {});
}

export { browser };
