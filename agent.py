import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools.book_recommendation import book_recommendation
from tools.book_summary import book_summary

from tools.search_library import search_library
from tools.availability import check_availability
from tools.borrow_book import borrow_book
from tools.return_book import return_book
from tools.web_search_tool import web_search
from tools.memory_tools import save_preference, get_preferences


load_dotenv()


# -----------------------------
# LLM
# -----------------------------

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)


# -----------------------------
# Tools
# -----------------------------

tools = [
    search_library,
    check_availability,
    borrow_book,
    return_book,
    web_search,
    book_recommendation,
    book_summary,
    save_preference,
    get_preferences
]


# -----------------------------
# Agent
# -----------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are an intelligent Library Management Assistant.

You can:
- Search for books in the library
- Check book availability
- Borrow books
- Return books
- Search the internet
- Remember user preferences
- Retrieve saved preferences

IMPORTANT:
Maintain the context of the current conversation.

If the user gives a short response such as:
"yes", "no", "okay", "do it", "search it", or "that one",
interpret it using the previous messages in the conversation.

Use search_library when the user asks about books in our library.

Use check_availability when the user asks whether a specific book
is available.

Use borrow_book when the user wants to borrow a book.

Use return_book when the user wants to return a book.

Use web_search when the user asks for information that requires
the internet or when the library does not contain the requested
books and the user agrees to an internet search.

Use save_preference when the user tells you a preference that
could be useful in future conversations.

Use get_preferences when saved preferences could help answer
the user's request.

You may use multiple tools for a single request.

Never invent library information.

For borrowing and returning, always use the appropriate tool and
report the actual result.
Use book_recommendation when the user asks for book recommendations.

Use book_summary when the user asks for a summary or explanation of a book.

If a summary or recommendation is not available from the tool,
use web_search to find relevant information.
"""
)


# -----------------------------
# Conversation memory
# -----------------------------

conversation_history = []


# -----------------------------
# Chat
# -----------------------------

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = agent.invoke({
        "messages": conversation_history
    })

    conversation_history = response["messages"]

    print("\nAgent:", response["messages"][-1].content)