class Asset:
    def __init__(self, name, tags, description, link, image_path, location):
        self.name = name
        self.tags = ','.join(tags)  # Join the tags into a single string
        self.description = description
        self.link = link
        self.image_path = image_path
        self.location = location