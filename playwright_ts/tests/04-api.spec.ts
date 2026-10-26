import { test, expect } from '@playwright/test';

// API testing: the `request` fixture needs no browser.
test.use({ baseURL: 'https://jsonplaceholder.typicode.com' });

test('GET a resource', async ({ request }) => {
    const response = await request.get('/posts/1');

    expect(response.ok()).toBeTruthy();
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toContain('application/json');

    const body = await response.json();
    expect(body).toMatchObject({ id: 1, userId: 1 });
});

test('POST creates a resource', async ({ request }) => {
    const response = await request.post('/posts', {
        data: { title: 'hello', body: 'world', userId: 7 },
    });

    expect(response.status()).toBe(201);
    expect(await response.json()).toMatchObject({ title: 'hello', userId: 7 });
});

test('query params and list assertions', async ({ request }) => {
    const response = await request.get('/comments', { params: { postId: 1 } });
    const comments = await response.json();

    expect(comments.length).toBeGreaterThan(0);
    for (const c of comments) {
        expect(c.postId).toBe(1);
    }
});

test('404 for a missing resource', async ({ request }) => {
    const response = await request.get('/posts/99999');
    expect(response.status()).toBe(404);
});

// data-driven: one test per row
const ids = [1, 2, 3];
for (const id of ids) {
    test(`post ${id} has a title`, async ({ request }) => {
        const post = await (await request.get(`/posts/${id}`)).json();
        expect(post.title.length).toBeGreaterThan(0);
    });
}
