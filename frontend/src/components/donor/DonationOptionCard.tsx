import { Link } from "@tanstack/react-router";
import Card from "../ui/Card";
import "./DonationOptionCard.css";

interface DonationOptionCardProps {
  icon: string;
  title: string;
  description: string;
  to: string;
  recommended?: boolean;
}

export default function DonationOptionCard({
  icon,
  title,
  description,
  to,
  recommended = false,
}: DonationOptionCardProps) {
  return (
    <Card
      hoverable
      className={`donation-option ${recommended ? "donation-option--recommended" : ""}`}
      data-testid="donation-option"
    >
      <span className="donation-option__icon" aria-hidden="true">
        {icon}
      </span>
      <h3 className="donation-option__title">{title}</h3>
      <p className="donation-option__description">{description}</p>
      {recommended && (
        <span className="donation-option__badge">Recommended</span>
      )}
      <Link to={to} className="donation-option__link">
        {title}
      </Link>
    </Card>
  );
}
