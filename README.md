# Programming a Drone Parcel Delivery System
THis repository looks at the problems associated with developing a system of drones working autonomously to delvier packages across a campus/local area. The drones are expected to automatically reach different sites along the map and consist of an intelligent navigation and anti-collision system in place. This system requires that drones within the same zone utilize the same frequency for communication. This leads to three challenges which will be addressed in this project:

1. The users of the service would like to have a graphical system to search possible destinations from aalready existing database.
2. Each zone will require its own frequency. To achieve this, a system of zoning needs to be put in place and we must guaranty that two neighboring zones do not share frequencies.
3. Lastly, we are required to aid the drones by searching for the shortest path which they can take while doing multiple deliveries at any given instant. This needs to be done as efficiently as possible.

## Code Structure
The solutions to these problems are discussed over multiple `Python` Jupyter notebooks:
1. `Indexing.ipynb`: Tackles the problem of efficiently search for all zones that match a prefix given by the user from a preset database.
2. `Graphical Interface and Zoning`: Tackles the problem of zoning by creating Voronoi diagrams between each site, ensuring that within any zone, the nearest site is the one corresponding to that zone only.
3. `Maps and Graph Coloring`: Graph coloring tackles the problem of assigning frequencies to each zone so that no two neighboring zones have the same frequency.
4. `Optimizing Package Delivery`: Solves the problem of finding the most efficient path to take given a list of sites to visit.

## Running the code
Executing the code is quite simple, and only requires Python3 and jupyter notebook installed. Each jupyter notebook can be excuted independant of the other.