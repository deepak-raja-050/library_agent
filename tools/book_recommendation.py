from langchain_core.tools import tool

@tool
def book_recommendation(topic: str) -> str:
    """Recommend books based on a topic, subject, skill level, or user interest."""

    recommendations = {
        "python": [
            "Python Crash Course by Eric Matthes",
            "Automate the Boring Stuff with Python by Al Sweigart",
            "Fluent Python by Luciano Ramalho"
        ],
        "c programming": [
            "The C Programming Language by Brian Kernighan and Dennis Ritchie",
            "C Programming: A Modern Approach by K. N. King"
        ],
        "machine learning": [
            "Hands-On Machine Learning by Aurélien Géron",
            "Introduction to Machine Learning with Python by Andreas Müller and Sarah Guido"
        ],
        "ai": [
            "Artificial Intelligence: A Modern Approach by Stuart Russell and Peter Norvig",
            "Deep Learning by Ian Goodfellow, Yoshua Bengio, and Aaron Courville"
        ]
    }

    topic_lower = topic.lower()

    for key in recommendations:
        if key in topic_lower:
            return "\n".join(recommendations[key])

    return (
        f"No predefined recommendations for '{topic}'. "
        "Use web_search to find current book recommendations."
    )