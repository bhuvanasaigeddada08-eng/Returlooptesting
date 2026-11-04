# ReturnLoop LPU - Android APK Integration & Build Guide

This document describes how to package **ReturnLoop LPU** as an Android application using **Capacitor**, run it on physical devices or emulators, and build production APKs/AAB bundles.

---

## 1. Project Configuration Summary

- **App Identifier**: `com.returnloop.lpu`
- **Application Name**: `ReturnLoop LPU`
- **Capacitor Configuration**: `frontend/capacitor.config.json`
- **Native Android Project**: Located in `frontend/android/`
- **Web Build Assets**: Compiled via `npm run build` into `frontend/dist/` and synchronized to `frontend/android/app/src/main/assets/public/`

---

## 2. Critical Mobile Network Requirement

> [!IMPORTANT]
> **Android `localhost` Caveat**:
> On an Android device or emulator, `localhost` (or `127.0.0.1`) refers strictly to the **phone itself**, NOT the developer's laptop running Flask.
>
> To connect an Android device to your backend:
> 1. Find your developer computer's reachable LAN IP (e.g. `192.168.1.15` or `172.22.80.54` via `ipconfig`).
> 2. Set the `VITE_API_BASE_URL` in `frontend/.env.production` or `frontend/.env`:
>    ```env
>    VITE_API_BASE_URL=http://192.168.1.15:5000
>    ```
> 3. Start the Flask backend binding to `0.0.0.0`:
>    ```bash
>    python run.py
>    ```
> 4. Ensure your Windows Defender / local firewall allows incoming connections on port `5000`.

---

## 3. Prerequisites for Building the APK

To build the APK on your workstation, ensure you have:
1. **Java Development Kit (JDK 17 or 21)** installed and added to `JAVA_HOME`.
   - Download: [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) or [Eclipse Temurin](https://adoptium.net/)
   - Verify in terminal: `java -version`
2. **Android Studio** (Koala or Ladybug recommended) with Android SDK and Command-line Tools installed.
   - Download: [developer.android.com/studio](https://developer.android.com/studio)

---

## 4. Step-by-Step Android Studio Build Workflow

The complete native Android project has already been initialized and pre-synchronized in `frontend/android`.

### Step 1: Open Project in Android Studio
1. Launch Android Studio.
2. Select **Open** and choose the folder:
   ```
   c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\frontend\android
   ```
3. Allow Gradle to sync dependencies and index the project (takes ~1-2 minutes).

### Step 2: Synchronize Web Changes (When updating React code)
Whenever you modify frontend React components:
```bash
cd frontend
npm run build
npx cap sync android
```

### Step 3: Run on Physical Device or Emulator
1. Enable **Developer Options** and **USB Debugging** on your Android smartphone.
2. Connect your phone via USB cable and allow debugging.
3. In Android Studio, select your phone from the device dropdown at the top.
4. Click the green **Run (▶)** button.
5. Android Studio will compile, install the APK, and launch ReturnLoop LPU on your phone!

---

## 5. Building the Debug APK from Command Line

Once `JAVA_HOME` is set:
```bash
cd frontend/android
.\gradlew.bat assembleDebug
```
The output APK will be generated at:
```
frontend/android/app/build/outputs/apk/debug/app-debug.apk
```
You can install this APK onto any Android phone directly via USB or by running:
```bash
adb install frontend/android/app/build/outputs/apk/debug/app-debug.apk
```

---

## 6. Building a Signed Release APK for Distribution

To distribute the APK to students or campus users:
1. In Android Studio, click **Build > Generate Signed Bundle / APK...**
2. Choose **APK** and click **Next**.
3. Create a new Keystore file (or choose an existing `.jks` keystore), set alias and password.
4. Select build variant **release**, check **V1 (Jar Signature)** and **V2 (Full APK Signature)**.
5. Click **Finish**.
6. The signed release APK will be generated in:
   ```
   frontend/android/app/release/app-release.apk
   ```

---

## 7. Verified Local Build Command & Status (Tested & Confirmed)

The Android debug APK has been **successfully compiled and verified** directly on this workstation!

- **Generated APK**: `frontend/android/app/build/outputs/apk/debug/app-debug.apk`
- **Binary Size**: ~4.27 MB (4,271,260 bytes)
- **Application ID**: `com.returnloop.lpu`
- **Application Name**: `ReturnLoop LPU`

### One-Liner PowerShell Build Command
To rebuild the debug APK at any time without Android Studio:
```powershell
$env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"; $env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"; & "C:\Users\bhuva\.gradle\wrapper\dists\gradle-9.3.0-bin\79n14ral3mx1ozqr3csh2u872\gradle-9.3.0\bin\gradle.bat" assembleDebug
```
*(Run from `c:\Users\bhuva\OneDrive\Desktop\ReturnLoop\frontend\android`)*
