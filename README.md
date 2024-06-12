# Repo for creating a tests in various methodologies 

## Test types and tools
Blog: https://testerzy.pl/baza-wiedzy/narzedzia/10-najlepszych-narzedzi-do-testow-wydajnosci

# Unit tests
Unit testing is a software testing technique where individual units or components of a program are tested in isolation to ensure their correctness. It focuses on verifying the functionality of small, independent parts of the code.

Some popular frameworks and tools for unit testing include:
- JUnit (Java)
- NUnit (C#)
- pytest (Python)
- Mocha (JavaScript)
- PHPUnit (PHP)
- RSpec (Ruby)

These frameworks provide a set of assertions, test runners, and mocking/stubbing capabilities to facilitate the creation and execution of unit tests.

# Integration tests
Integration testing is a software testing technique where multiple components or modules of a system are combined and tested as a group to ensure their proper interaction and functionality. It focuses on verifying the integration and communication between different parts of the code.

Integration tests can be used to test various aspects such as API integrations, database interactions, and external service integrations.

Some popular frameworks and tools for integration testing include:
- Postman: A popular tool for testing APIs and performing integration tests by sending HTTP requests and validating responses.
- Selenium: A widely used framework for testing web applications that allows for the automation of browser interactions and can be used for integration testing.
- Apache Kafka: A distributed streaming platform that can be used for testing the integration and communication between different components of a system.
- WireMock: A tool for simulating HTTP-based APIs and services, which can be used for integration testing by mocking external dependencies.

Integration tests help ensure that the different components of a system work together correctly and can detect issues related to data flow, communication, and dependencies between modules.

# Functional tests
Functional testing is a software testing technique where the functionality of a system or application is tested against the specified requirements. It focuses on verifying that the system behaves as expected and meets the functional requirements.

Functional tests are typically written from a user's perspective and cover various scenarios to ensure that all features and functionalities are working correctly. These tests can include actions such as inputting data, interacting with user interfaces, and validating the expected outputs.

Some popular frameworks and tools for functional testing include:
- Selenium: A widely used framework for testing web applications that allows for the automation of browser interactions. It provides a rich set of features for writing and executing functional tests.
- Cypress: A JavaScript-based end-to-end testing framework that enables developers to write fast, reliable, and easy-to-understand functional tests for web applications.
- Appium: An open-source framework for automating mobile applications. It supports both Android and iOS platforms and allows for functional testing of mobile apps.
- Cucumber: A behavior-driven development (BDD) framework that enables collaboration between developers, testers, and business stakeholders. It allows for the creation of executable specifications in a human-readable format.

These frameworks and tools provide capabilities for writing and executing functional tests, generating test reports, and integrating with continuous integration/continuous delivery (CI/CD) pipelines.

# Complex tests
Complex tests are a type of software testing that involves testing intricate scenarios and interactions within a system. These tests go beyond simple functional or integration testing and focus on validating complex business logic, edge cases, and intricate workflows.

Complex tests often involve multiple components, dependencies, and interactions between different parts of the system. They aim to uncover potential issues related to data flow, error handling, concurrency, and performance under complex scenarios.

Some popular frameworks and tools for complex testing include:
- Apache JMeter: Although primarily known for performance testing, JMeter can also be used for complex testing scenarios. It allows for simulating complex user interactions, handling dynamic data, and validating intricate workflows.
- TestNG: A testing framework for Java that provides advanced features for complex testing scenarios. It supports data-driven testing, parallel test execution, and flexible test configuration.
- Cucumber: With its behavior-driven development (BDD) approach, Cucumber can be used for complex testing by defining and executing scenarios in a human-readable format. It enables collaboration between developers, testers, and business stakeholders.
- SoapUI: A widely used tool for testing SOAP and REST web services. It supports complex testing scenarios by allowing the creation of test cases with multiple steps, assertions, and data-driven testing.
- JUnit: Although primarily used for unit testing, JUnit can also be leveraged for complex testing. It provides a robust framework for writing and executing tests, including complex scenarios involving multiple test cases and assertions.

These frameworks and tools provide capabilities for designing, executing, and validating complex test scenarios. They help ensure the correctness and reliability of systems under intricate conditions.

# Acceptance tests
Acceptance testing is a software testing technique where the behavior and functionality of a system are tested against the business requirements and user expectations. It focuses on ensuring that the system meets the desired criteria and is ready for deployment.

Acceptance tests are typically written from a user's perspective and cover end-to-end scenarios to validate the system's functionality, usability, and compliance with business rules. These tests simulate real-world user interactions and validate the system's behavior in different scenarios.

Some popular frameworks and tools for acceptance testing include:
- Cucumber: A behavior-driven development (BDD) framework that enables collaboration between developers, testers, and business stakeholders. It allows for the creation of executable specifications in a human-readable format.
- Selenium: A widely used framework for testing web applications that allows for the automation of browser interactions. It provides a rich set of features for writing and executing acceptance tests.
- Robot Framework: An open-source test automation framework that uses a keyword-driven approach for acceptance testing. It supports various test libraries and can be used for testing web, desktop, and mobile applications.
- SpecFlow: A BDD framework for .NET that integrates with Visual Studio and allows for the creation of acceptance tests using Gherkin syntax.

These frameworks and tools provide capabilities for writing and executing acceptance tests, generating test reports, and integrating with continuous integration/continuous delivery (CI/CD) pipelines.

# Performance Tests  

Performance testing is a software testing technique used to evaluate the speed, responsiveness, stability, and scalability of a system under various workload conditions. It aims to identify performance bottlenecks, measure system performance metrics, and ensure that the system meets the desired performance requirements.

Performance tests simulate real-world scenarios and measure the system's response time, throughput, resource utilization, and scalability. These tests help identify performance issues such as slow response times, high resource consumption, memory leaks, and concurrency problems.

Some popular tools and frameworks used for performance testing include:

- Apache JMeter: A widely used open-source tool for load testing and performance measurement. It allows for simulating various types of requests, generating load, and analyzing performance metrics.

- Gatling: An open-source load testing framework written in Scala. It provides a high-performance engine for simulating large-scale load scenarios and supports scripting in a user-friendly DSL.

- LoadRunner: A commercial performance testing tool by Micro Focus. It offers a comprehensive set of features for load testing, including protocol support, load generation, and result analysis.

- Locust: An open-source load testing tool written in Python. It allows for defining user behavior using code and supports distributed load generation.

- BlazeMeter: A cloud-based load testing platform that integrates with popular testing tools and provides scalability for testing large-scale applications.

These tools and frameworks provide capabilities for load generation, performance monitoring, result analysis, and integration with CI/CD pipelines. They help identify performance bottlenecks, optimize system performance, and ensure that the system can handle expected workloads.

# Good testing practices

When it comes to naming files, variables, and classes, it's important to follow certain naming conventions to ensure code readability and maintainability. Here are some best practices:

File Names:
Use lowercase letters.
Separate words with hyphens or underscores.
Avoid using spaces or special characters.
Example: test-various-methods.js

Variable Names:
Use camelCase for variables and function names.
Start with a lowercase letter.
Choose descriptive and meaningful names.
Example: var myVariable = 10;

Class Names:
Use PascalCase for class names.
Start with an uppercase letter.
Choose descriptive and meaningful names.
Example: class MyClass { }

Remember, consistency is key. Stick to a naming convention throughout your codebase to make it more readable and maintainable.

## WebKit

WebKit is an open-source web browser engine that powers several popular web browsers, including Safari and some versions of Google Chrome. It provides the rendering capabilities necessary to display web content, including HTML, CSS, and JavaScript.

As the third default browser in Playwright, WebKit offers a reliable and efficient option for automated web testing. It supports the latest web standards and provides a fast and secure browsing experience.

When using Playwright, you can choose to run your tests in WebKit by specifying it as the browser option. This allows you to test your web applications across different browser engines and ensure compatibility and consistent behavior.

To use WebKit in Playwright, you can use the following code snippet:

```javascript
const { webkit } = require('playwright');

(async () => {
    const browser = await webkit.launch();
    const context = await browser.newContext();
    const page = await context.newPage();

    // Your test code here

    await browser.close();
})();
```

By leveraging WebKit in your Playwright tests, you can expand your test coverage and ensure that your web applications work seamlessly across different browsers and platforms.
