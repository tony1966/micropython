#main.py
#not applicable for ESP-01 module (no onboard LED)
from machine import Pin,PWM
import network
import time
WAIT_FOR_CONNECT=8

pwm2=PWM(Pin(2), freq=5, duty=512)  

def set_ap():
    html="""
    <!DOCTYPE html>
    <html>
      <head><title>AP Setup</title></head>
      <body>
        %s
      </body>
    </html>
    """
    form="""
        <form method=get action='/update_ap'>
          <table border="0">
            <tr>
              <td>SSID</td>
              <td><input name=ssid type=text></td>
            </tr>
            <tr>
              <td>PWD </td>
              <td><input name=pwd type=text></td>
            </tr>
            <tr>
              <td></td>
              <td align=right><input type=submit value=Connect></td>
            </tr>
          </table>
        </form>
    """
    import socket
    addr=socket.getaddrinfo('192.168.4.1', 80)[0][-1]
    s=socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print('listening on', addr)
    while True:
        cs, addr=s.accept()
        print('client connected from', addr)
        data=cs.recv(1024)        
        request=str(data,'utf8')
        print(request, end='\n')
        if request.find('update_ap?') == 5:
            para=request[request.find('ssid='):request.find(' HTTP/')]
            ssid=para.split('&')[0].split('=')[1]
            pwd=para.split('&')[1].split('=')[1]
            sta.connect(ssid,pwd)
            while not sta.isconnected():
                pass
            print('Connected:IP=',sta.ifconfig()[0])
            cs.send(html % 'Connected:IP=' + sta.ifconfig()[0])
        else:
            cs.send(html % form)
        cs.close()
    s.close()

def get_ip():
  return (network.WLAN(network.STA_IF).ifconfig()[0],
  network.WLAN(network.AP_IF).ifconfig()[0])

def ap_on():
  network.WLAN(network.AP_IF).active(True)

def ap_off():
  network.WLAN(network.AP_IF).active(False)

#try connecting to lastest configured AP
sta=network.WLAN(network.STA_IF)
sta.active(True)
print('Connecting to AP ...')
time.sleep(WAIT_FOR_CONNECT)
if not sta.isconnected():
    set_ap()
else:
    pwm2.deinit()  
    Pin(2).value(0)  
    print('Connected:IP=', sta.ifconfig()[0])
    #Application code is written here or import from a separate file
    import myapp
    myapp.main()
