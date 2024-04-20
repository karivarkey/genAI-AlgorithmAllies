import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Inventory } from "./Inventory"; // Assuming Inventory is a component
import Home from "./Home";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/inv" element={<Inventory />} />
      </Routes>
    </Router>
  );
}

export default App;
