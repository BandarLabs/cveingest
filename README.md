# CVEingest - Prompt Friendly CVEs

Using this tool, you can gather and convert CVEs published by `GitHub advisories` and `cve.org` using one user interface. The tool takes care of fetching the references referenced by the CVEs. So, if some details like code changes are in some reference, it will be fetched.

<details>
<summary>Sample JSON Output</summary>

```json
[
  {
    "ghsa_id": "GHSA-66fj-74pq-7rwx",
    "cve_id": "CVE-2024-56829",
    "url": "https://api.github.com/advisories/GHSA-66fj-74pq-7rwx",
    "html_url": "",
    "summary": "",
    "description": "Huang Yaoshi Pharmaceutical Management Software through 16.0 allows arbitrary file upload via a .asp filename in the fileName element of the UploadFile element in a SOAP request to /XSDService.asmx.",
    "severity": "critical",
    "published_at": "2025-01-02T06:30:47Z",
    "updated_at": "2025-01-02T06:30:52Z",
    "source_code": "",
    "cvss_score": 10,
    "vulnerabilities": [],
    "references": [
      {
        "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-56829",
        "type": "NIST",
        "status_code": 200,
        "info": "Huang Yaoshi Pharmaceutical Management Software through 16.0 allows arbitrary file upload via a .asp filename in the fileName element of the UploadFile element in a SOAP request to /XSDService.asmx."
      }
    ],
    "assigner_name": ""
  }
]
```

</details>

### 🚀 Features
* You can download the CVEs Json with all the references crawled.
* You can download the SSML to feed into your speech generator service.



### 📦 How to launch the tool

```bash
export GITHUB_TOKEN=

# optional for ssml
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
