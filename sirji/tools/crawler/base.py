import os
import time
from urllib.parse import urlparse

class BaseContentHandler:
    def handle(self, url, output_dir):
        raise NotImplementedError("Each handler must implement the 'handle' method.")

    @staticmethod
    def save_content(content, url, output_dir, extension):
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            unix_timestamp = int(time.time())
            filename = "index_" + unix_timestamp.__str__()
        filename = f"{filename}.{extension}"
        output_path = os.path.join(output_dir, "external_resources", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved: {output_path}")
