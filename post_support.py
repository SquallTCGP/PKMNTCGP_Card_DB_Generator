#!/usr/bin/env python3
import requests
import argparse

def send_support_request(support_text, keyword_text):
    """
    Send a POST request to the Pokemon TCG Pocket support API
    
    Args:
        support_text (str): The support text to send
        keyword_text (str): The keyword text to send
    
    Returns:
        dict: The response from the API
    """
    url = "https://gift.pokemontcgpocket.com/api/gift/post-support/"
    
    # Use form data instead of JSON
    form_data = {
        "support": support_text,
        "keyword": keyword_text
    }
    
    response = requests.post(url, data=form_data)
    
    return {
        "status_code": response.status_code,
        "response": response.text
    }

def main():
    parser = argparse.ArgumentParser(description="Send a support request to Pokemon TCG Pocket")
    parser.add_argument("--support", "-s", required=True, help="The support text to send")
    parser.add_argument("--keyword", "-k", required=True, help="The keyword text to send")
    
    args = parser.parse_args()
    
    result = send_support_request(args.support, args.keyword)
    
    print(f"Status code: {result['status_code']}")
    print(f"Response: {result['response']}")

if __name__ == "__main__":
    main() 