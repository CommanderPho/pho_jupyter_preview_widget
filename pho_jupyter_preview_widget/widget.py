from ipywidgets import DOMWidget
from traitlets import Unicode
import os

class MyWidget(DOMWidget):
    _view_name = Unicode('MyWidgetView').tag(sync=True)
    _view_module = Unicode('pho_jupyter_preview_widget').tag(sync=True)
    _view_module_version = Unicode('0.1.0').tag(sync=True)

    action = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def _get_static_path():
        return os.path.join(os.path.dirname(__file__), 'static', 'js')

    @classmethod
    def install(cls):
        from IPython.display import display, Javascript
        js_code = """
        require.undef('pho_jupyter_preview_widget');
        define('pho_jupyter_preview_widget', ["@jupyter-widgets/base"], function(widgets) {
            return {
                MyWidgetView: widgets.DOMWidgetView.extend({
                    render: function() {
                        this.el.innerHTML = '<div class="my-widget">Right-click me!</div>';

                        this.el.addEventListener('contextmenu', (event) => {
                            event.preventDefault();
                            const menu = document.createElement('div');
                            menu.style.position = 'absolute';
                            menu.style.top = `${event.clientY}px`;
                            menu.style.left = `${event.clientX}px`;
                            menu.style.background = '#fff';
                            menu.style.border = '1px solid #ccc';
                            menu.innerHTML = `
                                <div class="menu-item">Custom Action 1</div>
                                <div class="menu-item">Custom Action 2</div>
                            `;
                            document.body.appendChild(menu);

                            const removeMenu = () => {
                                document.body.removeChild(menu);
                                document.removeEventListener('click', removeMenu);
                            };
                            document.addEventListener('click', removeMenu);

                            menu.querySelectorAll('.menu-item').forEach(item => {
                                item.addEventListener('click', () => {
                                    this.model.set('action', item.textContent);
                                    this.model.save_changes();
                                });
                            });
                        });
                    },
                })
            };
        });
        """
        display(Javascript(js_code))

