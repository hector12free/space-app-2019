# space-app-2019

This work is for NASA Space Apps Hackathon 2019. 

We are working on this challenge: "Orbital Scrap Metal — The Video Game".

https://2019.spaceappschallenge.org/challenges/stars/orbital-scrap-metal-the-video-game/details

# Pre-requsite
* download & install Anaconda
* create an environment with a specific version of Python, e.g. 2.7
* activate python
* install pygame
```bash
conda update conda
conda create -n pygame python=2.7
conda activate pygame
pip install pygame
```

Note: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

# TODOs
- [ ] avoid collision between satellite and collector
- [ ] make space junks move in different directions with satellite in the center of the map
- [ ] add multiple satellites
- [x] refractor: rename "collector" to "starShip"
- [ ] improve on starShip movement, make it (accelerate/decelerate) smoothly
- [ ] make starShip change movement direction (making turns, like a shark eating fishes)

# Reference
* https://2019.spaceappschallenge.org/challenges/
