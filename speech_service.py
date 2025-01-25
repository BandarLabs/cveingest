from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
from app.services.openai_service import OpenAIService
import os
import re
import textwrap
import xml.etree.ElementTree as ET


load_dotenv()

openai_service = OpenAIService()

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

    def text_to_mp3(self, ssml_string: str) -> bytes | None:
        """
        Converts a string to an mp3 bytes object using Azure Text to Speech

        Args:
            ssml_string (str): Text to be converted to speech

        Returns:
            bytes | None: Returns mp3 bytes object, None if error
        """

        if not self.speech_key or not self.speech_region:
            return None
        print(self.speech_key, ssml_string)

        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        print("s1")
        # The neural multilingual voice can speak different languages based on the input text.
        speech_config.speech_synthesis_voice_name = 'en-US-AvaMultilingualNeural'

        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

        # # Creates a memory stream as the audio output stream instead of a file.
        # audio_config = speechsdk.audio.AudioOutputConfig(stream=speechsdk.audio.PushAudioOutputStream(speechsdk.audio.MemoryStreamCallback()), use_default_speaker=True)
        # speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Creates a memory stream as the audio output stream instead of a file.
        stream_callback = MemoryStreamCallback()
        audio_stream = speechsdk.audio.AudioOutputConfig(stream=speechsdk.audio.PushAudioOutputStream(stream_callback))

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_stream)

        result = speech_synthesizer.speak_ssml_async(ssml_string).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return stream_callback.get_audio_data()
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
            return b""

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
            ssml_response = openai_service.call_openai_for_response(file_paths, prompt)
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


