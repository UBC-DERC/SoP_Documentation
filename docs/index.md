# UBC Dairy Education and Research Center Technical Documentation

The Dairy farm at UBC is a leading research instutution globally. Research into animal welfare on the farm has been cited more than 10,000 times, and policy developed through the farm and its researchers impacts millions of dairy cattle in Canada and around the world on a daily basis.

## Technology at the Farm

The farm has a range of equipment, suppliers, research tools and data sources. These include log books, daily work plans, cloud services, machine readouts, and other software sources.

Technology at the farm serves the dairy cattle, farm managers and researchers. All have different needs from the data generated, and there are different time-frames over which we need to retain the data:

* Some cows on the farm only "need" data about milk production up until their next milking period. This is the length of time required to know if a cow needs to be fetched and brought by a farm worker to the robot.
* A farm manager needs to know information about a calves weight through the entire weaning process, to assess growth and intervene if neccessary. Once a calf moves from the calf barn to the heifer barn, there is no need for this information.
* A researcher may want weight data across the weaning period, and all milking data for an individual cow, to assess how weight gain trajectories during the weaning period may impact long-term milk production.
* A funder or scientific publisher wants the raw data, and other data produced as part of a publication, and wants this stored in perpetuity on some data service.

The goal of a fully implemented system is to support all human and non-human workers at the Dairy farm.

## UBC Dairy Farm Technology Documentation

* [`ssh` and remote connections](docs/technical/ssh/index.md)
* [Video data](docs/technical/carmera/index.md)
* [Smart Plugs and IoT](docs/technical/smart_plugs/index.md)
* Milking Robots
* Automated Feeders
* Integrated Database
