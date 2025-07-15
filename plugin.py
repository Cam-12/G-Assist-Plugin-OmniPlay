import json
import sys
import requests
import logging
import os
from ctypes import byref, windll, wintypes
from typing import Optional, Dict, Any
import requests
import urllib.parse
from bs4 import BeautifulSoup

Response = Dict[bool, Optional[str]]

LOG_FILE = os.path.join(os.environ.get('USERPROFILE', '.'), 'omniplay-plugin.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

NOTES_DIR = os.path.join(os.environ.get("USERPROFILE", "."), "GAssistNotes")
os.makedirs(NOTES_DIR, exist_ok=True)

def save_game_note(params: dict = None) -> dict:
    if not params or "game" not in params:
        logging.error("Game parameter is required in save_game_note")
        return {"success": False, "message": "Game parameter is required."}
    
    if not params or "note" not in params:
        logging.error("Note parameter is required in save_game_note")
        return {"success": False, "message": "Note parameter is required."}

    game = params["game"]
    note = params["note"]

    note_file = os.path.join(NOTES_DIR, f"{game}.txt")
    try:
        with open(note_file, "a", encoding="utf-8") as f:
            f.write(note + "\n")
            logging.info(f"Note recorded for game: {game}")
            return {
                "success": True,
                "message": "Note created"
            }
    except Exception as e:
        logging.error(f"Note recording failed: {str(e)}")
        return {"success": False, "message": f"An unexpected error occurred: {str(e)}"}
    
def search_fandom(game: str, topic: str) -> Optional[str]:
    guessed = f"https://{game.replace(' ', '').lower()}.fandom.com/api.php"
    try:
        r = requests.get(guessed, params={
            "action": "query", "format": "json",
            "prop": "extracts", "exintro": True, "explaintext": True,
            "titles": topic
        }, timeout=5)
        if r.status_code == 200:
            pages = r.json().get("query", {}).get("pages", {})
            for page in pages.values():
                extract = page.get("extract")
                if extract and len(extract.strip()) > 0:
                    return extract
    except Exception as e:
        logging.error(f"[Fandom] Error: {e}")
    return None

def search_mediawiki(game: str, topic: str) -> Optional[str]:
    domain = f"{game.replace(' ', '').lower()}.wiki.gg"
    api = f"https://{domain}/api.php"
    try:
        r = requests.get(api, params={
            "action": "query", "list": "search",
            "srsearch": topic, "format": "json", "srlimit": 3
        }, timeout=10)
        r.raise_for_status()
        sr = r.json().get("query", {}).get("search", [])
        if not sr:
            return None
        title = sr[0]["title"]
        page = requests.get(f"https://{domain}/wiki/{urllib.parse.quote(title)}", timeout=10)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, "lxml")
        for p in soup.select("div.mw-parser-output > p"):
            txt = p.get_text(separator=" ", strip=True)
            if txt and len(txt) > 50 and "cookie" not in txt.lower():
                return txt
    except Exception as e:
        logging.error(f"MediaWiki search error: {e}")
    return None


