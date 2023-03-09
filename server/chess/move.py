import re

class Move(object):
    pattern = r"[a-h][1-8][a-h][1-8]q?"
    def __init__(self, lan) -> None:
        assert re.fullmatch(self.pattern, lan), lan
        self.start, self.end, self.promotion = lan[:2], lan[2:4], lan[4:]

    def __repr__(self):
        return self.start + self.end + self.promotion
    