## Changes required to switch the original project from the book to use Parcel V2

**Add  `type="module"` to script tag in _index.html_**  

**Delete _dev-server.js_** (Use `npm start` instead of `npm run dev`)

**Add _.parcelrc_ file**
```json
{
  "extends": ["@parcel/config-default"],
  "transformers": {
    "*.py": ["parcel-transformer-transcrypt"]
  }
}
```
**Add _.proxyrc_ file**
```json
{
  "/api": {
    "target": "http://localhost:8000/"
  }
}
```

**Update _package.json_:**
- Remove key entry for "main": "index.js" if it exists
- Update scripts:
  - _Add_ "start": "NODE_ENV=development parcel --log-level info src/index.html --dist-dir dist/dev --port 8080",
  - _Add_ "build": "NODE_ENV=production parcel build --log-level info src/index.html --no-source-maps --dist-dir dist/prod --no-cache --reporter @parcel/reporter-bundle-analyzer"
  - _Remove_ "dev": "node dev-server.js"
- Update dependencies:
  - _Add_ @material-ui/styles (this is likely just due to an update of MUI)
- Update devDependencies:
  - _Change to_ parcel
  - _Change to_ parcel-transformer-transcrypt
  - _Change to_ @parcel/reporter-bundle-analyzer
  - _Remove_ express
  - _Remove_ http-proxy-middleware
- Add alias key (for relative static imports):
```json
  "alias": {
    "./static/**": "./src/static/$1"
  }
```
