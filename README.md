# Fishipus (or whatever I decide to call it)
This project is meant to provide a framework for future projects involving pygame, so I don't have to spend half of my time rewriting and modifying old code from previous projects. 

# What will it do?
It will handle physics, entity management, camera, animation, particle systems, ui, loading assets, tile and chunk systems, shaders (moderngl), rendering, audio and more for me

# Why do this
This will allow me to 'plug' this in to a project, or start a project from this so that I can just add my code & graphics, etc and have a fast, working game. I also have implemented module for shaders - using moderngl - which allows me to just write a fragment & a vertex shader and not have to worry about all the opengl stuff behind the scenes. For the entity management & physics, I can just inherit from the parent Entity class which handles rendering, physics and animation for me, and (if it is not the player) it will be automatically added to the EntityManager's entities. The EntityManager handles updating & rendering the entities, and uses a system of chunks/quads to optimise this. In the .__init__ method of each Entity (if it is not the player) it will add itself to this entity manager.
