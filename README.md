# SLM

Type this below in the terminal in the same directory of Modelfile 
to use this file `ollama create <name of bot> -f ./Modelfile`
Thereafter, to use, run `ollama run <name of bot>`

# Quantization for bigger models

Tweak ollama to run bigger models on the machine
OLLAMA_FLASH_ATTENTION=true ollama serve
or
OLLAMA_KV_CACHE+TYPE=f16 ollama serve
Need to try the settings to see which work better
ASITOP installed for monitoring Mac resources, for Linux us NVTOP
https://github.com/tlkh/asitop