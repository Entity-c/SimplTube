import os
import yt_dlp
from pytube import YouTube


def download_audio(url, folder_path):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
    filename = os.path.splitext(filename)[0] + '.mp3'
    return filename


def combine_audio_video(audio_file, video_file, output_file):
    os.system(
        f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -b:a 320k "{output_file}"')


def download_video(url, folder_path):
    options = {
        'format': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160][ext=mp4]',
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
    return filename


def sanitize_filename(filename):
    disallowed_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in disallowed_chars:
        filename = filename.replace(char, '')
    return filename


if __name__ == '__main__':

    video_url = input("Enter the YouTube video URL: ")
    yt = YouTube(video_url)
    video_name = sanitize_filename(yt.title)

    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    folder_path = os.path.join(downloads_folder, video_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    while True:
        try:
            audio_filepath = download_audio(video_url, folder_path)
            print("Audio downloaded successfully.")

            video_filepath = download_video(video_url, folder_path)
            print("Video downloaded successfully.")

            output_filepath = os.path.join(folder_path, f'{video_name}_combined.mp4')
            final_output_filepath = os.path.join(folder_path, f'{video_name}.mp4')
            combine_audio_video(audio_filepath, video_filepath, output_filepath)

            print("Audio and video combined successfully.")
            os.remove(audio_filepath)
            os.remove(video_filepath)
            os.rename(output_filepath, final_output_filepath)
            print("Filepath: ", final_output_filepath)
            os.startfile(final_output_filepath)
            break

        except Exception as e:
            print(f"Error occurred: {e}")
            retry = input("Do you want to try again? (yes/no): ").lower()
            if retry != 'yes':
                break
