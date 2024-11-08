from copy import deepcopy
from typing import Dict, List, Tuple, Optional, Callable, Union, Any, NewType, TypeVar
import IPython
import IPython.display
from typing_extensions import TypeAlias
from nptyping import NDArray

import numpy as np
import pandas as pd
import dask.array as da

import ipykernel # ip: "ipykernel.zmqshell.ZMQInteractiveShell)" = IPython.get_ipython()
from IPython.display import display, HTML, Javascript
from ipywidgets import widgets, VBox, HBox

from io import BytesIO
import base64


import matplotlib.pyplot as plt


# ==================================================================================================================== #
# 2024-05-30 - Custom Formatters                                                                                       #
# ==================================================================================================================== #

def render_scrollable_colored_table_from_dataframe(df: pd.DataFrame, cmap_name: str = 'viridis', max_height: int = 400, width: str = '100%', is_dark_mode: bool=True, **kwargs) -> Union[HTML, str]:
    """ Takes a numpy array of values and returns a scrollable and color-coded table rendition of it

    Usage:    
        from pho_jupyter_preview_widget.pho_jupyter_preview_widget.display_helpers import render_scrollable_colored_table

        # Example usage:

        # Example 2D NumPy array
        array = np.random.rand(100, 10)
        # Draw it
        render_scrollable_colored_table(array)
        
        # Example 2:
			render_scrollable_colored_table(np.random.rand(100, 10), cmap_name='plasma', max_height=500, width='80%')

    """
    # Validate input array
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a DataFrame array.")
        
    # Validate colormap name
    if cmap_name is not None:
        if cmap_name not in plt.colormaps():
            raise ValueError(f"Invalid colormap name '{cmap_name}'. Use one of: {', '.join(plt.colormaps())}.")
    
    # Convert the array to a Pandas DataFrame

    ## Normalize each column to the 0, 1 range or ignore formatting
    # Normalize the data to [0, 1] range
    # normalized_df = (df - df.min().min()) / (df.max().max() - df.min().min())
    
    normalized_df = deepcopy(df)
    
    # Function to calculate luminance and return appropriate text color
    def text_contrast(rgba):
        r, g, b, a = rgba[:4]
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return 'black' if luminance > 0.5 else 'white'

    # Define a function to apply a colormap and text color based on luminance
    def color_map(val):
        use_default_formatting = True
        cmap = None
        if cmap_name is not None:
            cmap = plt.get_cmap(cmap_name)  # Use the provided colormap
        
        try:
            color = cmap(val)
            text_color = text_contrast(color)
            use_default_formatting = False
        except TypeError as e:
            ## Not formattable, return default text color (white)
            use_default_formatting = True
        except Exception as e:
            raise e
        
        if use_default_formatting:
            if is_dark_mode:
                color = 'black'
                text_color = 'white'
            else:
                color = 'white'
                text_color = 'black'

        return f'background-color: rgba({color[0]*255}, {color[1]*255}, {color[2]*255}, {color[3]}); color: {text_color}'

    # Apply the color map with contrast adjustment
    styled_df = normalized_df.style.applymap(color_map)
    formatted_table = styled_df.set_table_attributes(f'style="display:block;overflow-x:auto;max-height:{max_height}px;width:{width};border-collapse:collapse;"').render()
    # Render the DataFrame as a scrollable table with color-coded values
    scrollable_table = HTML(formatted_table)

    return scrollable_table


