import YouTubeMusicAPI

query: str = input()

result = YouTubeMusicAPI.search(query)

if result:
    print(result)
else:
    print("No Result Found")