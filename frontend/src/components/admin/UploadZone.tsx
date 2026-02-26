import "./UploadZone.css";

export default function UploadZone() {
  return (
    <div className="upload-zone-wrapper">
      <div
        className="upload-zone"
        aria-label="Upload wish list file — click or drag files here"
      >
        <span className="upload-zone__icon" aria-hidden="true">
          📁
        </span>
        <p className="upload-zone__title">
          Upload your wish list
        </p>
        <p className="upload-zone__description">
          Drag & drop or click to upload. Accepts photos, PDFs, documents, and
          screenshots of your current wish list.
        </p>
        <button type="button" className="upload-zone__button">
          Choose File
        </button>
      </div>
      <p className="upload-zone__alt">
        Or email your wish list to{" "}
        <a href="mailto:upload@donationgenie.org" className="upload-zone__link">
          upload@donationgenie.org
        </a>
      </p>
    </div>
  );
}
