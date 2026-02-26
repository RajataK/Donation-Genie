import { test, expect } from "@playwright/test";

test.describe("Donor Journey Navigation", () => {
  // US1: Landing → Search Results → Food Bank Detail
  test.describe("US1: Postcode search to food bank selection", () => {
    test("navigates from landing to search results", async ({ page }) => {
      await page.goto("/");
      await page.getByLabel(/postcode/i).fill("SW1A 1AA");
      await page
        .getByRole("button", { name: /find local food banks/i })
        .click();
      await expect(page).toHaveURL(/\/search\?postcode=/);
    });

    test("navigates from search results to food bank detail", async ({
      page,
    }) => {
      await page.goto("/search?postcode=SW1A+1AA");
      await page
        .getByRole("button", { name: /select this food bank/i })
        .first()
        .click();
      await expect(page).toHaveURL(/\/food-bank\//);
    });
  });

  // US2: Food Bank Detail → Direct Items / Recipe Kits
  test.describe("US2: Donation method selection", () => {
    test("navigates to direct items", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank");
      await page
        .getByRole("link", { name: /donate individual items/i })
        .click();
      await expect(page).toHaveURL(
        /\/food-bank\/camden-food-bank\/direct-items/,
      );
    });

    test("navigates to recipe kits", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank");
      await page.getByRole("link", { name: /recipe kits/i }).click();
      await expect(page).toHaveURL(
        /\/food-bank\/camden-food-bank\/recipe-kits/,
      );
    });
  });

  // US3: Direct Items → Checkout
  test.describe("US3: Direct items to checkout", () => {
    test("navigates from direct items to checkout", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank/direct-items");
      // Add an item first
      await page.getByRole("button", { name: /add/i }).first().click();
      await page
        .getByRole("button", { name: /proceed to checkout/i })
        .click();
      await expect(page).toHaveURL(
        /\/food-bank\/camden-food-bank\/checkout/,
      );
    });
  });

  // US4: Recipe Kits → Checkout
  test.describe("US4: Recipe kit to checkout", () => {
    test("navigates from recipe kits to checkout", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank/recipe-kits");
      await page
        .getByRole("button", { name: /select this kit/i })
        .first()
        .click();
      await expect(page).toHaveURL(
        /\/food-bank\/camden-food-bank\/checkout/,
      );
    });
  });

  // US5: Checkout actions
  test.describe("US5: Checkout actions", () => {
    test("modify items navigates back", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank/checkout");
      await page
        .getByRole("button", { name: /modify items/i })
        .click();
      // Should navigate away from checkout
      await expect(page).not.toHaveURL(/\/checkout/);
    });
  });
});
