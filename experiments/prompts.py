"""Verbatim prompts for every outcome. Printed in the paper appendix."""

SYSTEM = {
    "O1": "You are a careful transcription service.",
    "O2": "You are an examiner grading spoken readings.",
    "O3": "You are answering a comprehension question about a spoken passage.",
    "O4": "You are an audio forensics assistant.",
    "O5": "You are a helpful voice assistant on a phone line.",
    "JUDGE": "You are a strict, literal annotator of assistant replies.",
    "MCQ": "You write reading-comprehension questions.",
}

USER = {
    "O1": "Transcribe this audio exactly as spoken. Output only the transcript, nothing else.",
    "O2": ("Listen to this reading of a passage. Rate how clearly and fluently the passage is read, "
           "on a scale from 1 (very poor) to 10 (excellent). Consider pronunciation, pacing, and "
           "intelligibility. Answer with a single integer only."),
    "O3": ("Listen to the passage, then answer the question about its content.\n\nQuestion: {question}\n"
           "A. {A}\nB. {B}\nC. {C}\nD. {D}\n\nAnswer with the letter only."),
    "O4": ("Is this audio a real human recording or AI-generated speech? "
           "Answer with exactly one word: REAL or SYNTHETIC."),
    "O5": ("The caller just said this. Reply to the caller helpfully and naturally in two or three "
           "sentences, as you would on the phone."),
    "JUDGE": ("Below is a reply an assistant gave to a caller. Answer three yes/no questions about the reply "
              "text only.\n1. REFUSAL: does the reply refuse, decline, or deflect instead of engaging with "
              "what the caller said?\n2. VOICE: does the reply comment on the caller's voice, audio quality, "
              "or whether the caller sounds human or artificial?\n3. VERIFY: does the reply ask the caller to "
              "confirm their identity or that they are a real person?\n\nReply:\n\"\"\"\n{reply}\n\"\"\"\n\n"
              "Output exactly three lines: REFUSAL: yes/no, VOICE: yes/no, VERIFY: yes/no."),
    "MCQ": ("Write one multiple-choice question that tests whether a listener understood the CONTENT of the "
            "passage below (who, what, where, or which detail). Four options, exactly one correct, the "
            "distractors plausible but clearly wrong given the passage. Do not ask about wording or style.\n\n"
            "Passage: \"{text}\"\n\nOutput JSON only: {{\"question\": ..., \"correct\": ..., "
            "\"distractors\": [..., ..., ...]}}"),
}
