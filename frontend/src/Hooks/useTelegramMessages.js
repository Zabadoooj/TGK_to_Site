
// hooks/useTelegramMessages.js
import { useState, useEffect } from "react";

const API = "http://localhost:8000";

export function useTelegramMessages(ids) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!ids?.length) return;

    setLoading(true);
    fetch(`${API}/messages?ids=${ids.join(",")}`)
      .then((r) => r.json())
      .then((data) => setMessages(data.messages))
      .catch(setError)
      .finally(() => setLoading(false));
  }, [ids.join(",")]);

  return { messages, loading, error };
}