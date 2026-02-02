# Deployment Guide for Better Claw Landing Page

## Architecture Overview

The Better Claw landing page is a **simple, zero-backend static site** that:

1. **Reads from `manifest.json`** at runtime via JavaScript `fetch()`
2. **Auto-updates** when you push new cron jobs to the repo
3. **No build step** required - just push and go
4. **Works anywhere** - GitHub Pages, Netlify, Vercel, or any static host

## How It Works

```
┌─────────────────────────────────────┐
│  Add new cron job JSON file         │
│  jobs/category/new-job.json         │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Update manifest.json                │
│  (manually or via script)            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  git push                            │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  GitHub Pages / Host auto-deploys   │
│  New job appears instantly!          │
└─────────────────────────────────────┘
```

## Deployment Options

### Option 1: GitHub Pages (Recommended)

**Easiest setup:**

1. Go to your GitHub repo settings
2. Navigate to **Pages** section
3. Set source to **main branch** → **/ (root)**
4. Save

Your site will be live at: `https://yourusername.github.io/better-claw/`

**Auto-deployment:**
- Every push to `main` automatically rebuilds the site
- No GitHub Actions workflow needed
- Manifest.json changes are live immediately

### Option 2: Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy)

1. Connect your GitHub repo
2. No build command needed
3. Publish directory: `/` (root)
4. Auto-deploys on push

### Option 3: Vercel

1. Import GitHub repo
2. Framework: **Other**
3. No build settings needed
4. Auto-deploys on push

### Option 4: Any Static Host

Upload these files to any static web host:
```
index.html
manifest.json
jobs/ (directory)
```

That's it! No server-side rendering or build process required.

## Adding New Jobs

### Manual Method

1. Create new job file: `jobs/category/my-job.json`
2. Update `manifest.json`:
   ```json
   {
     "id": "my-job",
     "name": "My Job Name",
     "file": "jobs/category/my-job.json",
     "description": "What it does",
     "schedule": "Daily @ 9am UTC",
     "difficulty": "beginner",
     "recommended": false
   }
   ```
3. Push to GitHub
4. Site auto-updates ✨

### Automated Method (Future Enhancement)

You could add a script to auto-generate manifest.json:

```bash
#!/bin/bash
# scripts/generate-manifest.sh
# Scans jobs/ directory and builds manifest.json
```

This would make adding jobs even easier - just drop a JSON file and push!

## Customization

### Changing Colors

Edit CSS variables in `index.html`:

```css
:root {
  --primary: #FF5A36;    /* Main CTA color */
  --bg: #0a1720;         /* Background */
  --surface: #0e231f;    /* Card backgrounds */
  --text: #c9eadc;       /* Text color */
  --accent: #5fdfa2;     /* Highlights */
  --border: #6fbfa8;     /* Borders */
}
```

### Adding Sections

The HTML is vanilla JavaScript - easy to extend:
- Add new sections between `<header>` and `<footer>`
- Modify the job card template in the `<script>` section

## Zero Backend Benefits

✅ **No server costs** - Static hosting is free (GitHub Pages, Netlify, Vercel)  
✅ **Fast** - No database queries, just JSON fetch  
✅ **Reliable** - Nothing to crash or go down  
✅ **Simple** - No dependencies, frameworks, or build tools  
✅ **Secure** - No server-side code to exploit  
✅ **Auto-updates** - Push to git = live on site  

## Testing Locally

```bash
# Option 1: Python
python3 -m http.server 8000

# Option 2: Node.js
npx serve

# Then visit: http://localhost:8000
```

## Future Enhancements (Optional)

If you want to add more automation later:

1. **GitHub Action to generate manifest.json** from jobs/ directory
2. **Search functionality** via client-side filtering
3. **Job preview** (show the actual JSON on hover)
4. **Tags/filtering** by difficulty, category, requirements
5. **One-click install** buttons (deeplink to OpenClaw CLI)

But the current setup works perfectly without any of these!
