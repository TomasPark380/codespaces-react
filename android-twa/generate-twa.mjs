import { TwaManifest, TwaGenerator } from '@bubblewrap/core';
import { join } from 'path';
import { writeFileSync } from 'fs';

const targetDirectory = process.cwd();
const iconUrl = process.env.ICON_URL || 'http://localhost:8765/logo512.png';

const twaManifest = new TwaManifest({
  packageId: 'app.vercel.luxederma.twa',
  host: 'service-4-0-phy-luxe-derma-1063505152868.us-west1.run.app',
  name: 'Luxe Derma',
  launcherName: 'Luxe Derma',
  display: 'standalone',
  themeColor: '#FFFFFF',
  themeColorDark: '#000000',
  navigationColor: '#000000',
  navigationColorDark: '#000000',
  navigationDividerColor: '#00000000',
  navigationDividerColorDark: '#00000000',
  backgroundColor: '#FFFFFF',
  enableNotifications: true,
  startUrl: '/',
  iconUrl,
  appVersionName: '1',
  appVersionCode: 1,
  signingKey: {
    path: join(targetDirectory, 'android.keystore'),
    alias: 'android',
  },
  splashScreenFadeOutDuration: 300,
  orientation: 'default',
  fingerprints: [],
  generatorApp: 'bubblewrap-cli',
  enableSiteSettingsShortcut: true,
  isChromeOSOnly: false,
  isMetaQuest: false,
  minSdkVersion: 21,
  shortcuts: [],
  additionalTrustedOrigins: [],
  retainedBundles: [],
  fullScopeUrl: 'https://service-4-0-phy-luxe-derma-1063505152868.us-west1.run.app/',
});

const generator = new TwaGenerator();
await twaManifest.saveToFile(join(targetDirectory, 'twa-manifest.json'));
await generator.createTwaProject(targetDirectory, twaManifest, console);
console.log('TWA project generated at', targetDirectory);
