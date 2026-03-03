import { test, expect } from "../fixtures/axe-test";

test.describe("RecipeKitsPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/food-bank/camden-food-bank/recipe-kits");
  });

  test("recipe cards are keyboard-navigable", async ({ page }) => {
    const selectBtns = page.getByRole("button", {
      name: /select this kit/i,
    });
    await expect(selectBtns.first()).toBeVisible();
    await selectBtns.first().focus();
    await expect(selectBtns.first()).toBeFocused();
  });

  test("ingredient lists use semantic ul", async ({ page }) => {
    const ingredientLists = page.locator(".recipe-card__ingredients ul");
    await expect(ingredientLists.first()).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
