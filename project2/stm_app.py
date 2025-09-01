import streamlit as st
from AI_agents import AI
from audio_control import Call
from audiorecorder import audiorecorder
import io

voice = Call()
ai=AI()
chats = {
        'user':[],
        'AI':[],
        }
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["call","chat"])

if page=='chat':
    st.title('Chat bot')
    if chats:
        for i in range(len(chats["AI"])):
            st.write(f'user:{chats['user'][i]}')
            st.write(f'AI:{chats['AI'][i]}')

    prompt = st.chat_input("Ask my anything")
    if prompt:
        st.write(f'user:{prompt}')
        result=ai.rn(query=prompt)
        st.write(f'AI:{result}')
        chats['user'].append(prompt)
        chats['AI'].append(result)

elif page=='call':
    st.title("🎙️ Record Audio in Streamlit")

# Add recorder
    audio = audiorecorder("Click to record", "Click to stop recording")

    # If audio is recorded
    if len(audio) > 0:
        st.audio(audio.export(io.BytesIO(), format="wav").read(), format="audio/wav")

        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        txt = voice.listen(audio=wav_io)
        st.write(txt)
        response = ai.rn(query=txt)
        st.write(response)
        voice.speak(response)

        