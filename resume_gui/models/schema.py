# resume_gui/models/schema.py
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Experience:
    role: str = ""
    company: str = ""
    start: str = ""
    end: str = ""
    location: str = ""
    blurb: str = ""
    highlights: List[str] = field(default_factory=list)

# Similarly define Education, Project if you’d like.
# You can convert to/from dict when saving/loading JSON.
