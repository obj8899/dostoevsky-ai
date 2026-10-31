import { useRef, useState, type FormEvent } from "react";

import {
  ApiError,
  generateInnerMonologue,
  type InnerMonologueResponse,
} from "../api/client";

const MIN_ALLOWED_WORDS = 50;
const MAX_ALLOWED_WORDS = 500;
const MAX_SCENARIO_LENGTH = 2000;

async function copyText(value: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return;
  }

  const temporary = document.createElement("textarea");
  temporary.value = value;
  temporary.setAttribute("readonly", "");
  temporary.style.position = "fixed";
  temporary.style.opacity = "0";
  document.body.append(temporary);
  temporary.select();
  const copied = document.execCommand("copy");
  temporary.remove();
  if (!copied) {
    throw new Error("Clipboard copy was not available.");
  }
}

export default function InnerMonologue() {
  const [scenario, setScenario] = useState("");
  const [perspective, setPerspective] = useState<
    "first_person" | "third_person"
  >("first_person");
  const [minWords, setMinWords] = useState(180);
  const [maxWords, setMaxWords] = useState(250);
  const [result, setResult] = useState<InnerMonologueResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [copyMessage, setCopyMessage] = useState("");
  const inFlight = useRef(false);

  async function requestMonologue(
    source: string,
    selectedPerspective: "first_person" | "third_person",
    minimum: number,
    maximum: number,
  ) {
    if (inFlight.current) {
      return;
    }
    inFlight.current = true;
    setBusy(true);
    setError("");
    setResult(null);
    setCopyMessage("");

    try {
      setResult(
        await generateInnerMonologue(
          source,
          selectedPerspective,
          minimum,
          maximum,
        ),
      );
    } catch (requestError) {
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "The monologue could not be completed. Please try again.",
      );
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!scenario.trim()) {
      setError("Describe the situation for the inner monologue.");
      setResult(null);
      return;
    }
    if (scenario.length > MAX_SCENARIO_LENGTH) {
      setError(
        `The scenario is ${scenario.length.toLocaleString()} characters; shorten it to ${MAX_SCENARIO_LENGTH.toLocaleString()} characters or fewer.`,
      );
      setResult(null);
      return;
    }
    if (
      minWords < MIN_ALLOWED_WORDS ||
      maxWords > MAX_ALLOWED_WORDS ||
      maxWords < minWords
    ) {
      setError(
        `Choose a word range from ${MIN_ALLOWED_WORDS} to ${MAX_ALLOWED_WORDS}, with the maximum at least the minimum.`,
      );
      setResult(null);
      return;
    }

    void requestMonologue(scenario, perspective, minWords, maxWords);
  }

  async function copyMonologue() {
    if (!result) {
      return;
    }
    try {
      await copyText(result.generated_text);
      setCopyMessage("The monologue has been copied.");
    } catch {
      setCopyMessage("Copy was unavailable. Select the passage and copy it manually.");
    }
  }

  return (
    <section
      className="monologue-workspace"
      aria-label="Inner Monologue workspace"
    >
      <div className="rewrite-intro">
        <div className="welcome-kicker">
          <span className="welcome-kicker__rule" />
          <span>A MIND IN MOTION</span>
        </div>
        <p>
          Give a character a situation and a divided motive. The voice may
          hesitate; the facts should not.
        </p>
      </div>

      <form className="rewrite-form monologue-form" onSubmit={handleSubmit}>
        <label className="rewrite-label" htmlFor="monologue-scenario">
          The situation
          <span>Up to {MAX_SCENARIO_LENGTH.toLocaleString()} characters</span>
        </label>
        <textarea
          id="monologue-scenario"
          className="rewrite-editor"
          value={scenario}
          disabled={busy}
          onChange={(event) => {
            setScenario(event.target.value);
            setError("");
            setResult(null);
            setCopyMessage("");
          }}
          placeholder="For example: After a cruel argument, I want to apologize to my sister, but I keep remembering the things she said years ago."
          aria-describedby="monologue-scenario-help monologue-scenario-count"
          aria-invalid={Boolean(
            error &&
              (!scenario.trim() || scenario.length > MAX_SCENARIO_LENGTH),
          )}
        />
        <div className="rewrite-form__meta">
          <p id="monologue-scenario-help">
            Include the relationships and facts the narrator should preserve.
          </p>
          <span id="monologue-scenario-count" aria-live="polite">
            {scenario.length.toLocaleString()} /{" "}
            {MAX_SCENARIO_LENGTH.toLocaleString()}
          </span>
        </div>

        <div className="monologue-controls">
          <div className="monologue-control">
            <label htmlFor="monologue-perspective">Point of view</label>
            <select
              id="monologue-perspective"
              value={perspective}
              disabled={busy}
              onChange={(event) =>
                setPerspective(
                  event.target.value === "third_person"
                    ? "third_person"
                    : "first_person",
                )
              }
            >
              <option value="first_person">First person — I</option>
              <option value="third_person">Third person — he / she / they</option>
            </select>
          </div>
          <div className="monologue-control monologue-control--word">
            <label htmlFor="monologue-min-words">Minimum words</label>
            <input
              id="monologue-min-words"
              type="number"
              min={MIN_ALLOWED_WORDS}
              max={MAX_ALLOWED_WORDS}
              step={1}
              value={minWords}
              disabled={busy}
              onChange={(event) => setMinWords(Number(event.target.value))}
            />
          </div>
          <div className="monologue-control monologue-control--word">
            <label htmlFor="monologue-max-words">Maximum words</label>
            <input
              id="monologue-max-words"
              type="number"
              min={MIN_ALLOWED_WORDS}
              max={MAX_ALLOWED_WORDS}
              step={1}
              value={maxWords}
              disabled={busy}
              onChange={(event) => setMaxWords(Number(event.target.value))}
            />
          </div>
        </div>
        <p className="monologue-range-note">
          Default length is 180–250 words. Range limits: {MIN_ALLOWED_WORDS}–
          {MAX_ALLOWED_WORDS} words. Shorter ranges (e.g. 100–180 words) may
          produce more reliable results with the local 3B model. Generated
          length can vary; the application will report any mismatch.
        </p>
        {error && (
          <p className="rewrite-error" role="alert">
            {error}
          </p>
        )}
        <div className="rewrite-actions">
          <button className="rewrite-submit" type="submit" disabled={busy}>
            {busy ? (
              <>
                <span className="rewrite-spinner" aria-hidden="true" />
                Listening for the inner voice…
              </>
            ) : (
              "Begin the Monologue"
            )}
          </button>
          {error &&
            scenario.trim() &&
            scenario.length <= MAX_SCENARIO_LENGTH &&
            !busy && (
              <button
                className="rewrite-retry"
                type="button"
                onClick={() =>
                  void requestMonologue(
                    scenario,
                    perspective,
                    minWords,
                    maxWords,
                  )
                }
                disabled={
                  minWords < MIN_ALLOWED_WORDS ||
                  maxWords > MAX_ALLOWED_WORDS ||
                  maxWords < minWords
                }
              >
                Try again
              </button>
            )}
        </div>
      </form>

      {result ? (
        <section
          className="monologue-result"
          aria-labelledby="monologue-result-heading"
          aria-live="polite"
        >
          <div className="rewrite-result__heading">
            <div>
              <p className="rewrite-result__eyebrow">AN INTERIOR VOICE</p>
              <h2 id="monologue-result-heading">The monologue</h2>
            </div>
            <button
              className="rewrite-copy"
              type="button"
              onClick={() => void copyMonologue()}
              aria-label="Copy generated monologue"
            >
              Copy
            </button>
          </div>
          <div className="monologue-result__metadata">
            <span>{result.word_count} words</span>
            <span>
              Requested: {result.requested_min_words}–{result.requested_max_words}
            </span>
            <span
              className={
                result.within_requested_range
                  ? "monologue-range monologue-range--within"
                  : "monologue-range monologue-range--outside"
              }
              role="status"
            >
              {result.within_requested_range
                ? "Within range"
                : "Outside requested range"}
            </span>
          </div>
          <article className="monologue-paper">
            <div className="rewrite-paper__topline">
              <span>INNER MONOLOGUE</span>
              <span>{result.model}</span>
            </div>
            <p>{result.generated_text}</p>
            <div className="rewrite-paper__foot">
              <span>{result.word_count} WHITESPACE-DELIMITED WORDS</span>
              <span>LOCAL GENERATION</span>
            </div>
          </article>
          {result.validation_warnings.map((warning) => (
            <p className="rewrite-warning" role="status" key={warning}>
              {warning}
            </p>
          ))}
          <p className="rewrite-disclaimer">
            Word-count and completion checks do not verify narrative quality or
            semantic fidelity. Review the result against your scenario.
          </p>
          {copyMessage && (
            <p className="rewrite-copy-message" role="status">
              {copyMessage}
            </p>
          )}
        </section>
      ) : (
        !busy && (
          <div className="cabinet-empty monologue-empty" role="status">
            <span className="rewrite-empty__rule" />
            <div>
              <p className="cabinet-empty__title">
                A private argument, not a settled answer
              </p>
              <p>
                Your monologue will appear here with its measured word count
                and requested-range status.
              </p>
            </div>
            <span className="rewrite-empty__rule" />
          </div>
        )
      )}
    </section>
  );
}
