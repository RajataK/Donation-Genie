import { test, expect } from "../fixtures/axe-test";

test.describe("OnboardingPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/admin");
  });

  test("upload zone has aria-label and action button", async ({ page }) => {
    const zone = page.locator("[aria-label*='Upload wish list']");
    await expect(zone).toBeVisible();
    const chooseFile = page.getByRole("button", { name: /choose file/i });
    await expect(chooseFile).toBeVisible();
  });

  test("extracted items grid uses semantic list markup", async ({ page }) => {
    const list = page.locator("[data-testid='extracted-items'] ul");
    await expect(list).toBeVisible();
  });

  test("action buttons have descriptive labels", async ({ page }) => {
    const confirm = page.getByRole("button", { name: /confirm/i });
    await expect(confirm).toBeVisible();
    const edit = page.getByRole("button", { name: /edit/i });
    await expect(edit).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
