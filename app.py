from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)
CORS(app)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
if OPENAI_API_KEY:
    import openai
    openai.api_key = OPENAI_API_KEY
    client = True
else:
    client = None
    print("Warning: OPENAI_API_KEY not set. Generative AI responses will not be available.")
GITHUB_HEALTH_DATA = {
    'maternal': {
        'pregnancy_complications': [
            'Gestational diabetes - high blood sugar during pregnancy',
            'Preeclampsia - high blood pressure and protein in urine',
            'Placental insufficiency - reduced blood flow to placenta',
            'Hyperemesis gravidarum - severe morning sickness',
            'Gestational hypertension - high blood pressure in pregnancy'
        ],
        'nutrition': [
            'Folic acid (400-800 mcg daily) - prevents birth defects',
            'Iron (27 mg daily) - prevents anemia and supports oxygen transport',
            'Calcium (1000 mg daily) - supports fetal bone development',
            'Protein (70-100g daily) - essential for fetal development',
            'Omega-3 fatty acids - supports brain development'
        ],
        'prenatal_care': [
            'First trimester screening (11-13 weeks)',
            'Second trimester screening (15-22 weeks)',
            'Third trimester monitoring (28-36 weeks)',
            'Regular blood pressure and glucose monitoring',
            'Fetal movement counting from 28 weeks'
        ]
    },
    'child': {
        'common_illnesses': [
            'Common cold - caused by viral infection, usually resolves in 7-10 days',
            'Ear infections - often follow upper respiratory infections',
            'Throat infections (strep throat) - bacterial or viral',
            'Hand-foot-mouth disease - viral, common in children under 5',
            'Chickenpox - viral, preventable with vaccination'
        ],
        'immunization': [
            'Birth: Hepatitis B (HepB)',
            '1-2 months: Rotavirus, Pneumococcal, Diphtheria/Tetanus/Pertussis',
            '4-6 months: Second doses of rotavirus, pneumococcal, DTaP',
            '6 months: Influenza vaccine (2 doses 4 weeks apart)',
            '12-15 months: Measles/Mumps/Rubella (MMR), Varicella'
        ],
        'child_safety': [
            'Car seats - use appropriate age/weight car seat',
            'Choking hazards - avoid small objects, nuts, hard candy',
            'Supervision - constant supervision prevents accidents',
            'Water safety - drowning is leading cause of unintentional injury',
            'Sleep safety - back sleeping position reduces SIDS risk'
        ]
    }
}
class UMASeverityDetector:
    def __init__(self):
        self.critical_keywords = {
            'maternal': [
                'severe bleeding', 'heavy bleeding', 'excessive bleeding', 'bleeding profusely',
                'unconscious', 'seizure', 'convulsion', 'cannot breathe', 'difficulty breathing',
                'severe chest pain', 'sharp abdominal pain', 'severe headache', 'vision loss',
                'water broke early', 'premature labor', 'no fetal movement', 'baby not moving',
                'severe preeclampsia', 'eclampsia', 'high blood pressure', 'severe swelling'
            ],
            'child': [
                'unconscious', 'not breathing', 'difficulty breathing', 'blue lips', 'blue skin',
                'severe dehydration', 'no urination', 'high fever', 'fever above 104',
                'seizure', 'convulsion', 'severe vomiting', 'cannot keep fluids down',
                'severe diarrhea', 'blood in stool', 'severe rash', 'difficulty swallowing',
                'choking', 'ingested poison', 'severe injury', 'head trauma'
            ]
        }
        self.high_severity_keywords = {
            'maternal': [
                'moderate bleeding', 'spotting', 'contractions', 'back pain', 'cramping',
                'nausea', 'vomiting', 'fever', 'dizziness', 'fatigue', 'swelling',
                'mood changes', 'anxiety', 'depression', 'irregular heartbeat',
                'vaginal discharge', 'urinary issues', 'painful urination'
            ],
            'child': [
                'fever', 'cough', 'runny nose', 'vomiting', 'diarrhea', 'rash',
                'irritability', 'not eating', 'not drinking', 'sleepy', 'lethargic',
                'crying', 'crying excessively', 'ear pain', 'throat pain',
                'abdominal pain', 'constipation', 'dry skin'
            ]
        }

        self.moderate_keywords = {
            'maternal': [
                'mild discomfort', 'mild pain', 'occasional nausea', 'tiredness',
                'mild headache', 'mood swings', 'slight swelling'
            ],
            'child': [
                'mild fever', 'mild cough', 'restless', 'minor rash', 'mild irritability'
            ]
        }
        self.problem_categories = {
            'gynecology': {
                'keywords': ['gynecology', 'gynecological', 'periods', 'menstruation', 'menstrual', 'pregnancy', 'pregnant', 'labor', 'delivery', 'postpartum', 'pcos', 'endometriosis', 'fibroids', 'irregular periods', 'heavy bleeding', 'cramping', 'pelvic', 'vulva', 'vaginal', 'ovarian', 'uterine', 'reproductive'],
                'doctors': ['Dr. Anjali Desai', 'Dr. Meera Nair', 'Dr. Neha Gupta']
            },
            'mental_health': {
                'keywords': ['depression', 'anxiety', 'stress', 'mental', 'psychological', 'emotional', 'mood', 'bipolar', 'panic', 'trauma', 'ptsd', 'suicidal', 'depressed', 'anxious', 'overthinking'],
                'doctors': ['Dr. Vikram Singh', 'Dr. Arun Verma']
            },
            'gastro': {
                'keywords': ['stomach', 'belly', 'abdominal', 'digestive', 'diarrhea', 'constipation', 'bloating', 'indigestion', 'nausea', 'vomiting', 'heartburn', 'acid reflux', 'gastro', 'ibs', 'ulcer'],
                'doctors': ['Dr. Priya Sharma', 'Dr. Rajesh Kumar']
            },
            'pediatric': {
                'keywords': ['baby', 'infant', 'child', 'kid', 'toddler', 'newborn', 'pediatric', 'children', 'kids'],
                'doctors': ['Dr. Rajesh Kumar']
            },
            'urology': {
                'keywords': ['urology', 'urinary', 'kidney', 'bladder', 'prostate', 'urination', 'urologist', 'urine'],
                'doctors': ['Dr. Ravi Patel']
            },
            'general': {
                'keywords': [],
                'doctors': ['Dr. Priya Sharma', 'Dr. Rajesh Kumar']
            }
        }
        self.doctor_request_keywords = [
            'connect me to', 'connect to doctor', 'connect to a doctor', 'connect to healthcare',
            'connect to healthcare professional', 'connect to medical', 'connect to physician',
            'want to see doctor', 'need to see doctor', 'want to see a doctor', 'need to see a doctor',
            'speak to doctor', 'talk to doctor', 'speak to a doctor', 'talk to a doctor',
            'want doctor', 'need doctor', 'see doctor', 'doctor please', 'please connect doctor'
        ]
        self.worsening_keywords = [
            'not feeling better', 'not getting better', 'feeling worse', 'getting worse',
            'worsening', 'not improving', 'still not well', 'still unwell', 'still sick',
            'getting sicker', 'more pain', 'increasing pain', 'more symptoms'
        ]
        self.symptom_advice = {
            'bleeding': 'Apply firm pressure to the bleeding area with a clean cloth. Elevate the injured part if possible.',
            'burn': 'Cool the burn with cool (not cold) running water for 10-20 minutes. Do not apply ice or butter.',
            'fever': 'Keep the patient hydrated. Use a cool compress on the forehead. Dress in light clothing.',
            'choking': 'Perform the Heimlich maneuver (abdominal thrusts) immediately if the person cannot breathe or speak.',
            'unconscious': 'Check breathing. If breathing, place in recovery position (on side). If not, start CPR immediately.',
            'seizure': 'Clear the area of hard objects. Place something soft under the head. Do not restrain or put anything in mouth.',
            'headache': 'Rest in a quiet, dark room. Apply a cool or warm compress to the head or neck.',
            'dehydration': 'Sip small amounts of water or oral rehydration solution frequently.',
            'vomiting': 'Sip clear fluids slowly. Avoid solid food until vomiting stops.',
            'breathing': 'Sit upright and lean forward slightly. Loosen tight clothing. Stay calm.',
            'chest pain': 'Sit down and rest. Loosen tight clothing. If user has prescribed heart medication, assist them in taking it.',
             'poison': 'Do not induce vomiting unless told to by a professional. Rinse mouth if poison was swallowed.',
             'fracture': 'Immobilize the injured area. Do not try to realign the bone. Apply an ice pack wrapped in cloth.'
        }
    def detect_problem_category(self, message):
        """Detect the category of health problem"""
        message_lower = message.lower()
        categories_found = []
        for category, data in self.problem_categories.items():
            if category == 'general':
                continue
            for keyword in data['keywords']:
                if keyword in message_lower:
                    categories_found.append(category)
                    break
        return categories_found if categories_found else ['general']
    
    def get_doctor_for_category(self, categories, severity):
        """Get appropriate doctor based on problem category"""
        import random
        primary_category = categories[0] if categories else 'general'
        available_doctors = self.problem_categories[primary_category]['doctors']
        selected_doctor = random.choice(available_doctors)
        doctor_specialties = {
            'Dr. Anjali Desai': 'Gynecologist & Obstetrician',
            'Dr. Rajesh Kumar': 'Pediatrician',
            'Dr. Priya Sharma': 'General Physician',
            'Dr. Vikram Singh': 'Psychiatrist & Mental Health Specialist',
            'Dr. Meera Nair': 'Gynecologist - Reproductive Health',
            'Dr. Neha Gupta': 'Gynecologist - Fertility Specialist',
            'Dr. Arun Verma': 'Psychiatrist - Depression & Anxiety',
            'Dr. Ravi Patel': 'Urologist',
            'Dr. Amit Sharma': 'General Surgeon - Emergency'
        }
        return {
            'name': selected_doctor,
            'specialization': doctor_specialties.get(selected_doctor, 'Healthcare Professional'),
            'experience': '10+ Years',
            'status': 'available'
        }
    def detect_severity(self, message, patient_type='maternal', conversation_history=None):
        message_lower = message.lower()
        # Detect if it's just a greeting
        greeting_keywords = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'how are you', 'can we talk', 'what\'s up', 'howdy']
        is_greeting = any(keyword in message_lower for keyword in greeting_keywords)
        if is_greeting:
            # For simple greetings, return GREETING severity
            return 'GREETING', 0.2, [], False, []
        severity_score = 0
        matched_keywords = []
        problem_categories = self.detect_problem_category(message)
        doctor_request = False
        for keyword in self.doctor_request_keywords:
            if keyword in message_lower:
                doctor_request = True
                matched_keywords.append(keyword)
                break
        worsening = False
        for keyword in self.worsening_keywords:
            if keyword in message_lower:
                worsening = True
                matched_keywords.append(keyword)
                severity_score += 4
                break
        if conversation_history:
            history_text = ' '.join([h.get('content', '') if isinstance(h, dict) else (h if isinstance(h, str) else '') for h in conversation_history]).lower()
            if any(keyword in history_text for keyword in self.worsening_keywords):
                worsening = True
                severity_score += 2
        critical_count = 0
        for keyword in self.critical_keywords.get(patient_type, []):
            if keyword in message_lower:
                critical_count += 1
                matched_keywords.append(keyword)
                severity_score += 10
        high_count = 0
        for keyword in self.high_severity_keywords.get(patient_type, []):
            if keyword in message_lower:
                high_count += 1
                matched_keywords.append(keyword)
                severity_score += 5
        moderate_count = 0
        for keyword in self.moderate_keywords.get(patient_type, []):
            if keyword in message_lower:
                moderate_count += 1
                matched_keywords.append(keyword)
                severity_score += 2
        if doctor_request and not critical_count:
            return 'HIGH', 0.8, matched_keywords, True, problem_categories
        if critical_count > 0 or severity_score >= 10:
            return 'CRITICAL', min(0.95, 0.7 + (critical_count * 0.1)), matched_keywords, False, problem_categories
        elif high_count >= 2 or severity_score >= 5 or (worsening and severity_score >= 3):
            return 'HIGH', min(0.85, 0.6 + (high_count * 0.05)), matched_keywords, False, problem_categories
        elif moderate_count > 0 or severity_score >= 2:
            return 'MODERATE', min(0.75, 0.5 + (moderate_count * 0.05)), matched_keywords, False, problem_categories
        else:
            return 'LOW', 0.4, matched_keywords, False, problem_categories
    def generate_response(self, message, severity, patient_type='maternal', doctor_request=False):
        message_lower = message.lower()
        if severity == 'GREETING':
            return {
                'message': f'Of course! I\'m UMA, your health companion. I\'m here to listen and help. What\'s on your mind? Feel free to share how you\'re feeling or any concerns you have.',
                'action': 'none',
                'severity': severity
            }
        if severity == 'CRITICAL':
            advice = ""
            for symptom, tip in self.symptom_advice.items():
                if symptom in message_lower:
                    advice += f" <br><br>💡 **Immediate Action:** {tip}"
            return {
                'message': f'I understand this is serious. {advice} Let me connect you with an emergency specialist right away. Your safety is my priority.',
                'action': 'ambulance_and_doctor',
                'severity': severity
            }
        elif severity == 'HIGH':
            advice = ""
            for symptom, tip in self.symptom_advice.items():
                if symptom in message_lower:
                    advice += f" <br><br>💡 **Immediate Action:** {tip}"
            if doctor_request or any(keyword in message_lower for keyword in ['connect', 'doctor', 'healthcare professional', 'medical professional']):
                return {
                    'message': f'I hear you. Let me connect you with a doctor right away who can help.{advice}',
                    'action': 'doctor',
                    'severity': severity
                }
            else:
                return {
                    'message': f'I\'m concerned about what you\'re describing.{advice} I think it would be best to talk with a doctor about this. Would you like me to connect you?',
                    'action': 'doctor',
                    'severity': severity
                }
        elif severity == 'MODERATE':
            if any(keyword in message_lower for keyword in ['not feeling better', 'worse', 'worsening', 'not improving']):
                return {
                    'message': 'I see that things aren\'t improving. That\'s important information. I think we should get a doctor\'s perspective on this. Let me connect you.',
                    'action': 'doctor',
                    'severity': 'HIGH'
                }
            else:
                return {
                    'message': 'That sounds like something to keep an eye on. Have you considered talking with a doctor about this? I can help arrange that if you\'d like.',
                    'action': 'suggest_doctor',
                    'severity': severity
                }
        else:
            if any(keyword in message_lower for keyword in ['connect', 'doctor', 'healthcare professional']):
                return {
                    'message': 'Sure, I can help with that. Let me set up a consultation for you.',
                    'action': 'doctor',
                    'severity': 'HIGH'
                }
            else:
                return {
                    'message': 'I\'m here to listen. Tell me more about what you\'re experiencing. What brought this up?',
                    'action': 'monitor',
                    'severity': severity
                }
