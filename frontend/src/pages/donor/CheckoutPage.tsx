import { useParams, useNavigate } from "@tanstack/react-router";
import FlowDiagram from "../../components/donor/FlowDiagram";
import CheckoutBasket from "../../components/donor/CheckoutBasket";
import Button from "../../components/ui/Button";
import { supermarketProducts, foodBanks } from "../../data/mock-data";
import "./CheckoutPage.css";

export default function CheckoutPage() {
  const { id } = useParams({ from: "/food-bank/$id/checkout" });
  const navigate = useNavigate();
  const foodBank = foodBanks.find((fb) => fb.id === id) ?? foodBanks[0]!;

  const handleModify = () => {
    navigate({ to: "/food-bank/$id", params: { id } });
  };

  return (
    <section className="checkout">
      <h1>Review Your Donation</h1>
      <FlowDiagram />
      <CheckoutBasket
        kitName={`Donation for ${foodBank.name}`}
        products={supermarketProducts}
        deliveryCost={3.5}
      />
      <div className="checkout__actions">
        <Button onClick={() => {}}>
          Complete Donation via Tesco
        </Button>
        <Button variant="secondary" onClick={handleModify}>
          Modify Items
        </Button>
      </div>
    </section>
  );
}
