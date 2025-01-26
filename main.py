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

import json
import tempfile
from gemini_service import GeminiService


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

# To run the app, use the command:
# uvicorn your_script_name:app --reload


# if __name__ == "__main__":
#     TOKEN = os.environ.get("GITHUB_TOKEN")
#     start_date = '2025-01-15'
#     end_date = '2025-01-16'

#     results = []
#     with ThreadPoolExecutor(max_workers=4) as executor:
#         futures = {
#             executor.submit(process_day, start, end, 'github', TOKEN): (start, end)
#             for start, end in generate_date_ranges(start_date, end_date)
#         }

#         for future in as_completed(futures):
#             start, end = futures[future]
#             try:
#                 results.extend(future.result())
#                 print(f"Completed processing for date range {start} to {end}")
#             except Exception as e:
#                 print(f"Error processing date range {start} to {end}: {e}")

#     with open("critical_advisories_with_references.json", "w") as f:
#         json.dump(results, f, indent=4)

#     print(f"Processed and saved {len(results)} critical advisories with detailed references.")
import os
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import gradio as gr

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
                    ["Write a comprehensive report on new cybersecurity threats. Make it very detailed, use code examples whenever possible."]
                ],
                inputs=[ssml_prompt_input]
            )

        with gr.Column():
            json_output = gr.JSON(label="Raw JSON Format")
            status_output = gr.Textbox(label="Processing Status")
            length_output = gr.Textbox(label="Article Format", interactive=False)
            download_json_button = gr.Button("Download JSON")
            download_length_button = gr.Button("Download Article Format")
            external_link = gr.HTML("<a href='https://notebooklm.google.com' target='_blank'>Go to NotebookLM</a>")

    process_button.click(
        fn=process_dates,
        inputs=[start_date_input, end_date_input, token_input],
        outputs=[json_output, status_output],
    ).then(
        fn=generate_ssml_from_json,
        inputs=[json_output, ssml_prompt_input],
        outputs=length_output
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
        inputs=[length_output],
        outputs=[]
    )

demo.launch(auth=('hacker', 'news'), server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))