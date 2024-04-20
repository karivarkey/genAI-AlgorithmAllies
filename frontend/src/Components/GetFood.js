import React from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export const GetFood = () => {
  async function Clicked() {
    const history = useNavigate();
    try {
      const response = await axios.post("/handle_click");

      if (response == null) {
        history("/");
      } else {
        history("/inv");
      }
    } catch (error) {
      console.log(error);
    }
  }
  return (
    <div>
      <button
        className="hover:scale-x-105 hover:scale-y-105 absolute right-5 bottom-10 p-4 bg-blue-500 text-white rounded-md shadow-md"
        onClick={Clicked}
      >
        Get Recipie!
      </button>
    </div>
  );
};