# @function_attributes(short_name=None, tags=['table', 'scrollable'], input_requires=[], output_provides=[], uses=[], used_by=[], creation_date='2024-10-25 19:12', related_items=[])
def render_scrollable_colored_table(array: NDArray, cmap_name: str = 'viridis', max_height: int = 400, width: str = '100%', **kwargs) -> Union[HTML, str]:
    """ Takes a numpy array of values and returns a scrollable and color-coded table rendition of it

    Usage:    
        from pho_jupyter_preview_widget.pho_jupyter_preview_widget.display_helpers import render_scrollable_colored_table

        # Example usage:

        # Example 2D NumPy array
        array = np.random.rand(100, 10)
        # Draw it
        render_scrollable_colored_table(array)
        
        # Example 2:
			render_scrollable_colored_table(np.random.rand(100, 10), cmap_name='plasma', max_height=500, width='80%')

    """
    # Validate input array
    if not isinstance(array, np.ndarray):
        raise TypeError("Input must be a NumPy array.")
    
    if array.ndim != 2:
        raise ValueError("Input array must be 2D.")
        
    # Convert the array to a Pandas DataFrame
    df = pd.DataFrame(array)

    # Normalize the data to [0, 1] range
    normalized_df = (df - df.min().min()) / (df.max().max() - df.min().min())

    return render_scrollable_colored_table_from_dataframe(df=normalized_df, cmap_name=cmap_name, max_height=max_height, width=width, **kwargs)
    

    

    
    
def array_preview_with_shape(arr):
    """ Text-only Represntation that prints np.shape(arr) 
    
        from pho_jupyter_preview_widget.display_helpers import array_preview_with_shape

        # Register the custom display function for numpy arrays
        import IPython
        ip = IPython.get_ipython()
        ip.display_formatter.formatters['text/html'].for_type(np.ndarray, array_preview_with_shape) # only registers for NDArray

        # Example usage
        arr = np.random.rand(3, 4)
        display(arr)

    """
    if isinstance(arr, np.ndarray):
        display(HTML(f"<pre>array{arr.shape} of dtype {arr.dtype}</pre>"))
    elif isinstance(arr, (list, tuple)):
        display(HTML(f"<pre>native-python list {len(arr)}</pre>"))
    elif isinstance(arr, pd.DataFrame):
        display(HTML(f"<pre>DataFrame with {len(arr)} rows and {len(arr.columns)} columns</pre>"))
    else:
        raise ValueError("The input is not a NumPy array.")


def array_preview_with_graphical_shape_repr_html(arr):
    """Generate an HTML representation for a NumPy array, similar to Dask.
        
    from pho_jupyter_preview_widget.display_helpers import array_preview_with_graphical_shape_repr_html
    
    # Register the custom display function for NumPy arrays
    import IPython
    ip = IPython.get_ipython()
    ip.display_formatter.formatters['text/html'].for_type(np.ndarray, lambda arr: array_preview_with_graphical_shape_repr_html(arr))

    # Example usage
    arr = np.random.rand(3, 4)
    display(arr)


    arr = np.random.rand(9, 64)
    display(arr)

    arr = np.random.rand(9, 64, 4)
    display(arr)

    """
    if isinstance(arr, np.ndarray):
        arr = da.array(arr)
        return display(arr)
        # shape_str = ' &times; '.join(map(str, arr.shape))
        # dtype_str = arr.dtype
        # return f"<pre>array[{shape_str}] dtype={dtype_str}</pre>"
    else:
        raise ValueError("The input is not a NumPy array.")



