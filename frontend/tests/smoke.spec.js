import { test, expect } from '@playwright/test'

test('home page renders navigation', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('link', { name: 'Проектирование API' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Теория' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Практика' })).toBeVisible()
})

test('theory block renders markdown content', async ({ page }) => {
  await page.goto('/theory')
  await expect(page.getByRole('heading', { name: 'Теория' })).toBeVisible()

  await page.getByText('Основы REST и HTTP-методы').first().click()
  await expect(page.getByRole('heading', { name: 'Основы REST и HTTP-методы' }).first()).toBeVisible()
  await expect(page.getByText('REST (Representational State Transfer)')).toBeVisible()
})

test('practice: incorrect then correct answer updates progress', async ({ page }) => {
  await page.goto('/practice')
  await expect(page.getByRole('heading', { name: 'Практика' })).toBeVisible()

  await page.getByText('Метод для частичного обновления').click()
  await expect(page.getByRole('heading', { name: 'Метод для частичного обновления' })).toBeVisible()

  // Submit a deliberately wrong answer first (provocative edge case: user
  // picks the "obviously wrong" GET option for a partial-update question).
  await page.getByText('GET', { exact: true }).click()
  await page.getByRole('button', { name: 'Проверить ответ' }).click()
  await expect(page.getByText('Неверно')).toBeVisible()

  await page.getByRole('button', { name: 'Попробовать снова' }).click()
  await page.getByText('PATCH', { exact: true }).click()
  await page.getByRole('button', { name: 'Проверить ответ' }).click()
  await expect(page.getByText('Верно!')).toBeVisible()

  await page.getByRole('link', { name: 'К списку заданий' }).click()
  await expect(page.getByText(/Решено 1 из 30/)).toBeVisible()
})

test('progress page shows aggregate stats table', async ({ page }) => {
  await page.goto('/progress')
  await expect(page.getByRole('heading', { name: 'Прогресс', exact: true })).toBeVisible()
  await expect(page.getByRole('heading', { name: 'Аналитика по всем участникам' })).toBeVisible()
  await expect(page.locator('table.stats-table')).toBeVisible()
})

test('practice: API_REQUEST task accepts a hand-written request', async ({ page }) => {
  await page.goto('/practice')
  await page.getByText('Запрос на полную замену ресурса').click()
  await expect(page.getByRole('heading', { name: 'Запрос на полную замену ресурса' })).toBeVisible()

  // Wrong method first (provocative edge case: PATCH instead of PUT for a
  // full-replace task).
  await page.locator('textarea').fill('PATCH /articles/15')
  await page.getByRole('button', { name: 'Проверить ответ' }).click()
  await expect(page.getByText('Неверно')).toBeVisible()

  await page.getByRole('button', { name: 'Попробовать снова' }).click()
  await page.locator('textarea').fill('PUT /articles/15')
  await page.getByRole('button', { name: 'Проверить ответ' }).click()
  await expect(page.getByText('Верно!')).toBeVisible()
})
