import os
import uuid

from openai import AzureOpenAI
import azure.cognitiveservices.speech as speechsdk
from django.conf import settings

speech_key, service_region = os.getenv("AZURE_SPEECH_KEY"), os.getenv("AZURE_SPEECH_REGION")


def get_openai_response(prompt: str) -> str:

    client = AzureOpenAI(
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="jpchat35",  # your deployment name
        messages=[{"role": "system", "content": "你是一個童話故事作家，請幫我根據user的動物與場景，來編一個童話故事。"},
                    {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

    return completion.choices[0].message.content


def send_to_tts(story: str):
    speech_config = speechsdk.SpeechConfig(subscription=speech_key,
                                           region=service_region)
    speech_config.speech_synthesis_voice_name = "zh-TW-YunJheNeural"
    speech_config.speech_synthesis_language = "zh-TW"
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3)

    audio_filename = uuid.uuid4().hex + ".mp4"
    static_path = os.path.join(settings.MEDIA_ROOT, audio_filename)

    audio_config = speechsdk.AudioConfig(filename=static_path)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(story).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return f"{settings.MEDIA_URL}{audio_filename}"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
