import type { FeatureId } from "./FeatureNav";

const titles: Record<FeatureId, { number: string; name: string; note: string }> =
  {
    rewrite: {
      number: "01",
      name: "Literary Rewrite",
      note: "Meaning, recast",
    },
    cabinet: {
      number: "02",
      name: "Word Cabinet",
      note: "The exact word",
    },
    monologue: {
      number: "03",
      name: "Inner Monologue",
      note: "A mind in motion",
    },
  };

type WorkspaceHeaderProps = {
  feature: FeatureId;
};

export default function WorkspaceHeader({ feature }: WorkspaceHeaderProps) {
  const current = titles[feature];

  return (
    <header className="workspace-header">
      <div className="workspace-header__eyebrow">
        <span>Writing studio</span>
        <span className="eyebrow-separator" aria-hidden="true">
          /
        </span>
        <span>{current.number}</span>
      </div>
      <div className="workspace-header__title-row">
        <h1>{current.name}</h1>
        <p>{current.note}</p>
      </div>
    </header>
  );
}

