import UploadZone from "../../components/admin/UploadZone";
import ExtractedItemsPreview from "../../components/admin/ExtractedItemsPreview";
import ImpactStory from "../../components/donor/ImpactStory";
import Button from "../../components/ui/Button";
import "./OnboardingPage.css";

export default function OnboardingPage() {
  return (
    <section className="onboarding">
      <h1>Welcome to Donation Genie</h1>
      <p className="onboarding__subtitle">
        Set up your food bank profile in minutes. Upload your current wish list
        and our AI will extract and categorise your needed items.
      </p>
      <UploadZone />
      <p className="onboarding__processing">
        Our AI is processing your wish list...
      </p>
      <ExtractedItemsPreview />
      <div className="onboarding__actions">
        <Button>Confirm &amp; Publish</Button>
        <Button variant="secondary">Edit Items</Button>
      </div>
      <ImpactStory
        story="Once published, your wish list will be visible to donors in your area. They can donate individual items or select AI-generated recipe kits built from your needs."
        heading="What Happens Next"
      />
    </section>
  );
}
