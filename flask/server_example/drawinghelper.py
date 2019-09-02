# import the necessary packages
import os
import time
from threading import Thread
import requests
import json

import numpy as np
import logging
import cv2
import queue

logger = logging.getLogger("DrawingHelper")

class DrawingHelper:
    """ Manages the drawing on screen using the inferenced frames. """
    def __init__(self, VID_HEIGHT, VID_WIDTH):
        
        # Thread management and queueing
        self.stopped = False
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.queue = queue.Queue()
        self.drawn_frame = np.array([])

        # Video dimensions
        self.VID_HEIGHT = VID_HEIGHT
        self.VID_WIDTH = VID_WIDTH

        # Drawing constants
        # Possibly replace with a namespace?
        self.BB_COLOUR = (255, 98, 0)   # IBM blue 
        self.BB_THICKNESS = 3

        # Letter tracking constants
        # NOTE: Alot of these values are chosen through trial and error for
        # a nice looking visual effect. Do not read too much into the values.
        self.FRAME_THRESHOLD = 12  # This should be an even number.

    def start(self):
        # start the thread to read frames from the queue
        self.thread.start()
        return self

    def enqueue(self, item):
        self.queue.put_nowait(item)

    def update(self):
        try:
            # keep looping infinitely until the thread is stopped
            while True:
                # if the thread indicator variable is set, stop the thread
                if self.stopped:
                    return

                try:
                    inferred_frame = self.queue.get(block=True)
                    json_resp = inferred_frame['json_resp']
                    frame_data = inferred_frame['frame']

                    if not json_resp:
                        json_resp = [{'xmin': 0, 'ymin': 0, 'xmax': 0, 'ymax': 0, 'confidence': 0, 'label': ''}]

                    self.draw_bounding_box(json_resp, frame_data)
                    self.drawn_frame = frame_data

                except queue.Empty:
                    logger.debug("Slept and nothing to do... Trying again.")
                    time.sleep(1)
                    continue

        except Exception as e:
            logger.error("Exception occurred = {}".format(e))

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

    def draw_bounding_box(self, json_resp, image):
        x_max = json_resp[0]['xmax']
        y_max = json_resp[0]['ymax']

        x_min = json_resp[0]['xmin']
        y_min = json_resp[0]['ymin']

        cv2.rectangle(image, (x_max,y_max), (x_min, y_min), self.BB_COLOUR, self.BB_THICKNESS)
