const users = [
  { username: "user1", password: "pass123" },
  { username: "user2", password: "pass456" },
  { username: "user3", password: "pass789" }
];

test("User Login", () => {
  // Test valid credentials
  console.log('testing valid usernames and passwords');
  expect(login("user1", "pass123")).toBe(true);
  expect(login("user2", "pass456")).toBe(true);
  expect(login("user3", "pass789")).toBe(true);

  // Test invalid credentials
  expect(login("user1", "wrongpass")).toBe(false);
  expect(login("wronguser", "pass123")).toBe(false);
  expect(login("wronguser", "wrongpass")).toBe(false);
});

function login(username, password) {
  const user = users.find(user => user.username === username && user.password === password);
  return !!user;
}