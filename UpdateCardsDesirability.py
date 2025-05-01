import json
import sys
import os

def update_desirability_values(old_json_path, new_json_path, output_path=None):
    """
    Copy card_desirability values from old JSON database to new JSON database.
    
    Args:
        old_json_path: Path to the old JSON database file
        new_json_path: Path to the new JSON database file
        output_path: Path where to save the updated JSON (defaults to overwriting new_json_path)
    
    Returns:
        tuple: (updated_count, not_found_count, total_old_cards)
    """
    # Set default output path if not provided
    if output_path is None:
        output_path = new_json_path
    
    # Load the JSON files
    with open(old_json_path, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    with open(new_json_path, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
    
    updated_count = 0
    not_found = []
    
    # For each card in the old database
    for card_key, card_data in old_data.items():
        # Get the desirability value from the old database
        old_desirability = card_data.get('card_desirability', 0)
        
        # Skip if the desirability is 0 (default value)
        if old_desirability == 0:
            continue
        
        # Try to find the same card in the new database
        if card_key in new_data:
            # Update the desirability value in the new database
            new_data[card_key]['card_desirability'] = old_desirability
            updated_count += 1
        else:
            # Keep track of cards that weren't found
            not_found.append({
                'key': card_key,
                'name': card_data.get('card_name', 'Unknown'),
                'desirability': old_desirability
            })
    
    # Save the updated new database
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    
    return updated_count, len(not_found), len(old_data)

def main():
    if len(sys.argv) < 3:
        print("Usage: python update_desirability.py <old_json_path> <new_json_path> [output_path]")
        print("  If output_path is not provided, the script will overwrite the new_json_path")
        sys.exit(1)
    
    old_json_path = sys.argv[1]
    new_json_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.isfile(old_json_path):
        print(f"Error: Old JSON file not found: {old_json_path}")
        sys.exit(1)
    
    if not os.path.isfile(new_json_path):
        print(f"Error: New JSON file not found: {new_json_path}")
        sys.exit(1)
    
    print(f"Updating desirability values from {old_json_path} to {new_json_path}")
    updated_count, not_found_count, total_old = update_desirability_values(
        old_json_path, new_json_path, output_path
    )
    
    print(f"\nSummary:")
    print(f"  Total cards in old database: {total_old}")
    print(f"  Cards with desirability updated: {updated_count}")
    print(f"  Cards not found in new database: {not_found_count}")
    
    if not_found_count > 0:
        print("\nWarning: Some cards from the old database were not found in the new database.")
        print("The desirability values for these cards could not be transferred.")
        print("These may be cards that have been removed or renamed.")
    
    output_display = output_path if output_path else new_json_path
    print(f"\nUpdated database saved to: {output_display}")

if __name__ == "__main__":
    main() 