## How to set up a proxy to not get banned for scrapping
  
[Article 1](https://multilogin.com/blog/7-effective-ways-for-web-scraping-without-getting-blocked/)
- Respect Robots.txt
- Use a Rotating Proxy
- Implement a Delay Between Requests

## Is it worth to create virtual environments for projects? (venv)
In JavaScript, the concept similar to Python's virtual environments is achieved through the use of package managers like npm or yarn, which manage dependencies specific to your project.

so the npm works like an virtual environment which makes sens because package.json holds all dependencies for the project cool

## Nested functions and chaining in javascript
``` 
function fetchData() {
  return new Promise((resolve, reject) => {
    // Perform some asynchronous operation here
    // For example, fetch data from an API
    // You can use the fetch() function or any other asynchronous operation

    // If the operation is successful, call resolve() with the result
    // If there is an error, call reject() with the error message

    // Example:
    fetch('https://api.example.com/data')
      .then(response => response.json())
      .then(data => {
        // Process the data or perform any other operations
        // ...

        // Call resolve() with the processed data
        resolve(data);
      })
      .catch(error => {
        // Handle the error or perform any other error handling logic
        // ...

        // Call reject() with the error message
        reject(error);
      });
  });
}

// Usage:
fetchData()
  .then(result => {
    // Handle the resolved result
    // ...

    // Example:
    console.log(result);
  })
  .catch(error => {
    // Handle the rejected error
    // ...

    // Example:
    console.error(error);
  });
``` 
- Nested Functions: This refers to functions defined within other functions. In your example, the anonymous function provided to new Promise and the callback functions provided to then and catch are all nested functions.

- Promise-Based Asynchronous Programming: The overall pattern uses Promises to handle asynchronous operations. The new Promise constructor allows you to perform asynchronous work inside it and resolve or reject based on the outcome. The then and catch methods are used to handle the resolved value or any errors that occur.

- Callback Functions: The functions passed to then and catch are callback functions, which are invoked when the Promise is resolved or rejected.

- Anonymous Functions: The functions defined within new Promise, then, and catch are anonymous functions because they are not named.

- Chaining: Promises can be chained together using then and catch to handle sequences of asynchronous operations in a readable manner.


## About asynchronous functions


### Promises: An Overview
A Promise is an object representing the eventual completion or failure of an asynchronous operation. It has three states:

Pending: Initial state, neither fulfilled nor rejected.
Fulfilled: The operation completed successfully.
Rejected: The operation failed.

```
async function getSiteData(url) {
  return new Promise(async (resolve, reject) => {
    try {
      const browser = await puppeteer.launch();
```

The promise object represents the eventual completion (or failure) of an asynchronous operation and its resulting value.
This is useful for controlling asynchronous workflows and ensuring that operations that depend on the completion of another operation can be properly sequenced.

### Install wsl to move on with executing bash scripts for example to clear all screenshots