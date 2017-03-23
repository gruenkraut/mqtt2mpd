#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
from mpd import MPDClient

sOrt0="bad"
iMPDPort0=6600

sOrt1="wc"
iMPDPort1=6601

def on_connect(client, userdata, flags, rc):
		print("Connected with result code " + str(rc))
		client.subscribe(sOrt0 + "/audio/control")
                client.subscribe(sOrt1 + "/audio/control")


def on_message(client, userdata, msg):
		print(msg.topic + " " + str(msg.payload))

		if msg.topic == sOrt0 + "/audio/control":
			pass #payload = msg.payload.decode("utf-8")
                        payload=str(msg.payload)

			if str.startswith(payload, "play"):
                                mpdclient0.clear()
                                mpdclient0.load("swr3")
                                mpdclient0.play(0)
                        if str.startswith(payload, "volume:"):
                                mpdclient0.setvol(int(payload.split(':')[:-1]))
                        if str.startswith(payload, "consume:"):
				mpdclient0.consume(payload[-1])
			if str.startswith(payload, "next"):
				mpdclient0.next()
			if str.startswith(payload, "previous"):
				mpdclient0.previous()
			if str.startswith(payload, "pause"):
				mpdclient0.pause()
			if str.startswith(payload, "stop"):
				mpdclient0.stop()
			if str.startswith(payload, "incvol"):
				volume = int(mpdclient0.status()['volume'])
				if volume < 100:
					mpdclient0.setvol(volume+1)
			if str.startswith(payload, "decvol"):
				volume = int(mpdclient0.status()['volume'])
				if volume > 0:
					mpdclient0.setvol(volume-1)

                if msg.topic == sOrt1 + "/audio/control":
                        pass #payload = msg.payload.decode("utf-8")
                        payload=str(msg.payload)

                        if str.startswith(payload, "play"):
                                mpdclient1.clear()
                                mpdclient1.load("swr3")
                                mpdclient1.play(0)
                        if str.startswith(payload, "volume:"):
                                mpdclient1.setvol(int(payload.split(':')[:-1]))
                        if str.startswith(payload, "consume:"):
                                mpdclient1.consume(payload[-1])
                        if str.startswith(payload, "next"):
                                mpdclient1.next()
                        if str.startswith(payload, "previous"):
                                mpdclient1.previous()
                        if str.startswith(payload, "pause"):
                                mpdclient1.pause()
                        if str.startswith(payload, "stop"):
                                mpdclient1.stop()
                        if str.startswith(payload, "incvol"):
                                volume = int(mpdclient1.status()['volume'])
                                if volume < 100:
                                        mpdclient1.setvol(volume+1)
                        if str.startswith(payload, "decvol"):
                                volume = int(mpdclient1.status()['volume'])
                                if volume > 0:
                                        mpdclient1.setvol(volume-1)



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("dc.home.castle", 1883, 60)
client.loop_start()

mpdclient0 = MPDClient()
mpdclient0.connect("192.168.101.220", iMPDPort0)

mpdclient1 = MPDClient()
mpdclient1.connect("192.168.101.220", iMPDPort1)


while True:
		time.sleep(10)
		client.publish(sOrt1 + "/audio/status", str(mpdclient1.status()))
		client.publish(sOrt1 + "/audio/currentsong", str(mpdclient1.currentsong()))
                client.publish(sOrt0 + "/audio/status", str(mpdclient0.status()))
                client.publish(sOrt0 + "/audio/currentsong", str(mpdclient0.currentsong()))


