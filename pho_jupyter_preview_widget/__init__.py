# Import and expose key functionality
from . import display_helpers
from . import ipython_helpers
from . import widget


# from .display_helpers import array_repr_with_graphical_preview
# from .array_shape_display import array_repr_html

# Define version
__version__ = "0.3.1"

# You can also define __all__ to control what gets imported with "from package import *"
# __all__ = ['array_repr_with_graphical_preview', 'array_repr_html']

# Define what gets imported with "from package import *"
__all__ = [
    'display_helpers',
    'ipython_helpers',
    'widget',
]