import unittest

from analysis_cli import cli as analysis_cli
from transform_cli import cli as transform_cli


class NewCliSmokeTests(unittest.TestCase):
    def test_analysis_workflows_non_empty(self) -> None:
        self.assertTrue(analysis_cli.ANALYSIS_SCRIPTS)

    def test_transform_parser_builds(self) -> None:
        parser = transform_cli._build_parser()
        self.assertIsNotNone(parser)


if __name__ == "__main__":
    unittest.main()
