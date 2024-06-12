const { ENDPOINTS } = require('../constants/endpoints');
const ApiClient = require('../helpers/method-group-1');
const { test, expect, afterEach } = require('@playwright/test');

test('Test apiClient methods', async () => {
    const apiClient = new ApiClient();
    await apiClient.getOtomotoOffer();
});

test("Get otomotoCar", async ({ request }) => {
  const response = await request.get(ENDPOINTS.facebook);

  expect(response.status()).toBe(200);
  console.log(response.status());
  console.log(response.statusText());
  console.log(response.url());
  console.log(response.headers());
  console.log(response.body());
});