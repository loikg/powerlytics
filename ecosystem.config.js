module.exports = {
  apps: [{
    name: "carbon-analytics",
    script: "./node_modules/node-red/red.js",
    args: "-D contextStorage.default.module=memory -D contextStorage.file.module=localfilesystem",
    env: {
      NODE_ENV: "development",
      NODE_TLS_REJECT_UNAUTHORIZED: 0,
      API_URL: "",
      APP_ID: "",
      TOKEN_URL: "",
      AUTHORIZATION_URL: ""
    },
    env_test: {
      NODE_ENV: "test",
    },
    env_staging: {
      NODE_ENV: "staging",
    },
    env_production: {
      NODE_ENV: "production",
      NODE_TLS_REJECT_UNAUTHORIZED: 0,
      API_URL: "{{PROD_API_URL}}",
      APP_ID: "{{PROD_APP_ID}}",
      TOKEN_URL: "{{PROD_TOKEN_URL}}",
      AUTHORIZATION_URL: "{PROD_AUTHORIZATION_URL}}"
    }
  }]
}
