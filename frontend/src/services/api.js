// API layer. Swap `askQuestion` for a real call once the RAG endpoint exists.
// Check http://127.0.0.1:8000/docs for the actual route and response shape.
export const API_BASE = "http://127.0.0.1:8000";

const KB = [
  {
    match: /gradient descent/i,
    explanation:
      "Gradient descent is an iterative optimization method. Starting from an initial guess, it repeatedly steps in the direction that most decreases the objective function, using the gradient to decide the direction.",
    formula: "θ ← θ − α · ∇J(θ)",
    intuition:
      "Picture standing on a foggy hillside and wanting to reach the valley. You can't see the bottom, but you can feel which way the ground slopes under your feet. Step downhill, re-check the slope, repeat.",
    example:
      "```python\ndef gradient_descent(grad, x, lr=0.1, steps=100):\n    for _ in range(steps):\n        x = x - lr * grad(x)\n    return x\n```\nFor J(x) = x², the gradient is 2x, so each step shrinks x toward 0.",
    takeaway:
      "The learning rate α controls the trade-off: too small is slow, too large overshoots the minimum.",
    sources: [
      { name: "MIT6_0002F16_lec09_300k", chunk: 30, distance: 1.006 },
      { name: "MIT6_0002F16_lec08_300k", chunk: 12, distance: 1.0412 },
    ],
  },
  {
    match: /objective function/i,
    explanation:
      "An objective function is the quantity an optimization problem tries to minimize or maximize. It turns a vague goal such as “fit the data well” into a single number that algorithms can compare.",
    intuition:
      "Think of it as a score. Every candidate solution gets a score, and optimization is the search for the best one, subject to any constraints.",
    example:
      "In the knapsack problem, the objective is the total value of the items taken, and the constraint is the weight limit.",
    takeaway: "Choosing the objective function is a modeling decision; it defines what “best” means.",
    sources: [{ name: "MIT6_0002F16_lec01_300k", chunk: 14, distance: 0.9873 }],
  },
  {
    match: /k-?means|cluster/i,
    explanation:
      "K-means partitions data into k clusters by alternating two steps: assign each point to its nearest centroid, then move each centroid to the mean of its assigned points. It repeats until assignments stop changing.",
    intuition:
      "It's like placing k flags on a map, letting each house join its nearest flag, then moving each flag to the center of its neighborhood.",
    takeaway: "Results depend on the initial centroids and on the choice of k, so run it several times.",
    sources: [
      { name: "MIT6_0002F16_lec12_300k", chunk: 21, distance: 1.0188 },
      { name: "MIT6_0002F16_lec12_300k", chunk: 22, distance: 1.0731 },
    ],
  },
  {
    match: /linear regression/i,
    explanation:
      "Linear regression is a model: it assumes the output is a linear function of the inputs. Gradient descent is an algorithm: one way of finding the model's best parameters.",
    intuition:
      "Regression is the shape you're fitting; gradient descent is one of the ways you search for it. Linear regression can also be solved in closed form.",
    takeaway: "Model and optimizer are separate choices.",
    sources: [{ name: "MIT6_0002F16_lec09_300k", chunk: 8, distance: 1.1021 }],
  },
];

const FALLBACK = {
  explanation:
    "This is a mock answer. Once the RAG endpoint is connected, responses will be grounded in the MIT 6.0002 lecture transcripts.",
  takeaway: "Connect src/services/api.js to the backend to see real answers.",
  sources: [],
};

export async function askQuestion(question) {
  await new Promise((r) => setTimeout(r, 1400));
  return KB.find((k) => k.match.test(question)) || FALLBACK;
}
