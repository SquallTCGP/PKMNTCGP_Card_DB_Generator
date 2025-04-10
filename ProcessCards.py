"""
Pokemon TCG Card Database Generator
Created by SquallTCGP

This script processes Pokemon Trading Card Game (TCG) image files and generates JSON databases
containing card information. It supports both regular set cards and promo cards, with the ability
to process individual sets or all sets at once.

The script matches local card images with online card data from pokemon-zone.com, organizing cards
based on their sets and packs. It handles special cases like pack-exclusive cards and promo cards,
generating separate database files for different card types.

Key Features:
- Processes both regular and promo cards
- Supports individual set processing or all sets at once
- Handles pack-exclusive cards for main sets
- Generates organized JSON databases with card details
- Uses image matching to ensure accurate card identification

Usage:
    Process a specific set:
        python ProcessCards.py --setName "Set Name"
    Process all sets:
        python ProcessCards.py

Requirements:
    - Python 3.6+
    - Required packages: requests, beautifulsoup4, Pillow, imagehash
    - config.py file with proper configuration
    - Image files in the assets/[SetName] directory structure
"""

import os
import argparse
import json
import requests
from bs4 import BeautifulSoup
from PIL import Image
import imagehash
from config import PACK_CONFIGS, SET_NAME_TO_EXPANSION_ID, RARITY_MAP

# Constants
BASE_URL = "https://www.pokemon-zone.com"
SET_PATH = "/sets/{}/"
PACKS_PATH = "/sets/{}/packs/{}/"
PROMO_SET_URL = "https://www.pokemon-zone.com/sets/promo-a/"
ASSETS_BASE_PATH = "assets"

def get_pack_urls(set_name, expansion_id):
    """Get all pack URLs for a main set"""
    if set_name in PACK_CONFIGS:
        return [
            (PACKS_PATH.format(expansion_id, pack_name), pack_suffix)
            for pack_name, pack_suffix in PACK_CONFIGS[set_name]["packs"].items()
        ]
    return [(SET_PATH.format(expansion_id), "")]

def get_card_set_name(set_name, pack_url):
    """Determine the card set name based on the pack URL"""
    if set_name in PACK_CONFIGS:
        for pack_name in PACK_CONFIGS[set_name]["packs"].keys():
            if pack_name in pack_url:
                return pack_name.split('-')[0].capitalize()
    # Special handling for Space-Time Smackdown
    if set_name == "Space-Time Smackdown":
        return "Space-Time"
    # For all other sets, return just the first word
    return set_name.split()[0]

def get_card_set(set_name, pack_url, base_initials):
    """Determine the card set based on the pack URL"""
    if set_name in PACK_CONFIGS:
        for pack_name, pack_suffix in PACK_CONFIGS[set_name]["packs"].items():
            if pack_name in pack_url:
                return f"{base_initials}{pack_suffix}"
    return base_initials

def compute_image_hash(image_path):
    with Image.open(image_path) as img:
        return imagehash.average_hash(img)


def slug_to_card_name(slug):
    parts = slug.split("-")
    formatted_parts = []
    for part in parts:
        if part == "ex":
            formatted_parts.append("EX")
        else:
            formatted_parts.append(part.capitalize())
    return " ".join(formatted_parts)


def get_set_initials(set_name):
    """Get the initials for a set name with special handling for Space-Time Smackdown"""
    if set_name == "Space-Time Smackdown":
        return "STS"
    return "".join(word[0].upper() for word in set_name.split())


def get_card_rarity_from_filename(filename):
    # Extract the rarity letter from the filename
    rarity_code = filename.split("_")[5]
    return RARITY_MAP.get(rarity_code, 0)  # Default to 0 if not found


def is_promo_card(filename):
    """Check if a card is a promo card based on the '_90_' identifier in filename."""
    return '_90_' in filename


