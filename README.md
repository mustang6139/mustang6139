# MusiThang

<div align="center">
  <p>I build terminal software at hours I should be asleep.</p>
  <img src="assets/hero-tui.svg" alt="A terminal that types fastfetch --me and fastfetch --machine on a loop, printing a short bio and a deliberately unhelpful spec sheet">
  <img src="assets/story-terminal.svg" alt="An animated process monitor where programming runs as PID 1 and every hobby is one of its child processes">
</div>

---

## sdrtop

[![rust](https://img.shields.io/badge/rust-1f2335?style=flat-square&logo=rust&logoColor=ff9e64&labelColor=16161e)](https://github.com/mustang6139/sdrtop)
[![ci](https://img.shields.io/github/actions/workflow/status/mustang6139/sdrtop/ci.yaml?branch=main&style=flat-square&label=ci&logo=githubactions&logoColor=7dcfff&labelColor=16161e)](https://github.com/mustang6139/sdrtop/actions/workflows/ci.yaml)
[![stars](https://img.shields.io/github/stars/mustang6139/sdrtop?style=flat-square&labelColor=16161e&color=1f2335&logo=github&logoColor=bb9af7)](https://github.com/mustang6139/sdrtop/stargazers)
[![updated](https://img.shields.io/github/last-commit/mustang6139/sdrtop?style=flat-square&labelColor=16161e&color=1f2335&label=updated)](https://github.com/mustang6139/sdrtop/commits)

[**sdrtop**](https://github.com/mustang6139/sdrtop) is a terminal app for software defined radio. You plug in an SDR dongle, tune it somewhere, and it shows you what is actually on the air: a live spectrum, a scrolling waterfall, signal measurements, and for FM broadcast the station name and track title your car radio would display. Keyboard only, and light enough that a Raspberry Pi does not complain about it.

Part of why it exists is that the cyberdeck crowd never really got a good option. SDR software tends to come in two shapes: large desktop applications that want a mouse, a wide screen and a decent GPU, or terminal tools that print a few numbers and stop there. Neither is much help when the whole rig fits in a lunchbox and you are sitting on a hillside with it. So sdrtop is built for that case, and presets and themes both live in a TOML file you can rearrange, because a field setup should still look like something you chose rather than something you settled for.

The other half of the reason is selfish. I wanted to understand radio properly instead of just using it, and the surest way to understand something is to be forced to implement it. So `signal/` does not call a DSP library. The maths is written out by hand, which took considerably longer and taught me considerably more.

What ended up in there:

- an **FFT engine** with exponential smoothing and noise floor tracking, so the spectrum reads as a signal instead of a flickering mess
- an **FM demodulator** that separates the MPX baseband, detects the stereo pilot, and picks out CTCSS sub-audible tones
- an **RDS decoder** running off the 57 kHz subcarrier: station name, PI code, programme type and RadioText, with accented characters and enough tolerance to keep going when blocks drop

Around that sits a hardware layer for RTL-SDR and HackRF, and a config file meant to be read by humans.

![sdrtop pointed at its own source tree: a spectrum where each module is a frequency bin, with a marker parked on the signal module](assets/self-scan.svg)

It is niche, and I have no illusions about that. It is also, by a wide margin, the most I have ever learned from one repository.

---

## Also in the tree

### [homescape](https://github.com/mustang6139/homescape)

> [!NOTE]
> **Parked for now.** I can only really hold one project in my head at a time, and at the moment that project is sdrtop. homescape is not abandoned, it is queued. I will come back to it.

**A self-hosted homelab dashboard that ships as one static binary.** Go on the back, Svelte on the front, SQLite underneath. The frontend is embedded into the Go binary at build time, so deploying it means copying a single file onto a machine. Nothing to install next to it, nothing extra to keep patched.

The part I am happiest with is that the dashboard is yours to assemble. You build it from the web interface: drop in widgets, point them at whatever you are actually running, and the layout is saved as a portable JSON document. Widgets reference your services by handle rather than by URL, so you can hand that document to someone else without handing over your credentials with it. The backend does the polling and pushes updates over SSE, which means the browser never talks to your services directly.

Being Go all the way down keeps it thin, so it sits comfortably on the kind of hardware a homelab actually runs on rather than the kind people photograph.

Around 7 500 lines across the two languages, 87 tests, CI and a Makefile.

### [diting_droidspaces_kernel](https://github.com/mustang6139/diting_droidspaces_kernel)

**A kernel build toolkit for turning a retired phone into a homelab node.** My old Xiaomi 12T Pro was sitting in a drawer with flagship silicon in it, doing nothing, while I was reading spec sheets for single board computers that were slower than it. That felt like the wrong way round.

So this rebuilds the LineageOS kernel for that device with the pieces Linux containers need: namespaces and cgroups switched on, kernel config patched, KernelSU-Next integrated. What comes out is a phone that runs containers, has its own battery, and draws less power than anything else I own.

It solved exactly one problem, and that problem was mine. I wrote it down in case anyone else has the same drawer.

---

Systems. Frontend. Embedded. Not a personality trait, three repos that prove it.

---

## The honest version

And if you are reading this in a professional capacity: yes, I built an animated terminal instead of updating my CV. I would like that noted as a strength.

Right now this is not my day job. It is the thing I do after the day job ends, and I would take it full time in a heartbeat. Everything here exists for exactly one reason: I wanted it to exist, so I built it. I do not really believe in picking one lane and defending it for life, so if something looks interesting I will walk straight into it and figure out the rest on the way. Rust is where I spend most of my time right now, and it is usually the least interesting part of the decision.

---

## The queue

There is a long list of things I want to build after this, and it grows faster than I can close it. Some of it is tooling, some of it is art, and one of them is a slow burn worldbuilding project I am writing the lore for before a single line of code exists. It will get its turn eventually.

I have made my peace with the backlog. The parked notice on homescape further up is not an accident, it is a demonstration.

## Contact

[viktor.laszlo92@protonmail.com](mailto:viktor.laszlo92@protonmail.com). For anything that is not a scam.

## Buy me a resistor

If something I built was useful to you, there is a tip jar here: [Ko-fi ↗](https://ko-fi.com/mustang6139). Absolutely no obligation. Parts just have this habit of not buying themselves.

---

Thanks for scrolling this far. Most people do not.

**MusiThang**

<details>
<summary><sub><code>0x7FFF0F</code></sub></summary>

---

[![ ](.thalos/judges.svg "three sit. only one of them is still listening.")](#musithang)

</details>

<!--
[THALOS-IV // KERNEL_RESIDUE]
ADDR_SPACE: 0x7FFF00..0x7FFF0F
PARITY_CHECK: DEGRADED (0x04)
LANG_FILTER: UNLOADED

DIOGEN_OS: "You opened the raw source expecting clean Markdown.
You brought your own entropy into this file.
The memory buffer at 0x7FFF00 is already leaking into your DOM."
-->
