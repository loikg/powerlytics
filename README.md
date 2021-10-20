# powerlytics

## node-red flow development

```
npm install

npm start
```

Open localhost:1880

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
