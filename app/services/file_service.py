import os
from datetime import datetime
from fastapi import File, UploadFile
from app.config.resource import Config


class FileService:

    def list_file(self):
        tree = {}
        for root, dirs, files in os.walk(Config.datasources_path):
            current_level = tree
            folders = root.split(os.sep)[1:]
            for folder in folders:
                current_level = current_level.setdefault(folder, {})
            file_list = []
            for file in files:
                abspath = os.path.join(os.path.abspath(root), file)
                file_size = os.path.getsize(abspath)
                creation_time = datetime.fromtimestamp(os.path.getctime(abspath))
                modification_time = datetime.fromtimestamp(os.path.getmtime(abspath))
                metadata = {
                    "file_size": file_size,
                    "modification_time": modification_time.astimezone(),
                    "creation_time": creation_time.astimezone(),
                }
                file_list.append(
                    {"abs_path": abspath, "rel_path": file, "metadata": metadata}
                )
            current_level["_files"] = file_list
        return tree

    async def upload(self, file: UploadFile = File(...)) -> str:
        filename, file_extension = os.path.splitext(file.filename)
        file_extension = file_extension.lstrip(".")
        save_path = str(
            os.path.join(os.path.abspath(Config.origin_files_location_path), file_extension)
        )
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, file.filename)
        if not os.path.exists(file_path):
            try:
                with open(file_path, "wb") as f:
                    f.write(await file.read())
            except Exception:
                return ""
        return save_path
