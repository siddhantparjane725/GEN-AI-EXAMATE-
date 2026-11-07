from dataclasses import asdict, dataclass

@dataclass
class Record:
    form_number: str
    purpose: str
    who_should_fill: str
    documents_needed: str
    submit_to: str
    source_url: str
    record_id: str = ""
    record_type: str = "form"
    question: str = ""
    answer: str = ""
    category: str = ""

    def to_dict(self):
        return asdict(self)
