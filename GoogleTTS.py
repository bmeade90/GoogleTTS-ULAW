import sys
import requests #py.exe -m pip install requests
import warnings
import logging
import os
import json
import base64
import google.auth #py.exe -m pip install google-auth
import google.auth.transport.requests

#List of voices and languages available- https://cloud.google.com/text-to-speech/docs/voices


def main():
   warnings.filterwarnings("ignore")

   text_for_tts = 'Thank you for calling Fake Insurance Company.  The user at this extension is either on the phone or away from their desk.  Please leave a message and they will call you back.'

   #Authenticate with Google Cloud platform using JSON file
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:\\Users\\Brian\\Google Drive\\send-spark-message-16ac39805baf.json'
   creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
   auth_req = google.auth.transport.requests.Request()
   creds.refresh(auth_req)

   s = requests.Session()
   headers= {'Authorization': 'Bearer ' + creds.token}

   #AudioEncoding Enums
   #AUDIO_ENCODING_UNSPECIFIED = 0;
   #LINEAR16 = 1;
   #MP3 = 2;
   #OGG_OPUS = 3;
   #MP3_64_KBPS = 4;
   #MULAW = 5;
   #ALAW = 6;
   json_body = {'input':{'text':text_for_tts},'voice':{'languageCode':'en-us','name':'en-US-Wavenet-F','ssmlGender':'FEMALE'},'audioConfig':{'audioEncoding': 5,'sampleRateHertz':8000}}

   tts_req = s.post('https://texttospeech.googleapis.com/v1/text:synthesize',headers=headers, json=json_body)
   response = json.loads(tts_req.text)

   with open("output.wav", "wb") as out:
       out.write(base64.b64decode(response['audioContent']))
       print('Audio content written to file "output.wav"')


if __name__ == "__main__":
   main()
