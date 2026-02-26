import { useParams } from "@tanstack/react-router";
import ImpactStory from "../../components/donor/ImpactStory";
import WishListItemCard from "../../components/donor/WishListItemCard";
import DonationOptionCard from "../../components/donor/DonationOptionCard";
import Badge from "../../components/ui/Badge";
import { foodBanks, wishListItems } from "../../data/mock-data";
import "./FoodBankDetailPage.css";

export default function FoodBankDetailPage() {
  const { id } = useParams({ from: "/food-bank/$id" });
  const foodBank = foodBanks.find((fb) => fb.id === id) ?? foodBanks[0]!;

  return (
    <section className="food-bank-detail">
      <header className="food-bank-detail__header">
        <div>
          <h1>{foodBank.name}</h1>
          <p className="food-bank-detail__meta">
            {foodBank.distance} &middot; Serving {foodBank.familiesServed}{" "}
            families per week
          </p>
        </div>
        <Badge variant={foodBank.urgencyStatus}>
          {foodBank.urgencyStatus === "urgent" ? "Urgent" : "Active"}
        </Badge>
      </header>

      <ImpactStory story={foodBank.impactStory} />

      <section>
        <h2>Current Wish List</h2>
        <div className="food-bank-detail__wish-list">
          {wishListItems.map((item) => (
            <WishListItemCard key={item.id} item={item} />
          ))}
        </div>
      </section>

      <section>
        <h2>How Would You Like to Donate?</h2>
        <div
          className="food-bank-detail__options"
          role="group"
          aria-label="Donation method options"
        >
          <DonationOptionCard
            icon="📦"
            title="Donate Individual Items"
            description="Select specific items from the wish list and choose quantities"
            to={`/food-bank/${id}/direct-items`}
          />
          <DonationOptionCard
            icon="🍳"
            title="Create Recipe Kits"
            description="AI-generated meal kits built from wish list items"
            to={`/food-bank/${id}/recipe-kits`}
            recommended
          />
        </div>
      </section>
    </section>
  );
}
