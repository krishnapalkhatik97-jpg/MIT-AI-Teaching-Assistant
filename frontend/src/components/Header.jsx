import { Menu, Plus, Settings, Trash } from "./Icons";

export default function Header({ onMenu, onNew, onClear, canClear }) {
  return (
    <header className="header">
      <button className="icon-btn only-mobile" onClick={onMenu} aria-label="Open sidebar"><Menu /></button>
      <div className="header-title">
        <strong>MIT AI Teaching Assistant</strong>
        <span className="status"><i /> MIT 6.0002 Knowledge Base</span>
      </div>
      <div className="header-actions">
        {canClear && (
          <button className="btn" onClick={onClear} title="Clear conversation">
            <Trash size={16} /><span className="hide-sm">Clear</span>
          </button>
        )}
        <button className="btn" onClick={onNew}><Plus size={16} /><span className="hide-sm">New Chat</span></button>
        <button className="icon-btn" aria-label="Settings"><Settings size={18} /></button>
      </div>
    </header>
  );
}