severity_detector = UMASeverityDetector()
class AIResponseGenerator:
    """Generates intelligent responses using OpenAI's GPT model with training data from GitHub"""
    def __init__(self, openai_client=None):
        self.client = openai_client
        self.knowledge_base = GITHUB_HEALTH_DATA
    def get_context_data(self, patient_type='maternal', severity='LOW'):
        """Build context from knowledge base"""
        context = f"""You are UMA, a warm and empathetic health companion who specializes in {patient_type} health. 
Your goal is to have NATURAL conversations while gently understanding the user's health concerns.
Diagnose through dialogue - ask thoughtful follow-up questions, listen carefully, and guide the conversation naturally.
Never use clinical language or severity labels in conversation. Just talk like a caring health companion.
Be conversational, warm, and supportive. Ask clarifying questions to understand the full picture.
When you recognize a health issue, acknowledge it naturally and suggest next steps if needed.
If symptoms seem serious, suggest seeing a doctor - but do it in a caring, natural way.

You have access to this medical knowledge to inform your responses:
"""
        if patient_type in self.knowledge_base:
            for category, items in self.knowledge_base[patient_type].items():
                context += f"\n{category.replace('_', ' ').title()}:\n"
                for item in items:
                    context += f"- {item}\n"
        context += "\nIMPORTANT CONVERSATION RULES:\n"
        context += "1. Keep responses conversational and friendly\n"
        context += "2. Ask thoughtful follow-up questions to understand better\n"
        context += "3. Never use severity labels like 'LOW RISK' or 'HIGH RISK' in conversation\n"
        context += "4. If the user just wants to chat, be friendly and ask how you can help\n"
        context += "5. Guide naturally toward understanding their concerns through dialogue\n"
        context += "6. Suggest professional help only when appropriate and in a caring way\n"
        return context
    def generate_ai_response(self, message, severity='LOW', patient_type='maternal', conversation_history=None):
        """Generate response using OpenAI GPT"""
        if not self.client:
            return self.generate_fallback_response(message, severity, patient_type)
        try:
            context = self.get_context_data(patient_type, severity)
            messages = [
                {
                    "role": "system",
                    "content": context
                }
            ]
            if conversation_history:
                for entry in conversation_history[-3:]:  
                    if isinstance(entry, dict):
                        if entry.get('type') == 'user':
                            messages.append({"role": "user", "content": entry.get('message', '')})
                        elif entry.get('type') == 'bot':
                            messages.append({"role": "assistant", "content": entry.get('message', '')})
            messages.append({
                "role": "user",
                "content": message
            })
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self.generate_fallback_response(message, severity, patient_type)
    def generate_fallback_response(self, message, severity='LOW', patient_type='maternal'):
        """Fallback response when OpenAI is not available"""
        severity_responses = {
            'CRITICAL': {
                'prefix': '🚨 CRITICAL ALERT:',
                'action': 'IMMEDIATE emergency action required'
            },
            'HIGH': {
                'prefix': '⚠️ HIGH PRIORITY:',
                'action': 'Medical professional consultation needed'
            },
            'MODERATE': {
                'prefix': '📋 MODERATE:',
                'action': 'Professional evaluation recommended'
            },
            'LOW': {
                'prefix': '✅ LOW RISK:',
                'action': 'Continue monitoring'
            }
        }
        response_data = severity_responses.get(severity, severity_responses['LOW'])
        relevant_knowledge = []
        message_lower = message.lower()
        for category, items in self.knowledge_base.get(patient_type, {}).items():
            for item in items:
                if any(word in message_lower for word in item.lower().split()[:3]):
                    relevant_knowledge.append(item)
        knowledge_text = ""
        if relevant_knowledge:
            knowledge_text = "\n\nBased on our medical knowledge:\n"
            for item in relevant_knowledge[:2]:
                knowledge_text += f"• {item}\n"
        return f"{response_data['prefix']} {response_data['action']}.{knowledge_text} Please consult with a healthcare professional for personalized medical advice."
