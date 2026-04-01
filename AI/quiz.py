import feedparser
import ollama
import re
import random

# 1. Define a dictionary of different BBC News categories
BBC_CATEGORIES = {
    "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "Science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "Entertainment": "http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    "Health": "http://feeds.bbci.co.uk/news/health/rss.xml"
}

def get_random_bbc_news():
    """Picks a random category and fetches the top 5 stories."""
    category_name, url = random.choice(list(BBC_CATEGORIES.items()))
    print(f"--- Today's Category: {category_name} ---")
    
    feed = feedparser.parse(url)
    articles = [f"Story: {e.title}. {e.description}" for e in feed.entries[:5]]
    return "\n".join(articles)

def get_quiz_from_ai(news):
    """Generates the quiz via Ollama."""
    prompt = f"""
    Based on this news:
    {news}
    
    Create 5 multiple choice questions. 
    Format EXACTLY like this for each question:
    Q: [Question text]
    A) [Option]
    B) [Option]
    C) [Option]
    D) [Option]
    Correct: [Letter]
    """
    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def play_quiz(quiz_text):
    """Interactive loop for user answers."""
    questions = re.split(r'Q:', quiz_text)[1:] 
    score = 0
    
    for i, q_block in enumerate(questions):
        print(f"\nQuestion {i+1}:")
        lines = q_block.strip().split('\n')
        
        # We find the 'Correct:' line safely
        main_content = []
        correct_answer = ""
        for line in lines:
            cleaned_line = line.strip().replace("**", "")
            if cleaned_line.startswith("Correct:") or cleaned_line.startswith("Correct Answer:"):
                ans_text = cleaned_line.split(":", 1)[1].upper()
                match = re.search(r'[ABCD]', ans_text)
                correct_answer = match.group(0) if match else ans_text.strip()
            else:
                main_content.append(line)
        
        print("\n".join(main_content))
        
        user_choice = input("Your answer (A, B, C, or D): ").strip().upper()
        
        if user_choice == correct_answer:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. The correct answer was {correct_answer}.")
            
    print(f"\nFinal Score: {score}/5")

if __name__ == "__main__":
    try:
        news_data = get_random_bbc_news()
        if news_data:
            print("Generating quiz...")
            raw_quiz = get_quiz_from_ai(news_data)
            play_quiz(raw_quiz)
        else:
            print("Couldn't fetch news. Check your connection.")
    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")