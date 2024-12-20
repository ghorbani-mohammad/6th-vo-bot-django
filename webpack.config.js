const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const { SourceMapDevToolPlugin } = require("webpack");

module.exports = {
    entry: './static/assets/index.js',  // Path to your input file
    output: {
        filename: '[name].bundle.js',  // Output bundle file name
        path: path.resolve(__dirname, './static/dist'),  // Path to Django static directory
    },

    module: {
        rules: [
            // JavaScript/JSX Files
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',  // Using Babel to transpile JS/JSX
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react'],
                    },
                },
            },
            // CSS Files
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader'],
            },
            // Image Files
            {
                test: /\.(png|jpe?g|gif|svg)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'images/[name][ext][query]'
                }
            },
            // Font Files
            {
                test: /\.(ttf|eot|woff|woff2)$/,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name][ext][query]'
                }
            },
        ],
    },

    resolve: {
        extensions: ['.js', '.jsx', '.css'],  // Removed empty string
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css',  // Output CSS file name
        }),
        new SourceMapDevToolPlugin({
            filename: "[file].map"
        })
    ],

    optimization: {
        minimizer: [
            new CssMinimizerPlugin(),
            '...',  // This ensures that existing minimizers (like Terser for JS) are included
        ],
    },

    mode: 'production',  // Ensure you're in production mode for optimizations
};
