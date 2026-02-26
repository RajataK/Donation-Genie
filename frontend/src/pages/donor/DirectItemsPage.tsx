import { useState } from "react";
import { useParams, useNavigate } from "@tanstack/react-router";
import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import QuantityControl from "../../components/donor/QuantityControl";
import DonationBasket from "../../components/donor/DonationBasket";
import { wishListItems } from "../../data/mock-data";
import type { BasketItem } from "../../data/types";
import "./DirectItemsPage.css";

export default function DirectItemsPage() {
  const { id } = useParams({ from: "/food-bank/$id/direct-items" });
  const navigate = useNavigate();
  const [basketItems, setBasketItems] = useState<BasketItem[]>([]);

  const handleAddItem = (itemId: string, itemName: string, price: number, quantity: number) => {
    setBasketItems((prev) => {
      const existing = prev.find((i) => i.id === itemId);
      if (existing) {
        return prev.map((i) =>
          i.id === itemId ? { ...i, quantity: i.quantity + quantity } : i,
        );
      }
      return [...prev, { id: itemId, name: itemName, quantity, unitPrice: price }];
    });
  };

  const handleRemoveItem = (itemId: string) => {
    setBasketItems((prev) => prev.filter((i) => i.id !== itemId));
  };

  const handleCheckout = () => {
    navigate({ to: "/food-bank/$id/checkout", params: { id } });
  };

  return (
    <section className="direct-items">
      <h1>Select Items to Donate</h1>
      <div className="direct-items__layout">
        <div className="direct-items__grid">
          {wishListItems.map((item) => (
            <Card key={item.id} className="direct-items__card">
              <div className="direct-items__card-header">
                <h3 title={item.name}>{item.name}</h3>
                <Badge variant={item.urgencyLevel}>
                  {item.urgencyLevel === "urgent" ? "Urgent" : "Needed"}
                </Badge>
              </div>
              <p className="direct-items__card-desc">{item.description}</p>
              <p className="direct-items__card-price">
                &pound;{item.estimatedPrice.toFixed(2)} each
              </p>
              <QuantityControl
                itemName={item.name}
                onAdd={(qty) =>
                  handleAddItem(item.id, item.name, item.estimatedPrice, qty)
                }
              />
            </Card>
          ))}
        </div>
        <aside className="direct-items__sidebar">
          <DonationBasket
            items={basketItems}
            onCheckout={handleCheckout}
            onRemoveItem={handleRemoveItem}
          />
        </aside>
      </div>
    </section>
  );
}
