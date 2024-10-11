# VegaBot - Personal AI Assistant with Face Recognition & Voice Interaction

VegaBot is an AI-powered personal assistant that uses **face recognition** to verify access, **text-to-speech (TTS)** for voice interaction, and **Ollama** language models to assist users. This assistant identifies a user through a real-time camera feed, verifies their identity using **DeepFace**, and interacts with them through a conversational chatbot.

---

## Video Demo

![VegaBot Chatbot Demo](/Demo/Demo.gif)

*Above is a screen recording showing VegaBot in action. It demonstrates the face recognition and chatbot functionalities.*

---

## Features
- **Real-time face recognition** with a webcam feed using `DeepFace`.
- **Text-to-Speech** (TTS) interaction with `pyttsx3`.
- **Natural Language Processing** through **Ollama's `gemma:2b` language model**.
- **Chainlit** integration for interactive chat with a responsive interface.

---

## Prerequisites
- Python 3.7+
- Webcam for face recognition
- Speakers for audio output

---

## Installation Guide

### Step 1: Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Install Python Packages
Install the required Python dependencies using `pip`:
```bash
pip install -r requirements.txt
```

If you don't have the `requirements.txt` file, manually install the required libraries:
```bash
pip install deepface opencv-python pyttsx3 chainlit langchain langchain_community
```

### Step 3: Install Ollama on Windows

To install and configure **Ollama** on Windows, follow these steps:

1. **Download and Install Ollama**:
   - Visit the official [Ollama website](https://ollama.com/download) and download the Windows installer.
   - Run the installer and follow the instructions.

2. **Verify Ollama Installation**:
   After installation, open a terminal and run:
   ```bash
   ollama
   ```
   You should see a list of available commands.

3. **Pull the `gemma:2b` Model**:
   Once Ollama is installed, you need to pull the `gemma:2b` model:
   ```bash
   ollama pull gemma:2b
   ```

4. **Run Ollama Server**:
   Start the Ollama server:
   ```bash
   ollama run
   ```

---

## Running the Application

Once all the dependencies and Ollama are set up, you can run the application.

### Step 1: Set up the Face Database
Ensure you have a folder named `Faces` that contains images of the users you want to recognize. The structure should look like this:
```
Faces/
├── Ephraim.jpg
├── User2.jpg
```
You can add more images of different people to recognize them.

### Step 2: Start VegaBot

Run the main Python script:
```bash
python main.py
```

### Step 3: Interact with VegaBot
1. **Face Recognition**: VegaBot will start real-time face recognition using your webcam. The system will look for faces in the `Faces/` directory and authenticate the user based on a matching image.
   - If a match is found (e.g., **Ephraim**), the bot will grant access and display "Access Granted".
   - If no match is found, the message "Access Denied" will be displayed.
  
2. **Chat with VegaBot**: After access is granted, the chatbot interface will start. You can ask questions, and VegaBot will respond using the `gemma:2b` language model from Ollama.

3. **Voice Interaction**: VegaBot will speak the responses using text-to-speech (TTS) technology, powered by `pyttsx3`.

---

## Application Flow

1. **Face Recognition**:
   - The app captures a live video feed from the webcam.
   - It uses the **DeepFace** library to match the user's face against a pre-existing database (`Faces/` directory).
   - If the user is recognized, access is granted, and the chatbot interface is activated.

2. **Chatbot Interaction**:
   - After successful recognition, the user can interact with VegaBot.
   - The chatbot uses **Ollama's `gemma:2b` model** to generate responses.
   - Responses are displayed in the Chainlit interface and spoken aloud via the TTS engine.

---

## Usage Tips
- **Adding New Faces**: To recognize new users, simply add their image to the `Faces/` directory.
- **TTS Customization**: You can modify the voice and speech rate of the TTS engine by configuring `pyttsx3` settings.
- **Video Capture**: Ensure your webcam is working and accessible. You can adjust the frame processing rate by resizing the frames.

---

## Troubleshooting

- **Face Not Recognized**: Ensure the face image in `Faces/` is clear and well-lit. Adjust the `DeepFace` model or metrics if needed.
- **Audio Issues**: If TTS is not working, ensure your system's audio output is correctly configured.
- **Model Errors**: Ensure that the `gemma:2b` model is correctly pulled by Ollama and that the server is running.

---

