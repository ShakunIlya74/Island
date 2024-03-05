from moviepy.editor import VideoFileClip
import os
import matplotlib.pyplot as plt
import shutil
from sql.queries import sql_execute


def get_video_duration(file_path):
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None


def copy_videos_with_categories():
    video_names = sql_execute("""
    SELECT v.file_name
    FROM exercises e
    JOIN videos v ON e.video_id = v.video_id
    WHERE e.default_categories IS NOT NULL;
    """)
    video_names = [v[0] for v in video_names]
    for i,video_name in enumerate(video_names):
        if i % 10 == 0:
            print(f"Processed video {i + 1}/{len(video_names)}: {video_name}")
        source = f"../data/short_videos/all/{video_name}"
        destination = f"../data/app_videos/{video_name}"
        shutil.copyfile(source, destination)



if __name__ == '__main__':
    # get the list of all the video files in a directory
    # directory_path = "../data/short_videos/all"
    # video_files = [f for f in os.listdir(directory_path) if f.endswith('.mp4')]
    # list_of_durations = []
    #
    # search_query = 'band'
    # a = 0
    # for i, video_file in enumerate(video_files):
    #     video_file_path = os.path.join(directory_path, video_file)
    #     if search_query in video_file:
    #         print(video_file)
    #     a += 1
    # print(a)
    #     duration_seconds = get_video_duration(video_file_path)
    #     if duration_seconds is not None:
    #         list_of_durations.append(duration_seconds)
    #         print(f"Processed video {i + 1}/{len(video_files)}: {video_file} : {duration_seconds} seconds")

    # # build a histogram of the durations
    # print(f"List of durations: {list_of_durations}")
    # print(f"Number of videos: {len(list_of_durations)}")
    # print(f"Minimum duration: {min(list_of_durations)}")
    # print(f"Maximum duration: {max(list_of_durations)}")
    # print(f"Average duration: {sum(list_of_durations)/len(list_of_durations)}")
    # print(f"Median duration: {sorted(list_of_durations)[len(list_of_durations)//2]}")

    # build a bar chart of the durations

    # plt.hist(list_of_durations, bins=20)
    # plt.show()

    copy_videos_with_categories()

