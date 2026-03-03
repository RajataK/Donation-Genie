import type { SupermarketProduct } from "../../data/types";
import "./CheckoutBasket.css";

interface CheckoutBasketProps {
  kitName: string;
  products: SupermarketProduct[];
  deliveryCost: number;
}

export default function CheckoutBasket({
  kitName,
  products,
  deliveryCost,
}: CheckoutBasketProps) {
  const itemsTotal = products.reduce((sum, p) => sum + p.price, 0);
  const grandTotal = itemsTotal + deliveryCost;

  return (
    <div className="checkout-basket">
      <h2>{kitName}</h2>
      <table className="checkout-basket__table">
        <thead>
          <tr>
            <th scope="col">Product</th>
            <th scope="col">Retailer</th>
            <th scope="col">Price</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.name}>
              <td>{product.name}</td>
              <td>{product.retailer}</td>
              <td>&pound;{product.price.toFixed(2)}</td>
            </tr>
          ))}
          <tr className="checkout-basket__delivery">
            <td colSpan={2}>Delivery</td>
            <td>&pound;{deliveryCost.toFixed(2)}</td>
          </tr>
        </tbody>
        <tfoot>
          <tr className="checkout-basket__total">
            <td colSpan={2}>
              <strong>Total</strong>
            </td>
            <td>
              <strong>&pound;{grandTotal.toFixed(2)}</strong>
            </td>
          </tr>
        </tfoot>
      </table>
      <p className="checkout-basket__note">
        Items will be delivered directly to the food bank via {products[0]?.retailer ?? "the supermarket"}.
      </p>
    </div>
  );
}
