import unittest

from ..xafsdb_web.utils import term_checker


class TestTermChecker(unittest.TestCase):
    def test_term_checker(self):
        # Setup
        datasetList = []
        dataset = {
            "datasetName": "Sample Dataset",
            "ownerGroup": "Group1",
            "owner": "OwnerName",
            "contactEmail": "contact@example.com",
            "updatedBy": "UpdaterName",
            "scientificMetadata": {
                "Description": "A detailed description",
                "Data": {"Source": "Synchrotron", "Measurement": "X-ray"},
                "instrument": {"facility": "LHC", "beamline": "ATLAS"},
            },
            "history": [
                {
                    "updatedscientificMetadata": {
                        "Description": "Updated description",
                        "Data": {"Source": "Lab", "Measurement": "Neutron"},
                    }
                }
            ],
        }

        # Test with term present in updated history metadata
        term_checker(dataset, "neutron", datasetList)
        self.assertEqual(
            len(datasetList),
            1,
            "The dataset should be found when term is in updated history metadata",
        )

        # Test with term present in current scientific metadata
        datasetList.clear()
        term_checker(dataset, "x-ray", datasetList)
        self.assertEqual(
            len(datasetList),
            1,
            "The dataset should be found when term is in current scientific metadata",
        )

        # Test with term present in top-level attributes
        datasetList.clear()
        term_checker(dataset, "sample", datasetList)
        self.assertEqual(
            len(datasetList),
            1,
            "The dataset should be found when term is in datasetName",
        )

        # Test with term not present
        datasetList.clear()
        term_checker(dataset, "unrelated", datasetList)
        self.assertEqual(
            len(datasetList),
            0,
            "The dataset should not be found when term is unrelated",
        )


# Run the tests
if __name__ == "__main__":
    unittest.main()
