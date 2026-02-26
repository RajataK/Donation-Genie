import Navigation from "./Navigation";
import "./PageShell.css";

interface PageShellProps {
  children: React.ReactNode;
}

export default function PageShell({ children }: PageShellProps) {
  return (
    <div className="page-shell">
      <header>
        <Navigation />
      </header>
      <main className="page-shell__main container">{children}</main>
      <footer className="page-shell__footer">
        <div className="container">
          <p>&copy; 2026 Donation Genie. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
