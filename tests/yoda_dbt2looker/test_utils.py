import pytest
import json
import yaml
from pathlib import Path
from unittest.mock import mock_open, patch
from yoda_dbt2looker import utils


class TestUtils:
    @pytest.fixture
    def mock_manifest(self):
        return {
            "metadata": {
                "dbt_schema_version": "https://schemas.getdbt.com/dbt/manifest/v1.json"
            },
            "nodes": {}
        }

    @pytest.fixture
    def mock_dbt_project(self):
        return {
            "name": "test_project",
            "version": "1.0.0"
        }

    @patch("pathlib.Path.open", new_callable=mock_open, read_data=json.dumps({"key": "value"}))
    def test_load_json_file(self, mock_file):
        result = utils.load_json_file(Path("dummy_path.json"))
        assert result == {"key": "value"}

    @patch("pathlib.Path.open", new_callable=mock_open, read_data=yaml.dump({"key": "value"}))
    def test_load_yaml_file(self, mock_file):
        result = utils.load_yaml_file(Path("dummy_path.yml"))
        assert result == {"key": "value"}

    @patch("yoda_dbt2looker.utils.load_json_file")
    @patch("yoda_dbt2looker.parser.validate_manifest")
    def test_get_manifest(self, mock_validate_manifest, mock_load_json_file, mock_manifest):
        mock_load_json_file.return_value = mock_manifest
        result = utils.get_manifest("dummy_prefix")
        assert result == mock_manifest

    @patch("yoda_dbt2looker.utils.load_yaml_file")
    def test_get_dbt_project_config(self, mock_load_yaml_file, mock_dbt_project):
        mock_load_yaml_file.return_value = mock_dbt_project
        result = utils.get_dbt_project_config("dummy_prefix")
        assert result == mock_dbt_project

    @patch("pathlib.Path.open", side_effect=FileNotFoundError)
    def test_load_json_file_not_found(self, mock_file):
        with pytest.raises(SystemExit):
            utils.load_json_file(Path("dummy_path.json"))

    @patch("pathlib.Path.open", side_effect=FileNotFoundError)
    def test_load_yaml_file_not_found(self, mock_file):
        with pytest.raises(SystemExit):
            utils.load_yaml_file(Path("dummy_path.yml"))

    @patch("yoda_dbt2looker.utils.load_json_file", side_effect=SystemExit)
    def test_get_manifest_file_not_found(self, mock_load_json_file):
        with pytest.raises(SystemExit):
            utils.get_manifest("dummy_prefix")

    @patch("yoda_dbt2looker.utils.load_yaml_file", side_effect=SystemExit)
    def test_get_dbt_project_config_file_not_found(self, mock_load_yaml_file):
        with pytest.raises(SystemExit):
            utils.get_dbt_project_config("dummy_prefix")
