import cv2
from base_camera import BaseCamera

from fps import FPS
from inferencehelper import InferenceHelper
from drawinghelper import DrawingHelper

import logging
import time

logger = logging.getLogger("Camera")

# Starting the FPS thread.
fps = FPS().start()

logger.info("Starting inference thread")
INFERENCE_API = ""
inference_thread = InferenceHelper(INFERENCE_API).start()

logger.info("Starting drawing thread")
drawing_thread = DrawingHelper(1280, 720).start()

class Camera(BaseCamera):
    video_source = 0

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, frame = camera.read()
            # update the FPS counter
            fps.update()
            frame_name = "./output/frame{}.jpg".format(fps.current_frame_number())

            # Queue up a new frame for inference every time the queue is empty.
            # This prevents the inference thread being queued with every single frame
            if inference_thread.queue.empty():
                inference_thread.enqueue({'name': frame_name, 'frame': frame, 'type': 'inference_queued'})

		    # Everytime the inference thread processes a frame it returns the json_resp
		    # This then adds the frame and json_resp to the drawing thread queue.
            drawing_thread.enqueue({'frame': frame, 'json_resp': inference_thread.json_resp})

            if drawing_thread.drawn_frame.size:
                yield cv2.imencode('.jpg', drawing_thread.drawn_frame)[1].tobytes()
            else:
                yield cv2.imencode('.jpg', frame)[1].tobytes()
