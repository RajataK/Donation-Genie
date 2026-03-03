import { test, expect } from "@playwright/test";

const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
];

test.describe("Donor Pages Responsive @responsive", () => {
  // US1: Landing Page
  test.describe("US1: LandingPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/");
        const body = page.locator("body");
        const box = await body.boundingBox();
        expect(box).toBeTruthy();
        // Check no horizontal overflow
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });

  // US1: Search Results Page
  test.describe("US1: SearchResultsPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/search?postcode=SW1A+1AA");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }

    test("cards stack on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/search?postcode=SW1A+1AA");
      const cards = page.locator(".search-results__list li");
      const count = await cards.count();
      if (count >= 2) {
        const first = await cards.nth(0).boundingBox();
        const second = await cards.nth(1).boundingBox();
        expect(first).toBeTruthy();
        expect(second).toBeTruthy();
        // On mobile, cards should stack vertically (second below first)
        expect(second!.y).toBeGreaterThan(first!.y);
      }
    });
  });

  // US2: Food Bank Detail Page
  test.describe("US2: FoodBankDetailPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/food-bank/camden-food-bank");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }

    test("donation option cards stack on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/food-bank/camden-food-bank");
      const options = page.locator("[data-testid='donation-option']");
      const count = await options.count();
      if (count >= 2) {
        const first = await options.nth(0).boundingBox();
        const second = await options.nth(1).boundingBox();
        expect(first).toBeTruthy();
        expect(second).toBeTruthy();
        expect(second!.y).toBeGreaterThan(first!.y);
      }
    });
  });

  // US3: Direct Items Page
  test.describe("US3: DirectItemsPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/food-bank/camden-food-bank/direct-items");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });

  // US4: Recipe Kits Page
  test.describe("US4: RecipeKitsPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/food-bank/camden-food-bank/recipe-kits");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });

  // US5: Checkout Page
  test.describe("US5: CheckoutPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/food-bank/camden-food-bank/checkout");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });
});
