import { Doc } from "./Icons";

export default function SourceCard({ source }) {
  return (
    <div className="source">
      <Doc size={15} />
      <div className="source-body">
        <span className="source-name">{source.name}</span>
        <span className="source-meta">
          Chunk {source.chunk}
          {source.distance != null && <> · Distance {Number(source.distance).toFixed(4)}</>}
        </span>
      </div>
    </div>
  );
}
