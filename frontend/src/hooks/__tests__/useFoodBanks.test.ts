import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { useFoodBanks } from "../useFoodBanks";

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

vi.mock("../../api/client", () => ({
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
  return ({ children }: { children: React.ReactNode }) =>
    createElement(QueryClientProvider, { client: queryClient }, children);
}

describe("useFoodBanks", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns food bank data on success", async () => {
    const { apiClient } = await import("../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: mockFoodBanks,
      error: undefined,
      response: new Response(),
    });

    const { result } = renderHook(() => useFoodBanks(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual(mockFoodBanks);
  });

  it("returns error state on fetch failure", async () => {
    const { apiClient } = await import("../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: undefined,
      error: { detail: "Server error" },
      response: new Response(null, { status: 500 }),
    });

    const { result } = renderHook(() => useFoodBanks(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));
  });

  it("uses staleTime to avoid refetching within cache period", async () => {
    const { apiClient } = await import("../../api/client");
    vi.mocked(apiClient.GET).mockResolvedValue({
      data: mockFoodBanks,
      error: undefined,
      response: new Response(),
    });

    const queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });
    const wrapper = ({ children }: { children: React.ReactNode }) =>
      createElement(QueryClientProvider, { client: queryClient }, children);

    const { result } = renderHook(() => useFoodBanks(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    // Render a second instance — should use cache, not refetch
    const { result: result2 } = renderHook(() => useFoodBanks(), { wrapper });
    await waitFor(() => expect(result2.current.isSuccess).toBe(true));

    expect(apiClient.GET).toHaveBeenCalledTimes(1);
  });
});
