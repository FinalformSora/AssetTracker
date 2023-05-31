class Asset:
    def __init__(self, id, name, tags, description, link, image_path, location, image=None):
        self.id = id
        self.name = name
        self.tags = tags.split(",") if isinstance(tags, str) else tags
        self.description = description
        self.link = link
        self.image_path = image_path
        self.location = location
        self.image = image

