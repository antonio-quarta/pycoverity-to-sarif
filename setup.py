from pathlib import Path

from setuptools import setup


readme = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="coverity-scan-results-to-sarif",
    version="1.0.0",
    description="Convert Coverity JSON results to SARIF 2.1.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="GPL-3.0-only",
    packages=["coverity_sarif"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "coverity-to-sarif=coverity_sarif.cli:main",
        ],
    },
)