# Generate heatmap
class MatplotlibToIPythonWidget:
    """ 
    
    from pho_jupyter_preview_widget.display_helpers import MatplotlibToIPythonWidget
    
    MatplotlibToIPythonWidget.matplotlib_fig_to_ipython_HTML(fig=fig)
    
    """
    @classmethod
    def _matplotlib_fig_to_bytes(cls, fig) -> Optional[BytesIO]: # , omission_indices: list = None
        """ 
        
        #TODO 2024-08-16 04:05: - [ ] Make non-interactive and open in the background

        from neuropy.utils.matplotlib_helpers import matplotlib_configuration
        with matplotlib_configuration(is_interactive=False, backend='AGG'):
            # Perform non-interactive Matplotlib operations with 'AGG' backend
            plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('Non-interactive Mode with AGG Backend')
            plt.savefig('plot.png')  # Save the plot to a file (non-interactive mode)

                
        import matplotlib
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        _bak_rcParams = mpl.rcParams.copy()

        matplotlib.use('Qt5Agg')
        # %matplotlib inline
        # %matplotlib auto


        # _restore_previous_matplotlib_settings_callback = matplotlib_configuration_update(is_interactive=True, backend='Qt5Agg')
        _restore_previous_matplotlib_settings_callback = matplotlib_configuration_update(is_interactive=True, backend='Qt5Agg')

            
        """
        try:                
            buf = BytesIO()            
            fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)
        except BaseException as err:
            # SystemError: tile cannot extend outside image
            print(f'ERROR: Encountered error while convert matplotlib fig: {fig} to bytes:\n\terr: {err}')
            buf = None
        # finally:
        #     plt.close()        
        
        return buf


    @classmethod
    def matplotlib_fig_to_ipython_img(cls, fig, **img_kwargs) -> Optional[widgets.Image]:
        img_kwargs = dict(width=None, height=img_kwargs.get('height', 100), format='png') | img_kwargs
        buf = cls._matplotlib_fig_to_bytes(fig)
        if buf is not None:
            # Create an IPython Image object
            img = widgets.Image(data=buf.getvalue(), **img_kwargs)
            return img
        else:
            return None
    

    # Convert to ipywidgets Image
    @classmethod
    def matplotlib_fig_to_ipython_HTML(cls, fig, horizontal_layout=True, **kwargs) -> str:
        """ Generate an HTML representation for a NumPy array with a Dask shape preview and a thumbnail heatmap
        
            from pho_jupyter_preview_widget.pho_jupyter_preview_widget.display_helpers import array_preview_with_heatmap_repr_html

            # Register the custom display function for numpy arrays
            import IPython
            ip = IPython.get_ipython()
            ip.display_formatter.formatters['text/html'].for_type(np.ndarray, array_preview_with_heatmap) # only registers for NDArray

            # Example usage
            arr = np.random.rand(3, 4)
            display(arr)

        """

        # print(f'WARN: n_dim: {n_dim} greater than 2 is unsupported!')
        # # from pyphocorehelpers.plotting.media_output_helpers import get_array_as_image_stack
        # # #TODO 2024-08-13 05:05: - [ ] use get_array_as_image_stack to render the 3D array
        # message = f"Heatmap Err: n_dim: {n_dim} greater than 2 is unsupported!"
        # heatmap_html = f"""
        # <div style="text-align: center; padding: 20px; border: 1px solid #ccc;">
        #     <p style="font-size: 16px; color: red;">{message}</p>
        # </div>
        # """

        out_image = cls.matplotlib_fig_to_ipython_img(fig, **kwargs)
        if (out_image is not None):
            orientation = "row" if horizontal_layout else "column"
            ## Lays out side-by-side:
            # Convert the IPython Image object to a base64-encoded string
            out_image_data = out_image.data
            b64_image = base64.b64encode(out_image_data).decode('utf-8')
            # Create an HTML widget for the heatmap
            fig_size_format_str: str = ''
            width = kwargs.get('width', None)
            if (width is not None) and (width > 0):
                fig_size_format_str = fig_size_format_str + f'width="{width}" '
            height = kwargs.get('height', None)
            if (height is not None) and (height > 0):
                fig_size_format_str = fig_size_format_str + f'height="{height}" '
            
            fig_image_html = f'<img src="data:image/png;base64,{b64_image}" {fig_size_format_str}style="background:transparent;"/>' #  width="{ndarray_preview_config.heatmap_thumbnail_width}"

        else:
            # getting image failed:
            # Create an HTML widget for the heatmap
            message = "Heatmap Err"
            fig_image_html = f"""
            <div style="text-align: center; padding: 20px; border: 1px solid #ccc;">
                <p style="font-size: 16px; color: red;">{message}</p>
            </div>
            """

            
        # Combine both HTML representations
        if horizontal_layout:
            combined_html = f"""
            <div style="display: flex; flex-direction: row; align-items: flex-start;">
                <div>{fig_image_html}</div>
            </div>
            """
        else:
            combined_html = f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div>{fig_image_html}</div>
                <div style="margin-top: 10px;">
                </div>
            </div>
            """
        return combined_html


    
def _subfn_create_heatmap(data: NDArray, brokenaxes_kwargs=None) -> Optional[BytesIO]: # , omission_indices: list = None
    """ 
    
    #TODO 2024-08-16 04:05: - [ ] Make non-interactive and open in the background

    from neuropy.utils.matplotlib_helpers import matplotlib_configuration
    with matplotlib_configuration(is_interactive=False, backend='AGG'):
        # Perform non-interactive Matplotlib operations with 'AGG' backend
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Non-interactive Mode with AGG Backend')
        plt.savefig('plot.png')  # Save the plot to a file (non-interactive mode)

            
    import matplotlib
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    _bak_rcParams = mpl.rcParams.copy()

    matplotlib.use('Qt5Agg')
    # %matplotlib inline
    # %matplotlib auto


    # _restore_previous_matplotlib_settings_callback = matplotlib_configuration_update(is_interactive=True, backend='Qt5Agg')
    _restore_previous_matplotlib_settings_callback = matplotlib_configuration_update(is_interactive=True, backend='Qt5Agg')

        
    """
    if (data.ndim < 2):
        data = np.atleast_2d(data)
        # fix issues with 1D data like `TypeError: Invalid shape (58,) for image data`
    
    import matplotlib.pyplot as plt
    
    try:
        imshow_shared_kwargs = {
            'origin': 'lower',
        }

        active_cmap = 'viridis'
        fig = plt.figure(figsize=(3, 3), num='_jup_backend')
        ax = fig.add_subplot(111)
        ax.imshow(data, cmap=active_cmap, **imshow_shared_kwargs)
        ax.axis('off')
            
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        
    except SystemError as err:
        # SystemError: tile cannot extend outside image
        print(f'ERROR: Encountered error while plotting heatmap:\n\terr: {err}')
        print(f'\tnp.shape(data): {np.shape(data)}\n\tdata: {data}')
        buf = None

    finally:
        plt.close()        
    
    return buf

# Convert to ipywidgets Image
def _subfn_display_heatmap(data: NDArray, brokenaxes_kwargs=None, **img_kwargs) -> Optional[IPython.core.display.Image]:
    """ Renders a small thumbnail Image of a heatmap array
    
    """
    img_kwargs = dict(width=None, height=img_kwargs.get('height', 100), format='png') | img_kwargs
    buf = _subfn_create_heatmap(data, brokenaxes_kwargs=brokenaxes_kwargs)
    if buf is not None:
        # Create an IPython Image object
        img = IPython.core.display.Image(data=buf.getvalue(), **img_kwargs) # IPython.core.display.Image
        return img
    else:
        return None

def array_preview_with_heatmap_repr_html(arr, include_shape: bool=True, horizontal_layout=True, include_plaintext_repr:bool=False, **kwargs):
    """ Generate an HTML representation for a NumPy array with a Dask shape preview and a thumbnail heatmap
    
        from pho_jupyter_preview_widget.pho_jupyter_preview_widget.display_helpers import array_preview_with_heatmap_repr_html

        # Register the custom display function for numpy arrays
        import IPython
        ip = IPython.get_ipython()
        ip.display_formatter.formatters['text/html'].for_type(np.ndarray, array_preview_with_heatmap) # only registers for NDArray

        # Example usage
        arr = np.random.rand(3, 4)
        display(arr)

    """
    max_allowed_arr_elements: int = 10000

    if isinstance(arr, np.ndarray):
        
        n_dim: int = np.ndim(arr)
        if n_dim > 2:
            print(f'WARN: n_dim: {n_dim} greater than 2 is unsupported!')
            # from pyphocorehelpers.plotting.media_output_helpers import get_array_as_image_stack
            # #TODO 2024-08-13 05:05: - [ ] use get_array_as_image_stack to render the 3D array
            message = f"Heatmap Err: n_dim: {n_dim} greater than 2 is unsupported!"
            heatmap_html = f"""
            <div style="text-align: center; padding: 20px; border: 1px solid #ccc;">
                <p style="font-size: 16px; color: red;">{message}</p>
            </div>
            """

        else:
            ## n_dim == 2
            if np.shape(arr)[0] > max_allowed_arr_elements: 
                # truncate 
                arr = arr[max_allowed_arr_elements:]
            
            heatmap_image = _subfn_display_heatmap(arr, **kwargs)
            if (heatmap_image is not None):
                orientation = "row" if horizontal_layout else "column"
                ## Lays out side-by-side:
                # Convert the IPython Image object to a base64-encoded string
                heatmap_image_data = heatmap_image.data
                b64_image = base64.b64encode(heatmap_image_data).decode('utf-8')
                # Create an HTML widget for the heatmap
                heatmap_size_format_str: str = ''
                width = kwargs.get('width', None)
                if (width is not None) and (width > 0):
                    heatmap_size_format_str = heatmap_size_format_str + f'width="{width}" '
                height = kwargs.get('height', None)
                if (height is not None) and (height > 0):
                    heatmap_size_format_str = heatmap_size_format_str + f'height="{height}" '
                
                heatmap_html = f'<img src="data:image/png;base64,{b64_image}" {heatmap_size_format_str}style="background:transparent;"/>' #  width="{ndarray_preview_config.heatmap_thumbnail_width}"

            else:
                # getting image failed:
                # Create an HTML widget for the heatmap
                message = "Heatmap Err"
                heatmap_html = f"""
                <div style="text-align: center; padding: 20px; border: 1px solid #ccc;">
                    <p style="font-size: 16px; color: red;">{message}</p>
                </div>
                """

        # height="{height}"
        dask_array_widget_html = ""
        plaintext_html = ""
        
        if include_shape:
            dask_array_widget: widgets.HTML = widgets.HTML(value=da.array(arr)._repr_html_())
            dask_array_widget_html: str = dask_array_widget.value
            dask_array_widget_html = f"""
                <div style="margin-left: 10px;">
                    {dask_array_widget_html}
                </div>
            """

        if include_plaintext_repr:                
            # plaintext_repr = np.array2string(arr, edgeitems=3, threshold=5)  # Adjust these parameters as needed
            plaintext_repr = np.array2string(arr)
            plaintext_html = f"<pre>{plaintext_repr}</pre>"
            plaintext_html = f"""
                <div style="margin-left: 10px;">
                    {plaintext_html}
                </div>
            """
            
        # Combine both HTML representations
        if horizontal_layout:
            combined_html = f"""
            <div style="display: flex; flex-direction: row; align-items: flex-start;">
                <div>{heatmap_html}</div>
                {dask_array_widget_html}
                {plaintext_html}
            </div>
            """
        else:
            combined_html = f"""
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div>{heatmap_html}</div>
                <div style="margin-top: 10px;">
                    {dask_array_widget_html}
                    {plaintext_html}
                </div>
            </div>
            """
        return combined_html

    else:
        raise ValueError("The input is not a NumPy array.")



# ---------------------------------------------------------------------------- #
#                       Jupyter Datatype Printing Helpers                      #
# ---------------------------------------------------------------------------- #

def array_repr_with_graphical_shape(ip: "ipykernel.zmqshell.ZMQInteractiveShell") -> "ipykernel.zmqshell.ZMQInteractiveShell":
    """Generate an HTML representation for a NumPy array, similar to Dask.
        
    from preferences_helpers import array_graphical_shape
    from pho_jupyter_preview_widget.display_helpers import array_preview_with_graphical_shape_repr_html
    
    # Register the custom display function for NumPy arrays
    import IPython
    
    ip: "ipykernel.zmqshell.ZMQInteractiveShell)" = IPython.get_ipython()


    """
    from pho_jupyter_preview_widget.display_helpers import array_preview_with_graphical_shape_repr_html
    # Register the custom display function for NumPy arrays
    ip.display_formatter.formatters['text/html'].for_type(np.ndarray, lambda arr: array_preview_with_graphical_shape_repr_html(arr))
    return ip


def array_repr_with_graphical_preview(ip: "ipykernel.zmqshell.ZMQInteractiveShell", include_shape: bool=True, horizontal_layout:bool=True, include_plaintext_repr:bool=True, height:int=50, width:Optional[int]=None) -> "ipykernel.zmqshell.ZMQInteractiveShell":
    """Generate an HTML representation for a NumPy array with a Dask shape preview and a thumbnail heatmap
    
    """
    from pho_jupyter_preview_widget.display_helpers import array_preview_with_heatmap_repr_html

    # Register the custom display function for NumPy arrays
    ip.display_formatter.formatters['text/html'].for_type(np.ndarray, lambda arr: array_preview_with_heatmap_repr_html(arr, include_shape=include_shape, horizontal_layout=horizontal_layout, include_plaintext_repr=include_plaintext_repr, height=height, width=width))
    
    # ## Plain-text type representation can be suppressed like:
    if include_plaintext_repr:
        # Override text formatter to prevent plaintext representation
        ## SIDE-EFFECT: messes up printing NDARRAYs embedded in lists, dicts, other objects, etc. It seems that when rendering these they use the 'text/plain' representations
        ip.display_formatter.formatters['text/plain'].for_type(
            np.ndarray, 
            lambda arr, p, cycle: None
        )
    
    return ip


#TODO 2024-08-07 13:02: - [ ] Finish custom plaintext formatting
# # Register the custom display function for NumPy arrays
# import IPython
# ip = IPython.get_ipython()

# def format_list_of_ndarrays(obj, p, cycle):
#     if all(isinstance(x, np.ndarray) for x in obj):
#         return "[" + ", ".join(np.array2string(a) for a in obj) + "]"
#     else:
#         # Fallback to the original formatter
#         return p.text(repr(obj))
#         # # Use the existing formatter if present, or default to repr
#         # existing_formatter = ip.display_formatter.formatters['text/plain'].lookup_by_type(list)
#         # return existing_formatter(obj, p, cycle) if existing_formatter else repr(obj)
    

# # ip.display_formatter.formatters['text/plain'].for_type(
# #     List[NDArray], 
# #     lambda arr, p, cycle: np.array2string(arr)
# # )

# # Register the custom formatter
# ip.display_formatter.formatters['text/plain'].for_type(list, format_list_of_ndarrays)
# ip.display_formatter.formatters['text/plain'].type_printers[np.ndarray]


# ip.display_formatter.formatters['text/plain'].type_printers.pop(list, None)


def dataframe_show_more_button(ip: "ipykernel.zmqshell.ZMQInteractiveShell") -> "ipykernel.zmqshell.ZMQInteractiveShell":
    """Adds a functioning 'show more' button below each displayed dataframe to show more rows.

    Usage:
        ip = get_ipython()
        ip = dataframe_show_more_button(ip=ip)
    """
    def _subfn_dataframe_show_more(df, initial_rows=10, default_more_rows=50):
        """Generate an HTML representation for a Pandas DataFrame with a 'show more' button."""
        total_rows = df.shape[0]
        if total_rows <= initial_rows:
            return df.to_html()

        # Create the initial view
        initial_view = df.head(initial_rows).to_html()

        # Escape backticks and newlines in the DataFrame HTML to ensure proper JavaScript string
        df_html = df.to_html().replace("`", "\\`").replace("\n", "\\n")

        # Generate the script for the 'show more' button with input for number of rows
        script = f"""
        <script type="text/javascript">
            function showMore() {{
                var numRows = document.getElementById('num-rows').value;
                if (numRows === "") {{
                    numRows = {default_more_rows};
                }} else {{
                    numRows = parseInt(numRows);
                }}
                var div = document.getElementById('dataframe-more');
                var df_html = `{df_html}`;
                var parser = new DOMParser();
                var doc = parser.parseFromString(df_html, 'text/html');
                var rows = doc.querySelectorAll('tbody tr');
                for (var i = 0; i < rows.length; i++) {{
                    if (i >= numRows) {{
                        rows[i].style.display = 'none';
                    }} else {{
                        rows[i].style.display = '';
                    }}
                }}
                div.innerHTML = doc.body.innerHTML;
            }}
        </script>
        """

        # Create the 'show more' button and input field with default value
        button_and_input = f"""
        <input type="number" id="num-rows" placeholder="Enter number of rows to display" value="{default_more_rows}">
        <button onclick="showMore()">Show more</button>
        <div id="dataframe-more"></div>
        """

        # Combine everything into the final HTML
        html = f"""
        {script}
        {initial_view}
        {button_and_input}
        """
        return HTML(html)


    ip.display_formatter.formatters['text/html'].for_type(pd.DataFrame, lambda df: display(_subfn_dataframe_show_more(df)))
    return ip




    
