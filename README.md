# musicNFTintegration

Thank you to 0xZurf and Afrideva for the huge help.

This code is used to pull Music NFT data from various sources and organizes the repository for filtering and discovery purposes.

More documenation on setting up the service to store data in google sheets here: https://erikrood.com/Posts/py_gsheets.html

Needed libraries:

- platform
- urllib #Web query integrator
- gql #Zora API interface
- gql import gql, Client #Zora API Client
- gql.transport.aiohttp import AIOHTTPTransport #Zora API Client
- pandas as pd #Used for Data trasnformation and database structuring
- json #Data trasnformation
- pygsheets #Google cloud integration
- requests #Web query integrator

A version of the filtering tool can be found here: https://datastudio.google.com/u/1/reporting/cd07d3ca-2dea-40c6-afbb-3fa018e22d0e/page/jR9uC

A DJ mix made from filtering for 'electronic' in tge "tags: field can be found here: https://soundcloud.com/muta_official/the-undergound-sessions-16

The set list with timestamps can be found here: https://datastudio.google.com/u/1/reporting/cd07d3ca-2dea-40c6-afbb-3fa018e22d0e/page/p_vk35lpttvc

More documentation on overall data structure of v.1 of the tool can be found here:https://datastudio.google.com/u/1/reporting/cd07d3ca-2dea-40c6-afbb-3fa018e22d0e/page/p_p1inexttvc

A version of the storage endpoint can be found here (this is the data souce for the google data studio interface): https://docs.google.com/spreadsheets/d/19I_3MT4Py6Kc_Oxjosv6kJkgp7l_iK62M7ra1Y_eNMM/edit?usp=sharing

Google data studio is an open source web based visualazation tool. The data source used can be replicated with this code and the interface can be repicated relatively easily.
