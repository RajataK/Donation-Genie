import { test, expect } from "@playwright/test";

test.describe("Full Donor Journey End-to-End", () => {
  test("completes direct items donation path: landing → search → detail → direct items → checkout", async ({
    page,
  }) => {
    // Step 1: Landing page — enter postcode
    await page.goto("/");
    await expect(
      page.getByRole("heading", { name: /donation genie/i }),
    ).toBeVisible();
    await page.getByLabel(/postcode/i).fill("SW1A 1AA");
    await page
      .getByRole("button", { name: /find local food banks/i })
      .click();

    // Step 2: Search results — select first food bank
    await expect(page).toHaveURL(/\/search\?postcode=/);
    await expect(
      page.getByRole("heading", { name: /food banks near/i }),
    ).toBeVisible();
    await page
      .getByRole("button", { name: /select this food bank/i })
      .first()
      .click();

    // Step 3: Food bank detail — choose direct items
    await expect(page).toHaveURL(/\/food-bank\//);
    await expect(page.getByText(/current wish list/i)).toBeVisible();
    await page
      .getByRole("link", { name: /donate individual items/i })
      .click();

    // Step 4: Direct items — add item and proceed to checkout
    await expect(page).toHaveURL(/\/direct-items/);
    await expect(
      page.getByRole("heading", { name: /select items to donate/i }),
    ).toBeVisible();
    await page.getByRole("button", { name: /add/i }).first().click();
    await page
      .getByRole("button", { name: /proceed to checkout/i })
      .click();

    // Step 5: Checkout — verify page loaded
    await expect(page).toHaveURL(/\/checkout/);
    await expect(
      page.getByRole("heading", { name: /review your donation/i }),
    ).toBeVisible();
    await expect(
      page.getByRole("button", { name: /complete donation/i }),
    ).toBeVisible();
  });

  test("completes recipe kit donation path: landing → search → detail → recipe kits → checkout", async ({
    page,
  }) => {
    // Step 1: Landing page
    await page.goto("/");
    await page.getByLabel(/postcode/i).fill("N1 9GU");
    await page
      .getByRole("button", { name: /find local food banks/i })
      .click();

    // Step 2: Search results
    await expect(page).toHaveURL(/\/search\?postcode=/);
    await page
      .getByRole("button", { name: /select this food bank/i })
      .first()
      .click();

    // Step 3: Food bank detail — choose recipe kits
    await expect(page).toHaveURL(/\/food-bank\//);
    await page.getByRole("link", { name: /recipe kits/i }).click();

    // Step 4: Recipe kits — select a kit
    await expect(page).toHaveURL(/\/recipe-kits/);
    await expect(
      page.getByRole("heading", { name: /ai recipe kits/i }),
    ).toBeVisible();
    await page
      .getByRole("button", { name: /select this kit/i })
      .first()
      .click();

    // Step 5: Checkout
    await expect(page).toHaveURL(/\/checkout/);
    await expect(
      page.getByRole("heading", { name: /review your donation/i }),
    ).toBeVisible();
  });
});
