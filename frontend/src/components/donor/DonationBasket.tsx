import type { BasketItem } from "../../data/types";
import Button from "../ui/Button";
import "./DonationBasket.css";

interface DonationBasketProps {
  items: BasketItem[];
  onCheckout: () => void;
  onRemoveItem: (id: string) => void;
}

export default function DonationBasket({
  items,
  onCheckout,
  onRemoveItem,
}: DonationBasketProps) {
  const total = items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0,
  );
  const isEmpty = items.length === 0;

  return (
    <section className="donation-basket">
      <h2>Your Donation Basket</h2>
      <div aria-live="polite">
        {isEmpty ? (
          <p className="donation-basket__empty">
            Your donation basket is empty. Add items to get started.
          </p>
        ) : (
          <>
            <ul className="donation-basket__list">
              {items.map((item) => (
                <li key={item.id} className="donation-basket__item">
                  <span className="donation-basket__item-name">{item.name}</span>
                  <span className="donation-basket__item-qty">
                    x{item.quantity}
                  </span>
                  <span className="donation-basket__item-price">
                    &pound;{(item.quantity * item.unitPrice).toFixed(2)}
                  </span>
                  <button
                    type="button"
                    className="donation-basket__remove"
                    onClick={() => onRemoveItem(item.id)}
                    aria-label={`Remove ${item.name} from basket`}
                  >
                    &times;
                  </button>
                </li>
              ))}
            </ul>
            <p className="donation-basket__total">
              Total: &pound;{total.toFixed(2)}
            </p>
          </>
        )}
      </div>
      <Button
        onClick={onCheckout}
        disabled={isEmpty}
        aria-disabled={isEmpty}
      >
        Proceed to Checkout
      </Button>
    </section>
  );
}
