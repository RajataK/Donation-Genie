import { Link, useRouterState } from "@tanstack/react-router";
import "./Navigation.css";

export default function Navigation() {
  const routerState = useRouterState();
  const currentPath = routerState.location.pathname;
  const isDonorJourney = !currentPath.startsWith("/admin");

  return (
    <nav className="nav" aria-label="Main navigation">
      <div className="nav__inner container">
        <span className="nav__brand">Donation Genie</span>
        <ul className="nav__links">
          <li>
            <Link
              to="/"
              className={`nav__link ${isDonorJourney ? "nav__link--active" : ""}`}
              aria-current={isDonorJourney ? "page" : undefined}
            >
              Donor Journey
            </Link>
          </li>
          <li>
            <Link
              to="/admin"
              className={`nav__link ${!isDonorJourney ? "nav__link--active" : ""}`}
              aria-current={!isDonorJourney ? "page" : undefined}
            >
              Admin
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}
