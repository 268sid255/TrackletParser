from copy import deepcopy
from typing import Dict

class Tracklet:
    _frame_number: int
    _type: str
    _truncated: float
    _occluded: int
    _alpha: float
    _bbox: Dict[str, float]
    _dimensions: Dict[str, float]
    _location: Dict[str, float]
    _rotation_z: float

    def __init__(self) -> None:
        self._frame_number = -1
        self._type = ''
        self._truncated = 0.0
        self._occluded = 0
        self._alpha = 0.0
        self._bbox = {'left': 0.0, 'top': 0.0, 'right': 0.0, 'bottom': 0.0}
        self._dimensions = {'height': 0.0, 'width': 0.0, 'length': 0.0}
        self._location = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        self._rotation_z = 0.0
    
    @property
    def frame_number(self) -> int:
        return self._frame_number
    
    @property
    def type(self) -> str:
        return self._type
    
    @property
    def truncated(self) -> float:
        return self._truncated
    
    @property
    def occluded(self) -> int:
        return self._occluded
    
    @property
    def alpha(self) -> float:
        return self._alpha
    
    @property
    def bbox(self) -> Dict[str, float]:
        return deepcopy(self._bbox)
    
    @property
    def dimensions(self) -> Dict[str, float]:
        return deepcopy(self._dimensions)
    
    @property
    def location(self) -> Dict[str, float]:
        return deepcopy(self._location)
    
    @property
    def rotation_z(self) -> float:
        return self._rotation_z
    
    def set_frame_number(self, frame_number: int):
        self._frame_number = frame_number

    def set_type(self, object_type: str):
        self._type = object_type
    
    def set_truncated(self, truncated: float):
        if not 0 <= truncated <= 1:
            raise ValueError(f'{truncated} is an unknown truncation representative.')
        self._truncated = truncated
    
    def set_occluded(self, occluded: int):
        if not 0 <= occluded <= 3:
            raise ValueError(f'{occluded} is an unknown occlusion representative.')
    
    def set_alpha(self, alpha: float):
        self._alpha = alpha
    
    def set_bbox(self, key: str, value: float):
        self._bbox[key] = value
    
    def set_dimensions(self, key: str, value: float):
        self._dimensions[key] = value
    
    def set_location(self, key: str, value: float):
        self._location[key] = value
    
    def set_rotation_z(self, rotation_z: float):
        self._rotation_z = rotation_z