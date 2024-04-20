import React from "react";
import { useNavigate } from "react-router-dom";
const Home = () => {
  const navigate = useNavigate();
  function HandleClick() {
    navigate("/inv");
  }
  return (
    <div className="flex justify-center items-center h-screen bg-blue-400">
      {/* Your existing Home component content here */}
      <div className="card bg-white rounded-md  shadow-md p-4 w-1/4 h-1/2 ">
        <p className="text-center text-3xl">WELCOME USER!</p>
        <div className="flex flex-col text-xl items-center gap-10 pt-10 font-poppins">
          <button
            className="bg-blue-100 text-black-100 w-1/2 p-2 rounded-md text-center hover:scale-x-105 hover:scale-y-105 transition-all"
            onClick={HandleClick}
          >
            INVENTORY
          </button>
          <button className="bg-blue-100 text-black-100 w-1/2  p-2 rounded-md text-center hover:scale-x-105 hover:scale-y-105 transition-all">
            RECIPIES
          </button>
          <button className="bg-blue-100 text-black-100 w-1/2 p-2 rounded-md text-center hover:scale-x-105 hover:scale-y-105 transition-all">
            ADD ITEMS
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;
