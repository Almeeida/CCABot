class Collection:
    def __init__(self, collection, id, register):
        self.db = collection
        self.id = id

        self.data = self.get_data()
        if not self.data and register:
            self.data = self.register()

    def get_data(self):
        return self.db.find_one({"_id": self.id})

    def get_structure(self):
        return {
          "_id": self.id
        }

    def register(self):
        data = self.get_structure()
        self.db.insert_one(data)
        return data

    def update(self, data: dict):
        return self.db.update_one({"_id": self.id}, {"$set": data})

    def insert(self, data: dict):
        return self.db.update_one({"_id": self.id}, {"$push": data})

    def remove(self, data: dict):
        return self.db.update_one({"_id": self.id}, {"$pull": data})

    def delete(self):
        return self.db.delete_one({"_id": self.id})
  