import { useState } from "react";
import "./QuantityControl.css";

interface QuantityControlProps {
  itemName: string;
  onAdd: (quantity: number) => void;
}

export default function QuantityControl({
  itemName,
  onAdd,
}: QuantityControlProps) {
  const [quantity, setQuantity] = useState(1);

  const handleDecrease = () => {
    setQuantity((q) => Math.max(1, q - 1));
  };

  const handleIncrease = () => {
    setQuantity((q) => q + 1);
  };

  const handleAdd = () => {
    onAdd(quantity);
    setQuantity(1);
  };

  return (
    <div className="quantity-control">
      <div className="quantity-control__stepper">
        <button
          type="button"
          className="quantity-control__btn"
          onClick={handleDecrease}
          aria-label={`Decrease quantity of ${itemName}`}
          disabled={quantity <= 1}
        >
          &minus;
        </button>
        <input
          type="number"
          className="quantity-control__input"
          value={quantity}
          min={1}
          onChange={(e) => setQuantity(Math.max(1, Number(e.target.value)))}
          aria-label={`Quantity of ${itemName}`}
        />
        <button
          type="button"
          className="quantity-control__btn"
          onClick={handleIncrease}
          aria-label={`Increase quantity of ${itemName}`}
        >
          +
        </button>
      </div>
      <button
        type="button"
        className="quantity-control__add"
        onClick={handleAdd}
        aria-label={`Add ${itemName} to basket`}
      >
        Add
      </button>
    </div>
  );
}
