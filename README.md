# powerlytics

## node-red flow development

Create a `ecosystem.config.js` and change the value of `API_URL`, `APP_ID`, `TOKEN_URL`, `AUTHORIZATION_URL`.

```
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
    }
  }]
}
```

```
npm i

npm start
```

Node-red will be running at http://localhost:1880

## Create .exe installer

<b> NOTE: requires python >= 3.7 </b>

```
pip install pyinstaller

pyinstaller --onefile --windowed installer.py

pyinstaller --onefile --windowed start.py

pyinstaller --onefile --windowed stop.py
```

The folders `build` and `dist` will be created as a result of this. The.exe files should now be located in the `dist` directory.

<b> NOTE: The old build and dist folders should be deleted before starting a new build. </b>
