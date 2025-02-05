from enum import Enum

class Image2VideoModelType(str, Enum):
    """
    Enum class for image2video model type.
    """
    REPLICATE = "Replicate"
    STABILITY = "Stability"
