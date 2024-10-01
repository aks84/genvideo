import os
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

# Script from the file
script_title = "How to Install Python 3.12 on Ubuntu 20.04 LTS Focal Fossa Step by Step Guide"
steps = [
    "Step 1: Update Your Package List",
    "Step 2: Install Prerequisites",
    "Step 3: Add the Deadsnakes PPA",
    "Step 4: Update Your Package List Again",
    "Step 5: Install Python 3.12",
    "Step 6: Verify the Installation",
    "Step 7: Install pip for Python 3.12",
    "Step 8: Download get-pip.py"
]
step_instructions = [
    "Before installing Python 3.12, it's a good idea to ensure that your package list is updated. Run the following bash command:\nsudo apt update",
    "You'll need to install some prerequisites required for adding new repositories. Run the following bash command:\nsudo apt install -y software-properties-common",
    "Add the Deadsnakes PPA to your system to get newer Python versions. Run the following bash command:\nsudo add-apt-repository ppa:deadsnakes/ppa",
    "Update your package list again to include the new packages from the PPA. Run the following bash command:\nsudo apt update",
    "Now you can install Python 3.12 using the following command:\nsudo apt install -y python3.12",
    "Confirm that Python 3.12 has been successfully installed by checking the version:\npython3.12 --version",
    "Install pip for Python 3.12 to manage Python packages. Run the following bash command:\nsudo apt install -y python3.12-distutils",
    "Download the get-pip.py script to install pip. Run the following bash command:\nwget https://bootstrap.pypa.io/get-pip.py"
]

# Step 1: Create audio and images
audio_files = []
image_clips = []

# Title for the video
tts_title = gTTS(text=script_title, lang='en')
title_audio_filename = "title.mp3"
tts_title.save(title_audio_filename)
audio_files.append(title_audio_filename)

title_clip = TextClip(script_title, fontsize=50, color='white', bg_color='black', size=(1280, 720)).set_duration(5)
image_clips.append(title_clip)

# Loop through each step to generate audio and images
for i in range(len(steps)):
    step_title = steps[i]
    step_instruction = step_instructions[i]
    
    # Generate audio for step
    combined_text = f"{step_title}: {step_instruction}"
    audio_filename = f"step_{i+1}.mp3"
    tts = gTTS(text=combined_text, lang='en')
    tts.save(audio_filename)
    audio_files.append(audio_filename)

    # Generate image for the step
    step_title_clip = TextClip(step_title, fontsize=60, color='orange', bg_color='black', size=(1280, 720)).set_duration(3)
    step_instruction_clip = TextClip(step_instruction, fontsize=50, color='yellow', bg_color='black', size=(1280, 720)).set_duration(5)
    
    # Composite title and instruction
    step_instruction_clip = step_instruction_clip.set_position(("center", 500))
    composite_clip = CompositeVideoClip([step_title_clip, step_instruction_clip]).set_duration(5)
    
    # Add fade-in and fade-out transition
    composite_clip = composite_clip.fadein(0.5).fadeout(0.5)
    
    # Add composite clip to image clips
    image_clips.append(composite_clip)

# Step 2: Combine audio and images into video clips
final_clips = []

# First, add the title audio and image
title_audio_clip = AudioFileClip(title_audio_filename)
title_clip_with_audio = title_clip.set_duration(title_audio_clip.duration).set_audio(title_audio_clip)
final_clips.append(title_clip_with_audio)

# Then add each step's audio and image
for i in range(len(image_clips[1:])):
    audio_clip = AudioFileClip(audio_files[i+1])
    image_clip_with_audio = image_clips[i+1].set_duration(audio_clip.duration).set_audio(audio_clip)
    final_clips.append(image_clip_with_audio)

# Step 3: Concatenate video clips with transitions
final_video = concatenate_videoclips(final_clips, method="compose")

# Step 4: Write the final video to a file
final_video.write_videofile("instruct_video.mp4", fps=24)

# Step 5: Cleanup temporary files (audio)
for audio_file in audio_files:
    os.remove(audio_file)

print("Video creation complete and temporary files cleaned up!")
