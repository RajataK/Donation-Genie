import { test, expect } from "../fixtures/axe-test";

test.describe("SearchResultsPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/search?postcode=SW1A+1AA");
  });

  test("has AI summary section with aria-label", async ({ page }) => {
    const summary = page.locator('[aria-label="AI-generated needs summary"]');
    await expect(summary).toBeVisible();
  });

  test("has food bank cards in list markup", async ({ page }) => {
    const items = page.locator(".search-results__list li");
    await expect(items).toHaveCount(3);
  });

  test("urgency badges have aria-labels", async ({ page }) => {
    const badges = page.locator("[aria-label*='Urgency level']");
    await expect(badges.first()).toBeVisible();
  });

  test("food bank cards are keyboard-focusable", async ({ page }) => {
    const selectButtons = page.getByRole("button", {
      name: /select this food bank/i,
    });
    await expect(selectButtons.first()).toBeVisible();
    await selectButtons.first().focus();
    await expect(selectButtons.first()).toBeFocused();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
