import os, requests
from config import FOOTBALL_API_KEY, ODDS_API_KEY

def get_matches():
    # Football-data provider connection point
    # Add provider endpoint and key in Railway Variables
    if not FOOTBALL_API_KEY:
        return []
    return []

def get_odds():
    # Odds API connection point
    if not ODDS_API_KEY:
        return []
    return []
