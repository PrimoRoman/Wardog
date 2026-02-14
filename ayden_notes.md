

brew install --cask miniconda
conda --version
> 25.11.1
python3 --version
> 3.9.6
conda create -n wardog python=3.9.6
conda init zsh # mac only, must open new terminal after running
conda activate wardog
> Success
* python3 warhammerclock.py
} Missing module. PyQt6
* pip3 install PyQt6
* python3 warhammerclock.py
> It just works. Sweet.