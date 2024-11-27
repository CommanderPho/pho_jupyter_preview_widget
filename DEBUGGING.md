# 2024-11-25 Errors
```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
File c:\Users\pho\repos\Spike3DWorkEnv\Spike3D\.venv\lib\site-packages\IPython\core\formatters.py:340, in BaseFormatter.__call__(self, obj)
    338     pass
    339 else:
--> 340     return printer(obj)
    341 # Finally look for special method names
    342 method = get_real_method(obj, self.print_method)

File ~\repos\Spike3DWorkEnv\pho_jupyter_preview_widget\pho_jupyter_preview_widget\display_helpers.py:561, in array_repr_with_graphical_preview.<locals>.<lambda>(arr)
    558 from pho_jupyter_preview_widget.display_helpers import array_preview_with_heatmap_repr_html
    560 # Register the custom display function for NumPy arrays
--> 561 ip.display_formatter.formatters['text/html'].for_type(np.ndarray, lambda arr: array_preview_with_heatmap_repr_html(arr, include_shape=include_shape, horizontal_layout=horizontal_layout, include_plaintext_repr=include_plaintext_repr, height=height, width=width))
    563 # ## Plain-text type representation can be suppressed like:
    564 if include_plaintext_repr:
    565     # Override text formatter to prevent plaintext representation
    566     ## SIDE-EFFECT: messes up printing NDARRAYs embedded in lists, dicts, other objects, etc. It seems that when rendering these they use the 'text/plain' representations

File ~\repos\Spike3DWorkEnv\pho_jupyter_preview_widget\pho_jupyter_preview_widget\display_helpers.py:454, in array_preview_with_heatmap_repr_html(arr, include_shape, horizontal_layout, include_plaintext_repr, **kwargs)
    450 if np.shape(arr)[0] > max_allowed_arr_elements: 
    451     # truncate 
    452     arr = arr[max_allowed_arr_elements:]
--> 454 heatmap_image = _subfn_display_heatmap(arr, **kwargs)
    455 if (heatmap_image is not None):
    456     orientation = "row" if horizontal_layout else "column"

File ~\repos\Spike3DWorkEnv\pho_jupyter_preview_widget\pho_jupyter_preview_widget\display_helpers.py:409, in _subfn_display_heatmap(data, brokenaxes_kwargs, **img_kwargs)
    405 """ Renders a small thumbnail Image of a heatmap array
    406 
    407 """
    408 img_kwargs = dict(width=None, height=img_kwargs.get('height', 100), format='png') | img_kwargs
--> 409 buf = _subfn_create_heatmap(data, brokenaxes_kwargs=brokenaxes_kwargs)
    410 if buf is not None:
    411     # Create an IPython Image object
    412     img = IPython.core.display.Image(data=buf.getvalue(), **img_kwargs) # IPython.core.display.Image

File ~\repos\Spike3DWorkEnv\pho_jupyter_preview_widget\pho_jupyter_preview_widget\display_helpers.py:385, in _subfn_create_heatmap(data, brokenaxes_kwargs)
    383 fig = plt.figure(figsize=(3, 3), num='_jup_backend')
    384 ax = fig.add_subplot(111)
--> 385 ax.imshow(data, cmap=active_cmap, **imshow_shared_kwargs)
    386 ax.axis('off')
    388 buf = BytesIO()

File c:\Users\pho\repos\Spike3DWorkEnv\Spike3D\.venv\lib\site-packages\matplotlib\__init__.py:1493, in _preprocess_data.<locals>.inner(ax, data, *args, **kwargs)
   1490 @functools.wraps(func)
   1491 def inner(ax, *args, data=None, **kwargs):
   1492     if data is None:
-> 1493         return func(ax, *map(sanitize_sequence, args), **kwargs)
   1495     bound = new_sig.bind(ax, *args, **kwargs)
   1496     auto_label = (bound.arguments.get(label_namer)
   1497                   or bound.kwargs.get(label_namer))

File c:\Users\pho\repos\Spike3DWorkEnv\Spike3D\.venv\lib\site-packages\matplotlib\axes\_axes.py:5759, in Axes.imshow(self, X, cmap, norm, aspect, interpolation, alpha, vmin, vmax, origin, extent, interpolation_stage, filternorm, filterrad, resample, url, **kwargs)
   5756 if aspect is not None:
   5757     self.set_aspect(aspect)
-> 5759 im.set_data(X)
   5760 im.set_alpha(alpha)
   5761 if im.get_clip_path() is None:
   5762     # image does not already have clipping set, clip to axes patch

File c:\Users\pho\repos\Spike3DWorkEnv\Spike3D\.venv\lib\site-packages\matplotlib\image.py:723, in _ImageBase.set_data(self, A)
    721 if isinstance(A, PIL.Image.Image):
    722     A = pil_to_array(A)  # Needed e.g. to apply png palette.
--> 723 self._A = self._normalize_image_array(A)
    724 self._imcache = None
    725 self.stale = True

File c:\Users\pho\repos\Spike3DWorkEnv\Spike3D\.venv\lib\site-packages\matplotlib\image.py:688, in _ImageBase._normalize_image_array(A)
    686 A = cbook.safe_masked_invalid(A, copy=True)
    687 if A.dtype != np.uint8 and not np.can_cast(A.dtype, float, "same_kind"):
--> 688     raise TypeError(f"Image data of dtype {A.dtype} cannot be "
    689                     f"converted to float")
    690 if A.ndim == 3 and A.shape[-1] == 1:
    691     A = A.squeeze(-1)  # If just (M, N, 1), assume scalar and apply colormap.

TypeError: Image data of dtype object cannot be converted to float

```

<!-- =============================================================================================================== -->
<!-- 2024-11-27 06:56 Issues with List[NDArray]                                                                      -->
<!-- =============================================================================================================== -->
```python
# For example the variable `split_most_likely_positions_arrays`
split_most_likely_positions_arrays = [np.array([119.191, 142.107, 180.3, 191.757, 245.227, 84.8181]), np.array([84.8181, 84.8181, 138.288]), np.array([134.469, 69.5411]), np.array([249.046]), np.array([249.046, 249.046])]
# is rendered as "[, , , , ]" (incorrect)
print(split_most_likely_positions_arrays) # [array([119.191, 142.107, 180.3, 191.757, 245.227, 84.8181]), array([84.8181, 84.8181, 138.288]), array([134.469, 69.5411]), array([249.046]), array([249.046, 249.046])]
type(split_most_likely_positions_arrays) # list
[type(v) for v in split_most_likely_positions_arrays] # [numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]
for v in split_most_likely_positions_arrays:
	display(v)
```


