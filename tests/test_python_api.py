import os
import tarfile
import unittest
import urllib.request
from pathlib import Path

from stl_to_h5m import stl_to_h5m
import dagmc_h5m_file_inspector as di


class TestApiUsage(unittest.TestCase):
    """Test usage cases"""

    def test_h5m_file_creation_and_contents(self):
        """Checks that a h5m file is created from a single stl file"""

        test_h5m_filename = "test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = stl_to_h5m(
            files_with_tags=[("tests/part2.stl", "mat1")],
            h5m_filename=test_h5m_filename,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename
        assert di.get_volumes_from_h5m(test_h5m_filename) == [1]
        assert di.get_materials_from_h5m(test_h5m_filename) == ["mat1"]
        assert di.get_volumes_and_materials_from_h5m(test_h5m_filename) == {1: "mat1"}

    def test_h5m_file_creation_and_contents_in_subfolder(self):
        """Checks that a h5m file is created in a subfolder from a single stl
        file"""

        test_h5m_filename = "subfolder/test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = stl_to_h5m(
            files_with_tags=[("tests/part1.stl", "mat1")],
            h5m_filename=test_h5m_filename,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename
        assert di.get_volumes_from_h5m(test_h5m_filename) == [1]
        assert di.get_materials_from_h5m(test_h5m_filename) == ["mat1"]
        assert di.get_volumes_and_materials_from_h5m(test_h5m_filename) == {1: "mat1"}

    def test_h5m_file_creation_and_contents_from_multiple_h5m_files(self):
        """Checks that a h5m file is created from multiple stl files"""

        test_h5m_filename = "subfolder/test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = stl_to_h5m(
            files_with_tags=[("tests/part1.stl", "mat1"), ("tests/part2.stl", "mat2")],
            h5m_filename=test_h5m_filename,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename
        assert di.get_volumes_from_h5m(test_h5m_filename) == [1, 2]
        assert di.get_materials_from_h5m(test_h5m_filename) == ["mat1", "mat2"]
        assert di.get_volumes_and_materials_from_h5m(test_h5m_filename) == {
            1: "mat1",
            2: "mat2",
        }
