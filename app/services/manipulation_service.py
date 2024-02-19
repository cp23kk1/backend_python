import os
from app.services.english_service import EnglishService
import spacy
import pandas as pd
import nltk
import uuid
from app.config.resource import Config
from app.config.database.mysql import MySQL
import json
import shutil

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

config = Config.load_config()
english_service = EnglishService()

temp_value = "Temp"


class ManipulationService:

    passage_df: pd.DataFrame = pd.DataFrame(columns=["id", "title", "difficulty_id"])
    sentence_df: pd.DataFrame = pd.DataFrame(
        columns=["id", "passage_id", "sequence", "sentence", "meaning", "tense"]
    )
    vocabulary_df: pd.DataFrame = pd.DataFrame(
        columns=[
            "id",
            "sentence_id",
            "vocabulary",
            "definition",
            "meaning",
            "difficulty_id",
            "pos",
            "tag",
            "lemma",
            "dep",
        ]
    )
    vocabulary_related_df: pd.DataFrame = pd.DataFrame(
        columns=["vocabulary_id", "sentence_id"]
    )

    def convert_to_passage_df(self, passage_df: pd.DataFrame):
        try:
            result_df = pd.DataFrame()
            for index, row in passage_df.iterrows():
                result_df = result_df._append(
                    {
                        "id": uuid.uuid4(),
                        "title": (
                            row["title"]
                            if "title" in passage_df.columns
                            else temp_value
                        ),
                        # "difficulty_id": row["label"],
                        "difficulty_id": None,
                    },
                    ignore_index=True,
                )
        except Exception as error:
            raise error
        return result_df

    def convert_to_sentence_df(self, passage_id: str, sentences: str):
        try:
            result_df = pd.DataFrame()
            sentences = english_service.sentence_info(sentences)
            for key, value in sentences.items():
                result_df = result_df._append(
                    {
                        "id": uuid.uuid4(),
                        "passage_id": passage_id,
                        "sequence": int(key),
                        "sentence": value["sentence"],
                        "meaning": value["meaning"],
                        "tense": json.dumps(value["tense"]),
                    },
                    ignore_index=True,
                )
        except Exception as error:
            raise error
        return result_df

    def convert_to_vocabulary_df(self, sentence_id: str, sentence: str):
        try:
            result_df = pd.DataFrame()
            sentence = english_service.vocab_info(sentence)
            for key, value in sentence.items():
                if value["is_alpha"]:
                    result_df = result_df._append(
                        {
                            "id": uuid.uuid4(),
                            "sentence_id": sentence_id,
                            "vocabulary": value["vocabulary"],
                            "meaning": value["meaning"],
                            "definition": value["definition"],
                            "difficulty_id": None,
                            "pos": config.POS[value["pos"]],
                            "tag": config.POS_TAGS[value["tag"]],
                            "lemma": value["lemma"],
                            "dep": config.DEP[value["dep"]],
                        },
                        ignore_index=True,
                    )
        except Exception as error:
            raise error
        return result_df

    def convert_to_vocabulary_related_df(self, vocabulary_df: pd.DataFrame):
        try:
            result_df = pd.DataFrame()
            for index, row in vocabulary_df.iterrows():
                result_df = result_df._append(
                    {
                        "vocabulary_id": (
                            row["id"] if "id" in self.vocabulary_df.columns else ""
                        ),
                        "sentence_id": (
                            row["sentence_id"]
                            if "id" in self.vocabulary_df.columns
                            else ""
                        ),
                    },
                    ignore_index=True,
                )
        except Exception as error:
            raise error
        return result_df

    def convert_to_information_df(self):
        try:
            result_df = pd.DataFrame()
        except Exception as error:
            raise error
        return result_df

    def save_file(
        self,
        new_df: pd.DataFrame,
        filename: str,
        extension: str,
    ):
        try:
            save_path = os.path.join(config.computed_files_path, extension)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_abspath = os.path.join(
                config.computed_files_path,
                extension,
                f"{filename}.{extension}",
            )
            if os.path.exists(file_abspath):
                existing_df = pd.read_csv(file_abspath)
                new_df = existing_df._append(new_df, ignore_index=True)
            new_df.to_csv(file_abspath, index=False)
        except Exception as error:
            raise error
        return True

    def extract_csv(self, file_path: str):
        try:
            source_df = pd.read_csv(file_path)
            self.passage_df = self.convert_to_passage_df(source_df)
            for p_index, p_row in self.passage_df.iterrows():
                sentence_df = self.convert_to_sentence_df(
                    p_row["id"],
                    source_df.iloc[0]["text"],
                )
                self.sentence_df = self.sentence_df._append(
                    sentence_df,
                    ignore_index=True,
                )
                for s_index, s_row in sentence_df.iterrows():
                    vocabulary_df = self.convert_to_vocabulary_df(
                        s_row["id"], s_row["sentence"]
                    )
                    self.vocabulary_df = self.vocabulary_df._append(
                        vocabulary_df,
                        ignore_index=True,
                    )
                break

            print("-----------------------------------------------")
            # create vocabulary_related and drop from self.vocabulary_df
            self.vocabulary_related_df = self.convert_to_vocabulary_related_df(
                self.vocabulary_df
            )
            self.vocabulary_df.drop(columns=["sentence_id"], inplace=True)
            # Save passage
            self.save_file(self.passage_df, "passage", "csv")
            # Save sentence
            self.save_file(self.sentence_df, "sentence", "csv")
            # Save vocabulary
            self.save_file(self.vocabulary_df, "vocabulary", "csv")
            # Save vocabulary_related
            self.save_file(self.vocabulary_related_df, "vocabulary_related", "csv")
            completed_file_df = pd.DataFrame()
            if os.path.exists(config.computed_file_path):
                completed_file_df = pd.read_csv(config.computed_file_path)
            completed_file_df = completed_file_df._append(
                {
                    "id": uuid.uuid4(),
                    "file_path": file_path,
                    "passage_id": self.passage_df["id"].to_list(),
                    "sentence_id": self.sentence_df["id"].to_list(),
                    "vocabulary_id": self.vocabulary_df["id"].to_list(),
                },
                ignore_index=True,
            )
            completed_file_df.to_csv(
                config.computed_file_path,
                index=False,
            )
        except Exception as error:
            raise error
        return True

    def separate_by_category(self, file_path: str):
        try:
            if not os.path.exists(config.computed_files_path):
                os.makedirs(config.computed_files_path)
            if not os.path.exists(config.computed_file_path):
                pd.DataFrame(
                    columns=[
                        "id",
                        "file_path",
                        "passage_id",
                        "sentence_id",
                        "vocabulary_id",
                    ]
                ).to_csv(
                    config.computed_file_path,
                    index=False,
                )
                self.extract_csv(file_path)
            elif not (
                file_path
                in pd.read_csv(config.computed_file_path)["file_path"].to_list()
            ):
                self.extract_csv(file_path)
            else:
                print(0)
                return False
        except Exception as error:
            raise error
        return True

    def import_data(self, csv_file, table_name):
        try:
            df = pd.read_csv(csv_file)
            df.to_sql(
                table_name,
                MySQL.engine,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000,
            )
        except Exception:
            return False
        return True

    def import_data_from_csv(self, files_path: list[str]):
        for file in files_path:
            try:
                table_name = os.path.splitext(os.path.basename(file))[0]
                extension = os.path.splitext(os.path.basename(file))[1].lstrip(".")
                if not self.import_data(file, table_name):
                    raise Exception(f"Unsuccessfully import file: {file} to database!")
                else:
                    if not os.path.exists(config.dumped_files_path):
                        os.makedirs(os.path.join(config.dumped_files_path, extension))
                        dumped_file = os.path.join(
                            config.dumped_files_path, extension, os.path.basename(file)
                        )
                        if not os.path.exists(dumped_file):
                            shutil.move(
                                file,
                                dumped_file,
                            )
                        else:
                            computed_df = pd.read_csv(file)
                            dumped_df = pd.read_csv(dumped_file)
                            dumped_df = dumped_df._append(
                                computed_df, ignore_index=True
                            )
                            dumped_df.to_csv(
                                config.computed_file_path,
                                index=False,
                            )
            except Exception as error:
                # raise Exception(
                #     f"A problem occured during import data in file: {file} to database!"
                # )
                raise error
        return True
