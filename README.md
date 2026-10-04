# Gym Subscription Manager

After starting my weight lifting journey at my local gym, I noticed they were using paper to track memberships, and I thought to myself, "I can automate this." I spoke to the owner about my idea and he seemed intrigued. After about a month of building, I presented them with working software, and they seemed impressed. Though I'm pretty sure they didn't use it for long. Nonetheless, taking the initiative and attempting to solve a real-world problem served as a useful experience.

The project was originally developed as a desktop application in Python. It allows gym memberships to be added, stored and searched, while keeping track of each member's membership expiry date.

## Android Version

I later decided to revisit the project and adapt it for Android using Kivy and Buildozer. I set up an Ubuntu development environment through WSL and rebuilt the application as an Android APK.

Getting the older project working on modern Android came with a few challenges, particularly around outdated dependencies and Android's notification system. After troubleshooting these issues, I implemented Android notifications that alert the user when a stored membership reaches its expiry date.

The Android version has been built and tested on a physical Android device. The APK can be found under the repository's **Releases** section.

## Features

- Add and store gym members and their membership expiry dates
- Search for existing members
- Persistent membership data between app launches
- Android notifications for memberships expiring on the current date
- Desktop and Android versions of the application

## Project Structure

- `dist/` - Original desktop version
- `android/` - Android version, including the Python source and Buildozer configuration
- **Releases** - Ready-to-install Android APK
