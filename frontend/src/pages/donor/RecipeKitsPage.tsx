import { useParams, useNavigate } from "@tanstack/react-router";
import RecipeCard from "../../components/donor/RecipeCard";
import ImpactStory from "../../components/donor/ImpactStory";
import { recipeKits, foodBanks } from "../../data/mock-data";
import "./RecipeKitsPage.css";

export default function RecipeKitsPage() {
  const { id } = useParams({ from: "/food-bank/$id/recipe-kits" });
  const navigate = useNavigate();
  const foodBank = foodBanks.find((fb) => fb.id === id) ?? foodBanks[0]!;

  const handleSelect = () => {
    navigate({ to: "/food-bank/$id/checkout", params: { id } });
  };

  return (
    <section className="recipe-kits">
      <h1>AI Recipe Kits</h1>
      <p className="recipe-kits__intro">
        These meal kits are built from {foodBank.name}&apos;s wish list items,
        designed to provide complete, nutritious meals for families.
      </p>
      <div className="recipe-kits__grid">
        {recipeKits.map((kit) => (
          <RecipeCard key={kit.id} kit={kit} onSelect={handleSelect} />
        ))}
      </div>
      <ImpactStory
        story={foodBank.impactStory}
        heading="Your Recipe Kit Makes a Difference"
      />
    </section>
  );
}
