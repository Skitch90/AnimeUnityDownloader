import asyncio
import json
import re
import sys

import requests

from anime_downloader import process_anime_download, parse_episodes_list
from src.general_utils import fetch_page_and_headers, clear_terminal

animeunity_base="https://animeunity.cx"

def search_anime(query):
    page, headers, cookies = fetch_page_and_headers(f"{animeunity_base}/").values()
    csrf_token = page.find("meta", attrs={"name": "csrf-token"})["content"]
    xsrf_token = cookies['XSRF-TOKEN']

    url = f"{animeunity_base}/livesearch"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': 'application/json, text/plain, */*',
        'X-CSRF-TOKEN': csrf_token,
        'Content-Type': 'application/json;charset=utf-8',
        'X-XSRF-TOKEN': xsrf_token,
    }

    data = json.dumps({"title":query})
    response = requests.post(url, headers=headers, data=data, cookies=cookies)

    return [
        {"id": item["id"], "title_eng": item['title_eng'], "real_episodes_count": item['real_episodes_count'], "slug": item['slug']}
        for item in response.json()['records']
    ]

async def main():
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter anime title to search: ")

    if not query:
        print("Empty query. Exiting.")
        return

    print(f"Searching for '{query}'...")
    options = search_anime(query)

    if not options:
        print("No options found.")
        return

    print("\nAvailable options:")
    for i, option in enumerate(options, 1):
        title = option.get("title_eng") or option.get("title_it") or option.get("title")
        episodes = option.get("real_episodes_count", "?")
        print(f"{i}) {title} ({episodes} episodes)")

    while True:
        try:
            choice = input(f"\nChoose an option (1-{len(options)}) or 'q' to quit: ") if len(options) > 1 else "1"
            if choice.lower() == 'q':
                break

            idx = int(choice) - 1
            if 0 <= idx < len(options):
                selected = options[idx]
                selected_id = selected.get("id")
                selected_slug = selected.get("slug")
                selected_title = selected.get("title_eng") or selected.get("title_it") or selected.get("title")
                selected_episodes = selected.get("real_episodes_count", "?")
                clear_terminal()
                print(f"Selected {selected_title} - {selected_episodes} episodes ({selected_id}-{selected_slug})")
                episodes_input = input("Enter episodes number/s [last], a for all or q to quit: ") or str(selected['real_episodes_count'])
                if episodes_input.lower() == 'q':
                    break
                await process_anime_download(
                    url=f"{animeunity_base}/anime/{selected_id}-{selected_slug}",
                    episodes=list(range(1,selected_episodes+1)) if episodes_input.lower() == 'a' else parse_episodes_list(re.split(r"[ ,]", episodes_input), int(selected_episodes)),
                    custom_path='/mnt/Data'
                )
                break
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    asyncio.run(main())
