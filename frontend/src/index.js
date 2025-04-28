// src/index.js

import React from "react";
import ReactDOM from "react-dom/client";
import InsuranceBot from "./insurance_bot"; // 👈 Make sure this matches your component name
import "./insurance_bot.css";               // 👈 Import your updated CSS here

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <InsuranceBot />
  </React.StrictMode>
);
