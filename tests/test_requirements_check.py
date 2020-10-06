import pytest
import subprocess


def test_requirements_dvd_info_not_in_path():
    with pytest.raises(FileNotFoundError):
        result = subprocess.run(['dvd_info', '--version'], capture_output=True, text=True)

def test_requirements_handbrakecli_in_path():
    result = subprocess.run(['HandBrakeCLI', '--version'], capture_output=True, text=True)
    assert result

