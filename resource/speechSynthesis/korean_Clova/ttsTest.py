from gtts import gTTS
text ="안녕하세요, 여러분. 제 이름은 래미 입니다!"

tts = gTTS(text=text, lang='ko')
tts.save("./resource/speechSynthesis/helloLEMME.mp3")