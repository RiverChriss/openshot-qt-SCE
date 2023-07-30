import os
import json
import openshot

from classes import info
from classes.image_types import get_media_type
from classes.query import Clip, Track

class Tag() :
    objectPath = os.path.join(info.IMAGES_PATH, "Tag.svg")

    def __init__(self, numeroTrack, colorHex, text, position, end):
        objectOpenShot = openshot.Clip(Tag.objectPath)
        self.object = Clip()
        self.object.data = json.loads(objectOpenShot.Json(), strict=False)
         
         # Add missing info in the json reader
        self.object.data["reader"]["media_type"] = get_media_type(self.object.data["reader"])

        # Update info
        self.object.data["layer"] = numeroTrack
        self.object.data["position"] = position
        self.object.data["end"] = end

        # Make the Clip invisible
        self.object.data["alpha"]["Points"][0]["co"]["Y"] = 0.0
        self.object.data["has_video"]["Points"][0]["co"]["Y"]  = 0.0
        self.object.data["has_audio"]["Points"][0]["co"]["Y"]  = 0.0

        # Add new dicionary for addition info only for Tag
        self.object.data["tag_Object"] = {}
        self.object.data["tag_Object"]["color_hex"] = colorHex
        self.object.data["tag_Object"]["text"] = text


    def save(self):
        self.object.save()
    
    