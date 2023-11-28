import flet
from flet import TextField, ElevatedButton, Column, Text, ProgressBar
import threading

import json
import torch
from transformers import pipeline
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn


def transcribe_audio(file_name, transcript_path="output.json", model_name="openai/whisper-large-v3"):
    pipe = pipeline(
    "automatic-speech-recognition",
    model=model_name,
    batch_size=32,
    torch_dtype=torch.float16,
    device="cuda",
    model_kwargs={"use_flash_attention_2": True},
    )

    pipe.model = pipe.model.to_bettertransformer()

    ts = True

    language = None
    
    with Progress(
        TextColumn("🤗 [progress.description]{task.description}"),
        BarColumn(style="yellow1", pulse_style="white"),
        TimeElapsedColumn(),
    ) as progress:
        progress.add_task("[yellow]Transcribing...", total=None)

        outputs = pipe(
            file_name,
            chunk_length_s=30,
            batch_size=32,
            generate_kwargs={"task": "transcribe", "language": "None"},
            return_timestamps=ts,
        )

    # Save the transcription to the specified path
    with open(transcript_path, 'w') as file:
        json.dump(transcription, file)

    return transcription

def main(page):
    # GUI elements
    file_name = TextField(label="Path or URL to the audio file", width=300)
    transcript_path = TextField(label="Transcript Path (optional, default 'output.json')", width=300)
    model_name = TextField(label="Model Name (optional, default 'openai/whisper-large-v3')", width=300)
    progress_bar = ProgressBar()  # Add a progress bar
    output_text = Text("")
    
    def update_progress_bar(progress):
        progress_bar.value = progress
        page.update()

    def transcribe_click(e):
        print('Transcribe button clicked')
        try:
            print('Running transcription...')
            threading.Thread(target=lambda: run_transcription(page, file_name, transcript_path, model_name, output_text, update_progress_bar)).start()
        except Exception as ex:
            output_text.value = f"Error: {str(ex)}"
        page.update()

    def run_transcription(page, file_name, device_id, transcript_path, model_name, output_text, update_progress):
        try:
            print('Transcribe_audio started')
            transcription = transcribe_audio(file_name.value, transcript_path.value, model_name.value)
            print('Transcription completed')
            output_text.value = transcription
        except Exception as ex:
            output_text.value = f"Transcription error: {str(ex)}"
        page.update()

    transcribe_btn = ElevatedButton("Transcribe", on_click=transcribe_click)

    # Layout
    page.add(
        Column([
            file_name,
            transcript_path,
            model_name,
            transcribe_btn,
            progress_bar,
            output_text
        ])
    )

# Running the Flet app
flet.app(target=main)