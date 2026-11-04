import json
import urllib.parse
import urllib.request
from flask import Blueprint, request, jsonify

translate_bp = Blueprint("translate_bp", __name__)

# In-memory translation cache to make responses instantaneous
_TRANSLATION_CACHE = {}

# Offline fallback dictionary for common campus Lost & Found words across 7 languages
OFFLINE_DICTIONARY = {
    "te": {
        "water bottle platic": "ప్లాస్టిక్ వాటర్ బాటిల్",
        "plastic": "ప్లాస్టిక్",
        "orange yellow": "నారింజ పసుపు",
        "black": "నలుపు",
        "blue": "నీలం",
        "navy": "నేవీ బ్లూ",
        "red": "ఎరుపు",
        "silver": "సిల్వర్",
        "gold": "బంగారు రంగు",
        "green": "ఆకుపచ్చ",
        "white": "తెలుపు",
        "grey": "గ్రే",
        "gray": "గ్రే",
        "brown": "గోధుమ రంగు",
        "laptop": "ల్యాప్‌టాప్",
        "keys": "కీలు (తాళాలు)",
        "wallet": "వాలెట్",
        "bag": "బ్యాగ్",
        "bottle": "బాటిల్",
        "phone": "మొబైల్ ఫోన్"
    },
    "hi": {
        "water bottle platic": "प्लास्टिक पानी की बोतल",
        "plastic": "प्लास्टिक",
        "orange yellow": "नारंगी पीला",
        "black": "काला",
        "blue": "नीला",
        "navy": "नेवी ब्लू",
        "red": "लाल",
        "silver": "सिल्वर",
        "gold": "सुनहरा",
        "green": "हरा",
        "white": "सफेद",
        "grey": "ग्रे",
        "gray": "ग्रे",
        "brown": "भूरा",
        "laptop": "लैपटॉप",
        "keys": "चाबियाँ",
        "wallet": "बटुआ",
        "bag": "बैग",
        "bottle": "बोतल",
        "phone": "मोबाइल फोन"
    },
    "pa": {
        "water bottle platic": "ਪਲਾਸਟਿਕ ਪਾਣੀ ਦੀ ਬੋਤਲ",
        "plastic": "ਪਲਾਸਟਿਕ",
        "orange yellow": "ਸੰਤਰੀ ਪੀਲਾ",
        "black": "ਕਾਲਾ",
        "blue": "ਨੀਲਾ",
        "navy": "ਨੇਵੀ ਬਲੂ",
        "red": "ਲਾਲ",
        "silver": "ਸਿਲਵਰ",
        "gold": "ਸੁਨਹਿਰੀ",
        "green": "ਹਰਾ",
        "white": "ਚਿੱਟਾ",
        "grey": "ਸਲੇਟੀ",
        "gray": "ਸਲੇਟੀ",
        "brown": "ਭੂਰਾ",
        "laptop": "ਲੈਪਟਾਪ",
        "keys": "ਚਾਬੀਆਂ",
        "wallet": "ਬਟੂਆ",
        "bag": "ਬੈਗ",
        "bottle": "ਬੋਤਲ",
        "phone": "ਮੋਬਾਈਲ ਫੋਨ"
    },
    "ml": {
        "water bottle platic": "പ്ലാസ്റ്റിക് വെള്ളക്കുപ്പി",
        "plastic": "പ്ലാസ്റ്റിക്",
        "orange yellow": "ഓറഞ്ച് മഞ്ഞ",
        "black": "കറുപ്പ്",
        "blue": "നീല",
        "navy": "നേവി ബ്ലൂ",
        "red": "ചുവപ്പ്",
        "silver": "വെള്ളി",
        "gold": "സ്വർണ്ണം",
        "green": "പച്ച",
        "white": "വെള്ള",
        "grey": "ഗ്രേ",
        "gray": "ഗ്രേ",
        "brown": "തവിട്ട്",
        "laptop": "ലാപ്‌ടോപ്പ്",
        "keys": "താക്കോലുകൾ",
        "wallet": "പഴ്സ്",
        "bag": "ബാഗ്",
        "bottle": "കുപ്പി",
        "phone": "മൊബൈൽ ഫോൺ"
    },
    "ta": {
        "water bottle platic": "பிளாஸ்டிக் தண்ணீர் பாட்டில்",
        "plastic": "பிளாஸ்டிக்",
        "orange yellow": "ஆரஞ்சு மஞ்சள்",
        "black": "கருப்பு",
        "blue": "நீலம்",
        "navy": "நேவி ப்ளூ",
        "red": "சிவப்பு",
        "silver": "வெள்ளி",
        "gold": "தங்கம்",
        "green": "பச்சை",
        "white": "வெள்ளை",
        "grey": "சாம்பல்",
        "gray": "சாம்பல்",
        "brown": "பழுப்பு",
        "laptop": "லேப்டாப்",
        "keys": "சாவிகள்",
        "wallet": "பணப்பை",
        "bag": "பை",
        "bottle": "பாட்டில்",
        "phone": "கைபேசி"
    },
    "kn": {
        "water bottle platic": "ಪ್ಲಾಸ್ಟಿಕ್ ನೀರಿನ ಬಾಟಲ್",
        "plastic": "ಪ್ಲಾಸ್ಟಿಕ್",
        "orange yellow": "ಕಿತ್ತಳೆ ಹಳದಿ",
        "black": "ಕಪ್ಪು",
        "blue": "ನೀಲಿ",
        "navy": "ನೇವಿ ಬ್ಲೂ",
        "red": "ಕೆಂಪು",
        "silver": "ಬೆಳ್ಳಿ",
        "gold": "ಚಿನ್ನದ ಬಣ್ಣ",
        "green": "ಹಸಿರು",
        "white": "ಬಿಳಿ",
        "grey": "ಬೂದು",
        "gray": "ಬೂದು",
        "brown": "ಕಂದು",
        "laptop": "ಲ್ಯಾಪ್‌ಟಾಪ್",
        "keys": "ಕೀಗಳು",
        "wallet": "ವ್ಯಾಲೆಟ್",
        "bag": "ಬ್ಯಾಗ್",
        "bottle": "ಬಾಟಲಿ",
        "phone": "ಮೊಬೈಲ್ ಫೋನ್"
    }
}

