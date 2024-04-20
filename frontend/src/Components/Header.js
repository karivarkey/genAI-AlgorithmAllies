import React from "react";
import { FaHome } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
export const Header = () => {
  const history = useNavigate();

  const handleGoBack = () => {
    history("/"); // Navigate back to the previous page
  };

  return (
    <header className="font-poppins text-3xl text-white bg-blue-600 text-center p-2 flex justify-between items-center">
      <button>
        <FaHome onClick={handleGoBack} /> {/* Add margin-right to FaHome */}
      </button>
      <h className="text-center ">Your Smort Fridge</h>
      <div></div>
    </header>
  );
};
