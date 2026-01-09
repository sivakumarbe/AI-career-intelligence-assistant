class DocumentStore:
    def __init__(self):
        self.resume_text = None
        self.jd_text = None
        self.vector_built = False

    def store_resume(self, text: str):
        self.resume_text = text
        self.vector_built = False

    def store_jd(self, text: str):
        self.jd_text = text
        self.vector_built = False

    def get_resume(self):
        return self.resume_text

    def get_jd(self):
        return self.jd_text

    def is_ready_for_vector(self):
        return self.resume_text is not None and self.jd_text is not None
