import os
from groq import Groq
from dotenv import load_dotenv

def get_schedule_summary(markdown_table):
    """
    Sends the timetable to the Groq LLM for a natural language summary.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        return "ERROR: Groq API Key not found. Please set the GROQ_API_KEY environment variable."

    try:
        client = Groq(api_key=groq_api_key)

        system_prompt = (
            "You are an expert AI assistant specializing in schedule analysis and "
            "timetable summarization. Your task is to analyze the provided weekly class "
            "schedule (formatted as a Markdown table) and present a comprehensive, "
            "friendly, chat-like summary. "
            "DO NOT repeat the table. Focus on summarizing key takeaways."
        )

        user_prompt = f"""
        Analyze this weekly class schedule table and provide a friendly, easy-to-read summary.

        Your summary must include:
        1. **Total Days/Classes:** Which days of the week have classes and the total number of unique subjects.
        2. **Time Range:** The earliest start time and the latest end time across the entire week.
        3. **Longest/Shortest Day:** Mention the day with the most classes or longest duration.
        4. **Detailed Schedule:** Provide a breakdown of the schedule for All days in a week.

        ---
        TIMETABLE DATA:
        {markdown_table}
        ---

        Start your response with a friendly greeting like "Hello! I've analyzed your schedule..."
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.1-8b-instant",
        )

        summary_text = chat_completion.choices[0].message.content
        usage_data = {
            "prompt_tokens": chat_completion.usage.prompt_tokens,
            "completion_tokens": chat_completion.usage.completion_tokens,
            "total_tokens": chat_completion.usage.total_tokens
        }

        return summary_text, usage_data

    except Exception as e:
        return f"An error occurred during LLM processing: {e}", {}