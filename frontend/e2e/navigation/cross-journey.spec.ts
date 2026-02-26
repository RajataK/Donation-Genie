import { test, expect } from "@playwright/test";

test.describe("Cross-Journey Navigation", () => {
  test("switches from Donor Journey to Admin and back", async ({ page }) => {
    // Start on donor landing page
    await page.goto("/");
    const donorLink = page.getByRole("link", { name: /donor journey/i });
    const adminLink = page.getByRole("link", { name: /admin/i });

    // Donor Journey should be active on landing
    await expect(donorLink).toHaveAttribute("aria-current", "page");
    await expect(adminLink).not.toHaveAttribute("aria-current", "page");

    // Switch to Admin
    await adminLink.click();
    await expect(page).toHaveURL(/\/admin/);
    await expect(adminLink).toHaveAttribute("aria-current", "page");
    await expect(donorLink).not.toHaveAttribute("aria-current", "page");

    // Switch back to Donor
    await donorLink.click();
    await expect(page).toHaveURL("/");
    await expect(donorLink).toHaveAttribute("aria-current", "page");
  });

  test("navigates between admin pages", async ({ page }) => {
    await page.goto("/admin");
    await expect(
      page.getByRole("heading", { name: /welcome to donation genie/i }),
    ).toBeVisible();

    // Admin page should have admin link active
    const adminLink = page.getByRole("link", { name: /admin/i });
    await expect(adminLink).toHaveAttribute("aria-current", "page");
  });

  test("maintains navigation context after deep donor page", async ({
    page,
  }) => {
    // Navigate to a deep donor page
    await page.goto("/food-bank/camden-food-bank/direct-items");
    const donorLink = page.getByRole("link", { name: /donor journey/i });
    await expect(donorLink).toHaveAttribute("aria-current", "page");

    // Switch to admin from deep page
    const adminLink = page.getByRole("link", { name: /admin/i });
    await adminLink.click();
    await expect(page).toHaveURL(/\/admin/);
    await expect(adminLink).toHaveAttribute("aria-current", "page");
  });
});
