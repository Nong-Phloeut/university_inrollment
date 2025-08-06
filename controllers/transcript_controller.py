from models.transcript_model import TranscriptModel

class TranscriptController:
    def __init__(self):
        self.model = TranscriptModel()

    def get_all_transcripts(self):
        return self.model.get_all_transcripts()
