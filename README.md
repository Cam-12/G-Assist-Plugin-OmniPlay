# OmniPlay Plugin for NVIDIA G-Assist
OmniPlay is a G-Assist plugin that enriches the gaming experience with two main features:
1. 🎮 In-game note-taking
Players can record personal notes on the fly as they play.
2. 🔍 Game information search
OmniPlay can provide contextual descriptions about :
- characters
- missions
- story or lore
- specific game elements

It automatically queries community wikis such as Fandom and wiki.gg, with a fallback search system if no direct info is found.

# Setup
## Prerequisites
- Python 3.10 or higher installed
- NVIDIA G-Assist installed

# Installation
## Step 1 : Download the code
```bash
git clone <repo link>
```
Download the code from GitHub

## Step 2: Setup and Build
1. Run the setup script:
```bash
setup.bat
```
This installs all required Python packages.
2. Run the build script:
```bash
build.bat
```
This creates the executable and prepares all necessary files.

## Step 3: Install the Plugin
1. Navigate to the dist folder created by the build script
2. Copy the `omniplay` folder to:
```bash
%PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins
```
💡 Tip: Make sure all files are copied, including:
- The executable
- manifest.json

# How to Use
Try these commands:
- "Hey omniplay, note chest behind wall in Elden Ring"
- "Hey omniplay, who is Melina in Elden Ring?"

# Troubleshooting Tips
The plugin logs all activity to:
```bash
%USERPROFILE%\omniplay-plugin.log
```

Recording note location :
```bash
%USERPROFILE%\GAssistNotes
```
# Want to Contribute?
All contributions are welcome!
Whether you want to fix a bug, improve a feature, or simply propose an idea, don't hesitate to participate.

🚀 How to contribute :
- Fork this repository.
- Create a branch (git checkout -b feature/my-feature).
- Commit your changes (git commit -m ‘Add feature’).
- Push your branch (git push origin feature/my-feature).
- Open a Pull Request.

Thank you for helping to improve this project! 🙌

# License
This project is licensed under the Apache License 2.0 – see the [LICENSE](LICENSE) file for details.
