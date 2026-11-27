<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.r5.svg">
  <img src="assets/header-light.r5.svg" width="100%" alt="Kaijun Lin. Building Cerebel AI, wearable perception that understands how people move.">
</picture>

I work on [Cerebel AI](https://cerebel.tech): AR glasses that see and hear what you do, and a cloud pipeline that turns phone video into joint angles and coaching feedback. Based in Boston.

### Cerebel glasses

Monocular AR glasses with a green microLED waveguide display, a camera and a microphone. A small Linux board in the frame handles capture and display; captions, translation and the voice assistant run together with a phone and a cloud service.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/glasses-dark.r5.svg">
  <img src="assets/glasses-light.r5.svg" width="100%" alt="Figure 1. The Cerebel glasses rendered from the production CAD.">
</picture>

### Motion analysis

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/system-dark.r5.svg">
  <img src="assets/system-light.r5.svg" width="100%" alt="Figure 2. System overview: glasses, phone, cloud.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/recon-dark.r5.svg">
  <img src="assets/recon-light.r5.svg" width="100%" alt="Figure 3. One recorded session: 77 body joints from GEM-X and joint angles from OpenSim.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/golf-dark.r5.svg">
  <img src="assets/golf-light.r5.svg" width="100%" alt="Figure 4. A golf swing in 3D with pelvis and thorax rotation.">
</picture>

### [cervical-retarget](https://github.com/Gary-Lin08/cervical-retarget) &nbsp;<sub>open source · Python · OpenSim</sub>

An articulated neck and head for markerless OpenSim inverse kinematics. Two cervical joints are added to the Rajagopal model and driven by landmarks derived from GEM-X joints; on two recorded sessions, head-orientation error drops by 34–36%.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/crhero-dark.r5.svg">
  <img src="assets/crhero-light.r5.svg" width="100%" alt="Figure 5. Baseline with the skull welded to the torso vs the articulated neck on one recorded session, with per-frame head orientation error.">
</picture>

### [Hey Cerebel](https://github.com/Gary-Lin08/cerebel-wake-word)

The wake word that runs on the glasses: a TC-ResNet with about 20k parameters, written in C for the firmware and trained only on synthetic speech (11,843 clips).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/wake-dark.r6.svg">
  <img src="assets/wake-light.r6.svg" width="100%" alt="Figure 6. Keyword spotting pipeline: waveform, log-mel, TC-ResNet, decision.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/results-dark.r6.svg">
  <img src="assets/results-light.r6.svg" width="100%" alt="Figure 7. Detection rate and false accepts per hour, v1 and v2.">
</picture>

### [Tennis AI](https://github.com/Gary-Lin08/Tennis-AI)

A monocular perception stack for tennis. A TrackNet heatmap network finds the ball in every frame, a court homography puts each detection in metres, a physics-based detector finds bounces and calls them in or out, MoveNet pose feeds a recurrent stroke classifier, and a state machine turns the events into rallies and a score. The networks run on device as Core ML models.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/tennis-dark.r6.svg">
  <img src="assets/tennis-light.r6.svg" width="100%" alt="Figure 8. Ball tracking on a calibrated court, with a bounce map.">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/tmodel-dark.r6.svg">
  <img src="assets/tmodel-light.r6.svg" width="100%" alt="Figure 9. The Tennis AI model stack: GridTrackNet, court homography, bounce detection, MoveNet, GRU stroke classifier, rally and score state machine.">
</picture>

### Other

- [agent-team-cli](https://github.com/Gary-Lin08/agent-team-cli): run several coding agents in parallel in split terminal panes (TypeScript).

Python · PyTorch · C · Swift / Core ML · TypeScript · OpenSim
