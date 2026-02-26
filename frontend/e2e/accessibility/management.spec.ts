import { test, expect } from "../fixtures/axe-test";

test.describe("ManagementPage Accessibility @a11y", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/admin/management");
  });

  test("checkboxes have associated labels", async ({ page }) => {
    const checkboxes = page.getByRole("checkbox");
    const first = checkboxes.first();
    await expect(first).toBeVisible();
    const id = await first.getAttribute("id");
    if (id) {
      const label = page.locator(`label[for='${id}']`);
      await expect(label).toBeVisible();
    }
  });

  test("sections use fieldset and legend", async ({ page }) => {
    const fieldset = page.locator("fieldset");
    await expect(fieldset.first()).toBeVisible();
    const legend = page.locator("legend");
    await expect(legend.first()).toBeVisible();
  });

  test("has no WCAG AA violations", async ({ page, makeAxeBuilder }) => {
    const results = await makeAxeBuilder().analyze();
    expect(results.violations).toEqual([]);
  });
});
