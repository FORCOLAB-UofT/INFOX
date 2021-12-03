from flask_restful import Resource


class ImportRepositories(Resource):
    def get(self):
        # TODO: REPLACE FAKE DATA
        # TODO: add active forks, last updated, forks containing unmerged code
        return {
            "importRepositories": [
                {
                    "repo": "test/repo1",
                    "description": "test2 description1",
                    "language": "Python",
                    "timesForked": 1,
                },
                {
                    "repo": "test/repo2",
                    "description": "test description2",
                    "language": "JavaScript",
                    "timesForked": 2,
                },
                {
                    "repo": "test/repo3",
                    "description": "test description3",
                    "language": "Rust",
                    "timesForked": 3,
                },
                {
                    "repo": "test/repo4",
                    "description": "test description4",
                    "language": "C#",
                    "timesForked": 432,
                },
            ]
        }
