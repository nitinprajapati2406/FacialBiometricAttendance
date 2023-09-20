from django.db import models
import json
import numpy as np

# Create your models here.
class FaceId(models.Model):
    faceid = models.JSONField()
    name = models.CharField(max_length=50)
    group = models.CharField(max_length=50)

    def set_face_encodings(self, face_encodings):
        # Serialize the numpy array(s) to JSON and store them in the field
        self.faceid = json.dumps(face_encodings[0].tolist())

    def get_face_encodings(self):
        # Deserialize the JSON data and convert it back to numpy array(s)
        if self.faceid:
            # return np.array(json.loads(self.faceid))
            return json.loads(self.faceid)
        return None
    
class Records(models.Model):
    attendees = models.TextField()
    data_time = models.DateTimeField()
    group = models.CharField(max_length=50)
    




