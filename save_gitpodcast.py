import requests

cookies = {
    'ext_name': 'ojplmecpdpgccookcobabopnaifgidhf',
    '__client_uat': '1737096105',
    '__client_uat_HKZXdSy7': '1737096105',
    '__session_HKZXdSy7': 'eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yclhReGl4MWQ4cFRlQVFaRWRaMTZEZnE4b3giLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL3d3dy5naXRwb2RjYXN0LmNvbSIsImV4cCI6MTczNzU0ODYxOSwiZnZhIjpbNzU0MCwtMV0sImlhdCI6MTczNzU0ODU1OSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5naXRwb2RjYXN0LmNvbSIsIm5iZiI6MTczNzU0ODU0OSwic2lkIjoic2Vzc18ycmtITWUwYmhJWmNCZVFVNnBQUE40QTF2aGQiLCJzdWIiOiJ1c2VyXzJyWGNNUnI0d0h1SEEybTVKY2pPcER3azFyYiJ9.SJGj4enzk3a3Q2semgb44ZPh4pLAyoang3PBWWpc7-qrF-OzXnc2BwTZwXcDryTWmEEia0xJTK0_WnAipTe2I7mZwXCOwXYBUQ-hSpjms8SFKv4YNDihritaR9T_VzkxmQl1vHVl7xZHtHJ58QLJaY-ujlSzzEOnJSHIUaoAMnuic44PGYglNhPI-hffvZ-quc81-D34r8dunweeF6681_qOuTf0tMkI_ZHCGoc9AhN3czkGVBDljHJrWfuxIV2_G30GD8gOdNHb0gPbSIR8WTtmkmFeb_2QTq3A7AnyaUNSf71p3bTFG_ev_L55jgcJX1IxhDSg_XGL2dF8yDRD6g',
    '__session': 'eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yclhReGl4MWQ4cFRlQVFaRWRaMTZEZnE4b3giLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL3d3dy5naXRwb2RjYXN0LmNvbSIsImV4cCI6MTczNzU0ODYxOSwiZnZhIjpbNzU0MCwtMV0sImlhdCI6MTczNzU0ODU1OSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5naXRwb2RjYXN0LmNvbSIsIm5iZiI6MTczNzU0ODU0OSwic2lkIjoic2Vzc18ycmtITWUwYmhJWmNCZVFVNnBQUE40QTF2aGQiLCJzdWIiOiJ1c2VyXzJyWGNNUnI0d0h1SEEybTVKY2pPcER3azFyYiJ9.SJGj4enzk3a3Q2semgb44ZPh4pLAyoang3PBWWpc7-qrF-OzXnc2BwTZwXcDryTWmEEia0xJTK0_WnAipTe2I7mZwXCOwXYBUQ-hSpjms8SFKv4YNDihritaR9T_VzkxmQl1vHVl7xZHtHJ58QLJaY-ujlSzzEOnJSHIUaoAMnuic44PGYglNhPI-hffvZ-quc81-D34r8dunweeF6681_qOuTf0tMkI_ZHCGoc9AhN3czkGVBDljHJrWfuxIV2_G30GD8gOdNHb0gPbSIR8WTtmkmFeb_2QTq3A7AnyaUNSf71p3bTFG_ev_L55jgcJX1IxhDSg_XGL2dF8yDRD6g',
    'ph_phc_Eq8LTXO71B8nu3NLW4zJOAszbKppr8kcCZ0TvqLisOK_posthog': '%7B%22distinct_id%22%3A%220194270f-503f-7a51-a195-93a1456a55bd%22%2C%22%24sesid%22%3A%5B1737548568184%2C%2201948dd7-0f2e-7417-a052-606b3264957d%22%2C1737546469166%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fwww.gitpodcast.com%2FBandarLabs%2Fclickclickclick%22%7D%7D',
}