def translate_single(text: str, target_lang: str) -> str:
    if not text or not text.strip() or target_lang == "en":
        return text

    clean_text = text.strip()
    cache_key = f"{target_lang}::{clean_text}"
    if cache_key in _TRANSLATION_CACHE:
        return _TRANSLATION_CACHE[cache_key]

    # Check offline dictionary first (case insensitive)
    lower = clean_text.lower()
    if target_lang in OFFLINE_DICTIONARY and lower in OFFLINE_DICTIONARY[target_lang]:
        res = OFFLINE_DICTIONARY[target_lang][lower]
        _TRANSLATION_CACHE[cache_key] = res
        return res

    # Use Google Free Translate endpoint with timeout
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={urllib.parse.quote(clean_text)}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=3.5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            if payload and payload[0]:
                translated_parts = [segment[0] for segment in payload[0] if segment and segment[0]]
                translated = "".join(translated_parts).strip()
                if translated:
                    _TRANSLATION_CACHE[cache_key] = translated
                    return translated
    except Exception as e:
        print(f"[Translate] Network error translating '{clean_text}' to {target_lang}: {e}")

    # Fallback to original text if translation service unavailable
    return clean_text

@translate_bp.route("", methods=["POST"])
@translate_bp.route("/", methods=["POST"])
def translate_endpoint():
    data = request.get_json() or {}
    target_lang = data.get("target_lang", "en").lower()
    
    # Check single text or array of texts
    if "text" in data:
        translated = translate_single(str(data["text"]), target_lang)
        return jsonify({"translated": translated, "target_lang": target_lang})

    texts = data.get("texts", [])
    results = {}
    for t in texts:
        if t and isinstance(t, str):
            results[t] = translate_single(t, target_lang)

    return jsonify({"translations": results, "target_lang": target_lang})

