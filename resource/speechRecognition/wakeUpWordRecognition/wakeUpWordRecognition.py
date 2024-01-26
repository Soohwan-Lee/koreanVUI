import pvporcupine

# Demo for default
# porcupine = pvporcupine.create(
#   access_key='${ACCESS_KEY}',
#   keywords=['picovoice', 'bumblebee']
# )

# # Demo for custom keywords
# porcupine = pvporcupine.create(
#   access_key='${ACCESS_KEY}',
#   keyword_paths=['${KEYWORD_FILE_PATH}']
# )

# Demo for non-english language
file_path = './resource/speechRecognition/wakeUpWordRecognition/'
porcupine = pvporcupine.create(
  access_key='9x0FaA466xUKn2jZkaAgAakVVBOG7RV6CFf/jI7rCpHJ3NB0HJ3V1w==',
  keyword_paths=['./resource/speechRecognition/wakeUpWordRecognition/lemmyWakeUp_Mac.ppn'],
  model_path='./resource/speechRecognition/wakeUpWordRecognition/porcupine_params_ko.pv'
)

def get_next_audio_frame():
  pass

while True:
  audio_frame = get_next_audio_frame()
  keyword_index = porcupine.process(audio_frame)
  if keyword_index == 0:
      print("Lemmy Detected!")