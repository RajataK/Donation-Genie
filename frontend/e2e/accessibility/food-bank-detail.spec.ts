import { test, expect } from "../fixtures/axe-test";

test.describe("FoodBankDetailPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/food-bank/camden-food-bank");
  });

  test("has proper heading hierarchy", async ({ page }) => {
    const h1 = page.locator("h1");
    await expect(h1).toBeVisible();
    const h2 = page.locator("h2");
    await expect(h2.first()).toBeVisible();
  });

  test("has impact story section", async ({ page }) => {
    const story = page.locator("[data-testid='impact-story']");
    await expect(story).toBeVisible();
  });

  test("wish list items include urgency in accessible name", async ({
    page,
  }) => {
    const badges = page.locator("[aria-label*='Urgency level']");
    await expect(badges.first()).toBeVisible();
  });

  test("donation options have role group with aria-label", async ({ page }) => {
    const group = page.locator("[role='group'][aria-label]");
    await expect(group).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
