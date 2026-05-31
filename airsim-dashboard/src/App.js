import { useEffect, useState } from "react";

const MOCK_DATA =
    {
  state: "RUNNING",
  scenario: {
    type: "RIGHT_TURN",
    Pedestrian: true
  },
  ASIL: "B",
  speed: 32,
  collision: false
};

function App() {

  const [state, setState] = useState(MOCK_DATA);

  useEffect(() => {

    // 개발 중에는 비활성화
    const ENABLE_WEBSOCKET = false;

    if (!ENABLE_WEBSOCKET) return;

    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      setState(JSON.parse(event.data));
    };

    ws.onerror = (err) => {
      console.log(err);
    };

    return () => ws.close();

  }, []);

  return (
    <div style={{ padding: 20 }}>

      <h1>🚗 AirSim Safety Dashboard</h1>

      <h3>STATE: {state.state}</h3>

      <h3>
        SCENARIO:
        {JSON.stringify(state.scenario)}
      </h3>

      <h3>ASIL LEVEL: {state.ASIL}</h3>

      <h3>SPEED: {state.speed} km/h</h3>

      <h3>
        COLLISION:
        {state.collision ? " YES " : " NO "}
      </h3>

    </div>
  );
}

export default App;