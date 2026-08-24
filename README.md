```
 ███╗   ██╗██╗██╗  ██╗██╗  ██╗██╗██╗
 ████╗  ██║██║██║ ██╔╝██║  ██║██║██║
 ██╔██╗ ██║██║█████╔╝ ███████║██║██║
 ██║╚██╗██║██║██╔═██╗ ██╔══██║██║██║
 ██║ ╚████║██║██║  ██╗██║  ██║██║███████╗
 ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
```

<img src="https://readme-typing-svg.demolab.com/?font=JetBrains+Mono&weight=500&size=17&duration=3000&pause=800&color=39D353&vCenter=true&width=700&lines=full-stack+developer+%E2%80%94+web+%2B+android;shipping+production+software+for+an+RBI-registered+NBFC;next.js+15+%C2%B7+typescript+%C2%B7+kotlin+%C2%B7+firebase;one+dev.+entire+stack." alt="typing" />

---

### `$ cat stack.yaml`

```yaml
frontend:
  framework:  Next.js 15 (App Router) · React 19
  language:   TypeScript
  styling:    Tailwind CSS · shadcn/ui · Framer Motion
  patterns:   RSC · Server Actions · SSG/ISR

mobile:
  language:   Kotlin
  ui:         Jetpack Compose · Material 3
  local:      Room · DataStore · Android Keystore
  arch:       MVVM · Coroutines · Flow

backend:
  baas:       Firebase (Auth · Firestore · Storage · Cloud Functions)
  runtime:    Node.js
  patterns:   REST · scheduled jobs · role-based access control

craft:
  deploy:     Vercel · Firebase Hosting · CI via GitHub Actions
  design:     Figma · Inkscape · brand systems + logo design
  daily:      Zorin OS · zsh · Neovim · git
```

---

### `$ whoami`

```bash
> nikhil sharma
> full-stack developer  ·  sikar, rajasthan (IN)  ·  BCA '23–'27
> role     : sole developer, technology & digital infrastructure
> org      : Shine Blue Hire Purchase Pvt. Ltd. (RBI-registered NBFC)
> scope    : public web · internal tooling · android apps · brand identity
> status   : open to freelance — web apps, android, design systems
```

I own the full delivery pipeline end to end — requirements, architecture, UI design, implementation, deployment, and maintenance. No handoffs, no team to hide behind. Everything below is running in production and used by real people.

---

### `$ ls -la ~/projects`

```bash
drwxr-xr-x   shine-blue-web/        next.js 15 · typescript · shadcn/ui     [LIVE]
drwxr-xr-x   payroll-attendance/    kotlin/compose + next.js · firebase     [PROD]
drwxr-xr-x   sentinelx/             kotlin · room · android keystore        [PROD]
drwxr-xr-x   filevault/             kotlin/compose · firestore realtime     [PROD]
```

<details>
<summary><b>shine-blue-web</b> — corporate site for an RBI-registered NBFC</summary>

<br>

Full ground-up rebuild of the company's public web presence. Next.js 15 App Router, TypeScript, Tailwind + shadcn/ui, deployed on Vercel.

- Six product verticals, multi-branch location data, career portal, EMI calculator
- Per-page SEO metadata, structured data, Lighthouse-tuned Core Web Vitals
- EmailJS-backed enquiry pipeline with client-side validation and spam guards
- Full accessibility and security pass — CSP headers, sanitized inputs, no exposed keys

`Next.js 15` `TypeScript` `Tailwind` `shadcn/ui` `Vercel`

</details>

<details>
<summary><b>payroll-attendance</b> — geofenced HR system, dual codebase</summary>

<br>

An Android app for employees and a Next.js admin dashboard for HR, sharing one Firebase backend.

- Geofenced attendance check-in validated against branch coordinates
- Leave management with approval chains and LOP-aware payroll computation
- Auto-generated PDF payslips and scheduled monthly runs via Cloud Functions
- Role-based access control separating employee, manager, and admin surfaces

`Kotlin` `Jetpack Compose` `Next.js` `Firebase` `Cloud Functions`

</details>

<details>
<summary><b>sentinelx</b> — offline-first encrypted vault for Android</summary>

<br>

A local-only secure vault built around hardware-backed cryptography. Nothing leaves the device.

- Keys generated and sealed in the Android Keystore, never persisted in plaintext
- Room persistence with a versioned migration path across six schema revisions
- Biometric unlock, session timeout, screenshot blocking
- Custom Compose design system with a dark, high-contrast visual language

`Kotlin` `Jetpack Compose` `Room` `Android Keystore`

</details>

<details>
<summary><b>filevault</b> — physical document tracking, digitized</summary>

<br>

Internal tool that maps a physical filing room (Series → Stack → Files 00–99) into a searchable, real-time index.

- Firestore realtime sync so every branch sees the same state instantly
- Hierarchical navigation mirroring the actual shelf layout
- Instant lookup that replaced a manual register used daily by staff

`Kotlin` `Jetpack Compose` `Firestore`

</details>

---

### `$ git log --oneline --graph`

<table>
<tr>
<td width="50%">

<img src="https://github-readme-stats.vercel.app/api?username=nikhilsharmaa733&show_icons=true&hide_border=true&theme=transparent&title_color=39D353&icon_color=39D353&text_color=8B949E&hide_title=true" alt="stats" />

</td>
<td width="50%">

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=nikhilsharmaa733&layout=compact&hide_border=true&theme=transparent&title_color=39D353&text_color=8B949E&langs_count=8" alt="languages" />

</td>
</tr>
</table>

<img src="https://streak-stats.demolab.com/?user=nikhilsharmaa733&hide_border=true&background=00000000&stroke=30363D&ring=39D353&fire=39D353&currStreakLabel=39D353&sideLabels=8B949E&dates=8B949E&currStreakNum=C9D1D9&sideNums=C9D1D9" alt="streak" />

---

### `$ cat philosophy.txt`

```
> ship it, then sharpen it — production teaches faster than planning
> design is not decoration; it is the interface contract with the user
> if it needs a manual, the UI failed
> one developer, full ownership, no excuses
```

---

### `$ ./connect.sh`

```bash
$ ./connect.sh --list

  [→] email      your.email@example.com
  [→] linkedin   linkedin.com/in/your-handle
  [→] portfolio  your-site.com
  [→] work       shinebluehpl.com

  status: available for freelance · web · android · brand systems
```

<sub><code>EOF</code> — thanks for scrolling. now go build something.</sub>
