import { Arrow } from "./Icons";

export default function SuggestionCard({ text, index, onClick }) {
  return (
    <button className="suggestion" onClick={() => onClick(text)}>
      <span className="suggestion-idx">0{index + 1}</span>
      <span className="suggestion-text">{text}</span>
      <Arrow size={16} className="suggestion-arrow" />
    </button>
  );
}
