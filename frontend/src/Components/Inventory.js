import React from "react";
import InventoryList from "./InventoryList";
import { Header } from "./Header";
import { GetFood } from "./GetFood";
const demoData = {
  contents: [
    "Apples",
    "Bananas",
    "Oranges",
    "Milk",
    "Eggs",
    "Butter",
    "Chicken",
    "Tomato",
  ],
  availableQuantity: [
    "10Kg",
    "5nos",
    "20nos",
    "3L",
    "12nos",
    "2nox",
    "5kg",
    "10",
  ],
  expiryDate: [
    "2024-05-15",
    "2024-04-25",
    null,
    "2024-05-02",
    null,
    "2024-05-08",
    "2026-03-2",
    null,
  ],
};
export const Inventory = () => {
  return (
    <div>
      <Header />
      <InventoryList {...demoData} />
      <GetFood />
    </div>
  );
};
