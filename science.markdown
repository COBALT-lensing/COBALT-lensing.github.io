---
layout: page
title: The science of self-lensing
permalink: /science/
---

## What is self-lensing?

Lensing comes in all shapes and sizes but in all cases rests on the principle of curved paths of light (geodesics) in curved space-time. Over the preceding decades, a number of surveys (notably by [OGLE](https://ogle.astrouw.edu.pl/)) have detected large numbers of micro-lensing events associated with foreground lenses passing in front of background stars in the Magellanic clouds and Galactic bulge. 

Similar in nature but harder to detect is self-lensing which occurs in a binary system. When the compact object (white dwarf, neutron star or black hole - or something even more exotic) passes in front of the normal star then lensing of the light occurs. 

Self-lensing has been located in three white dwarf systems to date. The hunt is now on to find the neutron stars and black holes.

# The maths

As described across several seminal papers ([Witt & Mao 1994](https://ui.adsabs.harvard.edu/abs/1994ApJ...430..505W/abstract); [Gould 1995](https://ui.adsabs.harvard.edu/abs/1995ApJ...446..541G/abstract); [Agol 2002](https://ui.adsabs.harvard.edu/abs/2002ApJ...579..430A/abstract); [Agol 2003](https://ui.adsabs.harvard.edu/abs/2003ApJ...594..449A/abstract)), the self-lensing signal depends on some key characteristics of the system, notably the masses of the star and lens, radius of the source star, binary separation, impact parameter and limb darkening. The full equations are implemented in the code found here: <ADDURL for the current code> but a simplified picture is shown below.

<img src="https://render.githubusercontent.com/render/math?math=R_{E}=\sqrt{\frac{4aGMsin(i)}{c^{2}}}">  
  
# Predicted  numbers
  
Determining the numbers of self-lensing systems is not straightforward and requires us to first simulate the binary population of the Milky Way. For this, we used the population synthesis code, [STARTRACK](https://ui.adsabs.harvard.edu/abs/2008ApJS..174..223B/abstract) and followed the evolution of the binaries. Allowing for random inclinations then allows us to determine how many systems might be oriented in such a way as to produce a detectable self-lensing signal by a variety of instruments. The numbers which should be accessible to the [Transiting Exoplanet Survey Satellite (TESS)](https://tess.mit.edu/), [Zwicky Transient facility (ZTF)](https://www.ztf.caltech.edu/) and Vera C. Rubin [Legacy Survey of Space and Time (LSST)](https://www.lsst.org/) are shown below and in [Wiktorowicz et al. 2021](https://ui.adsabs.harvard.edu/abs/2021MNRAS.507..374W/abstract) as function of the key system parameters: Einstein crossing time (<img src="https://render.githubusercontent.com/render/math?math=\tau">), peak magnification (<img src="https://render.githubusercontent.com/render/math?math=\mu">), compact object mass and source star mass. 
