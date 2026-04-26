import React, { useState, useRef, useEffect } from 'react';
import {
  Mic, MicOff, Camera, Activity, History, Heart, Thermometer,
  Droplets, Zap, ShieldAlert, Stethoscope, ChevronRight,
  User, LayoutDashboard, Settings, LogOut, Info
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://medisync-production-e21e.up.railway.app';

// Dampened cubic-bezier specified by Stitch
const clinicalEase = [0.2, 0, 0, 1];

const SidebarItem = ({ date, symptom, active }) => (
  <motion.div
    className={`history-item ${active ? 'active' : ''}`}
    whileHover={{ x: 5 }}
  >
    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
      <div style={{ width: '4px', height: '24px', background: active ? 'var(--primary)' : 'transparent', borderRadius: '2px' }} />
      <div>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', fontWeight: 700, textTransform: 'uppercase' }}>{date}</div>
        <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{symptom}</div>
      </div>
    </div>
  </motion.div>
);

const VitalCard = ({ label, value, unit, icon: Icon, color }) => (
  <div className="vital-card">
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <div>
        <span style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</span>
        <div className="vital-value">{value} <span style={{ fontSize: '0.85rem', color: 'var(--text-dim)', fontWeight: 400 }}>{unit}</span></div>
      </div>
      <div style={{ padding: '0.5rem', background: 'rgba(255,255,255,0.03)', borderRadius: '10px' }}>
        <Icon size={18} color={color} />
      </div>
    </div>
    {/* Micro-sparkline simulation */}
    <div style={{ marginTop: '0.75rem', height: '2px', background: 'rgba(255,255,255,0.05)', borderRadius: '1px', position: 'relative' }}>
      <motion.div
        style={{ height: '100%', background: color, width: '40%' }}
        animate={{ width: ['40%', '60%', '45%'] }}
        transition={{ duration: 2, repeat: Infinity }}
      />
    </div>
  </div>
);

const TeamMember = ({ name, role }) => (
  <motion.div
    className="team-member-card"
    whileHover={{ y: -8 }}
  >
    <div className="member-avatar">
      <User size={32} />
    </div>
    <div className="member-info">
      <div className="member-name">{name}</div>
      <div className="member-role">{role}</div>
    </div>
  </motion.div>
);

const TeamSection = () => (
  <div className="team-section">
    <div className="team-header">
      <div className="diagnostic-dot" />
      <h3 className="team-title">Project Architects</h3>
    </div>
    <div className="team-grid">
      <TeamMember name="UDIT NARAYAN YADAV" role="Lead Vision Architect" />
      <TeamMember name="ANSH SONI" role="Neural Core Engineer & tester" />
      <TeamMember name="NILESH SONI" role="PRESENTATIONS" />
    </div>
  </div>
);

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [diagnosis, setDiagnosis] = useState('');
  const [audioUrl, setAudioUrl] = useState(null);
  const [status, setStatus] = useState('SYSTEM READY');

  const [vitals, setVitals] = useState({ bpm: 72, temp: 98.6, o2: 98 });

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioPlayerRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setVitals(v => ({
        bpm: Math.floor(70 + Math.random() * 5),
        temp: (98.4 + Math.random() * 0.4).toFixed(1),
        o2: Math.floor(97 + Math.random() * 3)
      }));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setStatus('BIO-SCAN CAPTURED');
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      mediaRecorderRef.current.ondataavailable = (e) => audioChunksRef.current.push(e.data);
      mediaRecorderRef.current.onstop = () => submitConsultation(new Blob(audioChunksRef.current, { type: 'audio/webm' }));
      mediaRecorderRef.current.start();
      setIsRecording(true);
      setStatus('LISTENING...');
    } catch (err) {
      setStatus('HW FAILURE: MIC');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      setStatus('NEURAL PROCESSING...');
    }
  };

  const submitConsultation = async (audioBlob) => {
    if (!image) {
      setStatus('SCAN REQUIRED');
      return;
    }
    setIsProcessing(true);
    const formData = new FormData();
    formData.append('image', image);
    formData.append('audio', audioBlob, 'voice.webm');
    try {
      const resp = await axios.post(`${API_BASE_URL}/api/process`, formData);
      setTranscription(resp.data.transcription);
      setDiagnosis(resp.data.response);
      setAudioUrl(`${API_BASE_URL}${resp.data.audio_url}?v=${Date.now()}`);
      setStatus('ANALYSIS COMPLETE');
    } catch (err) {
      setStatus('LINK FAILURE');
    } finally {
      setIsProcessing(false);
    }
  };

  useEffect(() => {
    if (audioUrl && audioPlayerRef.current) audioPlayerRef.current.play().catch(() => { });
  }, [audioUrl]);

  return (
    <>
      <div className="mesh-bg" />

      <div className="app-container">
        {/* LEFT NAV: History & Navigation */}
        <motion.div
          className="tonal-card sidebar"
          initial={{ x: -40, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ ease: clinicalEase, duration: 0.8 }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2.5rem', paddingLeft: '1rem' }}>
            <div className="diagnostic-dot" />
            <h3 style={{ fontSize: '0.8rem', letterSpacing: '2px', color: 'var(--primary)' }}>SYNAPSE AI</h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ fontSize: '0.65rem', fontWeight: 800, color: 'var(--text-dim)', marginBottom: '0.5rem', paddingLeft: '1rem' }}>CONSULTATION LOG</div>
            <SidebarItem date="20 APR 2024" symptom="Dermatological Check" active />
            <SidebarItem date="18 APR 2024" symptom="Vision Fatigue" />
            <SidebarItem date="15 APR 2024" symptom="Acute Migraine" />
          </div>

          <div style={{ marginTop: 'auto', padding: '1.25rem', background: '#111318', borderRadius: '16px', border: '1px solid var(--glass-border)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.7rem', fontWeight: 700 }}>
              <Zap size={14} color="var(--primary)" /> CORE OPTIMAL
            </div>
            <p style={{ fontSize: '0.6rem', color: 'var(--text-dim)', marginTop: '0.5rem', lineHeight: '1.4' }}>
              Neural Link: Active (0.4ms lat)<br />
              Clinical Core: v2.4.0-stich
            </p>
          </div>
        </motion.div>

        {/* MAIN: Diagnostic Center */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 1rem' }}>
            <div className="title-section">
              <motion.h1
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 1 }}
              >MEDIGEN-AI-VISION AND VOICE</motion.h1>
              <p style={{ color: 'var(--text-dim)', fontSize: '0.8rem', fontWeight: 600, letterSpacing: '3px', marginTop: '-5px' }}>NEXT-GEN DIAGNOSTIC INTERFACE</p>
            </div>
            <div style={{ width: '40px', height: '40px', borderRadius: '50%', background: 'var(--surface-high)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <User size={20} color="var(--text-dim)" />
            </div>
          </header>

          <motion.div
            className="vision-portal"
            initial={{ scale: 0.98, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ ease: clinicalEase, duration: 1 }}
            onClick={() => fileInputRef.current.click()}
          >
            {isProcessing && <div className="scanline-active" />}
            {preview ? (
              <img src={preview} style={{ width: '100%', height: '100%', objectFit: 'cover' }} alt="Scan" />
            ) : (
              <div style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <Camera size={48} style={{ color: 'var(--primary)', opacity: 0.4, marginBottom: '1rem' }} />
                <p style={{ fontSize: '0.75rem', fontWeight: 800, letterSpacing: '2px', color: 'var(--text-dim)' }}>PLACE SCAN FOR ANALYSIS</p>
              </div>
            )}
            <input type="file" ref={fileInputRef} hidden onChange={handleImageChange} />
          </motion.div>

          <AnimatePresence>
            {diagnosis && (
              <motion.div
                className="insight-glow"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ ease: clinicalEase }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                  <Stethoscope size={18} color="var(--primary)" />
                  <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '2px' }}>Clinical Synthesized Report</h3>
                </div>
                <p style={{ lineHeight: '1.7', fontSize: '1rem', color: '#f0f0f0', fontWeight: 400 }}>{diagnosis}</p>
                <div style={{ marginTop: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.7rem', color: 'var(--text-dim)' }}>
                  <Info size={14} /> Report generated by Synapse-4o Neural Core
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* RIGHT: Vitals & Comm Link */}
        <motion.div
          className="tonal-card vitals-panel"
          initial={{ x: 40, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ ease: clinicalEase, duration: 0.8 }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem' }}>
            <Activity size={18} color="var(--primary)" />
            <h3 style={{ fontSize: '0.8rem', letterSpacing: '2px' }}>BIOMETRIC STREAM</h3>
          </div>

          <VitalCard label="Heart Rate" value={vitals.bpm} unit="BPM" icon={Heart} color="#00E5FF" />
          <VitalCard label="O2 Saturation" value={vitals.o2} unit="%" icon={Droplets} color="#bcff90" />
          <VitalCard label="Thermal Profile" value={vitals.temp} unit="°F" icon={Thermometer} color="#ffab40" />

          <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.25rem' }}>
            <p style={{ fontSize: '0.65rem', fontWeight: 800, letterSpacing: '1px', color: 'var(--text-dim)' }}>
              {status}
            </p>
            <motion.button
              className={`mic-button ${isRecording ? 'recording' : ''}`}
              onMouseDown={startRecording}
              onMouseUp={stopRecording}
              onMouseLeave={stopRecording}
              disabled={!image || isProcessing}
              whileTap={{ scale: 0.95 }}
            >
              {isRecording ? <MicOff size={36} /> : <Mic size={36} />}
            </motion.button>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.55rem', color: 'rgba(255,255,255,0.3)', background: 'rgba(255,0,0,0.05)', padding: '4px 12px', borderRadius: '20px' }}>
              <ShieldAlert size={10} /> CLINICAL ADVISORY MODE ONLY
            </div>
          </div>
        </motion.div>

        <TeamSection />
      </div>

      {audioUrl && <audio ref={audioPlayerRef} src={audioUrl} />}
    </>
  );
}

export default App;
