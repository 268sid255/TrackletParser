# Tracklet-Parser

[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/268sid255/TrackletParser/blob/main/LICENSE.txt)
[![python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/downloads/)

 Tracklet Parser - a parser for tracklet labels in KITTI Raw Format 1.0 created by the [Computer Vision Annotation Tool (CVAT)](https://github.com/openvinotoolkit/cvat). <br> Based https://github.com/holtvogt/tracklet_parser

## Installation and Usage

1) Install poetry
```python
pipx install poetry
```
2) Initialize the virtual environment
```python
poetry install
```
3) Add tracklet_labels.xml and frame_list.txt to the labels folder and run the script
```python
poetry run tracklet-run
```

