import {
  createRouter,
  createRootRoute,
  createRoute,
  Outlet,
} from "@tanstack/react-router";
import PageShell from "./components/layout/PageShell";
import LandingPage from "./pages/donor/LandingPage";
import SearchResultsPage from "./pages/donor/SearchResultsPage";
import FoodBankDetailPage from "./pages/donor/FoodBankDetailPage";
import DirectItemsPage from "./pages/donor/DirectItemsPage";
import RecipeKitsPage from "./pages/donor/RecipeKitsPage";
import CheckoutPage from "./pages/donor/CheckoutPage";
import OnboardingPage from "./pages/admin/OnboardingPage";
import ManagementPage from "./pages/admin/ManagementPage";

const rootRoute = createRootRoute({
  component: () => (
    <PageShell>
      <Outlet />
    </PageShell>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: LandingPage,
});

const searchRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/search",
  validateSearch: (search: Record<string, unknown>) => ({
    postcode: (search.postcode as string) ?? "",
  }),
  component: SearchResultsPage,
});

const foodBankDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/food-bank/$id",
  component: FoodBankDetailPage,
});

const directItemsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/food-bank/$id/direct-items",
  component: DirectItemsPage,
});

const recipeKitsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/food-bank/$id/recipe-kits",
  component: RecipeKitsPage,
});

const checkoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/food-bank/$id/checkout",
  component: CheckoutPage,
});

const adminRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/admin",
  component: OnboardingPage,
});

const adminManagementRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/admin/management",
  component: ManagementPage,
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  searchRoute,
  foodBankDetailRoute,
  directItemsRoute,
  recipeKitsRoute,
  checkoutRoute,
  adminRoute,
  adminManagementRoute,
]);

export const router = createRouter({ routeTree });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
