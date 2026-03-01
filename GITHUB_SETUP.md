# Connecting Your Code to GitHub

## Prerequisites

- Git installed locally (already done)
- A GitHub account
- GitHub CLI (`gh`) installed (optional but recommended)

## Steps

### 1. Create a GitHub Repository

**Option A: Using GitHub CLI**
```bash
gh repo create llamaindex --public --source=. --remote=origin
```

**Option B: Using GitHub Website**
1. Go to [github.com/new](https://github.com/new)
2. Enter repository name (e.g., `llamaindex`)
3. Choose public or private
4. Do NOT initialize with README, .gitignore, or license (you already have code)
5. Click "Create repository"

### 2. Add Remote Origin

If you created the repo via the website, connect it:
```bash
git remote add origin https://github.com/YOUR_USERNAME/llamaindex.git
```

Or using SSH:
```bash
git remote add origin git@github.com:YOUR_USERNAME/llamaindex.git
```

### 3. Stage and Commit Your Changes

```bash
git add .
git commit -m "Initial project setup"
```

### 4. Push to GitHub

```bash
git push -u origin main
```

## Verify Connection

Check your remote is configured:
```bash
git remote -v
```

## Common Issues

**Authentication failed**: Set up a personal access token or SSH key
- [GitHub Token Guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [SSH Key Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

**Remote already exists**: Remove and re-add
```bash
git remote remove origin
git remote add origin <your-repo-url>
```

…or create a new repository on the command line
```
echo "# llamaindex" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Twilightin/llamaindex.git
git push -u origin main
```

…or push an existing repository from the command line
```
git remote add origin https://github.com/Twilightin/llamaindex.git
git branch -M main
git push -u origin main
```