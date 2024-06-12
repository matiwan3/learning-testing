# Playwright

DOC: https://playwright.dev/

Setup:
npm init playwright@latest
Do you want to use TypeScript or JavaScript? · JavaScript
√ Where to put your end-to-end tests? · e2e
√ Add a GitHub Actions workflow? (y/N) · true
√ Install Playwright browsers (can be done manually via 'npx playwright install')? (Y/n) · true
Installing Playwright Test (npm install --save-dev @playwright/test)…









## Playwright methods and objects described down below 

# page object
In Playwright, the "page" object represents a single tab or window in a browser. It provides methods and properties to interact with the web page, such as navigating to URLs, clicking elements, filling forms, and extracting data. You can create a new page using the `browser.newPage()` method. Once you have a page object, you can perform various actions and assertions on it using the Playwright API.