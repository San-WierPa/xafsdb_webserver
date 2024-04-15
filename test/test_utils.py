import unittest
from xafsdb_web.utils import term_checker

class TestTermChecker(unittest.TestCase):

    def setUp(self):
        self.dataset_sample = {
            "_id": 'PID.SAMPLE.PREFIX787acf5e-974f-4302-8bd6-861d939c2939',
            "principalInvestigator": 'someone',
            "creationLocation": 'wuppertal',
            "scientificMetadata": {
                "Description": '',
                "Data": {
                    "Source": 'SYNCHROTRON',
                    "Mode": 'Absorption'
                },
                "RAW": {
                    "edge_step": {
                        "value": 0,
                        "unit": 'a.u.',
                        "documentation": 'Height of the detected edge step.',
                        "valueSI": 0,
                        "unitSI": 'a.u.'
                    },
                    "k_max": {
                        "value": 0,
                        "unit": 'Å⁻¹',
                        "documentation": 'Considered angular wavenumber.',
                        "valueSI": 0,
                        "unitSI": 'Å⁻¹'
                    }
                },
                "PROCESSED": {
                    "amplitude_reduction_factor": {
                        "Z_ranges": {
                            "tentoforty": {
                                "value": 0
                            },
                            "fortytoeighty": {
                                "value": 0
                            }
                        },
                        "unit": 'a.u.',
                        "documentation": 'amplitude factor from the processed spectrum'
                    }
                }
            },
            "ownerGroup": 'ResearchGroup1',
            "owner": 'ResearchOwner1',
            "contactEmail": 'research_owner1@example.com',
            "datasetName": 'Ni_foil_Ni_K_300_1.xdi 2023-09-06-17_37_43',
            "isPublished": False
        }

    def test_term_checker(self):
        datasetList = []

        # Test case 1: Search term found in datasetName
        term_checker(self.dataset_sample, '300_1.xdi', datasetList)
        self.assertEqual(len(datasetList), 1)

        datasetList.clear()

        # Test case 2: Search term found in ownerGroup
        term_checker(self.dataset_sample, 'ResearchGroup1', datasetList)
        self.assertEqual(len(datasetList), 1)

        datasetList.clear()

        # Test case 3: Search term not found
        term_checker(self.dataset_sample, 'nonexistent', datasetList)
        self.assertEqual(len(datasetList), 0)


if __name__ == '__main__':
    unittest.main()
