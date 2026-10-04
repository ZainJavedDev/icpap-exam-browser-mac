# ICPAP Exam Browser for macOS

A modified version of [Safe Exam Browser for macOS](https://github.com/SafeExamBrowser/seb-mac) for the ICPAP Online Examination System, the macOS counterpart of [icpap-exam-browser](https://github.com/ZainJavedDev/icpap-exam-browser) for Windows. It stays under the Mozilla Public License 2.0; the original copyright notices are unchanged.

Changes from upstream, all on the `icpap` branch:

- **Built-in settings** (`Classes/Global/SEBConstants.h`, `Classes/ConfigFiles/SEBSettings.m`): starts at the exam system's login page, only allows main-page navigation to the exam system's domain and `meet.jit.si`, quits at `/seb/quit`, allows the camera and microphone, and refuses to run in a virtual machine. No `.seb` file is needed.
- **Config Key header** (`Classes/BrowserComponents/SEBBrowserController.m`, `SEBAbstractModernWebView.swift`): sends `X-SafeExamBrowser-ConfigKeyHash` with the same fixed Config Key as the Windows version, so the exam system checks both with one key. Upstream's modern WebView (needed for the camera) sends no headers, so page loads are repeated with the header, and the page's `fetch`/`XMLHttpRequest` calls to its own origin get it added. **Form submissions (POST) and synchronous requests go without the header**: WebKit offers no way to add it there.
- **Plain-http test servers**: when the start page is `http://`, media capture is allowed on insecure origins so the camera works against a development server on the local network.
- **Classic kiosk mode**: Apple's Automatic Assessment Configuration needs an entitlement Apple grants only to a paid developer team, so the lockdown uses SEB's classic kiosk mode.
- **Unsigned build**: the closed-source `libSEBSupport.a` (not in the public repository) is no longer linked, and the app is ad-hoc signed with its own bundle identifier, `org.icpap.ExamBrowser`.
- **Branding**: ICPAP seal and the name "ICPAP Exam Browser" on the app icon, About window, menus and messages. Regenerate the images with `python3 Branding/make-branding.py` after replacing `Branding/icpap-logo.png`.
- **Build**: `.github/workflows/icpap-build.yml` builds a universal (Apple silicon and Intel) disk image on GitHub Actions. Run it from the Actions tab with the exam address; it reads the Config Key from the `ICPAP_CONFIG_KEY` repository secret, which must match the Windows repository's.

## Opening the app

The app isn't signed with an Apple Developer ID, so macOS blocks it the first time. Copy it to Applications, try to open it, then go to System Settings → Privacy & Security and click **Open Anyway** (or run `xattr -dr com.apple.quarantine "/Applications/ICPAP Exam Browser.app"`). Each new build is a different app to macOS, so it asks again for this and for camera and microphone access.

Signing with an Apple Developer ID ($99 a year) and notarising would remove these prompts and allow Automatic Assessment Configuration.

---

# seb-mac
Safe Exam Browser for macOS and iOS,
SEB Verificator for macOS

To build, SafeExamBrowser.xcworkspace needs to be opened in a recent version of Xcode (currently 14.3.1). Note: When building SEB for iOS with Xcode 15.x, the custom SEB User Agent cannot be set in UIWebView, which leads to issues when using some SEB integrations in assessment systems. For building, own code signing identities need to be added. SEB uses the com.apple.developer.edu-assessment-mode entitlement, which needs to be requested from Apple for your developer team.

Currently main reflects SEB for macOS/iOS 3.3.2 or newer. SEB is using a unified macOS/iOS/iPadOS Xcode project (Xcode workspace with both macOS and iOS targets and a SEBVerificator target). 

This repository contains the open source SEB code base. Binary security modules and Zoom integration (with proprietary licenses) are not included. You might have to remove missing references in the Xcode workspace and particular security-related code. Please note that we can only consult SEB Alliance Platinum or Diamond contributors about building (customized) SEB versions. The open source code is available mainly for educational purposes and not for building own versions of SEB.

All information about Safe Exam Browser you'll find at http://safeexambrowser.org, especially see https://safeexambrowser.org/developer/overview.html. Other documentation is available in the according repositories. Search discussions boards if you don't find information in the manual and SEB How To document (see links on page Support).

For your information: The correct way how to spell SEB for user-facing text is all three letters in CAPS. If you find SEB written as seb in code, then that's ok if it's some symbol users will never see. If you find SEB written as Seb, then that is definitely WRONG.
