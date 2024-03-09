---
layout: default
---

# Electromagnetic Field 2024 Shuttle Bus

We are be providing a shuttle bus service between Ledbury train station 
and the EMF site. Timetables, and real-time tracking can be accessed via the
link in the menu. We will attempt to align the shuttle bus service with the
arrival and departure times of the trains, but this might not always be possible.

## Cost

There is no additional cost for the shuttle service, it is included in your 
admission ticket.

## Luggage

The shuttle service will be provided by coaches, with a large amount of luggage
space available underneath. Carriage of anything that looks dangerous is at
the driver's discretion.

## Lost property

If you lose something on the shuttle bus, please contact the EMF helpdesk at 
[contact@emfcamp.org](mailto:contact@emfcamp.org) and we will do our best to
reunite you with your lost property.

## Delay repay

Delay repay will only be accepted with the following documentation:
* Real-time data showing the exact departure and arrival time
* A delay confirmation stamp from a DB mainline station
* A confirmation stamp available from the security office at 38C3

This must all be printed in lowercase black ballpoint on your EMF Delay Repay 
Form, and must be dated within 12 months.

## APIs

This wouldn't be an EMF project without some APIs. The following methods to
access Transport for EMF data are available:

### GTFS and GTFS-RT

Specification: [GTFS](https://gtfs.org/)  
GTFS feed: `https://tracking.tfemf.uk/media/gtfs.zip`  
GTFS-RT feed: `https://tracking.tfemf.uk/media/gtfs-rt.pb`

### HACON HAFAS

Licensing restrictions prevent public distribution of the HAFAS API specification,
but its the same one used by Deutsche Bahn and other European rail operators. 
Message Q ([magicalcodewit.ch](https://magicalcodewit.ch)) if you have questions 
about our specific implementation.

HAFAS base URL: `https://tracking.tfemf.uk/hafas` (not yet active)