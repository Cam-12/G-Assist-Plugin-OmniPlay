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
setup.bat
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
