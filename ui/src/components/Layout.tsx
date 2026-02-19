import { ReactNode } from "react";
import { Link, useLocation } from "react-router-dom";

type Props = {
  children: ReactNode;
};

function Layout({ children }: Props) {
  const location = useLocation();

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="logo">SecureSAR</div>
        <nav className="nav-links">
          <Link to="/cases" className={location.pathname.startsWith("/cases") ? "active" : ""}>
            Cases
          </Link>
        </nav>
      </header>
      <main className="app-main">{children}</main>
    </div>
  );
}

export default Layout;

