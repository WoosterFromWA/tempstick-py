.. tempstick-py documentation master file, created by
   sphinx-quickstart on Mon Sep 12 15:45:30 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tempstick-py's documentation!
========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Purpose
=========

Create a python toolset for interacting with IdealSciences' `Temp°Stick™ <https://tempstick.com/>`_ climate sensor.

I came to this trying to find a way to integrate with `Home Assistant <https://home-assistant.io>`_, but at the time, there was no API. I did get a good start on a scraping tool for it, but never got so far as to create the integration in Home Assistant.

Lo-and-behold, I'm ready to start building the integration and come across a documented API from Temp°Stick™.

Without further ado, here's how to use it.

Installation
=============

In its pre-release state, it is recommended to explicity specify the version as shown below.

.. substitution-code-block:: console

   pip install tempstick-py==|ProjectVersion|

API Key
========

To use any of the methods or functions available in this package, an API key will need to be provided.

.. |far fa-eye| raw:: html

   <i class="far fa-eye"></i>

1. Go to https://temperaturestick.com/sensors/
2. Login or create account, as required
3. Click on **ACCOUNT**
4. Click on **</> Developers**
5. Click on **Show Key** |far fa-eye|
6. Copy the API key; save for future reference