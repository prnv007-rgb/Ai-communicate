import spacy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentence_transformers import SentenceTransformer, util
import re



class RubricScorer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        
        # Initialize heavy models once
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Define reference sentences for semantic matching
        self.semantic_targets = {
            "Family": "I live with my family parents mother father siblings brothers sisters",
            "Hobbies": "I like to play cricket read books enjoy dancing hobbies interests free time activities sports",
            "Ambition": "I want to become a doctor engineer scientist dream goal aspiration future career",
            "Location": "I am from India city village live in hometown place origin",
            "About_Family": "my family is kind loving supportive caring special thing about family",
            "Fun_Fact": "fun fact interesting thing unique about me special quality",
            "Strengths": "good at achievement award won certificate strength talent skill"
        }

    def analyze(self, text, duration_sec):
        doc = self.nlp(text)
        words = [token.text for token in doc if not token.is_punct]
        word_count = len(words)
        
        scores = {}
        feedback = {}

    
        # 1. SALUTATION (5 points)
     
        lower_text = text.lower()
        if any(x in lower_text for x in ["excited to introduce", "feeling great"]):
            salutation_score = 5
            feedback['Salutation'] = "Excellent salutation with enthusiasm detected."
        elif any(x in lower_text for x in ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]):
            salutation_score = 4
            feedback['Salutation'] = "Good formal greeting found."
        elif any(x in lower_text for x in ["hi", "hello"]):
            salutation_score = 2
            feedback['Salutation'] = "Basic greeting found."
        else:
            salutation_score = 0
            feedback['Salutation'] = "No salutation detected."
        scores['Salutation'] = salutation_score

       
        # 2. KEYWORDS (30 points)
        # Must Have: 4 points each
        # Good to Have: 2 points each
      
        found_must_have = []
        found_good_to_have = []
        
        
        if any(ent.label_ == "PERSON" for ent in doc.ents) or "myself" in lower_text or "my name is" in lower_text:
            found_must_have.append("Name")
        
        
        if any(ent.label_ == "DATE" for ent in doc.ents) or "years old" in lower_text or any(word.isdigit() and 5 <= int(word) <= 20 for word in words if word.isdigit()):
            found_must_have.append("Age")
        
 
        if any(word in lower_text for word in ["school", "class", "grade", "section", "studying"]):
            found_must_have.append("School/Class")
        
      
        input_embedding = self.embedder.encode(text)
        
    
        for key in ["Family", "Hobbies"]:
            target_embedding = self.embedder.encode(self.semantic_targets[key])
            sim = util.cos_sim(input_embedding, target_embedding).item()
            if sim > 0.25: 
                found_must_have.append(key)
        
      
        for key in ["Location", "Ambition", "About_Family", "Fun_Fact", "Strengths"]:
            target_embedding = self.embedder.encode(self.semantic_targets[key])
            sim = util.cos_sim(input_embedding, target_embedding).item()
            if sim > 0.25:
                found_good_to_have.append(key)
        
        keyword_score = (len(found_must_have) * 4) + (len(found_good_to_have) * 2)
        keyword_score = min(keyword_score, 30)
        scores['Keywords'] = keyword_score
        feedback['Keywords'] = f"Found {len(found_must_have)} must-have keywords ({', '.join(found_must_have)}) and {len(found_good_to_have)} good-to-have keywords ({', '.join(found_good_to_have)})."

    
        # 3. FLOW (5 points)
        # Order: Salutation → Name → Mandatory → Optional → Closing
       
        sentences = [sent.text for sent in doc.sents]
        
        
        has_salutation_first = salutation_score > 0
        has_closing = any(word in lower_text for word in ["thank you", "thanks", "grateful", "bye", "goodbye"])
        
       
        name_early = False
        if len(sentences) >= 2:
            first_two = " ".join(sentences[:2]).lower()
            if "myself" in first_two or any(ent.label_ == "PERSON" for ent in self.nlp(first_two).ents):
                name_early = True
        
        if has_salutation_first and name_early and has_closing:
            flow_score = 5
            feedback['Flow'] = "Good flow: proper order followed."
        else:
            flow_score = 0
            feedback['Flow'] = "Flow could be improved. Expected order: Salutation → Name → Details → Closing."
        scores['Flow'] = flow_score

   
        # 4. SPEECH RATE / WPM (10 points)
       
        if duration_sec > 0:
            wpm = (word_count / duration_sec) * 60
            if 111 <= wpm <= 140:
                wpm_score = 10
            elif (81 <= wpm <= 110) or (141 <= wpm <= 160):
                wpm_score = 6
            elif wpm > 160:
                wpm_score = 2
            elif wpm < 81:
                wpm_score = 2
            else:
                wpm_score = 2
            feedback['Speech Rate'] = f"WPM: {int(wpm)}. "
            if wpm_score == 10:
                feedback['Speech Rate'] += "Ideal pace!"
            elif wpm_score == 6:
                feedback['Speech Rate'] += "Slightly fast/slow but acceptable."
            else:
                feedback['Speech Rate'] += "Too fast or too slow."
        else:
            wpm = 0
            wpm_score = 0
            feedback['Speech Rate'] = "Duration not provided."
        scores['Speech Rate'] = wpm_score

       
        # 5. GRAMMAR (10 points)
        # Formula: (1 - min(errors per 100 words / 10, 1)) × 10
      
        grammar_errors = 0
        for sent in sentences:
            if sent and len(sent) > 0:
                # Only count severe issues
                if not sent[0].isupper():
                    grammar_errors += 0.5  
                if sent[-1] not in '.!?':
                    grammar_errors += 0.5  
        
        errors_per_100 = (grammar_errors / word_count) * 100 if word_count > 0 else 0
        grammar_score = (1 - min(errors_per_100 / 10, 1)) * 10
        grammar_score = max(2, grammar_score)  
        scores['Grammar'] = round(grammar_score, 1)
        feedback['Grammar'] = f"Estimated {grammar_errors} grammar issues. Score based on error rate."

      
        # 6. VOCABULARY / TTR (10 points)
        
        unique_words = set([w.lower() for w in words])
        ttr = len(unique_words) / word_count if word_count > 0 else 0
        
        if ttr >= 0.9:
            vocab_score = 10
        elif ttr >= 0.7:
            vocab_score = 8
        elif ttr >= 0.5:
            vocab_score = 6
        elif ttr >= 0.3:
            vocab_score = 4
        else:
            vocab_score = 2
        scores['Vocabulary'] = vocab_score
        feedback['Vocabulary'] = f"TTR: {ttr:.2f}. "
        if vocab_score >= 8:
            feedback['Vocabulary'] += "Rich vocabulary!"
        else:
            feedback['Vocabulary'] += "Try using more varied words."

       
        # 7. CLARITY / Filler Word Rate (15 points)
        
        fillers = ["um", "uh", "like", "you know", "so", "actually", "basically", "right", 
                   "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"]
        filler_count = sum(1 for w in words if w.lower() in fillers)
        filler_rate = (filler_count / word_count) * 100 if word_count > 0 else 0
        
        if filler_rate <= 3:
            clarity_score = 15
        elif filler_rate <= 6:
            clarity_score = 12
        elif filler_rate <= 9:
            clarity_score = 9
        elif filler_rate <= 12:
            clarity_score = 6
        else:
            clarity_score = 3
        scores['Clarity'] = clarity_score
        feedback['Clarity'] = f"Filler word rate: {filler_rate:.1f}%. Found {filler_count} filler words."

        
        # 8. ENGAGEMENT / Sentiment (15 points)
        # Using VADER positive score only
       
       
        sentiment = self.sentiment_analyzer.polarity_scores(text)
        
        
        compound_score = sentiment['compound'] 
        positive_score = sentiment['pos']  
        
        normalized_compound = (compound_score + 1) / 2
        
        # Weighted average: 70% compound, 30% positive
        engagement_metric = (0.7 * normalized_compound) + (0.3 * positive_score)
        
        if engagement_metric >= 0.75:
            engagement_score = 15
        elif engagement_metric >= 0.60:
            engagement_score = 12
        elif engagement_metric >= 0.45:
            engagement_score = 9
        elif engagement_metric >= 0.30:
            engagement_score = 6
        else:
            engagement_score = 3
        scores['Engagement'] = engagement_score
        feedback['Engagement'] = f"Sentiment metric: {engagement_metric:.2f} (compound: {compound_score:.2f}, positive: {positive_score:.2f}). "
        if engagement_score >= 12:
            feedback['Engagement'] += "Very engaging and positive tone!"
        else:
            feedback['Engagement'] += "Try to sound more enthusiastic."

        
        # FINAL SCORE CALCULATION
        
        total_score = sum(scores.values())
        
        return {
            "overall_score": round(total_score, 1),
            "metrics": scores,
            "feedback": feedback,
            "details": {
                "wpm": int(wpm) if duration_sec > 0 else 0,
                "word_count": word_count,
                "filler_count": filler_count,
                "ttr": round(ttr, 2),
                "sentiment_compound": round(sentiment['compound'], 2),
                "sentiment_positive": round(sentiment['pos'], 2)
            }
        }


