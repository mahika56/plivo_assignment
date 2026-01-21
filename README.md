This project implements a fully functional multi-level IVR (Interactive Voice Response) system using Flask, Plivo Voice API, and DTMF menu handling.  
It demonstrates outbound calling, language selection, audio playback, and call forwarding.



## Features

### Outbound Call Trigger
Enter a phone number on the web UI to automatically place an outbound call using Plivo.

### Multi-Level IVR
**Level 1 — Language Menu**
- Press 1 → English  
- Press 2 → Spanish  

**Level 2 — Action Menu**
- Press 1 → Play audio file  
- Press 2 → Connect to a live associate  

### Audio Playback
Plays a publicly hosted MP3 using Plivo’s `<Play>` XML verb.

### Call Forwarding
Uses Plivo’s `<Dial>` to forward the call to a configured number.

### Webhook Debugging (ngrok)
`http://127.0.0.1:4040` shows Plivo webhook requests in real time.


## Required Plivo Credentials

Before running this project, you need the following from your Plivo Dashboard:

1. Auth ID
2. Auth Token
3. Plivo Phone Number (FROM_NUMBER)

Add them in `app.py`:

AUTH_ID = "YOUR_AUTH_ID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
FROM_NUMBER = "YOUR_PLIVO_NUMBER"



## Setup Instructions

Follow these steps to set up and run the Plivo IVR demo locally.



### 1. Clone the repository
git clone https://github.com/<your-username>/plivo_assignment.git
cd plivo_assignment



### 2️. Create and activate a virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate



### 3️. Install project dependencies
pip install -r requirements.txt



### 4️. Add your Plivo credentials in app.py

Replace these values in app.py:

AUTH_ID = "YOUR_AUTH_ID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
FROM_NUMBER = "YOUR_PLIVO_NUMBER"



### 5️. Start the Flask server
python app.py

You should see:
Running on http://127.0.0.1:5000/

Keep this terminal open.



### 6️. Start ngrok (in a NEW terminal)
ngrok http 5000

Copy the URL shown, e.g.:
https://abcd1234.ngrok-free.app



### 7️. Update webhook URLs in code

Replace <your-ngrok-url> in:

app.py:
answer_url="https://<your-ngrok-url>/ivr/level1"

ivr.py (3 locations):
https://<your-ngrok-url>/ivr/level1
https://<your-ngrok-url>/ivr/level2
https://<your-ngrok-url>/ivr/action

Save changes → Restart Flask.



### 8️. Test the frontend
Open in browser:
http://localhost:5000/

Enter your phone number in E.164 format:
+91XXXXXXXXXX

Click Call.



### 9️. Test the IVR on your phone

You will hear:
"Press 1 for English. Press 2 for Spanish."

Then:
- Press 1 → Play audio file  
- Press 2 → Forward call to associate  



### 10. Inspect webhook logs (optional)
Open:
http://127.0.0.1:4040

You can see every webhook request Plivo sends to your server.



###  Setup complete!
Your IVR system is now fully deployed locally and connected to Plivo.





