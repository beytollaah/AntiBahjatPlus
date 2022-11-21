"""
Women, Life, Liberty
A pipeline and UI to blur human faces in videos, and change the audio
Contact me: twitter.com/beytollaah

"""
import gradio as gr
import os
import subprocess


def video_func(video, keep_audio, defacing_sensitivity, audio_change_coef):

  name = ''.join(video.split(sep='.')[:-1])
  extension = video.split(sep='.')[-1]

  # run deface algorithm
  deface_thresh_command = '-- thresh ' + str(1 - defacing_sensitivity)
  run = subprocess.run(["deface", video, deface_thresh_command])
  output = name + '_anonymized.' + extension

  if keep_audio:
    # extract audio from the original video
    subprocess.run(["ffmpeg", '-i', video, '-vn', name + '_audio.wav'])

    # change the voice if requested
    if audio_change_coef != 0:
      tone_freq = 44100 * (1 + audio_change_coef)
      voice_change_command = 'asetrate=' + str(tone_freq) + ',aresample=44100,' + 'atempo=' + str(1/(1 + audio_change_coef))
      subprocess.run(['ffmpeg', '-i', name + '_audio.wav', '-af', voice_change_command, name + '_altered_audio.wav'])

      # add altered audio the the new video
      subprocess.run(["ffmpeg", '-i', name + '_anonymized.' + extension, '-i', name + '_altered_audio.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-shortest', name + '_anonymized_with_audio.' + extension])
    else:
      # add the original audio to the new video
      subprocess.run(["ffmpeg", '-i', name + '_anonymized.' + extension, '-i', name + '_audio.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-shortest', name + '_anonymized_with_audio.' + extension])
    
    if os.path.isfile(name + '_anonymized_with_audio.' + extension):
      output = name + '_anonymized_with_audio.' + extension
  
  # remove sensitive files
  os.remove(video)
  if os.path.isfile(name + '_audio.wav'):
    os.remove(name + '_audio.wav')

  return output


with gr.Blocks() as ui:
    gr.Markdown("upload the video and click Run")
    with gr.Row():
        video = gr.Video(source='upload')
        
    keep_audio = gr.Checkbox(value=True, interactive=True, label='Keep the audio/صدا رو نگه دار')
    defacing_sensitivity = gr.Slider(minimum=0.01, maximum=0.99, value=0.9, interactive=True, label='Sensitivity of face detection/حساسیت تشخیص چهره')
    audio_change_coef = gr.Slider(minimum=-0.49, maximum=0.99, value=0, interactive=True, label='Audio Change Coefficient/ضریب تغییر صدا')
    btn = gr.Button("Run")
    out = gr.File()

    btn.click(fn=video_func, inputs=[video, keep_audio, defacing_sensitivity, audio_change_coef], outputs=out, queue=True)

ui.queue(concurrency_count=1)
ui.launch()