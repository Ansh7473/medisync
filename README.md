# Medisync: Synapse Clinical AI Doctor 🩺

**Medisync** is a premium, high-tech AI-powered medical consultation dashboard designed to bridge the gap between patient symptoms and clinical insights. Powered by the **Synapse Clinical AI** design system, it provides a high-density, futuristic diagnostic HUD for the next generation of healthcare.

![Synapse AI Banner](https://img.shields.io/badge/Branding-Synapse%20AI-00E5FF?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)

## ✨ Key Features
- **Multimodal AI Analysis**: Combines medical image processing (Vision) with voice transcription (STT) for a complete consultation.
- **Synapse HUD**: A professional 3-column dashboard featuring:
  - **Clinical Sentinel Sidebar**: Patient history and system status.
  - **Neural Vision Portal**: Active bio-scanning and image analysis.
  - **Biometric Stream**: Real-time vital signs monitoring with heartbeat waveforms.
- **Voice-to-Voice Pipelines**: Automated speech-to-text and premium text-to-speech feedback.
- **Premium Glassmorphism**: High-end UI detailing with dampening animations and tonal depth.

## 🛠️ Technology Stack
- **Frontend**: React (Vite), Framer Motion, Lucide Icons, Axios.
- **Backend**: FastAPI (Python), Groq Cloud (Vision & STT), gTTS/ElevenLabs (TTS).
- **Design Core**: StitchMCP "Synapse" Clinical UI.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js (v18+)
- Groq API Key (Sign up at [Groq Cloud](https://console.groq.com/))

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Ansh7473/medisync.git
   cd medisync
   ```

2. **Backend Setup**
   ```bash
   # Create a virtual environment
   python -m venv .venv

   # Activate the virtual environment
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Create a .env file with your GROQ_API_KEY
   python main.py
   ```
   
   OR RUN DIRECTLY

   ```bash

   run_and_setup.bat

   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📜 Disclaimer
This software is intended for **educational and research purposes only**. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## 👨‍💻 Author
**Ansh7473** - [GitHub Profile](https://github.com/Ansh7473)

---
*Powered by Synapse Clinical AI Design System*
