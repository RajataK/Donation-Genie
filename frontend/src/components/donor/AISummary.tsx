import "./AISummary.css";

interface AISummaryProps {
  summary: string;
}

export default function AISummary({ summary }: AISummaryProps) {
  return (
    <section
      className="ai-summary"
      aria-label="AI-generated needs summary"
    >
      <p className="ai-summary__text">{summary}</p>
    </section>
  );
}
