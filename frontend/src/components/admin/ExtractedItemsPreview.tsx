import { wishListItems } from "../../data/mock-data";
import "./ExtractedItemsPreview.css";

export default function ExtractedItemsPreview() {
  return (
    <section className="extracted-items" data-testid="extracted-items">
      <h2>AI-Extracted Items</h2>
      <p className="extracted-items__note">
        We found the following items in your uploaded wish list:
      </p>
      <ul className="extracted-items__grid">
        {wishListItems.map((item) => (
          <li key={item.id} className="extracted-items__item">
            <span className="extracted-items__check" aria-hidden="true">
              ✓
            </span>
            <span className="extracted-items__name">{item.name}</span>
            <span className="extracted-items__category">{item.category}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
