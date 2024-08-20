const path = require('path');

module.exports = {
    mode: 'development',  // Or 'production'
    entry: './pho_jupyter_preview_widget/static/js/widget.js',
    output: {
        filename: 'widget.bundle.js',
        path: path.resolve(__dirname, 'pho_jupyter_preview_widget/static/js'),
        libraryTarget: 'amd',  // This is compatible with JupyterLab
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
        ],
    },
    externals: {
        '@jupyter-widgets/base': '@jupyter-widgets/base',
    },
};
