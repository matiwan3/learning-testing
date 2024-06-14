# Testing language - C#

C# is a powerful programming language that can also be used for testing purposes. It provides a rich set of features and frameworks for writing automated tests, making it a popular choice among developers.

To set up C# for testing in Visual Studio Code (VSC), you can follow these steps:

1. Install the .NET Core SDK: C# testing typically relies on the .NET Core framework. You can download and install the .NET Core SDK from the official Microsoft website.

2. Install the C# extension for VSC: Open VSC and navigate to the Extensions view (Ctrl+Shift+X). Search for "C#" and install the official C# extension by Microsoft.

3. Create a new test project: In VSC, open the Command Palette (Ctrl+Shift+P) and search for "dotnet new". Select the "Test Project" template to create a new test project.

4. Write your tests: Once the project is created, you can start writing your tests using a testing framework like NUnit, xUnit, or MSTest. You can create test classes and methods, and use various assertions and test attributes provided by the chosen testing framework.

5. Run your tests: To run your tests, open the integrated terminal in VSC (Ctrl+`) and navigate to the root folder of your test project. Use the "dotnet test" command to execute all the tests in your project.

- To initialize new c# project use:
    ```
    dotnet new console -o app
    ```
- Use ctrl + shift + P and choose: ".NET generate assets for build and debug"
- To build the project use:
    ```
    dotnet build
    ```
- To run particular file use:
    ```
    dotnet run [filename]
    ``` 