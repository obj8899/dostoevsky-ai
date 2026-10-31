import { useRef, useState, type FormEvent } from "react";

import {
  ApiError,
  openWordCabinet,
  type WordCabinetResponse,
} from "../api/client";

const MAX_CONTEXT_LENGTH = 2000;

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

export default function WordCabinet() {
  const [context, setContext] = useState("");
  const [count, setCount] = useState(6);
  const [result, setResult] = useState<WordCabinetResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [copyMessage, setCopyMessage] = useState("");
  const inFlight = useRef(false);

  async function requestWords(source: string, requestedCount: number) {
    if (inFlight.current) {
      return;
    }
    inFlight.current = true;
    setBusy(true);
    setError("");
    setResult(null);
    setCopyMessage("");

    try {
      setResult(await openWordCabinet(source, requestedCount));
    } catch (requestError) {
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "The vocabulary request could not be completed. Please try again.",
      );
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!context.trim()) {
      setError("Describe the feeling or state of mind you want to name.");
      setResult(null);
      return;
    }
    if (context.length > MAX_CONTEXT_LENGTH) {
      setError(
        `The context is ${context.length.toLocaleString()} characters; shorten it to ${MAX_CONTEXT_LENGTH.toLocaleString()} characters or fewer.`,
      );
      setResult(null);
      return;
    }
    void requestWords(context, count);
  }

  async function copyValue(value: string, label: string) {
    try {
      await copyText(value);
      setCopyMessage(`${label} copied.`);
    } catch {
      setCopyMessage("Copy was unavailable. Select the text and copy it manually.");
    }
  }

  return (
    <section className="cabinet-workspace" aria-label="Word Cabinet workspace">
      <div className="rewrite-intro">
        <div className="welcome-kicker">
          <span className="welcome-kicker__rule" />
          <span>THE EXACT WORD</span>
        </div>
        <p>
          Describe a state of mind. Explore its shades, neighboring words, and
          the difference each one makes.
        </p>
      </div>

      <form className="rewrite-form cabinet-form" onSubmit={handleSubmit}>
        <label className="rewrite-label" htmlFor="cabinet-context">
          The feeling or situation
          <span>Up to {MAX_CONTEXT_LENGTH.toLocaleString()} characters</span>
        </label>
        <textarea
          id="cabinet-context"
          className="rewrite-editor"
          value={context}
          disabled={busy}
          onChange={(event) => {
            setContext(event.target.value);
            setError("");
            setResult(null);
            setCopyMessage("");
          }}
          placeholder="For example: I am grateful for the opportunity, but resentful that I was overlooked until someone else declined."
          aria-describedby="cabinet-context-help cabinet-context-count"
          aria-invalid={Boolean(
            error && (!context.trim() || context.length > MAX_CONTEXT_LENGTH),
          )}
        />
        <div className="rewrite-form__meta">
          <p id="cabinet-context-help">
            A specific context helps distinguish a feeling from its nearest
            neighbors.
          </p>
          <span id="cabinet-context-count" aria-live="polite">
            {context.length.toLocaleString()} /{" "}
            {MAX_CONTEXT_LENGTH.toLocaleString()}
          </span>
        </div>
        <div className="cabinet-form__options">
          <label htmlFor="cabinet-count">Number of suggestions</label>
          <select
            id="cabinet-count"
            value={count}
            disabled={busy}
            onChange={(event) => setCount(Number(event.target.value))}
            aria-describedby="cabinet-count-help"
          >
            {[3, 4, 5, 6, 7, 8].map((value) => (
              <option key={value} value={value}>
                {value} words
              </option>
            ))}
          </select>
        </div>
        <p id="cabinet-count-help" className="cabinet-count-help">
          Fewer suggestions can reduce generation time on local hardware. Try four entries for a quicker vocabulary session.
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
                Turning the words…
              </>
            ) : (
              "Open the Cabinet"
            )}
          </button>
          {error &&
            context.trim() &&
            context.length <= MAX_CONTEXT_LENGTH &&
            !busy && (
              <button
                className="rewrite-retry"
                type="button"
                onClick={() => void requestWords(context, count)}
              >
                Try again
              </button>
            )}
        </div>
      </form>

      {result ? (
        <section
          className="cabinet-results"
          aria-labelledby="cabinet-results-heading"
          aria-live="polite"
        >
          <div className="rewrite-result__heading">
            <div>
              <p className="rewrite-result__eyebrow">WORDS IN CONTEXT</p>
              <h2 id="cabinet-results-heading">The cabinet is open</h2>
            </div>
            <span className="cabinet-results__count">
              {result.words.length} {result.words.length === 1 ? "entry" : "entries"}
            </span>
          </div>
          {result.validation_warnings.map((warning) => (
            <p className="rewrite-warning" role="status" key={warning}>
              {warning}
            </p>
          ))}
          {result.words.length ? (
            <div className="cabinet-cards">
              {result.words.map((entry, index) => (
                <article className="cabinet-card" key={`${entry.word}-${index}`}>
                  <div className="cabinet-card__topline">
                    <span className="cabinet-card__index">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    <span className="cabinet-card__part">
                      {entry.part_of_speech}
                    </span>
                    <button
                      className="cabinet-card__copy"
                      type="button"
                      onClick={() => void copyValue(entry.word, entry.word)}
                      aria-label={`Copy the word ${entry.word}`}
                    >
                      Copy word
                    </button>
                  </div>
                  <h3>{entry.word}</h3>
                  <p className="cabinet-card__definition">{entry.definition}</p>
                  <div className="cabinet-card__intensity">
                    <span>INTENSITY</span>
                    <span
                      className="cabinet-card__scale"
                      role="img"
                      aria-label={`Intensity ${entry.intensity} out of 5`}
                    >
                      {Array.from({ length: 5 }, (_, scaleIndex) => (
                        <span
                          className={
                            scaleIndex < entry.intensity
                              ? "cabinet-card__scale-mark is-filled"
                              : "cabinet-card__scale-mark"
                          }
                          key={scaleIndex}
                        />
                      ))}
                    </span>
                    <span>{entry.intensity} / 5</span>
                  </div>
                  <dl className="cabinet-card__details">
                    <div>
                      <dt>Connotation</dt>
                      <dd>{entry.connotation}</dd>
                    </div>
                    <div>
                      <dt>A nearby distinction</dt>
                      <dd>{entry.distinction}</dd>
                    </div>
                  </dl>
                  <div className="cabinet-card__example">
                    <div className="cabinet-card__example-heading">
                      <span>IN A SENTENCE</span>
                      <button
                        className="cabinet-card__copy"
                        type="button"
                        onClick={() => void copyValue(entry.example, "Example")}
                        aria-label={`Copy the example for ${entry.word}`}
                      >
                        Copy example
                      </button>
                    </div>
                    <p>{entry.example}</p>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <p className="cabinet-empty-result">
              No usable vocabulary entries were returned. Try refining the
              context and request again.
            </p>
          )}
          <p className="rewrite-disclaimer">
            These are language suggestions, not authoritative dictionary
            definitions or clinical guidance. Connotations can vary by context
            and speaker.
          </p>
          <p className="cabinet-model-note">LOCAL MODEL · {result.model}</p>
          {copyMessage && (
            <p className="rewrite-copy-message" role="status">
              {copyMessage}
            </p>
          )}
        </section>
      ) : (
        !busy && (
          <div className="cabinet-empty" role="status">
            <span className="rewrite-empty__rule" />
            <div>
              <p className="cabinet-empty__title">A cabinet of distinctions</p>
              <p>
                Suggested words will appear with meaning, nuance, intensity,
                and an example in use.
              </p>
            </div>
            <span className="rewrite-empty__rule" />
          </div>
        )
      )}
    </section>
  );
}
