import streamlit as st
from pytube import YouTube
import tempfile

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="./logo_nphi.png",
    layout="wide",
)

st.markdown("<h1 style='text-align: center; color: red; font-style:italic;'>YouTube Downloader</h1>", unsafe_allow_html=True)

link = st.text_input(label="Paste your link here", placeholder="https://www.youtube.com/..")

# Function for checking if a YouTube link is valid
def is_youtube(link):
    try:
        yt = YouTube(link)
        return yt.streams.filter(only_video=True).first() is not None
    except:
        return False

# Function for searching a key in a dictionary
def key_search(dicti, value):
    closest_resolution = None
    closest_diff = float('inf')
    
    for key, val in dicti.items():
        if val == value:
            return key
        else:
            diff = abs(int(val[:-1]) - int(value[:-1]))
            if diff < closest_diff:
                closest_diff = diff
                closest_resolution = key
    
    if closest_resolution is not None:
        return closest_resolution
    
    raise ValueError(f"Value '{value}' not found in dictionary")

if (is_youtube(link)):
    youtube_1 = YouTube(link)
    title = youtube_1.title
    st.image(youtube_1.thumbnail_url, width=200)
    
    with st.expander("Video Details"):
        st.write(f"Title: {title}")
        st.write(f"Length: {youtube_1.length} seconds")

        # Define list_vid dictionary
        video = [stream for stream in youtube_1.streams if stream.includes_audio_track and stream.includes_video_track]
        list_vid = {}
        for i in range(len(video)):
            resolution = video[i].resolution
            file_size = f"{(video[i].filesize / (1024 * 1024)):.2f} MB" if video[i].filesize else "Unknown"
            list_vid[resolution] = file_size
        st.write("Available Resolutions:")
        for resolution, file_size in list_vid.items():
            st.write(f"Resolution: {resolution} - File Size: {file_size}")

        out = st.selectbox("Select format", ('Audio', 'Video'))

        # Now for audio
        if out == "Audio":
            audio = youtube_1.streams.filter(only_audio=True)
            list_aud = {}
            for i in range(len(audio)):
                list_aud[i] = audio[i].abr
            strm = st.selectbox("Select Quality", (list_aud.values()))

            key_val = key_search(list_aud, strm)
            temp_dir = tempfile.mkdtemp()
            temp_file_path = temp_dir + f"/{title}.mp3"

            if audio[key_val].download(output_path=temp_dir, filename=f'{title}.mp3'):
                st.download_button(
                    label="download",
                    data=open(temp_file_path, 'rb').read(),
                    file_name=f'nphi-{title}.mp3',
                    mime='audio/mp3'
                )

        # For video
        elif out == "Video":
            strm = st.selectbox("Select Quality", [resolution for resolution in list_vid.keys()])
            key_val = key_search(list_vid, strm)
            extension = video[key_val].mime_type.split('/')[1]

            temp_dir = tempfile.mkdtemp()
            temp_file_path = temp_dir + f"/{title}.{extension}"

            if video[key_val].download(output_path=temp_dir, filename=f'{title}.{extension}'):
                st.download_button(
                    label="download",
                    data=open(temp_file_path, 'rb').read(),
                    file_name=f'nphi-{title}.{extension}',
                    mime='video/mp4'
                )

else:
    st.write("Please Enter a Valid Link")


