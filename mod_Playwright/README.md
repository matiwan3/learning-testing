# Playwright (づ￣ 3￣)づ

Playwright is a powerful automation framework for web browsers. It allows you to write end-to-end tests and perform browser automation tasks with ease. With Playwright, you can interact with web pages, navigate to URLs, click elements, fill forms, extract data, and much more.

Playwright supports multiple browsers, including Chromium, Firefox, and WebKit, allowing you to test your web applications across different browser engines. It provides a unified API that works consistently across all supported browsers, making it easy to write and maintain your tests.

One of the key features of Playwright is its ability to run tests in parallel, which can significantly reduce the overall test execution time. It also integrates well with popular testing frameworks like Jest and Mocha, making it seamless to incorporate Playwright into your existing test suites.

Whether you are performing end-to-end testing, automating repetitive tasks, or scraping data from websites, Playwright is a versatile framework that can help you achieve your goals efficiently.

For more information and detailed documentation, please refer to the [Playwright website](https://playwright.dev/).


DOC: https://playwright.dev/

Setup:
npm init playwright@latest
Do you want to use TypeScript or JavaScript? · JavaScript  
√ Where to put your end-to-end tests? · e2e   
√ Add a GitHub Actions workflow? (y/N) · true  
√ Install Playwright browsers (can be done manually via 'npx playwright install')? (Y/n) · true  
Installing Playwright Test (npm install --save-dev @playwright/test)…  

## Playwright methods and objects described down below

### page object
In Playwright, the "page" object represents a single tab or window in a browser. It provides methods and properties to interact with the web page, such as navigating to URLs, clicking elements, filling forms, and extracting data. You can create a new page using the `browser.newPage()` method. Once you have a page object, you can perform various actions and assertions on it using the Playwright API.