def fetch_cards_from_url(url):
    """Fetch cards from a specific URL with error handling"""
    try:
        response = requests.get(BASE_URL + url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        cards = []
        
        for a in soup.select(".card-grid__cell a"):
            href = a.get("href")
            img_tag = a.select_one("img")
            if not href or not img_tag:
                continue
            
            image_url = img_tag.get("src").split("?")[0]
            cards.append((BASE_URL + href, image_url))
        
        return cards
    except Exception as e:
        print(f"Error fetching cards from {url}: {str(e)}")
        return []


def process_set(set_name):
    image_folder = os.path.join(ASSETS_BASE_PATH, set_name)
    if not os.path.exists(image_folder):
        print(f"Folder not found: {image_folder}")
        return

    expansion_id = SET_NAME_TO_EXPANSION_ID.get(set_name)
    if not expansion_id:
        print(f"Expansion ID for {set_name} not found!")
        return

    promo_cards_json = {}
    regular_cards_json = {}
    base_initials = get_set_initials(set_name)

    # Get all pack URLs for this set
    pack_urls = get_pack_urls(set_name, expansion_id)
    
    print(f"\nProcessing {set_name}...")
    print("Fetching online cards from all packs...")
    
    # Track which cards appear in which packs
    card_pack_appearances = {}  # key: card_url, value: list of pack_urls
    all_cards = {}  # Store all card URLs and their data
    
    # First fetch regular cards from all packs
    for pack_url, _ in pack_urls:
        print(f"  Fetching from {pack_url}...")
        cards = fetch_cards_from_url(pack_url)
        
        for card_url, image_url in cards:
            if card_url not in card_pack_appearances:
                card_pack_appearances[card_url] = []
                # Store the image URL for later use
                all_cards[card_url] = image_url
            card_pack_appearances[card_url].append(pack_url)
    
    print("Computing image hashes for online cards...")
    online_cards = {}
    for full_card_url, image_url in all_cards.items():
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            # A card is pack-specific only if it appears in exactly one pack
            pack_urls_list = card_pack_appearances[full_card_url]
            is_pack_specific = len(pack_urls_list) == 1
            pack_url = pack_urls_list[0] if is_pack_specific else None
            
            online_cards[full_card_url] = {
                "image_url": image_url,
                "hash": imagehash.average_hash(Image.open(response.raw)),
                "is_promo": False,
                "pack_url": pack_url,
                "is_pack_specific": is_pack_specific
            }
        except Exception as e:
            print(f"Error processing image for {full_card_url}: {str(e)}")
            continue

    # Then fetch promo cards
    print("Fetching promo cards...")
    promo_cards = fetch_cards_from_url(PROMO_SET_URL.replace(BASE_URL, ''))
    
    for card_url, image_url in promo_cards:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            online_cards[card_url] = {
                "image_url": image_url,
                "hash": imagehash.average_hash(Image.open(response.raw)),
                "is_promo": True,
                "pack_url": PROMO_SET_URL,
                "is_pack_specific": True
            }
        except Exception as e:
            print(f"Error processing promo image for {card_url}: {str(e)}")
            continue

    # Process local images
    print("\nProcessing local images...")
    total_files = len([f for f in os.listdir(image_folder) 
                      if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))])
    processed_files = 0

    for filename in os.listdir(image_folder):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue

        processed_files += 1
        print(f"Processing file {processed_files}/{total_files}: {filename}")

        filepath = os.path.join(image_folder, filename)
        local_hash = compute_image_hash(filepath)
        is_promo = is_promo_card(filename)

        # Prepare key: strip first "c", cut at 4th underscore
        base_key = filename
        if filename.startswith("c"):
            base_key = filename[1:]
        key_parts = base_key.split("_")
        if len(key_parts) >= 4:
            json_key = "_".join(key_parts[:4])
        else:
            print(f"Skipping unrecognized format: {filename}")
            continue

        best_match_url = None
        best_distance = float("inf")

        # Only compare with cards of the same type (promo vs regular)
        for url, card_data in online_cards.items():
            if card_data["is_promo"] == is_promo:
                dist = local_hash - card_data["hash"]
                if dist < best_distance:
                    best_distance = dist
                    best_match_url = url

        if best_distance > 10:
            print(f"No close match found for {filename}")
            continue

        if best_match_url:
            print(f"Matched {filename} with {best_match_url}")

            # Extract card_number, card_name from URL
            parts = best_match_url.replace(BASE_URL + "/cards/", "").split("/")
            if len(parts) < 3:
                print(f"Invalid card URL format: {best_match_url}")
                continue

            card_number = parts[1]
            card_slug = parts[2]
            card_name = slug_to_card_name(card_slug)

            # Get the rarity from the filename
            card_rarity = get_card_rarity_from_filename(filename)

            card_data = online_cards[best_match_url]
            pack_url = card_data["pack_url"]
            
            # For promo cards, we don't need to check pack specificity
            if is_promo:
                card_set = base_initials
                card_set_name = set_name.split()[0]  # Just take the first word
            else:
                is_pack_specific = card_data["is_pack_specific"]
                card_set = get_card_set(set_name, pack_url, base_initials) if is_pack_specific else base_initials
                card_set_name = get_card_set_name(set_name, pack_url) if is_pack_specific else set_name.split()[0]  # Just take the first word
            
            card_data = {
                "card_number": card_number,
                "card_name": card_name,
                "card_rarity": card_rarity,
                "card_set": card_set,
                "card_set_name": card_set_name,
                "card_set_base_name": set_name,
                "expansion_id": "Promo-a" if is_promo else expansion_id.capitalize(),
                "card_desirability": 0,
                "card_tradable": False,
                "card_obtainable": False if is_promo else (card_rarity not in [8, 9, 10, 11, 12])
            }

            # Add to appropriate dictionary
            if is_promo:
                promo_cards_json[json_key] = card_data
            else:
                regular_cards_json[json_key] = card_data
        else:
            print(f"No match found for {filename}")

    print("\nSorting and saving results...")
    # Sort and save regular cards
    sorted_regular = None
    sorted_promo = None

    if regular_cards_json:
        sorted_regular = dict(sorted(regular_cards_json.items(),
                                   key=lambda x: int(x[1]['card_number'].replace('TL', '').replace('P', ''))))
        
        if args.setName:
            output_file = f"{get_set_initials(set_name)}_Cards_Database.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(sorted_regular, f, indent=4, ensure_ascii=False)
            print(f"Saved regular cards to {output_file}")

    # Sort and save promo cards
    if promo_cards_json:
        sorted_promo = dict(sorted(promo_cards_json.items(),
                                 key=lambda x: int(x[1]['card_number'].replace('TL', '').replace('P', ''))))
        
        if args.setName:
            output_file = "Promo_Cards_Database.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(sorted_promo, f, indent=4, ensure_ascii=False)
            print(f"Saved promo cards to {output_file}")

    return sorted_regular, sorted_promo


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setName", required=False,
                       help="Full name of the card set (e.g., 'Triumphant Light')")
    args = parser.parse_args()

    if args.setName:
        if args.setName in SET_NAME_TO_EXPANSION_ID:
            process_set(args.setName)
        else:
            print(f"Unknown set: {args.setName}")
    else:
        # Process all sets
        all_regular_cards = {}
        all_promo_cards = {}
        
        for set_name in SET_NAME_TO_EXPANSION_ID.keys():
            print(f"\nProcessing set: {set_name}")
            regular_cards, promo_cards = process_set(set_name)
            
            # Sort the individual set's cards before adding to the combined dictionary
            if regular_cards:
                sorted_regular = dict(sorted(regular_cards.items(),
                                          key=lambda x: int(x[1]['card_number'].replace('TL', '').replace('P', ''))))
                all_regular_cards.update(sorted_regular)
            if promo_cards:
                sorted_promo = dict(sorted(promo_cards.items(),
                                        key=lambda x: int(x[1]['card_number'].replace('TL', '').replace('P', ''))))
                all_promo_cards.update(sorted_promo)

        # Save combined cards
        if all_regular_cards:
            with open("Full_Cards_Database.json", "w", encoding="utf-8") as f:
                json.dump(all_regular_cards, f, indent=4, ensure_ascii=False)
            print("\nSaved all regular cards to Full_Cards_Database.json")

        if all_promo_cards:
            with open("TCGP_Promo_Cards_Database.json", "w", encoding="utf-8") as f:
                json.dump(all_promo_cards, f, indent=4, ensure_ascii=False)
            print("Saved all promo cards to TCGP_Promo_Cards_Database.json")
