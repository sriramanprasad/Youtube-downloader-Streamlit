import streamlit as st
from pytube import YouTube
import os
import re

directory = 'downloads/'
if not os.path.exists(directory):
    os.makedirs(directory)

st.set_page_config(page_title="YTD", page_icon="🚀", layout="wide", )

@st.cache(allow_output_mutation=True)
def get_info(url):
    yt = YouTube(url)
    streams = yt.streams.filter(progressive=True, type='video')
    details = {}
    details["image"] = yt.thumbnail_url
    details["streams"] = streams
    details["title"] = yt.title
    details["length"] = yt.length
    itag, resolutions = ([] for i in range(2))
    for i in streams:
        res = re.search(r'(\d+)p', str(i))
        tag = re.search(r'(\d+)', str(i))
        itag.append(str(i)[tag.start():tag.end()])
        resolutions.append(str(i)[res.start():res.end()])
    details["resolutions"] = resolutions
    details["itag"] = itag
    return details

st.title("YouTube Downloader 🚀")
st.write(":red[NO ADS only fast downloading...]")
url = st.text_input("Paste URL here 👇", placeholder='https://www.youtube.com/')
if url:
    v_info = get_info(url)
    col1, col2 = st.columns([1, 1.5], gap="small")
    with st.container():
        with col1:
            st.image(v_info["image"])
        with col2:
            st.subheader("Video Details ⚙️")
            st.write(f"__Title:__ {v_info['title']}")
            st.write(f"__Length:__ {v_info['length']} sec")
            st.write("__Available Resolutions:__")
            for resolution in v_info["resolutions"]:
                id = v_info["resolutions"].index(resolution)
                if st.button(f"- Resolution: {resolution}"):
                    st.write(f"__Resolution:__ {resolution}")
                    st.write(f"__Size:__ {v_info['streams'][id].filesize / 1000000:.2f} MB")
                    st.write(f"__Format:__ {v_info['streams'][id].mime_type}")
                    file_name = st.text_input('__Save as 🎯__', placeholder=v_info['title'])
                    if file_name:
                        if file_name != v_info['title']:
                            file_name += ".mp4"
                    else:
                        file_name = v_info['title'] + ".mp4"
                    button = st.button("Download ⚡️")
                    if button:
                        with st.spinner('Downloading...'):
                            try:
                                ds = v_info["streams"].get_by_itag(v_info['itag'][id])
                                ds.download(filename=file_name, output_path="downloads/")
                                st.success('Download Complete', icon="✅")
                                st.balloons()
                            except:
                                st.error('Error: Save with a different name!', icon="🚨")


st.markdown("""
DONE by **:green[YUKESH G SRIRAMAN PRASAD]**
AS A PART OF FINAL YEAR PROJECT 
""")
