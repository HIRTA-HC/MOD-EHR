const path = require("path");
const webpack = require('webpack');
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = (env) => {
    return {
        entry: {
            index: "./src/index.js",
            dashboard: "./src/dashboard.js",
            appointments: "./src/appointments.js",
            patients: "./src/patients.js",
            common: "./src/common.js",
            usermanagement: "./src/usermanagement.js",
            settingspanel: "./src/settingspanel.js",
            logs: "./src/logs.js"
        },
        output: {
            filename: "[name].js",
            path: path.resolve(__dirname, "dist"),
        },

        plugins: [

            new webpack.DefinePlugin({
                'process.env': JSON.stringify(env),
                'process.env.ENV': JSON.stringify(env.ENV || "LOCAL"),
            }),

            new CopyWebpackPlugin({
                patterns: [{ from: "src", to: path.resolve(__dirname, "dist") }],
            }),
        ],
        mode: "production",
    }
};
