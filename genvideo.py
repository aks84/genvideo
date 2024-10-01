import os
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips

# Function to wrap text into multiple lines
def wrap_text(text, max_chars_per_line=40):
    words = text.split(' ')
    wrapped_text = []
    current_line = []
    
    for word in words:
        if sum(len(w) for w in current_line) + len(word) + len(current_line) <= max_chars_per_line:
            current_line.append(word)
        else:
            wrapped_text.append(' '.join(current_line))
            current_line = [word]

    wrapped_text.append(' '.join(current_line))  # Add the last line
    return '\n'.join(wrapped_text)  # Join lines with newlines

# Step 1: Read the script from the file
with open('script.txt', 'r') as file:
    script_lines = file.readlines()

# Extract the title and steps from the script
script_title = script_lines[0].strip()  # First line is the title
steps = []
step_instructions = []

current_step = None
for line in script_lines[1:]:
    line = line.strip()
    if line.startswith("Step") and line:
        if current_step:  # Save the previous step's instructions if it exists
            step_instructions.append(current_step)
        steps.append(line)  # Append step titles
        current_step = []  # Reset for the next instruction
    elif line:  # Append lines to the current step's instructions
        current_step.append(line)  # Keep adding instructions to the current step

# Add the last instruction if it exists
if current_step:
    step_instructions.append(current_step)

# Ensure the number of steps and instructions are equal
if len(steps) != len(step_instructions):
    print("Warning: The number of steps and instructions do not match.")
    print(f"Steps: {len(steps)}, Instructions: {len(step_instructions)}")
    exit()

# Step 2: Create audio and images
audio_files = []
image_clips = []

# Create title audio
tts_title = gTTS(text=script_title, lang='en')
title_audio_filename = "title.mp3"
tts_title.save(title_audio_filename)
audio_files.append(title_audio_filename)

# Create image clip for the title
wrapped_title = wrap_text(script_title, max_chars_per_line=35)  # Wrap title text
title_clip = TextClip(wrapped_title, fontsize=60, color='pink', bg_color='black', size=(1280, 720))
title_audio_clip = AudioFileClip(title_audio_filename)

# Set image duration to match the audio duration
title_clip_with_audio = title_clip.set_duration(title_audio_clip.duration).set_audio(title_audio_clip)
image_clips.append(title_clip_with_audio)

# Loop through each step to generate audio and images
for i in range(len(steps)):
    step_title = steps[i]
    
    # Generate audio for step title
    audio_filename = f"step_{i + 1}.mp3"
    tts = gTTS(text=step_title, lang='en')
    tts.save(audio_filename)
    audio_files.append(audio_filename)

    # Generate image for the step title and wrap the text
    wrapped_step_title = wrap_text(step_title, max_chars_per_line=35)
    step_title_clip = TextClip(wrapped_step_title, fontsize=60, color='yellowgreen', bg_color='black', size=(1280, 720))
    
    # Apply a zoom-in animation to the step titles (Text Animation)
    # step_title_clip = step_title_clip.resize(lambda t: 1 + 0.05*t)  # Slight zoom-in effect
    
    # Sync image duration with audio length
    step_title_audio = AudioFileClip(audio_filename)
    step_title_with_audio = step_title_clip.set_duration(step_title_audio.duration).set_audio(step_title_audio)
    image_clips.append(step_title_with_audio)

    # Process each instruction line
    for j, instruction in enumerate(step_instructions[i]):
        # Generate audio for instruction with step and instruction index
        instruction_audio_filename = f"step_{i + 1}_instruction_{j + 1}.mp3"
        tts_instruction = gTTS(text=instruction, lang='en')
        tts_instruction.save(instruction_audio_filename)
        audio_files.append(instruction_audio_filename)

        # Generate image for the instruction and wrap the text
        wrapped_instruction = wrap_text(instruction, max_chars_per_line=40)
        
        # Apply line height (interline) to the instructions text
        instruction_clip = TextClip(wrapped_instruction, fontsize=50, color='yellow', bg_color='black', size=(1280, 720), interline=10)
        
        # Sync image duration with audio length
        instruction_audio_clip = AudioFileClip(instruction_audio_filename)
        instruction_with_audio = instruction_clip.set_duration(instruction_audio_clip.duration).set_audio(instruction_audio_clip)

        # Apply crossfade transition to smooth the audio transitions
        instruction_with_audio = instruction_with_audio.crossfadein(0.5)
        
        image_clips.append(instruction_with_audio)

        # Add a pause of 1 second after each instruction
        pause_clip = TextClip("dummy text", fontsize=50, color='black', bg_color='black', size=(1280, 720)).set_duration(1)
        image_clips.append(pause_clip)  # Add pause between instructions

# Step 3: Combine audio and images into video clips
final_clips = []

# Add each step's audio and image sequentially
for clip in image_clips:
    final_clips.append(clip)

# Step 4: Concatenate video clips
final_video = concatenate_videoclips(final_clips, method="compose")

# Step 5: Write the final video to a file
final_video.write_videofile("gen_video.mp4", fps=24)

# Step 6: Cleanup temporary files (audio)
for audio_file in audio_files:
    os.remove(audio_file)  # Delete each audio file after the video is created

print("Video creation complete and temporary files cleaned up!")
