import requests

url = "https://jelly.local.mdal.dk/Items/?recursive=True&SourceType=Library&searchTerm=The%20hunger%20games&ParentId=ca66a3e7bbc66972778a197eb546edbf"

payload = {}
headers = {
  'Authorization': 'MediaBrowser Token=5731b055aaa14a49826f53b950b4c75d'
}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:
    media_data = response.json()

    # Get file size from metadata
    file_size_bytes = media_data.get('Size')

    # Convert file size to human-readable format
    if file_size_bytes is not None:
        file_size_mb = file_size_bytes / (1024 * 1024)  # Convert bytes to megabytes
        print(f"File size: {file_size_mb:.2f} MB")
    else:
        print("File size information not available.")

else:
    print(f"Error: {response.status_code}")


print(response.text)


ob = response.json()
print(response.text)
film = ob['Items'][0]
print()
print(ob['Items'])
print(film['Name'])