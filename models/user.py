from membership import Membership

class User:
    def __init__(self, user_id, username, membership="normal"):
        self.user_id = user_id
        self.username = username
        self.membership = Membership(membership) if isinstance(membership, str) else membership

    def change_membership(self, new_membership):
        if isinstance(new_membership, str):
            self.membership = Membership(new_membership)
        else:
            self.membership = new_membership

    def __str__(self):
        return f"User({self.username}, {self.membership.level})"
