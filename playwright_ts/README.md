# Table of Contents

- [Table of Contents](#table-of-contents)
- [Playwright (づ￣ 3￣)づ](#playwright-づ-3づ)
  - [Playwright methods and objects described down below](#playwright-methods-and-objects-described-down-below)
    - [page object](#page-object)
    - [Difference between import and require](#difference-between-import-and-require)
  - [Playwright docs](#playwright-docs)
    - [Writing tests](#writing-tests)
    - [Test Isolation](#test-isolation)
    - [Test Fixtures](#test-fixtures)
    - [Best practices](#best-practices)

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

### Difference between import and require

In JavaScript, `import` and `require` are both used to import external modules or files into your code. However, there are some key differences between them:

- `require` is a CommonJS syntax used in Node.js, while `import` is an ES6 syntax used in modern JavaScript environments.

- `require` is a synchronous function, meaning that it blocks the execution of the code until the required module is loaded. On the other hand, `import` is asynchronous and allows for more efficient loading of modules.

- `require` is used to import the entire module or file, while `import` allows you to selectively import specific parts of a module using named imports or default imports.

- `require` uses `module.exports` to export modules, while `import` uses `export` and `export default` to export modules.

- `import` supports static analysis, which means that the imported modules are resolved at compile-time, allowing for better optimization and tree-shaking. `require` does not have this feature.

Overall, `import` is the recommended syntax for importing modules in modern JavaScript projects, especially in browser environments. However, `require` is still widely used in Node.js and older JavaScript codebases.

## Playwright docs

### Writing tests

### Test Isolation
Playwright Test is based on the concept of **test fixtures** such as the built in page fixture, which is passed into your test. Pages are isolated between tests due to the Browser Context, which is equivalent to a brand new browser profile, where every test gets a fresh environment, even when multiple tests run in a single Browser.

### Test Fixtures

In Playwright Test, test fixtures are a way to set up and tear down the environment for your tests. They provide a clean and isolated context for each test, ensuring that tests run in a consistent and predictable state.

One of the built-in test fixtures in Playwright Test is the `page` fixture. This fixture provides a new browser page for each test, allowing you to interact with the web page and perform actions specific to that test.

To use the `page` fixture, you can simply include it as a parameter in your test function. Playwright Test will automatically create a new page and pass it to your test function.

```javascript
const { test, expect } = require('@playwright/test');

test('Example test', async ({ page }) => {
        // Use the 'page' fixture to interact with the web page
        await page.goto('https://example.com');
        const title = await page.title();
        
        // Perform assertions using the 'expect' function
        expect(title).toBe('Example Domain');
});
```

By using test fixtures, you can easily set up the necessary environment for your tests, such as launching a browser, navigating to a specific URL, or logging in to a user account. This ensures that each test starts from a known state and can be executed independently.

Test fixtures can also be customized and extended to fit your specific testing needs. You can create your own fixtures by defining functions or classes that set up the desired environment for your tests.

Overall, test fixtures in Playwright Test provide a powerful mechanism for managing the test environment and ensuring test isolation. They help you write clean, maintainable, and reliable tests for your web applications.

### <a href="https://playwright.dev/docs/best-practices">Best practices</a>

**Test user-visible behavior**
Automated tests should verify that the application code works for the end users, and avoid relying on implementation details such as things which users will not typically use, see, or even know about such as the name of a function, whether something is an array, or the CSS class of some element. The end user will see or interact with what is rendered on the page, so your test should typically only see/interact with the same rendered output.

**Make tests as isolated as possible**
Each test should be completely isolated from another test and should run independently with its own local storage, session storage, data, cookies etc. Test isolation improves reproducibility, makes debugging easier and prevents cascading test failures.

**Testing with a database**
If working with a database then make sure you control the data. Test against a staging environment and make sure it doesn't change. For visual regression tests make sure the operating system and browser versions are the same.

**Use locators**
In order to write end to end tests we need to first find elements on the webpage. We can do this by using Playwright's built in locators. Locators come with auto waiting and retry-ability. Auto waiting means that Playwright performs a range of actionability checks on the elements, such as ensuring the element is visible and enabled before it performs the click. To make tests resilient, we recommend prioritizing user-facing attributes and explicit contracts.

**Use web first assertions**
Assertions are a way to verify that the expected result and the actual result matched or not. By using web first assertions Playwright will wait until the expected condition is met. For example, when testing an alert message, a test would click a button that makes a message appear and check that the alert message is there. If the alert message takes half a second to appear, assertions such as toBeVisible() will wait and retry if needed.

**Use Soft assertions**
If your test fails, Playwright will give you an error message showing what part of the test failed which you can see either in VS Code, the terminal, the HTML report, or the trace viewer. However, you can also use soft assertions. These do not immediately terminate the test execution, but rather compile and display a list of failed assertions once the test ended.