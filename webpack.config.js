var autoprefixer = require('autoprefixer');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');
var webpack = require('webpack');

var bundleTrackerPlugin = new BundleTracker({
  filename: 'webpack-bundle.json'
});

var commonsChunkPlugin = new webpack.optimize.CommonsChunkPlugin('vendor', '[name].[chunkhash].js');

var extractTextPlugin = new ExtractTextPlugin(
  '[name].[chunkhash].css'
);

var providePlugin = new webpack.ProvidePlugin({
  $: 'jquery',
  '_': 'underscore',
  jQuery: 'jquery',
  'window.jQuery': 'jquery',
  Backbone: 'backbone',
  'window.Backbone': 'backbone'
});

var config = {
  entry: {
    cart: './mychichair/static/js/cart.js',
    dashboard: './mychichair/static/js/dashboard.js',
    storefront: './mychichair/static/js/storefront.js',
    vendor: [
      'bootstrap-sass',
      'jquery',
      'jquery.cookie'
    ]
  },
  output: {
    path: path.resolve(__dirname, 'mychichair/static/assets/'),
    filename: '[name].[chunkhash].js'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel'
      },
      {
        test: /\.json$/,
        loader: 'json'
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract([
          'css?sourceMap',
          'postcss',
          'sass'
        ])
      },
      {
        test: /\.(eot|otf|png|svg|ttf|woff|woff2)(\?v=[0-9.]+)?$/,
        loader: 'file?name=[name].[hash].[ext]',
        include: [
          path.resolve(__dirname, 'node_modules'),
          path.resolve(__dirname, 'mychichair/static/fonts'),
          path.resolve(__dirname, 'mychichair/static/images'),
          path.resolve(__dirname, 'mychichair/static/img')
        ]
      }
    ]
  },
  plugins: [
    bundleTrackerPlugin,
    commonsChunkPlugin,
    extractTextPlugin,
    providePlugin
  ],
  postcss: function() {
    return [autoprefixer];
  },
  resolve: {
    alias: {
      'jquery': path.resolve(__dirname, 'node_modules/jquery/dist/jquery.js')
    }
  },
  sassLoader: {
    sourceMap: true
  }
};

module.exports = config;
