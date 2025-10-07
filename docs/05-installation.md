# Installation Guide

This guide will help you install `ephem` on macOS, Windows, or Linux. Choose the section that matches your operating system.

- [macOS](#macos)
- [Windows](#windows)
- [Linux](#linux)

<a name="macos"></a>
## macOS

### Prerequisites

First, you need Python 3.8 or later. Check if you have it:

```sh
python3 --version
```

If you see a version number like `Python 3.11.x` or higher, you're good to go! If not, install Python from [python.org](https://www.python.org/downloads/).

### Installing with pipx

`pipx` installs Python CLI applications in isolated environments, which is perfect for tools like `ephem`.

#### Step 1: Install pipx

If you have Homebrew (recommended):

```sh
brew install pipx
pipx ensurepath
```

Or install via Python:

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

After installation, **close and reopen your terminal** for the changes to take effect.

#### Step 2: Install ephem

```sh
pipx install ephem-cli
```

#### Step 3: Verify installation

```sh
ephem --version
```

You should see the version number printed out. Now you can run `ephem now` to cast your first chart!

<a name="windows"></a>
## Windows

### Prerequisites

You need Python 3.8 or later. Check if you have it by opening **PowerShell** or **Command Prompt** and running:

```powershell
python --version
```

If Python isn't installed, download it from [python.org](https://www.python.org/downloads/).

**Important:** During installation, check the box that says "Add Python to PATH".

### Installation with pipx

#### Step 1: Install pipx

Open PowerShell or Command Prompt and run:

```powershell
python -m pip install --user pipx
python -m pipx ensurepath
```

**Close and reopen PowerShell/Command Prompt** after this step.

#### Step 2: Install ephem

```powershell
pipx install ephem-cli
```

#### Step 3: Verify installation

```powershell
ephem --version
```

You should see the version number. Now try `ephem now` to cast your first chart!

### Troubleshooting Windows

**If you get "command not found" errors:**

1. Make sure Python is in your PATH (search Windows for "Environment Variables")
2. Look for the pipx installation directory (usually `%USERPROFILE%\.local\bin` or `%APPDATA%\Python\Scripts`)
3. Add that directory to your PATH


<a name="linux"></a>
## Linux

### Stable release

The stable release of `ephem` can be installed directly from [PyPI](https://pypi.org/project/ephem-cli):

```sh
# Run directly without installing
uvx ephem-cli

# Or install globally
uv tool install ephem-cli

# Traditional methods
pip install --user ephem-cli    # if you use pip
pipx install ephem-cli          # if you use pipx, especially Debian/Ubuntu
```

### Building from source

To build from the `main` branch:

```sh
git clone https://codeberg.org/sailorfe/ephem.git
cd ephem
uv run -m ephem.cli             # run directly
# or
uv sync && uv run -m ephem.cli  # for development
```

### Testing pre-releases

You can install the current pre-release from Codeberg:

```sh
# Run pre-release directly from Codeberg
uvx --from https://codeberg.org/sailorfe/ephem ephem-cli

# Or install pre-release
uv tool install ephem-cli \
  --index https://codeberg.org/api/packages/sailorfe/pypi/simple/ \
  --prerelease allow
```


## What's next?

Once installed, continue to [Getting Started](./10-getting-started.md) to cast your first chart and configure your default location!

### Getting help

If you run into issues:

- Check that Python 3.8+ is installed: `python --version` or `python3 --version`
- Make sure the installation directory is in your PATH
- Hit up the Discord or [file an issue](https://codeberg.org/sailorfe/ephem/issues) OS details and error messages
