import os
from openai import OpenAI
from mem0 import MemoryClient
from multion.client import MultiOn

# Configuration - YOUR_API_KEY
OPENAI_API_KEY = "YOUR_API_KEY"  # Replace with your actual OpenAI API key
MULTION_API_KEY = "YOUR_API_KEY"  # Replace with your actual MultiOn API key
MEM0_API_KEY = "YOUR_API_KEY"  # Replace with your actual Mem0 API key
USER_ID = "test_travel_agent"

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize Mem0 and MultiOn
memory = MemoryClient(api_key=MEM0_API_KEY)
multion = MultiOn(api_key=MULTION_API_KEY)

# Add conversation to Mem0
conversation = [
    {"role": "user", "content": "What are the best travel destinations in the world?"},
    {
        "role": "assistant",
        "content": (
            "Could you please specify your interests or the type of travel information you are looking for? "
            "This will help me find the most relevant information for you."
        ),
    },
    {"role": "user", "content": "Sure, I want to travel to San Francisco."},
    {
        "role": "assistant",
        "content": (
            "Based on the information gathered from TripAdvisor, here are some popular attractions, activities, "
            "and travel tips for San Francisco:\n\n"
            "1. **Golden Gate Bridge**: A must-see iconic landmark.\n"
            "2. **Alcatraz Island**: Famous former prison offering tours.\n"
            "3. **Fisherman's Wharf**: Popular tourist area with shops, restaurants, and sea lions.\n"
            "4. **Chinatown**: The largest Chinatown outside of Asia.\n"
            "5. **Golden Gate Park**: Large urban park with gardens, museums, and recreational activities.\n"
            "6. **Cable Cars**: Historic streetcars offering a unique way to see the city.\n"
            "7. **Exploratorium**: Interactive science museum.\n"
            "8. **San Francisco Museum of Modern Art (SFMOMA)**: Modern and contemporary art museum.\n"
            "9. **Lombard Street**: Known for its steep, one-block section with eight hairpin turns.\n"
            "10. **Union Square**: Major shopping and cultural hub.\n\n"
            "Travel Tips:\n"
            "- **Weather**: San Francisco has a mild climate, but it can be foggy and windy. Dress in layers.\n"
            "- **Transportation**: Use public transportation like BART, Muni, and cable cars to get around.\n"
            "- **Safety**: Be aware of your surroundings, especially in crowded tourist areas.\n"
            "- **Dining**: Try local specialties like sourdough bread, seafood, and Mission-style burritos."
        ),
    },
    {"role": "user", "content": "Show me hotels around Golden Gate Bridge."},
    {
        "role": "assistant",
        "content": (
            "The search results for hotels around Golden Gate Bridge in San Francisco include:\n\n"
            "1. Hilton Hotels In San Francisco - Hotel Near Fishermans Wharf (hilton.com)\n"
            "2. The 10 Closest Hotels to Golden Gate Bridge (tripadvisor.com)\n"
            "3. Hotels near Golden Gate Bridge (expedia.com)\n"
            "4. Hotels near Golden Gate Bridge (hotels.com)\n"
            "5. Holiday Inn Express & Suites San Francisco Fishermans Wharf, an IHG Hotel $146 (1.8K) 3-star hotel Golden Gate Bridge • 3.5 mi DEAL 19% less than usual\n"
            "6. Holiday Inn San Francisco-Golden Gateway, an IHG Hotel $151 (3.5K) 3-star hotel Golden Gate Bridge • 3.7 mi Casual hotel with dining, a bar & a pool\n"
            "7. Hotel Zephyr San Francisco $159 (3.8K) 4-star hotel Golden Gate Bridge • 3.7 mi Nautical-themed lodging with bay views\n"
            "8. Lodge at the Presidio\n"
            "9. The Inn Above Tide\n"
            "10. Cavallo Point\n"
            "11. Casa Madrona Hotel and Spa\n"
            "12. Cow Hollow Inn and Suites\n"
            "13. Samesun San Francisco\n"
            "14. Inn on Broadway\n"
            "15. Coventry Motor Inn\n"
            "16. HI San Francisco Fisherman's Wharf Hostel\n"
            "17. Loews Regency San Francisco Hotel\n"
            "18. Fairmont Heritage Place Ghirardelli Square\n"
            "19. Hotel Drisco Pacific Heights\n"
            "20. Travelodge by Wyndham Presidio San Francisco"
        ),
    },
]

memory.add(conversation, user_id=USER_ID)

def get_travel_info(question, use_memory=True):
    """
    Get travel information based on user's question and optionally their preferences from memory.
    """
    if use_memory:
        previous_memories = memory.search(question, user_id=USER_ID)
        relevant_memories_text = ""
        if previous_memories:
            print("Using previous memories to enhance the search...")
            relevant_memories_text = "\n".join(mem["memory"] for mem in previous_memories)

        command = "Find travel information based on my interests:"
        prompt = f"{command}\n Question: {question} \n My preferences: {relevant_memories_text}"
    else:
        command = "Find travel information based on my interests:"
        prompt = f"{command}\n Question: {question}"

    print("Searching for travel information...")
    browse_result = multion.browse(cmd=prompt)
    return browse_result.message

question = "Show me flight details for it."
answer_without_memory = get_travel_info(question, use_memory=False)
answer_with_memory = get_travel_info(question, use_memory=True)
print("Answer without memory:", answer_without_memory)
print("Answer with memory:", answer_with_memory)
