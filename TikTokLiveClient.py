import gspread
from typing import List
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent

# Instantiate the client with the user's username
client: TikTokLiveClient = TikTokLiveClient(unique_id="")

sa = gspread.service_account(filename="keys.json")
sh =  sa.open("TikTokLiveTest")

wks = sh.worksheet ("Client Data")


# Define how you want to handle specific events via decorator
@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

#===== Comment Count =====#
count_cmt = 1
async def on_comment(event: CommentEvent):
    print(f"{event.user.nickname} --> {event.comment}")
    global count_cmt 
    count_cmt += 1
    wks.update('A' + str(count_cmt), event.user.nickname)
    wks.update('B' + str(count_cmt), event.comment)
client.add_listener("comment", on_comment)

#===== Viewer Count =====#
@client.on("viewer_count_update")
async def on_connect(event: ViewerCountUpdateEvent):
    print("Received a new viewer count:", event.viewerCount)
    wks.update('G2', event.viewerCount)

#===== Follow Event =====#
count_follow = 1
async def on_follow(event: FollowEvent):
    print(f"{event.user.nickname} ==========> followed the streamer")
    global count_follow
    count_follow += 1
    wks.update('C' + str(count_follow), event.user.nickname)

client.add_listener("follow", on_follow)

#===== Like Event =====#
count_like = 1
async def on_like(event: LikeEvent):
    print(f"{event.user.nickname} ----------> like streamer")
    new_like = event.user.nickname
    global count_like
    
    count_like = count_like + 1
    wks.update('D' + str(count_like), new_like) 

client.add_listener("like", on_like)

#===== Share Event =====#
count_share = 1
async def on_share(event: ShareEvent):
    print(f"{event.user.nickname} ++++++++++> Share streamer")
    global count_share
    count_share += 1
    wks.update('E' + str(count_share), event.user.nickname) 
client.add_listener("share", on_share)

#===== Gife Event =====#
count_gift = 1
@client.on("gift")
async def on_gift(event: GiftEvent):
    global count_gift
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")
        count_gift = count_gift + 1
        wks.update('F' + str(count_gift), event.gift.extended_gift.name) 

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")
        count_gift = count_gift + 1
        wks.update('F' + str(count_gift), event.gift.extended_gift.name) 




if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    client.run()