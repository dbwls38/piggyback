import { useEffect, useState } from "react";

export default function Dashboard() {

  const [state, setState] = useState({
    state: "IDLE",
    scenario: null
  });

  useEffect(() => {

    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setState(data);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error", err);
    };

    return () => ws.close();

  }, []);

  return (
    <div style={{ padding: 20 }}>

      <h1>🚗 AirSim Live Dashboard</h1>

      <h2>Status: {state.state}</h2>

      <pre>
        {JSON.stringify(state.scenario, null, 2)}
      </pre>

    </div>
  );
}