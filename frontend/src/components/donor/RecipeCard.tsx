import type { RecipeKit } from "../../data/types";
import Card from "../ui/Card";
import Button from "../ui/Button";
import "./RecipeCard.css";

interface RecipeCardProps {
  kit: RecipeKit;
  onSelect: (id: string) => void;
}

export default function RecipeCard({ kit, onSelect }: RecipeCardProps) {
  return (
    <Card hoverable className="recipe-card">
      <span className="recipe-card__icon" aria-hidden="true">
        {kit.icon}
      </span>
      <h3 className="recipe-card__name">{kit.name}</h3>
      <div className="recipe-card__meta">
        <span>{kit.servings}</span>
        <span>{kit.prepTime}</span>
      </div>
      <div className="recipe-card__ingredients">
        <strong>Ingredients:</strong>
        <ul>
          {kit.ingredients.map((ing) => (
            <li key={ing.name} className={ing.matched ? "matched" : ""}>
              {ing.name}
              {ing.matched && (
                <span className="recipe-card__match" aria-label="Matches wish list">
                  ✓
                </span>
              )}
            </li>
          ))}
        </ul>
      </div>
      <p className="recipe-card__cost">
        Kit total: &pound;{kit.totalCost.toFixed(2)}
      </p>
      <Button onClick={() => onSelect(kit.id)}>Select This Kit</Button>
    </Card>
  );
}