def fallback_scrape(game: str, topic: str) -> str:
    info = search_mediawiki(game, topic)
    if info:
        return info

    query = f"site:wiki.gg {game} {topic}"
    try:
        r = requests.get("https://html.duckduckgo.com/html/",
                         params={"q": query}, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.select("a.result__a"):
            href = a.get("href")
            if href and "wiki.gg" in href:
                page = requests.get(href, timeout=10)
                page.raise_for_status()
                sp = BeautifulSoup(page.text, "lxml")
                for p in sp.select("div.mw-parser-output > p"):
                    txt = p.get_text(separator=" ", strip=True)
                    if txt and len(txt) > 50 and "cookie" not in txt.lower():
                        return txt
    except Exception as e:
        logging.error(f"DuckDuckGo fallback error: {e}")

    return "Aucune information trouvée."


def search_fallback(game: str, topic: str) -> str:
    info = search_fandom(game, topic)
    if info:
        return info
    info = fallback_scrape(game, topic)
    return info or "Aucune information trouvée."
    
def query_character_info(params: dict = None, messages=None, system_info=None) -> Response:
    try:
        if not params:
            return {"success": False, "message": "Missing parameters."}
        game = params.get("game")
        topic = params.get("character")
        if not game or not topic:
            return {"success": False, "message": "Missing 'game' or 'character'."}
        
        info = search_fallback(game, topic)
        return {"success": True, "message": f"[OmniPlay] {info}"}
    except Exception as e:
        logging.error(f"Exception in query_character_info: {e}")
        return {"success": False, "message": f"Failed to retrieve information"}

def main():
    INITIALIZE_COMMAND = 'initialize'
    SHUTDOWN_COMMAND = 'shutdown'
    SAVE_GAME_NOTE = 'save_game_note'
    QUERY_CHARACTER_INFO = 'query_character_info'

    commands = {
        'initialize': lambda _: {"success": True, "message": "Plugin initialized"},
        'shutdown': lambda _: {"success": True, "message": "Plugin shutdown"},
        'save_game_note': save_game_note,
        'query_character_info': query_character_info
    }
    
    while True:
        command = read_command()
        if command is None:
            logging.error('Error reading command')
            continue
        
        tool_calls = command.get("tool_calls", [])
        for tool_call in tool_calls:
            logging.info(f"Tool call: {tool_call}")
            func = tool_call.get("func")
            logging.info(f"Function: {func}")
            params = tool_call.get("params", {})
            logging.info(f"Params: {params}")
            
            if func == INITIALIZE_COMMAND:
                response = commands.get(INITIALIZE_COMMAND, lambda _: {"success": False, "message": "Unknown command"})()
            elif func == SAVE_GAME_NOTE:
                logging.info(f"Getting note info for {params}")
                response = save_game_note(params)
                logging.info(f"Note info: {response}")
            elif func == "query_character_info":
                logging.info(f"Querying character info with: {params}")
                response = query_character_info(params)
            elif func == SHUTDOWN_COMMAND:
                response = commands.get(SHUTDOWN_COMMAND, lambda _: {"success": False, "message": "Unknown command"})()
                write_response(response)
                return
            else:
                response = {'success': False, 'message': "Unknown function call"}
            
            write_response(response)
    
def read_command() -> dict | None:
    try:
        STD_INPUT_HANDLE = -10
        pipe = windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)

        chunks = []
        while True:
            BUFFER_SIZE = 4096
            message_bytes = wintypes.DWORD()
            buffer = bytes(BUFFER_SIZE)
            success = windll.kernel32.ReadFile(
                pipe,
                buffer,
                BUFFER_SIZE,
                byref(message_bytes),
                None
            )

            if not success:
                logging.error('Error reading from command pipe')
                return None
            
            chunk = buffer.decode('utf-8')[:message_bytes.value]
            chunks.append(chunk)

            if message_bytes.value < BUFFER_SIZE:
                break

        retval = ''.join(chunks)
        return json.loads(retval)

    except json.JSONDecodeError:
        logging.error(f'Received invalid JSON: {retval}')
        return None
    except Exception as e:
        logging.error(f'Exception in read_command(): {str(e)}')
        return None


def write_response(response:Response) -> None:
    try:
        STD_OUTPUT_HANDLE = -11
        pipe = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        json_message = json.dumps(response) + '<<END>>'
        message_bytes = json_message.encode('utf-8')
        message_len = len(message_bytes)

        bytes_written = wintypes.DWORD()
        success = windll.kernel32.WriteFile(
            pipe,
            message_bytes,
            message_len,
            bytes_written,
            None
        )

        if not success:
            logging.error('Error writing to response pipe')

    except Exception as e:
        logging.error(f'Exception in write_response(): {str(e)}')


if __name__ == '__main__':
    main()