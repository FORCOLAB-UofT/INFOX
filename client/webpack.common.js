const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.js', // Assuming your entry point is src/index.js
  output: {
    path: path.resolve(__dirname, 'dist'), // Output directory
    filename: 'bundle.js', // Output bundle file name
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/, // For JavaScript and JSX files
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader', // Using Babel to transpile JavaScript
        },
      },
      {
        test: /\.css$/, // For CSS files
        use: ['style-loader', 'css-loader'], // Process CSS with style-loader and css-loader
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif|ico)$/, // For image files
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'images', // Output directory for images
            },
          },
        ],
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/, // For font files
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts', // Output directory for fonts
            },
          },
        ],
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html', // Your HTML file to be used as a template
      favicon: './public/favicon.ico', // Favicon
    }),
  ],
  resolve: {
    extensions: ['.js', '.jsx'], // Automatically resolve these file extensions
  },
};
