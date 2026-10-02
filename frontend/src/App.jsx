import { useRef, useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import { askQuestion } from "./services/api";

const SEED = ["What is gradient descent?", "Explain objective functions", "Linear regression vs gradient descent", "What is K-means clustering?"]
  .map((title, i) => ({ id: "seed" + i, title, messages: [] }));

let uid = 0;
const nid = () => `m${Date.now()}_${uid++}`;

export default function App() {
  const [conversations, setConversations] = useState(SEED);
  const [activeId, setActiveId] = useState(null);
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const inputRef = useRef(null);

  const active = conversations.find((c) => c.id === activeId);
  const messages = active?.messages ?? [];

  const patch = (id, fn) =>
    setConversations((cs) => cs.map((c) => (c.id === id ? { ...c, messages: fn(c.messages) } : c)));

  const newChat = () => {
    setActiveId(null);
    setDraft("");
    setSidebarOpen(false);
    inputRef.current?.focus();
  };

  const clearChat = () => active && patch(active.id, () => []);

  const send = async () => {
    const q = draft.trim();
    if (!q || loading) return;
    let id = activeId;
    if (!id) {
      id = "c" + Date.now();
      setConversations((cs) => [{ id, title: q, messages: [] }, ...cs]);
      setActiveId(id);
    }
    setDraft("");
    setLoading(true);
    patch(id, (m) => [...m, { id: nid(), role: "user", content: q }]);
    try {
      const answer = await askQuestion(q);
      patch(id, (m) => [...m, { id: nid(), role: "ai", content: answer }]);
    } catch {
      patch(id, (m) => [...m, { id: nid(), role: "ai", error: "Something went wrong reaching the backend. Is it running on http://127.0.0.1:8000?" }]);
    } finally {
      setLoading(false);
    }
  };

  const suggest = (text) => {
    setDraft(text);
    inputRef.current?.focus();
  };

  return (
    <div className="app">
      <Sidebar
        conversations={conversations}
        activeId={activeId}
        onSelect={(id) => { setActiveId(id); setSidebarOpen(false); }}
        onNew={newChat}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />
      <main className="main">
        <Header onMenu={() => setSidebarOpen(true)} onNew={newChat} onClear={clearChat} canClear={messages.length > 0} />
        <ChatWindow messages={messages} loading={loading} onSuggest={suggest} />
        <InputBox value={draft} onChange={setDraft} onSend={send} disabled={loading} inputRef={inputRef} />
      </main>
    </div>
  );
}
