import { useEffect, useState } from "react";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking backend...");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => response.json())
      .then((data) => {
        setBackendStatus(data.status);
      })
      .catch(() => {
        setBackendStatus("Backend unavailable");
      });
  }, []);

  return (
    <div>
      <h1>Intelligent Project Delivery Workspace</h1>

      <p>
        Backend status: <strong>{backendStatus}</strong>
      </p>
    </div>
  );
}

export default App;