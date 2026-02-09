class Membership:
    def __init__(self, level="normal"):
        self.level = level

    def rent_limit(self):
        if self.level == "member":
            return 5
        elif self.level == "premium":
            return 10
        else:
            return 3
