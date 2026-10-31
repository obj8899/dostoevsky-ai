export type FeatureId = "rewrite" | "cabinet" | "monologue";

type FeatureNavProps = {
  activeFeature: FeatureId;
  onSelect: (feature: FeatureId) => void;
};

const features: Array<{ id: FeatureId; number: string; label: string }> = [
  { id: "rewrite", number: "01", label: "Literary Rewrite" },
  { id: "cabinet", number: "02", label: "Word Cabinet" },
  { id: "monologue", number: "03", label: "Inner Monologue" },
];

export default function FeatureNav({
  activeFeature,
  onSelect,
}: FeatureNavProps) {
  return (
    <nav className="feature-nav" aria-label="Writing studios">
      <p className="nav-caption">The writing rooms</p>
      <div className="feature-nav__list">
        {features.map((feature) => (
          <button
            className={`feature-nav__item ${
              activeFeature === feature.id ? "is-active" : ""
            }`}
            type="button"
            key={feature.id}
            aria-current={activeFeature === feature.id ? "page" : undefined}
            onClick={() => onSelect(feature.id)}
          >
            <span className="feature-nav__number">{feature.number}</span>
            <span>{feature.label}</span>
            <span className="feature-nav__arrow" aria-hidden="true">
              ↗
            </span>
          </button>
        ))}
      </div>
    </nav>
  );
}

