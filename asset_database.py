import sqlite3
import os
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
                location TEXT,
                image BLOB
            )
        """)
        self.conn.commit()

    def get_assets(self):
        cursor = self.conn.execute('SELECT * FROM assets')
        return [Asset(*row) for row in cursor]

    def add_asset(self, asset):
        # Try to load the image from the file
        image_data = None
        if asset.image_path and os.path.exists(asset.image_path):
            with open(asset.image_path, 'rb') as f:
                image_data = f.read()

        # If image data could not be loaded from the file, use the image property
        if not image_data and asset.image:
            # Insert the asset data into the database
            self.conn.execute("""
                INSERT INTO assets (name, tags, description, link, image_path, location) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (asset.name, ','.join(asset.tags), asset.description, asset.link, asset.image_path, asset.location))
        else:
            self.conn.execute("""
                INSERT INTO assets (name, tags, description, link, image_path, location, image) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (asset.name, ','.join(asset.tags), asset.description, asset.link, asset.image_path, asset.location,
                  image_data))
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
        #yas


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
