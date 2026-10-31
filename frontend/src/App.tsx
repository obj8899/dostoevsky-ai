import { useCallback, useEffect, useState } from "react";

import {
  ApiError,
  fetchHealth,
  evaluateHealthStatus,
  type ConnectionState,
} from "./api/client";
import AppShell from "./components/AppShell";
import type { FeatureId } from "./components/FeatureNav";
import InnerMonologue from "./components/InnerMonologue";
import LiteraryRewrite from "./components/LiteraryRewrite";
import WordCabinet from "./components/WordCabinet";
import WorkspaceHeader from "./components/WorkspaceHeader";
import { FEATURE_TO_HASH, getFeatureFromHash } from "./utils/navigation";

export default function App() {
  const [activeFeature, setActiveFeature] = useState<FeatureId>(() => {
    if (typeof window !== "undefined" && window.location.hash) {
      return getFeatureFromHash(window.location.hash);
    }
    return "rewrite";
  });
  const [connection, setConnection] = useState<ConnectionState>("checking");
  const [checkVersion, setCheckVersion] = useState(0);

  const handleSelectFeature = useCallback((feature: FeatureId) => {
    setActiveFeature(feature);
    const targetHash = FEATURE_TO_HASH[feature];
    if (typeof window !== "undefined" && window.location.hash !== targetHash) {
      window.location.hash = targetHash;
    }
  }, []);

  useEffect(() => {
    const handleHashChange = () => {
      const feature = getFeatureFromHash(window.location.hash);
      setActiveFeature(feature);
    };

    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const checkBackend = useCallback(async () => {
    setConnection("checking");
    try {
      const health = await fetchHealth();
      setConnection(evaluateHealthStatus(health));
    } catch (error) {
      if (
        error instanceof ApiError &&
        error.message.includes("invalid health response")
      ) {
        setConnection("malformed");
      } else {
        setConnection("unavailable");
      }
    }
  }, []);

  useEffect(() => {
    void checkBackend();
  }, [checkBackend, checkVersion]);

  return (
    <AppShell
      activeFeature={activeFeature}
      connection={connection}
      onSelectFeature={handleSelectFeature}
      onRetryConnection={() => setCheckVersion((version) => version + 1)}
    >
      <WorkspaceHeader feature={activeFeature} />

      <div
        className="studio-panel"
        id="studio-panel-rewrite"
        role="region"
        aria-label="Literary Rewrite Studio"
        hidden={activeFeature !== "rewrite"}
      >
        <LiteraryRewrite />
      </div>
      <div
        className="studio-panel"
        id="studio-panel-cabinet"
        role="region"
        aria-label="Word Cabinet Studio"
        hidden={activeFeature !== "cabinet"}
      >
        <WordCabinet />
      </div>
      <div
        className="studio-panel"
        id="studio-panel-monologue"
        role="region"
        aria-label="Inner Monologue Studio"
        hidden={activeFeature !== "monologue"}
      >
        <InnerMonologue />
      </div>

      <section className="lower-note" aria-label="Workspace introduction">
        <span className="lower-note__index">A—</span>
        <p>
          {activeFeature === "rewrite"
            ? "A faithful rewrite changes the cadence, not the cause."
            : activeFeature === "cabinet"
              ? "A precise word does not end a feeling; it gives it a boundary."
              : "The mind's divided voice can tell more than a tidy conclusion."}
        </p>
        <span className="lower-note__rule" />
      </section>
    </AppShell>
  );
}
