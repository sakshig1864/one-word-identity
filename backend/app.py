from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    word = data.get('word', '').strip()
    explanation = data.get('explanation', '').strip()

    if not word or not explanation:
        return jsonify({'error': 'Both word and explanation are required'}), 400

    # Analyze word and explanation separately
    word_sentiment = analyzer.polarity_scores(word)['compound']
    explanation_sentiment = analyzer.polarity_scores(explanation)['compound']
    
    # Combined sentiment for overall score
    combined_sentiment = analyzer.polarity_scores(f"{word} {explanation}")['compound']
    rating = round((combined_sentiment + 1) * 5, 1)  # scale 0-10

    # Grammar check using TextBlob
    blob = TextBlob(explanation)
    corrected_text = str(blob.correct())

    # BUILD HONEST FEEDBACK
    feedback_parts = []
    
    # 1. Analyze the WORD itself
    feedback_parts.append(f"Your word '{word}'")
    
    if word_sentiment > 0.3:
        feedback_parts.append("suggests positivity and strength.")
    elif word_sentiment < -0.3:
        feedback_parts.append("reflects challenging emotions or difficulty.")
    else:
        feedback_parts.append("is neutral or describes a state of being.")
    
    # 2. Analyze the EXPLANATION
    if explanation_sentiment > 0.3:
        feedback_parts.append("Your explanation shows optimism and forward momentum.")
    elif explanation_sentiment < -0.3:
        feedback_parts.append("Your explanation reveals struggle or frustration. That's honest and important to acknowledge.")
    else:
        feedback_parts.append("Your explanation is balanced and reflective.")
    
    # 3. Check for MISMATCH (like "happy" but sad explanation)
    if abs(word_sentiment - explanation_sentiment) > 0.6:
        feedback_parts.append("\n\n⚠️ **Honest observation:** Your word and explanation don't quite match. This might mean:")
        feedback_parts.append("- You're trying to stay positive despite difficulties")
        feedback_parts.append("- You're experiencing mixed feelings")
        feedback_parts.append("- There's a gap between how you want to feel and how you actually feel")
        feedback_parts.append("\nThis self-awareness is valuable. Consider exploring why there's a difference.")
    
    # 4. Grammar suggestion (if needed)
    if corrected_text.lower() != explanation.lower():
        feedback_parts.append(f"\n\n✍️ Grammar suggestion: '{corrected_text}'")
    
    # 5. ACTIONABLE ADVICE based on overall sentiment
    if combined_sentiment < -0.3:
        feedback_parts.append("\n\n💡 **Moving forward:** It's okay to struggle. Consider: What's one small step you could take today? Who could you talk to about this?")
    elif combined_sentiment < 0.3:
        feedback_parts.append("\n\n💡 **Moving forward:** You seem in a transitional space. Reflect on what would help you move toward your goals.")
    else:
        feedback_parts.append("\n\n💡 **Keep going:** You're in a good headspace. Channel this energy into concrete actions toward your goals.")

    feedback = " ".join(feedback_parts)

    return jsonify({
        'rating': rating,
        'feedback': feedback,
        'word_sentiment': round((word_sentiment + 1) * 5, 1),
        'explanation_sentiment': round((explanation_sentiment + 1) * 5, 1)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import send_from_directory

@app.route('/')
def serve():
    return send_from_directory('../frontend/build', 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory('../frontend/build', 'index.html')
