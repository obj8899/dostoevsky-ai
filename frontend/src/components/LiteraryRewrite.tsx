import { useRef, useState, type FormEvent } from "react";

import {
  ApiError,
  rewriteLiteraryText,
  type LiteraryRewriteResponse,
} from "../api/client";

const MAX_INPUT_LENGTH = 5000;

export default function LiteraryRewrite() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<LiteraryRewriteResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [copyMessage, setCopyMessage] = useState("");
  const inFlight = useRef(false);

  async function requestRewrite(source: string) {
    if (inFlight.current) {
      return;
    }
    inFlight.current = true;
    setBusy(true);
    setError("");
    setResult(null);
    setCopyMessage("");

    try {
      setResult(await rewriteLiteraryText(source));
    } catch (requestError) {
      setResult(null);
      setError(
        requestError instanceof ApiError
          ? requestError.message
          : "The rewrite could not be completed. Please try again.",
      );
    } finally {
      inFlight.current = false;
      setBusy(false);
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!text.trim()) {
      setError("Enter a passage before asking for a rewrite.");
      setResult(null);
      return;
    }
    if (text.length > MAX_INPUT_LENGTH) {
      setError(
        `The passage is ${text.length.toLocaleString()} characters; shorten it to ${MAX_INPUT_LENGTH.toLocaleString()} characters or fewer.`,
      );
      setResult(null);
      return;
    }
    void requestRewrite(text);
  }

  async function copyRewrite() {
    if (!result) {
      return;
    }
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(result.rewritten_text);
      } else {
        const temporary = document.createElement("textarea");
        temporary.value = result.rewritten_text;
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
      setCopyMessage("The rewrite has been copied.");
    } catch {
      setCopyMessage("Copy was unavailable. Select the passage and copy it manually.");
    }
  }

  return (
    <section className="rewrite-workspace" aria-label="Literary Rewrite workspace">
      <div className="rewrite-intro">
        <div className="welcome-kicker">
          <span className="welcome-kicker__rule" />
          <span>MEANING, RECAST</span>
        </div>
        <p>
          Keep the heart of the passage intact; let its inner tensions come
          nearer to the surface.
        </p>
      </div>

      <form className="rewrite-form" onSubmit={handleSubmit}>
        <label className="rewrite-label" htmlFor="source-text">
          Your passage
          <span>Up to {MAX_INPUT_LENGTH.toLocaleString()} characters</span>
        </label>
        <textarea
          id="source-text"
          className="rewrite-editor"
          value={text}
          disabled={busy}
          onChange={(event) => {
            setText(event.target.value);
            setError("");
            setResult(null);
            setCopyMessage("");
          }}
          placeholder="Write or paste a passage. The rewrite will preserve its people, events, relationships, and outcome."
          aria-describedby="source-help source-count"
          aria-invalid={Boolean(
            error && (!text.trim() || text.length > MAX_INPUT_LENGTH),
          )}
        />
        <div className="rewrite-form__meta">
          <p id="source-help">
            The source is sent to your configured local Ollama service for
            processing.
          </p>
          <span id="source-count" aria-live="polite">
            {text.length.toLocaleString()} / {MAX_INPUT_LENGTH.toLocaleString()}
          </span>
        </div>
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
                Attending to the passage…
              </>
            ) : (
              "Rewrite"
            )}
          </button>
          {error &&
            text.trim() &&
            text.length <= MAX_INPUT_LENGTH &&
            !busy && (
            <button
              className="rewrite-retry"
              type="button"
              onClick={() => void requestRewrite(text)}
            >
              Try again
            </button>
          )}
        </div>
      </form>

      {result ? (
        <section
          className="rewrite-result"
          aria-labelledby="rewrite-result-heading"
          aria-live="polite"
        >
          <div className="rewrite-result__heading">
            <div>
              <p className="rewrite-result__eyebrow">A NEW READING</p>
              <h2 id="rewrite-result-heading">The rewritten passage</h2>
            </div>
            <button
              className="rewrite-copy"
              type="button"
              onClick={() => void copyRewrite()}
              aria-label="Copy rewritten passage"
            >
              Copy
            </button>
          </div>
          <div className="rewrite-comparison">
            <article className="rewrite-original">
              <h3>Original passage</h3>
              <p>{result.original_text}</p>
            </article>
            <article className="rewrite-paper">
              <div className="rewrite-paper__topline">
                <span>LITERARY REWRITE</span>
                <span>{result.word_count} WORDS</span>
              </div>
              <p className="rewrite-paper__prose">{result.rewritten_text}</p>
              <div className="rewrite-paper__foot">
                <span>{result.model}</span>
                <span>LOCAL GENERATION</span>
              </div>
            </article>
          </div>
          {result.validation_warnings.map((warning) => (
            <p className="rewrite-warning" role="status" key={warning}>
              {warning}
            </p>
          ))}
          {copyMessage && (
            <p className="rewrite-copy-message" role="status">
              {copyMessage}
            </p>
          )}
          <p className="rewrite-disclaimer">
            This format check does not verify that the meaning has been
            preserved; review the rewrite before using it.
          </p>
        </section>
      ) : (
        !busy && (
          <div className="rewrite-empty" role="status">
            <span className="rewrite-empty__rule" />
            <p>Your rewritten passage will appear here.</p>
            <span className="rewrite-empty__rule" />
          </div>
        )
      )}
    </section>
  );
}
