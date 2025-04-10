# Pokemon TCG Card Database Generator

A Python-based tool for generating JSON databases of Pokemon Trading Card Game cards by processing local card images and matching them with online card data.

Created by SquallTCGP

## Features

- Processes both regular set cards and promo cards
- Supports individual set processing or all sets at once
- Handles pack-exclusive cards for main sets
- Generates organized JSON databases with card details
- Uses image matching to ensure accurate card identification
- Supports multiple card rarities and special card types

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - requests
  - beautifulsoup4
  - Pillow
  - imagehash

## Installation

1. Clone this repository:
   ```bash
   git clone [repository-url]
   ```

2. Install required packages:
   ```bash
   pip install requests beautifulsoup4 Pillow imagehash
   ```

## Directory Structure

```
.
├── ProcessCards.py    # Main processing script
├── config.py         # Configuration file
├── assets/          # Card image directory
│   ├── Genetic Apex/
│   ├── Space-Time Smackdown/
│   ├── Triumphant Light/
│   └── ...
```

## Usage

### Process a Specific Set

```bash
python ProcessCards.py --setName "Set Name"
```

Example:
```bash
python ProcessCards.py --setName "Genetic Apex"
```

### Process All Sets

```bash
python ProcessCards.py
```

## Output Files

The script generates the following JSON database files:

- For individual set processing:
  - `[SET_INITIALS]_Cards_Database.json` (e.g., `GA_Cards_Database.json`)
  - `TCGP_Promo_Cards_Database.json` (for promo cards)

- For processing all sets:
  - `Full_Cards_Database.json` (all regular cards)
  - `TCGP_Promo_Cards_Database.json` (all promo cards)

## Card Data Structure

Each card entry in the JSON database contains:

```json
{
    "card_number": "123",                  // Card number
    "card_name": "Pokemon Name",           // Name of the card
    "card_rarity": 1,                      // Rarity of the card
    "card_set": "GA",                      // Base set initials or pack-specific (e.g., GAP, STSD)
    "card_set_name": "Genetic",            // Base set name or pack name (Short)
    "card_set_base_name": "Genetic Apex",  // Base set name or pack name (Long)
    "expansion_id": "A1",                  // Capitalized expansion ID or "Promo-a"
    "card_desirability": 0,                // Desirability of the card.
    "card_tradable": false,                // If this card can be traded. Based on rarity and promo status
    "card_obtainable": true                // If this card can be obtained in Wonderpicks. Based on rarity and promo status
}
```

## Configuration

The `config.py` file contains three main configuration components:

### 1. Pack Configurations (PACK_CONFIGS)
Defines pack structures for main sets that have multiple packs:
```python
"Genetic Apex": {
    "expansion_id": "a1",
    "packs": {
        "charizard-pack": "C",  # GAC suffix
        "mewtwo-pack": "M",     # GAM suffix
        "pikachu-pack": "P"     # GAP suffix
    }
}
```

### 2. Set Name to Expansion ID Mapping
Maps full set names to their expansion IDs used in URLs and card data.

### 3. Card Rarity System

The TCG uses a diamond-based rarity system with special designations for premium cards:

| Rarity Code | Display        | Trade Status | Wonderpick Status |
|-------------|---------------|--------------|-------------------|
| C           | 1 Diamond     | Tradeable    | Available         |
| U           | 2 Diamonds    | Tradeable    | Available         |
| R           | 3 Diamonds    | Tradeable    | Available         |
| RR          | 4 Diamonds    | Tradeable    | Available         |
| AR          | ⭐            | Tradeable    | Available         |
| SR          | ⭐⭐          | Untradeable  | Available         |
| SAR         | 🌈⭐⭐        | Untradeable  | Available         |
| IM          | ⭐⭐⭐        | Untradeable  | Unavailable       |
| UR          | 👑            | Untradeable  | Unavailable       |
| S           | ✨            | Untradeable  | Unavailable       |
| SSR         | ✨✨          | Untradeable  | Unavailable       |
| IR          | ✨✨✨        | Untradeable  | Unavailable       |

### Rarity Notes
- Cards with rarity SR and above cannot be traded
- Cards with rarity IM and above will not appear in wonderpicks
- Diamond ratings (C through RR) represent standard obtainable cards
- Special ratings (AR through IR) represent premium or chase cards 

## Error Handling

The script includes robust error handling for:
- Missing or invalid image files
- Network connection issues
- Image processing errors
- Invalid card matches (distance > 10)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0), which allows you to use, modify, and share the software only for non-commercial purposes. Commercial use, including using the software to provide paid services or selling it (even if donations are involved), is not allowed under this license.

## Acknowledgments

- Pokemon TCG data sourced from pokemon-zone.com
- Created and maintained by SquallTCGP 

