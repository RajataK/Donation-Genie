import { useState } from "react";
import { deliveryPreferences, supermarketPartners } from "../../data/mock-data";
import Card from "../ui/Card";
import "./IntegrationSettings.css";

export default function IntegrationSettings() {
  const [preferences, setPreferences] = useState(deliveryPreferences);
  const [deliveryNotes, setDeliveryNotes] = useState("");

  const togglePreference = (id: string) => {
    setPreferences((prev) =>
      prev.map((p) => (p.id === id ? { ...p, enabled: !p.enabled } : p)),
    );
  };

  return (
    <div className="integration-settings">
      <fieldset className="integration-settings__section">
        <legend>Delivery Preferences</legend>
        <div className="integration-settings__checkboxes">
          {preferences.map((pref) => (
            <div key={pref.id} className="integration-settings__checkbox">
              <input
                type="checkbox"
                id={pref.id}
                checked={pref.enabled}
                onChange={() => togglePreference(pref.id)}
              />
              <label htmlFor={pref.id}>
                <strong>{pref.label}</strong>
                <span className="integration-settings__checkbox-desc">
                  {pref.description}
                </span>
              </label>
            </div>
          ))}
        </div>
        <div className="integration-settings__notes">
          <label htmlFor="delivery-notes">Delivery Notes</label>
          <textarea
            id="delivery-notes"
            value={deliveryNotes}
            onChange={(e) => setDeliveryNotes(e.target.value)}
            placeholder="Add any special delivery instructions..."
            rows={3}
          />
        </div>
      </fieldset>

      <fieldset className="integration-settings__section">
        <legend>Supermarket Partners</legend>
        <div className="integration-settings__partners">
          {supermarketPartners.map((partner) => (
            <Card
              key={partner.id}
              className={`integration-settings__partner ${!partner.available ? "integration-settings__partner--disabled" : ""}`}
              aria-disabled={!partner.available || undefined}
            >
              <h3>{partner.name}</h3>
              <p className="integration-settings__partner-time">
                {partner.deliveryTime}
              </p>
              <span
                className={`integration-settings__partner-status ${partner.enabled ? "enabled" : ""}`}
              >
                {partner.enabled
                  ? "Enabled"
                  : partner.available
                    ? "Available"
                    : "Coming Soon"}
              </span>
            </Card>
          ))}
        </div>
      </fieldset>
    </div>
  );
}
