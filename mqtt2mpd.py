#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from mpd import MPDClient

sOrt="wc"
iMPDPort=6601

def on_connect(client, userdata, flags, rc):
		print("Connected with result code " + str(rc))
		client.subscribe(sOrt + "/audio/control")


def on_message(client, userdata, msg):
		print(msg.topic + " " + str(msg.payload))

		if msg.topic == sOrt + "/audio/control":
			pass #payload = msg.payload.decode("utf-8")
                        payload=str(msg.payload)

			if str.startswith(payload, "play"):
                                mpdclient.clear()
                                mpdclient.load("swr3")
                                mpdclient.play(0)
                        if str.startswith(payload, "volume:"):
                                mpdclient.setvol(int(payload.split(':')[:-1]))
                        if str.startswith(payload, "consume:"):
				mpdclient.consume(payload[-1])
			if str.startswith(payload, "next"):
				mpdclient.next()
			if str.startswith(payload, "previous"):
				mpdclient.previous()
			if str.startswith(payload, "pause"):
				mpdclient.pause()
			if str.startswith(payload, "stop"):
				mpdclient.stop()
			if str.startswith(payload, "incvol"):
				volume = int(mpdclient.status()['volume'])
				if volume < 100:
					mpdclient.setvol(volume+1)
			if str.startswith(payload, "decvol"):
				volume = int(mpdclient.status()['volume'])
				if volume > 0:
					mpdclient.setvol(volume-1)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.101.240", 1883, 60)
client.loop_start()

mpdclient = MPDClient()
mpdclient.connect("192.168.101.220", iMPDPort)


while True:
		time.sleep(10)
		client.publish("wc/audio/status", str(mpdclient.status()))
		client.publish("wc/audio/currentsong", str(mpdclient.currentsong()))


