# Luxe Derma TWA (Android App Bundle)

This directory contains a Trusted Web Activity (TWA) wrapper that packages
`https://service-4-0-phy-luxe-derma-1063505152868.us-west1.run.app` as an
Android App Bundle (`.aab`) suitable for Google Play.

The project was scaffolded with [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap).
All source, Gradle configuration, Android resources and the generated launcher
icons are committed. The only things you must supply locally are the Android
SDK and a signing keystore — both of which are free but cannot be downloaded
from this sandboxed web environment.

## Key configuration

| Field        | Value                                                                          |
|--------------|--------------------------------------------------------------------------------|
| Start URL    | `https://service-4-0-phy-luxe-derma-1063505152868.us-west1.run.app/`           |
| Package ID   | `app.vercel.luxederma.twa`                                                     |
| App name     | Luxe Derma                                                                     |
| Version      | 1 (versionCode 1)                                                              |
| Icon         | `icon.png` (512×512, sourced from `public/logo512.png`)                        |
| Display      | standalone                                                                     |
| Min SDK      | 21                                                                             |

Edit [`twa-manifest.json`](./twa-manifest.json) and re-run `npm run generate`
(see below) to tweak any of these values.

## Build the AAB locally

Requirements:

- Node.js 18+
- JDK 17 (Bubblewrap can install one for you)
- ~2 GB free disk space (Android SDK will be downloaded on first build)

```bash
cd android-twa
npm install

# 1. Create the signing keystore (only needed once). The keystore is
#    gitignored — keep it safe.
./node_modules/.bin/bubblewrap init --manifest=file://$(pwd)/twa-manifest.json \
    --directory=. || true # prints the same prompts; you can abort after key creation

# Alternatively, create the keystore directly with keytool:
keytool -genkeypair -v -keystore android.keystore -alias android \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass <keystore-password> -keypass <key-password> \
    -dname "CN=Luxe Derma, OU=Mobile, O=Luxe Derma, L=Unknown, ST=Unknown, C=KR"

# 2. Build the signed release AAB.
./node_modules/.bin/bubblewrap build --skipPwaValidation
```

Artifacts produced:

- `app-release-bundle.aab` — upload this to Google Play Console
- `app-release-signed.apk` — for local sideloading/testing

## Digital Asset Links (required for TWA)

For the URL bar to be hidden on device, the host must serve a valid
`.well-known/assetlinks.json` file that lists the keystore's SHA-256
fingerprint. After signing, print the fingerprint with:

```bash
keytool -list -v -keystore android.keystore -alias android -storepass <pw> \
  | grep "SHA-256"
```

Then deploy the following to the origin:

```json
// https://service-4-0-phy-luxe-derma-1063505152868.us-west1.run.app/.well-known/assetlinks.json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "app.vercel.luxederma.twa",
    "sha256_cert_fingerprints": ["<PASTE SHA-256 HERE>"]
  }
}]
```

## Regenerating the project

If you change `twa-manifest.json`, regenerate derived Android files:

```bash
node generate-twa.mjs
```

## Why the AAB isn't already in the repo

Building the `.aab` requires the Android SDK (distributed from `dl.google.com`)
and AndroidX/Google Maven dependencies (from `maven.google.com`). Those hosts
are not reachable from this web-based sandbox, so the final `bubblewrap build`
step must be run on a machine with normal internet access (your laptop,
GitHub Actions, Cloud Build, etc.). Everything else is ready.
