import os
import cv2

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



# Define input and output paths

image_folder = './image_folder/'  # Replace with the path to your images

video_name = 'video.mp4' # Name of the output video file

video_from_images(video_name,5,image_folder)

