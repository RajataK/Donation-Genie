import "./Badge.css";

interface BadgeProps {
  variant: "urgent" | "active" | "needed";
  children: React.ReactNode;
}

export default function Badge({ variant, children }: BadgeProps) {
  const label =
    variant === "urgent"
      ? "Urgency level: urgent"
      : variant === "needed"
        ? "Urgency level: needed"
        : "Status: active";

  return (
    <span className={`badge badge--${variant}`} aria-label={label}>
      {children}
    </span>
  );
}
