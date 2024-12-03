import glob
import json
import os
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote

from better_proxy import Proxy

from bot.config import settings
from bot.exceptions import MissingTelegramAPIException


def calculate_real_number(number):
    return number / 1000000000


def update_or_add_dict(list_of_dicts, key, key_value, new_data):
    """
    Updates a dictionary in a list of dictionaries if the key exists, otherwise adds a new dictionary.

    :param list_of_dicts: List of dictionaries to update or add to.
    :param key: The key to check for existence in each dictionary.
    :param key_value: The value of the key to match.
    :param new_data: The data to update or add to the dictionary.
    """
    for dictionary in list_of_dicts:
        if dictionary.get(key) == key_value and dictionary.get("upgrade_lvl") < new_data.get(
            "upgrade_lvl"
        ):
            dictionary.update(new_data)
            return
    # If the key_value is not found, add a new dictionary
    # new_dict = {key: key_value}
    # new_dict.update(new_data)
    list_of_dicts.append(new_data)


def get_session_names() -> list[str]:
    session_names = glob.glob("sessions/*.session")
    session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]

    return session_names


def check_telegram_api():
    API_ID = settings.API_ID
    API_HASH = settings.API_HASH

    if not API_ID or not API_HASH:
        raise MissingTelegramAPIException(
            "API_ID and API_HASH is missing, please check your .env file!"
        )


def get_proxies() -> list[Proxy]:
    if settings.USE_PROXY_FROM_FILE.lower() == "true":
        with open(file="bot/config/proxies.txt", encoding="utf-8-sig") as file:
            proxies = [Proxy.from_str(proxy=row.strip()).as_url for row in file]
    else:
        proxies = []
    return proxies


def convert_datetime_str_to_utc(datetime_str):
    decimal_index = datetime_str.find(".")
    if decimal_index != -1:
        # Ensure only 3 digits after the decimal point for milliseconds
        datetime_str = datetime_str[: decimal_index + 4]

    return datetime.fromisoformat(datetime_str).replace(tzinfo=timezone.utc)


def format_duration(seconds):
    message = ""
    duration_td = timedelta(seconds=seconds)
    days, day_remainder = divmod(duration_td.total_seconds(), 86400)
    hours, remainder = divmod(day_remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        message = f"{int(days)} days "

    if hours:
        message = message + f"{int(hours)} hours "

    if minutes:
        message = message + f"{int(minutes)} minute "

    if seconds:
        message = message + f"{int(seconds)} seconds"
    return message.strip()


def mapping_role_color(role):
    if role == "admin":
        role = f"[cyan]{role}[/cyan]"
    elif role == "premium":
        role = f"[magenta]{role}[/magenta]"

    return role


def decode_query_id(query_id):
    query_string = query_id
    if "tgWebAppData" in query_id:
        query_string = unquote(
            string=query_id.split("tgWebAppData=", maxsplit=1)[1].split(
                "&tgWebAppVersion", maxsplit=1
            )[0]
        )
    parameters = query_string.split("&")
    decoded_pairs = [(param.split("=")[0], unquote(param.split("=")[1])) for param in parameters]
    result = dict()
    for key, value in decoded_pairs:
        result[key] = value

    reassign(result)
    return result


def reassign(d):
    """
    check if you have a dict after using literal_eval and reassign
    """
    for k, v in d.items():
        if v[0] in {"{", "["}:
            try:
                evald = json.loads(v)
                if isinstance(evald, dict):
                    d[k] = evald
            except ValueError as err:
                pass


async def get_query_ids():
    temp_lines = []
    with open("query_ids.txt", "r") as file:
        temp_lines = file.readlines()

    lines = [line.strip() for line in temp_lines]
    return lines


def get_tele_user_obj_from_query_id(query_id):
    # formatted_query_id = unquote(string=query_id)
    query_obj = decode_query_id(query_id)
    tele_user_obj = query_obj.get("user", {})
    return tele_user_obj
