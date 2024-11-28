# File: test_formatter.py
import unittest
import numpy as np

from pho_jupyter_preview_widget.display_helpers import array_preview_with_heatmap_repr_html, single_NDArray_array_preview_with_heatmap_repr_html

class TestArrayPreviewWithHeatmapReprHtml(unittest.TestCase):
    
    def setUp(self):
        """Set up the test cases and formatter."""
        # self.formatter = CustomJupyterFormatter()
        self.test_data = [
            np.array([119.191, 142.107, 180.3, 191.757, 245.227, 84.8181]),
            np.array([84.8181, 84.8181, 138.288]),
            np.array([134.469, 69.5411]),
            np.array([249.046]),
            np.array([249.046, 249.046]),
        ]    

    def test_single_array(self):
        """Test rendering a single numpy array."""
        input_data = np.array([1.23, 4.56, 7.89])
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("Heatmap Preview:", rendered.data, "Single array preview should include heatmap text")
        self.assertIn("1.23, 4.56, 7.89", rendered.data, "Array content should appear in the preview")

    def test_empty_array(self):
        """Test rendering an empty numpy array."""
        input_data = np.array([])
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("Heatmap Preview:", rendered.data, "Empty array preview should still include heatmap text")
        self.assertIn("[]", rendered.data, "Empty array should render as []")

    def test_list_of_arrays(self):
        """Test rendering a list of numpy arrays."""
        input_data = [
            np.array([1.23, 4.56, 7.89]),
            np.array([9.87, 6.54, 3.21])
        ]
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("<ul>", rendered.data, "List of arrays should render as an HTML list")
        self.assertIn("<li>", rendered.data, "Each array in the list should be wrapped in a list item")
        self.assertIn("1.23, 4.56, 7.89", rendered.data, "First array content should appear in the preview")
        self.assertIn("9.87, 6.54, 3.21", rendered.data, "Second array content should appear in the preview")

    def test_mixed_list(self):
        """Test rendering a list with non-numpy array items."""
        input_data = [np.array([1.23]), "string_value", 123]
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("Unsupported list elements:", rendered.data, "Mixed lists should render an unsupported message")

    def test_empty_list(self):
        """Test rendering an empty list."""
        input_data = []
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("<ul></ul>", rendered.data, "Empty list should render as an empty HTML list")

    def test_nested_list_of_arrays(self):
        """Test rendering nested lists of numpy arrays."""
        input_data = [
            [np.array([1.23, 4.56])],
            np.array([7.89, 10.11])
        ]
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("Unsupported type:", rendered.data, "Nested lists should render an unsupported message")

    def test_fallback_for_unsupported_type(self):
        """Test rendering unsupported types."""
        input_data = "string_value"
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("Unsupported type:", rendered.data, "Unsupported types should render an error message")

    def test_precision_handling(self):
        """Test precision handling in numpy array rendering."""
        input_data = np.array([1.23456789])
        rendered = array_preview_with_heatmap_repr_html(input_data)
        self.assertIn("1.235", rendered.data, "Array values should respect the precision setting")
        self.assertNotIn("1.23456789", rendered.data, "Excessive precision should not appear")


if __name__ == "__main__":
    unittest.main()
