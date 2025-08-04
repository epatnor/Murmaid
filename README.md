# Murmaid

> 🧠 The whispering voice inside your machine.

**Murmaid** is a local-first conversational assistant that speaks back using high-quality text-to-speech – all running offline on your own hardware. It combines:

- 🧠 Any **local LLM** via [Ollama](https://ollama.com) for intelligent text generation
- 🔊 **Dia** by [Nari Labs](https://github.com/nari-labs/dia) for realistic voice synthesis
- 🌐 A simple web interface (FastAPI + HTML) to type prompts and hear responses

---

## 🎯 Features

- Fully **offline** – no APIs, no accounts, no surveillance
- Compatible with **any Ollama model** (e.g. Qwen, LLaMA, Mistral, Gemma, etc.)
- Sends your typed question to the selected LLM, then uses Dia to **speak the reply**
- Modern web UI with real-time audio playback
- Works on consumer GPUs – runs well on **RTX 4070 (8 GB)** or better

---

## 📸 Preview

> 💬 _"What's the weather like in the Shire?"_  
> 🗣️ _"Sunny, with a chance of second breakfast."_  

---

## 🛠 Requirements

- Windows 10/11 (Linux possible with slight tweaks)
- Python 3.10+
- [Ollama](https://ollama.com/download)
- Any Ollama-supported model (e.g. `ollama run mistral`, `ollama run llama3`, etc.)
- [Dia TTS](https://github.com/nari-labs/dia) installed and working locally

---

## 🚀 Installation

1. **Clone this repository**

⚠️ On first run, Murmaid will automatically download and set up Dia (~6 GB). Make sure you have a stable internet connection.

```bash
git clone https://github.com/epatnor/murmind.git
cd murmind
