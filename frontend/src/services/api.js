const API_BASE = "http://127.0.0.1:8000";

function parseAnswer(answer) {
  const getSection = (start, end) => {
    const startIndex = answer.indexOf(start);

    if (startIndex === -1) return "";

    const contentStart = startIndex + start.length;

    const endIndex = end
      ? answer.indexOf(end, contentStart)
      : answer.length;

    return answer
      .slice(contentStart, endIndex === -1 ? answer.length : endIndex)
      .trim();
  };

  return {
    explanation: getSection(
      "### Explanation",
      "### Intuition"
    ),

    intuition: getSection(
      "### Intuition",
      "### Example"
    ),

    example: getSection(
      "### Example",
      "### Key Takeaway"
    ),

    takeaway: getSection(
      "### Key Takeaway",
      "### Sources"
    ),
  };
}

export async function askQuestion(question) {
  const response = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to get answer from backend");
  }

  const data = await response.json();

  const answer = parseAnswer(data.answer || "");

  return {
    ...answer,

    sources: (data.sources || []).map((source) => ({
      name: source.lecture,
      chunk: source.chunk_id,
      distance: source.distance,
    })),
  };
}