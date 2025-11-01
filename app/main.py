from app.scrape import get_first_level_links
from app.embedding import find_top_results
from app.llm import call_llm
import asyncio

base_url = "https://www.kecktm.edu.np/"
intent = "all department heads"

# Get all the links from the homepage
links = asyncio.run(get_first_level_links(base_url))

# Use embeddings to find top-k matches
top_results = find_top_results(intent, links)

# Call llm to predict the best match
final_result = call_llm(intent, top_results)

# Return the best match
print(f'{intent} may be found at {final_result}')