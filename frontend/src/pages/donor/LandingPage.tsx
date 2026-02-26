import { useState } from "react";
import { useNavigate } from "@tanstack/react-router";
import Button from "../../components/ui/Button";
import Input from "../../components/ui/Input";
import "./LandingPage.css";

export default function LandingPage() {
  const [postcode, setPostcode] = useState("");
  const navigate = useNavigate();

  const handleSearch = () => {
    if (postcode.trim()) {
      navigate({ to: "/search", search: { postcode: postcode.trim() } });
    }
  };

  return (
    <section className="landing">
      <div className="landing__hero">
        <h1 className="landing__title">Donation Genie</h1>
        <p className="landing__tagline">
          AI-powered donation companion — find your local food bank and donate
          what they need most
        </p>
        <div className="landing__search">
          <Input
            id="postcode"
            label="Enter your postcode"
            type="text"
            placeholder="e.g. SW1A 1AA"
            value={postcode}
            onChange={(e) => setPostcode(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSearch();
            }}
          />
          <Button onClick={handleSearch}>Find Local Food Banks</Button>
        </div>
      </div>
    </section>
  );
}
