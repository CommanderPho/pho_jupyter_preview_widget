# Provides Data Previews for many common data types, such as Numpy Arrays and Pandas Dataframes

# Usage
Use a jupyter-lab notebook like below:
```python
from pho_jupyter_preview_widget.display_helpers import array_repr_with_graphical_preview
from pho_jupyter_preview_widget.ipython_helpers import PreviewWidgetMagics

ip = get_ipython()

# Register the magic
ip.register_magics(PreviewWidgetMagics)


# from pyphocorehelpers.ipython_helpers import MyMagics

# %config_ndarray_preview width=500

# Register the custom display function for NumPy arrays
# ip.display_formatter.formatters['text/html'].for_type(np.ndarray, lambda arr: array_preview_with_graphical_shape_repr_html(arr))
# ip = array_repr_with_graphical_shape(ip=ip)
ip = array_repr_with_graphical_preview(ip=ip)
# ip = dataframe_show_more_button(ip=ip)
```

