import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Header: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <header className="bg-white shadow-md p-6 relative flex justify-center items-center">
      {location.pathname !== "/" && (
        <button
          onClick={() => navigate("/")}
          className="absolute left-6 px-3 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 transition"
        >
          ← Back
        </button>
      )}

      {/* Only show title on Dashboard */}
      {location.pathname === "/" && (
        <h1 className="text-3xl font-bold text-green-700 text-center">
          Welcome to BillEasy
        </h1>
      )}
    </header>
  );
};

export default Header;

