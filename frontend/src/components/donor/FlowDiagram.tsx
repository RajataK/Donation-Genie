import "./FlowDiagram.css";

const steps = [
  { label: "Select Items", icon: "📋" },
  { label: "AI Mapping", icon: "🤖" },
  { label: "Basket Created", icon: "🛒" },
  { label: "Checkout", icon: "✅" },
];

export default function FlowDiagram() {
  return (
    <div
      className="flow-diagram"
      aria-label="Donation process: Select Items, AI Mapping, Basket Created, Checkout"
    >
      {steps.map((step, index) => (
        <div key={step.label} className="flow-diagram__step">
          <span className="flow-diagram__icon" aria-hidden="true">
            {step.icon}
          </span>
          <span className="flow-diagram__label">{step.label}</span>
          {index < steps.length - 1 && (
            <span className="flow-diagram__arrow" aria-hidden="true">
              →
            </span>
          )}
        </div>
      ))}
    </div>
  );
}
