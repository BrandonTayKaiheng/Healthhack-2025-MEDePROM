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
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 gap-4">
      <img src={Robot} alt="Robot" className="w-48 mb-8 translate-x-3" />
      <img src={MedepromLogo} alt="MEDePROM" className="w-64 mb-8" />
      {/* <h1 className="text-3xl font-bold text-black mb-4 text-center">
        Welcome to MEDePROM
      </h1> */}
      {/* <p className="text-indigo-100 mb-8 text-center">
        Start a new conversation and connect instantly
      </p> */}
      <button
        onClick={() => navigate("/chat")}
        className="flex flex-row gap-3 bg-dark-blue text-white text-2xl px-8 py-3 rounded-xl font-semibold shadow-lg hover:bg-indigo-50 transition-colors transform hover:scale-105 duration-200"
      >
        Chat
        <MessageCircle size={36} className="text-white" />
      </button>
      <button
        onClick={() => navigate("/")}
        className="flex flex-row gap-3 bg-orange text-white text-2xl px-8 py-3 rounded-xl font-semibold shadow-lg hover:bg-indigo-50 transition-colors transform hover:scale-105 duration-200"
      >
        Call
        <Phone size={36} className="text-white" />
      </button>
    </div>
  );
}

export default WelcomeScreen;
