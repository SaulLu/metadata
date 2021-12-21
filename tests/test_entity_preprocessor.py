import unittest

from datasets import Dataset

from bsmetadata.preprocessing_utils import EntityPreprocessor


class TestEntityPreprocessor(unittest.TestCase):
    def test_extract_entities(self):

        my_dict = {
            "text": [
                "Paris is the beautiful place to visit",
                "This Friday, Obama and Merkel will be meeting to discuss on issues related to climate change",
                "Bieber performed at the concert last night",
                "Paris is the beautiful place to visit",
                "He was playing a game",
            ],
            "metadata": [[], [], [], [], []],
        }  # toy dataset


        target_text = [
            "Paris is the beautiful place to visit",
            "This Friday, Obama and Merkel will be meeting to discuss on issues related to climate change",
            "Bieber performed at the concert last night",
            "Paris is the beautiful place to visit",
            "He was playing a game",
        ]

        target_metadata = [
            [
                {
                    "char_end_idx": 5,
                    "char_start_idx": 0,
                    "ent_desc": "Paris  is the capital and most populous city of France, with an estimated population of 2,175,601 residents , in an area of more than .",
                    "key": "entity",
                    "type": "local",
                    "value": "Paris",
                }
            ],
            [
                {
                    "char_end_idx": 18,
                    "char_start_idx": 13,
                    "ent_desc": "Barack Hussein Obama II  is an American politician, author, and retired attorney who served as the 44th president of the United States from 2009 to 2017.",
                    "key": "entity",
                    "type": "local",
                    "value": "Barack_Obama",
                },
                {
                    "char_end_idx": 29,
                    "char_start_idx": 23,
                    "ent_desc": "Angela Dorothea Merkel  MdB  is a German politician serving as the chancellor of Germany since 2005.",
                    "key": "entity",
                    "type": "local",
                    "value": "Angela_Merkel",
                },
            ],
            [
                {
                    "char_end_idx": 6,
                    "char_start_idx": 0,
                    "ent_desc": "Justin Drew Bieber  is a Canadian singer.",
                    "key": "entity",
                    "type": "local",
                    "value": "Justin_Bieber",
                }
            ],
            [
                {
                    "char_end_idx": 5,
                    "char_start_idx": 0,
                    "ent_desc": "Paris  is the capital and most populous city of France, with an estimated population of 2,175,601 residents , in an area of more than .",
                    "key": "entity",
                    "type": "local",
                    "value": "Paris",
                }
            ],
            [],
        ]
        processor = EntityPreprocessor(
            base_url="/gpfsssd/scratch/rech/six/uue59kq/modeling-metadata-artefacts/entity_preprocessing",
            path_wiki_db="/gpfsscratch/rech/six/uue59kq/modeling-metadata-artefacts/wiki_en_dump.db",
            path_or_url_flair_ner_model="/gpfsscratch/rech/six/uue59kq/cache_dir/flair/ner-fast/en-ner-fast-conll03-v0.4.pt",
        )

        ds = Dataset.from_dict(my_dict)
        ds = ds.map(lambda ex: processor.preprocess(ex), batched=True, batch_size=3)

        self.assertEqual(ds[:]["text"], target_text)
        self.assertEqual(ds[:]["metadata"], target_metadata)

if __name__ == "__main__":
    unittest.main()
