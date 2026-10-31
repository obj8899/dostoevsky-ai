import type { ReactNode } from "react";

import type { ConnectionState } from "../api/client";
import FeatureNav, { type FeatureId } from "./FeatureNav";

type AppShellProps = {
  activeFeature: FeatureId;
  connection: ConnectionState;
  onSelectFeature: (feature: FeatureId) => void;
  onRetryConnection: () => void;
  children: ReactNode;
};

const connectionCopy: Record<ConnectionState, string> = {
  checking: "Checking backend",
  connected: "Backend connected",
  degraded: "Ollama unavailable",
  unavailable: "Backend unavailable",
  malformed: "Health check failed",
};

export default function AppShell({
  activeFeature,
  connection,
  onSelectFeature,
  onRetryConnection,
  children,
}: AppShellProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Application navigation">
        <a className="brand" href="#rewrite" aria-label="Dostoevsky AI home">
          <span className="brand__mark" aria-hidden="true">
            <svg viewBox="0 0 44 44" fill="none">
              <path d="M8 7.5h19.5a8 8 0 0 1 8 8V36H16a8 8 0 0 1-8-8V7.5Z" />
              <path d="M14 13.5h13.5M14 19.5h13.5M14 25.5h8" />
              <path d="M35.5 14.5 40 10v25.5h-4.5" />
            </svg>
          </span>
          <span className="brand__type">
            <span>Dostoevsky</span>
            <span className="brand__sub">Artificial Intelligence</span>
          </span>
        </a>

        <div className="sidebar__rule" />
        <FeatureNav
          activeFeature={activeFeature}
          onSelect={onSelectFeature}
        />

        <div className="sidebar__foot">
          <div className="sidebar__foot-rule" />
          <p className="sidebar__motto">“The soul is healed by being with children.”</p>
          <p className="sidebar__attribution">— Fyodor Dostoevsky</p>
          <div className="local-note">
            <span className="local-note__seal" aria-hidden="true" />
            <span>Private by design · runs locally</span>
          </div>
        </div>
      </aside>

      <main className="main-column" id="home">
        <div className="topbar">
          <div className="topbar__edition">
            <span className="topbar__line" />
            <span>THE UNDERGROUND STUDY</span>
            <span className="topbar__edition-number">No. 01</span>
          </div>
          <div className="topbar__status-wrap">
            {connection !== "connected" && connection !== "checking" ? (
              <button
                className={`connection-status connection-status--${connection}`}
                type="button"
                onClick={onRetryConnection}
                aria-label={`${connectionCopy[connection]}. Retry health check.`}
              >
                <span className="connection-status__dot" aria-hidden="true" />
                <span>{connectionCopy[connection]}</span>
                <span className="connection-status__retry">Retry</span>
              </button>
            ) : (
              <div
                className={`connection-status connection-status--${connection}`}
                role="status"
                aria-live="polite"
              >
                <span className="connection-status__dot" aria-hidden="true" />
                <span>{connectionCopy[connection]}</span>
              </div>
            )}
          </div>
        </div>

        <div className="mobile-brand">
          <span className="mobile-brand__monogram" aria-hidden="true">
            D.
          </span>
          <span>Dostoevsky AI</span>
        </div>

        <div className="mobile-nav">
          <FeatureNav
            activeFeature={activeFeature}
            onSelect={onSelectFeature}
          />
        </div>

        <div className="workspace">{children}</div>

        <footer className="page-footer">
          <span>AN EXPERIMENT IN ATTENTION</span>
          <span>LOCAL LANGUAGE MODEL · PROMPT-CONFIGURED, NOT FINE-TUNED</span>
        </footer>
      </main>
    </div>
  );
}
