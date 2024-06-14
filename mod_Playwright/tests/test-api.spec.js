import { url } from '../constants/urls';
import ApiClient from '../helpers/method-group-1';
import { test, expect } from '@playwright/test';

test('Test apiClient methods', async () => {
  const apiClient = new ApiClient();

  await apiClient.getOtomotoOffer();
});

test.skip('Get otomoto Car', async ({ request }) => {
  const response = await request.get(url.facebook);

  expect(response.status()).toBe(200);
  console.log(response.status());
  console.log(response.statusText());
  console.log(response.url());
  console.log(response.headers());
  console.log(response.body());
});
