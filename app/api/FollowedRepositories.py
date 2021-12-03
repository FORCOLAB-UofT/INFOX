from flask_restful import Resource


class FollowedRepositories(Resource):
    def get(self):
        # TODO: replace fake data with real user data, code to get followed repositories should be in views.py at /index
        return {
            "followedRepositories": [
                {
                    "repo": "test/repo1",
                    "description": "test2 description1",
                    "language": "python",
                    "timesForked": 1,
                    "updated": "2021-11-26 04:06(UTC)",
                },
                {
                    "repo": "test/repo2",
                    "description": "test description2",
                    "language": "javascript",
                    "timesForked": 2,
                    "updated": "2021-11-26 04:06(UTC)",
                },
                {
                    "repo": "test/repo3",
                    "description": "test description3",
                    "language": "java",
                    "timesForked": 3,
                    "updated": "2021-11-26 04:06(UTC)",
                },
                {
                    "repo": "test/repo4",
                    "description": "test description4",
                    "language": "rust",
                    "timesForked": 4,
                    "updated": "2021-11-26 04:06(UTC)",
                },
                {
                    "repo": "test/repo5",
                    "description": "test description5",
                    "language": "python",
                    "timesForked": 5,
                    "updated": "2021-11-26 04:06(UTC)",
                },
            ]
        }
