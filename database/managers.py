from .models import user

class UserManager:
  def __init__(self, collection):
    self.db = collection

  def get (self, user_id, created_at, register = True):
    return user.UserCollection(self.db, user_id, created_at, register)
   