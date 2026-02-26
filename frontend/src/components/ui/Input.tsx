import type { InputHTMLAttributes } from "react";
import "./Input.css";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  id: string;
}

export default function Input({ label, id, className = "", ...props }: InputProps) {
  return (
    <div className={`input-group ${className}`}>
      <label htmlFor={id} className="input-group__label">
        {label}
      </label>
      <input id={id} className="input-group__input" {...props} />
    </div>
  );
}
