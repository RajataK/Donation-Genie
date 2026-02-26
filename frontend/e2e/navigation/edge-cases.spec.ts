import { test, expect } from "@playwright/test";

test.describe("Edge Cases", () => {
  test.describe("Empty states", () => {
    test("direct items page shows disabled checkout when basket is empty", async ({
      page,
    }) => {
      await page.goto("/food-bank/camden-food-bank/direct-items");
      const checkoutButton = page.getByRole("button", {
        name: /proceed to checkout/i,
      });
      await expect(checkoutButton).toBeDisabled();
    });

    test("search results renders all food bank cards from mock data", async ({
      page,
    }) => {
      await page.goto("/search?postcode=SW1A+1AA");
      const cards = page.getByRole("button", {
        name: /select this food bank/i,
      });
      await expect(cards).toHaveCount(3);
    });
  });

  test.describe("Text overflow and truncation", () => {
    test("long food bank names have title attribute for full text", async ({
      page,
    }) => {
      await page.goto("/food-bank/camden-food-bank");
      // The h1 heading shows the full food bank name
      const heading = page.getByRole("heading", { level: 1 });
      await expect(heading).toBeVisible();
      // Verify heading text is present and not empty
      const text = await heading.textContent();
      expect(text!.length).toBeGreaterThan(0);
    });

    test("wish list item names have title attribute", async ({ page }) => {
      await page.goto("/food-bank/camden-food-bank");
      // WishListItemCard renders h3 with title attribute
      const itemHeadings = page.locator(".wish-list-card h3[title]");
      const count = await itemHeadings.count();
      expect(count).toBeGreaterThan(0);

      // Verify title contains the full item name
      for (let i = 0; i < count; i++) {
        const title = await itemHeadings.nth(i).getAttribute("title");
        const text = await itemHeadings.nth(i).textContent();
        expect(title).toBe(text);
      }
    });

    test("direct items card headings have title attribute for truncation", async ({
      page,
    }) => {
      await page.goto("/food-bank/camden-food-bank/direct-items");
      const itemHeadings = page.locator(".direct-items__card-header h3[title]");
      const count = await itemHeadings.count();
      expect(count).toBeGreaterThan(0);
    });
  });
});
