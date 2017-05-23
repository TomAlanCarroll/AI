# AI
*Problems and solutions for various AI topics*

##How to Run

```
# OS X (Install homebrew first)
brew install sdl sdl_image sdl_mixer sdl_ttf portmidi mercurial
conda env create -f aind-environment-macos.yml
source activate aind
pip install git+https://github.com/hmmlearn/hmmlearn.git
pip install pygame

# Unix
conda env create -f aind-environment-unix.yml
source activate aindunix
pip install git+https://github.com/hmmlearn/hmmlearn.git
pip install pygame

# Windows
conda env create -f aind-environment-windows.yml
activate aindwindows
pip install hmmlearn-0.2.1-yourpythonwindows.whl
pip install pygame
```