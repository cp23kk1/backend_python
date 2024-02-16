import codecs
import csv
import fitz
import os
from typing import List
from http import HTTPStatus
from app.services.english_service import EnglishService
from common.response_message import Result, Error
import spacy
from spacy.language import Language
import re
import pandas as pd
from fastapi import File, UploadFile
import nltk
import pandas as pd
import uuid
from app.config import constant

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

english_service = EnglishService()


class ExtractService:

    passage_df: pd.DataFrame = pd.DataFrame(columns=["id", "title", "level"])
    sentence_df: pd.DataFrame = pd.DataFrame(
        columns=["id", "passage_id", "sequence", "sentence", "meaning", "tense"]
    )
    vocabulary_df: pd.DataFrame = pd.DataFrame(
        columns=[
            "id",
            "sentence_id",
            "vocabulary",
            "meaning",
            "difficulty",
            "pos",
            "tag",
            "lemma",
            "dep",
        ]
    )

    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        text = ""

        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()

        doc.close()
        return text

    @Language.component("custom_sentence_boundary")
    def custom_sentence_boundary(doc):
        for token in doc[:-1]:
            # If a period is followed by a token with an initial uppercase letter, don't split
            if token.text == "." and doc[token.i + 1].is_title:
                doc[token.i + 1].is_sent_start = False
        return doc

    def sentence_tokenize(self, pdf_path):
        # Download the spaCy model 'en_core_web_sm' if not already installed
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            spacy.cli.download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")

        # Add the custom sentence boundary detection component
        nlp.add_pipe(
            "custom_sentence_boundary", name="custom_sentence_boundary", before="parser"
        )

        # Extract text from the PDF using PyMuPDF
        text = self.extract_text_from_pdf(pdf_path)

        # Exclude lines starting with "chapter"
        lines = [
            line.strip()
            for line in text.split("\n")
            if not (
                line.lower().startswith("chapter")
                or "http" in line.lower()
                or re.match("^[0-9\\s\\W]+$", line)
            )
        ]

        # Process the text using SpaCy
        doc = nlp(" ".join(lines))

        # num_sentences = len(list(doc.sents))
        # Extract sentences
        sentences = [sent.text.strip() for sent in doc.sents]
        print(sentences)
        return ""

    def extract_text(
        self, source_path: str, destination_path: str, extension: str
    ) -> Result:
        source_path = os.path.abspath(source_path)
        destination_path = os.path.abspath(destination_path)

        if (extension in destination_path) == False:
            return Result(
                [],
                Error(
                    status_code=HTTPStatus.BAD_REQUEST,
                    error={
                        "Error": f"Directory: {source_path} and Extension: {extension} is not match!"
                    },
                ),
            )
        if not os.path.exists(source_path):
            return Result(
                [],
                Error(
                    status_code=HTTPStatus.NOT_FOUND,
                    error={"Error": f"Directory: {destination_path} does not exist!"},
                ),
            )
        if not os.path.exists(destination_path):
            return Result(
                [],
                Error(
                    status_code=HTTPStatus.NOT_FOUND,
                    error={"Error": f"Directory: {destination_path} does not exist!"},
                ),
            )

        file_names_arr: List[str] = os.listdir(source_path)

        count_check = 0
        for i in range(len(file_names_arr)):
            file_path = os.path.join(source_path, file_names_arr[i])
            file_name = os.path.splitext(file_names_arr[i])[0]
            output_file_path = (
                f"{os.path.join(destination_path, file_name)}.{extension}"
            )

            # extracted_text = self.sentence_tokenize(file_path)
            self.sentence_tokenize(file_path)
            count_check += 1
            # with open(output_file_path, 'w', encoding='utf-8') as output_file:
            #     output_file.write(extracted_text)

        if not (len(file_names_arr) == count_check):
            return Result(
                [],
                Error(
                    status_code=HTTPStatus.BAD_REQUEST,
                    error={"Error": f"Error occurs during processiong!"},
                ),
            )
        else:
            return Result(result=[])

    def convert_to_passage_df(self, passage_df: pd.DataFrame):
        result_df = pd.DataFrame()
        for index, row in passage_df.iterrows():
            result_df = result_df._append(
                {
                    "id": uuid.uuid4(),
                    "title": row["title"] if "title" in passage_df.columns else "",
                    "level": row["label"],
                },
                ignore_index=True,
            )
        return result_df

    def convert_to_sentence_df(self, passage_id: str, sentences: str):
        result_df = pd.DataFrame()
        sentences = english_service.sentence_info(sentences)
        for key, value in sentences.items():
            result_df = result_df._append(
                {
                    "id": uuid.uuid4(),
                    "passage_id": passage_id,
                    "sequence": int(key),
                    "sentence": value["sentence"],
                    "meaning": "",
                    "tense": value["tense"],
                },
                ignore_index=True,
            )
        return result_df

    def convert_to_vocabulary_df(self, sentence_id: str, sentence: str):
        result_df = pd.DataFrame()
        sentence = english_service.vocab_info(sentence)
        for key, value in sentence.items():
            if value["is_alpha"]:
                result_df = result_df._append(
                    {
                        "id": uuid.uuid4(),
                        "sentence_id": sentence_id,
                        "vocabulary": value["vocabulary"],
                        "meaning": "",
                        "difficulty": "",
                        "pos": value["pos"],
                        "tag": value["tag"],
                        "lemma": value["lemma"],
                        "dep": value["dep"],
                    },
                    ignore_index=True,
                )
        return result_df

    def save_file(
        self,
        new_df: pd.DataFrame,
        filename: str,
        extension: str,
    ):
        file_abspath = os.path.join(
            os.path.abspath(constant.datasources_path),
            extension,
            f"{filename}.{extension}",
        )
        if os.path.exists(file_abspath):
            existing_df = pd.read_csv(file_abspath)
            new_df = existing_df._append(new_df, ignore_index=True)
        new_df.to_csv(file_abspath, index=False)

    def separate_by_category(self, file_path: str):
        if not os.path.exists(constant.completed_file_path):
            pd.DataFrame(
                columns=["id", "file_path", "passage_id" "sentence_id", "vocabulary_id"]
            ).to_csv(
                constant.completed_file_path,
                index=False,
            )
        elif (
            not file_path
            in pd.read_csv(constant.completed_file_path)["file_path"].to_list()
        ):
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
            # Save passage
            self.save_file(self.passage_df, "passage", "csv")
            # Save sentence
            self.save_file(self.sentence_df, "sentence", "csv")
            # Save vocabulary
            self.save_file(self.vocabulary_df, "vocabulary", "csv")
            completed_file_df = pd.DataFrame()
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
                constant.completed_file_path,
                index=False,
            )
        else:
            return "Have computed this file!"
        return "finish!"
