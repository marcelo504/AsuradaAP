# Asurada - Fuzzy Logic Controller based on GAs Autopilot Project
KSP Autopilot for Final Rendezvous and Docking Operations, built up using kRCP mod for Kerbal Space Program.

## Dependences:
* [kRPC](https://krpc.github.io/krpc/index.html)

## System Components:  

## Fuzzy Logic Controller
It is recommended to read the code before running, because KSP ip and port need to be configured manually
```console
sudo python3 asuradaAP.py
```

## Genetic Algorithm
Asurada's final version and training was implemented in this folder, once again it is recommended to read the code before running it.  
To Run Asurada in game use:
```console
sudo python3 asurada_interface.py <ksp_ip>
```
To start training, use:
```console
sudo python3 trainer_ga.py
```
