Pygame Battletech - Documentation
#################################

Designed and built to provide a framework for building low-res games inspired
by GB Studio but without the virtual hardware restrictions. 

The real goal was to make it easy for me to create the kinds of games I'd like
to play or wished I could have played.

I used Python because I'm already familiar with it, it's easy to debug, and
it's portable. 

I intend to make the engine available to anyone who would like to use it. 

I've also started making a world builder to help with creating collision maps
and adding triggers to maps. The ultimate goal would be to enable authoring of
games from the world builder.

I'm trying to keep everything as simple as possible. I hope it could also be
useful as a holistic tool for creating role playing games.

Some of my insprations:

* Pokemon: Fire Red
* Battletech: The Crescent Hawk's Inception
* Shadowrun: Returns

Those are the kinds of games I'm trying to emulate.

Ideas
======

1. Ability to embed Python in the game file.
2. Implement more "actions" such as:
   
   * Choice selector - similar to message but also captures up/down and A/B keys and returns the selected value.
   * if/then or case statement
   * create/destroy sprites
   * create/destroy collisions
