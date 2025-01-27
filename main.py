import json
import os
from github_crawler import GitHubAdvisoryCrawler
from reference_crawlers.reference_crawler_factory import ReferenceCrawlerFactory
from cve_crawler import CVECrawler
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gradio as gr

import tempfile
from gemini_service import GeminiService
from speech_service import SpeechService


def clean_advisories(advisories):
    cleaned_advisories = []
    for advisory in advisories:
        advisory_dict = advisory.to_dict()

        # Check if both 'summary' and 'description' are present
        if 'summary' in advisory_dict and 'description' in advisory_dict:
            summary_start = advisory_dict['summary'][:50]
            description_start = advisory_dict['description'][:50]

            # Update summary to an empty string if the first 50 characters match
            if summary_start == description_start:
                advisory_dict['summary'] = ''

            # remove html url as to reduce token count (repeat of url)
            advisory_dict['html_url'] = ''

        if 'references' in advisory_dict:
            # Filter references to exclude those with empty 'info'
            advisory_dict['references'] = [
                ref for ref in advisory_dict['references']
                if ref.get('info', '').strip() != ''
            ]
        cleaned_advisories.append(advisory_dict)

    # Sort advisories by 'stars' in descending order and by 'cvss_score' if 'stars' are the same
    sorted_advisories = sorted(cleaned_advisories, key=lambda x: (-x.get('stars', 0), -x.get('cvss_score', 0)))

    return sorted_advisories


# Define FastAPI app
app = FastAPI()

class AdvisoryRequest(BaseModel):
    start_date: str
    end_date: str
    source: str

