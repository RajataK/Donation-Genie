import type { HTMLAttributes } from "react";
import "./Card.css";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hoverable?: boolean;
}

export default function Card({
  hoverable = false,
  className = "",
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={`card ${hoverable ? "card--hoverable" : ""} ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