headers = {
    'accept': 'text/x-component',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    # 'cookie': 'ext_name=ojplmecpdpgccookcobabopnaifgidhf; __client_uat=1737096105; __client_uat_HKZXdSy7=1737096105; __session_HKZXdSy7=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yclhReGl4MWQ4cFRlQVFaRWRaMTZEZnE4b3giLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL3d3dy5naXRwb2RjYXN0LmNvbSIsImV4cCI6MTczNzU0ODYxOSwiZnZhIjpbNzU0MCwtMV0sImlhdCI6MTczNzU0ODU1OSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5naXRwb2RjYXN0LmNvbSIsIm5iZiI6MTczNzU0ODU0OSwic2lkIjoic2Vzc18ycmtITWUwYmhJWmNCZVFVNnBQUE40QTF2aGQiLCJzdWIiOiJ1c2VyXzJyWGNNUnI0d0h1SEEybTVKY2pPcER3azFyYiJ9.SJGj4enzk3a3Q2semgb44ZPh4pLAyoang3PBWWpc7-qrF-OzXnc2BwTZwXcDryTWmEEia0xJTK0_WnAipTe2I7mZwXCOwXYBUQ-hSpjms8SFKv4YNDihritaR9T_VzkxmQl1vHVl7xZHtHJ58QLJaY-ujlSzzEOnJSHIUaoAMnuic44PGYglNhPI-hffvZ-quc81-D34r8dunweeF6681_qOuTf0tMkI_ZHCGoc9AhN3czkGVBDljHJrWfuxIV2_G30GD8gOdNHb0gPbSIR8WTtmkmFeb_2QTq3A7AnyaUNSf71p3bTFG_ev_L55jgcJX1IxhDSg_XGL2dF8yDRD6g; __session=eyJhbGciOiJSUzI1NiIsImNhdCI6ImNsX0I3ZDRQRDExMUFBQSIsImtpZCI6Imluc18yclhReGl4MWQ4cFRlQVFaRWRaMTZEZnE4b3giLCJ0eXAiOiJKV1QifQ.eyJhenAiOiJodHRwczovL3d3dy5naXRwb2RjYXN0LmNvbSIsImV4cCI6MTczNzU0ODYxOSwiZnZhIjpbNzU0MCwtMV0sImlhdCI6MTczNzU0ODU1OSwiaXNzIjoiaHR0cHM6Ly9jbGVyay5naXRwb2RjYXN0LmNvbSIsIm5iZiI6MTczNzU0ODU0OSwic2lkIjoic2Vzc18ycmtITWUwYmhJWmNCZVFVNnBQUE40QTF2aGQiLCJzdWIiOiJ1c2VyXzJyWGNNUnI0d0h1SEEybTVKY2pPcER3azFyYiJ9.SJGj4enzk3a3Q2semgb44ZPh4pLAyoang3PBWWpc7-qrF-OzXnc2BwTZwXcDryTWmEEia0xJTK0_WnAipTe2I7mZwXCOwXYBUQ-hSpjms8SFKv4YNDihritaR9T_VzkxmQl1vHVl7xZHtHJ58QLJaY-ujlSzzEOnJSHIUaoAMnuic44PGYglNhPI-hffvZ-quc81-D34r8dunweeF6681_qOuTf0tMkI_ZHCGoc9AhN3czkGVBDljHJrWfuxIV2_G30GD8gOdNHb0gPbSIR8WTtmkmFeb_2QTq3A7AnyaUNSf71p3bTFG_ev_L55jgcJX1IxhDSg_XGL2dF8yDRD6g; ph_phc_Eq8LTXO71B8nu3NLW4zJOAszbKppr8kcCZ0TvqLisOK_posthog=%7B%22distinct_id%22%3A%220194270f-503f-7a51-a195-93a1456a55bd%22%2C%22%24sesid%22%3A%5B1737548568184%2C%2201948dd7-0f2e-7417-a052-606b3264957d%22%2C1737546469166%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fwww.gitpodcast.com%2FBandarLabs%2Fclickclickclick%22%7D%7D',
    'dnt': '1',
    'next-action': '6005f0443974b42a223d4d9b6369cda0e730fa48df',
    'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%5B%22username%22%2C%22FallibleInc%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%5B%22repo%22%2C%22security-guide-for-developers%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2FFallibleInc%2Fsecurity-guide-for-developers%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
    'origin': 'https://www.gitpodcast.com',
    'priority': 'u=1, i',
    'referer': 'https://www.gitpodcast.com/FallibleInc/security-guide-for-developers',
    'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

data = '["FallibleInc","security-guide-for-developers|short"]'

response = requests.post(
    'https://www.gitpodcast.com/FallibleInc/security-guide-for-developers',
    cookies=cookies,
    headers=headers,
    data=data,
)