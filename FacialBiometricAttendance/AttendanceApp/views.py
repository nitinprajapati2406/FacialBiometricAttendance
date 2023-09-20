from django.shortcuts import render, redirect, reverse
from . models import FaceId, Records
import face_recognition
from django.core.files.storage import FileSystemStorage
import os
import os.path
from django.contrib import messages
import json
from itertools import chain
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request,'index.html')

def attendance(request):
    print("Hiiii")
    print(request.FILES.getlist("images[]"))
    if request.method == "POST" and request.FILES.getlist("images[]"):
        # Get the selected group from the form
        selected_group = request.POST.get('group')

        # Remove single quotes around keys and convert to double quotes to make it valid JSON
        selected_group = selected_group.replace("'", "\"")

        # Parse the string as JSON
        data = json.loads(selected_group)

        # Access the value associated with the "group" key
        selected_group = data['group']
    
        # Retrieve all FaceId objects belonging to the selected group
        face_ids = FaceId.objects.filter(group=selected_group)

        # Create a dictionary to store face encodings and names
        known_face_encodings = []
        known_face_names = []

        for face_id in face_ids:
            face_encoding =  face_id.get_face_encodings()
            known_face_encodings.append(face_encoding)
            known_face_names.append(face_id.name)

        # Get the uploaded images
        uploaded_files = request.FILES.getlist('images[]')
        my_path = os.path.abspath(os.path.dirname('FacialBiometricAttendance'))
        # List to store detected names
        detected_names = []

        for uploaded_file in uploaded_files:
            # Process and save each uploaded file
            filename = uploaded_file.name
            print(filename)

            # Save the uploaded file to a temporary location
            fs = FileSystemStorage()
            temp_file = fs.save(filename, uploaded_file)

            # Load the uploaded image using face_recognition
            image_path = os.path.join(my_path,temp_file)
            image = face_recognition.load_image_file(image_path)

            # Get the face locations in the image
            face_locations = face_recognition.face_locations(image)
            
            # Get the face encodings from the image
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Initialize list to store names detected in the image
            names_in_image = []

            # Iterate through the face encodings in the image
            for face_encoding in face_encodings:
                # Compare the face encoding with known face encodings
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.6
                )

                name = ""  # Default name if no match is found

                # If a match is found, use the name of the known face
                if True in matches:
                    match_index = matches.index(True)
                    name = known_face_names[match_index]
                    names_in_image.append(name)

            detected_names.append(names_in_image)

            # Delete the temporary file
            fs.delete(temp_file)
        detected_names = list(chain.from_iterable(detected_names))
        record = Records(attendees='\n'.join(detected_names), group=selected_group, data_time=timezone.now())
        record.save()
        return redirect(reverse('AttendanceApp:result'))
    # If it's a GET request or no images are uploaded
    unique_groups = FaceId.objects.values('group').distinct()
    return render(request, 'attendance.html', locals())


def faceid(request):
    print("inside faceid")
    if request.method == "POST" and request.FILES.getlist("images"):
        print("Got files")
        if request.POST['selectgroup'] != "" and request.POST['inputgroup'] != "":
            return render(request,'faceid.html',{'message':'Either select from the existing class/group or create a new class by providing the name of the new class/group'})

        if request.POST['selectgroup'] == "" and request.POST['inputgroup'] == "":
            return render(request,'faceid.html',{'message':'Either select from the existing class/group or create a new class by providing the name of the new class/group'})
        
        # Get uploaded images
        uploaded_files = request.FILES.getlist('images')
        print(uploaded_files)
        message = ""
        my_path = os.path.abspath(os.path.dirname('FacialBiometricAttendance'))
        print(my_path)
        # Iterate through the uploaded files
        for uploaded_file in uploaded_files:
            # Process and save each uploaded file
            filename = uploaded_file.name
            name = uploaded_file.name.split(".")[0]
            # Save the uploaded file to a temporary location
            fs = FileSystemStorage()
            temp_file = fs.save(filename, uploaded_file)
            
            # Load the uploaded image using face_recognition

            image_path = os.path.join(my_path,temp_file)

            print(image_path)

            image = face_recognition.load_image_file(image_path)
            
            # Get the face encodings from the image
            face_encodings = face_recognition.face_encodings(image)
            print(face_encodings)

            # Check if at least one face encoding is found
            if len(face_encodings) > 0:
                # Assuming you have the 'selectgroup' value for the group name
                group_name = request.POST.get('selectgroup') or request.POST.get('inputgroup')
                
                # Save face encodings, name, and group to the FaceId model
                for face_encoding in face_encodings:
                    face_id = FaceId(name=name, group=group_name)
                    face_id.set_face_encodings(face_encodings=face_encodings)
                    face_id.save()
            else:
                message = message + f"No face detected in {filename}\n"
                print(f"No face detected in {filename}")
            
            # Delete the temporary file
            fs.delete(temp_file)
        message = message + "IDs have been saved"
        messages.success(request, message)
        return redirect(reverse('AttendanceApp:attendance'))
    unique_groups = FaceId.objects.values('group').distinct()
    return render(request,'faceid.html',locals())

def result(request):
    # Retrieve the latest record based on the 'date_time' field
    latest_record = Records.objects.latest('data_time')

    # access the fields of the latest record for a group
    attendees = latest_record.attendees
    group = latest_record.group
    date_time = latest_record.data_time

    return render(request,'result.html',locals())

def record(request):
    if request.method == "POST":
        group = request.POST['group']
        group = request.POST.get('group')

        # Remove single quotes around keys and convert to double quotes to make it valid JSON
        group = group.replace("'", "\"")

        # Parse the string as JSON
        data = json.loads(group)

        # Access the value associated with the "group" key
        group = data['group']
        group_records = Records.objects.filter(group=group)
    unique_groups = FaceId.objects.values('group').distinct()
    return render(request,'records.html', locals())
