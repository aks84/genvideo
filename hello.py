import os
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

# Step 1: Prepare your script
step_titles = ["Step 1", "Step 2", "Step 3"]
step_text = ["Install software", "Configure settings", "Run the program"]

# Step 2: Generate audio and images from the script
audio_files = []
title_clips = []
step_clips = []

for i, step in enumerate(step_text):
    # Generate audio for both title and step text separately
    title_audio_filename = f"title_{i+1}.mp3"
    step_audio_filename = f"step_{i+1}.mp3"
    
    tts_title = gTTS(text=step_titles[i], lang='en')
    tts_title.save(title_audio_filename)
    audio_files.append(title_audio_filename)

    tts_step = gTTS(text=step, lang='en')
    tts_step.save(step_audio_filename)
    audio_files.append(step_audio_filename)

    # Generate title as a TextClip
    title_clip = TextClip(step_titles[i], fontsize=70, color='white', bg_color='black', size=(1280, 720)).set_duration(3)

    # Generate step text as a TextClip
    step_text_clip = TextClip(step, fontsize=50, color='yellow', bg_color='black', size=(1280, 720)).set_duration(3)

    # Add fade-in and fade-out to the title and step clips
    title_clip = title_clip.fadein(0.5).fadeout(0.5)
    step_text_clip = step_text_clip.fadein(0.5).fadeout(0.5)

    # Position title and step text (optional if you want to adjust positioning)
    title_clip = title_clip.set_position(("center", "center"))
    step_text_clip = step_text_clip.set_position(("center", "center"))

    # Create AudioFileClips for both title and step text
    title_audio_clip = AudioFileClip(title_audio_filename)
    step_audio_clip = AudioFileClip(step_audio_filename)

    # Sync the audio with the clips
    title_clip_with_audio = title_clip.set_duration(title_audio_clip.duration).set_audio(title_audio_clip)
    step_clip_with_audio = step_text_clip.set_duration(step_audio_clip.duration).set_audio(step_audio_clip)

    # Store the clips
    title_clips.append(title_clip_with_audio)
    step_clips.append(step_clip_with_audio)

# Step 3: Combine title and step clips with transitions
final_clips = []
for i in range(len(title_clips)):
    # First show the title, then the step text
    final_clips.append(title_clips[i])
    final_clips.append(step_clips[i])

# Step 4: Concatenate all clips with transitions
final_video = concatenate_videoclips(final_clips, method="compose")

# Step 5: Write the final video to a file
final_video.write_videofile("output_video.mp4", fps=24)

# Step 6: Cleanup temporary files (audio)
for audio_file in audio_files:
    os.remove(audio_file)

print("Video creation complete and temporary files cleaned up!")
