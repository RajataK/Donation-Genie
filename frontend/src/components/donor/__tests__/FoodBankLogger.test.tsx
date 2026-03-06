import { render, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, it, expect, vi, beforeEach } from "vitest";
import FoodBankLogger from "../FoodBankLogger";

const mockFoodBanks = [
  {
    id: "550e8400-e29b-41d4-a716-446655440000",
    name: "Hackney Food Bank",
    postcode: "E8 1DY",
    latitude: "51.543800",
    longitude: "-0.055300",
    address: "29 Dalston Lane, London E8 1DY",
    families_served_weekly: 150,
    urgency_level: "urgent" as const,
    last_updated: "2026-03-06T12:00:00Z",
  },
];

vi.mock("../../../api/client", () => ({
  apiClient: {
    GET: vi.fn(),
  },
}));

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe("FoodBankLogger", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.spyOn(console, "log").mockImplementation(() => {});
    vi.spyOn(console, "error").mockImplementation(() => {});
  });

  it("logs food bank data to console on successful fetch", async () => {
    const { apiClient } = await import("../../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: mockFoodBanks,
      error: undefined,
      response: new Response(),
    });

    const Wrapper = createWrapper();
    render(
      <Wrapper>
        <FoodBankLogger />
      </Wrapper>,
    );

    await waitFor(() => {
      expect(console.log).toHaveBeenCalledWith(
        "Food banks loaded:",
        mockFoodBanks,
      );
    });
  });

  it("logs error to console on fetch failure", async () => {
    const { apiClient } = await import("../../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: undefined,
      error: { detail: "Server error" },
      response: new Response(null, { status: 500 }),
    });

    const Wrapper = createWrapper();
    render(
      <Wrapper>
        <FoodBankLogger />
      </Wrapper>,
    );

    await waitFor(() => {
      expect(console.error).toHaveBeenCalled();
    });
  });

  it("handles empty food bank list without errors", async () => {
    const { apiClient } = await import("../../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: [],
      error: undefined,
      response: new Response(),
    });

    const Wrapper = createWrapper();
    render(
      <Wrapper>
        <FoodBankLogger />
      </Wrapper>,
    );

    await waitFor(() => {
      expect(console.log).toHaveBeenCalledWith("Food banks loaded:", []);
    });
  });
});
