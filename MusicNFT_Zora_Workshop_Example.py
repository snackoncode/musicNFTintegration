from platform import node, platform
from urllib import request
import gql
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import json
import pygsheets
import requests

# Define transport variable
transport = AIOHTTPTransport(url="https://api.zora.co/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

#Define MusicNFT_DF

MusicNFT_DF = pd.DataFrame(columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate', 'recordLabel','publisher','license', 'image', 'losslessAudio', 'duration'])

# Mint songs: 0x2B5426A5B98a3E366230ebA9f95a24f09Ae4a584

#var reset
hasNextPage = True
counter = 0
endCursor = ""
TokenTracker = 0

#Mint Songs Query
while hasNextPage == True:
    counter = counter + 1

    if counter == 1:
        query_string = """
                query MyQuery {
                mints(pagination: {limit: 50, after: ""}, where: {collectionAddresses: "0x2B5426A5B98a3E366230ebA9f95a24f09Ae4a584"}) {
                    nodes {
                    mint {
                        collectionAddress
                    }
                    token {
                        tokenId
                        metadata
                        collectionName
                    }
                    }
                    pageInfo {
                    endCursor
                    hasNextPage
                    }
                }
                }


        """

    if counter > 1:
        query_string = """
                query MyQuery {
                mints(pagination: {limit: 50, after: "%s"}, where: {collectionAddresses: "0x2B5426A5B98a3E366230ebA9f95a24f09Ae4a584"}) {
                    nodes {
                    mint {
                        collectionAddress
                    }
                    token {
                        tokenId
                        metadata
                        collectionName
                    }
                    }
                     pageInfo {
                     endCursor
                     hasNextPage
                    }
                }
                }


        """ % endCursor

    #print(query_string)

    # Provide a GraphQL query
    query = gql(query_string)

    # Execute the query on the transport
    result = client.execute(query)

    df = pd.DataFrame.from_dict(result)


    node_page = df['mints'][0]

    for i in range(len(node_page)):

        #If token is missing metadata, skip and trigger message
        if (df['mints'][0][i]['token']['metadata']) is None:
            print('Token ID:' + str(df['mints'][0][i]['token']['tokenId'])+ " is missing!!!!")
            continue

        #Grab metadata tag for each node

        plat = df['mints'][0][i]['token']['collectionName']
        artist = df['mints'][0][i]['token']['metadata']['artist']
        projectTitle = df['mints'][0][i]['token']['metadata']['project']['title']
        songTitle = df['mints'][0][i]['token']['metadata']['title']
        bpm = df['mints'][0][i]['token']['metadata']['bpm']
        key = df['mints'][0][i]['token']['metadata']['key']
        genre = df['mints'][0][i]['token']['metadata']['genre']
        tags = df['mints'][0][i]['token']['metadata']['tags']
        locationCreated = df['mints'][0][i]['token']['metadata']['locationCreated']
        originalReleaseDate = df['mints'][0][i]['token']['metadata']['originalReleaseDate']
        recordLabel = df['mints'][0][i]['token']['metadata']['recordLabel']
        publisher = df['mints'][0][i]['token']['metadata']['publisher']
        license = df['mints'][0][i]['token']['metadata']['license']

        image = df['mints'][0][i]['token']['metadata']['image']
        losslessAudio = df['mints'][0][i]['token']['metadata']['losslessAudio']
        duration = df['mints'][0][i]['token']['metadata']['duration']
        tokenID = df['mints'][0][i]['token']['tokenId']
        #print(plat)

        tempData = [[plat,artist,projectTitle,songTitle,bpm,key,genre,tags,locationCreated,originalReleaseDate,recordLabel,publisher,license, image, losslessAudio, duration, tokenID]]
        temp_MusicNFT_DF = pd.DataFrame(tempData, columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate','recordLabel','publisher','license', 'image','losslessAudio', 'duration','tokenID'])

        MusicNFT_DF = pd.concat([MusicNFT_DF,temp_MusicNFT_DF])

        # print("Platform: " + str(platform))
        # print("Artist: " + str(artist))
        # print("Project Title: " + str(projectTitle))
        # print("Song Title: " + str(songTitle))
        # print("bpm: " + str(bpm))
        # print("key: " + str(key))
        # print("genre: " + str(genre))
        # print("tags: " + str(tags))
        # print("locationCreated: " + str(locationCreated))
        # print("originalReleaseDate: " + str(tags))
        # print("record Label: " + str(recordLabel))
        # print("publisher: " + str(publisher))
        # print("license: " + str(license))
        # print("image: " + str(image))
        # print("Audio: " + str(losslessAudio))
        # print("Duration: " + str(duration))
    
    TokenTracker =  len(node_page)

    endCursor = df['mints'][1]['endCursor']
    hasNextPage = df['mints'][1]['hasNextPage']

    #print(endCursor)
    #print(hasNextPage)

print("MintsongsV2 library via Zora API done processing...")
print("Total songs in library... " + str(len(MusicNFT_DF)) + " songs")
print(MusicNFT_DF)

#Pass google sheets service authentication
gc = pygsheets.authorize(service_file='/Users/Your/FilePath/to/googleauthenticate.json') #Google service authenication JSON, see read me for more info

#Push dataframe to google sheets

sh = gc.open('Name of google sheet') #It will paste the dataframe on the first sheet

MusicNFT_DF_gs = sh[0]

MusicNFT_DF_gs.set_dataframe(MusicNFT_DF,(1,1))