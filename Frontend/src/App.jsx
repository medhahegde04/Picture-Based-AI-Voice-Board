import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Home from "./components/Home";
import Favorites from "./components/Favourites";
import Profile from "./components/Profile";
import CameraModal from "./components/CameraModal";
import io from 'socket.io-client';

// --- BACKEND CONFIGURATION ---
const API_URL = "http://localhost:8000";
const socket = io(API_URL, {
  transports: ['websocket'],
  autoConnect: true,
});
// ------------------------------

export default function App() {
  
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("profile")) || null);
  const [isLoggedIn, setIsLoggedIn] = useState(() => !!localStorage.getItem("auth"));
  const [view, setView] = useState(isLoggedIn ? "home" : "login");
  const [menuOpen, setMenuOpen] = useState(false);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [detectionResult, setDetectionResult] = useState({
    object: null,
    phrase: "Awaiting detection...",
    confidence: null,
  });

  // Socket.IO and Backend Integration 
  useEffect(() => {
    socket.on('detection_update', (data) => {
      console.log('Received real-time detection:', data);
      setDetectionResult({
        object: data.object,
        phrase: data.phrase || "No object detected recently.",
        confidence: data.confidence,
      });
    });

    socket.on('connect', () => console.log('Connected to backend Socket.IO'));
    socket.on('disconnect', () => console.log('Disconnected from backend Socket.IO'));

    return () => {
      socket.off('detection_update');
      socket.off('connect');
      socket.off('disconnect');
    };
  }, []);

  // Function to process the captured image with the REAL backend endpoint
  async function processCapturedImage(dataUrl) {
    setCapturedImage(dataUrl);
    setCameraOpen(false);
    setDetectionResult({
      object: null,
      phrase: "Image captured. Analyzing...",
      confidence: null,
    });
    
    // --- REAL API CALL START ---
    try {
        const response = await fetch(`${API_URL}/analyze-image`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: dataUrl }),
        });

        const result = await response.json();

        if (response.ok) {
            setDetectionResult({
                object: result.object,
                phrase: result.phrase,
                confidence: result.confidence,
            });
        } else {
            console.error("Analysis API Error:", result.error);
            setDetectionResult({
                object: null,
                phrase: `Analysis failed: ${result.error || 'Server error'}`,
                confidence: null,
            });
        }

    } catch (error) {
        console.error("Network or Fetch Error analyzing image:", error);
        setDetectionResult({
            object: null,
            phrase: "Network error during analysis. Is Python server running and accessible?",
            confidence: null,
        });
    }
    // --- REAL API CALL END ---
  }


  // Effects and Navigation
  useEffect(() => {
    if (user) localStorage.setItem("profile", JSON.stringify(user));
  }, [user]);

  useEffect(() => {
    isLoggedIn ? localStorage.setItem("auth", "1") : localStorage.removeItem("auth");
  }, [isLoggedIn]);

  function navigate(to) {
    setMenuOpen(false);
    setView(to);
  }

  // Render Logic
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white shadow-2xl rounded-2xl overflow-hidden border border-slate-200">
        {view === "login" && (
          <Login
            onLogin={(cred) => {
              const stored = JSON.parse(localStorage.getItem("profile")) || null;
              if (stored && stored.username === cred.username && stored.password === cred.password) {
                setUser(stored);
                setIsLoggedIn(true);
                setView("home");
              } else {
                alert("Invalid credentials.");
              }
            }}
            onSignup={() => setView("signup")}
          />
        )}
        {view === "signup" && (
          <Signup
            onSignup={(data) => {
              localStorage.setItem("profile", JSON.stringify(data));
              setUser(data);
              setIsLoggedIn(true);
              setView("home");
            }}
            onLogin={() => setView("login")}
          />
        )}
        {view === "home" && (
          <Home
            user={user}
            onLogout={() => {
              setIsLoggedIn(false);
              setView("login");
            }}
            openMenu={() => setMenuOpen(true)}
            onOpenCamera={() => setCameraOpen(true)}
            capturedImage={capturedImage}
            detectionResult={detectionResult}
            navigate={navigate}
            menuOpen={menuOpen}
            setMenuOpen={setMenuOpen}
          />
        )}
        {view === "fav" && <Favorites onBack={() => setView("home")} />}
        {view === "profile" && (
          <Profile
            user={user}
            onUpdate={(u) => setUser(u)}
            onBack={() => setView("home")}
            onLogout={() => {
              setIsLoggedIn(false);
              setView("login");
            }}
          />
        )}
        {cameraOpen && (
          <CameraModal
            onClose={() => setCameraOpen(false)}
            onCapture={processCapturedImage} 
          />
        )}
      </div>
    </div>
  );
}