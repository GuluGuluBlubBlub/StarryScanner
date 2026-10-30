import socket #i chose the socket module for this project!
import sys #last minute decision,because I never expected the loop on get_server to not work
import asyncio #so all 65535 ports can be scanned faster!

def get_server(): #input sanitization! 
    for i in range(1): #so the input is checked ONE time
        global target_server #so the target_server variable can be used outside of the loop,for example it is also used when scanning the ports
        target_server=input("\nI want to target..(IP ADDRESSES ONLY)\n"
                    ).strip() #i will release a non-GUI version of the scanner before i reuse this code for the 
                              #tkinter part because tkinter does not allow input()
        try: 
            target_server==socket.inet_aton(target_server) #IPv4 address translated from ASCII to see if the IP is actually real
        except OSError: #OSError occurs when something in the network fails. In this case,the IP address failed because it is not real.
            print('Enter a website or IPv4 address.')
            sys.exit() #exits program

get_server()

print('Scanning open ports..') 

global open_ports
open_ports=[] #to print all ports that are open

max_tasks=2000 #semaphore controls the amount of tasks that run. maximum is 2000!
sem=asyncio.Semaphore(max_tasks)

async def scan_port(port):
    async with sem: #async has to be used,or else await cant be written
        try:
            reader,writer=await asyncio.wait_for(asyncio.open_connection(target_server,port), timeout=0.2) #sends a tcp syn packet to the target,stops after
                                                                                                        #0.2 secs
            print(f'port {port} is open!') #yay!
            open_ports.append(port) #adds that port into the open_ports list to be printed to show all open ports! 
            print('Please be patient. Scanning ports...') #as 65535 ports are scanned,this makes the program less boring than it already is
            writer.close() #reader receives packets. writer sends packets. writer is now closed after scanning all 65535 ports
            await writer.wait_closed() #makes sure writer is closed before moving on
        except (OSError,TimeoutError,ConnectionRefusedError): #if port is closed..
            print(f'Port {port} is not open.')

async def main():
    global scanned_ports
    scanned_ports=[scan_port(port)for port in range(1,65535)] #gathers all scanned ports
    await asyncio.gather(*scanned_ports) #so ports are scanned at the same time instead of one by one

asyncio.run(main()) #RUN THE CODE

print(f'Open ports are {open_ports}') #all open ports are printed!

print("Byebyeee")
