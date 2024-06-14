import os
import hashlib

from sirji_tools.logger import create_logger

class BaseContentHandler:
    def handle(self, url, output_dir):
        raise NotImplementedError(
            "Each handler must implement the 'handle' method.")

    def save_content(self, content, url, output_dir, extension):
        logger = create_logger("researcher.log", "debug")
        logger.info(f"Saving crawled content to file at path: {output_dir}")

        filename = f"{self.url_to_md5(url)}.{extension}"
        output_path = os.path.join(output_dir, "external_resources", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Saved crawled content to file at path: {output_dir}")

    def url_to_md5(self, url):
        md5_hash = hashlib.md5()
        md5_hash.update(url.encode('utf-8'))
        hex_md5 = md5_hash.hexdigest()

        return hex_md5
