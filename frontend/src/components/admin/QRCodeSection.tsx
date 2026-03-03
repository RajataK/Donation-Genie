import { qrCodeFormats } from "../../data/mock-data";
import Button from "../ui/Button";
import Card from "../ui/Card";
import "./QRCodeSection.css";

export default function QRCodeSection() {
  return (
    <fieldset className="qr-section">
      <legend>QR Code Generator</legend>
      <div className="qr-section__preview">
        <div className="qr-section__placeholder" aria-label="QR code preview">
          <span aria-hidden="true">📱</span>
          <p>QR Code Preview</p>
        </div>
      </div>
      <div className="qr-section__formats">
        {qrCodeFormats.map((format) => (
          <Card key={format.id} className="qr-section__format">
            <h3>{format.label}</h3>
            <p className="qr-section__format-desc">{format.description}</p>
            <Button variant="secondary">
              Download {format.fileType}
            </Button>
          </Card>
        ))}
      </div>
      <Button>Generate All Formats</Button>
    </fieldset>
  );
}
