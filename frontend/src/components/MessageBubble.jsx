import { Spark } from "./Icons";
import SourceCard from "./SourceCard";

// Minimal renderer: ```fenced``` blocks and `inline code`, no extra libraries.
function RichText({ text }) {
  const parts = text.split(/```(\w*)\n?([\s\S]*?)```/g);
  const out = [];
  for (let i = 0; i < parts.length; i += 3) {
    const prose = parts[i].trim();
    if (prose)
      out.push(
        <p key={"p" + i}>
          {prose.split(/`([^`]+)`/g).map((s, j) => (j % 2 ? <code key={j}>{s}</code> : s))}
        </p>
      );
    if (i + 2 < parts.length)
      out.push(
        <pre key={"c" + i} className={parts[i + 1] === "math" ? "formula" : "codeblock"}>
          <code>{parts[i + 2].trim()}</code>
        </pre>
      );
  }
  return out;
}

const Section = ({ label, children }) => (
  <section className="section">
    <h4>{label}</h4>
    {children}
  </section>
);

export default function MessageBubble({ message }) {
  if (message.role === "user") {
    return (
      <div className="msg msg-user">
        <div className="bubble-user">{message.content}</div>
      </div>
    );
  }
  const a = message.content;
  return (
    <div className="msg msg-ai">
      <div className="avatar"><Spark size={15} /></div>
      <div className="ai-body">
        {message.error ? (
          <p className="error">{message.error}</p>
        ) : (
          <>
            {a.explanation && <Section label="Explanation"><RichText text={a.explanation} /></Section>}
            {a.formula && <pre className="formula"><code>{a.formula}</code></pre>}
            {a.intuition && <Section label="Intuition"><RichText text={a.intuition} /></Section>}
            {a.example && <Section label="Example"><RichText text={a.example} /></Section>}
            {a.takeaway && (
              <div className="takeaway">
                <h4>Key takeaway</h4>
                <p>{a.takeaway}</p>
              </div>
            )}
            {a.sources?.length > 0 && (
              <Section label="Sources">
                <div className="sources">
                  {a.sources.map((s, i) => <SourceCard key={i} source={s} />)}
                </div>
              </Section>
            )}
          </>
        )}
      </div>
    </div>
  );
}
