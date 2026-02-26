import { test, expect } from "../fixtures/axe-test";

test.describe("LandingPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("has h1 with application name", async ({ page }) => {
    const h1 = page.locator("h1");
    await expect(h1).toBeVisible();
    await expect(h1).toContainText("Donation Genie");
  });

  test("has labeled postcode input", async ({ page }) => {
    const input = page.getByLabel(/postcode/i);
    await expect(input).toBeVisible();
  });

  test("has search button with descriptive text", async ({ page }) => {
    const button = page.getByRole("button", { name: /find local food banks/i });
    await expect(button).toBeVisible();
  });

  test("has main landmark", async ({ page }) => {
    const main = page.locator("main");
    await expect(main).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
