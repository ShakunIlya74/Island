from moviepy.editor import VideoFileClip
import os
import matplotlib.pyplot as plt


def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == '__main__':
    # get the list of all the video files in a directory
    directory_path = "../data/short_videos/all"
    video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
    list_of_durations = []
    for i, video_file in enumerate(video_files):

        video_file_path = os.path.join(directory_path, video_file)
        duration_seconds = get_video_duration(video_file_path)
        if duration_seconds is not None:
            list_of_durations.append(duration_seconds)
            print(f"Processed video {i + 1}/{len(video_files)}: {video_file} : {duration_seconds} seconds")
    # build a histogram of the durations
    print(f"List of durations: {list_of_durations}")
    print(f"Number of videos: {len(list_of_durations)}")
    print(f"Minimum duration: {min(list_of_durations)}")
    print(f"Maximum duration: {max(list_of_durations)}")
    print(f"Average duration: {sum(list_of_durations)/len(list_of_durations)}")
    print(f"Median duration: {sorted(list_of_durations)[len(list_of_durations)//2]}")
    # build a bar chart of the durations

    plt.hist(list_of_durations, bins=20)
    plt.show()

