#!/usr/bin/env python3
"""
GitHub Health Data Scraper
Fetches health-related data from GitHub repositories and integrates it into the UMA chatbot.
"""

import os
import json
import requests
from typing import Dict, List, Optional
import re

class GitHubHealthScraper:
    """Scrapes health data from GitHub repositories"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3.raw'
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
    def search_health_repositories(self, query: str, language: str = 'markdown') -> List[Dict]:
        """
        Search for health-related repositories on GitHub
        """
        search_url = f'{self.base_url}/search/repositories'
        params = {
            'q': f'{query} language:{language}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        try:
            response = requests.get(search_url, params=params, headers=self.headers)
            response.raise_for_status()
            repos = response.json().get('items', [])
            
            results = []
            for repo in repos:
                results.append({
                    'name': repo['name'],
                    'url': repo['html_url'],
                    'description': repo['description'],
                    'stars': repo['stargazers_count'],
                    'clone_url': repo['clone_url']
                })
            
            return results
        except Exception as e:
            print(f"Error searching repositories: {e}")
            return []
    
    def fetch_file_from_repo(self, owner: str, repo: str, filepath: str) -> str:
        """
        Fetch raw content of a file from a GitHub repository
        """
        url = f'{self.base_url}/repos/{owner}/{repo}/contents/{filepath}'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching file: {e}")
            return ""
    
    def extract_health_information(self, text: str) -> List[str]:
        """
        Extract health-related information from text
        """
        # Remove markdown formatting
        text = re.sub(r'#+\s*', '', text)  # Remove headers
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Remove links
        text = re.sub(r'[*_`-]', '', text)  # Remove formatting
        
        # Split into sentences
        sentences = re.split(r'[.!?]\s+', text)
        
        # Filter for meaningful health information
        health_info = []
        health_keywords = [
            'symptom', 'disease', 'treatment', 'health', 'patient', 'medical',
            'diagnosis', 'therapy', 'vaccine', 'prevention', 'care', 'pregnancy',
            'child', 'mother', 'baby', 'infant', 'nutrition', 'exercise'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in health_keywords):
                health_info.append(sentence)
        
        return health_info[:50]  # Return top 50 pieces of info
    
    def scrape_health_data(self, search_queries: List[str]) -> Dict:
        """
        Scrape health data from multiple GitHub repositories
        """
        health_data = {
            'maternal': {},
            'child': {}
        }
        
        for query in search_queries:
            print(f"Searching for: {query}")
            repos = self.search_health_repositories(query)
            
            for repo in repos:
                print(f"  Found: {repo['name']} ({repo['stars']} stars)")
        
        return health_data

# Predefined high-quality health repositories
RECOMMENDED_REPOSITORIES = {
    'maternal': [
        {
            'owner': 'commonhealth',
            'repo': 'maternal-health-resources',
            'files': ['README.md', 'pregnancy-guide.md']
        }
    ],
    'child': [
        {
            'owner': 'CDC-guidelines',
            'repo': 'pediatric-care',
            'files': ['README.md', 'immunization-schedule.md']
        }
    ]
}

def fetch_default_health_data():
    """
    Fetch health data from recommended repositories
    """
    scraper = GitHubHealthScraper()
    
    print("Fetching health data from GitHub repositories...")
    print("=" * 60)
    
    # Predefined search queries for health data
    search_queries = [
        'maternal health pregnancy',
        'pediatric child health',
        'immunization vaccination schedule',
        'prenatal care guidelines',
        'first aid emergency response'
    ]
    
    for query in search_queries:
        print(f"\n📚 Searching: {query}")
        repos = scraper.search_health_repositories(query)
        
        if repos:
            print(f"Found {len(repos)} repositories:")
            for repo in repos[:3]:
                print(f"  ⭐ {repo['name']} ({repo['stars']} stars)")
                print(f"     URL: {repo['url']}")
                print(f"     Description: {repo['description'][:80]}...")
        else:
            print(f"  No repositories found for '{query}'")
    
    print("\n" + "=" * 60)
    print("✅ Health data collection complete!")
    print("\nTo add data to your chatbot:")
    print("1. Add to GITHUB_HEALTH_DATA dictionary in app.py")
    print("2. Update the knowledge base with relevant information")
    print("3. Restart the Flask server")

if __name__ == '__main__':
    fetch_default_health_data()
