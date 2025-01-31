# CVEingest - Prompt Friendly CVEs

Using this tool, you can gather and convert CVEs published by `GitHub advisories` and `cve.org` using one user interface. The tool takes care of fetching the references referenced by the CVEs. So, if some details like code changes are in some reference, it will be fetched.


### 🚀 Features
* You can download the CVEs Json with all the references crawled.
* You can download the SSML to feed into your speech generator service.



### 📦 How to launch the tool

```bash
export GITHUB_TOKEN=

export GEMINI_API_KEY=

#optional for podcast
export SPEECH_REGION=
export SPEECH_KEY=F76..

```



```bash
pip install -r requirements.txt
python main.py
```
![image](https://github.com/user-attachments/assets/94750d92-2dc2-4b25-9a08-ba8a590ae728)


### 💡 How to use

* Enter the date range for the CVEs published (or choose one from examples).
* Keep the range at most 3 days.
* Set the SSML prompt from the example.
* Click on Process Advisories



### Processed Output Json + Podcast



![image](https://github.com/user-attachments/assets/4844f000-ff99-4e56-8399-a7ba93f976d0)





💡 You can use the download JSON in notebookLM directly and it will generate a nice podcast.
