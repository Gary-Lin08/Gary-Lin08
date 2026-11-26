<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.r3.svg">
  <img src="assets/header-light.r3.svg" width="100%" alt="Kaijun Lin. On-device perception, human motion, agent systems.">
</picture>

I build perception for wearables. On one end are small models that run on a pair of AR glasses; on the other is a cloud pipeline that turns ordinary video into a musculoskeletal model of how someone moves. In between, a language model explains what happened, but every number it quotes comes from a deterministic tool.

<p>
  <a href="https://cerebel.tech"><b>Cerebel AI</b></a> &nbsp;·&nbsp; Wearable Motion Intelligence &nbsp;·&nbsp; <a href="https://cerebel.tech">cerebel.tech</a> &nbsp;·&nbsp; Japan
</p>

<table>
  <tr>
    <td width="33%" valign="top"><b>Edge perception</b><br><sub>Wake words, capture and display on a 128 MB ARM board. Every model has to earn its milliwatts.</sub></td>
    <td width="33%" valign="top"><b>Human motion</b><br><sub>Monocular video to body mesh to musculoskeletal inverse kinematics, with joint angles you can defend.</sub></td>
    <td width="33%" valign="top"><b>Agent systems</b><br><sub>Language models that orchestrate tools and other agents, and never invent a number.</sub></td>
  </tr>
</table>

<br>

### Cerebel glasses &nbsp;<sub>closed source</sub>

A monocular waveguide display, a camera and a microphone on a lightweight Linux frame. The glasses run captions, translation, a voice assistant and photo capture, and they show coaching cues mid-session.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/glasses-dark.r3.svg">
  <img src="assets/glasses-light.r3.svg" width="100%" alt="Figure 1. Line drawing of the Cerebel glasses with component callouts, and the 640 by 480 green display.">
</picture>

<sub><b>Figure 1.</b> <i>The glasses, as a line drawing.</i> Callouts mark where each part sits. On the right, the display at its native resolution: the wearer asks about a swing and gets a number back.</sub>

<br>

### Cerebel motion stack &nbsp;<sub>closed source</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/system-dark.r3.svg">
  <img src="assets/system-light.r3.svg" width="100%" alt="Figure 2. The Cerebel stack: glasses, phone, cloud.">
</picture>

<sub><b>Figure 2.</b> <i>From a glance to a coaching cue.</i> Video (orange) is reconstructed into a musculoskeletal model in the cloud; audio (blue) is gated on the glasses by a 20k-parameter wake word.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/recon-dark.r3.svg">
  <img src="assets/recon-light.r3.svg" width="100%" alt="Figure 3. Input frame with 2D keypoints, a rotating body mesh, and a rotating musculoskeletal model.">
</picture>

<sub><b>Figure 3.</b> <i>Video to mesh to muscles.</i> The body mesh is estimated with GEM-X and joint kinematics are solved with <a href="https://opensim.stanford.edu/">OpenSim</a> inverse kinematics. The renderings here are my own schematic drawings, not output from either tool.</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/golf-dark.r3.svg">
  <img src="assets/golf-light.r3.svg" width="100%" alt="Figure 4. A golf swing reconstructed in 3D with swing plane, and thorax and pelvis rotation curves.">
</picture>

<sub><b>Figure 4.</b> <i>A golf swing in 3D.</i> The pelvis and thorax frames rotate on the swing plane. The shaded gap between their rotation curves is the X-factor, which peaks at the top of the backswing. Illustrative data.</sub>

<br>

### [Hey Cerebel](https://github.com/Gary-Lin08/cerebel-wake-word) &nbsp;<sub>PyTorch · C · speech synthesis</sub>

The glasses' wake word: a 20k-parameter temporal ResNet that runs in firmware. It was trained only on synthetic speech, 11,843 clips from more than 1,000 TTS voices.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/wake-dark.r3.svg">
  <img src="assets/wake-light.r3.svg" width="100%" alt="Figure 5. Keyword spotting pipeline: waveform, log-mel, TC-ResNet, decision.">
</picture>

<sub><b>Figure 5.</b> <i>Keyword spotting on a glasses frame.</i> A temporal ResNet over 40 mel bands. The C port that ships in firmware matches PyTorch to six decimal places.</sub>

<br>

### [Tennis AI](https://github.com/Gary-Lin08/Tennis-AI) &nbsp;<sub>SwiftUI · Core ML · Python</sub>

On-device ball tracking, pose and shot recognition for tennis practice video, plus an offline pipeline that splits rallies and keeps score.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/tennis-dark.r3.svg">
  <img src="assets/tennis-light.r3.svg" width="100%" alt="Figure 6. A ball track on a calibrated court, and a top-down bounce map.">
</picture>

<sub><b>Figure 6.</b> <i>Ball tracking on a calibrated court.</i> Four keypoints fix the court homography, and each bounce is projected onto the ground plane. Illustrative rally.</sub>

<br>

### Also

**[agent-team-cli](https://github.com/Gary-Lin08/agent-team-cli)** &nbsp;<sub>TypeScript · Ink · MCP</sub><br>
Runs a team of coding agents in parallel and streams each one into its own terminal pane. It works with Cursor, Claude Code and Codex.

**[Calculus BC Quest](https://gary-lin08.github.io/Calculus-BC-Quest/)** &nbsp;<sub>HTML</sub><br>
A browser practice game covering all ten AP Calculus BC units and past papers from 2017 to 2022.

<br>

### Tools

Python, PyTorch, C &nbsp;·&nbsp; Swift, Core ML &nbsp;·&nbsp; TypeScript, React, Node &nbsp;·&nbsp; OpenSim &nbsp;·&nbsp; FastAPI, Supabase

<br>

<sub>Reach me through <a href="https://cerebel.tech">cerebel.tech</a>. Every figure on this page is hand-built SVG, generated by the scripts in <a href="tools/">tools/</a>.</sub>
