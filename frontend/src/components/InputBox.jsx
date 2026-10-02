import { useEffect } from "react";
import { Send } from "./Icons";

export default function InputBox({ value, onChange, onSend, disabled, inputRef }) {
  useEffect(() => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 200) + "px";
  }, [value, inputRef]);

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      if (!disabled && value.trim()) onSend();
    }
  };

  const canSend = value.trim() && !disabled;
  return (
    <div className="input-wrap">
      <div className="input-box">
        <textarea
          ref={inputRef}
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Ask anything about MIT 6.0002..."
          aria-label="Ask a question"
        />
        <button className="send" onClick={onSend} disabled={!canSend} aria-label="Send">
          <Send size={18} />
        </button>
      </div>
      <p className="hint">Enter to send · Shift + Enter for a new line</p>
    </div>
  );
}
