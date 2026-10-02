import { Close, Plus, Settings } from "./Icons";

export default function Sidebar({ conversations, activeId, onSelect, onNew, open, onClose }) {
  return (
    <>
      <div className={"overlay" + (open ? " show" : "")} onClick={onClose} />
      <aside className={"sidebar" + (open ? " open" : "")}>
        <div className="brand">
          <div className="logo">MIT</div>
          <div>
            <strong>MIT AI TA</strong>
            <span>MIT 6.0002</span>
          </div>
          <button className="icon-btn only-mobile" onClick={onClose} aria-label="Close sidebar"><Close /></button>
        </div>

        <button className="new-btn" onClick={onNew}><Plus size={16} /> New Question</button>

        <div className="side-label">Recent Questions</div>
        <nav className="history">
          {conversations.length === 0 && <p className="side-empty">Your questions will appear here.</p>}
          {conversations.map((c) => (
            <button key={c.id} className={"history-item" + (c.id === activeId ? " active" : "")} onClick={() => onSelect(c.id)} title={c.title}>
              {c.title}
            </button>
          ))}
        </nav>

        <div className="side-foot">
          <div>
            <strong>MIT 6.0002</strong>
            <span>AI Teaching Assistant</span>
          </div>
          <button className="icon-btn" aria-label="Settings"><Settings size={18} /></button>
        </div>
      </aside>
    </>
  );
}
