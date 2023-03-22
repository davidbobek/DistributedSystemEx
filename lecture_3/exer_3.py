import aiohttp
import asyncio

#Print the headers of the http response
#Print the body of the http response

def check_http_response(response):
    if response < 100 or response > 599:
        raise Exception("HTTP response code is not valid")

async def main():
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession() as session:
        website_input = input("Enter a website to extract the URL's from: ")
        
        async with session.get(website_input) as response:
            if check_http_response(response.status) == False:
                raise Exception("HTTP response code is not valid")
            #print("Status:", response.status)
            #print("Content-type:", response.headers['content-type'])
            
            #print the headers of the http response
            print("Headers:")
            for header in response.headers:
                print(header,":",response.headers[header])
            
            #print the body of the http response
       
            html = await response.text()
            print("Body:", html, "...")
            
            
            


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
