import { useNavigate, useSearch } from "@tanstack/react-router";
import AISummary from "../../components/donor/AISummary";
import FoodBankCard from "../../components/donor/FoodBankCard";
import { foodBanks, aiSummaryText } from "../../data/mock-data";
import "./SearchResultsPage.css";

export default function SearchResultsPage() {
  const search = useSearch({ from: "/search" });
  const navigate = useNavigate();
  const postcode = (search as { postcode?: string }).postcode ?? "";

  const handleSelect = (id: string) => {
    navigate({ to: "/food-bank/$id", params: { id } });
  };

  return (
    <section className="search-results">
      <h1>Food Banks near {postcode}</h1>
      <AISummary summary={aiSummaryText} />
      <ul className="search-results__list">
        {foodBanks.map((fb) => (
          <li key={fb.id}>
            <FoodBankCard foodBank={fb} onSelect={handleSelect} />
          </li>
        ))}
      </ul>
    </section>
  );
}
