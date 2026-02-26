import { test, expect } from "@playwright/test";

const viewports = [
  { name: "mobile", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
];

test.describe("Admin Pages Responsive @responsive", () => {
  // US6: Onboarding Page
  test.describe("US6: OnboardingPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/admin");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });

  // US7: Management Page
  test.describe("US7: ManagementPage responsive", () => {
    for (const vp of viewports) {
      test(`renders without horizontal overflow at ${vp.name} (${vp.width}px)`, async ({
        page,
      }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.goto("/admin/management");
        const scrollWidth = await page.evaluate(
          () => document.documentElement.scrollWidth,
        );
        expect(scrollWidth).toBeLessThanOrEqual(vp.width);
      });
    }
  });
});
