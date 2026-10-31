import socket #i chose the socket module for this project!
import asyncio #faster port scanning so it doesnt take 30+ mins for all 65535 ports

global target_server #how organized,all variables at the top!
target_server=''
open_ports=[]
max_tasks=2000
sem=asyncio.Semaphore(max_tasks) #semaphore controls the amount of tasks that run. maximum is 2000!

async def scan_port(port):
    async with sem: #semaphore controls the amount of tasks that run. maximum is 2000!
        try:
            reader,writer=await asyncio.wait_for(asyncio.open_connection(target_server,port), timeout=0.5) #sends a tcp syn packet to the target,stops after
                                                                                                        #0.5 secs
            print(f'port {port} is open!') #yay!
            open_ports.append(port) #adds that port into the open_ports list to be printed to show all open ports! 
            print('Please be patient. Scanning ports...') #as 65535 ports are scanned,this makes the program less boring than it already is
            writer.close() #reader receives packets. writer sends packets. writer is now closed after scanning all 65535 ports
            await writer.wait_closed() ##makes sure writer is closed before moving on
        except (OSError,TimeoutError,ConnectionRefusedError): #if error uh oh port closed
            print(f'Port {port} is closed.')

async def main():
    global scanned_ports
    scanned_ports=[scan_port(port)for port in range(1,65536)] #gathers all scanned ports
    await asyncio.gather(*scanned_ports) #so ports are scanned at the same time instead of one by one
    print(f'Open ports are {open_ports}') #all open ports are printed!
    print("Byebyeee") #notice how everything is in a function? try running this code,nothing happens on the terminal! this is necessary for the frontend

def scanner(target_server): #input sanitazation
    try:
        socket.inet_atom(target_server) #IPv4 address translated from ASCII to see if the IP is actually real
    except (OSError): #if its valid why oserror
        print('ENTER A VALID IPv4 ADDRESS.')

def everything(chosen_ip): #EVERYTHING PACKED IN ONE FOR ORGANIZED FRONTEND
    global open_ports
    global target_server
    target_server=chosen_ip
    open_ports=[]
    try:
        socket.inet_aton(target_server)
    except (OSError):
        print('ENTER A IPv4 ADDRESS')
        return
    print('Please be patient. Scanning ports...')
    asyncio.run(main())