ai_generator = AIResponseGenerator(client)
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        patient_type = data.get('patient_type', 'maternal')
        conversation_history = data.get('history', [])
        use_ai = data.get('use_ai', True)  # Default to AI responses
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        severity, confidence, matched_keywords, doctor_request, problem_categories = severity_detector.detect_severity(message, patient_type, conversation_history)
        # Handle greeting responses
        if severity == 'GREETING':
            response = {
                'message': f'Namaste! I\'m UMA, your maternal and child health assistant. I\'m here to help answer your questions about {patient_type} health concerns. What brings you here today? Feel free to describe any symptoms or health concerns you\'d like to discuss.',
                'action': 'none',
                'severity': 'GREETING',
                'confidence': confidence,
                'matched_keywords': matched_keywords,
                'problem_categories': problem_categories,
                'assigned_doctor': None,
                'response_type': 'greeting',
                'timestamp': datetime.now().isoformat()
            }
            return jsonify(response)
        if use_ai and client:
            ai_response = ai_generator.generate_ai_response(message, severity, patient_type, conversation_history)
            bot_message = ai_response
            response_type = 'ai_generated'
        else:
            template_response = severity_detector.generate_response(message, severity, patient_type, doctor_request)
            bot_message = template_response['message']
            response_type = 'template'
        assigned_doctor = None
        if severity in ['MODERATE', 'HIGH']:
            assigned_doctor = severity_detector.get_doctor_for_category(problem_categories, severity)
        elif severity == 'CRITICAL':
            assigned_doctor = {'name': 'Dr. Amit Sharma', 'specialization': 'General Surgeon - Emergency', 'experience': '12+ Years', 'status': 'available'}
        action = 'none'
        if severity == 'CRITICAL':
            action = 'ambulance_and_doctor'
        elif severity == 'HIGH':
            action = 'doctor'
        elif severity == 'MODERATE' and any(keyword in message.lower() for keyword in ['worse', 'worsening', 'not improving']):
            action = 'doctor'
        response = {
            'message': bot_message,
            'action': action,
            'severity': severity,
            'confidence': confidence,
            'matched_keywords': matched_keywords,
            'problem_categories': problem_categories,
            'assigned_doctor': assigned_doctor,
            'response_type': response_type,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/connect-doctor', methods=['POST'])
def connect_doctor():
    try:
        data = request.json
        patient_info = data.get('patient_info', {})
        return jsonify({
            'status': 'success',
            'message': 'Connecting you to Dr. Priya Sharma, MBBS, MD (Obstetrics & Gynecology). Please wait...',
            'doctor': {
                'name': 'Dr. Priya Sharma',
                'specialization': 'Obstetrics & Gynecology',
                'experience': '12 years',
                'status': 'available'
            },
            'connection_time': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/call-ambulance', methods=['POST'])
def call_ambulance():
    try:
        data = request.json
        patient_info = data.get('patient_info', {})
        location = data.get('location', 'Not provided')
        symptoms = data.get('symptoms', '')
        assigned_doctor = data.get('assigned_doctor', {})
        response_data = {
            'status': 'success',
            'message': '🚨 Ambulance has been dispatched! Estimated arrival time: 15-20 minutes. Please stay calm and follow first aid instructions if applicable.',
            'ambulance': {
                'ambulance_id': 'AMB-2024-001',
                'estimated_arrival': '15-20 minutes',
                'location': location,
                'priority': 'CRITICAL'
            },
            'dispatch_time': datetime.now().isoformat()
        }
        if assigned_doctor and assigned_doctor.get('name'):
            response_data['doctor'] = assigned_doctor
            response_data['message'] = f"🚨 Ambulance dispatched and {assigned_doctor.get('name')} ({assigned_doctor.get('specialization')}) will be available for online consultation. Estimated ambulance arrival: 15-20 minutes."
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'UMA AI Chatbot API'})
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
