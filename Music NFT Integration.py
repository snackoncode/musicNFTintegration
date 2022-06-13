from platform import node, platform
from urllib import request
import gql
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import pandas as pd
import json
import pygsheets
import requests

#Pass google sheets service authentication
gc = pygsheets.authorize(service_file='/Users/yourfilepath/googleservice.json') #Google service authenication JSON, see read me for more info

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://api.zora.co/graphql")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

#Define MusicNFT_DF

MusicNFT_DF = pd.DataFrame(columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate', 'recordLabel','publisher','license', 'image', 'losslessAudio', 'duration'])

# Mint songs: 0x2B5426A5B98a3E366230ebA9f95a24f09Ae4a584
# Catalog: 0x0bC2A24ce568DAd89691116d5B34DEB6C203F342
# Jadyn Violet / TwinnyTwin Independent Release: 0xA33EdB3810ee9faE9077dAf9AcDD834E1860a72C

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
                        metadata
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
                        metadata
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

    endCursor = df['mints'][1]['endCursor']
    hasNextPage = df['mints'][1]['hasNextPage']

    #print(endCursor)
    #print(hasNextPage)

    node_page = df['mints'][0]

    for i in range(len(node_page)):

        #If token is missing metadata, skip and trigger message
        if (df['mints'][0][i]['token']['metadata']) is None:
            print('Token ID:' + str(TokenTracker + i + 1)+ " is missing!!!!")
            continue

        #Grab metadata tag for each node

        platform = 'Mint Songs'
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

        tempData = [[platform,artist,projectTitle,songTitle,bpm,key,genre,tags,locationCreated,originalReleaseDate,recordLabel,publisher,license, image, losslessAudio, duration]]
        temp_MusicNFT_DF = pd.DataFrame(tempData, columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate','recordLabel','publisher','license', 'image','losslessAudio', 'duration'])

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

#var reset
hasNextPage = True
counter = 0
endCursor = ""
TokenTracker = 0

#Catalog Query
while hasNextPage == True:
    counter = counter + 1

    if counter == 1:
        query_string = """
                query MyQuery {
                mints(pagination: {limit: 50, after: ""}, where: {collectionAddresses: "0x0bC2A24ce568DAd89691116d5B34DEB6C203F342"}) {
                    nodes {
                    mint {
                        collectionAddress
                    }
                    token {
                        metadata
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
                mints(pagination: {limit: 50, after: "%s"}, where: {collectionAddresses: "0x0bC2A24ce568DAd89691116d5B34DEB6C203F342"}) {
                    nodes {
                    mint {
                        collectionAddress
                    }
                    token {
                        metadata
                    }
                    }
                    pageInfo {
                    endCursor
                    hasNextPage
                    }
                }
                }


        """ % endCursor

    # Provide a GraphQL query
    query = gql(query_string)

    # Execute the query on the transport
    result = client.execute(query)
    #print(result)

    df = pd.DataFrame.from_dict(result)

    endCursor = df['mints'][1]['endCursor']
    hasNextPage = df['mints'][1]['hasNextPage']

    #print(endCursor)
    #print(hasNextPage)

    node_page = df['mints'][0]

    for i in range(len(node_page)):

        #If token is missing metadata, skip and trigger message
        if (df['mints'][0][i]['token']['metadata']) is None:
            print('Token ID:' + str(TokenTracker + i + 1)+ " is missing!!!!")
            continue

        #Grab metadata tag for each node

        platform = 'Catalog'
        artist = df['mints'][0][i]['token']['metadata']['attributes']['artist']
        projectTitle = df['mints'][0][i]['token']['metadata']['attributes']['artist']
        songTitle = df['mints'][0][i]['token']['metadata']['title']
        bpm = None
        key = None
        genre = None
        tags = None
        locationCreated = None
        originalReleaseDate = None
        recordLabel = None
        publisher = None
        license = None

        image = df['mints'][0][i]['token']['metadata']['image']
        losslessAudio = df['mints'][0][i]['token']['metadata']['losslessAudio']
        duration = df['mints'][0][i]['token']['metadata']['duration']

        tempData = [[platform,artist,projectTitle,songTitle,bpm,key,genre,tags,locationCreated,originalReleaseDate,recordLabel,publisher,license, image, losslessAudio, duration]]
        temp_MusicNFT_DF = pd.DataFrame(tempData, columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate','recordLabel','publisher','license', 'image','losslessAudio', 'duration'])

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

#var reset
hasNextPage = True
counter = 0
endCursor = ""
TokenTracker = 0

#Jadyn Violet / TwinnyTwin Drop
query_string = """
        query MyQuery {
        mints(pagination: {limit: 50, after: ""}, where: {collectionAddresses: "0xA33EdB3810ee9faE9077dAf9AcDD834E1860a72C"}) {
            nodes {
            mint {
                collectionAddress
            }
            token {
                metadata
            }
            }
            pageInfo {
            endCursor
            hasNextPage
            }
        }
        }


"""

# Provide a GraphQL query
query = gql(query_string)

# Execute the query on the transport
result = client.execute(query)

df = pd.DataFrame.from_dict(result)

platform = 'Jadyn Violet / TwinnyTwin'
artist = df['mints'][0][1]['token']['metadata']['attributes']['Artists']
projectTitle = df['mints'][0][1]['token']['metadata']['attributes']['Song Title']
songTitle = df['mints'][0][1]['token']['metadata']['attributes']['Song Title']
bpm = None
key = None
genre = df['mints'][0][1]['token']['metadata']['attributes']['Genre']
tags = None
locationCreated = df['mints'][0][1]['token']['metadata']['attributes']['Location']
originalReleaseDate = None
recordLabel = None
publisher = None
license = None

image = df['mints'][0][1]['token']['metadata']['image']
losslessAudio = None
duration = None

tempData = [[platform,artist,projectTitle,songTitle,bpm,key,genre,tags,locationCreated,originalReleaseDate,recordLabel,publisher,license, image, losslessAudio, duration]]
temp_MusicNFT_DF = pd.DataFrame(tempData, columns=['platform','artist','project','songTitle','bpm','key','genre','tags','locationCreated','originalReleaseDate','recordLabel','publisher','license', 'image','losslessAudio', 'duration'])

MusicNFT_DF = pd.concat([MusicNFT_DF,temp_MusicNFT_DF])

MusicNFT_DF = MusicNFT_DF.reset_index(drop=True)

#print(MusicNFT_DF)

#Pull Futuretape bm data into dataframe for matching

url = 'https://futuretape.xyz/catalog-genre-bpm-hackathon.json'

header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=header)

FT_DT = pd.read_json(r.text)

#remove null data from dataset

FT_DT2 = FT_DT[FT_DT[['tags', 'bpm', 'token_id']].notnull().all(1)]

#Iterate through Zora API data and cross reference with Futuretape tag and BPM data

for z in range(len(MusicNFT_DF)):
    artistSearchName = MusicNFT_DF.iloc[z]['artist']
    songSearchName = MusicNFT_DF.iloc[z]['songTitle']

    # print(artistSearchName)
    # print(songSearchName)

    Filtered_DF = FT_DT2[FT_DT2['artist'] == artistSearchName]
    Filtered_DF = Filtered_DF[Filtered_DF['title'] == songSearchName]

    if len(Filtered_DF) > 0:

        #print(Filtered_DF)

        bpm = Filtered_DF.iloc[0]['bpm']
        tags = Filtered_DF.iloc[0]['tags']

        #print(bpm)
        #print(tags)

        MusicNFT_DF.iloc[z]['tags'] = str(tags)
        MusicNFT_DF.iloc[z]['bpm'] = str(bpm)

        #print(MusicNFT_DF.at[z,'bpm'])

        #print(tags)
        #print(bpm)

#print(MusicNFT_DF['bpm'])

#Push dataframe to google sheets

sh = gc.open('ZoraAPI - Directory')

MusicNFT_DF_gs = sh[0]

MusicNFT_DF_gs.set_dataframe(MusicNFT_DF,(1,1))