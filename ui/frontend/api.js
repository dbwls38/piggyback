import axios from "axios";

const API = "http://localhost:8000";

export const runScenario = async (type) => {
  const res = await axios.post(`${API}/scenario`, { type });
  return res.data;
};
