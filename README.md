[![License](https://img.shields.io/github/license/xAkre/Wuthering-Waves-RPC?style=for-the-badge)](https://github.com/xAkre/Wuthering-Waves-RPC/blob/master/LICENSE.md)
[![Downloads](https://img.shields.io/github/downloads/xAkre/Wuthering-Waves-RPC/total?style=for-the-badge)](https://github.com/xAkre/Wuthering-Waves-RPC/releases)
[![PyPresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)
![Language](https://img.shields.io/github/languages/top/xAkre/Wuthering-Waves-RPC?style=for-the-badge)

# Wuthering Waves Discord Rich Presence

Enables Discord Rich Presence for Wuthering Waves
<div style="display: flex; flex-direction: column; gap: 10px">
    <div style="width: 100%; display: flex; gap: 10px; justify-content: center;">
        <img src="screenshots/light-db.png" style="width: 45%; height: 50%">
        <img src="screenshots/dark-db.png" style="width: 45%; height: 50%">
    </div>
    <div style="width: 100%; display: flex; gap: 10px; justify-content: center;">
        <img src="screenshots/dark-no-db.png"   style="width: 45%; height: 50%">
        <img src="screenshots/light-no-db.png" style="width: 45%; height: 50%">
    </div>
</div>

## Table of Contents

<ol>
    <li><a href="#features">Features</a></li>
    <li><a href="#installing">Installing</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#building-from-source">Building from source</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#warning">Warning</a></li>
</ol>

## Features

- RPC variants
  - Database access variant
    - This variant accesses the game's local database to retrieve information about the user's union level and region. You should note, however, that this could violate the game's terms of service, potentially leading to account suspension or banning
  - Non-Database access variant
    - This variant does not access the game's local database, eliminating the risk of violating the game's terms of service
- Automatic launch on startup
  - Allows the RPC application to start automatically when the user logs in, removing the need to manually start the application

## Installing

1. Download the [latest release](
    https://github.com/xAkre/Wuthering-Waves-RPC/releases/latest
) 
2. Run the setup executable
3. Go through the setup process
4. You're done!

You may delete the setup executable after installation

## Usage

1. Simply run the RPC application like any other program

## Building from source

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Run `build.bat`
4. The executable will be located in the `dist/` directory

# Issues

If you encounter any issues, please open an issue on the [issues page](https://github.com/xAkre/Wuthering-Waves-RPC/issues)

## Warning

This is a third-party application and is not affiliated with Wuthering Waves or its developers. Should you choose to use the RPC with the database access option, you do so at your own risk

