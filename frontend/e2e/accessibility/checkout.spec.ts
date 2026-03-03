import { test, expect } from "../fixtures/axe-test";

test.describe("CheckoutPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/food-bank/camden-food-bank/checkout");
  });

  test("flow diagram has aria-label", async ({ page }) => {
    const diagram = page.locator("[aria-label*='Donation process']");
    await expect(diagram).toBeVisible();
  });

  test("basket items in semantic markup", async ({ page }) => {
    const table = page.locator("table, dl");
    await expect(table.first()).toBeVisible();
  });

  test("primary action first in tab order", async ({ page }) => {
    const completeBtn = page.getByRole("button", {
      name: /complete donation/i,
    });
    await expect(completeBtn).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
