const users = [
  { username: 'user1', password: 'pass123' },
  { username: 'user2', password: 'pass456' },
  { username: 'user3', password: 'pass789' },
];

test('User Login', () => {
  // Test valid credentials
  console.log('testing valid usernames and passwords');
  expect(login('user1', 'pass123')).toBe(true);
  expect(login('user2', 'pass456')).toBe(true);
  expect(login('user3', 'pass789')).toBe(true);

  // Test invalid credentials
  expect(login('user1', 'wrongpass')).toBe(false);
  expect(login('wronguser', 'pass123')).toBe(false);
  expect(login('wronguser', 'wrongpass')).toBe(false);
});

function login(username, password) {
  const user = users.find((user) => user.username === username && user.password === password);

  return !!user;
  // Truthy values in JavaScript include non-empty strings, numbers other than 0, arrays, objects, and functions. Falsy values include null, undefined, false, 0, an empty string (""), and NaN.
  // So, the code snippet is checking whether the variable user has a truthy value and will return true if it does, and false if it doesn't.
}
