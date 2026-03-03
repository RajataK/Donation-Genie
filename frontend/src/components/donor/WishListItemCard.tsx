import type { WishListItem } from "../../data/types";
import Card from "../ui/Card";
import Badge from "../ui/Badge";
import "./WishListItemCard.css";

interface WishListItemCardProps {
  item: WishListItem;
}

export default function WishListItemCard({ item }: WishListItemCardProps) {
  return (
    <Card className="wish-list-card">
      <div className="wish-list-card__header">
        <h3 className="wish-list-card__name" title={item.name}>
          {item.name}
        </h3>
        <Badge variant={item.urgencyLevel}>
          {item.urgencyLevel === "urgent" ? "Urgent" : "Needed"}
        </Badge>
      </div>
      <p className="wish-list-card__description">{item.description}</p>
      <p className="wish-list-card__price">
        ~&pound;{item.estimatedPrice.toFixed(2)} each
      </p>
    </Card>
  );
}
