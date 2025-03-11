import Chatbot from "./components/Chatbot";
import StartPage from "./components/StartPage";
import { BrowserRouter, Routes, Route } from "react-router";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<StartPage />} />
        <Route path="/chat" element={<Chatbot />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
