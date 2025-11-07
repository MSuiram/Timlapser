import os
import cv2
from datetime import timedelta
import numpy as np

def video_from_images(video_name, fps , image_name_folder):

    # Get list of images
    images = [img for img in os.listdir(image_name_folder) if img.endswith(".jpg")]

    # Read the first image to get the size
    first_image = cv2.imread(os.path.join(image_name_folder, images[0]))
    height, width, _ = first_image.shape

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format
    video = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # Add images to the video
    for image in images:
        img_path = os.path.join(image_name_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)

    # Release the video writer
    video.release()
    cv2.destroyAllWindows()

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return (result + ".00").replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s

def creat_img(video_file, SAVING_FRAMES_PER_SECOND, image_folder, index):
    # make a folder by the name of the video file
    if not os.path.isdir(image_folder):
        os.mkdir(image_folder)
    # read the video file    
    cap = cv2.VideoCapture(video_file)
    # get the FPS of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # get the list of duration spots to save
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # start the loop
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # break out of the loop if there are no frames to read
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            # get the earliest duration to save
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration, 
            # then save the frame
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(image_folder, f"frame{index}{frame_duration_formatted}.jpg"), frame) 
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1



# Define input and output paths

videos = [vid for vid in os.listdir("./video/") if vid.endswith(".mp4")]

video_name = 'video.mp4' # Name of the output video file
image_folder, _= os.path.splitext(video_name)
image_folder += "_img_folder"
index = 0

for video in videos:
    print(video)
    video = os.path.join("./video/", video)
    creat_img(video,5,image_folder, index)
    index += 1

video_from_images(video_name,30,image_folder)

