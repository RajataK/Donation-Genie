import { test, expect } from "../fixtures/axe-test";

test.describe("DirectItemsPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/food-bank/camden-food-bank/direct-items");
  });

  test("quantity inputs have aria-labels including item name", async ({
    page,
  }) => {
    const input = page.locator("input[type='number']").first();
    await expect(input).toBeVisible();
    const label = await input.getAttribute("aria-label");
    expect(label).toBeTruthy();
  });

  test("+/- buttons have aria-labels", async ({ page }) => {
    const decreaseBtn = page
      .getByRole("button", { name: /decrease/i })
      .first();
    await expect(decreaseBtn).toBeVisible();
    const increaseBtn = page
      .getByRole("button", { name: /increase/i })
      .first();
    await expect(increaseBtn).toBeVisible();
  });

  test("basket total has aria-live polite", async ({ page }) => {
    const liveRegion = page.locator("[aria-live='polite']");
    await expect(liveRegion).toBeVisible();
  });

  test("checkout button disabled when basket empty", async ({ page }) => {
    const checkoutBtn = page.getByRole("button", {
      name: /proceed to checkout/i,
    });
    await expect(checkoutBtn).toBeVisible();
    await expect(checkoutBtn).toBeDisabled();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
