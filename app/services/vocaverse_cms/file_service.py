import os
import uuid
import math
import pandas as pd
from datetime import datetime
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from app.exceptions.errors import FileExists, AlreadyProcessed
from app.models import cms_models
from app.schemas import cms_schemas
from app.config.resource import Config
from app.services.vocaverse_cms import level_service, passage_cms_service

Config.load_config()
# passage_df: pd.DataFrame = pd.DataFrame(columns=["id", "title", "difficulty_id"])
# sentence_df: pd.DataFrame = pd.DataFrame(
#     columns=["id", "passage_id", "sequence", "sentence", "meaning", "tense"]
# )
# vocabulary_df: pd.DataFrame = pd.DataFrame(
#     columns=[
#         "id",
#         "sentence_id",
#         "vocabulary",
#         "definition",
#         "meaning",
#         "difficulty_id",
#         "pos",
#         "tag",
#         "lemma",
#         "dep",
#     ]
# )
# vocabulary_related_df: pd.DataFrame = pd.DataFrame(
#     columns=["vocabulary_id", "sentence_id"]
# )


def get_files(db: Session):
    return db.query(cms_models.FileCms).all()


def get_file_by_id(db: Session, file_id: int):
    return db.query(cms_models.FileCms).filter(cms_models.FileCms.id == file_id).first()


def get_file_by_name_extension(db: Session, filename: str, extension: str):
    return (
        db.query(cms_models.FileCms)
        .filter(cms_models.FileCms.filename == filename)
        .filter(cms_models.FileCms.extension == extension)
        .first()
    )


def get_file_by_process_status(db: Session, process_status: bool):
    return (
        db.query(cms_models.FileCms)
        .filter(cms_models.FileCms.process_status == process_status)
        .first()
    )


def create_file(db: Session, file_data: cms_schemas.FileCmsCreate):
    db_file = cms_models.FileCms(**file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def create_or_update_file(db: Session, file_data: cms_schemas.FileCmsCreate):
    if file_data.id:
        existing_file = get_file_by_id(db, file_data.id)
        if existing_file:
            for key, value in file_data.__dict__.items():
                setattr(existing_file, key, value)
            db.commit()
            db.refresh(existing_file)
            return existing_file
    return create_file(db, file_data)


def delete_file(db: Session, file_id: str):
    file = get_file_by_id(db, file_id)
    if file:
        db.delete(file)
        db.commit()
        os.remove(file.path)
        return file
    raise FileNotFoundError


async def upload(
    db: Session, category: cms_schemas.FileCategory, file: UploadFile = File(...)
):
    filename, file_extension = os.path.splitext(file.filename)
    existing_file = get_file_by_name_extension(db, filename, file_extension)
    if not existing_file:
        save_path = str(
            os.path.join(Config.origin_files_path, file_extension.lstrip("."))
        )
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, filename + file_extension)
        if not os.path.exists(file_path):
            try:
                with open(file_path, "wb") as f:
                    f.write(await file.read())
            except Exception as e:
                raise Exception(f"A problem occured during saving file: {file}")
            finally:
                upload_time = datetime.fromtimestamp(os.path.getctime(file_path))
                save_file = create_file(
                    db,
                    file_data={
                        "filename": filename,
                        "extension": file_extension,
                        "path": file_path,
                        "category": category,
                        "upload_at": upload_time,
                        "process_status": 0,
                    },
                )
                if save_file:
                    return save_file
    raise FileExists(f"This file is duplicated in the directory!")


def retrieve_passage_from_csv(db: Session, file_id: int):
    passage_id_list = []
    current_file = get_file_by_id(db, file_id)
    if current_file.process_status is not 1:
        source_df = pd.read_csv(current_file.path, encoding="iso-8859-1")
        for index, row in source_df.iterrows():
            if index < 1000:
                import re

                def filter_unsupported_characters(text):
                    pattern = re.compile(r"[^\x00-\x7F]")
                    filtered_text = re.sub(pattern, "", text)
                    return filtered_text

                filtered_text = filter_unsupported_characters(row["text"])

                level = ""
                if not math.isnan(row.get("level")):
                    level = level_service.get_level_by_name(db, row["level"].lower())

                save_passage = passage_cms_service.create_passage(
                    db,
                    passage_data={
                        "id": uuid.uuid4(),
                        "title": (row["title"] if "title" in source_df.columns else ""),
                        "text": filtered_text,
                        "process_status": 0,
                        "level_cms_id": (
                            level.id
                            if not math.isnan(row.get("standard")) and row["standard"] == level.proficiency_standard.name
                            else None
                        ),
                        "file_cms_id": file_id,
                        "transfer_status": 0,
                    },
                )
                passage_id_list.append(save_passage.id)
        current_file.process_status = 1
        create_or_update_file(db, current_file)
        return {"message": f"File ID: {file_id} processed successfully"}
    raise AlreadyProcessed(f"File ID: {file_id} have been processed")
