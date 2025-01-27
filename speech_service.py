from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from gemini_service import GeminiService
import os
import re
import textwrap
import xml.etree.ElementTree as ET
import time
import requests
import uuid
import zipfile
from io import BytesIO

load_dotenv()

gemini_service = GeminiService()

class MemoryStreamCallback(speechsdk.audio.PushAudioOutputStreamCallback):
    def __init__(self):
        super().__init__()
        self._audio_data = bytes()

    def write(self, audio_buffer: memoryview) -> int:
        self._audio_data += bytes(audio_buffer)
        return audio_buffer.nbytes

    def close(self):
        pass

    def get_audio_data(self) -> bytes:
        return self._audio_data


class SpeechService:
    def __init__(self):
        # Load environment variables
        self.speech_key = os.environ.get("SPEECH_KEY")
        self.speech_region = os.environ.get("SPEECH_REGION")

    # def text_to_mp3(self, ssml_string: str) -> bytes | None:
    #     """
    #     Converts a string to an mp3 bytes object using Azure Text to Speech

    #     Args:
    #         ssml_string (str): Text to be converted to speech

    #     Returns:
    #         bytes | None: Returns mp3 bytes object, None if error
    #     """

    #     MAX_RETRIES = 3
    #     RETRY_DELAY = 2

    #     if not self.speech_key or not self.speech_region:
    #         return None
    #     print(self.speech_key, ssml_string)

    #     # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    #     speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    #     print("s1")
    #     # The neural multilingual voice can speak different languages based on the input text.
    #     speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'

    #     speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    #     for attempt in range(MAX_RETRIES):
    #         try:
    #             # Creates a memory stream as the audio output stream instead of a file.
    #             stream_callback = MemoryStreamCallback()
    #             audio_stream = speechsdk.audio.AudioOutputConfig(stream=speechsdk.audio.PushAudioOutputStream(stream_callback))

    #             speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_stream)

    #             result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    #             if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #                 return stream_callback.get_audio_data()
    #             elif result.reason == speechsdk.ResultReason.Canceled:
    #                 cancellation_details = result.cancellation_details
    #                 print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #                 if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #                     print("Error details: {}".format(cancellation_details.error_details))
    #                 if attempt < MAX_RETRIES - 1:
    #                     print("Retrying... (attempt {}/{})".format(attempt + 1, MAX_RETRIES))
    #                     time.sleep(RETRY_DELAY)
    #                 else:
    #                     return b""
    #         except Exception as e:
    #             print("Exception occurred: {}".format(str(e)))
    #             if attempt < MAX_RETRIES - 1:
    #                 print("Retrying... (attempt {}/{})".format(attempt + 1, MAX_RETRIES))
    #                 time.sleep(RETRY_DELAY)
    #             else:
    #                 return b""

    def text_to_mp3(self, ssml_string: str) -> bytes | None:
        """
        Converts a string to an mp3 bytes object using Azure Text to Speech Batch Synthesis API.

        Args:
            ssml_string (str): Text to be converted to speech

        Returns:
            bytes | None: Returns mp3 bytes object, None if error
        """

        MAX_RETRIES = 3
        RETRY_DELAY = 2

        if not self.speech_key or not self.speech_region:
            return None

        synthesis_id = str(uuid.uuid4())
        put_url = f"https://{self.speech_region}.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"

        headers = {
            "Ocp-Apim-Subscription-Key": self.speech_key,
            "Content-Type": "application/json"
        }

        body = {
            "description": "my ssml test",
            "inputKind": "SSML",
            "inputs": [
                {"content": ssml_string}
            ],
            "properties": {
                "outputFormat": "riff-24khz-16bit-mono-pcm",
                "wordBoundaryEnabled": False,
                "sentenceBoundaryEnabled": False,
                "concatenateResult": False,
                "decompressOutputFiles": False
            }
        }

        for attempt in range(MAX_RETRIES):
            try:
                put_response = requests.put(put_url, headers=headers, json=body)
                put_response.raise_for_status()

                # Polling operation status
                status_url = f"https://{self.speech_region}.api.cognitive.microsoft.com/texttospeech/batchsyntheses/{synthesis_id}?api-version=2024-04-01"
                while True:
                    time.sleep(RETRY_DELAY)
                    status_response = requests.get(status_url, headers=headers)
                    status_response.raise_for_status()
                    status = status_response.json()
                    operation_status = status.get("status")

                    if operation_status == "Succeeded":
                        download_url = status["outputs"]["result"]
                        zip_response = requests.get(download_url)
                        zip_response.raise_for_status()

                        # Extract .wav file from zip
                        with zipfile.ZipFile(BytesIO(zip_response.content)) as zip_file:
                            for file_name in zip_file.namelist():
                                if file_name.endswith(".wav"):
                                    with zip_file.open(file_name) as audio_file:
                                        audio_content = audio_file.read()

                                        # # Save the file locally
                                        # with open(file_name, 'wb') as local_file:
                                        #     local_file.write(audio_content)

                                        return audio_content
                    elif operation_status == "Failed":
                        raise Exception("Batch synthesis failed")
                    elif operation_status in ["Running", "NotStarted"]:
                        continue
                    else:
                        raise Exception(f"Unexpected operation status: {operation_status}")

            except Exception as e:
                print(f"Exception occurred: {str(e)}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying... (attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(RETRY_DELAY)
                else:
                    return None

    def calculate_duration(self, text_line, wpm=135):
        words = len(text_line.split())
        minutes = words / wpm
        seconds = minutes * 60
        return seconds

    def no_of_words(self, text_lines):
        if isinstance(text_lines, str):  # If it's a single string
            return len([word for word in text_lines.split() if word])
        elif isinstance(text_lines, list):  # If it's a list of strings
            return sum(len([word for word in line.split() if word]) for line in text_lines)
        else:
            return 0

    def ssml_to_webvtt(self, ssml_content, duration_in_seconds, max_line_length=45, max_words_per_cue=30):
        # Helper function to insert line breaks at appropriate places
        def add_line_breaks(text, max_length):
            words = text.split()
            lines, current_line = [], ""
            for word in words:
                # Check if adding the next word exceeds the length limit
                if len(current_line) + len(word) + 1 > max_length:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line += (" " if current_line else "") + word
            if current_line:  # Add the remainder of the text if any
                lines.append(current_line)
            return "\n".join(lines)

        # Step 1: Extract text from SSML, remove specific tags, and empty lines
        text_content = re.sub(r'<speak[^>]*>|</speak>|<break[^>]*>', '', ssml_content)
        text_content = re.sub(r'<voice[^>]*>', '\n\n', text_content)
        text_content = re.sub(r'</voice>', '', text_content)
        text_content = re.sub(r'<emphasis[^>]*>|</emphasis>', '', text_content)
        text_lines = list(filter(None, [line.strip() for line in text_content.splitlines()]))

        # Step 2: Generate WebVTT content with sequential timestamps
        vtt_content = textwrap.dedent("""\
            WEBVTT

            """)
        cumulative_time = 0.0
        cue_index = 0
        wpm = int(self.no_of_words(text_lines) / duration_in_seconds * 60)
        print(wpm, " Words per minute")
        for i, line in enumerate(text_lines):

            # Break the line if it's too long into sub-lines based on word count
            words = line.split()
            sub_lines = []
            for j in range(0, len(words), max_words_per_cue):
                sub_line = ' '.join(words[j:j + max_words_per_cue])
                sub_lines.append(sub_line)

            # Generate VTT for each sub-line
            for sub_line in sub_lines:
                duration = self.calculate_duration(sub_line, wpm=wpm)
                start_time = cumulative_time
                end_time = start_time + duration
                cumulative_time = end_time  # Update cumulative time for next line

                # Convert seconds to VTT timestamp format (HH:MM:SS.mmm)
                def seconds_to_timestamp(seconds):
                    hours = int(seconds // 3600)
                    minutes = int((seconds % 3600) // 60)
                    seconds = seconds % 60
                    return f"{hours:02}:{minutes:02}:{seconds:06.3f}"

                formatted_sub_line = add_line_breaks(sub_line, max_line_length)
                cue_index += 1
                vtt_content += f"{cue_index}\n"
                vtt_content += f"{seconds_to_timestamp(start_time)} --> {seconds_to_timestamp(end_time)} line:5% align:center\n"
                vtt_content += f"{formatted_sub_line}\n\n"

        return vtt_content

        # Function to remove the first occurrence of the <speak> tag using regex
    def remove_first_speak_tag(self, content):
        # Regex pattern to match the <speak> tag with version and xmlns attributes
        speak_pattern = r'<speak[^>]*>'

        # Replace the first occurrence of the <speak> tag
        content_no_speak = re.sub(speak_pattern, '', content, count=1)

        # Similarly, remove the first occurrence of the closing </speak> tag
        content_no_speak = re.sub(r'</speak>', '', content_no_speak, count=1)

        return content_no_speak

    # Function to validate SSML
    def is_valid_ssml(self, ssml: str) -> bool:
        try:
            # Attempt to parse the SSML as XML
            ET.fromstring(ssml)
            return True
        except ET.ParseError:
            print(ssml)
            return False

    # Function to sanitize SSML by removing invalid break and code tags
    def sanitize_ssml(self, ssml: str) -> str:
        try:
            # Parse the input SSML
            root = ET.fromstring(ssml)

            # The namespace URI if any (extracted from the root tag)
            default_ns_uri = root.tag.split('}')[0].strip('{')

            # Remove non-<voice> children while preserving the element itself
            for child in list(root):
                # Extract the local name by splitting the namespace
                tag_name = child.tag
                tag_without_ns = tag_name.split('}')[1] if '}' in tag_name else tag_name

                if tag_without_ns != 'voice':
                    root.remove(child)

            # Declare default namespaces
            ET.register_namespace('', default_ns_uri)

            # Return the modified XML as a string
            return ET.tostring(root, encoding='unicode')
        except ET.ParseError:
            # In case of parsing errors, simply return the original SSML
            return ssml

    # Function to generate SSML with retry logic
    def generate_ssml_with_retry(self, file_paths, prompt, max_retries=3, delay=2):
        attempts = 0
        while attempts < max_retries:
            # Call the OpenAI function to generate SSML
            ssml_response = gemini_service.call_gemini_flash_for_ssml(file_paths, prompt)
            filtered_ssml_response = '\n'.join(line for line in ssml_response.split('\n') if '```' not in line)
            # Sanitize the SSML
            sanitized_ssml = self.sanitize_ssml(filtered_ssml_response)

            # Check if the sanitized SSML is valid
            if self.is_valid_ssml(sanitized_ssml):
                return sanitized_ssml

            # If not valid, increment attempts and wait before retrying
            attempts += 1

        # Optionally raise an exception or return an error if max retries reached
        raise ValueError("Failed to generate valid SSML after multiple attempts.")


if __name__ == '__main__':
    ss = SpeechService()
    ss.text_to_mp3("""<speak xmlns="http://www.w3.org/2001/10/synthesis" version="1.0" xml:lang="en-US"><voice name="en-US-AvaMultilingualNeural">
And to our listeners, that’s all for this week’s episode of “Secure Code Insights.” Stay tuned for more next week.
<break time="500ms" />
Happy coding and stay secure.
</voice>
</speak>""")