import sqlite3
from asset import Asset


class AssetDatabase:
    def __init__(self, db_name="assets.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tags TEXT,
                description TEXT,
                link TEXT,
                image_path TEXT,
                location TEXT
            )
        """)

    def get_assets(self):
        self.cursor.execute("SELECT * FROM assets")
        results = self.cursor.fetchall()
        # Convert the results to Assets
        assets = []
        for result in results:
            id, name, tags, description, link, image_path, location = result
            tags = tags.split(',')  # Split the tags back into a list
            asset = Asset(name, tags, description, link, image_path, location)
            assets.append(asset)
        return assets

    def add_asset(self, asset):
        tags_string = ",".join(asset.tags)  # convert list of tags to a comma-separated string
        self.cursor.execute("""
            INSERT INTO assets (name, tags, description, link, image_path, location) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (asset.name, tags_string, asset.description, asset.link, asset.image_path,
              asset.location))  # use tags_string instead of asset.tags
        self.conn.commit()

    def search_assets(self, query):
        self.cursor.execute("SELECT * FROM assets WHERE name LIKE ? OR tags LIKE ?",
                            ('%' + query + '%', '%' + query + '%',))
        results = self.cursor.fetchall()
        # Convert the tags string back to a list before returning the results
        formatted_results = []
        for result in results:
            id, name, tags, description, link, image_path, location = result
            tags_list = tags.split(',')  # split the tags string into a list
            formatted_results.append({
                'id': id,
                'name': name,
                'tags': tags_list,  # replace the tags string with the list
                'description': description,
                'link': link,
                'image_path': image_path,
                'location': location
            })
        return formatted_results

    def close(self):
        # Don't forget to close the connection when you're done
        self.conn.close()

    def get_latest_assets(self, limit=10):
        self.cursor.execute("SELECT * FROM assets ORDER BY id DESC LIMIT ?", (limit,))
        results = self.cursor.fetchall()
        formatted_results = []
        for result in results:
            id, name, tags, description, link, image_path, location = result
            tags_list = tags.split(',')
            formatted_results.append({
                'id': id,
                'name': name,
                'tags': tags_list,
                'description': description,
                'link': link,
                'image_path': image_path,
                'location': location
            })
        return formatted_results
