import type { FoodBank } from "../../data/types";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import Button from "../ui/Button";
import "./FoodBankCard.css";

interface FoodBankCardProps {
  foodBank: FoodBank;
  onSelect: (id: string) => void;
}

export default function FoodBankCard({ foodBank, onSelect }: FoodBankCardProps) {
  return (
    <Card hoverable className="food-bank-card">
      <div className="food-bank-card__header">
        <h3 className="food-bank-card__name">{foodBank.name}</h3>
        <Badge variant={foodBank.urgencyStatus}>
          {foodBank.urgencyStatus === "urgent" ? "Urgent" : "Active"}
        </Badge>
      </div>
      <p className="food-bank-card__distance">{foodBank.distance}</p>
      <p className="food-bank-card__families">
        Serving {foodBank.familiesServed} families per week
      </p>
      <div className="food-bank-card__needs">
        <strong>Top needs:</strong> {foodBank.topNeeds.join(", ")}
      </div>
      <Button onClick={() => onSelect(foodBank.id)}>
        Select This Food Bank
      </Button>
    </Card>
  );
}
