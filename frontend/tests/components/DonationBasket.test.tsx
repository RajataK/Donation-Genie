import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import DonationBasket from "../../src/components/donor/DonationBasket";
import type { BasketItem } from "../../src/data/types";

describe("DonationBasket", () => {
  const mockItems: BasketItem[] = [
    { id: "1", name: "Tinned Tomatoes", quantity: 2, unitPrice: 0.85 },
    { id: "2", name: "Pasta", quantity: 1, unitPrice: 1.2 },
  ];

  it("displays items with quantities and prices", () => {
    render(
      <DonationBasket
        items={mockItems}
        onCheckout={vi.fn()}
        onRemoveItem={vi.fn()}
      />,
    );
    expect(screen.getByText("Tinned Tomatoes")).toBeInTheDocument();
    expect(screen.getByText("Pasta")).toBeInTheDocument();
  });

  it("calculates and displays total cost", () => {
    render(
      <DonationBasket
        items={mockItems}
        onCheckout={vi.fn()}
        onRemoveItem={vi.fn()}
      />,
    );
    // 2 * 0.85 + 1 * 1.20 = 2.90
    expect(screen.getByText(/2\.90/)).toBeInTheDocument();
  });

  it("shows empty state when no items", () => {
    render(
      <DonationBasket
        items={[]}
        onCheckout={vi.fn()}
        onRemoveItem={vi.fn()}
      />,
    );
    expect(
      screen.getByText(/your donation basket is empty/i),
    ).toBeInTheDocument();
  });

  it("disables checkout button when basket is empty", () => {
    render(
      <DonationBasket
        items={[]}
        onCheckout={vi.fn()}
        onRemoveItem={vi.fn()}
      />,
    );
    const btn = screen.getByRole("button", { name: /proceed to checkout/i });
    expect(btn).toBeDisabled();
  });

  it("enables checkout button when basket has items", () => {
    render(
      <DonationBasket
        items={mockItems}
        onCheckout={vi.fn()}
        onRemoveItem={vi.fn()}
      />,
    );
    const btn = screen.getByRole("button", { name: /proceed to checkout/i });
    expect(btn).toBeEnabled();
  });

  it("calls onCheckout when checkout button clicked", async () => {
    const user = userEvent.setup();
    const onCheckout = vi.fn();
    render(
      <DonationBasket
        items={mockItems}
        onCheckout={onCheckout}
        onRemoveItem={vi.fn()}
      />,
    );
    await user.click(
      screen.getByRole("button", { name: /proceed to checkout/i }),
    );
    expect(onCheckout).toHaveBeenCalled();
  });
});
