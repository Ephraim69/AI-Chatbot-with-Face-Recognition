from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
import threading
import time
from deepface import DeepFace
import cv2
import pyttsx3

# Initialize the TTS engine
tts_engine = pyttsx3.init()


backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace",
          "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
metrics = ["cosine", "euclidean", "euclidean_l2"]
frame = None
stop_thread = False
access_granted = False  # Flag to check if the face recognition is successful


# Global flag to control speech
should_speak = True

def video_capture_thread(vid):
    global frame, stop_thread
    while not stop_thread:
        ret, frame = vid.read()


def realtime_face_recognition():
    global frame, stop_thread, access_granted

    # Define a video capture object
    vid = cv2.VideoCapture(1)

    # Start the video capture thread
    capture_thread = threading.Thread(target=video_capture_thread, args=(vid,))
    capture_thread.start()

    recognized_start_time = None
    required_duration = 4  # seconds

    while True:
        if frame is None:
            continue

        # Resize frame to reduce processing load
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Perform face recognition on the captured frame
        people = DeepFace.find(img_path=small_frame, db_path="./Faces",
                               model_name=models[2], distance_metric=metrics[2], enforce_detection=False)

        if len(people) > 0:
            for df in people:
                for _, person in df.iterrows():

                    if 'source_x' in person and 'source_y' in person and 'source_w' in person and 'source_h' in person:
                        # Adjust coordinates after resizing
                        x = person['source_x'] * 2
                        y = person['source_y'] * 2
                        w = person['source_w'] * 2
                        h = person['source_h'] * 2

                        cv2.rectangle(frame, (int(x), int(y)),
                                      (int(x+w), int(y+h)), (0, 255, 0), 2)

                        name = person['identity'].split('\\')[1]
                        # Remove .jpg from the filename
                        name = name[:-4].capitalize()
                        cv2.putText(frame, f"{name}, {round((1 - person['distance']) * 100, 2)}% Match", (int(x), int(y)),
                                    cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

                    if name == "Ephraim":
                        if recognized_start_time is None:
                            recognized_start_time = time.time()
                        elif time.time() - recognized_start_time >= required_duration:
                            access_granted = True
                            stop_thread = True
                            print("Access Granted.")
                            cv2.putText(frame, "Access Granted", (50, 50),
                                        cv2.FONT_ITALIC, 2, (0, 255, 0), 3)
                            break
                    else:
                        recognized_start_time = None
        else:
            recognized_start_time = None

        # Display the resulting frame with the name or access status
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', 960, 720)
        cv2.imshow('frame', frame)

        # Check if the 'q' button is pressed to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_thread = True
            break

        if stop_thread:
            break

    # Release the video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()
    capture_thread.join()


# Start the face recognition in the main thread before starting the chatbot
realtime_face_recognition()


@cl.on_chat_start
async def on_chat_start():
    global access_granted
    should_speak = True

    if not access_granted:
        await cl.Message(content="Access Denied. You are not authorized to use this bot.").send()
        return

    # Sending an image with the local file path
    elements = [
        cl.Image(name="image1", display="inline", path="VEGABOT.gif")
    ]
    welcome_message = "Hello there, I am VegaBot. Ephraim's Personal Assistant. How can I help you?"

    await cl.Message(content=welcome_message, elements=elements).send()

    if should_speak:

        # Use TTS to say the welcome message
        tts_engine.say(welcome_message)
        tts_engine.runAndWait()

    model = Ollama(model="gemma2:2b", base_url="http://localhost:11434")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "",
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    global access_granted, should_speak

    if not access_granted:
        await cl.Message(content="Access Denied. You are not authorized to use this bot.").send()
        return

    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")
    full_response = ""  # Initialize a variable to collect the full response

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
        full_response += chunk  # Append each chunk to the full response

    await msg.send()



@cl.on_stop
def on_stop():
    global should_speak
    should_speak = False  # Disable speech when chat ends
    
    try:
        # Stop any ongoing speech
        tts_engine.stop()
    except:
        pass  # Ignore any errors when trying to stop the engine
    
 

