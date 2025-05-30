"""
Pokemon TCG Card Database Configuration
Created by SquallTCGP

This configuration file contains the necessary mappings and settings for the Pokemon TCG
card database generator. It defines the relationships between set names, expansion IDs,
pack configurations, and card rarities.

Configuration Components:

1. PACK_CONFIGS:
   Defines the pack structure for main sets that have multiple packs.
   Each pack configuration includes:
   - expansion_id: The ID used in URLs and card data
   - packs: Mapping of pack URLs to their suffix identifiers
   Note: This configuration is regularly updated as new main sets are added to the game.

2. SET_NAME_TO_EXPANSION_ID:
   Maps full set names to their corresponding expansion IDs used in URLs
   and card data. This mapping is continuously updated to include new sets
   and mini-sets as they are released.

3. RARITY_MAP:
   Defines the numerical values for different card rarities, used for
   determining card obtainability and sorting.

4. CURRENT_SET:
   Identifies the newest set whose cards cannot be traded until a new set is released.
"""

# Current newest set (cards from this set cannot be traded)
CURRENT_SET = "Extradimensional Crisis"

# Pack configurations for main sets
PACK_CONFIGS = {
    "Genetic Apex": {
        "expansion_id": "a1",
        "packs": {
            "charizard-pack": "C",  # Cards exclusive to Charizard pack get GAC suffix
            "mewtwo-pack": "M",     # Cards exclusive to Mewtwo pack get GAM suffix
            "pikachu-pack": "P"     # Cards exclusive to Pikachu pack get GAP suffix
        }
    },
    "Space-Time Smackdown": {
        "expansion_id": "a2",
        "packs": {
            "dialga-pack": "D",     # Cards exclusive to Dialga pack get STSD suffix
            "palkia-pack": "P"      # Cards exclusive to Palkia pack get STSP suffix
        }
    },
    "Celestial Guardians": {
        "expansion_id": "a3",
        "packs": {
            "celestial-guardians-lunala": "L",     # Cards exclusive to Lunala pack get CGL suffix
            "celestial-guardians-solgaleo": "S"      # Cards exclusive to Solgaleo pack get CGS suffix
        }
    }

}

# All supported sets
SET_NAME_TO_EXPANSION_ID = {
    "Genetic Apex": "a1",
    "Mythical Island": "a1a",
    "Space-Time Smackdown": "a2",
    "Triumphant Light": "a2a",
    "Shining Revelry": "a2b",
    "Celestial Guardians": "a3",
    "Extradimensional Crisis": "a3a"
}

# Rarity Mapping
RARITY_MAP = {
    "C": 1,      # Normal / 1 Diamonds
    "U": 2,      # Normal / 2 Diamonds
    "R": 3,      # Normal / 3 Diamonds
    "RR": 4,     # EX / 4 Diamonds
    "AR": 5,     # 1 Star
    "SR": 6,     # 2 Star
    "SAR": 7,    # Rainbow 2 Star
    "IM": 8,     # Immersive / 3 Star
    "UR": 9,     # Crown Rare
    "S": 10,     # Shiny
    "SSR": 11,   # Double Shiny
    "IR": 12,    # Immersive / Triple Shiny
} 