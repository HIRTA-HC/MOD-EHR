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
                // 'process.env.ENV': JSON.stringify(env.ENV || "LOCAL"),
                // 'process.env': {
                //     'ENV': JSON.stringify(env.ENV || "LOCAL"),
                //     'REGION': JSON.stringify(env.REGION || "us-east-1"),
                //     'POOL_ID': JSON.stringify(env.POOL_ID || "us-east-1_dCo7aAKQk"),
                //     'CLIENT_ID': JSON.stringify(env.CLIENT_ID || "22eofn4rjh9l4sdvmfsbg271o5"),
                //     'IDENTITY_POOL_ID': JSON.stringify(env.IDENTITY_POOL_ID || "us-east-1:cf5f0f25-b76d-44bc-b5ce-7d5aa484bc3e"),
                //     'GOOGLE_MAPS_KEY': JSON.stringify(env.GOOGLE_MAPS_KEY || "AIzaSyANCIsb2avj0G07Cdvb3LMcAsgK1coFE54"),
                //     'BASE_URL': JSON.stringify(env.BASE_URL || "https://c18fik9rmg.execute-api.us-east-1.amazonaws.com")
                // }
            }),

            new CopyWebpackPlugin({
                patterns: [{ from: "src", to: path.resolve(__dirname, "dist") }],
            }),
        ],
        mode: "production",
    }
};
