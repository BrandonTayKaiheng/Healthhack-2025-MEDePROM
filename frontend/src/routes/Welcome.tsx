import React, { useState, useRef, useEffect } from "react";
import {
  MessageCircle,
  Phone,
  Send,
  ArrowLeft,
  Share2,
  Check,
  Copy,
  Loader2,
} from "lucide-react";
import MedepromLogo from "../../assets/MedepromLogo.svg";
import Robot from "../../assets/Robot.svg";
import { useNavigate } from "react-router";

function WelcomeScreen() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-light-grey flex flex-col items-center justify-center">
      <div className="bg-white flex flex-col items-center justify-center p-10 gap-4 rounded-xl border border-gray-200 ">
        <img src={Robot} alt="Robot" className="w-36 mb-4 translate-x-3" />
        <img src={MedepromLogo} alt="MEDePROM" className="w-60 mb-8" />
        {/* <h1 className="text-3xl font-bold text-black mb-4 text-center">
        Welcome to MEDePROM
      </h1> */}
        {/* <p className="text-indigo-100 mb-8 text-center">
        Start a new conversation and connect instantly
      </p> */}
        <button
          onClick={() => navigate("/chat")}
          className="flex flex-row justify-center w-56 gap-3 bg-dark-blue text-white text-2xl px-8 py-3 rounded-xl font-semibold hover:shadow-lg"
        >
          Chat
          <MessageCircle size={36} className="text-white" />
        </button>
        <button
          onClick={() => navigate("/")}
          className="flex flex-row justify-center w-56 gap-3 bg-orange text-white text-2xl px-8 py-3 rounded-xl font-semibold hover:shadow-lg"
        >
          Call
          <Phone size={36} className="text-white" />
        </button>
      </div>
    </div>
  );
}

export default WelcomeScreen;