def generate_date_ranges(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    current_date = start_date

    while current_date < end_date:
        yield current_date.strftime("%Y-%m-%d"), (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        current_date += timedelta(days=1)

def process_day(start_date, end_date, source, token):
    if source == 'github':
        crawler = GitHubAdvisoryCrawler(token)
    elif source == 'cve-search':
        crawler = CVECrawler()
    else:
        raise ValueError("Invalid source! Must be 'github' or 'cve-search'")

    advisories = crawler.fetch_advisories(start_date=start_date, end_date=end_date)

    # Assuming advisory object has 'references' and need processing
    for idx, advisory in enumerate(advisories, start=1):
        detailed_references = []
        for ref_idx, reference_url in enumerate(advisory.references, start=1):
            crawler = ReferenceCrawlerFactory.get_crawler(reference_url)
            detailed_references.append(crawler.fetch_reference(reference_url, advisory.cve_id))
        advisory.references = detailed_references

    return clean_advisories(advisories)

@app.post("/fetch")
def process_advisories(request: AdvisoryRequest):
    try:
        results = []
        TOKEN = os.environ.get("GITHUB_TOKEN", "")  # Use default empty string if token is not set

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(process_day, start, end, request.source, TOKEN): (start, end)
                for start, end in generate_date_ranges(request.start_date, request.end_date)
            }

            for future in as_completed(futures):
                start, end = futures[future]
                try:
                    results.extend(future.result())
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error processing date range {start} to {end}: {e}")

        return {"result": results, "message": f"Processed and found {len(results)} advisories"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


def process_dates(start_date, end_date, token=None):
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
    print("token = ", token)
    results = []
    futures_status = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(process_day, start, end, 'github', token): (start, end)
            for start, end in generate_date_ranges(start_date, end_date)
        }

        total_futures = len(futures)
        completed_futures = 0

        for future in as_completed(futures):
            start, end = futures[future]
            try:
                results.extend(future.result())
                completed_futures += 1
                status_message = f"Completed {completed_futures}/{total_futures} for date range {start} to {end}"
            except Exception as e:
                status_message = f"Error processing date range {start} to {end}: {e}"

            futures_status.append(status_message)
            yield json.dumps(results, indent=4), status_message

def generate_ssml_from_json(json_data, ssml_prompt):
    if not ssml_prompt:
        ssml_prompt = """Convert it into a podcast so that someone could listen to it and understand what's going on.
                         Make it SSML similar to this <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
                         <voice name="en-US-AvaMultilingualNeural">Welcome to Next Gen Innovators!...</voice>
                         <voice name="en-US-BrianMultilingualNeural">Thank you, Ava...</voice>"""

    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        json_string = json.dumps(json_data[0])
        temp_file.write(json_string)
        temp_file_path = temp_file.name

    gemini_service = GeminiService()
    ssml_response = gemini_service.call_gemini_flash_for_ssml([temp_file_path], ssml_prompt)

    return ssml_response


def download_file(content, filename):
    content_as_str = json.dumps(content) if isinstance(content, dict) else str(content)
    with open(filename, "w") as file:
        file.write(content_as_str)

def handle_temporary_file(json_data) -> list:
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json') as temp_file:
        temp_file.write(json.dumps(json_data))
        return [temp_file.name]


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            start_date_input = gr.Textbox(label="Start Date (YYYY-MM-DD)")
            end_date_input = gr.Textbox(label="End Date (YYYY-MM-DD)")
            token_input = gr.Textbox(label="GitHub Token (Optional)", type="password")
            ssml_prompt_input = gr.Textbox(label="SSML Prompt (Optional)", lines=10)
            process_button = gr.Button("Process")

            examples = gr.Examples(
                examples=[
                    ["Create a detailed article on this week's vulnerability. Make it very detailed, use code examples whenever possible."],
                    ["Generate a podcast script discussing the latest trends in tech. Make it very detailed, use code examples whenever possible."],
                    ["Write a comprehensive report on new cybersecurity threats. Make it very detailed, use code examples whenever possible."],
                    ["""Host name is Ava. Dont waste too much time on intro. Can you convert it into a podcast so that someone could listen to it and understand what's going on, also discuss project structure or go in detail for some files, long 8-10 min podcast is fine by me - make it a ssml similar to this: <speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang=\"en-US\">\n<voice name=\"en-US-AvaMultilingualNeural\">\nWelcome to Next Gen Innovators!  (no need to open links) ..
                        also make it a conversation between host and guest of a podcast, question answer kind. \n\n<break time=\"500ms\" />\nI'm your host, Ava, and today we’re diving into an exciting topic: how students can embark on their entrepreneurial journey right from college.\n<break time=\"700ms\" />\nJoining us is Arun Sharma, a seasoned entrepreneur with over two decades of experience and a passion for mentoring young innovators.\n<break time=\"500ms\" />\nArun, it’s a pleasure to have you here.\n</voice>\n\n<voice name=\""en-US-DustinMultilingualNeural"\">\n    Thank you, Ava.\n    <break time=\"300ms\" />\n    It’s great to be here. I’m excited to talk about how students can channel their creativity and energy into building impactful ventures.\n</voice> ..\n", Use "en-US-DustinMultilingualNeural" voice as guest (and must use en-US-AvaMultilingualNeural voice as host always but her actual name can be something else). Add little bit of fillers like umm or uh so that it feels natural (dont over do it),
                        This is this week's vulnerability list.

                        Focus on those which will be interesting to principal engineers, top security researchers - - do not address them as it though, just the context, discuss code fixes if its there. Choose the ones which will be interesting to listeners.

                        Do not read out numeric and cve numbers - they are jarring.

                        Do not add fluff like generic security gyan about importance of code review etc, those are already known to listeners, just specifics of this weeks vulnerabilities will do.. Long answers all the time makes it monotonous.
                        Make it a 20 minute long or longer podcast if possible.  Give atleast 200 voice tags for the host + Same amount of voice tags for guest. Slowly count them and re-write the ssml if its falling short and then return the ssml."""]
                ],
                inputs=[ssml_prompt_input]
            )

        with gr.Column():
            audio_output = gr.Audio(label="Generated Podcast")
            json_output = gr.JSON(label="Raw JSON Format")
            status_output = gr.Textbox(label="Processing Status")
            ssml_output = gr.Textbox(label="Article Format", interactive=False)

            download_json_button = gr.Button("Download JSON")
            download_length_button = gr.Button("Download Article Format")
            external_link = gr.HTML("<a href='https://notebooklm.google.com' target='_blank'>Go to NotebookLM</a>")
    temp_file_paths = gr.State()
    process_button.click(
        fn=process_dates,
        inputs=[start_date_input, end_date_input, token_input],
        outputs=[json_output, status_output],
    ).then(
        fn=lambda x: handle_temporary_file(x),
        inputs=[json_output],
        outputs=temp_file_paths  # output variable name
    ).then(
        fn=SpeechService().generate_ssml_with_retry,
        inputs=[temp_file_paths, ssml_prompt_input],
        outputs=ssml_output
    ).then(
        fn=SpeechService().text_to_mp3,
        inputs=[ssml_output],
        outputs=audio_output
    )

    def download_json(json_data):
        download_file(json_data, "cveRAW.txt")

    def download_article(article):
        download_file(article, "cveArticle.txt")

    download_json_button.click(
        fn=download_json,
        inputs=[json_output],
        outputs=[]
    )

    download_length_button.click(
        fn=download_article,
        inputs=[ssml_output],
        outputs=[]
    )

demo.launch(auth=('hacker', 'news'), server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))