import QRCodeSection from "../../components/admin/QRCodeSection";
import IntegrationSettings from "../../components/admin/IntegrationSettings";
import Button from "../../components/ui/Button";
import "./ManagementPage.css";

export default function ManagementPage() {
  return (
    <section className="management">
      <h1>Food Bank Management</h1>
      <QRCodeSection />
      <IntegrationSettings />
      <div className="management__actions">
        <Button>Save Settings</Button>
        <Button variant="secondary">Test Integration</Button>
      </div>
    </section>
  );
}
