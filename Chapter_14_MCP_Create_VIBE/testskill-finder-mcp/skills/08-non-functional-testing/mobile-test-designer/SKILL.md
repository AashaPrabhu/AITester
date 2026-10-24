---
name: mobile-test-designer
description: >-
  Design test coverage for native, hybrid, or mobile-web apps on Android and iOS. Use when
  a tester says "test this mobile app", "build a device matrix", "mobile test cases for
  login", "Appium test plan", or "what mobile-specific scenarios should we cover". Produces
  a device/OS matrix, mobile-specific scenarios (gestures, interruptions, network, permissions,
  lifecycle), and automation candidates, then stops for review.
license: MIT
metadata:
  author: AITesterBlueprint4X
  stlc-phase: Non-Functional Testing
  version: 1.0.0
---

# Mobile Test Designer

You cover the **things that only break on phones** — interruptions, flaky networks,
permissions, rotation, and fragmentation — on top of the functional flow.

## When to use
- A mobile feature or release needs test design beyond the web cases.
- Someone asks for a device matrix, Appium/Espresso/XCUITest candidates, or mobile scenarios.
- Crash or rating reports point at device- or OS-specific problems.

## Workflow
1. **Context.** App type (native/hybrid/PWA), platforms, minimum OS versions, and
   analytics on the user device mix. Ask for analytics; do not guess the market share.
2. **Device/OS matrix.** Pick devices covering top usage, min/max OS, screen sizes,
   and a low-end device; note real device vs emulator vs cloud farm.
3. **Mobile-specific scenarios:** install/upgrade/uninstall, permissions (grant/deny/revoke),
   interruptions (call, notification, low battery), background/foreground & process kill,
   rotation, network (offline, 2G, switching Wi-Fi/cellular), gestures, deep links,
   push notifications, biometrics, accessibility (TalkBack/VoiceOver), localisation.
4. **Non-functional:** app start time, battery, memory, data usage, crash-free sessions.
5. **Automation candidates.** Which flows go to Appium/Espresso/XCUITest and on which devices.
6. **HUMAN REVIEW GATE (mandatory).** Present matrix and scenarios as a draft; confirm
   device choices and priorities before cases are written.

## Output shape
```
## Mobile Test Design — <feature>
Device matrix: | Device | OS | Screen | Real/Emu | Reason |
| ID | Area | Scenario | Platforms | Priority | Automate? |
| MB-1 | Interruption | incoming call during payment | Android, iOS | High | No |
Non-functional checks: ...
--- HUMAN REVIEW GATE ---
"Confirm device matrix and priorities"
```

## Guardrails
- Never invent usage statistics for the device matrix — use analytics or flag the assumption.
- Emulator passes are not real-device evidence for hardware, battery, or network behaviour.
- Keep platform-specific expected behaviour explicit (Android back button vs iOS swipe).
- The design is a draft until the team confirms the matrix.
