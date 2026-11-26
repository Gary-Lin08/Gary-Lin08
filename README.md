<p align="center">
  <img src="assets/hero.svg" width="100%" alt="Gary Lin: on-device ML, 3D biomechanics, multi-agent tooling" />
</p>

<p align="center">
  <a href="https://cerebel.tech"><img src="https://img.shields.io/badge/Cerebel_AI-cerebel.tech-22D3EE?style=for-the-badge&labelColor=0A1022" alt="Cerebel AI" /></a>
  <img src="https://img.shields.io/badge/Based_in-Japan-F472B6?style=for-the-badge&labelColor=0A1022" alt="Based in Japan" />
  <img src="https://img.shields.io/badge/Focus-Perception_%C2%B7_Motion_%C2%B7_Agents-A78BFA?style=for-the-badge&labelColor=0A1022" alt="Focus" />
</p>

<br/>

### `$ whoami`

I build systems that **see, hear and understand human movement**, all the way from firmware on a pair of AR glasses to 3D musculoskeletal models in the cloud.

- 🥽 **Edge ML.** Tiny models that run on the glasses frame. My wake-word network has about 20k parameters and its C port matches PyTorch to 6 decimal places.
- 🦴 **Biomechanics.** Video goes to a 3D pose and body mesh, then OpenSim inverse kinematics produces joint angles and loads, and those feed coaching.
- 🤖 **Agent tooling.** Orchestrating teams of coding agents from one terminal.
- 🎯 **Principle.** The language model explains; deterministic tools compute. Every number a user sees should be traceable.

<br/>

## ◆ What I'm building

<p align="center">
  <img src="assets/cerebel-stack.svg" width="100%" alt="Cerebel system architecture: glasses, phone, cloud" />
</p>

<p align="center">
  <img src="assets/biomech.svg" width="100%" alt="Golf swing reconstructed as a skeleton with joint-angle curves" />
</p>

<br/>

## ◆ Featured work

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/Gary-Lin08/cerebel-wake-word"><img src="assets/card-wake.svg" width="100%" alt="Hey Cerebel wake word" /></a>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/Gary-Lin08/agent-team-cli"><img src="assets/card-agent.svg" width="100%" alt="agent-team-cli" /></a>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://gary-lin08.github.io/Calculus-BC-Quest/"><img src="assets/card-calculus.svg" width="100%" alt="Calculus BC Quest" /></a>
    </td>
    <td width="50%" valign="top">
      <sub><b>More in progress.</b> Most of the Cerebel stack (glasses firmware, reconstruction server, coaching agent) is closed-source for now. Happy to walk through it. Reach out via <a href="https://cerebel.tech">cerebel.tech</a>.</sub>
    </td>
  </tr>
</table>

<br/>

## ◆ Algorithm spotlight: keyword spotting on a glasses frame

<p align="center">
  <img src="assets/wake-pipeline.svg" width="100%" alt="Wake word pipeline: waveform, log-mel spectrogram, TC-ResNet, decision" />
</p>

<details>
<summary><b>How it works</b> (click to expand)</summary>
<br/>

| Stage | What happens |
|---|---|
| **(a) Audio** | 16 kHz mono from the frame microphone, sliding 1.5 s window |
| **(b) Features** | 40-band log-mel spectrogram, recomputed every 50 ms |
| **(c) Model** | TC-ResNet: temporal 1-D convolutions treat mel bands as channels, about 20k parameters and under 1M MACs |
| **(d) Decision** | Fires only when **two consecutive** scores clear θ = 0.85; the cloud then re-verifies |
| **Data** | 100% synthetic speech: 1,000+ TTS speakers, augmented with noise, room reverb, a glasses-mic frequency response, and "Hey …" half-phrases as hard negatives |

The C inference code is checked against PyTorch on every release, with a max absolute difference of 4 × 10⁻⁶.
→ [cerebel-wake-word](https://github.com/Gary-Lin08/cerebel-wake-word)

</details>

<br/>

## ◆ Toolbox

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" />
  <img src="https://img.shields.io/badge/Core_ML-0A84FF?style=flat-square&logo=apple&logoColor=white" />
  <img src="https://img.shields.io/badge/OpenSim-34D399?style=flat-square" />
  <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white" />
  <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=flat-square&logo=kaggle&logoColor=white" />
</p>

<br/>

<p align="center">
  <img src="assets/footer.svg" width="100%" alt="" />
</p>
