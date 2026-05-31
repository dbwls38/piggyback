import { useEffect, useState } from "react";

function App() {

  const [state, setState] = useState({});

  useEffect(() => {

    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      setState(JSON.parse(event.data));
    };

    ws.onerror = (err) => {
      console.log("WebSocket error", err);
    };

    return () => ws.close();

  }, []);

  return (
    <div style={{ padding: 20 }}>

      <h1>🚗 AirSim Safety Dashboard</h1>

      <h3>STATE: {state.state}</h3>
      <h3>SCENARIO: {JSON.stringify(state.scenario)}</h3>

      <h3>ASIL LEVEL: {state.ASIL}</h3>
      <h3>SPEED: {state.speed}</h3>

      <h3>
        COLLISION: {state.collision ? "YES ❌" : "NO ✅"}
      </h3>

    </div>
  );
}

export default App;
