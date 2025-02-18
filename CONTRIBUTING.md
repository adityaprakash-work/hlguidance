## Contributing Using Git-Flow

This project follows the **Git-Flow** branching model. Below are step-by-step instructions for contributing using the `git-flow` command-line tool.

### 1. Install Git-Flow
If you haven't installed `git-flow`, do so with:
```sh
# Debian/Ubuntu
sudo apt install git-flow

# macOS (via Homebrew)
brew install git-flow-avh
```

### 2. Initialize Git-Flow
Before contributing, ensure Git-Flow is initialized in your local repository:
```sh
git flow init
```
You can accept the default branch names or customize them as needed.

### 3. Start a New Feature
All feature development must happen in a feature branch:
```sh
git flow feature start <feature-name>
```
Work on your feature, commit your changes:
```sh
git add .
git commit -m "Describe your change"
```

To push your feature branch to the remote repository:
```sh
git flow feature publish <feature-name>
```

### 4. Update Your Feature Branch
If changes have been merged into `develop`, sync your branch:
```sh
git checkout develop
git pull origin develop
git checkout feature/<feature-name>
git merge develop
```
If conflicts arise, resolve them, then:
```sh
git add .
git commit -m "Resolve merge conflicts"
```

### 5. Finish a Feature
Once the feature is complete and tested:
```sh
git flow feature finish <feature-name>
```
This merges the feature into `develop` and deletes the local branch.

Push the updated `develop` branch:
```sh
git push origin develop
```

### 6. Start a Release
When preparing for a new release:
```sh
git flow release start <version-number>
```
Update version numbers and necessary documentation. Commit those changes.

Push the release branch if collaboration is needed:
```sh
git flow release publish <version-number>
```

### 7. Finish a Release
To finalize the release:
```sh
git flow release finish <version-number>
```
This:
- Merges the release into `main`
- Tags the release
- Merges the release into `develop`
- Deletes the local release branch

Push the changes and tags:
```sh
git push origin main
git push origin develop
git push --tags
```

### 8. Hotfixes (Critical Fixes for Production)
For urgent fixes in `main`:
```sh
git flow hotfix start <hotfix-name>
```
Make and commit the necessary changes.

Finish the hotfix:
```sh
git flow hotfix finish <hotfix-name>
```
This:
- Merges the fix into `main`
- Tags the hotfix
- Merges it into `develop`
- Deletes the local hotfix branch

Push the changes:
```sh
git push origin main
git push origin develop
git push --tags
```

### 9. Handling Bugs in Released Versions
If the bug affects `develop` only:
```sh
git flow feature start bugfix/<issue-number>
```
If the bug affects `main`, treat it as a hotfix.

### 10. Keeping Your Fork Up to Date
If you're working on a fork, update it regularly:
```sh
git remote add upstream <original-repo-url>
git fetch upstream
git checkout develop
git merge upstream/develop
git push origin develop
```