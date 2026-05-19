import nltk
from textblob import TextBlob
import random
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class FoodTherapist:
    """
    AI Food Therapist module for psychological support in healthy food choices.
    
    Features:
    - Analyzes user input for emotions and intent using NLP
    - Detects cravings and suggests healthy alternatives
    - Provides empathetic, motivational responses
    - Tracks interaction patterns for personalized adjustments
    - Offers mindful eating tips
    
    Example usage:
        therapist = FoodTherapist()
        response = therapist.chat("I really want to eat pizza, but I know it's unhealthy")
        print(response)  # "It's okay! You can try a homemade veggie pizza or just one slice. Remember, balance is key! You're doing great..."
    """

    def __init__(self):
        # Initialize NLTK components
        self.sentiment_analyzer = None
        try:
            from nltk.sentiment import SentimentIntensityAnalyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except ImportError:
            print("NLTK SentimentIntensityAnalyzer not available. Using TextBlob only.")
        
        # Dictionary of healthy food alternatives
        self.food_alternatives = {
            "pizza": ["homemade veggie pizza with whole wheat crust", "cauliflower crust pizza with veggies", "one slice of your favorite pizza"],
            "chocolate": ["dark chocolate (70%+ cocoa) with almonds", "Greek yogurt with berries", "a piece of fruit with nut butter"],
            "chips": ["air-popped popcorn with herbs", "veggie sticks with hummus", "baked sweet potato chips"],
            "ice cream": ["frozen yogurt with fruit", "nice cream (frozen bananas blended)", "a small bowl of your favorite ice cream"],
            "cake": ["fruit salad with a dollop of yogurt", "baked apples with cinnamon", "a small piece of dark chocolate cake"],
            "fried food": ["baked or grilled alternatives", "air-fried versions", "oven-baked fries"],
            "soda": ["sparkling water with lemon", "herbal tea", "infused water"],
            "candy": ["dried fruit", "nuts and seeds mix", "dark chocolate pieces"]
        }

        # Keywords for intent detection
        self.intent_keywords = {
            'hunger': ['hungry', 'starving', 'empty stomach', 'need food', 'craving food'],
            'boredom': ['bored', 'nothing to do', 'kill time', 'entertain myself', 'distract'],
            'stress': ['stressed', 'anxious', 'worried', 'overwhelmed', 'tense'],
            'emotions': ['sad', 'angry', 'happy', 'emotional', 'mood', 'feeling down', 'celebrating']
        }

        # Interaction history for pattern tracking
        self.history = []

        # Mindful eating tips
        self.mindful_tips = [
            "Eat slowly and savor each bite to enjoy your food more.",
            "Pause halfway through your meal to check in with your fullness level.",
            "Focus on the texture, aroma, and taste of your food.",
            "Put down your utensils between bites to eat more mindfully.",
            "Eat without distractions like TV or phone to stay present.",
            "Stop eating when you're 80% full to avoid overeating.",
            "Drink water before meals to help with portion control."
        ]

        # Positive reinforcement messages
        self.encouragements = [
            "You're doing great by being mindful of your choices!",
            "Every healthy decision is a step toward feeling better.",
            "Be kind to yourself - you're worthy of nourishing food.",
            "Progress takes time, and you're on the right path.",
            "Small changes add up to big results over time.",
            "You're stronger than your cravings - you've got this!",
            "Celebrate your awareness and commitment to health."
        ]

    def analyze_input(self, text):
        """
        Analyze user input for emotion, intent, and cravings.
        
        Returns:
            dict: {'emotion': str, 'intent': str, 'craving': str or None}
        """
        # Detect intent based on keywords
        intent = 'unknown'
        text_lower = text.lower()
        for key, words in self.intent_keywords.items():
            if any(word in text_lower for word in words):
                intent = key
                break
        
        # Analyze sentiment/emotion
        emotion = 'neutral'
        if self.sentiment_analyzer:
            scores = self.sentiment_analyzer.polarity_scores(text)
            compound = scores['compound']
            if compound > 0.05:
                emotion = 'positive'
            elif compound < -0.05:
                emotion = 'negative'
        else:
            # Fallback to TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                emotion = 'positive'
            elif polarity < -0.1:
                emotion = 'negative'
        
        # Detect food cravings using simple tokenization
        craving = None
        tokens = nltk.word_tokenize(text_lower)
        for token in tokens:
            if token in self.food_alternatives:
                craving = token
                break
        
        # Also check for common food words not in alternatives
        common_foods = ['burger', 'fries', 'pasta', 'bread', 'cookie', 'donut']
        if not craving:
            for food in common_foods:
                if food in text_lower:
                    craving = food
                    break

        return {
            'emotion': emotion,
            'intent': intent,
            'craving': craving
        }

    def generate_response(self, analysis):
        """
        Generate an empathetic, helpful response based on analysis.
        
        Args:
            analysis (dict): Result from analyze_input
            
        Returns:
            str: AI response
        """
        emotion = analysis['emotion']
        intent = analysis['intent']
        craving = analysis['craving']
        
        response_parts = []
        
        # Address the intent/emotion
        if intent == 'hunger':
            response_parts.append("It sounds like you're physically hungry. That's a great time to nourish your body with healthy choices!")
        elif intent == 'boredom':
            response_parts.append("Eating out of boredom is so common! Try finding a non-food activity first, like a quick walk or calling a friend.")
        elif intent == 'stress':
            response_parts.append("Stress eating is a natural response, but there are gentler ways to cope. Let's focus on foods that truly support you.")
        elif intent == 'emotions':
            response_parts.append("Emotional eating can be comforting, but let's also consider what your body really needs right now.")
        elif emotion == 'negative':
            response_parts.append("I hear that you're struggling with this choice. It's completely okay to have cravings - you're human!")
        else:
            response_parts.append("Thanks for sharing how you're feeling. Let's work together on making choices that feel good for you.")
        
        # Suggest alternatives for cravings
        if craving:
            alternatives = self.food_alternatives.get(craving, [f"a healthier version of {craving}"])
            alternative = random.choice(alternatives)
            response_parts.append(f"For your craving for {craving}, you could try {alternative}. Balance is key - you don't have to be perfect!")
        
        # Add positive reinforcement
        encouragement = random.choice(self.encouragements)
        response_parts.append(encouragement)
        
        # Add mindful eating tip
        tip = random.choice(self.mindful_tips)
        response_parts.append(f"Mindful eating tip: {tip}")
        
        # Sometimes ask a follow-up question to gather more info
        if random.random() < 0.3:  # 30% chance
            questions = [
                "How are you feeling emotionally right now?",
                "On a scale of 1-10, how hungry are you?",
                "What's one thing that might help you feel better besides food?"
            ]
            question = random.choice(questions)
            response_parts.append(question)
        
        return " ".join(response_parts)

    def chat(self, user_input):
        """
        Process user input and return AI response.
        
        Args:
            user_input (str): User's message
            
        Returns:
            str: AI response
        """
        analysis = self.analyze_input(user_input)
        response = self.generate_response(analysis)
        
        # Store in history for pattern tracking
        self.history.append({
            'timestamp': None,  # Could add datetime if needed
            'input': user_input,
            'analysis': analysis,
            'response': response
        })
        
        return response

    def get_patterns(self):
        """
        Analyze patterns in user interactions.
        
        Returns:
            dict: Counts of different intents and emotions
        """
        if not self.history:
            return {}
        
        intents = [entry['analysis']['intent'] for entry in self.history]
        emotions = [entry['analysis']['emotion'] for entry in self.history]
        cravings = [entry['analysis']['craving'] for entry in self.history if entry['analysis']['craving']]
        
        return {
            'intent_counts': Counter(intents),
            'emotion_counts': Counter(emotions),
            'craving_counts': Counter(cravings),
            'total_interactions': len(self.history)
        }

    def get_personalized_suggestions(self):
        """
        Generate suggestions based on interaction patterns.
        
        Returns:
            list: Personalized tips based on history
        """
        if not self.history:
            return ["Start by tracking your eating patterns to better understand your habits."]
        
        patterns = self.get_patterns()
        suggestions = []
        
        # Suggestions based on common intents
        intent_counts = patterns.get('intent_counts', {})
        if intent_counts.get('boredom', 0) > intent_counts.get('hunger', 0):
            suggestions.append("It seems boredom eating is common for you. Try keeping healthy snacks prepped and ready.")
        
        if intent_counts.get('stress', 0) > 2:
            suggestions.append("When stress triggers eating, try deep breathing or a short walk first.")
        
        # Suggestions based on emotions
        emotion_counts = patterns.get('emotion_counts', {})
        if emotion_counts.get('negative', 0) > len(self.history) * 0.5:
            suggestions.append("Remember to be gentle with yourself. Negative self-talk can make healthy choices harder.")
        
        if not suggestions:
            suggestions.append("Keep up the great work being mindful about your eating habits!")
        
        return suggestions


# Example usage and testing
if __name__ == "__main__":
    therapist = FoodTherapist()
    
    # Example interactions
    examples = [
        "I really want to eat pizza, but I know it's unhealthy",
        "I'm so stressed and just want chocolate",
        "I'm bored and thinking about chips",
        "I'm genuinely hungry for something good",
        "I'm feeling sad and want ice cream"
    ]
    
    for example in examples:
        print(f"User: {example}")
        response = therapist.chat(example)
        print(f"AI: {response}")
        print("-" * 50)
    
    # Show patterns
    print("Interaction Patterns:")
    patterns = therapist.get_patterns()
    for key, value in patterns.items():
        print(f"{key}: {value}")
    
    print("\nPersonalized Suggestions:")
    suggestions = therapist.get_personalized_suggestions()
    for suggestion in suggestions:
        print(f"- {suggestion}")