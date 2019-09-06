from .models import user

class UserManager:
  def __init__(self, collection):
    self.db = collection

  def get (self, user_id, register = True):
    return user.UserCollection(self.db, user_id, register)
   